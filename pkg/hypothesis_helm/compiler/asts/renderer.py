"""
Read fixed renderer context using Helm's own capabilities and chart loader.
"""

from __future__ import annotations

import io
import json
import shutil
import tarfile
import tempfile
from functools import lru_cache
from pathlib import Path, PurePosixPath
from textwrap import dedent

from attrs import define, field, frozen

from hypothesis_helm.charts import yamlio
from hypothesis_helm.execution.processes import Processes
from hypothesis_helm.schemas.contracts import mapping, sequence

MAX_CONTEXT_BYTES = 64 * 1024 * 1024


class Unavailable(ValueError):
    """Keep unavailable native context outside the compiler's supported domain."""


def archive_files(stream: io.BytesIO) -> dict[str, bytes]:
    """
    Read bounded regular chart members without extracting paths onto the filesystem.

    Args:
        stream (io.BytesIO): Helm chart archive, including its enclosing chart directory.

    Returns:
        dict[str, bytes]: Chart-relative member names and their exact bytes.
    """
    result: dict[str, bytes] = {}
    total = 0
    with tarfile.open(fileobj=stream) as bundle:
        for index, member in enumerate(bundle):
            name = PurePosixPath(member.name)
            total += member.size
            if index >= 10000 or total > MAX_CONTEXT_BYTES:
                raise Unavailable("chart files exceed the compiler inspection budget")
            if name.is_absolute() or ".." in name.parts or member.issym() or member.islnk():
                raise Unavailable("chart archive contains unsupported paths or links")
            if not member.isfile():
                continue
            content = bundle.extractfile(member)
            if content is None or len(name.parts) < 2:
                raise Unavailable("chart archive has an unsupported member")
            relative = "/".join(name.parts[1:])
            if relative in result:
                raise Unavailable("chart archive contains duplicate paths")
            result[relative] = content.read()
    return result


@frozen
class FileSet:
    """
    Retain chart-local files separately from metadata, templates and child charts.

    Attributes:
        contents (dict[str, bytes]): Exact names admitted by Helm's chart loader.
    """

    contents: dict[str, bytes]

    def __bool__(self) -> bool:
        """
        Preserve the truthiness of Helm's map of accessible files.

        Returns:
            bool: Whether at least one file is accessible.
        """
        return bool(self.contents)

    def get(self, name: str) -> str:
        """
        Read a UTF-8 chart file; absent names follow Helm's empty-string behavior.

        Args:
            name (str): Exact template lookup key, without filesystem normalization.

        Returns:
            str: Contents, or an empty string for a missing or inaccessible name.
        """
        try:
            return self.contents.get(name, b"").decode("utf-8")
        except UnicodeError as exc:
            raise Unavailable("binary chart file requires native Helm evaluation") from exc


def chart_files(files: dict[str, bytes], scope: tuple[str, ...], names: dict[tuple[str, ...], str]) -> FileSet:
    """
    Follow declared dependency aliases without exposing parent files to child contexts.

    Args:
        files (dict[str, bytes]): Loaded parent archive members.
        scope (tuple[str, ...]): Values namespace identifying the requested chart instance.
        names (dict[tuple[str, ...], str]): Discovered instance paths and original chart names.

    Returns:
        FileSet: Files visible to this chart's dot context.
    """
    prefix: tuple[str, ...] = ()
    for alias in scope:
        prefix = (*prefix, alias)
        candidates: dict[str, dict[str, bytes]] = {}
        for path, data in files.items():
            parts = path.split("/")
            if len(parts) < 2 or parts[0] != "charts" or parts[1].startswith(("_", ".")):
                continue
            if len(parts) == 2 and path.endswith(".tgz"):
                candidates[parts[1]] = archive_files(io.BytesIO(data))
            elif len(parts) > 2:
                candidates.setdefault(parts[1], {})["/".join(parts[2:])] = data
        matching = [
            child
            for child in candidates.values()
            if "Chart.yaml" in child and mapping(yamlio.load(child["Chart.yaml"].decode())).get("name") == names.get(prefix)
        ]
        if len(matching) != 1:
            raise Unavailable("dependency file context is missing or ambiguous")
        files = matching[0]
    metadata = mapping(yamlio.load(files["Chart.yaml"].decode()))
    reserved = {"Chart.yaml", "Chart.lock", "values.yaml", "values.schema.json"}
    if metadata.get("apiVersion") != "v1":
        reserved.update({"requirements.yaml", "requirements.lock"})
    return FileSet(
        {
            name: content
            for name, content in files.items()
            if name not in reserved and not name.startswith("templates/") and (not name.startswith("charts/") or name.endswith(".prov"))
        }
    )


@lru_cache(maxsize=128)
def probe(binary: str, stamp: int, kube_version: str | None, timeout: float, operation: str, arguments: tuple[str, ...] = ()) -> object:
    """
    Obtain bounded deterministic context operations from Helm rather than approximating them.

    Args:
        binary (str): Resolved Helm executable path.
        stamp (int): Executable modification time, invalidating stale cached probes.
        kube_version (str | None): The same override supplied to the real render.
        timeout (float): Probe subprocess deadline.
        operation (str): Capabilities or semverCompare; no arbitrary template source is accepted.
        arguments (tuple[str, ...]): Data-only arguments supplied through a values file.

    Returns:
        object: Native capability fields or a semantic-version comparison result.
    """
    expressions = {"capabilities": ".Capabilities", "semverCompare": "semverCompare .Values.first .Values.second"}
    expression = expressions[operation]
    with tempfile.TemporaryDirectory(prefix="helm-capabilities-") as temporary:
        root = Path(temporary)
        (root / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "context-probe", "version": "0.1.0"}))
        (root / "templates").mkdir()
        values = root / "probe-values.json"
        values.write_text(json.dumps(dict(zip(("first", "second"), arguments, strict=False))))
        (root / "templates/context.yaml").write_text(
            dedent(
                f"""
                apiVersion: v1
                kind: ConfigMap
                metadata:
                  name: context-probe
                data:
                  result: {{{{ {expression} | toJson | quote }}}}
                """
            )
        )
        command = [binary, "template", "context-probe", str(root), "--values", str(values)]
        if kube_version:
            command.extend(["--kube-version", kube_version])
        result = Processes().run(command, capture_output=True, text=True, timeout=timeout)
        if result.returncode:
            raise Unavailable(f"Helm {operation} probe failed")
        documents = [mapping(item) for item in yamlio.load_all(result.stdout) if item is not None]
        if len(documents) != 1:
            raise Unavailable("Helm context probe returned an unexpected document")
        return json.loads(str(mapping(documents[0]["data"])["result"]))


