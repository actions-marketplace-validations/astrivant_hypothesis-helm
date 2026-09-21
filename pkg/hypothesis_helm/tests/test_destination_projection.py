"""
Verify source-derived destinations independently of chart names or template snapshots.
"""

import itertools
import json
import shutil
from pathlib import Path
from textwrap import dedent, indent

import pytest
from jsonschema import validators

from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.projections import Input, Operation
from hypothesis_helm.compiler.passes.domain_constraints import guard_bounds, predicate
from hypothesis_helm.compiler.passes.domains import project
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.tests.test_input_domains import fixture_chart


def test_opaque_formatted_sibling_preserves_direct_destination(tmp_path: Path) -> None:
    """
    Retain a port mapping beside a quoted unsupported transformation.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: Only the known destination is constrained.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(template.read_text().replace(".Values.secretName | quote", 'printf "prefix-%s" .Values.secretName | quote'))
    rules = chart.input_domains().rules
    assert any(rule["path"] == ["port"] for rule in rules)
    assert not any(rule["path"] == ["secretName"] for rule in rules)


@pytest.mark.parametrize("operation", ["default", "coalesce"])
def test_fallback_keeps_empty_input_and_constrains_selected_reference(tmp_path: Path, operation: str) -> None:
    """
    Derive fallback guards from expressions rather than permitting empty strings by chart name.

    Args:
        tmp_path (Path): Isolated chart directory.
        operation (str): Supported fallback function.

    Returns:
        None: The empty fallback and valid reference remain eligible.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    call = f'{operation} "fallback" .Values.secretName' if operation == "default" else 'coalesce .Values.secretName "fallback"'
    template.write_text(template.read_text().replace(".Values.secretName | quote", f"{call} | quote"))
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    for value in ("", "valid-name", "0"):
        assert validator.is_valid(json_value({**chart.defaults, "secretName": value}))
    assert not validator.is_valid(json_value({**chart.defaults, "secretName": ">0"}))


@pytest.mark.parametrize("enabled", [False, True])
def test_branch_assignment_and_with_aliases(tmp_path: Path, enabled: bool) -> None:
    """
    Join lexical assignments and retain the condition selecting a helper argument.

    Args:
        tmp_path (Path): Isolated chart directory.
        enabled (bool): Branch selecting the input instead of a constant fallback.

    Returns:
        None: The input constraint applies exactly when the alias reaches the manifest.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "arbitrary.helper" -}}
        {{- $selected := "fallback" -}}
        {{- if .enabled -}}{{- $selected = .input -}}{{- end -}}
        {{- with (dict "forwarded" $selected) -}}{{- .forwarded -}}{{- end -}}
        {{- end -}}
        """)
    )
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        template.read_text().replace(
            ".Values.secretName | quote",
            'include "arbitrary.helper" (dict "input" .Values.secretName "enabled" .Values.enabled) | quote',
        )
    )
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value({**chart.defaults, "enabled": enabled, "secretName": ">0"})) is (not enabled)


