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

from attrs import Factory, define, field, frozen

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.limits import active_limits
from hypothesis_helm.exceptions.compiler import Unavailable
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = (
    "APIVersions",
    "ContextReference",
    "FileSet",
    "FixedFields",
    "RendererContext",
    "archive_files",
    "chart_files",
    "chart_members",
    "probe",
)


def archive_files(stream: io.BytesIO, *, limits: dict[str, int] | None = None) -> dict[str, bytes]:
    """
    Read bounded regular chart members without extracting paths onto the filesystem.

    Args:
        stream (io.BytesIO): Helm chart archive, including its enclosing chart directory.
        limits (dict[str, int] | None): Captured compiler budgets, or the inherited configuration.

    Returns:
        dict[str, bytes]: Chart-relative member names and their exact bytes.
    """
    limits = active_limits() if limits is None else limits
    if stream.getbuffer().nbytes > limits["max_context_bytes"]:
        raise Unavailable(f"chart archive exceeds compiler.max_context_bytes={limits['max_context_bytes']}")
    result: dict[str, bytes] = {}
    total = 0
    with tarfile.open(fileobj=stream) as bundle:
        for index, member in enumerate(bundle):
            name = PurePosixPath(member.name)
            total += member.size
            if index >= limits["max_files"]:
                raise Unavailable(f"chart files exceed compiler.max_files={limits['max_files']}")
            if total > limits["max_context_bytes"]:
                raise Unavailable(f"chart files exceed compiler.max_context_bytes={limits['max_context_bytes']}")
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


