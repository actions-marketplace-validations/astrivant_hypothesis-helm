"""
Resolve published report links and render linked prose in PDF paragraphs.
"""

import re
from collections.abc import Iterator
from html import escape
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit

from attrs import frozen

LINK = re.compile(r"\[([^\]]+)\]\((?:<([^>]+)>|([^\s)]+))\)")
CODE = re.compile(r"(`+)(.*?)\1(?!`)")


def web_url(value: object) -> str | None:
    """
    Accept shareable HTTPS destinations without exposing embedded credentials.

    Args:
        value (object): Optional recorded source or artifact URL.

    Returns:
        str | None: HTTPS URL, or None for local paths and unusable destinations.
    """
    if not isinstance(value, str) or any(ord(char) < 32 for char in value):
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password:
            return quote(value, safe="/:?#[]@!$&'()*+,;=%-._~")
    except ValueError:
        pass
    return None


def repository_url(value: object) -> str | None:
    """
    Convert supported Git clone URLs to credential-free repository browser URLs.

    Args:
        value (object): HTTPS, SSH, or SCP-style Git remote.

    Returns:
        str | None: GitHub, GitLab, or Bitbucket browser root, when recognized.
    """
    if not isinstance(value, str):
        return None
    scp = re.fullmatch(r"[\w.-]+@([\w.-]+):(.+)", value)
    if scp:
        value = f"https://{scp[1]}/{scp[2]}"
    if value.startswith("ssh://"):
        try:
            parsed = urlsplit(value)
            if parsed.password or parsed.port not in (None, 22) or parsed.query or parsed.fragment:
                return None
            value = f"https://{parsed.hostname}{parsed.path}"
        except ValueError:
            return None
    url = web_url(value)
    if url is None:
        return None
    parsed = urlsplit(url)
    if parsed.hostname not in {"github.com", "gitlab.com", "bitbucket.org"} or parsed.query or parsed.fragment:
        return None
    return url.rstrip("/").removesuffix(".git")


def chart_source_url(chart: dict[str, object], source: dict[str, object]) -> str | None:
    """
    Link a chart to its recorded Git revision or its declared source URL.

    Args:
        chart (dict[str, object]): Chart-relative path and optional declared source.
        source (dict[str, object]): Recorded repository URL, revision, and optional scan-root subdirectory.

    Returns:
        str | None: Chart source URL without guessing a repository branch or Helm registry layout.
    """
    repository = repository_url(source.get("url")) if source.get("kind") != "helm" else None
    revision = source.get("revision")
    path = PurePosixPath(str(source.get("path", "."))) / str(chart["chart"])
    tracked = source.get("chart_paths")
    present = tracked is None or isinstance(tracked, list) and chart["chart"] in tracked
    if repository and revision and present and not path.is_absolute() and ".." not in path.parts:
        host = urlsplit(repository).hostname
        route = "-/tree" if host == "gitlab.com" else "src" if host == "bitbucket.org" else "tree"
        suffix = "" if path == PurePosixPath(".") else "/" + quote(path.as_posix(), safe="/")
        return f"{repository}/{route}/{quote(str(revision), safe='')}{suffix}"
    return web_url(chart.get("source_url"))


def link_matches(line: str) -> Iterator[re.Match[str]]:
    """
    Find links outside inline code, preserving literal failing input values.

    Args:
        line (str): Markdown prose containing optional inline code.

    Yields:
        re.Match[str]: Link syntax occurring outside code spans.
    """
    spans = [match.span() for match in CODE.finditer(line)]
    for match in LINK.finditer(line):
        if not any(start <= match.start() < end for start, end in spans):
            yield match


@frozen
class Publication:
    """
    Locate report artifacts in a publicly browsable GitHub repository.

    Attributes:
        root (Path): Local checkout containing every published artifact.
        repository (str): HTTPS GitHub repository URL.
        revision (str): Branch, tag, or commit that will contain the published files.
    """

    root: Path
    repository: str
    revision: str

    def url(self, target: str, report: Path, *, image: bool = False) -> str:
        """
        Convert a report-relative artifact target into an absolute public URL.

        Args:
            target (str): Markdown link destination.
            report (Path): Markdown file from which relative links are resolved.
            image (bool): Serve an embedded image directly instead of its GitHub file viewer.

        Returns:
            str: Preserved internal or HTTPS destination, or a public GitHub artifact URL.

        Raises:
            ValueError: An artifact escapes the checkout or uses a nonpublic URL scheme.
        """
        parsed = urlsplit(target)
        if parsed.scheme == "https" or target.startswith("#"):
            return target
        if parsed.scheme or parsed.netloc:
            raise ValueError(f"Published reports require HTTPS links: {target}")
        path = (report.parent / unquote(parsed.path)).resolve() if parsed.path else report.resolve()
        relative = path.relative_to(self.root.resolve())
        kind = "raw" if image else "tree" if path.is_dir() else "blob"
        url = f"{self.repository.rstrip('/')}/{kind}/{quote(self.revision, safe='')}/{quote(relative.as_posix(), safe='/')}"
        return url + (f"#{parsed.fragment}" if parsed.fragment else "")


def publish_links(line: str, report: Path, publication: Publication) -> str:
    """
    Rewrite every Markdown link in a prose line for public consumption.

    Args:
        line (str): Report prose outside code fences.
        report (Path): Markdown output location.
        publication (Publication): Public repository destination.

    Returns:
        str: Prose retaining internal destinations while publishing artifact targets as HTTPS URLs.
    """
    for match in reversed(list(link_matches(line))):
        image = match.start() > 0 and line[match.start() - 1] == "!"
        replacement = f"[{match[1]}](<{publication.url(match[2] or match[3], report, image=image)}>)"
        line = line[: match.start()] + replacement + line[match.end() :]
    return line


def linked_prose(line: str) -> str:
    """
    Convert Markdown links to visibly underlined, clickable ReportLab paragraph markup.

    Args:
        line (str): Prose that may contain multiple inline links.

    Returns:
        str: XML-escaped paragraph content with blue underlined links.
    """
    parts = []
    offset = 0
    for match in link_matches(line):
        parts.append(escape(line[offset : match.start()]))
        target = escape(match[2] or match[3], quote=True)
        parts.append(f'<link href="{target}" color="#1459a6"><u>{escape(match[1])}</u></link>')
        offset = match.end()
    parts.append(escape(line[offset:]))
    return "".join(parts)