@pytest.mark.parametrize("merge", ["merge", "mergeOverwrite"])
def test_literal_tpl_serialization_and_local_map_merge(tmp_path: Path, merge: str) -> None:
    """
    Infer annotation contributions through renamed helpers, serialization and a local accumulator.

    Args:
        tmp_path (Path): Isolated chart directory.
        merge (str): Local map operation with either precedence.

    Returns:
        None: Both literal maps receive string-value constraints; dynamic template contents remain for Helm.
    """
    chart = fixture_chart(tmp_path)
    mapping(chart.schema["properties"]).update(first={"type": "object"}, second={"type": "object"})
    chart.defaults.update(first={"purpose": "example"}, second={"team": "platform"})
    (tmp_path / "values.schema.json").write_text(json.dumps(chart.schema))
    (tmp_path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "interpret" -}}
        {{- $value := typeIs "string" .value | ternary .value (.value | toYaml) -}}
        {{- if contains "{{" (toJson .value) -}}
        {{- tpl $value .context -}}
        {{- else -}}{{- $value -}}{{- end -}}
        {{- end -}}
        {{- define "combine" -}}
        {{- $result := dict -}}
        {{- range .values -}}
        {{- $result = include "interpret" (dict "value" . "context" $.context) | fromYaml | MERGE $result -}}
        {{- end -}}
        {{- $result | toYaml -}}
        {{- end -}}
        """).replace("MERGE", merge)
    )
    template = tmp_path / "templates/pod.yaml"
    annotations = indent(
        dedent("""
        name: example
        annotations: {{ include "combine" (dict "values" (list .Values.first .Values.second) "context" $) | nindent 4 }}
        """).strip(),
        "  ",
    )
    template.write_text(template.read_text().replace("  name: example", annotations))
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value(chart.defaults))
    for path in ("first", "second"):
        assert not validator.is_valid(json_value({**chart.defaults, path: {"bad": []}}))
        assert validator.is_valid(json_value({**chart.defaults, path: {"bad": '{{ fail "code" }}'}}))
        assert validator.is_valid(json_value({**chart.defaults, path: {"good": '{{ "generated" }}'}}))
        assert validator.is_valid(json_value({**chart.defaults, path: {"good": "literal"}}))
    if shutil.which("helm"):
        assert render(chart, chart.defaults)
        with pytest.raises(RenderFailure) as failure:
            render(chart, {**chart.defaults, "first": {"bad": []}})
        assert failure.value.code == "HH1109"
        assert render(chart, {**chart.defaults, "first": {"good": '{{ "generated" }}'}})
        with pytest.raises(RenderFailure, match="code"):
            render(chart, {**chart.defaults, "first": {"bad": '{{ fail "code" }}'}})


def test_independent_conditions_do_not_multiply_whole_template_variants(tmp_path: Path) -> None:
    """
    Analyze twelve independent branches without enumerating their 4096 combinations.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: Every direct port destination retains its individual guard.
    """
    chart = fixture_chart(tmp_path)
    branches = []
    for index in range(12):
        mapping(chart.schema["properties"])[f"enabled{index}"] = {"type": "boolean"}
        branches.append(
            dedent("""
            {{ if .Values.ENABLED }}
            - containerPort: {{ .Values.port }}
            {{ end }}
            """).replace("ENABLED", f"enabled{index}")
        )
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        template.read_text().replace(
            "        - containerPort: {{ .Values.port }}", "\n".join("        " + line for line in "".join(branches).splitlines())
        )
    )
    rules, notes = project(chart.path, chart.schema)
    ports = [rule for rule in rules if rule["path"] == ["port"]]
    assert len(ports) == 12
    assert not any("variants" in str(note) for note in notes)


def test_input_mutation_does_not_establish_stale_origins(tmp_path: Path) -> None:
    """
    Refuse a source mapping when a helper can replace the input map itself.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: Unknown shared mutation is explicit and does not constrain the old input.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text('{{ $_ := set .Values "secretName" "fixed" }}\n' + template.read_text())
    rules, notes = project(chart.path, chart.schema)
    assert not rules
    assert "shared input mutation" in str(notes)


def test_unknown_resource_identity_does_not_borrow_a_known_branch_schema(tmp_path: Path) -> None:
    """
    Require every possible resource identity before applying an API field constraint.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: An unresolved API version cannot inherit the alternate branch's schema.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        template.read_text().replace("apiVersion: v1", "apiVersion: {{ if .Values.enabled }}v1{{ else }}{{ .Values.secretName }}{{ end }}")
    )
    rules, _ = project(chart.path, chart.schema)
    assert not rules


def test_general_projection_survives_source_and_chart_renames(tmp_path: Path) -> None:
    """
    Recompute mappings after source edits without checking a known chart name or digest.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: A new chart name and comment leave the structural mapping intact.
    """
    chart = fixture_chart(tmp_path)
    metadata = tmp_path / "Chart.yaml"
    metadata.write_text(yamlio.dump({"apiVersion": "v2", "name": "never-in-a-catalog", "version": "3.2.1"}))
    template = tmp_path / "templates/pod.yaml"
    template.write_text("{{/* unrelated edit */}}\n" + template.read_text())
    template.rename(template.with_name("renamed.yaml"))
    rules, _ = project(chart.path, chart.schema)
    assert {tuple(sequence(rule["path"])) for rule in rules} == {("port",), ("secretName",)}


def test_unknown_fragment_does_not_invent_a_known_resource(tmp_path: Path) -> None:
    """
    Contain structural uncertainty to the affected resource and resume at a document separator.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: Only the independent second Pod establishes destinations.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        dedent("""
        apiVersion: v1
        kind: Pod
        {{ .Values.secretName }}
        spec:
          containers:
            - ports:
                - containerPort: {{ .Values.port }}
        ---
        """)
        + template.read_text()
    )
    rules, _ = project(chart.path, chart.schema)
    assert len([rule for rule in rules if rule["path"] == ["port"]]) == 1