@define
class RendererContext:
    """
    Lazily obtain native fixed context, keeping real chart templates out of context probes.

    Attributes:
        chart (Path): Original prepared chart.
        names (dict[tuple[str, ...], str]): Dependency aliases and original names.
        helm (str): Renderer binary.
        kube_version (str | None): Native capability override, unchanged from rendering.
        timeout (float): Deadline for each native context probe.
        release (str): Fixed Helm release name.
        namespace (str): Fixed release namespace.
        packed (dict[str, bytes] | None): Lazily loaded chart archive; none until file access is needed.
        files (dict[tuple[str, ...], FileSet]): Chart-local file views, reused across candidates.
    """

    chart: Path
    names: dict[tuple[str, ...], str] = field(factory=dict)
    helm: str = "helm"
    kube_version: str | None = None
    timeout: float = 30.0
    release: str = "hypothesis"
    namespace: str = "default"
    packed: dict[str, bytes] | None = None
    files: dict[tuple[str, ...], FileSet] = field(factory=dict)

    def capability_fields(self) -> dict[str, object]:
        """
        Resolve and fingerprint the same executable used for chart rendering.

        Returns:
            dict[str, object]: Known Helm capabilities or an explicit unavailable-context error.
        """
        binary = shutil.which(self.helm)
        if binary is None:
            raise Unavailable("Helm is unavailable for the capability probe")
        return mapping(probe(binary, Path(binary).stat().st_mtime_ns, self.kube_version, self.timeout, "capabilities"))

    def semver_compare(self, constraint: str, version: str) -> bool:
        """
        Delegate Helm's semantic-version constraint language to the selected renderer.

        Args:
            constraint (str): Concrete version constraint from the chart.
            version (str): Concrete version being compared.

        Returns:
            bool: Native comparison result, or explicit uncertainty if probing fails.
        """
        binary = shutil.which(self.helm)
        if binary is None:
            raise Unavailable("Helm is unavailable for version comparison")
        if len(constraint) + len(version) > 4096:
            raise Unavailable("version comparison exceeds the compiler inspection budget")
        result = probe(binary, Path(binary).stat().st_mtime_ns, self.kube_version, self.timeout, "semverCompare", (constraint, version))
        if type(result) is not bool:
            raise Unavailable("Helm version comparison returned a non-Boolean result")
        return result

    def chart_files(self, scope: tuple[str, ...]) -> FileSet:
        """
        Let Helm apply its loader and ignore rules before reading chart-local files.

        Args:
            scope (tuple[str, ...]): Calling chart's namespace, preserved through helper contexts.

        Returns:
            FileSet: Read-only loaded file contents, without templates or metadata.
        """
        if scope not in self.files:
            if self.packed is None:
                with tempfile.TemporaryDirectory(prefix="helm-context-files-") as temporary:
                    result = Processes().run(
                        [self.helm, "package", str(self.chart), "--destination", temporary],
                        capture_output=True,
                        text=True,
                        timeout=self.timeout,
                    )
                    archives = list(Path(temporary).glob("*.tgz"))
                    if result.returncode or len(archives) != 1:
                        raise Unavailable("Helm could not load the chart's file context")
                    if archives[0].stat().st_size > MAX_CONTEXT_BYTES:
                        raise Unavailable("chart files exceed the compiler inspection budget")
                    self.packed = archive_files(io.BytesIO(archives[0].read_bytes()))
            self.files[scope] = chart_files(self.packed, scope, self.names)
        return self.files[scope]


@frozen
class ContextReference:
    """
    Keep native capability and file lookups lazy across dot changes and helper arguments.

    Attributes:
        renderer (RendererContext | None): Fixed execution settings, absent in purely static analysis.
        kind (str): Files or Capabilities.
        scope (tuple[str, ...]): Source chart namespace for file access.
    """

    renderer: RendererContext | None
    kind: str
    scope: tuple[str, ...] = ()

    def value(self) -> object:
        """
        Obtain the native context only when an evaluated expression actually needs it.

        Returns:
            object: File view or capability mapping.
        """
        if self.renderer is None:
            raise Unavailable(f"{self.kind} requires the fixed Helm renderer context")
        if self.kind == "Files":
            return self.renderer.chart_files(self.scope)
        result = dict(self.renderer.capability_fields())
        result["APIVersions"] = APIVersions(tuple(str(item) for item in sequence(result["APIVersions"])))
        return result


@frozen
class APIVersions:
    """
    Distinguish Helm's version set and Has method from arbitrary candidate dictionaries.

    Attributes:
        versions (tuple[str, ...]): Exact API identifiers exposed by the chosen Helm invocation.
    """

    versions: tuple[str, ...]

    def __bool__(self) -> bool:
        """
        Preserve empty-version-set truthiness in supported guards.

        Returns:
            bool: Whether the renderer advertises any API versions.
        """
        return bool(self.versions)
