"""
Format and lint executable Bash and POSIX shell blocks inside maintained CI YAML.
"""

import argparse
import difflib
import json
import re
import shutil
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

from attrs import frozen
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from ruamel.yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode

from hypothesis_helm.schemas.contracts import mapping


@frozen
class ShellBlock:
    """
    Retain a script's source span without rewriting the surrounding YAML document.

    Attributes:
        node (ScalarNode): Original YAML scalar and its source coordinates.
        indent (int): YAML indentation for a newly written literal block.
        shell (str): Bash or POSIX shell dialect.
        group (str): Step identity, or GitLab job whose scripts share shell state.
    """

    node: ScalarNode
    indent: int
    shell: str
    group: str

    @property
    def code(self) -> str:
        """
        Return the decoded shell program with a terminal newline.

        Returns:
            str: Shell source without YAML indentation or scalar quoting.
        """
        return str(self.node.value).rstrip("\n") + "\n"

    @property
    def line(self) -> int:
        """
        Locate the first shell line in the YAML file.

        Returns:
            int: One-based source line for lint diagnostics.
        """
        return int(self.node.start_mark.line) + (2 if self.node.style in ("|", ">") else 1)


def blocks(node: Node, location: tuple[str, ...] = (), shell: str = "bash") -> Iterator[ShellBlock]:
    """
    Extract executable steps and GitLab scripts, respecting explicit shell selection.

    Args:
        node (Node): Parsed YAML node.
        location (tuple[str, ...]): Structural path within the CI document.
        shell (str): Inherited workflow or job shell.

    Yields:
        ShellBlock: Shell programs only; environment strings and non-shell steps are excluded.
    """
    if isinstance(node, SequenceNode):
        for index, child in enumerate(node.value):
            yield from blocks(child, (*location, str(index)), shell)
    elif isinstance(node, MappingNode):
        entries = {str(key.value): value for key, value in node.value}
        defaults = entries.get("defaults")
        if isinstance(defaults, MappingNode):
            for key, value in defaults.value:
                if key.value == "run" and isinstance(value, MappingNode):
                    shell = next((str(v.value) for k, v in value.value if k.value == "shell"), shell)
        if isinstance(entries.get("shell"), ScalarNode):
            shell = str(entries["shell"].value)
        dialect = Path(shell.split()[0]).name
        step = len(location) >= 2 and location[-2] == "steps"
        for key, value in node.value:
            name = str(key.value)
            selected = value
            if step and name == "run" and isinstance(value, MappingNode):
                options = {str(k.value): v for k, v in value.value}
                selected = options.get("command")
                dialect = Path(str(options["shell"].value).split()[0]).name if "shell" in options else dialect
            if step and name == "run" and isinstance(selected, ScalarNode) and dialect in ("bash", "sh"):
                yield ShellBlock(
                    selected, int(key.start_mark.column) + (4 if isinstance(value, MappingNode) else 2), dialect, "/".join(location)
                )
            elif len(location) <= 1 and name in ("before_script", "script", "after_script"):
                scripts = value.value if isinstance(value, SequenceNode) else [value]
                for script in scripts:
                    if not isinstance(script, ScalarNode) or script.tag != "tag:yaml.org,2002:str":
                        raise ValueError(f"{name} must contain resolved shell strings")
                    indent = int(script.start_mark.column) if isinstance(value, SequenceNode) else int(key.start_mark.column) + 2
                    # GitLab before_script and script run in the same shell;
                    # after_script starts a separate shell.
                    group = "/".join(location) + ("/after_script" if name == "after_script" else "/script")
                    yield ShellBlock(script, indent, "bash", group)
            else:
                yield from blocks(value, (*location, name), shell)


def replacement(source: str, block: ShellBlock, code: str) -> str:
    """
    Replace a scalar with formatted literal shell while preserving YAML comments.

    Args:
        source (str): Complete original YAML text.
        block (ShellBlock): Scalar to replace.
        code (str): Shell source produced by shfmt.

    Returns:
        str: YAML scalar text containing the formatted program.
    """
    original = source[block.node.start_mark.index : block.node.end_mark.index]
    if block.node.style not in ("|", ">") and code.count("\n") == 1:
        return json.dumps(code.rstrip("\n"), ensure_ascii=False)
    header = original.split("\n", 1)[0] if block.node.style == "|" else "|-"
    indent = block.indent
    if block.node.style in ("|", ">"):
        body = original.splitlines()[1:]
        indent = min((len(line) - len(line.lstrip(" ")) for line in body if line.strip()), default=indent)
    text = header + "\n" + "\n".join(" " * indent + line if line else "" for line in code.rstrip("\n").split("\n"))
    if original.endswith("\n"):
        text += "\n" * (len(original) - len(original.rstrip("\n")))
    return text