@pytest.mark.parametrize("enabled", [False, True])
def test_branch_local_map_mutation_updates_dot_and_aliases(tmp_path: Path, enabled: bool) -> None:
    """
    Keep the condition selecting a helper-local map entry after a write in one branch.

    Args:
        tmp_path (Path): Isolated chart directory.
        enabled (bool): Whether the source reference gets replaced with a fixed name.

    Returns:
        None: A replaced input is not constrained using its stale origin.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "update-local" -}}
        {{- if .enabled -}}{{- $_ := set . "name" "fixed" -}}{{- end -}}
        {{- .name -}}
        {{- end -}}
        """)
    )
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        template.read_text().replace(
            ".Values.secretName | quote",
            'include "update-local" (dict "name" .Values.secretName "enabled" .Values.enabled) | quote',
        )
    )
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value({**chart.defaults, "enabled": enabled, "secretName": ">0"})) is enabled


def test_with_else_uses_the_enclosing_dot(tmp_path: Path) -> None:
    """
    Follow the caller's dot when a statically empty with expression takes its else branch.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: The else branch still carries the original Secret-name path.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_helpers.tpl").write_text(
        '{{- define "empty-with" -}}{{- with nil -}}unreachable{{- else -}}{{ .Values.secretName }}{{- end -}}{{- end -}}'
    )
    template = tmp_path / "templates/pod.yaml"
    template.write_text(template.read_text().replace(".Values.secretName | quote", 'include "empty-with" . | quote'))
    assert any(rule["path"] == ["secretName"] for rule in chart.input_domains().rules)


@pytest.mark.parametrize("same_origin", [False, True])
def test_conflicting_helper_definitions_require_agreement(tmp_path: Path, same_origin: bool) -> None:
    """
    Join possible helper definitions without guessing which dependency Helm loads last.

    Args:
        tmp_path (Path): Isolated chart directory.
        same_origin (bool): Both implementations forward the same input.

    Returns:
        None: Shared constraints survive; a constraint established by only one definition does not.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_one.tpl").write_text('{{- define "conflict" -}}{{ .Values.secretName }}{{- end -}}')
    other = "print .Values.secretName" if same_origin else '"fixed"'
    (tmp_path / "templates/_two.tpl").write_text('{{- define "conflict" -}}{{ ' + other + " }}{{- end -}}")
    template = tmp_path / "templates/pod.yaml"
    template.write_text(template.read_text().replace(".Values.secretName | quote", 'include "conflict" . | quote'))
    rules = chart.input_domains().rules
    assert any(rule["path"] == ["secretName"] for rule in rules) is same_origin
    assert any(rule["path"] == ["port"] for rule in rules)


