"""
Resolve the generated character domain without changing chart-authored literals.
"""

from contextvars import ContextVar

__all__ = ("CHARACTER_SETS", "character_sets", "declared_text", "generated_text_policy", "validate_character_sets")


CHARACTER_SETS = ("ascii", "unicode")
SUITE_CHARACTER_SETS: ContextVar[str | None] = ContextVar("suite_character_sets", default=None)


def validate_character_sets(value: object) -> str:
    """
    Validate one supported generated character domain.

    Args:
        value (object): Configured mode from YAML, the CLI, or a saved suite.

    Returns:
        str: Validated ASCII or Unicode mode.

    Raises:
        ValueError: The mode is not supported.
    """
    if not isinstance(value, str) or value not in CHARACTER_SETS:
        raise ValueError("character_sets must be 'ascii' or 'unicode'")
    return value


def character_sets() -> str:
    """
    Read the saved suite or inherited worker policy, defaulting to ASCII.

    Returns:
        str: Active generated character domain.
    """
    from hypothesis_helm.schemas.configuration.policy import inherited_policy

    selected = SUITE_CHARACTER_SETS.get()
    return validate_character_sets(selected if selected is not None else inherited_policy().get("character_sets", "ascii"))


def generated_text_policy() -> str:
    """
    Describe the current sampling restriction for reports.

    Returns:
        str: Character coverage and the exceptions for authored inputs.
    """
    import json

    from hypothesis_helm.schemas.configuration.settings import global_settings

    defaults = global_settings()
    return (
        f"Generated text defaults: {character_sets()}; control_characters={json.dumps(defaults['control_characters'])}; "
        f"exclude_characters={json.dumps(defaults['exclude_characters'])}; "
        "branch overrides are recorded in input_domains.generation; supplied defaults are preserved"
    )


def declared_text(schema: dict[str, object]) -> frozenset[str]:
    """
    Collect literal strings and property names that a chart explicitly declares.

    Args:
        schema (dict[str, object]): Schema including local definitions and branches.

    Returns:
        frozenset[str]: Exact authored strings exempt from the ASCII sampling restriction.
    """
    result: set[str] = set()

    def literals(value: object) -> None:
        """
        Collect text inside a declared constant or enumeration value.

        Args:
            value (object): Literal JSON subtree.

        Returns:
            None: Strings and object names are added to the shared result.
        """
        if isinstance(value, str):
            result.add(value)
        elif isinstance(value, dict):
            result.update(str(key) for key in value)
            for child in value.values():
                literals(child)
        elif isinstance(value, list):
            for child in value:
                literals(child)

    pending: list[object] = [schema]
    while pending:
        node = pending.pop()
        if not isinstance(node, dict):
            continue
        for keyword in ("const", "enum"):
            if keyword in node:
                literals(node[keyword])
        for keyword in ("properties", "patternProperties", "$defs", "definitions", "dependentSchemas", "dependencies"):
            children = node.get(keyword)
            if isinstance(children, dict):
                if keyword == "properties":
                    result.update(str(key) for key in children)
                pending.extend(children.values())
        for keyword in (
            "items",
            "prefixItems",
            "additionalItems",
            "contains",
            "additionalProperties",
            "propertyNames",
            "not",
            "if",
            "then",
            "else",
        ):
            child = node.get(keyword)
            pending.extend(child if isinstance(child, list) else [child])
        for keyword in ("allOf", "anyOf", "oneOf"):
            children = node.get(keyword)
            if isinstance(children, list):
                pending.extend(children)
    return frozenset(result)
