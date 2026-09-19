"""
Check development bootstrapping without installing software or modifying the host.
"""

import hashlib
import os
import subprocess
from pathlib import Path
from textwrap import dedent

import pytest

SCRIPT = Path(__file__).resolve().parents[3] / "scripts/setup-dev.sh"


@pytest.mark.parametrize("platform", ["darwin", "linux"])
def test_setup_selects_platform_packages(tmp_path: Path, platform: str) -> None:
    """
    Select Homebrew or apt explicitly while retaining the shared system dependencies.

    Args:
        tmp_path (Path): Mock package manager directory.
        platform (str): Platform being configured.

    Returns:
        None: No real package manager runs, and both environments include Git LFS and GNU Parallel.
    """
    log = tmp_path / "commands"
    for name in ("brew", "apt-get", "sudo"):
        executable = tmp_path / name
        executable.write_text(
            dedent("""
            #!/usr/bin/env bash
            printf '%s %s\\n' "${0##*/}" "$*" >> "$SETUP_LOG"
            if [[ "${0##*/}" == sudo ]]; then exec "$@"; fi
            """).lstrip()
        )
        executable.chmod(0o755)
    environment = {**os.environ, "PATH": f"{tmp_path}:{os.environ['PATH']}", "SETUP_LOG": str(log)}
    subprocess.run(
        ["bash", "-c", 'source "$1"; install_system_packages "$2"', "setup-test", str(SCRIPT), platform],
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    commands = log.read_text()
    assert "git git-lfs parallel" in commands
    assert ("brew install" in commands) == (platform == "darwin")
    assert ("apt-get update" in commands) == (platform == "linux")


def test_setup_rejects_corrupt_downloads(tmp_path: Path) -> None:
    """
    Refuse extraction when a downloaded Go or Helm archive fails its SHA-256 check.

    Args:
        tmp_path (Path): Local fake archive.

    Returns:
        None: The checksum check accepts matching bytes and rejects different bytes.
    """
    archive = tmp_path / "archive.tar.gz"
    archive.write_bytes(b"downloaded archive")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    command = ["bash", "-c", 'source "$1"; verify_archive "$2" "$3"', "setup-test", str(SCRIPT), str(archive), digest]
    assert subprocess.run(command, capture_output=True, text=True).returncode == 0
    archive.write_bytes(b"corrupt archive")
    failed = subprocess.run(command, capture_output=True, text=True)
    assert failed.returncode != 0 and "Checksum mismatch" in failed.stderr
