"""
Apply reviewed input roles only while their complete template evidence still matches.
"""

import hashlib
import json
from pathlib import Path

from hypothesis_helm_catalog.builder import DATA

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.schemas.resources import destination, library


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
        quoted = bool(binding.get("quoted", True))
        if "profile" in binding:
            profile = mapping(mapping(mapping(library()["upstream"])["profiles"])[str(binding["profile"])])
            restriction: dict[str, object] = {"anyOf": [profile["schema"], {"const": ""}]}
        else:
            identity, _, output = str(binding["destination"]).partition(":$.")
            found = destination(identity, tuple(output.split("."))) if output else None
            if found is None:
                diagnostics.append(
                    {"path": binding["path"], "reason": "reviewed destination schema unavailable; input binding not applied"}
                )
                continue
            restriction, _ = found
        if quoted:
            restriction["type"] = "string"
        result.append(
            {
                "path": binding["path"],
                "schema": restriction,
                "source": "reviewed-chart-binding",
                "quoted": quoted,
                "serialized": bool(binding.get("serialized", False)),
                "profile": binding.get("profile"),
                "destination": binding["destination"],
                "files": files,
                "reference": binding["reference"],
                "scope": binding.get(
                    "scope", "generated literal references or the empty fallback; supplied tpl expressions remain unchanged"
                ),
            }
        )
    # Several reviewed chart versions can describe the same input. A matching
    # version supersedes source-mismatch notes for that path, not other paths.
    applied = {tuple(sequence(rule["path"])) for rule in result}
    return result, [note for note in diagnostics if tuple(sequence(note["path"])) not in applied]
