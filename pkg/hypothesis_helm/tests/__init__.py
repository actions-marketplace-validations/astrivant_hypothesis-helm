"""
Verify chart testing by responsibility and share stable repository fixture locations.
"""

from pathlib import Path

__all__ = ["FIXTURES", "PACKAGE_ROOT", "PACKAGES_ROOT", "PROJECT_ROOT"]

# Resolve paths here so individual tests can move between categories without changing fixtures.
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PACKAGES_ROOT = PACKAGE_ROOT.parent
PROJECT_ROOT = PACKAGES_ROOT.parent
