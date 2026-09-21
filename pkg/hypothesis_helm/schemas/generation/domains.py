"""
Resolve and report the generation-only domain for one chart.
"""

import copy
import hashlib
import json

from attrs import field, frozen
from jsonschema import validators
from ruamel.yaml.error import YAMLError

from hypothesis_helm.charts.model import Chart, _schema_nodes
from hypothesis_helm.charts.values.parsers import selected as selected_parser
from hypothesis_helm.schemas.configuration.characters import character_sets as active_character_sets
from hypothesis_helm.schemas.configuration.policy import inherited_policy, path_parts, restrict
from hypothesis_helm.schemas.configuration.selectors import matching_rules
from hypothesis_helm.schemas.configuration.settings import generation_settings, settings_at
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence

__all__ = ("InputDomains",)


@frozen
class InputDomains:
    """
    Keep source contracts separate from explicit and destination-derived test domains.

    Attributes:
        rules (list[dict[str, object]]): Resolved chart-specific constraints.
        diagnostics (list[dict[str, object]]): Unresolved destinations and default conflicts.
        identity (str): Stable content digest for reports and caching.
        character_sets (str): Generated text alphabet saved with this domain snapshot.
        generation (dict[str, object]): Frozen per-branch text and Hypothesis settings.
        yaml_parser (str): Manifest parser used when establishing and executing these domains.
    """

    rules: list[dict[str, object]]
    diagnostics: list[dict[str, object]]
    identity: str
    character_sets: str = "ascii"
    generation: dict[str, object] = field(factory=dict)
    yaml_parser: str = "ruamel"

    @classmethod
    def build(cls, chart: Chart) -> "InputDomains":
        """
        Resolve configured paths and conservative destination mappings once per chart.

        Args:
            chart (Chart): Original chart and unchanged source values.

        Returns:
            InputDomains: Domain policy with explicit evidence and limitations.
        """
        from hypothesis_helm.charts.suites.generate import coalesce
        from hypothesis_helm.compiler.passes.dependencies import Dependencies
        from hypothesis_helm.compiler.passes.domains import project

        policy = inherited_policy()
        if chart.dependency_model is None:
            chart.dependency_model = Dependencies.build(chart.path)
        diagnostics: list[dict[str, object]] = []
        try:
            schema = coalesce(chart).schema
        except (ValueError, YAMLError) as inference_error:
            # Optional domain analysis must not turn an unsupported inferred type
            # into an audit failure. Declared types remain usable evidence.
            schema = chart.schema
            diagnostics.append({"reason": "inferred domains unavailable; using declared paths only", "detail": str(inference_error)})
        generation = generation_settings(chart.path)
        rules: list[dict[str, object]] = []
        for rule in matching_rules(chart.path):
            path = path_parts(str(rule["path"]))
            settings_at(generation, path)
            if "schema" not in rule:
                continue
            if not _schema_nodes(schema, path, schema):
                raise ValueError(f"Input constraint {rule['path']} has no known path in chart {chart.path.name}")
            rules.append({**rule, "path": list(path)})
        projected, projection_diagnostics = (
            project(chart.path, schema, chart.dependency_model) if policy.get("downstream_inputs", True) else ([], [])
        )
        diagnostics.extend(projection_diagnostics)
        for rule in projected:
            path = tuple(str(part) for part in sequence(rule["path"]))
            if "element_path" in rule:
                element_path = tuple(str(part) for part in sequence(rule["element_path"]))
                try:
                    for node in _schema_nodes(schema, element_path, schema):
                        restrict(node, (), mapping(rule["element_schema"]))
                except ValueError:
                    diagnostics.append(
                        {"path": list(element_path), "reason": "destination conflicts with declared element domain; domain unchanged"}
                    )
                    continue
            nodes = _schema_nodes(schema, path, schema)
            kinds = {
                str(kind)
                for node in nodes
                for kind in ([node["type"]] if isinstance(node.get("type"), str) else sequence(node.get("type", [])))
            }
            # Quoting changes representation; a destination string constraint is not automatically an input-type constraint.
            if rule["quoted"] and kinds != {"string"}:
                diagnostics.append({"path": list(path), "reason": "quote converts a non-string or unknown input; domain unchanged"})
                continue
            allowed = {"string", "integer", "number", "boolean"}
            if rule.get("serialized"):
                allowed.update({"object", "array"})
            if (not kinds and not rule.get("serialized")) or not kinds <= allowed:
                diagnostics.append({"path": list(path), "reason": "direct mapping has no unambiguous scalar input type"})
                continue
            try:
                for node in nodes:
                    restrict(node, (), mapping(rule["schema"]))
            except ValueError:
                diagnostics.append({"path": list(path), "reason": "destination type or bounds conflict with source; domain unchanged"})
                continue
            rules.append(rule)
        selected = active_character_sets()
        parser = selected_parser()
        identity = hashlib.sha256(
            json.dumps(
                {"rules": rules, "character_sets": selected, "generation": generation, "yaml_parser": parser}, sort_keys=True
            ).encode()
        ).hexdigest()
        result = cls(rules, diagnostics, identity, selected, generation, parser)
        restricted = result.apply(schema)
        validator = validators.validator_for(restricted)(restricted)
        for error in validator.iter_errors(json_value(chart.defaults)):
            # Only report newly introduced conflicts, not unrelated original schema gaps.
            if validators.validator_for(schema)(schema).is_valid(json_value(chart.defaults)):
                diagnostics.append(
                    {"path": list(error.absolute_path), "reason": "supplied default outside generation domain", "detail": error.message}
                )
        return result

    def apply(self, schema: dict[str, object]) -> dict[str, object]:
        """
        Intersect every applicable rule, preserving conditional resource activation.

        Args:
            schema (dict[str, object]): Original, coalesced or focused generation contract.

        Returns:
            dict[str, object]: Generation-only copy of the contract.
        """
        result = copy.deepcopy(schema)
        for rule in self.rules:
            path = tuple(str(part) for part in sequence(rule["path"]))
            restriction = mapping(rule["schema"])
            guards = sequence(rule.get("guards", []))
            if guards:
                conditional: dict[str, object] = {"if": {"allOf": guards}, "then": restrict({}, path, restriction)}
                if rule.get("literal_fragment"):
                    conditional["x-hypothesis-helm-literal-fragment"] = True
                sequence(result.setdefault("allOf", [])).append(conditional)
            else:
                try:
                    result = restrict(result, path, restriction)
                except ValueError as exc:
                    raise ValueError(f"Input domain at $.{'.'.join(path)}: {exc}") from exc
        return result

    def report(self) -> dict[str, object]:
        """
        Expose reduced coverage and unchanged defaults in machine-readable reports.

        Returns:
            dict[str, object]: Active rules, provenance and unresolved mapping diagnostics.
        """
        return {
            "identity": self.identity,
            "character_sets": self.character_sets,
            "generation": self.generation,
            "yaml_parser": self.yaml_parser,
            "constraints": self.rules,
            "diagnostics": self.diagnostics,
            "scope": "generated cases satisfying these input domains; supplied defaults are tested unchanged",
        }
