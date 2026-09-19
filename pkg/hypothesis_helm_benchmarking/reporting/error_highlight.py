"""
Present matched error discovery, render counts and runtime from the error-surface study.
"""

from pathlib import Path
from statistics import mean, stdev

from hypothesis_helm.schemas.contracts import mapping, number, sequence

from hypothesis_helm_benchmarking.reporting.plots import finish


def plot(output: Path, document: dict[str, object]) -> bool:
    """
    Compare all clustering settings at five percent requested errors without selecting favorable seeds.

    Args:
        output (Path): Destination for the README highlight figure.
        document (dict[str, object]): Recorded error-surface results and their paired settings.

    Returns:
        bool: Whether a complete, matched comparison was available and plotted.

    Raises:
        ValueError: Duplicate observations or mismatched populations would invalidate the comparison.
    """
    metadata = mapping(document["metadata"])
    axes = mapping(metadata["axes"])
    if "clustering" not in axes:
        return False
    methods = ("default", "exact-equivalence")
    rows = [
        mapping(row)
        for row in sequence(document["rows"])
        if mapping(row).get("axis") == "clustering" and mapping(row).get("error_percent") == 5 and mapping(row).get("strategy") in methods
    ]
    expected = {
        (number(value), repeat, method)
        for value in sequence(axes["clustering"])
        for repeat in range(int(number(metadata["repeats"])))
        for method in methods
    }
    indexed = {(number(row["axis_value"]), int(number(row["repeat"])), str(row["strategy"])): row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError("Duplicate error-highlight observations")
    if set(indexed) != expected or any(row["status"] != "passed" for row in rows):
        return False
    for value, repeat, _ in expected:
        baseline, pruned = (indexed[value, repeat, method] for method in methods)
        for key in ("population_sha256", "chart_sha256", "error_count", "valid_domain"):
            if baseline[key] != pruned[key]:
                raise ValueError(f"Unmatched error-highlight {key}")
    populations = {int(number(row["error_count"])) for row in rows}
    domains = {int(number(row["valid_domain"])) for row in rows}
    if len(populations) != 1 or len(domains) != 1:
        return False

    from matplotlib import pyplot as plt

    figure, panels = plt.subplots(1, 3, figsize=(13, 4.8))
    colors = ("#64748b", "#059669")
    labels = ("Without pruning", "Exact-equivalence\npruning")
    for panel, key, title in zip(
        panels,
        ("errors_detected", "render_invocations", "total_seconds"),
        (f"Failing inputs found (out of {populations.pop()})", "Helm renders", "Total time (seconds)"),
        strict=True,
    ):
        batches = [[number(row[key]) for row in rows if row["strategy"] == method] for method in methods]
        values = [mean(batch) for batch in batches]
        deviations = [stdev(batch) if len(batch) > 1 else 0 for batch in batches]
        bars = panel.bar(labels, values, yerr=deviations, capsize=5, color=colors, width=0.55)
        panel.bar_label(bars, labels=[f"{value:.2f}" if key == "total_seconds" else f"{value:g}" for value in values], padding=9)
        panel.set_title(title, fontsize=12, pad=16)
        panel.set_ylim(0, max(value + sd for value, sd in zip(values, deviations, strict=True)) * 1.3 or 1)
        panel.spines[["top", "right"]].set_visible(False)
        panel.set_axisbelow(True)
        panel.grid(axis="y", alpha=0.15)
    figure.suptitle("Errors found, with fewer Helm renders", fontsize=20)
    finish(
        figure,
        output,
        "errors-found-fast",
        f"Synthetic input-aware failures; {domains.pop()} inputs checked per run. "
        f"Means ±1 SD across {len(rows) // 2} runs per method (all clustering settings and seeds).",
        question="Can we find the same failing inputs faster by reusing equivalent rendered manifests?",
    )
    return True
