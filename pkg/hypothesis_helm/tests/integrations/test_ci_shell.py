"""
Check embedded shell without changing YAML metadata, script contents or heredocs.
"""

import shutil
import subprocess
from pathlib import Path
from textwrap import dedent

import pytest
from ruamel.yaml import YAML

from hypothesis_helm.integrations.ci_shell import blocks, check, main

pytestmark = pytest.mark.skipif(not shutil.which("shfmt") or not shutil.which("shellcheck"), reason="shfmt and ShellCheck are required")


def test_format_preserves_yaml_and_heredocs(tmp_path: Path) -> None:
    """
    Reindent shell control flow while retaining comments, CI expressions and heredoc data.

    Args:
        tmp_path (Path): Isolated workflow and executable output.

    Returns:
        None: Formatting is idempotent and preserves the script's actual output.
    """
    path = tmp_path / "workflow.yml"
    path.write_text(
        dedent(
            """
            # Keep this workflow comment.
            on: [push, pull_request]
            env:
              run: 'this is data, not shell'
              TEST_VALUE: ${{ inputs.value }}
            jobs:
              test:
                runs-on: ubuntu-latest
                steps:
                  - run: | # Keep this script comment.
                      if true; then
                        cat <<'PAYLOAD'
                      alpha
                        two spaces
                      PAYLOAD
                      fi
                  - shell: python
                    run: print('not shell')
            """
        ).lstrip()
    )
    before = YAML(typ="safe").load(path.read_text())
    assert check(path) == 1
    assert check(path, write=True) == 0
    result = path.read_text()
    assert "# Keep this workflow comment." in result
    assert "| # Keep this script comment." in result
    assert "if true; then\n              cat" in result
    after = YAML(typ="safe").load(result)
    assert after["on"] == before["on"]
    assert after["env"] == before["env"]
    before_script = before["jobs"]["test"]["steps"][0]["run"]
    after_script = after["jobs"]["test"]["steps"][0]["run"]
    for code in (before_script, after_script):
        observed = subprocess.run(["bash"], input=code, text=True, capture_output=True, check=True)
        assert observed.stdout == "alpha\n  two spaces\n"
    assert check(path) == 0
    assert check(path, write=True) == 0
    assert path.read_text() == result


@pytest.mark.parametrize("style", ["plain", "quoted", "folded"])
def test_scalar_forms(tmp_path: Path, style: str) -> None:
    """
    Preserve decoded commands when formatting inline and folded YAML scalars.

    Args:
        tmp_path (Path): Isolated composite action.
        style (str): YAML spelling for the command.

    Returns:
        None: Formatting never turns YAML escapes or folding into different shell commands.
    """
    command = {"plain": 'echo "ok" >/dev/null', "quoted": "'echo \"ok\" >/dev/null'", "folded": '>\n        echo "ok"\n        >/dev/null'}[
        style
    ]
    path = tmp_path / "action.yml"
    path.write_text(f"runs:\n  using: composite\n  steps:\n    - shell: bash\n      run: {command}\n")
    assert check(path, write=True) == 0
    assert check(path) == 0
    document = YAML(typ="safe").compose(path.read_text())
    assert document is not None
    code = next(blocks(document)).code
    assert subprocess.run(["bash"], input=code, text=True, capture_output=True, check=True).stdout == ""


def test_shellcheck_reports_yaml_line(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Map ShellCheck findings back to the workflow's original source line.

    Args:
        tmp_path (Path): Workflow containing an unsafe expansion.
        capsys (pytest.CaptureFixture[str]): Captured diagnostic output.

    Returns:
        None: The unquoted expansion is reported at its YAML location.
    """
    path = tmp_path / "workflow.yml"
    path.write_text('jobs:\n  test:\n    steps:\n      - run: |\n          printf "%s" $INPUT\n')
    assert check(path) == 1
    assert f"{path}:5: SC2086" in capsys.readouterr().err


def test_gitlab_shared_shell_state(tmp_path: Path) -> None:
    """
    Analyze setup and script entries together so local variables retain their scope.

    Args:
        tmp_path (Path): Shared GitLab job definition.

    Returns:
        None: Variables used in a later script entry are not falsely reported as unused.
    """
    path = tmp_path / "gitlab.yml"
    path.write_text('test:\n  before_script:\n    - greeting=hello\n  script:\n    - printf "%s" "$greeting"\n')
    assert check(path) == 0


def test_circleci_command_and_shell_override(tmp_path: Path) -> None:
    """
    Lint CircleCI run mappings and honor a non-shell workflow default.

    Args:
        tmp_path (Path): Workflow containing Python and a Bash override.

    Returns:
        None: Explicit Bash commands are extracted while Python programs are left alone.
    """
    path = tmp_path / "circleci.yml"
    path.write_text(
        dedent(
            """
            defaults:
              run:
                shell: python
            jobs:
              test:
                steps:
                  - run: print('python')
                  - run:
                      name: Bash check
                      shell: /bin/bash -eo pipefail
                      command: |
                        if true; then
                          echo okay
                        fi
            """
        ).lstrip()
    )
    assert check(path, write=True) == 0
    assert check(path) == 0
    assert "print('python')" in path.read_text()


def test_ci_expressions_stay_out_of_executable_shell(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Require provider expressions to enter through environment variables.

    Args:
        tmp_path (Path): Workflow interpolating untrusted text into code.
        capsys (pytest.CaptureFixture[str]): Captured lint diagnostic.

    Returns:
        None: The checker cannot hide shell injection by substituting harmless placeholders.
    """
    path = tmp_path / "workflow.yml"
    path.write_text('jobs:\n  test:\n    steps:\n      - run: echo "${{ github.event.pull_request.title }}"\n')
    assert main([str(path)]) == 1
    assert "environment variables" in capsys.readouterr().err
