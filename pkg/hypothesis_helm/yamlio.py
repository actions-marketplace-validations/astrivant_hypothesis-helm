"""
Round-trip YAML I/O shared by chart loading, coalescing and generation.
"""

from io import StringIO

from ruamel.yaml import YAML


def yaml() -> YAML:
    """
    Check yaml.

    Returns:
        YAML: Result of the documented operation.
    """
    instance = YAML(typ="rt")
    instance.preserve_quotes = True
    instance.allow_duplicate_keys = False
    return instance


def load(text: str) -> object:
    """
    Check load.

    Args:
        text (str): YAML or template text to process.

    Returns:
        object: Parsed or generated value at the requested boundary.
    """
    return yaml().load(text)


def dump(value: object) -> str:
    """
    Check dump.

    Args:
        value (object): Candidate value supplied by the property strategy.

    Returns:
        str: Serialized output or resolved strategy expression.
    """
    stream = StringIO()
    yaml().dump(value, stream)
    return stream.getvalue()


def load_all(text: str) -> list[object]:
    """
    Check load all.

    Args:
        text (str): YAML or template text to process.

    Returns:
        list[object]: Result of the documented operation.
    """
    return list(yaml().load_all(text))
