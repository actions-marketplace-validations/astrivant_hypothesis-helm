"""
Recover independent block-YAML destinations from symbolic output and branch joins.
"""

from __future__ import annotations

import itertools
import re

from attrs import define, field

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.projections import Input, LocalMap, Operation, Piece
from hypothesis_helm.compiler.passes.domain_constraints import constraints, guard_bounds, input_origins, normalize, predicate
from hypothesis_helm.schemas.kubernetes.resources import destination

__all__ = ("Document", "Layout", "Position", "literals", "scalar", "unresolved")


@define
class Document:
    """
    Collect one resource's literal identities and independent output fields.

    Attributes:
        identities (dict[str, list[object]]): Symbolic apiVersion and kind values.
        fields (list[tuple[tuple[str, ...], Piece, tuple[object, ...]]]): Field paths, origins and enclosing conditions.
        barriers (list[tuple[str, ...]]): Subtrees whose structure is unresolved.
    """

    identities: dict[str, list[object]] = field(factory=dict)
    fields: list[tuple[tuple[str, ...], Piece, tuple[object, ...]]] = field(factory=list)
    barriers: list[tuple[str, ...]] = field(factory=list)


@define
class Position:
    """
    Track block indentation without enumerating combinations of independent branches.

    Attributes:
        document (Document): Current resource, shared by compatible branches.
        frames (list[tuple[int, tuple[str, ...], bool]]): Indentation, field path and sequence-item marker.
        line (str): Unfinished physical line, with symbolic markers.
        block (int | None): Indentation of an open block scalar.
        conditions (tuple[object, ...]): Conditions controlling this output.
    """

    document: Document
    frames: list[tuple[int, tuple[str, ...], bool]] = field(factory=list)
    line: str = ""
    block: int | None = None
    conditions: tuple[object, ...] = ()


