"""
Check transformation semantics and guarded preimage guidance against native Helm.
"""

import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import strategies as st

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.rendering import RenderFailure, render
from hypothesis_helm.charts.runner import check_chart
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.passes.rejections import RejectionPolicy, matches_rejection
from hypothesis_helm.schemas.contracts import mapping


@pytest.fixture
def transformed_chart(tmp_path: Path) -> Chart:
    """
    Create a minimal chart whose notes can reject transformed inputs independently of its manifest.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        Chart: Inferred inputs with valid baseline resource output.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "transforms", "version": "1.0.0"}))
    defaults: dict[str, object] = {"text": " SMALL ", "other": "", "count": 2, "enabled": True}
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: transformations
        data:
          text: {{ .Values.text | quote }}
        """)
    )
    return Chart(tmp_path, {"type": "object"}, defaults)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    ("predicate", "overrides"),
    [
        ('eq (lower .Values.text) " small "', {}),
        ('eq (.Values.text | trim | upper) "SMALL"', {}),
        ('eq (trimPrefix " " .Values.text) "SMALL "', {}),
        ('eq (trimSuffix " " .Values.text) " SMALL"', {}),
        ('eq (trimAll "xy" .Values.text) "ab"', {"text": "xyabxy"}),
        ('eq (trimAll "" .Values.text) "xy"', {"text": "xy"}),
        ('eq (replace "x" "y" .Values.text) "yy"', {"text": "xx"}),
        ('eq (replace "" "-" .Values.text) "-a-b-"', {"text": "ab"}),
        ('contains "MA" .Values.text', {}),
        ('hasPrefix " SM" .Values.text', {}),
        ('hasSuffix "LL " .Values.text', {}),
        ('eq (default "backup" .Values.other) "backup"', {}),
        ('eq (default "backup" .Values.other) "backup"', {"other": False}),
        ('eq (default "backup" .Values.other) "backup"', {"other": 0}),
        ('eq (default "backup" .Values.other) "backup"', {"other": []}),
        ('eq (default "backup" .Values.other) "backup"', {"other": {}}),
        ('eq (default "backup" .Values.missing) "backup"', {}),
        ('eq (coalesce .Values.other .Values.text "backup") " SMALL "', {}),
        ('eq (coalesce .Values.missing .Values.other "backup") "backup"', {}),
        ("empty (coalesce .Values.other false)", {}),
        ("eq (add .Values.count 3 4) 9", {}),
        ("eq (add1 .Values.count) 3", {}),
        ("eq (.Values.count | sub 10) 8", {}),
        ("eq (mul .Values.count 3 4) 24", {}),
        ("eq (min .Values.count 5) 2", {}),
        ("eq (max .Values.count 5) 5", {}),
        ('eq (toString .Values.enabled) "true"', {}),
        ('eq (toString .Values.count) "2"', {}),
        ("eq (atoi .Values.text) 8", {"text": "08"}),
        ("eq (atoi .Values.text) 12", {"text": "+12"}),
        ("eq (atoi .Values.text) 0", {"text": "wrong"}),
        ("eq (atoi .Values.text) 0", {"text": " 2 "}),
        ('regexMatch "^[A-Z ]+$" .Values.text', {}),
        ('mustRegexMatch "SMALL" .Values.text', {}),
        ('regexMatch "^[a-z][a-z0-9-]{0,62}$" .Values.text', {"text": "hello-2"}),
        ('not (regexMatch "^small$" .Values.text)', {"text": "small\n"}),
        ('regexMatch "^a.b$" .Values.text', {"text": "a\rb"}),
        ('regexMatch "^a[0-9]{2}$" .Values.text', {"text": "a12"}),
        ("regexMatch `^a\\.b$` .Values.text", {"text": "a.b"}),
    ],
)
def test_transformations_match_helm(transformed_chart: Chart, predicate: str, overrides: dict[str, object]) -> None:
    """
    Check rejecting and nonrejecting branches with the actual Sprig implementation.

    Args:
        transformed_chart (Chart): Renderable fixture.
        predicate (str): Supported expression expected to evaluate to true.
        overrides (dict[str, object]): Input-specific test values.

    Returns:
        None: Compiler and Helm agree on both the predicate and its negation.
    """
    note = transformed_chart.path / "templates/NOTES.txt"
    values = {**transformed_chart.defaults, **overrides}
    for condition, rejected in ((predicate, True), (f"not ({predicate})", False)):
        note.write_text("{{ if " + condition + ' }}{{ fail "transform rejected" }}{{ end }}')
        rejection = Contracts.build(transformed_chart.path).predict(values)
        assert (rejection is not None) is rejected
        if rejected:
            assert rejection is not None and rejection.transformed
            with pytest.raises(RenderFailure) as failure:
                render(transformed_chart, overrides)
            assert matches_rejection(str(failure.value), rejection)
        else:
            render(transformed_chart, overrides)


