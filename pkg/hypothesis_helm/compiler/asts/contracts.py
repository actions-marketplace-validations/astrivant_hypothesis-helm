"""
Evaluate explicit template rejection contracts without interpreting arbitrary Helm code.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import subprocess
import tarfile
from functools import lru_cache
from operator import eq, ge, gt, le, lt, ne
from pathlib import Path

from attrs import define, evolve, field, frozen
from ruamel.yaml.error import YAMLError

from hypothesis_helm.compiler.asts.contract_scope import UNRESOLVED, LoopControl, Scope
from hypothesis_helm.compiler.asts.contract_values import (
    BoundValue,
    ConstantList,
    ConstantMap,
    ContractText,
    DerivedValue,
    KeyList,
    UnorderedKeys,
    native,
)
from hypothesis_helm.compiler.asts.renderer import APIVersions, ContextReference, FileSet, FixedFields, RendererContext, Unavailable
from hypothesis_helm.compiler.asts.templates import Node, lower, walk
from hypothesis_helm.compiler.asts.transformations import FUNCTIONS, TransformedDomain, UnsupportedTransformation, calculate, inputs
from hypothesis_helm.compiler.builtins import EFFECTS, MUTATIONS, NATIVE_STATE
from hypothesis_helm.compiler.limits import active_limits, call_depth
from hypothesis_helm.compiler.passes.dependencies import Dependencies, lookup

TOKENS = re.compile(r'\s*("(?:\\.|[^"\\])*"|`[^`]*`|[()|]|[^\s()|]+)')
ASSIGNMENT = re.compile(r"(\$\w+)\s*(:=|=)\s*(.*)", re.DOTALL)
RANGE_ASSIGNMENT = re.compile(r"(\$\w+)(?:\s*,\s*(\$\w+))?\s*(:=|=)\s*(.*)", re.DOTALL)
LOGGER = logging.getLogger(__name__)


def declares_path(schema: object, path: tuple[str, ...]) -> bool:
    """
    Preserve explicitly authored domains and ambiguous schema relationships.

    Args:
        schema (object): Original authored schema, before inference from values.
        path (tuple[str, ...]): Field relative to this schema's chart.

    Returns:
        bool: A declaration or an unresolved schema relationship may constrain this field.
    """
    if not isinstance(schema, dict):
        return schema is not True
    if not path:
        return True
    if any(
        key in schema
        for key in (
            "$ref",
            "$dynamicRef",
            "$recursiveRef",
            "allOf",
            "anyOf",
            "oneOf",
            "not",
            "if",
            "then",
            "else",
            "dependencies",
            "dependentSchemas",
            "dependentRequired",
            "unevaluatedProperties",
            "enum",
            "const",
        )
    ):
        return True
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        return True
    if path[0] in properties:
        return declares_path(properties[path[0]], path[1:])
    if schema.get("patternProperties"):
        return True
    additional = schema.get("additionalProperties", True)
    return declares_path(additional, path[1:]) if isinstance(additional, dict) else additional is not True


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
class FieldAccess:
    """
    Select fields from a parenthesized expression without treating them as call arguments.

    Attributes:
        receiver (object): Expression producing the selected context.
        fields (tuple[str, ...]): Consecutive dot-separated field names.
    """

    receiver: object
    fields: tuple[str, ...]


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


@lru_cache(maxsize=8192)
def expression(source: str) -> object:
    """
    Parse prefix calls, parenthesized arguments, and pipelines into nested tuples.

    Args:
        source (str): One Go-template expression.

    Returns:
        object: Literal token or a nested call tuple.

    Raises:
        Unknown: Tokens or parentheses are malformed.
    """
    matches = list(TOKENS.finditer(source))
    tokens = [match[1] for match in matches]
    position = 0

    def pipeline() -> object:
        """
        Parse calls until a parenthesis or the end of the expression.

        Returns:
            object: Nested expression with pipeline arguments appended last.
        """
        nonlocal position
        result: object = None
        while True:
            parts: list[object] = []
            while position < len(tokens) and tokens[position] not in (")", "|"):
                token = tokens[position]
                position += 1
                if token == "(":
                    item = pipeline()
                    if position >= len(tokens) or tokens[position] != ")":
                        raise Unknown("unbalanced expression")
                    position += 1
                    if (
                        position < len(tokens)
                        and matches[position - 1].end(1) == matches[position].start(1)
                        and tokens[position].startswith(".")
                    ):
                        selector = tokens[position]
                        if not re.fullmatch(r"(?:\.[A-Za-z_][A-Za-z_0-9]*)+", selector):
                            raise Unknown("unsupported parenthesized field selector")
                        item = FieldAccess(item, tuple(selector[1:].split(".")))
                        position += 1
                    parts.append(item)
                else:
                    parts.append(token)
            if not parts:
                raise Unknown("empty expression")
            if result is not None:
                parts.append(result)
            result = parts[0] if len(parts) == 1 else tuple(parts)
            if position >= len(tokens) or tokens[position] != "|":
                return result
            position += 1

    result = pipeline()
    if position != len(tokens):
        raise Unknown("trailing expression")
    return result


def calls(expr: object) -> set[str]:
    """
    Traverse expression call nodes, ignoring string literals and comments.

    Args:
        expr (object): Parsed expression AST.

    Returns:
        set[str]: Function names and statically named helper-call edges.
    """
    if isinstance(expr, FieldAccess):
        return calls(expr.receiver)
    if isinstance(expr, str) and expr in NATIVE_STATE:
        return {expr}
    if not isinstance(expr, tuple) or not expr:
        return set()
    result = {str(expr[0])}
    if expr[0] in {"include", "template", "block"} and len(expr) in {2, 3} and isinstance(expr[1], str) and expr[1].startswith('"'):
        try:
            result.add("include:" + json.loads(expr[1]))
        except (ValueError, TypeError):
            pass
    if isinstance(expr[0], FieldAccess):
        result.update(calls(expr[0]))
    for argument in expr[1:]:
        result.update(calls(argument))
    return result


def context_effects(nodes: tuple[Node, ...]) -> bool:
    """
    Detect direct operations that could change the context of a later rejection.

    Args:
        nodes (tuple[Node, ...]): Statements preceding the candidate rejection.

    Returns:
        bool: Mutation or dynamic evaluation prevents a supported local prediction.
    """
    for node in walk(nodes):
        if node.kind != "text":
            assignment = ASSIGNMENT.fullmatch(node.text)
            functions = calls(expression(assignment[3] if assignment else node.text))
            if functions & (MUTATIONS | {"call"}):
                return True
    return False


@lru_cache(maxsize=128)
def tpl_nodes(text: str) -> tuple[Node, ...]:
    """
    Parse concrete tpl source without sharing mutable candidate state.

    Args:
        text (str): Already evaluated template string.

    Returns:
        tuple[Node, ...]: Immutable syntax nodes reused for identical strings.
    """
    return lower(text)


@define
class Contracts:
    """
    Hold parsed local helpers and root templates with explicit rejection sinks.

    Attributes:
        helpers (dict[str, tuple[str, tuple[Node, ...]]]): Unique local helper definitions.
        roots (dict[str, tuple[Node, ...]]): Executed chart templates, excluding partials.
        relevant (set[str]): Helpers transitively containing explicit rejection calls.
        explicit_relevant (set[str]): Helpers with statically visible fail or required calls, excluding possible dynamic code.
        diagnostics (list[str]): Unsupported or ambiguous source constructs.
        dependencies (Dependencies): Child namespaces and activation conditions.
        scopes (dict[str, tuple[str, ...]]): Values namespace for each root template.
        schemas (dict[tuple[str, ...], object]): Original authored schemas indexed by chart namespace.
        variable_uses (dict[str, set[str]]): Source-stable alias dependencies computed once per root template.
        max_call_depth (int): Maximum nested helper calls for this chart's analysis.
        chart (Path | None): Source chart used to resolve warning suppression.
        renderer (RendererContext | None): Exact fixed render context, attached by the executor.
        fallbacks (list[dict[str, object]]): Distinct unsupported evaluations, including suppressed warnings.
        incomplete_evaluations (int): Incomplete predictions, including repeated inputs and repair probes.
        fail_fast (bool): Stop on an unsuppressed compiler warning when requested by the executor.
        templates (dict[str, tuple[Node, ...]]): All parsed template bodies for statically resolved filename includes.
        limits (dict[str, int]): Resource budgets captured before evaluating candidates.
    """

    helpers: dict[str, tuple[str, tuple[Node, ...]]] = field(factory=dict)
    roots: dict[str, tuple[Node, ...]] = field(factory=dict)
    relevant: set[str] = field(factory=set)
    explicit_relevant: set[str] = field(factory=set)
    diagnostics: list[str] = field(factory=list)
    dependencies: Dependencies = field(factory=Dependencies)
    scopes: dict[str, tuple[str, ...]] = field(factory=dict)
    schemas: dict[tuple[str, ...], object] = field(factory=dict)
    variable_uses: dict[str, set[str]] = field(factory=dict)
    max_call_depth: int = field(factory=call_depth)
    chart: Path | None = None
    renderer: RendererContext | None = None
    fallbacks: list[dict[str, object]] = field(factory=list)
    incomplete_evaluations: int = 0
    fail_fast: bool = False
    templates: dict[str, tuple[Node, ...]] = field(factory=dict)
    limits: dict[str, int] = field(factory=active_limits, kw_only=True)

    def configure(self, *, helm: str, kube_version: str | None, timeout: float, release: str, namespace: str, fail_fast: bool) -> None:
        """
        Attach actual render settings while reusing chart-local native context across paths.

        Args:
            helm (str): The executor's Helm binary.
            kube_version (str | None): The executor's Kubernetes capability override.
            timeout (float): Deadline for context probes.
            release (str): Fixed release name.
            namespace (str): Fixed release namespace.
            fail_fast (bool): Stop on an enabled incomplete-analysis warning.

        Returns:
            None: Subsequent predictions use matching native context and finding policy.
        """
        previous = self.renderer
        if self.chart is not None and (
            previous is None
            or (previous.helm, previous.kube_version, previous.timeout, previous.release, previous.namespace)
            != (helm, kube_version, timeout, release, namespace)
        ):
            self.renderer = RendererContext(
                self.chart,
                {node.path: node.name for node in self.dependencies.nodes},
                helm,
                kube_version,
                timeout,
                release,
                namespace,
                limits=self.limits,
            )
        self.fail_fast = fail_fast

    @classmethod
    def build(cls, chart: Path, dependencies: Dependencies | None = None) -> Contracts:
        """
        Parse local helpers conservatively; duplicate definitions remain unresolved.

        Args:
            chart (Path): Prepared chart directory.
            dependencies (Dependencies | None): Already discovered children to reuse without reopening archives.

        Returns:
            Contracts: Immutable source nodes with explicit unsupported-source diagnostics.
        """
        limits = dict(dependencies.limits) if dependencies is not None else active_limits(chart)
        result = cls(
            dependencies=dependencies if dependencies is not None else Dependencies.build(chart),
            chart=chart,
            limits=limits,
            max_call_depth=limits["max_call_depth"],
        )
        if (chart / "values.schema.json").is_file():
            result.schemas[()] = json.loads((chart / "values.schema.json").read_text())
        duplicates: set[str] = set()
        sources: list[tuple[str, tuple[Node, ...], tuple[str, ...]]] = []
        for path in sorted((chart / "templates").rglob("*")):
            if not path.is_file():
                continue
            source = path.relative_to(chart).as_posix()
            try:
                nodes = lower(path.read_text())
            except (ValueError, UnicodeError, RecursionError) as exc:
                result.diagnostics.append(f"{source}: {exc}")
                continue
            sources.append((source, nodes, ()))
        for dependency in result.dependencies.nodes:
            sources.extend((source, nodes, dependency.path) for source, nodes in dependency.syntax)
            if dependency.declared_schema:
                result.schemas[dependency.path] = dependency.schema
        for source, nodes, scope in sources:
            result.templates[source] = nodes
            result.scopes[source] = scope
            for node in walk(nodes):
                match = re.match(r'(?:define|block)\s+"([^"\\]+)"(?:\s|$)', node.text) if node.kind == "opaque" else None
                if match:
                    name = match[1]
                    if name in result.helpers and result.helpers[name][1] != node.children:
                        duplicates.add(name)
                    result.helpers[name] = (source, node.children)
            if not Path(source).name.startswith("_"):
                result.roots[source] = tuple(node for node in nodes if not node.text.startswith("define "))
                result.scopes[source] = scope
        for name in duplicates:
            result.helpers.pop(name, None)
            result.diagnostics.append(f"Duplicate helper left unresolved: {name}")
        for _ in range(len(result.helpers) + 1):
            previous = (set(result.relevant), set(result.explicit_relevant))
            for name, (_, nodes) in result.helpers.items():
                if result.interesting(nodes):
                    result.relevant.add(name)
                if result.interesting(nodes, dynamic=False):
                    result.explicit_relevant.add(name)
            if (result.relevant, result.explicit_relevant) == previous:
                break
        result.roots = {name: nodes for name, nodes in result.roots.items() if result.interesting(nodes)}
        result.variable_uses = {name: result.variables(nodes) for name, nodes in result.roots.items()}
        return result

    def interesting(self, nodes: tuple[Node, ...], *, dynamic: bool = True) -> bool:
        """
        Locate explicit rejection expressions or calls into relevant helpers.

        Args:
            nodes (tuple[Node, ...]): Current template region.
            dynamic (bool): Include operations that may conceal runtime rejection behavior.

        Returns:
            bool: Whether the region may execute a recognized rejection contract.
        """
        for node in walk(nodes):
            if node.kind == "text":
                continue
            assignment = ASSIGNMENT.fullmatch(node.text)
            try:
                found = calls(expression(assignment[3] if assignment else node.text))
            except (Unknown, RecursionError):
                continue
            relevant = self.relevant if dynamic else self.explicit_relevant
            if (
                found & {"fail", "required"}
                or (dynamic and found & (EFFECTS["dynamic-code"] | NATIVE_STATE))
                or any("include:" + name in found for name in relevant)
            ):
                return True
        return False

    def predict(self, values: dict[str, object]) -> Rejection | None:
        """
        Evaluate supported contracts; unknown expressions never establish a rejection.

        Args:
            values (dict[str, object]): Effective coalesced Helm values.

        Returns:
            Rejection | None: Evaluated rejection, or no established rejection.
        """
        if self.diagnostics:
            self.incomplete_evaluations += 1
            for diagnostic in self.diagnostics:
                self.fallback(Unknown(diagnostic), "chart sources", {})
            return None
        effective = self.dependencies.context({}, values)
        states = self.dependencies.states({}, values)
        incomplete = False
        for source, nodes in self.roots.items():
            scope = self.scopes.get(source, ())
            if scope and states.get(scope) is not True:
                continue
            local = lookup(effective, scope)
            if not isinstance(local, dict):
                continue
            context: dict[str, object] = {
                "Values": BoundValue(local, scope),
                "Capabilities": ContextReference(self.renderer, "Capabilities"),
                "Files": ContextReference(self.renderer, "Files", scope),
                "Chart": ContextReference(self.renderer, "Chart", scope),
                "Template": ContextReference(self.renderer, "Template", scope, source),
            }
            if self.renderer is not None:
                context["Release"] = {
                    "Name": self.renderer.release,
                    "Namespace": self.renderer.namespace,
                    "IsInstall": True,
                    "IsUpgrade": False,
                    "Revision": 1,
                    "Service": "Helm",
                }
            evaluator = Evaluation(self, effective, context=context, scope=scope, needed=self.variable_uses[source])
            try:
                evaluator.visit(nodes, source, Scope({"$": evaluator.context}), strict=False)
                incomplete |= evaluator.incomplete
            except Rejection as rejection:
                if incomplete:
                    rejection = evolve(rejection, contextual=True)
                inferred_paths = {
                    *(tuple(name.removeprefix("$.").split(".")) for name in rejection.enums),
                    *(path for domain in rejection.transformed_domains for path in inputs(domain.expression)),
                }
                declared = (
                    any(
                        path[: len(namespace)] == namespace and declares_path(schema, path[len(namespace) :])
                        for path in inferred_paths
                        for namespace, schema in self.schemas.items()
                    )
                    if inferred_paths
                    else any(scope[: len(namespace)] == namespace for namespace in self.schemas)
                )
                if declared:
                    return evolve(rejection, declared_schema=True)
                return rejection
            except (Unknown, TypeError, KeyError, IndexError, OverflowError, RecursionError) as exc:
                incomplete = True
                self.fallback(exc, source, evaluator.inputs)
        if incomplete:
            self.incomplete_evaluations += 1
        return None

    def fallback(self, error: Exception, source: str, observed: dict[str, object]) -> None:
        """
        Explain incomplete analysis before rendering, without excluding the candidate.

        Args:
            error (Exception): Unsupported evaluator operation with optional source coordinates.
            source (str): Root template when no more precise location is available.
            observed (dict[str, object]): Values paths read before the analysis stopped.

        Returns:
            None: A deduplicated diagnostic is retained and an enabled warning is logged.
        """
        from hypothesis_helm.rules import RenderFailure, ignored

        source = getattr(error, "source", None) or source
        line = getattr(error, "line", 0)
        reason = str(error) if isinstance(error, Unknown) else f"unsupported evaluator operation ({type(error).__name__})"
        paths = tuple(tuple(path.removeprefix("$.").split(".")) for path in observed)
        suppressed = ignored("HH2007", chart=self.chart, paths=paths)
        record: dict[str, object] = {
            "code": "HH2007",
            "source": source,
            "line": line,
            "reason": reason,
            "suppressed": suppressed,
            "action": "defer unsupported analysis to native Helm; no exclusion based on this result",
        }
        message = f"{source}:{line}: {reason}; affected expressions retained for Helm rendering; no pruning based on this result"
        if record not in self.fallbacks:
            if len(self.fallbacks) < self.limits["max_fallbacks"]:
                self.fallbacks.append(record)
                if not suppressed:
                    LOGGER.warning(
                        "[HH2007] Compiler analysis incomplete: chart=%s; %s",
                        self.chart,
                        message,
                        extra={"diagnostic_key": json.dumps([str(self.chart), source, line, reason])},
                    )
        if self.fail_fast and not suppressed:
            raise RenderFailure(message, "HH2007")

    def variables(self, nodes: tuple[Node, ...]) -> set[str]:
        """
        Find aliases that can affect a rejection through assignments or enclosing guards.

        Args:
            nodes (tuple[Node, ...]): Complete root template before candidate evaluation.

        Returns:
            set[str]: Conservative variable dependencies, including shadowed names.
        """
        needed: set[str] = set()
        assignments: list[tuple[set[str], set[str]]] = []

        def names(text: str) -> set[str]:
            """
            Collect lexical variable references while ignoring quoted text.

            Args:
                text (str): Template action or pipeline.

            Returns:
                set[str]: Referenced variable names.
            """
            return {token.split(".")[0].rstrip(",") for token in TOKENS.findall(text) if token.startswith("$")}

        def visit(items: tuple[Node, ...], guards: set[str]) -> None:
            """
            Retain the control dependencies of each variable definition.

            Args:
                items (tuple[Node, ...]): Current lexical block.
                guards (set[str]): Variables controlling entry into this block.

            Returns:
                None: Dependency edges and rejection roots are collected.
            """
            for node in items:
                if node.kind == "text":
                    continue
                references = names(node.text)
                if self.interesting((node,)):
                    needed.update(references | guards)
                text = node.text.split(" ", 1)[1] if node.text.startswith(("with ", "range ")) else node.text
                binding = RANGE_ASSIGNMENT.fullmatch(text)
                if binding:
                    assigned = {name for name in (binding[1], binding[2]) if name}
                    assignments.append((assigned, names(binding[4]) | guards))
                visit(node.children, guards | references)
                visit(node.otherwise, guards | references)

        visit(nodes, set())
        for _ in range(len(assignments) + 1):
            previous = set(needed)
            for assigned, sources in assignments:
                if assigned & needed:
                    needed.update(sources)
            if needed == previous:
                break
        return needed


@define
class Evaluation:
    """
    Evaluate a closed validator subset with candidate-local variables and evidence.

    Attributes:
        contracts (Contracts): Parsed source and helper definitions.
        values (dict[str, object]): Effective chart input.
        inputs (dict[str, object]): Inspected concrete values paths.
        conditions (list[str]): Conditions traversed by the validator.
        depth (int): Bounded helper recursion depth.
        context (object): Current helper argument; dollar and dot reset together at each include.
        enums (dict[str, tuple[str, ...]]): Literal allowlists observed on active rejecting conditions.
        scope (tuple[str, ...]): Chart namespace retained across helper context changes.
        steps (int): Statements and iterations consumed by this bounded analysis.
        loops (int): Active lexical ranges in the current template invocation.
        needed (set[str]): Root aliases that can influence an explicit rejection.
        transformed_domains (list[TransformedDomain]): Branch-local transformed membership observations.
        transformed (bool): Whether this prediction used modeled transformations.
        contextual (bool): Whether this prediction depends on native context or concrete tpl evaluation.
        incomplete (bool): An unrelated root output was left to Helm; later predictions require native verification.
        declared_globals (bool): A forwarded global read is constrained by an authored dependency schema.
    """

    contracts: Contracts
    values: dict[str, object]
    inputs: dict[str, object] = field(factory=dict)
    conditions: list[str] = field(factory=list)
    depth: int = 0
    context: object = None
    enums: dict[str, tuple[str, ...]] = field(factory=dict)
    scope: tuple[str, ...] = ()
    steps: int = 0
    loops: int = 0
    needed: set[str] = field(factory=set)
    transformed_domains: list[TransformedDomain] = field(factory=list)
    transformed: bool = False
    contextual: bool = False
    incomplete: bool = False
    declared_globals: bool = False

    def context_value(self, value: object) -> object:
        """
        Resolve deferred native data while preserving explicit analysis uncertainty.

        Args:
            value (object): Current context value or a lazy native reference.

        Returns:
            object: Loaded fixed context, or the unchanged ordinary value.
        """
        if not isinstance(value, ContextReference):
            return value
        self.contextual = True
        try:
            return value.value()
        except (Unavailable, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, tarfile.TarError, YAMLError) as exc:
            raise Unknown(str(exc) if isinstance(exc, Unavailable) else f"native context unavailable ({type(exc).__name__})") from exc

    def resolve(self, expression: str, variables: Scope) -> object:
        """
        Resolve dot, dollar and lexical aliases while retaining the original values path.

        Args:
            expression (str): Direct context or variable access.
            variables (Scope): Current lexical bindings, including the template root dollar.

        Returns:
            object: Literal or path-bound candidate value.

        Raises:
            Unknown: Lookup requires an unsupported context, field name or parent.
        """
        context = self.context
        if expression == ".":
            return context
        parts = expression.split(".")
        head = parts.pop(0)
        if head == "":
            current = context
        else:
            current = variables.lookup(head)
            if isinstance(current, Unknown):
                cause = Unknown(str(current))
                cause.source, cause.line = current.source, current.line
                raise cause
            if current is UNRESOLVED:
                raise Unknown(f"unbound variable: {head}")
        return self.select(current, tuple(parts))

    def select(self, current: object, parts: tuple[str, ...]) -> object:
        """
        Follow a field chain with the same provenance rules for direct and parenthesized access.

        Args:
            current (object): Resolved receiver, including candidate-bound values and native context.
            parts (tuple[str, ...]): Fields to select from the receiver.

        Returns:
            object: Selected value retaining input provenance.

        Raises:
            Unknown: A field or its receiver is outside the supported context model.
        """
        for index, key in enumerate(parts):
            current = self.context_value(current)
            if isinstance(current, FixedFields):
                if key not in current.values:
                    raise Unknown(f"unsupported fixed context field: {key}")
                current = current.values[key]
                continue
            container = native(current)
            if not isinstance(container, dict) or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", key):
                raise Unknown("unsupported context lookup")
            if key not in container and index != len(parts) - 1:
                raise Unknown("missing parent context lookup")
            current = BoundValue(container.get(key), (*current.path, key)) if isinstance(current, BoundValue) else container.get(key)
        if isinstance(current, BoundValue):
            current = self.observe(current)
        return self.context_value(current)

    def observe(self, value: BoundValue) -> BoundValue:
        """
        Attribute forwarded scalar globals to the highest-priority ancestor supplying that field.

        Args:
            value (BoundValue): Logical field read from an effective dependency context.

        Returns:
            BoundValue: Actual input origin, or a deferred aggregate whose members may have different origins.

        Raises:
            Unknown: Global origin cannot be established without interpreting incompatible parent containers.
        """
        path = value.path
        namespace = next(
            (node.path for node in self.contracts.dependencies.nodes if path[: len(node.path) + 1] == (*node.path, "global")), None
        )
        if namespace is not None:
            # Dependency coalescing remains native-verified for every predicted rejection.
            self.contextual = True
            self.declared_globals |= any(
                path[: len(scope)] == scope and declares_path(schema, path[len(scope) :])
                for scope, schema in self.contracts.schemas.items()
            )
            if isinstance(value.value, dict):
                # A merged map has no single writable origin. Resolve each selected
                # member later; whole-map observations can still be checked by Helm.
                return value
            suffix = path[len(namespace) + 1 :]
            for depth in range(len(namespace) + 1):
                origin = (*namespace[:depth], "global")
                container = lookup(self.values, origin)
                if not isinstance(container, dict):
                    continue
                for key in suffix:
                    if not isinstance(container, dict):
                        raise Unknown("forwarded global has incompatible ancestor containers")
                    if key not in container:
                        break
                    container = container[key]
                else:
                    if type(container) is not type(value.value) or container != value.value:
                        raise Unknown("forwarded global value differs from its candidate origin")
                    value = BoundValue(value.value, (*origin, *suffix))
                    break
            else:
                raise Unknown("forwarded global input origin is absent")
        if value.path:
            self.inputs["$." + ".".join(value.path)] = value.value
        return value

    def evaluate(self, expr: object, source: str, line: int, variables: Scope) -> object:
        """
        Evaluate supported expressions using Helm-compatible scalar and string semantics.

        Args:
            expr (object): Parsed expression tree.
            source (str): Template filename for diagnostics.
            line (int): Template line for diagnostics.
            variables (Scope): Lexically visible local bindings.

        Returns:
            object: Evaluated scalar, list, or helper output.

        Raises:
            Unknown: An expression, conversion, context, or function is unsupported.
            Rejection: An explicit fail or required call rejects this input.
        """
        if isinstance(expr, FieldAccess):
            return self.select(self.evaluate(expr.receiver, source, line, variables), expr.fields)
        if isinstance(expr, str):
            if expr.startswith((".", "$")):
                return self.resolve(expr, variables)
            if expr.startswith('"'):
                try:
                    return json.loads(expr)
                except ValueError as exc:
                    raise Unknown("unsupported quoted literal") from exc
            if expr.startswith("`") and expr.endswith("`"):
                return expr[1:-1]
            if expr in ("true", "false"):
                return expr == "true"
            if re.fullmatch(r"-?\d+", expr):
                return int(expr)
            if expr == "list":
                return ConstantList(())
            if expr == "dict":
                return ConstantMap({})
            if expr == "nil":
                return None
            raise Unknown(f"unsupported expression: {expr}")
        if not isinstance(expr, tuple) or not expr:
            raise Unknown("invalid expression")
        function, *arguments = expr
        if function in {"include", "template"}:
            if len(arguments) not in ({2} if function == "include" else {1, 2}):
                raise Unknown("include requires a name and context")
            name = native(self.evaluate(arguments[0], source, line, variables))
            helper = self.contracts.helpers.get(name) if isinstance(name, str) else None
            if helper is None and isinstance(name, str) and self.contracts.renderer is not None:
                states = self.contracts.dependencies.states({}, self.values)
                for template_source, body in self.contracts.templates.items():
                    scope = self.contracts.scopes[template_source]
                    if scope and states.get(scope) is not True:
                        continue
                    try:
                        template = self.contracts.renderer.template_context(scope, template_source)
                    except (Unavailable, OSError, ValueError, KeyError, subprocess.SubprocessError, tarfile.TarError) as exc:
                        raise Unknown("native template filename is unavailable") from exc
                    if template["Name"] == name:
                        helper = (template_source, body)
                        self.contextual = True
                        break
            if helper is None:
                raise Unknown("unknown or ambiguous helper")
            if self.depth >= self.contracts.max_call_depth:
                raise Unknown(f"helper call depth exceeds compiler limit {self.contracts.max_call_depth}")
            helper_source, nodes = helper
            context = self.evaluate(arguments[1], source, line, variables) if len(arguments) == 2 else None
            previous_context = self.context
            previous_loops = self.loops
            self.context = context
            self.loops = 0
            self.depth += 1
            try:
                return self.visit(nodes, helper_source, Scope({"$": context}), strict=True)
            finally:
                self.depth -= 1
                self.context = previous_context
                self.loops = previous_loops
        if function in ("and", "or"):
            if not arguments:
                raise Unknown("empty boolean call")
            result: object = None
            for argument in arguments:
                result = self.evaluate(argument, source, line, variables)
                if bool(native(result)) == (function == "or"):
                    break
            return result
        evaluated = [self.evaluate(argument, source, line, variables) for argument in arguments]
        args = [native(value) for value in evaluated]
        if function == "lookup" and len(args) == 4 and all(isinstance(value, str) for value in args):
            if self.contracts.renderer is not None and self.contracts.renderer.offline:
                self.contextual = True
                return ConstantMap({})
            raise Unknown("lookup requires a verified offline renderer context; cluster contents remain external")
        if function == "getHostByName" and len(args) == 1 and isinstance(args[0], str):
            if self.contracts.renderer is not None and not self.contracts.renderer.enable_dns:
                self.contextual = True
                return ""
            raise Unknown("DNS is external unless disabled by the verified renderer context")
        if function == "semverCompare" and len(args) == 2 and all(isinstance(value, str) for value in args):
            if self.contracts.renderer is None:
                raise Unknown("semverCompare requires the fixed Helm renderer context")
            self.contextual = True
            try:
                return self.contracts.renderer.semver_compare(str(args[0]), str(args[1]))
            except (Unavailable, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, YAMLError) as exc:
                raise Unknown(str(exc) if isinstance(exc, Unavailable) else "native version comparison unavailable") from exc
        if isinstance(function, FieldAccess) or (isinstance(function, str) and function.startswith((".", "$")) and "." in function):
            if isinstance(function, FieldAccess):
                method = function.fields[-1]
                target = self.select(self.evaluate(function.receiver, source, line, variables), function.fields[:-1])
            else:
                receiver, method = str(function).rsplit(".", 1)
                target = self.resolve(receiver, variables)
            if isinstance(target, APIVersions) and method == "Has" and len(args) == 1 and isinstance(args[0], str):
                self.contextual = True
                return args[0] in target.versions
            if isinstance(target, FileSet) and method in {"Get", "Lines"} and len(args) == 1 and isinstance(args[0], str):
                self.contextual = True
                try:
                    file_text = target.get(args[0])
                except Unavailable as exc:
                    raise Unknown(str(exc)) from exc
                return file_text if method == "Get" else ConstantList(tuple(file_text.removesuffix("\n").split("\n")) if file_text else ())
            raise Unknown(f"unsupported context method: {method}")
        if function == "tpl" and len(args) == 2:
            if not isinstance(args[0], str):
                raise Unknown("tpl requires a concrete string")
            if self.depth >= self.contracts.max_call_depth:
                raise Unknown(f"tpl call depth exceeds compiler limit {self.contracts.max_call_depth}")
            if len(args[0].encode("utf-8")) > self.contracts.limits["max_template_bytes"]:
                raise Unknown(f"tpl source exceeds compiler.max_template_bytes={self.contracts.limits['max_template_bytes']}")
            try:
                nodes = tpl_nodes(args[0])
            except (ValueError, RecursionError) as exc:
                raise Unknown("tpl source cannot be parsed by the compiler") from exc
            if any(node.kind == "opaque" and node.text.startswith(("define ", "block ")) for node in walk(nodes)):
                raise Unknown("tpl-local template definitions require native Helm evaluation")
            previous_context, previous_loops = self.context, self.loops
            self.context, self.loops = evaluated[1], 0
            self.depth += 1
            self.contextual = True
            try:
                return self.visit(nodes, f"{source}:{line} (tpl)", Scope({"$": self.context}), strict=True)
            finally:
                self.context, self.loops = previous_context, previous_loops
                self.depth -= 1
        if function == "fail" and len(args) == 1 and isinstance(args[0], str):
            text = evaluated[0] if isinstance(evaluated[0], ContractText) else None
            raise Rejection(
                source,
                line,
                args[0],
                dict(self.inputs),
                tuple(self.conditions),
                dict(self.enums),
                text,
                declared_schema=self.declared_globals,
                transformed_domains=tuple(self.transformed_domains),
                transformed=self.transformed,
                contextual=self.contextual,
            )
        if function == "required" and len(args) == 2 and isinstance(args[0], str):
            # Helm's required accepts false and zero; only nil and empty strings reject.
            if args[1] is None or args[1] == "":
                raise Rejection(
                    source,
                    line,
                    args[0],
                    dict(self.inputs),
                    tuple(self.conditions),
                    declared_schema=self.declared_globals,
                    transformed_domains=tuple(self.transformed_domains),
                    transformed=self.transformed,
                    contextual=self.contextual,
                )
            return args[1]
        if function in FUNCTIONS:
            try:
                result = calculate(str(function), tuple(evaluated), limits=self.contracts.limits)
            except UnsupportedTransformation as exc:
                raise Unknown(str(exc)) from exc
            self.transformed = True
            return DerivedValue(result, str(function), tuple(evaluated))
        if function in ("not", "empty") and len(args) == 1:
            return not bool(args[0])
        if function in ("eq", "ne", "lt", "le", "gt", "ge") and len(args) == 2:
            first, second = args
            if type(first) is not type(second) or type(first) not in (str, bool, int):
                raise Unknown("unsupported comparison types")
            if type(first) is bool and function not in ("eq", "ne"):
                raise Unknown("ordered Boolean comparison")
            assert isinstance(first, str | int) and isinstance(second, str | int)
            return {"eq": eq, "ne": ne, "lt": lt, "le": le, "gt": gt, "ge": ge}[str(function)](first, second)
        if function == "int" and len(args) == 1 and type(args[0]) is int:
            return evaluated[0]
        if function == "len" and len(args) == 1 and isinstance(args[0], str | list | dict):
            return len(args[0].encode("utf-8")) if isinstance(args[0], str) else len(args[0])
        if function == "list":
            if all(isinstance(item, str) and item.startswith(('"', "`")) for item in arguments):
                return ConstantList(tuple(str(value) for value in args))
            return evaluated
        if function == "dict" and len(args) % 2 == 0 and all(isinstance(key, str) for key in args[::2]):
            entries = {str(args[index]): evaluated[index + 1] for index in range(0, len(args), 2)}
            if all(isinstance(item, str) and item.startswith(('"', "`")) for item in arguments[::2]):
                return ConstantMap(entries)
            return entries
        if function == "hasKey" and len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], str):
            present = args[1] in args[0]
            if not present and isinstance(evaluated[0], ConstantMap) and isinstance(evaluated[1], BoundValue):
                self.enums["$." + ".".join(evaluated[1].path)] = tuple(sorted(args[0]))
            if not present and isinstance(evaluated[0], ConstantMap) and isinstance(evaluated[1], DerivedValue):
                self.transformed_domains.append(TransformedDomain(evaluated[1], tuple(sorted(args[0]))))
            return present
        if function in ("has", "mustHas") and len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], list):
            if not all(isinstance(item, str) for item in args[1]):
                raise Unknown("membership requires a string list")
            present = args[0] in args[1]
            if not present and isinstance(evaluated[0], BoundValue) and isinstance(evaluated[1], ConstantList):
                self.enums["$." + ".".join(evaluated[0].path)] = tuple(sorted(set(evaluated[1].values)))
            if not present and isinstance(evaluated[0], DerivedValue) and isinstance(evaluated[1], ConstantList):
                self.transformed_domains.append(TransformedDomain(evaluated[0], tuple(sorted(set(evaluated[1].values)))))
            return present
        if function == "keys" and len(args) == 1 and isinstance(args[0], dict) and all(isinstance(key, str) for key in args[0]):
            return UnorderedKeys(tuple(args[0]))
        if function == "sortAlpha" and len(args) == 1 and isinstance(args[0], list) and all(isinstance(item, str) for item in args[0]):
            return sorted(args[0])
        if function in ("index", "get") and len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], str):
            if isinstance(evaluated[0], BoundValue):
                path = (*evaluated[0].path, args[1])
                if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9-]*", args[1]):
                    raise Unknown("input key cannot be represented by a dotted contract path")
                value = args[0].get(args[1], "" if function == "get" else None)
                return self.observe(BoundValue(value, path))
            return args[0].get(args[1], "" if function == "get" else None)
        if function == "append" and len(args) == 2 and isinstance(args[0], list):
            return [*args[0], args[1]]
        if function == "without" and args and isinstance(args[0], list):
            return [item for item in args[0] if item not in args[1:]]
        if function == "join" and len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], list):
            if all(isinstance(item, str) for item in args[1]):
                if isinstance(evaluated[1], UnorderedKeys):
                    return ContractText((KeyList(args[0], evaluated[1].values),))
                return args[0].join(args[1])
        if function == "printf" and args and isinstance(args[0], str) and all(isinstance(item, str) for item in args[1:]):
            if args[0].count("%s") == len(args) - 1 and "%" not in args[0].replace("%s", ""):
                parts: list[str | KeyList] = []
                literals = args[0].split("%s")
                for literal, value in zip(literals, evaluated[1:], strict=False):
                    parts.append(literal)
                    parts.extend(value.parts if isinstance(value, ContractText) else (str(native(value)),))
                parts.append(literals[-1])
                return (
                    ContractText(tuple(parts)) if any(isinstance(part, KeyList) for part in parts) else "".join(str(part) for part in parts)
                )
        if function == "printf" and args and isinstance(args[0], str):
            pieces = re.split(r"(%s|%d|%%)", args[0])
            rendered: list[str] = []
            position = 1
            for piece in pieces:
                if piece == "%%":
                    rendered.append("%")
                elif piece in {"%s", "%d"}:
                    if position >= len(args):
                        raise Unknown("printf argument count does not match its format")
                    item = args[position]
                    if (piece == "%s" and not isinstance(item, str)) or (piece == "%d" and type(item) is not int):
                        raise Unknown("printf argument type does not match its format")
                    operand = evaluated[position]
                    if piece == "%d" and not (
                        type(operand) is int
                        or isinstance(operand, DerivedValue)
                        and operand.function in {"int", "int64", "atoi", "add", "add1", "sub", "mul", "min", "max"}
                    ):
                        raise Unknown("printf integer formatting requires an explicit integer conversion or known integer result")
                    if isinstance(evaluated[position], ContractText):
                        raise Unknown("mixed printf formatting with unordered output requires native evaluation")
                    rendered.append(str(item))
                    position += 1
                elif "%" in piece:
                    raise Unknown("unsupported printf format")
                else:
                    rendered.append(piece)
            if position != len(args) or sum(map(len, rendered)) > self.contracts.limits["max_string_chars"]:
                raise Unknown("printf output or argument count exceeds supported limits")
            self.transformed = True
            return "".join(rendered)
        raise Unknown(f"unsupported function: {function}")

    def pipeline(self, text: str, source: str, line: int, variables: Scope) -> object:
        """
        Evaluate a pipeline and its optional declaration or assignment.

        Args:
            text (str): Pipeline, optionally prefixed by a variable binding.
            source (str): Source filename.
            line (int): Source line number.
            variables (Scope): Lexical scope receiving the binding.

        Returns:
            object: Pipeline result, retaining input provenance.
        """
        assignment = ASSIGNMENT.fullmatch(text)
        value = self.evaluate(expression(assignment[3] if assignment else text), source, line, variables)
        if assignment:
            variables.bind(assignment[1], value, assign=assignment[2] == "=")
        return value

    def named_template(self, text: str, source: str, line: int, variables: Scope) -> str:
        """
        Invoke a statically named template with a separately parsed argument pipeline.

        Args:
            text (str): Template or block action including its quoted name.
            source (str): Source filename.
            line (int): Source line number.
            variables (Scope): Caller bindings used only to evaluate the argument.

        Returns:
            str: Supported helper output; the callee receives a fresh variable scope.
        """
        match = re.fullmatch(r'(?:template|block)\s+("(?:[^"\\]|\\.)*"|`[^`]*`)(?:\s+(.*))?', text, re.DOTALL)
        if match is None:
            raise Unknown("template requires a literal name")
        argument = expression(match[2]) if match[2] else "nil"
        result = self.evaluate(("template", match[1], argument), source, line, variables)
        if not isinstance(result, str):
            raise Unknown("unsupported template output")
        return result

    def control(self, node: Node, source: str, variables: Scope, *, strict: bool) -> str:
        """
        Evaluate an if or with block with lexical declarations and restored dot.

        Args:
            node (Node): Conditional or opaque with node.
            source (str): Source filename.
            variables (Scope): Enclosing scope, shared by assignments but not declarations.
            strict (bool): Require complete helper text when assembling a message.

        Returns:
            str: Text produced by the selected branch.
        """
        local = Scope(parent=variables)
        text = node.text if node.kind == "if" else node.text.removeprefix("with ")
        previous_context, previous_enums = self.context, dict(self.enums)
        previous_domains = list(self.transformed_domains)
        try:
            condition = self.pipeline(text, source, node.line, local)
            enabled = bool(native(condition))
            self.conditions.append(f"{source}:{node.line}: {text} => {enabled}")
            if node.kind == "opaque" and enabled:
                self.context = condition
            return self.visit(node.children if enabled else node.otherwise, source, local, strict=strict)
        finally:
            self.context, self.enums = previous_context, previous_enums
            self.transformed_domains = previous_domains

    def iteration(self, node: Node, source: str, variables: Scope, *, strict: bool) -> str:
        """
        Follow finite list or string-key map ranges within a shared statement budget.

        Args:
            node (Node): Opaque range node retaining its body and empty branch.
            source (str): Source filename.
            variables (Scope): Enclosing lexical environment.
            strict (bool): Require complete helper output when assembling messages.

        Returns:
            str: Concatenated iterations or the empty-range branch.
        """
        local = Scope(parent=variables)
        text = node.text.removeprefix("range ")
        binding = RANGE_ASSIGNMENT.fullmatch(text)
        value = self.evaluate(expression(binding[4] if binding else text), source, node.line, local)
        collection = native(value)
        if isinstance(value, UnorderedKeys):
            raise Unknown("range over unsorted keys has nondeterministic order")
        if collection is None:
            collection = []
        if not isinstance(collection, list | dict) or (isinstance(collection, dict) and not all(isinstance(k, str) for k in collection)):
            raise Unknown("range requires a finite list or string-key map")
        if len(collection) > self.contracts.limits["max_range_items"]:
            raise Unknown(f"range exceeds compiler.max_range_items={self.contracts.limits['max_range_items']}")
        names = [name for name in (binding[1], binding[2]) if name] if binding else []
        if binding:
            for name in names:
                local.bind(name, value, assign=binding[3] == "=")
        if not collection:
            return self.visit(node.otherwise, source, local, strict=strict)
        previous_context, previous_enums = self.context, dict(self.enums)
        previous_domains = list(self.transformed_domains)
        output: list[str] = []
        self.loops += 1
        try:
            keys = sorted(collection) if isinstance(collection, dict) else range(len(collection))
            for key in keys:
                self.steps += 1
                if self.steps > self.contracts.limits["max_steps"]:
                    raise Unknown(f"contract analysis statement budget exceeded: compiler.max_steps={self.contracts.limits['max_steps']}")
                element = collection[key]
                # Map fields retain editable paths. List members retain the collection's
                # already-recorded evidence without inventing a dotted numeric field.
                if isinstance(value, BoundValue) and isinstance(key, str) and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9-]*", key):
                    element = BoundValue(element, (*value.path, key))
                if binding:
                    for name, item in zip(names, [key, element] if len(names) == 2 else [element], strict=True):
                        local.bind(name, item, assign=binding[3] == "=")
                self.context, self.enums = element, dict(previous_enums)
                self.transformed_domains = list(previous_domains)
                try:
                    output.append(self.visit(node.children, source, Scope(parent=local), strict=strict))
                except LoopControl as jump:
                    output.append(jump.output)
                    if jump.action == "break":
                        break
        finally:
            self.loops -= 1
            self.context, self.enums = previous_context, previous_enums
            self.transformed_domains = previous_domains
        return "".join(output)

    def visit(self, nodes: tuple[Node, ...], source: str, variables: Scope, *, strict: bool) -> str:
        """
        Execute bounded validator control flow, leaving unsupported operations unresolved.

        Args:
            nodes (tuple[Node, ...]): Template region to evaluate.
            source (str): Template filename for diagnostics.
            variables (Scope): Lexical bindings; child blocks retain enclosing assignment ownership.
            strict (bool): Require every helper statement; root output is outside the contract.

        Returns:
            str: Exact supported helper text, including whitespace.

        Raises:
            Unknown: An executed validator construct cannot be interpreted.
        """
        output: list[str] = []
        try:
            for node in nodes:
                self.steps += 1
                if self.steps > self.contracts.limits["max_steps"]:
                    raise Unknown(f"contract analysis statement budget exceeded: compiler.max_steps={self.contracts.limits['max_steps']}")
                if node.kind == "text":
                    output.append(node.text)
                    continue
                try:
                    assignment = ASSIGNMENT.fullmatch(node.text)
                    if not strict and not self.contracts.interesting((node,)):
                        has_bindings = False
                        for item in walk((node,)):
                            text = item.text.split(" ", 1)[1] if item.text.startswith(("range ", "with ")) else item.text
                            binding = RANGE_ASSIGNMENT.fullmatch(text)
                            if binding and {binding[1], binding[2]} & self.needed:
                                has_bindings = True
                        has_jumps = any(item.text in {"break", "continue"} for item in walk((node,)))
                        if not has_bindings and not has_jumps and not context_effects((node,)):
                            continue
                    if node.kind == "if" or (node.kind == "opaque" and node.text.startswith("with ")):
                        output.append(self.control(node, source, variables, strict=strict))
                    elif node.kind == "opaque" and node.text.startswith("range "):
                        output.append(self.iteration(node, source, variables, strict=strict))
                    elif node.kind == "opaque" and node.text.startswith("block "):
                        output.append(self.named_template(node.text, source, node.line, variables))
                    elif node.kind == "emit":
                        if context_effects((node,)):
                            raise Unknown("template statement can mutate or dynamically evaluate its context")
                        if assignment:
                            try:
                                self.pipeline(node.text, source, node.line, variables)
                            except Unknown as exc:
                                variables.bind(assignment[1], exc, assign=assignment[2] == "=")
                                raise
                        elif node.text in {"break", "continue"}:
                            if not self.loops:
                                raise Unknown("loop control outside a range")
                            raise LoopControl(node.text)
                        elif node.text.startswith("template "):
                            output.append(self.named_template(node.text, source, node.line, variables))
                        else:
                            value = native(self.evaluate(expression(node.text), source, node.line, variables))
                            if type(value) not in (str, int, bool):
                                raise Unknown("unsupported output type")
                            output.append(str(value).lower() if type(value) is bool else str(value))
                    else:
                        raise Unknown("unsupported control flow")
                except Unknown as exc:
                    if exc.source is None:
                        exc.source, exc.line = source, node.line
                    if strict or context_effects((node,)) or self.contracts.interesting((node,), dynamic=False):
                        raise
                    self.incomplete = self.contextual = True
                    self.contracts.fallback(exc, source, self.inputs)
        except LoopControl as jump:
            jump.output = "".join(output) + jump.output
            raise
        except Unknown as exc:
            if exc.source is None:
                exc.source, exc.line = source, node.line
            raise
        return "".join(output)
