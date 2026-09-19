"""
Apply reviewed input roles only while their complete template evidence still matches.
"""

import hashlib
import json
from pathlib import Path

from hypothesis_helm_catalog.builder import DATA

from hypothesis_helm.charts import yamlio
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.schemas.resources import library


def reviewed_bindings(chart: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """
    Bridge opaque helper and tpl calls using exact, reviewed chart source snapshots.

    Args:
        chart (Path): A root or unpacked dependency chart with its original values scope.

    Returns:
        tuple[list[dict[str, object]], list[dict[str, object]]]: Generation policies and source-change diagnostics.
    """
    if not (chart / "Chart.yaml").is_file():
        return [], []
    records = sequence(json.loads((DATA / "chart-bindings.json").read_text()))
    metadata = mapping(yamlio.load((chart / "Chart.yaml").read_text()))
    result: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    for raw in records:
        binding = mapping(raw)
        if metadata.get("name") != binding["chart"]:
            continue
        files = mapping(binding["files"])
        matches = all(
            (chart / name).is_file() and hashlib.sha256((chart / name).read_bytes()).hexdigest() == digest for name, digest in files.items()
        )
        if not matches:
            diagnostics.append({"path": binding["path"], "reason": "reviewed helper source changed; input binding not applied"})
            continue
        profile = mapping(mapping(mapping(library()["upstream"])["profiles"])[str(binding["profile"])])
        quoted = bool(binding.get("quoted", True))
        restriction: dict[str, object] = {"anyOf": [profile["schema"], {"const": ""}]}
        if quoted:
            restriction["type"] = "string"
        result.append(
            {
                "path": binding["path"],
                "schema": restriction,
                "source": "reviewed-chart-binding",
                "quoted": quoted,
                "profile": binding["profile"],
                "destination": binding["destination"],
                "files": files,
                "reference": binding["reference"],
                "scope": binding.get(
                    "scope", "generated literal references or the empty fallback; supplied tpl expressions remain unchanged"
                ),
            }
        )
    return result, diagnostics