def test_transformed_allowlist_retains_full_input_space(transformed_chart: Chart) -> None:
    """
    Keep normalized aliases and fallbacks eligible without publishing them as a raw enum.

    Args:
        transformed_chart (Chart): Chart with replaceable validation notes.

    Returns:
        None: Case variants, whitespace variants, and empty fallbacks remain valid configurations.
    """
    (transformed_chart.path / "templates/NOTES.txt").write_text(
        dedent("""
        {{ $mode := .Values.text | trim | lower | default "small" }}
        {{ if .Values.enabled }}
          {{ if not (hasKey (dict "small" true "large" true) $mode) }}{{ fail "invalid mode" }}{{ end }}
        {{ end }}
        """)
    )
    contracts = Contracts.build(transformed_chart.path)
    for text in ("small", "SMALL", " Small ", "LARGE", "", "  "):
        assert contracts.predict({**transformed_chart.defaults, "text": text}) is None
    assert contracts.predict({**transformed_chart.defaults, "text": "wrong", "enabled": False}) is None
    rejected = {**transformed_chart.defaults, "text": "wrong"}
    rejection = contracts.predict(rejected)
    assert rejection is not None and not rejection.enums
    assert len(rejection.transformed_domains) == 1
    domain = rejection.transformed_domains[0]
    assert set(domain.suggestions()["$.text"]) == {"small", "large"}
    evidence = domain.report()
    assert evidence["allowed_outputs"] == ["large", "small"]
    assert mapping(evidence["expression"])["function"] == "default"
    json.dumps(rejection.report())
    policy = RejectionPolicy(contracts, transformed_chart.defaults)
    policy.verified(rejection, rejected)
    policy.verified(rejection, {**rejected, "text": "also-wrong"})
    assert policy.needs_probe(rejection, rejected)
    repaired = policy.repair(rejected, rejection, (("text",),), lambda candidate: contracts.predict(candidate) is None)
    assert repaired is not None and repaired["text"] == "wrong" and repaired["enabled"] is False


