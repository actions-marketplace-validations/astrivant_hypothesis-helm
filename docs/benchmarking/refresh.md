# Repository refresh helpers

<!-- toc:start -->
**Table of contents**

- [Recovering an interrupted refresh](#recovering-an-interrupted-refresh)
  - [Recovery after measurement verification failed](#recovery-after-measurement-verification-failed)
- [Parallel refresh on GitHub Actions](#parallel-refresh-on-github-actions)
<!-- toc:end -->

[Full refresh command](README.md#reproduce-the-full-project-run) · [Benchmark results](../../studies/README.md)

These scripts prepare charts, run measurements, generate plots and publish reports.
The operation inventory lives in `pkg/hypothesis_helm/benchmarking/refresh/plan.py`.

Refresh workspaces and internal records live under `.cache/refresh/refresh-<epoch>/`.
That includes logs, timestamps, process journals, verification results, source snapshots and checksum inventories.
They are generated when needed and are not required in a fresh checkout.

The terminal shows each operation's stdout and stderr as it runs, prefixed with its name, such as `[checks]` or `[performance]`.
The complete, unprefixed output is also saved in `logs/<operation>.log`. Repository scans forward chart diagnostics while keeping
their JSON results in separate files. CI uses the same live output without progress bars.

Published measurements, plots and chart recipes remain under `studies/` and `pkg/hypothesis_helm/benchmarking/assets/fixture/`.
Repository scan reports remain under `docs/reports/`.

## Recovering an interrupted refresh

Refresh keeps completed measurements in its workspace after a failure. Keep that directory, including its
`operations.json`, logs, frozen source and checksum records. The CLI currently has no general `--resume` option;
starting it again does not continue the previous queue, and an unfinished run blocks a fresh refresh.

### Recovery after measurement verification failed

A recovery script was prepared locally for `refresh-1789617223`, where all measurements completed but the verifier
expected an obsolete clustering grid. From the project root, preview its remaining work, then resume:

```sh
bash scripts/project-run.sh python .cache/refresh/refresh-1789617223/resume.py --dry-run
bash scripts/project-run.sh python .cache/refresh/refresh-1789617223/resume.py
```

This script belongs to that saved workspace; it is not installed with the package or generated for new runs.
It preserves the 22 completed stages and starts the remaining 23 at `verify-measurements`, using the corrected verifier.
Successful verification allows profiling, diagrams, publication, and the Bitnami and Prometheus scans to continue.
It does not repeat completed benchmark measurements or resume partway through an individual measurement.

Before proceeding, it acquires the refresh lock, checks the recorded prerequisite results, and verifies the frozen source
and repaired verifier checksums. The original failed journal and logs remain available. Recovery writes its own progress
to `resumed/operations.json` and terminal output to `resumed/logs/` inside the same workspace.

The script refuses another attempt once `resumed/` exists. If recovery fails or is interrupted, inspect that journal and
its logs before planning another continuation; stages may already have published results or started repository scans.
Do not delete the recovery directory or mark failed stages complete to bypass this check. Other failure points need a
recovery plan based on their saved state, including whether the failed operation can safely run again.

## Parallel refresh on GitHub Actions

Run the **Benchmarks** workflow manually with **full-refresh** enabled. Preparation checks the project and snapshots its
inputs once. GitHub then runs each declared study on a separate runner, using the same source snapshot and parameters.
The matrix comes from the Python study inventory, so adding a study also adds its CI job.
There is no `max-parallel` setting: GitHub schedules as many jobs as the account's capacity and runner availability permit.
See [GitHub's matrix concurrency documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstrategymax-parallel).

Each study owns its output directory, status file and process journal. A failed study retains diagnostics without cancelling
other studies. The final job requires every study to succeed, verifies the merged measurements, publishes plots under `studies/`,
then runs Bitnami followed by Prometheus. Reports and logs are retained as workflow artifacts for 30 days.
Set `HH_CI_RUNNER` to override the default `ubuntu-latest-8-cores` runner label.

After pushing the workflow changes, launch it with:

```sh
gh workflow run benchmarks.yml -f full-refresh=true
```

Local `bash scripts/project-run.sh hypothesis-helm-refresh` still runs timing studies sequentially on one machine to avoid CPU contention affecting
measurements. Its `--workers` option controls independent operations within that machine; the GitHub matrix supplies separate
machines for concurrent studies. Each GitHub study job has a six-hour execution limit.

Sensitivity measures 48 input changes and all 1,128 pairs on the shared benchmark chart, with 64 structural components and a nine-minute budget.
It retains the chart sources and mutation inputs, before publication and repository scans.
Publication updates studies/sensitivity/ while preserving personal runs in studies/sensitivity/runs/.
The standalone `hypothesis-helm-benchmark sensitivity` command also updates that study automatically after a successful run.
Supplying `--output` keeps its results separate; refresh uses this option and publishes after verification.
