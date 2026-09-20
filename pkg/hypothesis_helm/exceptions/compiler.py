"""
Signal unsupported compiler analysis, explicit chart rejection, and template control flow.
"""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING

from attrs import define, field, frozen

if TYPE_CHECKING:
    from hypothesis_helm.compiler.asts.contract_values import ContractText
    from hypothesis_helm.compiler.asts.transformations import TransformedDomain


class Unknown(ValueError):
    """
    Indicate that the contract cannot be evaluated in the supported subset.

    Attributes:
        source (str | None): Innermost template source where evaluation stopped.
        line (int): Source line, or zero when parsing did not establish a location.
    """

    source: str | None = None
    line: int = 0


@frozen
class Rejection(Exception):
    """
    Retain an evaluated rejection and the input evidence used to reach it.

    Attributes:
        source (str): Template containing the rejection sink.
        line (int): Source line containing fail or required.
        message (str): Explicit chart-authored rejection message.
        inputs (dict[str, object]): Values inspected by the contract, including related fields.
        conditions (tuple[str, ...]): Evaluated branch conditions and their outcomes.
        enums (dict[str, tuple[str, ...]]): Literal allowlists inspected on the rejecting branch.
        text (ContractText | None): Exact message including known unordered key-list fragments.
        declared_schema (bool): The rejecting input belongs to an explicitly declared child schema.
        transformed_domains (tuple[TransformedDomain, ...]): Branch-local constraints on transformed outputs.
        transformed (bool): Prediction evaluated a supported transformation and needs native verification.
        contextual (bool): Prediction used capabilities, files or tpl and always needs native verification.
    """

    source: str
    line: int
    message: str
    inputs: dict[str, object]
    conditions: tuple[str, ...]
    enums: dict[str, tuple[str, ...]] = field(factory=dict)
    text: ContractText | None = None
    declared_schema: bool = False
    transformed_domains: tuple[TransformedDomain, ...] = ()
    transformed: bool = False
    contextual: bool = False

    @property
    def key(self) -> str:
        """
        Identify a rejection independently of candidate values.

        Returns:
            str: Stable source/message fingerprint within this loaded chart.
        """
        domain = (
            json.dumps({"enums": self.enums, "transformed_domains": [item.report() for item in self.transformed_domains]}, sort_keys=True)
            if self.transformed_domains
            else json.dumps(self.enums, sort_keys=True)
            if self.enums
            else self.message
        )
        return hashlib.sha256(f"{self.source}:{self.line}:{domain}".encode()).hexdigest()[:16]

    def report(self) -> dict[str, object]:
        """
        Export contract evidence separately from manifest failures.

        Returns:
            dict[str, object]: Source, requirement text, evaluated conditions, and joint values.
        """
        return {
            "id": self.key,
            "source": self.source,
            "line": self.line,
            "requirement": self.message.strip(),
            "inputs": dict(reversed(list(self.inputs.items()))),
            "conditions": list(self.conditions),
            "enums": {path: list(values) for path, values in self.enums.items()},
            "transformed_domains": [domain.report() for domain in self.transformed_domains],
        }


@define
class LoopControl(Exception):
    """
    Carry a loop jump and text emitted before it through nested lexical blocks.

    Attributes:
        action (str): Break or continue for the enclosing range.
        output (str): Text already emitted in the interrupted iteration.
    """

    action: str
    output: str = ""


class Unavailable(ValueError):
    """
    Keep unavailable native context outside the compiler's supported domain.
    """


class UnsupportedTransformation(ValueError):
    """
    Leave unsupported types, conversions, or overflow for native Helm execution.
    """