@pytest.mark.parametrize(
    ("expression", "outputs", "field", "expected"),
    [
        ('trimPrefix "prefix-" .Values.text', '"small"', "text", "small"),
        ('replace "_" "-" .Values.text', '"small-name"', "text", "small-name"),
        ("upper .Values.text", '"SMALL"', "text", "SMALL"),
        ("coalesce .Values.other .Values.text", '"small"', "other", "small"),
        ("toString (add .Values.count 3)", '"8"', "count", 5),
        ("toString (mul .Values.count 3)", '"15"', "count", 5),
        ("toString (sub 10 .Values.count)", '"5"', "count", 5),
        ("toString (atoi .Values.text)", '"8"', "text", "8"),
    ],
)
def test_preimages_are_verified_in_source_space(
    transformed_chart: Chart, expression: str, outputs: str, field: str, expected: object
) -> None:
    """
    Solve supported compositions backwards and check each proposal forwards before use.

    Args:
        transformed_chart (Chart): Chart providing original input types.
        expression (str): Transformation passed into an authored allowlist.
        outputs (str): Go-template literal allowlist entries.
        field (str): Source field expected to receive a valid proposal.
        expected (object): A source value producing an accepted output.

    Returns:
        None: Proposals refer to inputs rather than copying output spellings into the values file.
    """
    (transformed_chart.path / "templates/NOTES.txt").write_text(
        "{{ if not (has (" + expression + ") (list " + outputs + ')) }}{{ fail "transformed allowlist" }}{{ end }}'
    )
    contracts = Contracts.build(transformed_chart.path)
    rejection = contracts.predict(transformed_chart.defaults)
    assert rejection is not None and not rejection.enums
    suggestions = rejection.transformed_domains[0].suggestions()
    assert expected in suggestions["$." + field]
    for path, proposals in suggestions.items():
        for proposal in proposals:
            assert contracts.predict({**transformed_chart.defaults, path.removeprefix("$."): proposal}) is None


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_generation_uses_preimages_and_preserves_schema_conflicts(transformed_chart: Chart) -> None:
    """
    Verify rejected witnesses with Helm, test replacements, and retain contradictions with authored schemas.

    Args:
        transformed_chart (Chart): Inferred chart with a normalized allowlist.

    Returns:
        None: Sampled generation can be repaired, finite assignments and authored schemas cannot be silently changed.
    """
    (transformed_chart.path / "templates/NOTES.txt").write_text(
        dedent("""
        {{ if not (has (.Values.text | trim | lower) (list "small" "large")) }}{{ fail "invalid mode" }}{{ end }}
        """)
    )
    invalid = {**transformed_chart.defaults, "text": "wrong"}
    report = check_chart(
        transformed_chart, input_strategy=st.just(invalid), max_examples=1, filter_rejections=True, protected_paths=(("text",),)
    )
    assert report["status"] == "passed", report
    evidence = mapping(report["configuration_rejections"])
    assert evidence["verification_renders"] == evidence["adjusted_candidates"] == 1
    finite_chart = Chart(transformed_chart.path, {"enum": [transformed_chart.defaults, invalid]}, transformed_chart.defaults)
    exhaustive = check_chart(finite_chart, exhaustive=True, filter_rejections=True)
    assert mapping(exhaustive["configuration_rejections"])["adjusted_candidates"] == 0
    assert mapping(exhaustive["configuration_rejections"])["filtered_candidates"] == 1
    schema: dict[str, object] = {"type": "object", "properties": {"text": {"type": "string"}}}
    (transformed_chart.path / "values.schema.json").write_text(json.dumps(schema))
    declared_chart = Chart(transformed_chart.path, schema, transformed_chart.defaults)
    rejection = Contracts.build(transformed_chart.path).predict(invalid)
    assert rejection is not None and rejection.declared_schema
    assert rejection.transformed_domains
    conflict = check_chart(declared_chart, input_strategy=st.just(invalid), max_examples=1, filter_rejections=True)
    assert conflict["status"] == "failed"
    assert int(str(mapping(conflict["configuration_rejections"])["schema_conflicts"])) >= 1


