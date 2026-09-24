"""
Constrain probe ports by their Kubernetes destination while preserving inactive inputs.
"""

import copy
import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import find, settings
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.kubernetes.resources import destination


@pytest.mark.parametrize("action", ["tcpSocket", "httpGet"])
@pytest.mark.parametrize("probe", ["livenessProbe", "readinessProbe", "startupProbe"])
def test_probe_port_catalog_boundaries(action: str, probe: str) -> None:
    """
    Preserve numeric ports and named ports across every probe destination.

    Args:
        action (str): Probe handler with a numeric or named port.
        probe (str): Container probe containing the handler.

    Returns:
        None: Invalid names and out-of-range numbers fail without constraining unrelated strings.
    """
    for identity, prefix in (("v1/Pod", ("spec",)), ("apps/v1/DaemonSet", ("spec", "template", "spec"))):
        result = destination(identity, (*prefix, "containers", "*", probe, action, "port"))
        assert result is not None
        schema, _ = result
        validator = validators.validator_for(schema)(schema)
        for value in (1, 65535, "http", "http-2", "1-http", "a" * 15):
            assert validator.is_valid(value), value
        for invalid in (0, -1, 65536, 1.5, None, True, "", "123", "HTTP", "a--b", "-http", "http-", "a" * 16, "http\n", "I\n&"):
            assert not validator.is_valid(invalid), invalid


@pytest.mark.parametrize("action", ["tcpSocket", "httpGet"])
def test_probe_mapping_and_shrinking_use_port_domain(tmp_path: Path, action: str) -> None:
    """
    Carry port constraints into generated inputs and shrinking without a chart-name rule.

    Args:
        tmp_path (Path): Isolated chart using an arbitrary values path.
        action (str): Kubernetes handler selected by the fixture.

    Returns:
        None: Enabled probes reject malformed ports, inactive fields remain available, and valid ports render.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "probe-example", "version": "1.0.0"}))
    defaults = {"enabled": True, "endpoint": "http", "notes": "I\n&"}
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["enabled", "endpoint", "notes"],
        "properties": {"enabled": {"type": "boolean"}, "endpoint": {"type": ["integer", "string"]}, "notes": {"type": "string"}},
    }
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "values.schema.json").write_text(json.dumps(schema))
    (tmp_path / "templates/pod.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: Pod
        metadata:
          name: example
        spec:
          containers:
            - name: app
              image: example
              ports:
                - name: http
                  containerPort: 8080
              {{- if .Values.enabled }}
              livenessProbe:
                ACTION:
                  port: {{ .Values.endpoint }}
              {{- end }}
        """).replace("ACTION", action)
    )
    chart = Chart.load(tmp_path)
    restricted = chart.generation_schema()
    validator = validators.validator_for(restricted)(restricted)
    assert validator.is_valid(json_value(defaults))
    for value in ("I\n&", "'", "http--api", 0, 65536):
        assert not validator.is_valid(json_value({**defaults, "endpoint": value}))
        assert validator.is_valid(json_value({**defaults, "enabled": False, "endpoint": value}))
    domain = destination("v1/Pod", ("spec", "containers", "*", "livenessProbe", action, "port"))
    assert domain is not None
    port_validator = validators.validator_for(domain[0])(domain[0])

    def acceptable(values: dict[str, object]) -> bool:
        """
        Check each generated or shrinking candidate against the destination contract.

        Args:
            values (dict[str, object]): Candidate document produced by Hypothesis.

        Returns:
            bool: Whether the candidate exercises a named port on the enabled branch.
        """
        if values["enabled"]:
            assert port_validator.is_valid(json_value(values["endpoint"]))
        return values["enabled"] is True and isinstance(values["endpoint"], str)

    smallest = find(chart.strategy(), acceptable, settings=settings(max_examples=100, deadline=None, database=None))
    assert port_validator.is_valid(json_value(smallest["endpoint"]))
    assert chart.defaults == defaults
    assert chart.schema == schema
    if shutil.which("helm"):
        for value in (1, 65535, "http"):
            resources = render(chart, {"endpoint": value})
            container = mapping(sequence(mapping(resources[0]["spec"])["containers"])[0])
            assert mapping(mapping(container["livenessProbe"])[action])["port"] == value


@pytest.mark.integration
def test_fluentd_recorded_probe_input_is_excluded(tmp_path: Path) -> None:
    """
    Verify the reported input against source-derived Fluentd destinations.

    Args:
        tmp_path (Path): Private copy of the pinned chart and its common dependency.

    Returns:
        None: The active port rejects the recorded string while the disabled probe retains its input space.
    """
    from hypothesis_helm.tests import PROJECT_ROOT

    source = PROJECT_ROOT / "third_party/bitnami-charts/bitnami"
    if not all((source / name / "Chart.yaml").is_file() for name in ("fluentd", "common")):
        pytest.skip("requires the pinned Bitnami submodule")
    target = tmp_path / "chart"
    shutil.copytree(source / "fluentd", target, ignore=shutil.ignore_patterns("charts"))
    shutil.copytree(source / "common", target / "charts/common")
    chart = Chart(target, {"type": "object"}, mapping(yamlio.load((target / "values.yaml").read_text())))
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value(chart.defaults))
    candidate = copy.deepcopy(chart.defaults)
    probe = mapping(mapping(candidate["forwarder"])["livenessProbe"])
    mapping(probe["tcpSocket"])["port"] = "I\n&"
    assert not validator.is_valid(json_value(candidate))
    probe["enabled"] = False
    assert validator.is_valid(json_value(candidate))