def check(path: Path, *, write: bool = False) -> int:
    """
    Format YAML shell scalars and report ShellCheck findings against their source lines.

    Args:
        path (Path): Workflow, composite action or shared CI example.
        write (bool): Apply formatting changes without rewriting YAML metadata.

    Returns:
        int: Zero on success, one for formatting or lint failures.
    """
    source = path.read_text()
    document = YAML(typ="safe").compose(source)
    if document is None:
        return 0
    edits: list[tuple[int, int, str]] = []
    groups: dict[tuple[str, str], list[ShellBlock]] = {}
    status = 0
    for block in blocks(document):
        if re.search(r"\$\{\{|<<\s*(?:parameters|pipeline)\.", block.code):
            print(f"{path}:{block.line}: pass CI expressions through environment variables, not executable shell", file=sys.stderr)
            status = 1
            continue
        formatted = subprocess.run(
            ["shfmt", "-ln", "posix" if block.shell == "sh" else "bash", "-i", "4", "-ci"],
            input=block.code,
            text=True,
            capture_output=True,
            check=False,
        )
        if formatted.returncode:
            print(f"{path}:{block.line}: {formatted.stderr.strip()}", file=sys.stderr)
            status = 1
            continue
        if formatted.stdout != block.code:
            edits.append((int(block.node.start_mark.index), int(block.node.end_mark.index), replacement(source, block, formatted.stdout)))
        groups.setdefault((block.group, block.shell), []).append(block)
    for (_, shell), scripts in groups.items():
        code = "".join(block.code for block in scripts)
        lines = [block.line + offset for block in scripts for offset, _ in enumerate(block.code.splitlines())]
        result = subprocess.run(
            ["shellcheck", "--shell", shell, "--format=json", "-"], input=code, text=True, capture_output=True, check=False
        )
        if result.returncode:
            status = 1
            for raw in json.loads(result.stdout or "[]"):
                finding = mapping(raw)
                line = lines[min(int(str(finding["line"])) - 1, len(lines) - 1)]
                print(f"{path}:{line}: SC{finding['code']}: {finding['message']}", file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
    updated = source
    for start, end, text in sorted(edits, reverse=True):
        updated = updated[:start] + text + updated[end:]
    if write and edits:
        # Parse before writing so formatter changes cannot corrupt the YAML container.
        YAML(typ="safe").compose(updated)
        path.write_text(updated)
        print(f"Formatted embedded shell: {path}")
    elif edits:
        status = 1
        print(
            "".join(difflib.unified_diff(source.splitlines(True), updated.splitlines(True), fromfile=str(path), tofile=str(path))), end=""
        )
    return status


def main(argv: list[str] | None = None) -> int:
    """
    Check embedded scripts in CI examples and GitHub workflows using installed tools.

    Args:
        argv (list[str] | None): Explicit arguments, or the process command line.

    Returns:
        int: Zero on success, one for lint failures, or two for invalid setup.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path, help="CI YAML files; defaults to action.yml, .github/, .circleci/ and ci/")
    parser.add_argument("--write", action="store_true", help="Apply shfmt formatting to embedded shell blocks")
    args = parser.parse_args(argv)
    try:
        for tool in ("shfmt", "shellcheck"):
            if shutil.which(tool) is None:
                raise ValueError(f"{tool} is required; run bash scripts/setup-dev.sh")
        paths = args.files or [
            Path("action.yml"),
            *(p for root in (Path(".github"), Path(".circleci"), Path("ci")) for p in root.rglob("*") if p.suffix in (".yml", ".yaml")),
        ]
        status = 0
        for path in sorted(set(paths)):
            status |= check(path, write=args.write)
        return status
    except (OSError, ValueError, YAMLError) as exc:
        parser.exit(2, f"CI shell check failed: {exc}\n")
