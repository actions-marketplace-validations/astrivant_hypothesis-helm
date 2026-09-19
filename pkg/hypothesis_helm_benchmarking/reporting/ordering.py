"""
Plot discovery order without confusing joint configurations with unique values paths.
"""

from pathlib import Path
from statistics import mean, stdev
from textwrap import dedent

import matplotlib.pyplot as plt
from hypothesis_helm.reporting.contents import with_contents
from hypothesis_helm.schemas.contracts import mapping, sequence
from matplotlib.colors import to_hex

from hypothesis_helm_benchmarking.reporting.plots import finish
from hypothesis_helm_benchmarking.reporting.variation import repeated_line

FIGURES = ("sensitivity-order-sweep", "ordering-discovery", "ordering-bug-types")


def publish(output: Path, document: dict[str, object]) -> None:
    """
    Export fixed-chart sweeps, chart matrices and a readable measured summary.

    Args:
        output (Path): Directory containing the verified raw measurements.
        document (dict[str, object]): Fixed fixtures and paired-seed discovery traces.

    Returns:
        None: PNG, SVG and Markdown artifacts are regenerated from the observations.
    """
    metadata = mapping(document["metadata"])
    fixtures = mapping(document["fixtures"])
    rows = [mapping(row) for row in sequence(document["rows"])]
    structures = list(fixtures)
    methods = [str(method) for method in sequence(metadata["methods"])]
    maximum = int(str(metadata["permutations"]))
    colors = {method: to_hex(plt.get_cmap("tab10")(index % 10)) for index, method in enumerate(methods)}

    def trials(structure: str, method: str) -> list[dict[str, object]]:
        """
        Select comparable repeats without mixing chart populations.

        Args:
            structure (str): Fixed chart family.
            method (str): Traversal strategy and optional sensitivity order.

        Returns:
            list[dict[str, object]]: Paired seed measurements for this setting.
        """
        return [row for row in rows if row["structure"] == structure and row["method"] == method]

    fixed = "interactions" if "interactions" in fixtures else structures[0]
    orders = list(range(maximum + 1))
    figure, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    for axis, metric, title in zip(
        axes, ("early_recall_percent", "discovery_area_percent"), ("Bugs found after 25% of tests", "Discovery curve area"), strict=True
    ):
        repeated_line(
            axis,
            orders,
            [[float(str(row[metric])) for row in trials(fixed, "random" if order == 0 else f"sensitivity-{order}")] for order in orders],
            fixed,
            "#2563eb",
            upper=100,
        )
        axis.set(xlabel="Sensitivity order r (0 = seeded random)", ylabel=f"{title} (%)", xticks=orders, ylim=(0, 105))
        axis.grid(alpha=0.2)
    figure.suptitle(f"Sensitivity ordering on one fixed {fixed} chart (p={maximum})")
    finish(
        figure,
        output,
        FIGURES[0],
        "Higher is better. Profiling tests count in both metrics. Curve area rewards earlier discovery; it is not final recall.",
        question="Does measuring higher-order interactions find defects earlier, after counting the tests needed to learn them?",
    )

    figure, axes = plt.subplots(len(structures), 2, squeeze=False, figsize=(15, 3.3 * len(structures) + 1.6))
    for index, structure in enumerate(structures):
        fixture = mapping(fixtures[structure])
        count, total = int(str(fixture["cases"])), len(mapping(fixture["bug_orders"]))
        # At most 81 displayed checkpoints; every executed input remains in results.json.
        checkpoints = sorted({1, count, *(max(1, round(count * fraction / 80)) for fraction in range(1, 81))})
        for method in methods:
            batch = trials(structure, method)
            traces = [[mapping(point) for point in sequence(row["trace"])] for row in batch]
            repeated_line(
                axes[index, 0],
                checkpoints,
                [[float(str(trace[step - 1]["found"])) for trace in traces] for step in checkpoints],
                method,
                colors[method],
                upper=total,
            )
            paths = list(range(1, len(mapping(fixture["paths"])) + 1))
            repeated_line(
                axes[index, 1],
                paths,
                [
                    [float(str(next(point for point in trace if int(str(point["distinct_paths"])) >= size)["found"])) for trace in traces]
                    for size in paths
                ],
                method,
                colors[method],
                upper=total,
            )
        axes[index, 0].set(title=f"{structure}: {count} tests, {total} known bugs", xlabel="Test iteration (baseline included)")
        axes[index, 1].set(title=f"{structure}: first reaching each path count", xlabel="Distinct changed values paths reached")
        for axis in axes[index]:
            axis.set(ylabel="Distinct bugs found", ylim=(0, total * 1.1))
            axis.grid(alpha=0.2)
    axes[0, 0].legend(fontsize=7, ncol=2)
    figure.suptitle("How traversal changes the rate of bug discovery")
    finish(
        figure,
        output,
        FIGURES[1],
        "One fixed chart and bug population per row. A joint test can change several paths. "
        "Reaching every path does not exhaust its values. "
        "Right panels stop at the first test reaching each path count. Deterministic strategies repeat identically across seeds.",
        question="Which strategy finds more bugs at the same test iteration, and how many bugs have appeared when paths are first reached?",
    )

    figure, axes = plt.subplots(len(structures), maximum, squeeze=False, figsize=(max(12, 5 * maximum), 3.1 * len(structures) + 1.6))
    for index, structure in enumerate(structures):
        fixture = mapping(fixtures[structure])
        count = int(str(fixture["cases"]))
        checkpoints = sorted({1, count, *(max(1, round(count * fraction / 60)) for fraction in range(1, 61))})
        for order in range(1, maximum + 1):
            axis = axes[index, order - 1]
            total = sum(int(str(value)) == order for value in mapping(fixture["bug_orders"]).values())
            for method in methods:
                traces = [[mapping(point) for point in sequence(row["trace"])] for row in trials(structure, method)]
                repeated_line(
                    axis,
                    checkpoints,
                    [[float(str(mapping(trace[step - 1]["found_by_order"])[str(order)])) for trace in traces] for step in checkpoints],
                    method,
                    colors[method],
                    upper=total,
                )
            axis.set(title=f"{structure}: {order}-path bugs", xlabel="Test iteration", ylabel="Distinct bugs found", ylim=(0, total * 1.1))
            axis.grid(alpha=0.2)
    axes[0, 0].legend(fontsize=7, ncol=2)
    figure.suptitle("Discovery by chart structure and bug interaction order")
    finish(
        figure,
        output,
        FIGURES[2],
        dedent(
            """
            Categories count simultaneous Boolean conditions in each injected trigger.
            These synthetic semantic defects do not represent real-world failure rates.
            Bands show traversal-seed variation on each fixed chart.
            """
        ).strip(),
        question="Does an ordering help simple one-field defects, interacting defects, or both, and does that change with chart structure?",
    )
    summary = [
        "| Chart | Traversal | Bugs found after 25% of tests | Discovery area |",
        "| --- | --- | ---: | ---: |",
    ]
    for structure in structures:
        for method in methods:
            batch = trials(structure, method)
            cells = []
            for metric in ("early_recall_percent", "discovery_area_percent"):
                values = [float(str(row[metric])) for row in batch]
                cells.append(f"{mean(values):.1f}% ± {stdev(values) if len(values) > 1 else 0:.1f} pp")
            summary.append(f"| {structure} | {method} | {' | '.join(cells)} |")
    command = (
        f"bash scripts/project-run.sh hypothesis-helm-benchmark sensitivity-ordering --inputs {metadata['inputs']} "
        f"--permutations {maximum} --repeats {metadata['repeats']} --seed {metadata['seed']} "
        f"--bugs-per-order {metadata['bugs_per_order']} --structures {' '.join(structures)} "
        f"--time-limit {metadata['time_limit_seconds']}s --output .cache/benchmarks/sensitivity-ordering"
    )
    readme = dedent(
        f"""
        # Sensitivity ordering

        Does prioritizing interacting values find bugs earlier? These comparisons change only execution order within each chart.

        ## Sensitivity order on a fixed chart

        Here p={maximum} is the requested `--permutations` interaction strength. The sweep uses r=0..p:
        r=0 means random traversal without profiling; r>0 uses the production sensitivity scheduler up to that interaction order.
        The chart, bugs and selected configurations remain fixed. The normal small-space enumeration rule is enabled;
        each fixture records its effective coverage strength, which may exceed p.

        ![Fixed-chart sensitivity order sweep](sensitivity-order-sweep.png)

        ## Discovery across chart structures

        Each row uses the shared benchmark chart with a different structural setting. Fields sit at depths one through three.
        The left column counts joint configuration tests, including baseline and profiling tests. The right column shows bugs found
        at the first test reaching each number of distinct changed paths. It is not a one-path-per-test executor.

        ![Traversal discovery by chart structure](ordering-discovery.png)

        ## Bug interaction orders

        A one-path bug needs one Boolean condition; a three-path bug needs three conditions simultaneously.
        Bug placement is sampled independently of traversal priorities, then checked for reachability. The same bug population
        is used by every strategy and seed on a chart. Structure can make some triggers unreachable, so chart rows can differ.

        ![Bug discovery by trigger order](ordering-bug-types.png)

        ## Measurements

        Values below are means ± one sample standard deviation across {metadata["repeats"]} paired traversal seeds.
        Plot bands show one and two standard deviations, not confidence intervals or guarantees about other charts.
        Higher discovery area means bugs were generally found earlier. Every completed traversal visits the same inputs exactly once.

        ## Method and limits

        Each schema-valid candidate was actually rendered with Helm once, and its injected faults checked against an independent oracle.
        Those recorded outputs are replayed through the production traversal functions. Sensitivity sees an output only when its test
        is visited; a failing test supplies no ranking evidence, just as in the application. Missing references stay unknown.
        Profiling inputs are real bug tests, not free setup. Baseline-only equivalent outputs do not authorize new pruning.

        Filtering, sampling and failure expansion are disabled to isolate ordering. All strategies use serial scheduling here.
        Recorded render times are individual reference measurements, not fresh end-to-end runtimes of each strategy.
        These synthetic semantic defects exercise discovery; the experiment does not measure every type of Helm or Kubernetes error.

        Raw traces: [results.json](results.json). Summary: [results.csv](results.csv).
        Each chart has a retained `cases/*.yaml` generator recipe, source snapshot and compressed observations.

        ## Generate or redraw

        Run from the project root with benchmarking dependencies and Helm available. Use a fresh output directory for each measurement.
        `--time-limit` bounds reference renders and ordering replay per chart.
        An incomplete matrix is retained but not published as complete.

        ```bash
        {command}
        ```

        Redraw existing measurements without invoking Helm:

        ```bash
        hypothesis-helm-benchmark sensitivity-ordering --plot-only --output .cache/benchmarks/sensitivity-ordering
        ```
        """
    ).lstrip()
    readme = readme.replace("## Method and limits", "\n".join(summary) + "\n\n## Method and limits")
    (output / "README.md").write_text(with_contents(readme))
