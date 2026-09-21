"""
Resolve explicit text domains and Hypothesis settings for individual values branches.
"""

import copy
import math
from pathlib import Path

from hypothesis import HealthCheck, Phase

from hypothesis_helm.schemas.configuration.characters import validate_character_sets
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = (
    "DEFAULT_CONTROLS",
    "GENERATION_KEYS",
    "SETTING_KEYS",
    "custom_text",
    "generation_settings",
    "global_settings",
    "hypothesis_parameters",
    "is_control",
    "normalize_text",
    "settings_at",
    "text_allowed",
    "validate_settings",
)


SETTING_KEYS = {"hypothesis"}
GENERATION_KEYS = {"character_sets", "control_characters", "exclude_characters", "hypothesis"}
DEFAULT_CONTROLS: dict[str, object] = {"exclude": True, "allow": ["\n", "\r"]}


def validate_settings(raw: dict[str, object]) -> dict[str, object]:
    """
    Validate only supported knobs rather than forwarding unchecked Hypothesis arguments.

    Args:
        raw (dict[str, object]): Global configuration or one input constraint.

    Returns:
        dict[str, object]: Validated partial overrides, preserving unspecified inheritance.
    """
    if "hypothesis" not in raw:
        return {}
    configured = copy.deepcopy(mapping(raw["hypothesis"]))
    result = {key: configured.pop(key) for key in GENERATION_KEYS - {"hypothesis"} if key in configured}
    result["hypothesis"] = configured
    if "character_sets" in result:
        result["character_sets"] = validate_character_sets(result["character_sets"])
    if "exclude_characters" in result and not isinstance(result["exclude_characters"], str):
        raise ValueError("exclude_characters must be a string containing the characters to exclude")
    if "control_characters" in result:
        controls = mapping(result["control_characters"])
        if set(controls) - {"exclude", "allow"}:
            raise ValueError("control_characters accepts only 'exclude' and 'allow'")
        if "exclude" in controls and type(controls["exclude"]) is not bool:
            raise ValueError("control_characters.exclude must be a Boolean")
        if "allow" in controls and (
            not isinstance(controls["allow"], list)
            or any(not isinstance(char, str) or len(char) != 1 or not is_control(char) for char in sequence(controls["allow"]))
        ):
            raise ValueError("control_characters.allow must list individual C0/C1 control characters")
    if "hypothesis" in result:
        parameters = mapping(result["hypothesis"])
        if set(parameters) - {"max_examples", "deadline_ms", "phases", "suppress_health_check", "random_inputs"}:
            raise ValueError(
                "hypothesis accepts character_sets, control_characters, exclude_characters, "
                "max_examples, deadline_ms, phases, suppress_health_check and random_inputs"
            )
        if "random_inputs" in parameters and type(parameters["random_inputs"]) is not bool:
            raise ValueError("hypothesis.random_inputs must be a Boolean")
        examples = parameters.get("max_examples")
        if "max_examples" in parameters and (type(examples) is not int or int(str(examples)) < 1):
            raise ValueError("hypothesis.max_examples must be a positive integer")
        deadline = parameters.get("deadline_ms")
        if deadline is not None and (
            type(deadline) not in (int, float) or not math.isfinite(float(str(deadline))) or float(str(deadline)) <= 0
        ):
            raise ValueError("hypothesis.deadline_ms must be null or positive finite milliseconds")
        for key, allowed in (("phases", {"generate", "shrink"}), ("suppress_health_check", {check.name for check in HealthCheck})):
            if key in parameters:
                entries = parameters[key]
                if not isinstance(entries, list) or any(not isinstance(entry, str) or entry not in allowed for entry in entries):
                    raise ValueError(f"hypothesis.{key} must contain names from {', '.join(sorted(allowed))}")
        if "phases" in parameters and "generate" not in sequence(parameters["phases"]):
            raise ValueError("hypothesis.phases must include generate")
    return result


def is_control(char: str) -> bool:
    """
    Identify the explicitly documented C0/C1 ranges, including DEL.

    Args:
        char (str): One Unicode character.

    Returns:
        bool: Whether it is U+0000-U+001F or U+007F-U+009F.
    """
    return ord(char) < 32 or 127 <= ord(char) <= 159


def global_settings() -> dict[str, object]:
    """
    Read generation defaults without resolving a chart or changing authored input values.

    Returns:
        dict[str, object]: Complete text defaults and partial Hypothesis overrides.
    """
    from hypothesis_helm.schemas.configuration.characters import character_sets
    from hypothesis_helm.schemas.configuration.policy import inherited_policy

    policy = inherited_policy()
    return {
        "character_sets": character_sets(),
        "control_characters": {**DEFAULT_CONTROLS, **mapping(policy.get("control_characters", {}))},
        "exclude_characters": policy.get("exclude_characters", ""),
        "hypothesis": policy.get("hypothesis", {}),
    }


def generation_settings(chart: Path) -> dict[str, object]:
    """
    Freeze matching source selectors and generation controls into a replayable snapshot.

    Args:
        chart (Path): Chart source for selector matching.

    Returns:
        dict[str, object]: Defaults and branch rules usable by isolated workers and saved suites.
    """
    from hypothesis_helm.schemas.configuration.selectors import matching_rules, source_identity

    rules = [
        {"path": rule["path"], **{key: copy.deepcopy(rule[key]) for key in GENERATION_KEYS & rule.keys()}}
        for rule in matching_rules(chart)
        if GENERATION_KEYS & rule.keys()
    ]
    return {"defaults": global_settings(), "rules": rules, "source": source_identity(chart)}


