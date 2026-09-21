"""
Preserve values-path provenance and unordered text inside explicit template contracts.
"""

from __future__ import annotations

import re
from collections import Counter

from attrs import frozen
from ruamel.yaml.scalarbool import ScalarBoolean

__all__ = (
    "BoundValue",
    "ConstantList",
    "ConstantMap",
    "ContractText",
    "DerivedValue",
    "KeyList",
    "NilMap",
    "NilSlice",
    "UnorderedKeys",
    "native",
)


class NilSlice(list[object]):
    """
    Preserve Go's nil slice: empty for iteration, still a slice, but JSON null.
    """

    __slots__ = ()


class NilMap(dict[str, object]):
    """
    Preserve Go's nil map: readable as empty, JSON null, and unsafe for direct writes.
    """

    __slots__ = ()


@frozen
class BoundValue:
    """
    Associate a concrete helper argument with its original chart input.

    Attributes:
        value (object): Candidate value, including maps and lists.
        path (tuple[str, ...]): Absolute values path before helper context changes.
    """

    value: object
    path: tuple[str, ...]


@frozen
class DerivedValue:
    """
    Retain an evaluated transformation without mistaking its output for the source input.

    Attributes:
        value (object): Concrete result for this candidate.
        function (str): Supported transformation name.
        arguments (tuple[object, ...]): Operands retaining their original values paths.
    """

    value: object
    function: str
    arguments: tuple[object, ...]


@frozen
class ConstantMap:
    """
    Retain a dictionary whose keys were literal strings in the template.

    Attributes:
        values (dict[str, object]): Literal keys and evaluated, possibly bound values.
    """

    values: dict[str, object]


@frozen
class ConstantList:
    """
    Retain an allowlist constructed entirely from literal scalar strings.

    Attributes:
        values (tuple[str, ...]): Template-authored members in source order.
    """

    values: tuple[str, ...]


@frozen
class UnorderedKeys:
    """
    Preserve map keys without assuming Go's map iteration order.

    Attributes:
        values (tuple[str, ...]): Distinct dictionary keys.
    """

    values: tuple[str, ...]


@frozen
class KeyList:
    """
    Describe an unordered joined key list inside a chart-authored message.

    Attributes:
        separator (str): Literal join separator.
        values (tuple[str, ...]): Keys that must each occur exactly once.
    """

    separator: str
    values: tuple[str, ...]


@frozen
class ContractText:
    """
    Describe exact text while allowing only proved map-key ordering differences.

    Attributes:
        parts (tuple[str | KeyList, ...]): Literal fragments and unordered key lists.
    """

    parts: tuple[str | KeyList, ...]

    def text(self) -> str:
        """
        Produce a stable representative for reporting.

        Returns:
            str: Message with map keys sorted for deterministic artifacts.
        """
        return "".join(part if isinstance(part, str) else part.separator.join(sorted(part.values)) for part in self.parts)

    def matches(self, observed: str) -> bool:
        """
        Match an exact message modulo whitespace and known key-list order.

        Args:
            observed (str): Helm's chart-authored rejection message.

        Returns:
            bool: Literal text matches and every expected key occurs exactly once.
        """
        pattern = []
        groups: list[KeyList] = []
        for part in self.parts:
            if isinstance(part, str):
                pattern.append(re.sub(r"(?:\\[ \t\r\n])+", r"\\s+", re.escape(part)))
            else:
                if not part.separator or any(part.separator in key for key in part.values):
                    return False
                choices = "(?:" + "|".join(re.escape(key) for key in sorted(part.values, key=len, reverse=True)) + ")"
                segment = choices + "(?:" + re.escape(part.separator) + choices + ")*" if part.values else ""
                pattern.append(f"(?P<keys{len(groups)}>{segment})")
                groups.append(part)
        match = re.fullmatch("".join(pattern).strip(), observed.strip())
        # Compare key multiplicities after matching: regex alternatives alone would admit repeated keys.
        return match is not None and all(
            Counter(match[f"keys{index}"].split(group.separator) if group.values else []) == Counter(group.values)
            for index, group in enumerate(groups)
        )


def native(value: object) -> object:
    """
    Unwrap the outer analysis value without dropping nested argument provenance.

    Args:
        value (object): Concrete or analysis-wrapped value.

    Returns:
        object: Native value used by supported Helm scalar operations.
    """
    if isinstance(value, BoundValue | DerivedValue):
        return native(value.value)
    if isinstance(value, ConstantMap):
        # Keep nested wrappers intact so a later field lookup can still recover its input origin.
        return value.values
    if isinstance(value, ConstantList | UnorderedKeys):
        return list(value.values)
    if isinstance(value, ContractText):
        return value.text()
    if isinstance(value, str):
        return str(value)
    if isinstance(value, ScalarBoolean):
        return bool(value)
    if isinstance(value, int) and not isinstance(value, bool):
        return int(value)
    if isinstance(value, float):
        return float(value)
    return value