@define
class Layout:
    """
    Preserve established field destinations while containing opaque formatted fragments.

    Attributes:
        limits (dict[str, int]): Compiler work and indentation budgets.
        documents (list[Document]): Discovered resource fragments.
        markers (dict[str, Piece]): Symbolic values occurring on physical YAML lines.
        notes (list[dict[str, object]]): Explicit unresolved output locations.
        steps (int): Output traversal work already performed.
    """

    limits: dict[str, int]
    documents: list[Document] = field(factory=list)
    markers: dict[str, Piece] = field(factory=dict)
    notes: list[dict[str, object]] = field(factory=list)
    steps: int = 0

    def new_document(self) -> Document:
        """
        Allocate a separately analyzable resource.

        Returns:
            Document: Fresh identity and field inventory.
        """
        document = Document()
        self.documents.append(document)
        return document

    def marker(self, piece: Piece) -> str:
        """
        Replace an expression with a collision-checked symbolic scalar.

        Args:
            piece (Piece): Source-bearing expression.

        Returns:
            str: Internal marker consumed only by this layout analysis.
        """
        token = f"HHINPUTDOMAINMARKER{len(self.markers)}"
        self.markers[token] = piece
        return token

    def line(self, state: Position, piece: Piece) -> None:
        """
        Consume one physical block-YAML line and update its enclosing field path.

        Args:
            state (Position): Current indentation and resource.
            piece (Piece): Source location of the consumed line.

        Returns:
            None: Known field values are retained; opaque structure marks only its containing subtree.
        """
        raw, state.line = state.line, ""
        content = raw.lstrip(" ")
        indent = len(raw) - len(content)
        if not content or content.startswith("#"):
            return
        if state.block is not None and indent > state.block:
            return
        state.block = None
        if content in {"---", "..."} and indent == 0:
            state.document = self.new_document()
            state.frames = []
            return
        sequence = content.startswith("- ") or content == "-"
        while state.frames and (state.frames[-1][0] > indent or state.frames[-1][0] == indent and (not sequence or state.frames[-1][2])):
            state.frames.pop()
        parent = state.frames[-1][1] if state.frames else ()
        if sequence:
            parent = (*parent, "*")
            state.frames.append((indent, parent, True))
            indent += 2
            content = content[1:].lstrip()
            if re.fullmatch(r"[|>][+-]?[0-9]?(?:\s+#.*)?", content):
                state.block = indent - 2
                return
        if content in self.markers:
            selected = self.markers[content]
            if not parent or isinstance(selected.value, Operation) and selected.value.name in {"unknown", "unresolved"}:
                state.document.barriers.append(parent)
            else:
                if not sequence:
                    selected = Piece(Operation("yaml-fragment", (selected.value,)), selected.file, selected.line)
                state.document.fields.append((parent, selected, state.conditions))
            return
        match = re.fullmatch(r"""((?:[A-Za-z_][A-Za-z_0-9./-]*|"[^"\\]*"|'[^']*')):\s*(.*)""", content)
        if match is None:
            if "HHINPUTDOMAINMARKER" in content or content.startswith(("<<:", "&", "*", "{", "[")):
                state.document.barriers.append(parent)
            return
        key, raw_value = match.groups()
        if "HHINPUTDOMAINMARKER" in key:
            selected_key = self.markers.get(key.strip('"'))
            alternatives = literals(selected_key.value) if selected_key is not None else set()
            if alternatives:
                state.document.barriers.extend((*parent, candidate) for candidate in alternatives)
            else:
                state.document.barriers.append(parent)
            # Retain the indentation frame while withholding the unresolved key.
            # Its children cannot borrow a sibling's destination schema.
            if not raw_value:
                state.frames.append((indent, (*parent, key), False))
            return
        key = key[1:-1] if key[:1] in {'"', "'"} else key
        path = (*parent, key)
        if not raw_value or raw_value.startswith("#"):
            state.frames.append((indent, path, False))
            return
        if re.fullmatch(r"[|>][+-]?[0-9]?(?:\s+#.*)?", raw_value):
            state.block = indent
            return
        token = raw_value.strip('"')
        if token in self.markers:
            selected = self.markers[token]
            if raw_value.startswith('"'):
                selected = Piece(Operation("quote", (selected.value,)), selected.file, selected.line)
        else:
            try:
                value = yamlio.load(raw_value)
            except Exception:
                state.document.barriers.append(path)
                return
            if isinstance(value, str) and "HHINPUTDOMAINMARKER" in value:
                return  # Concatenation is not an identity mapping.
            selected = Piece(value, piece.file, piece.line)
        if path in {("apiVersion",), ("kind",)}:
            state.document.identities.setdefault(path[0], []).append(selected.value)
        else:
            state.document.fields.append((path, selected, state.conditions))

    def text(self, text: str, state: Position, piece: Piece, padding: int = 0) -> None:
        """
        Feed literal output through the line parser, preserving indentation introduced by nindent.

        Args:
            text (str): Literal or marker text.
            state (Position): Current output location.
            piece (Piece): Source location.
            padding (int): Prefix inserted after every output newline.

        Returns:
            None: Complete lines are consumed; a final partial line remains buffered.
        """
        lines = text.split("\n")
        if not state.line:
            state.line = " " * padding
        state.line += lines[0]
        for suffix in lines[1:]:
            self.line(state, piece)
            state.line = " " * padding + suffix

    def emit(self, piece: Piece, state: Position, padding: int = 0) -> None:
        """
        Traverse output branches independently and join their structural context.

        Args:
            piece (Piece): Symbolic output with source coordinates.
            state (Position): Enclosing output location.
            padding (int): Indentation imposed by an outer formatter.

        Returns:
            None: Fields are recorded with guards instead of multiplying independent branches.

        Raises:
            ValueError: The output traversal or indentation budget is exceeded.
        """
        self.steps += 1
        if self.steps > self.limits["max_discovery_nodes"]:
            raise ValueError(f"projection layout exceeds compiler.max_discovery_nodes={self.limits['max_discovery_nodes']}")
        value = normalize(piece.value)
        if isinstance(value, Operation):
            for reason in unresolved(value):
                self.notes.append({"file": piece.file, "line": piece.line, "reason": reason})
            if value.name == "unresolved" and padding == 0:
                state.document.barriers.append(())
        if isinstance(value, str):
            self.text(value, state, piece, padding)
            return
        if isinstance(value, Operation):
            name, args = value.name, value.arguments
            if name == "render-text":
                self.emit(Piece(args[0], piece.file, piece.line), state, padding)
                return
            if name == "fail":
                # fail aborts rendering and never emits its message into YAML.
                # Rejection analysis and native Helm retain ownership of the error.
                return
            if name == "text":
                for child in args:
                    if isinstance(child, Piece):
                        self.emit(child, state, padding)
                return
            if name in {"indent", "nindent"} and len(args) == 2 and type(args[0]) is int:
                width = args[0]
                if not 0 <= width <= self.limits["max_indent_width"]:
                    raise ValueError(f"indentation exceeds compiler.max_indent_width={self.limits['max_indent_width']}")
                self.text(("\n" if name == "nindent" else "") + " " * width, state, piece, padding)
                self.emit(Piece(args[1], piece.file, piece.line), state, padding + width)
                return
            if name == "choose" and len(args) == 3 and not scalar(value):
                branches = [
                    Position(state.document, list(state.frames), state.line, state.block, (*state.conditions, condition))
                    for condition in (args[0], Operation("not", (args[0],)))
                ]
                for branch, child in zip(branches, args[1:], strict=True):
                    self.emit(Piece(child, piece.file, piece.line), branch, padding)
                    if branch.line.strip():
                        self.line(branch, piece)
                        branch.line = " " * padding
                common = []
                for first, second in zip(branches[0].frames, branches[1].frames, strict=False):
                    if first != second:
                        break
                    common.append(first)
                state.frames = common
                state.line = branches[0].line if branches[0].line == branches[1].line else " " * padding
                state.block = branches[0].block if branches[0].block == branches[1].block else None
                if branches[0].document is not branches[1].document:
                    state.document = self.new_document()
                return
        self.text(self.marker(Piece(value, piece.file, piece.line)), state, piece, padding)

    def collect(self, pieces: list[Piece]) -> list[dict[str, object]]:
        """
        Build guarded destination constraints from independently established fields.

        Args:
            pieces (list[Piece]): Expanded root-template output.

        Returns:
            list[dict[str, object]]: Input-domain rules with source and API-schema provenance.
        """
        state = Position(self.new_document())
        for piece in pieces:
            self.emit(piece, state)
        if pieces:
            self.line(state, pieces[-1])
        result: list[dict[str, object]] = []
        for document in self.documents:
            version_choices = [literals(value) for value in document.identities.get("apiVersion", [])]
            kind_choices = [literals(value) for value in document.identities.get("kind", [])]
            if not version_choices or not kind_choices or not all((*version_choices, *kind_choices)):
                continue
            versions = set().union(*version_choices)
            kinds = set().union(*kind_choices)
            if len(versions) * len(kinds) > self.limits["max_symbolic_variants"]:
                self.notes.append({"reason": "resource identity alternatives exceed compiler.max_symbolic_variants"})
                continue
            identities = [f"{version}/{kind}" for version, kind in itertools.product(sorted(versions), sorted(kinds))]
            if not identities:
                continue
            for path, piece, conditions in document.fields:
                if not path or any(path[: len(barrier)] == barrier for barrier in document.barriers):
                    continue
                global_conditions = [condition for condition in conditions if not any("*" in path for path in input_origins(condition))]
                exact_guards = [predicate(condition) for condition in global_conditions]
                guards = [guard_bounds(condition)[0] for condition in global_conditions]
                if {"not": {}} in guards:
                    self.notes.append(
                        {"file": piece.file, "line": piece.line, "reason": "unresolved activation guard; field domain unchanged"}
                    )
                    continue
                if any(guard is None for guard in exact_guards):
                    self.notes.append(
                        {"file": piece.file, "line": piece.line, "reason": "partial guard; domain applies only in established regions"}
                    )
                matches = [destination(identity, path) for identity in identities]
                if not matches or any(match is None for match in matches):
                    continue
                schemas = [match[0] for match in matches if match is not None]
                if any(schema != schemas[0] for schema in schemas[1:]):
                    continue
                found = constraints(piece.value, schemas[0], conditions=conditions)
                for rule in found:
                    result.append(
                        {
                            **rule,
                            "destination": f"{identities[0]}:$.{'.'.join(path)}",
                            "file": piece.file,
                            "line": piece.line,
                            "source": next(match[1] for match in matches if match is not None),
                        }
                    )
                if not found and isinstance(piece.value, Input | Operation | LocalMap):
                    self.notes.append(
                        {
                            "file": piece.file,
                            "line": piece.line,
                            "reason": "unsupported output transformation; field domain unchanged",
                            "destination": list(path),
                        }
                    )
        return result