def settings_at(generation: dict[str, object], path: tuple[str | int, ...]) -> dict[str, object]:
    """
    Apply the deepest matching override independently for each setting.

    Args:
        generation (dict[str, object]): Frozen defaults and branch rules.
        path (tuple[str | int, ...]): Concrete or symbolic values path.

    Returns:
        dict[str, object]: Effective settings; equal-depth conflicting overrides raise ValueError.
    """
    from hypothesis_helm.schemas.configuration.policy import path_parts

    result = copy.deepcopy(mapping(generation["defaults"]) if "defaults" in generation else global_settings())
    selected: dict[tuple[str, ...], tuple[int, object]] = {}
    for raw in sequence(generation.get("rules", [])):
        rule = mapping(raw)
        prefix = path_parts(str(rule["path"]))
        if len(prefix) > len(path) or any(a != "*" and a != b for a, b in zip(prefix, path, strict=False)):
            continue
        for key in GENERATION_KEYS & rule.keys():
            entries: dict[tuple[str, ...], object] = (
                {(key, str(child)): value for child, value in mapping(rule[key]).items()}
                if isinstance(rule[key], dict)
                else {(key,): rule[key]}
            )
            for setting, value in entries.items():
                previous = selected.get(setting)
                if previous is not None and previous[0] == len(prefix) and previous[1] != value:
                    raise ValueError(f"Conflicting input constraints for {'.'.join(setting)} at {path!r}")
                if previous is None or previous[0] <= len(prefix):
                    selected[setting] = (len(prefix), value)
    for setting, (_, value) in selected.items():
        if len(setting) == 1:
            result[setting[0]] = value
        else:
            mapping(result.setdefault(setting[0], {}))[setting[1]] = value
    return result


def text_allowed(char: str, settings: dict[str, object]) -> bool:
    """
    Apply explicit exclusions and the configured control-character exception list.

    Args:
        char (str): Candidate character.
        settings (dict[str, object]): Effective settings at this values path.

    Returns:
        bool: Whether this character is admitted by the non-alphabet text controls.
    """
    controls = mapping(settings.get("control_characters", DEFAULT_CONTROLS))
    return char not in str(settings.get("exclude_characters", "")) and (
        not controls.get("exclude", True) or not is_control(char) or char in sequence(controls.get("allow", ["\n", "\r"]))
    )


def custom_text(generation: dict[str, object]) -> bool:
    """
    Determine when generated suites need the branch-aware text strategy.

    Args:
        generation (dict[str, object]): Saved defaults and branch overrides.

    Returns:
        bool: Whether default control filtering and one alphabet are insufficient.
    """
    defaults = mapping(generation.get("defaults", {}))
    return bool(
        defaults.get("exclude_characters")
        or defaults.get("control_characters", DEFAULT_CONTROLS) != DEFAULT_CONTROLS
        or any((GENERATION_KEYS - {"hypothesis"}) & mapping(rule).keys() for rule in sequence(generation.get("rules", [])))
    )


def normalize_text(value: object, generation: dict[str, object], path: tuple[str | int, ...], literals: frozenset[str]) -> object:
    """
    Normalize fresh text by field before validating the unchanged source schema.

    Args:
        value (object): Newly generated JSON candidate, never a supplied baseline.
        generation (dict[str, object]): Frozen generation policy.
        path (tuple[str | int, ...]): Current values path, including concrete array indices.
        literals (frozenset[str]): Authored strings exempt from ASCII-only sampling.

    Returns:
        object: Fresh candidate honoring branch text settings and requiring schema validation.
    """
    settings = settings_at(generation, path)
    if isinstance(value, str):
        replacement = next((char for char in "a0 _-" if text_allowed(char, settings)), "")
        return "".join(
            char
            if text_allowed(char, settings) and (settings["character_sets"] == "unicode" or char.isascii() or value in literals)
            else replacement
            for char in value
        )
    if isinstance(value, dict):
        return {
            normalize_text(key, generation, path, literals): normalize_text(child, generation, (*path, str(key)), literals)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [normalize_text(child, generation, (*path, index), literals) for index, child in enumerate(value)]
    return value


def hypothesis_parameters(generation: dict[str, object], path: tuple[str | int, ...], fallback_examples: int) -> dict[str, object]:
    """
    Resolve serializable Hypothesis settings for one property or a whole-chart sample.

    Args:
        generation (dict[str, object]): Frozen generation policy.
        path (tuple[str | int, ...]): Selected property path, or root for whole-chart sampling.
        fallback_examples (int): Command or library default when no override applies.

    Returns:
        dict[str, object]: Effective example budget, deadline, phases, and health-check exclusions.
    """
    configured = mapping(settings_at(generation, path).get("hypothesis", {}))
    return {
        "max_examples": configured.get("max_examples", fallback_examples),
        "deadline_ms": configured.get("deadline_ms"),
        "phases": configured.get("phases", [Phase.generate.name, Phase.shrink.name]),
        "suppress_health_check": configured.get("suppress_health_check", [HealthCheck.too_slow.name]),
    }