def chart_members(
    files: dict[str, bytes], scope: tuple[str, ...], names: dict[tuple[str, ...], str], *, limits: dict[str, int] | None = None
) -> dict[str, bytes]:
    """
    Follow declared dependency aliases without exposing parent files to child contexts.

    Args:
        files (dict[str, bytes]): Loaded parent archive members.
        scope (tuple[str, ...]): Values namespace identifying the requested chart instance.
        names (dict[tuple[str, ...], str]): Discovered instance paths and original chart names.
        limits (dict[str, int] | None): Captured compiler budgets for nested archives.

    Returns:
        dict[str, bytes]: Members of the selected chart, including its metadata and templates.
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
                candidates[parts[1]] = archive_files(io.BytesIO(data), limits=limits)
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
    return files


def chart_files(
    files: dict[str, bytes], scope: tuple[str, ...], names: dict[tuple[str, ...], str], *, limits: dict[str, int] | None = None
) -> FileSet:
    """
    Remove metadata, templates and dependencies from a chart's accessible files.

    Args:
        files (dict[str, bytes]): Loaded root chart archive.
        scope (tuple[str, ...]): Calling chart's values namespace.
        names (dict[tuple[str, ...], str]): Original dependency names indexed by their aliases.
        limits (dict[str, int] | None): Captured compiler budgets.

    Returns:
        FileSet: Files exposed through Helm's Files object.
    """
    files = chart_members(files, scope, names, limits=limits)
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
        operation (str): Capabilities, semverCompare or urlParse; arbitrary template source is never accepted.
        arguments (tuple[str, ...]): Data-only arguments supplied through a values file.

    Returns:
        object: Native capability fields, parsed URL fields or a semantic-version comparison result.
    """
    expressions = {
        "capabilities": ".Capabilities",
        "semverCompare": "semverCompare .Values.first .Values.second",
        "urlParse": "urlParse .Values.first",
    }
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
        offline (bool): Plain helm template has no cluster connection and lookup returns an empty map.
        enable_dns (bool): Whether the renderer was explicitly allowed to perform DNS queries.
        limits (dict[str, int]): Compiler budgets captured before loading and caching context.
        metadata (dict[tuple[str, ...], FixedFields]): Supported immutable metadata for each chart instance.
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
    offline: bool = True
    enable_dns: bool = False
    limits: dict[str, int] = field(default=Factory(lambda self: active_limits(self.chart), takes_self=True), kw_only=True)
    metadata: dict[tuple[str, ...], FixedFields] = field(factory=dict, kw_only=True)

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
        if len(constraint) + len(version) > self.limits["max_version_chars"]:
            raise Unavailable(f"version comparison exceeds compiler.max_version_chars={self.limits['max_version_chars']}")
        result = probe(binary, Path(binary).stat().st_mtime_ns, self.kube_version, self.timeout, "semverCompare", (constraint, version))
        if type(result) is not bool:
            raise Unavailable("Helm version comparison returned a non-Boolean result")
        return result

    def url_parse(self, value: str) -> dict[str, object]:
        """
        Parse a concrete URL using Sprig in the selected Helm binary, without network access.

        Args:
            value (str): Candidate URL supplied as data, never interpreted as template code.

        Returns:
            dict[str, object]: Native URL fields within the compiler's existing string budget.

        Raises:
            Unavailable: Helm cannot parse the value or the configured budget is exceeded.
        """
        if len(value) > self.limits["max_string_chars"]:
            raise Unavailable(f"URL exceeds compiler.max_string_chars={self.limits['max_string_chars']}")
        binary = shutil.which(self.helm)
        if binary is None:
            raise Unavailable("Helm is unavailable for URL parsing")
        result = probe(binary, Path(binary).stat().st_mtime_ns, self.kube_version, self.timeout, "urlParse", (value,))
        if not isinstance(result, dict) or not all(isinstance(key, str) and isinstance(item, str) for key, item in result.items()):
            raise Unavailable("Helm URL parsing returned unexpected fields")
        return mapping(result)

    def chart_files(self, scope: tuple[str, ...]) -> FileSet:
        """
        Let Helm apply its loader and ignore rules before reading chart-local files.

        Args:
            scope (tuple[str, ...]): Calling chart's namespace, preserved through helper contexts.

        Returns:
            FileSet: Read-only loaded file contents, without templates or metadata.
        """
        if scope not in self.files:
            self.files[scope] = chart_files(self.load_chart(), scope, self.names, limits=self.limits)
        return self.files[scope]

    def load_chart(self) -> dict[str, bytes]:
        """
        Load one bounded chart snapshot through Helm, shared by files and metadata.

        Returns:
            dict[str, bytes]: Exact package members admitted by Helm's loader.
        """
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
                if archives[0].stat().st_size > self.limits["max_context_bytes"]:
                    raise Unavailable(f"chart archive exceeds compiler.max_context_bytes={self.limits['max_context_bytes']}")
                self.packed = archive_files(io.BytesIO(archives[0].read_bytes()), limits=self.limits)
        return self.packed

    def chart_metadata(self, scope: tuple[str, ...]) -> FixedFields:
        """
        Expose immutable Helm metadata while leaving dependency-processing fields unknown.

        Args:
            scope (tuple[str, ...]): Chart instance namespace, including dependency aliases.

        Returns:
            FixedFields: Supported metadata with Helm's field names and zero values.
        """
        if scope not in self.metadata:
            members = chart_members(self.load_chart(), scope, self.names, limits=self.limits)
            metadata = mapping(yamlio.load(members["Chart.yaml"].decode()))
            fields: dict[str, object] = {
                name: metadata.get(key, "")
                for name, key in (
                    ("Name", "name"),
                    ("Version", "version"),
                    ("AppVersion", "appVersion"),
                    ("APIVersion", "apiVersion"),
                    ("KubeVersion", "kubeVersion"),
                    ("Description", "description"),
                    ("Home", "home"),
                    ("Icon", "icon"),
                    ("Type", "type"),
                )
            }
            fields.update(
                Name=scope[-1] if scope else metadata["name"],
                IsRoot=not scope,
                Annotations=metadata.get("annotations", {}),
                Deprecated=metadata.get("deprecated", False),
                Keywords=metadata.get("keywords", []),
                Sources=metadata.get("sources", []),
            )
            self.metadata[scope] = FixedFields(fields)
        return self.metadata[scope]

    def template_context(self, scope: tuple[str, ...], source: str) -> dict[str, object]:
        """
        Resolve the executing template's Helm name using dependency aliases.

        Args:
            scope (tuple[str, ...]): Namespace of the chart owning the root template.
            source (str): Compiler source filename, including archived dependency prefixes.

        Returns:
            dict[str, object]: Native Template Name and BasePath.
        """
        root_name = str(self.chart_metadata(()).values["Name"])
        prefix = root_name + "".join(f"/charts/{part}" for part in scope) + "/templates"
        relative = ("/" + source).rsplit("/templates/", 1)
        if len(relative) != 2:
            raise Unavailable("template source has no resolved chart-relative filename")
        return {"Name": f"{prefix}/{relative[1]}", "BasePath": prefix}


@frozen
class FixedFields:
    """
    Distinguish a partially modeled Go structure from an open template dictionary.

    Attributes:
        values (dict[str, object]): Supported fields; absent fields remain unknown rather than nil.
    """

    values: dict[str, object]


@frozen
class ContextReference:
    """
    Keep native capability and file lookups lazy across dot changes and helper arguments.

    Attributes:
        renderer (RendererContext | None): Fixed execution settings, absent in purely static analysis.
        kind (str): Files, Capabilities, Chart or Template.
        scope (tuple[str, ...]): Source chart namespace for file access.
        source (str): Root template source used to resolve Template fields.
    """

    renderer: RendererContext | None
    kind: str
    scope: tuple[str, ...] = ()
    source: str = ""

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
        if self.kind == "Chart":
            return self.renderer.chart_metadata(self.scope)
        if self.kind == "Template":
            return self.renderer.template_context(self.scope, self.source)
        if self.kind != "Capabilities":
            raise Unavailable(f"unsupported fixed context: {self.kind}")
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