def scalar(value: object) -> bool:
    """
    Distinguish inline expression choices from conditional blocks containing YAML lines.

    Args:
        value (object): Symbolic output.

    Returns:
        bool: Every output branch occupies a single symbolic scalar position.
    """
    if isinstance(value, str):
        return "\n" not in value
    if isinstance(value, Operation) and value.name == "choose":
        return all(scalar(branch) for branch in value.arguments[1:])
    if isinstance(value, Operation) and value.name == "text":
        return all(isinstance(piece, Piece) and scalar(piece.value) for piece in value.arguments)
    if isinstance(value, Operation) and value.name == "render-text":
        return scalar(value.arguments[0])
    if isinstance(value, Operation) and value.name == "indent":
        return scalar(value.arguments[-1])
    return not isinstance(value, Operation) or value.name not in {"text", "nindent"}


def literals(value: object) -> set[str]:
    """
    Collect a closed set of literal resource identities, refusing unknown alternatives.

    Args:
        value (object): Symbolic apiVersion or kind output.

    Returns:
        set[str]: Every possible literal identity component, or an empty set for unknown output.
    """
    if isinstance(value, str):
        return {value.strip()}
    if isinstance(value, Operation) and value.name == "render-text":
        return literals(value.arguments[0])
    if isinstance(value, Operation) and value.name == "choose":
        branches = [literals(branch) for branch in value.arguments[1:]]
        return set.union(*branches) if all(branches) else set()
    return set()


def unresolved(value: object) -> set[str]:
    """
    Preserve failed helper diagnostics through enclosing output formatters.

    Args:
        value (object): Symbolic expression or source-bearing fragment.

    Returns:
        set[str]: Distinct unresolved helper reasons without inspecting unused context arguments.
    """
    if isinstance(value, Piece):
        return unresolved(value.value)
    if not isinstance(value, Operation):
        return set()
    if value.name == "unresolved":
        return {str(value.arguments[0])}
    arguments = value.arguments[:1] if value.name == "tpl" else value.arguments
    return set().union(*(unresolved(argument) for argument in arguments))
