# Helm sharded test results

<!-- toc:start -->
**Table of contents**

- [Overview](#overview)
- [Scan summary](#scan-summary)
- [Status counts](#status-counts)
- [Settings](#settings)
- [Errors](#errors)
- [Charts](#charts)
  - [test_concurrent_shards_keep_wo0](#test_concurrent_shards_keep_wo0)
<!-- toc:end -->

## Overview

![Chart severity and scan-time matrices](<report-overview.png>)

Each cell is one chart; both grids follow chart-section order. Click a cell in the PDF for details. Colors show the highest observed finding
kind, not a security or business-impact score. Hatching marks unfinished or unavailable testing, even when a finding was recorded. No
findings means none in the completed sample, not exhaustive coverage. Elapsed chart time includes dependency preparation.

## Scan summary

Run: cold. All 3 shards reported; 12 selected properties.
Executed: 12; reused cached successes: 0; failures: 1; errors: 0; skipped: 0.
Render hashes are process-local; their counts cannot establish global output uniqueness.

Directory:
/private/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/pytest-of-emmadoyle/pytest-1056/popen-gw3/test_concurrent_shards_keep_wo0/results
Started (Unix epoch): 1789761763.417759
Elapsed (wall clock): 8.27 seconds
Charts discovered: 1
Scan status: completed
Discovery complete: True
Unstarted charts: 0

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

1 failed.

## Settings

Filtering: not recorded | Seed: not recorded | Traversal: random
Chart timeout: not recorded seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Disabled checks: HH2006

## Errors

1 distinct diagnostics across 1 occurrences; 0 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### test_concurrent_shards_keep_wo0

Overview cell: 01

Status: failed | Attempts: N/A

#### E001

```text
index = 7 @pytest.mark.parametrize("index", range(12)) def test_property(index): emit_manifest({"apiVersion": "v1", "kind": "ConfigMap",
"metadata": {"name": f"case-{index}"}}) > assert index != 7 E assert 7 != 7 test_chart_values.py:9: AssertionError
```

Phase: shard 3/3: test_chart_values.test_property[7] | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<../../../../../../../../../private/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/pytest-of-emmadoyle/pytest-1056/popen-gw3/test_concurrent_shards_keep_wo0/results/shards>)

[Chart artifacts](<../../../../../../../../../private/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/pytest-of-emmadoyle/pytest-1056/popen-gw3/test_concurrent_shards_keep_wo0/results/shards>)