def test_finite_field_names_do_not_block_unrelated_destinations(tmp_path: Path) -> None:
    """
    Localize a statically bounded dynamic key to its possible fields.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: An uncertain field name cannot erase sibling port and Secret mappings.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        template.read_text().replace(
            "spec:\n",
            dedent("""
        spec:
          {{ ternary "nodeSelector" "affinity" .Values.enabled }}:
            placeholder: example
        """).lstrip(),
        )
    )
    rules = chart.input_domains().rules
    assert {tuple(sequence(rule["path"])) for rule in rules} >= {("port",), ("secretName",)}


@pytest.mark.parametrize("conjunction", [False, True])
def test_partial_guard_regions_are_sufficient_for_every_unknown_value(conjunction: bool) -> None:
    """
    Check sufficient Boolean regions against every completion of an unresolved operand.

    Args:
        conjunction (bool): Combine the known and unknown inputs with AND rather than OR.

    Returns:
        None: Each established region agrees with both possible values of the unknown operand.
    """
    value = Operation("and" if conjunction else "or", (Input(("enabled",)), Operation("renderer-context")))
    yes, no = guard_bounds(value)
    accepts = validators.validator_for(yes)(yes)
    rejects = validators.validator_for(no)(no)
    for enabled in (False, True):
        outcomes = [(enabled and unknown) if conjunction else (enabled or unknown) for unknown in (False, True)]
        assert accepts.is_valid({"enabled": enabled}) == all(outcomes)
        assert rejects.is_valid({"enabled": enabled}) == (not any(outcomes))


@pytest.mark.parametrize("known", list(itertools.product((False, True), repeat=3)))
def test_conditional_guard_bounds_agree_with_every_unknown_completion(known: tuple[bool, bool, bool]) -> None:
    """
    Check conditional bounds against the complete Boolean truth table including unresolved operands.

    Args:
        known (tuple[bool, bool, bool]): Whether the selector and each arm have established input origins.

    Returns:
        None: Established regions agree with every possible completion; conflicting unknowns stay unresolved.
    """
    names = ("selector", "yes", "no")
    expression = Operation(
        "choose", tuple(Input((name,)) if resolved else Operation("renderer-context") for name, resolved in zip(names, known, strict=True))
    )
    bounds = guard_bounds(expression)
    accepts, rejects = (validators.validator_for(bound)(bound) for bound in bounds)
    exact = predicate(expression)
    assert (exact is not None) == all(known)
    for inputs in itertools.product((False, True), repeat=3):
        candidate = dict(zip(names, inputs, strict=True))
        possibilities = [(value,) if resolved else (False, True) for value, resolved in zip(inputs, known, strict=True)]
        outcomes = [yes if condition else no for condition, yes, no in itertools.product(*possibilities)]
        assert accepts.is_valid(candidate) == all(outcomes)
        assert rejects.is_valid(candidate) == (not any(outcomes))
        if exact is not None:
            assert validators.validator_for(exact)(exact).is_valid(candidate) == outcomes[0]


def test_conditional_item_guard_stays_relative_to_its_collection() -> None:
    """
    Express each element's choice locally without treating all elements as a single Boolean.

    Returns:
        None: Different array elements can select different predicate branches.
    """
    root = ("entries", "*")
    expression = Operation("choose", tuple(Input((*root, name)) for name in ("selector", "yes", "no")))
    assert predicate(expression) is None
    local = predicate(expression, root=root)
    assert local is not None
    validator = validators.validator_for(local)(local)
    for selector, yes, no in itertools.product((False, True), repeat=3):
        assert validator.is_valid({"selector": selector, "yes": yes, "no": no}) == (yes if selector else no)


def test_known_part_of_activation_guard_retains_the_supported_region(tmp_path: Path) -> None:
    """
    Retain certain activation regions while leaving renderer-dependent regions unconstrained.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: Disabling the known gate establishes the else branch regardless of renderer capabilities.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        dedent("""
        {{ if and .Values.enabled (.Capabilities.APIVersions.Has "example/v1") }}
        {{ fail "unsupported configuration" }}
        {{ else }}
        """)
        + template.read_text()
        + "{{ end }}"
    )
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert not validator.is_valid(json_value({**chart.defaults, "enabled": False, "port": 0}))
    assert validator.is_valid(json_value({**chart.defaults, "enabled": True, "port": 0}))


def test_inline_conditional_helper_inside_sequence_block_scalar(tmp_path: Path) -> None:
    """
    Keep shell arguments inside a YAML block scalar without changing later resource field paths.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: Conditional command text cannot move a later port or volume to the resource root.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "arguments" -}}
        {{- with .Values -}}
        {{- ternary " --enabled" "" .enabled -}}
        {{- if .secretName -}} --name={{ .secretName | quote }}{{- end -}}
        {{- end -}}
        {{- end -}}
        """)
    )
    template = tmp_path / "templates/pod.yaml"
    arguments = indent(
        dedent("""
        image: example
        args:
          - |
            echo {{ include "arguments" . }}
        """).strip(),
        "      ",
    )
    template.write_text(template.read_text().replace("      image: example", arguments))
    rules = chart.input_domains().rules
    assert {tuple(sequence(rule["path"])) for rule in rules} >= {("port",), ("secretName",)}
    assert all(".args." not in str(rule["destination"]) for rule in rules)


def test_unvisited_loop_write_cannot_leave_a_stale_input_mapping(tmp_path: Path) -> None:
    """
    Invalidate shared origins when an unbounded loop can mutate the values map.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        None: Unknown iteration counts never make a known mutation disappear from the analysis.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        dedent("""
        {{ range .Values.items }}
        {{ $_ := set $.Values "secretName" "fixed" }}
        {{ end }}
        """)
        + template.read_text()
    )
    rules, notes = project(chart.path, chart.schema)
    assert not rules
    assert "shared input mutation" in str(notes)


@pytest.mark.parametrize("literal", ["false", "0"])
def test_include_returns_text_before_a_caller_tests_truth(tmp_path: Path, literal: str) -> None:
    """
    Respect Helm's string-returning include boundary for Boolean and numeric helper output.

    Args:
        tmp_path (Path): Isolated chart directory.
        literal (str): A false-like value whose rendered text is nonempty.

    Returns:
        None: Both helper strings select the true branch, as native Helm does.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_helpers.tpl").write_text('{{- define "truth" -}}{{ ' + literal + " }}{{- end -}}")
    template = tmp_path / "templates/pod.yaml"
    template.write_text('{{ if include "truth" . }}\n' + template.read_text() + "{{ end }}")
    assert any(rule["path"] == ["port"] for rule in chart.input_domains().rules)
    if shutil.which("helm"):
        assert render(chart, chart.defaults)
