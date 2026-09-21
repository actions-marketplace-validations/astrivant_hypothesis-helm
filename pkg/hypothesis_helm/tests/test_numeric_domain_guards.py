"""
Check numeric activation regions and the string-returning boundary of Helm helpers.
"""

import copy
import json
import operator
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.projections import Input, Operation
from hypothesis_helm.compiler.passes.domain_constraints import guard_bounds
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import json_value, mapping
from hypothesis_helm.tests.test_input_domains import fixture_chart


@pytest.mark.parametrize("conversion", ["int", "int64"])
@pytest.mark.parametrize("comparison", ["gt", "ge", "lt", "le", "eq", "ne"])
@pytest.mark.parametrize("reversed_operands", [False, True])
def test_numeric_bounds_leave_unsupported_conversions_unknown(conversion: str, comparison: str, reversed_operands: bool) -> None:
    """
    Check both logical regions while keeping unsupported types and magnitudes outside either region.

    Args:
        conversion (str): Explicit Helm integer conversion.
        comparison (str): Numeric comparator applied after conversion.
        reversed_operands (bool): Place the converted input on the right of the comparison.

    Returns:
        None: True and false bounds are disjoint and agree throughout the supported input region.
    """
    converted = Operation(conversion, (Input(("count",)),))
    expression = Operation(comparison, (2, converted) if reversed_operands else (converted, 2))
    yes, no = guard_bounds(expression)
    positive, negative = (validators.validator_for(schema)(schema) for schema in (yes, no))
    compare = getattr(operator, comparison)
    for count in (-(2**31), -1, 0, 1, 2, 3, 2**31 - 1):
        expected = compare(2, count) if reversed_operands else compare(count, 2)
        assert positive.is_valid({"count": count}) == expected
        assert negative.is_valid({"count": count}) == (not expected)
    unsupported_values: tuple[object, ...] = (None, True, False, "2", "bad", [], {}, 1.5, 2**63, -(2**63))
    for unsupported in unsupported_values:
        assert not positive.is_valid(json_value({"count": unsupported}))
        assert not negative.is_valid(json_value({"count": unsupported}))
    assert not positive.is_valid({}) and not negative.is_valid({})


@pytest.mark.parametrize("otherwise", ["", "{{ false }}", "false"])
def test_helper_activation_tracks_rendered_text_not_boolean_truth(tmp_path: Path, otherwise: str) -> None:
    """
    Preserve empty helper output while treating the rendered word false as nonempty text.

    Args:
        tmp_path (Path): Fixture with a helper-gated Pod.
        otherwise (str): Helper output when its numeric condition is false.

    Returns:
        None: Input constraints activate exactly in the established nonempty output regions.
    """
    chart = fixture_chart(tmp_path)
    mapping(chart.schema["properties"])["count"] = {}
    chart.defaults["count"] = 1
    (tmp_path / "values.schema.json").write_text(json.dumps(chart.schema))
    (tmp_path / "values.yaml").write_text(yamlio.dump(chart.defaults))
    (tmp_path / "templates/_helpers.tpl").write_text(
        '{{ define "enabled" }}{{ if gt (int .Values.count) 0 }}{{ true }}{{ else }}' + otherwise + "{{ end }}{{ end }}"
    )
    template = tmp_path / "templates/pod.yaml"
    template.write_text('{{ if include "enabled" . }}\n' + template.read_text() + "{{ end }}\n")
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    for count in (-1, 0, 1, 2):
        candidate = {**chart.defaults, "count": count, "port": 0}
        assert validator.is_valid(json_value(candidate)) == (count <= 0 and not otherwise)
    if not otherwise:
        for unsupported in ("1", "invalid", 1.5, 2**63):
            assert validator.is_valid(json_value({**chart.defaults, "count": unsupported, "port": 0}))


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_elasticsearch_pdb_numeric_helper_and_native_render(tmp_path: Path) -> None:
    """
    Reproduce the scan's PDB failure and enforce its destination only when the helper enables the resource.

    Args:
        tmp_path (Path): Isolated Elasticsearch chart with local dependencies.

    Returns:
        None: Malformed active limits are excluded while disabled configurations and valid limits remain eligible.
    """
    source = Path(__file__).resolve().parents[3] / "third_party/bitnami-charts/bitnami"
    if not all((source / name / "Chart.yaml").is_file() for name in ("elasticsearch", "kibana", "common")):
        pytest.skip("requires the pinned Bitnami submodule")
    target = tmp_path / "elasticsearch"
    shutil.copytree(source / "elasticsearch", target, ignore=shutil.ignore_patterns("charts"))
    for name in ("kibana", "common"):
        shutil.copytree(source / name, target / "charts" / name, ignore=shutil.ignore_patterns("charts"))
    shutil.copytree(source / "common", target / "charts/kibana/charts/common")
    chart = Chart(target, {"type": "object"}, mapping(yamlio.load((target / "values.yaml").read_text())))
    with pytest.raises(RenderFailure) as error:
        render(chart, {"master": {"pdb": {"minAvailable": "[Ma"}}})
    assert error.value.code == "HH1101"
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    for count, autoscaling in ((0, False), (1, False), (0, True)):
        candidate = copy.deepcopy(chart.defaults)
        master = mapping(candidate["master"])
        master["replicaCount"] = count
        mapping(master["autoscaling"])["enabled"] = autoscaling
        mapping(master["pdb"])["minAvailable"] = "[Ma"
        assert validator.is_valid(json_value(candidate)) == (count == 0 and not autoscaling)
    assert render(chart, {"master": {"pdb": {"minAvailable": "50%"}}})


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_native_helm_agrees_with_supported_numeric_regions(tmp_path: Path) -> None:
    """
    Check comparison guards against Helm at zero, negative counts and integer boundaries.

    Args:
        tmp_path (Path): Chart rendering a matrix of numeric comparison results.

    Returns:
        None: Every asserted guard agrees with native Helm; unsupported conversions assert neither result.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "numbers", "version": "1.0.0"}))
    samples: list[object] = [-(2**31), -1, 0, 2, 3, 2**31 - 1, 2**53 - 1, "3", "bad", 1.5]
    values = {f"v{index}": sample for index, sample in enumerate(samples)}
    (tmp_path / "values.yaml").write_text(yamlio.dump(values))
    lines = []
    for conversion in ("int", "int64"):
        for comparison in ("gt", "ge", "lt", "le", "eq", "ne"):
            for index in range(len(samples)):
                call = f"{comparison} ({conversion} .Values.v{index}) 2"
                lines.append(f"  {conversion}_{comparison}_{index}: {{{{ {call} | quote }}}}\n")
    (tmp_path / "templates/result.yaml").write_text(
        dedent("""
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: numbers
            data:
            """)
        + "".join(lines)
    )
    observed = mapping(render(Chart(tmp_path, {"type": "object"}, dict(values)), {})[0]["data"])
    for conversion in ("int", "int64"):
        for comparison in ("gt", "ge", "lt", "le", "eq", "ne"):
            expression = Operation(comparison, (Operation(conversion, (Input(("count",)),)), 2))
            for bound, expected in zip(guard_bounds(expression), ("true", "false"), strict=True):
                validator = validators.validator_for(bound)(bound)
                for index, sample in enumerate(samples):
                    if validator.is_valid(json_value({"count": sample})):
                        assert observed[f"{conversion}_{comparison}_{index}"] == expected