@pytest.mark.parametrize(
    "expression",
    [
        'upper "ß"',
        'trim "\\u0085"',
        'add "2" 1',
        'atoi "9223372036854775808"',
        "add 9223372036854775807 1",
        "sub -9223372036854775808 1",
        "mul 9223372036854775807 2",
        'regexMatch "(?=a)" "a"',
        'regexMatch "a*a*" "a"',
        'regexMatch "[[:alpha:]]" "a"',
        'regexMatch `\\d` "1"',
        'regexMatch "a{1001}" "a"',
        'regexMatch "a{01}" "a"',
    ],
)
def test_unsupported_semantics_do_not_authorize_filtering(transformed_chart: Chart, expression: str) -> None:
    """
    Refuse Python-specific Unicode, coercion, overflow and regular-expression assumptions.

    Args:
        transformed_chart (Chart): Chart containing an otherwise reachable rejection.
        expression (str): Operation outside the implemented semantic subset.

    Returns:
        None: The compiler cannot exclude a candidate by guessing what the renderer would do.
    """
    (transformed_chart.path / "templates/NOTES.txt").write_text(
        "{{ $value := " + expression + ' }}{{ if $value }}{{ fail "unsafe prediction" }}{{ else }}{{ fail "unsafe too" }}{{ end }}'
    )
    assert Contracts.build(transformed_chart.path).predict(transformed_chart.defaults) is None


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_fallback_arguments_are_eager(transformed_chart: Chart) -> None:
    """
    Preserve errors in unselected default arguments rather than treating Sprig calls as short-circuit operators.

    Args:
        transformed_chart (Chart): Chart with a nonempty text value.

    Returns:
        None: Both the compiler and native renderer observe the eagerly evaluated failure.
    """
    (transformed_chart.path / "templates/NOTES.txt").write_text('{{ default (fail "eager argument") .Values.text }}')
    rejection = Contracts.build(transformed_chart.path).predict(transformed_chart.defaults)
    assert rejection is not None
    with pytest.raises(RenderFailure) as failure:
        render(transformed_chart, {})
    assert matches_rejection(str(failure.value), rejection)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_helper_provenance_and_partial_schema(transformed_chart: Chart) -> None:
    """
    Retain transformed input origins through helper dictionaries and partial schemas.

    Args:
        transformed_chart (Chart): Fixture with an inferred text field and declared unrelated Boolean.

    Returns:
        None: Guidance targets the caller's field while accepted aliases remain real Helm successes.
    """
    (transformed_chart.path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{ define "validate.mode" }}
          {{ if not (hasKey (dict "small" true "large" true) .nested.mode) }}{{ fail "helper mode" }}{{ end }}
        {{ end }}
        """)
    )
    (transformed_chart.path / "templates/NOTES.txt").write_text(
        '{{ include "validate.mode" (dict "nested" (dict "mode" (.Values.text | trim | lower))) }}'
    )
    (transformed_chart.path / "values.schema.json").write_text(
        json.dumps({"type": "object", "properties": {"enabled": {"type": "boolean"}}})
    )
    contracts = Contracts.build(transformed_chart.path)
    for text in ("SMALL", " small ", "LARGE"):
        assert contracts.predict({**transformed_chart.defaults, "text": text}) is None
        render(transformed_chart, {"text": text})
    rejection = contracts.predict({**transformed_chart.defaults, "text": "wrong"})
    assert rejection is not None and not rejection.declared_schema
    assert not RejectionPolicy(contracts, transformed_chart.defaults, declared_schema=True).preserves(rejection)
    assert set(rejection.transformed_domains[0].suggestions()) == {"$.text"}
    with pytest.raises(RenderFailure) as failure:
        render(transformed_chart, {"text": "wrong"})
    assert matches_rejection(str(failure.value), rejection)


def test_repeated_input_occurrences_do_not_produce_false_preimages(transformed_chart: Chart) -> None:
    """
    Reevaluate every alias occurrence instead of treating a repeated input as independent operands.

    Args:
        transformed_chart (Chart): Chart with a repeated integer source.

    Returns:
        None: An invalid single-operand solution is rejected; incomplete inversion remains explicit.
    """
    (transformed_chart.path / "templates/NOTES.txt").write_text(
        dedent("""
        {{ if not (has (toString (add .Values.count .Values.count)) (list "8")) }}
          {{ fail "count must sum to eight" }}
        {{ end }}
        """)
    )
    contracts = Contracts.build(transformed_chart.path)
    rejection = contracts.predict(transformed_chart.defaults)
    assert rejection is not None
    assert rejection.transformed_domains[0].suggestions() == {}
    assert contracts.predict({**transformed_chart.defaults, "count": 4}) is None
