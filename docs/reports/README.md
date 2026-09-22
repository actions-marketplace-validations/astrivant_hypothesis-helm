# Reports

<!-- toc:start -->
**Table of contents**

- [Diagrams and sensitivity](#diagrams-and-sensitivity)
- [Findings versus testing limitations](#findings-versus-testing-limitations)
<!-- toc:end -->

Final chart scan reports are published here. Benchmark studies and their plots live in top-level `studies/`.
Chart headings are larger than individual diagnostic headings. Finding codes link to an appendix at the end of each Markdown and PDF report,
with their meaning, default severity, and suggested action. The PDF appendix starts on a new page.
Chart names link to the recorded Git revision or the source URL declared in `Chart.yaml`, falling back to run artifacts when available.
Contents and overview links stay inside the report. Standalone reports omit links to unpublished artifacts.
Each chart's audit summary links **JSON** to its complete findings, including paths and template references, in a compressed
`<report>-data/*.audit.json.gz` attachment. Keep that directory with the report when sharing it; decompress the file to read the JSON.
Published reports use public links to these attachments, which include the scan's run fingerprint and timestamps.
From page two onward, the PDF includes a bottom-right link to the Hypothesis framework repository; page numbers are centered in the footer.
Historical scans without a recorded commit link to their recorded upstream branch.

Each report records the start and finish date/time in UTC and a SHA-256 run fingerprint, also saved in the scan JSON.
The finish time records when execution stopped, including interrupted or timed-out scans; check the scan status for completion.
For older records without a finish timestamp, the report labels the estimate from the recorded start and elapsed duration.
An aggregate uses the latest shard finish time, not the time its report was generated.

The fingerprint identifies the source, execution identity, start/finish timestamps, and recorded settings
(`sha256-run-metadata-v1`). It stays the same when the report is republished or reformatted.
It is a run identifier, not a checksum of the PDF or proof that a scan completed successfully.
Aggregated bundles retain separate artifact checksums for file integrity.

- [Bitnami charts](bitnami.md) · [PDF](bitnami.pdf)
- [Prometheus Community charts](prometheus.md) · [PDF](prometheus.pdf)
- [Benchmark studies](../../studies/README.md)

Worker files, raw measurements, generated chart copies and resume journals stay under `.cache/`.
See [refresh and recovery](../benchmarking/refresh.md) for regeneration and resume commands.

## Diagrams and sensitivity

Report titles and PDF page headers identify the scanned source, such as `Scan results: github.com/bitnami/charts`.

PDF reports begin with a title page naming the scanned source, its recorded start and finish times in UTC, and the source commit when available.
The title-page source and commit link to their public repository pages when those URLs are known.
The contents follow on page two and the overview on page three. When published chart-topology measurements are available, two aggregate
graph plots follow on page four, before the scan summary. These plots include only charts listed in the report, with missing measurements
counted explicitly. Each chart heading is immediately followed by its topology and sensitivity panels, including charts without reported
errors. Larger labels are used so the plots remain readable side by side in the PDF.
Sensitivity heatmap rows and columns use short field numbers. A caption beneath each chart's plots maps those numbers to full values paths.
Overview matrices and sensitivity heatmaps use square plotting areas and square cells. The overview places its two matrices side by side;
large chart inventories use numbered cells linked to the full chart names in the report.

Sensitivity measures how rendered fields change after selected input changes, and whether pairs interact. These measurements are separate
from the scan's findings and elapsed time. The default measures up to eight existing Boolean or integer paths and all pairs among them,
using six concurrent chart jobs and a three-minute measurement budget per chart. Dependency preparation is separate.
Only schema-valid changes are attempted; rendering failures and unavailable measurements are never plotted as zero sensitivity.
Charts with uncontrolled effects or changing baseline renders receive an explanatory panel instead of an attributed sensitivity score.
These observations describe one baseline and a small sample, not every possible configuration or a proof that pruning is safe.

Repository refresh generates these panels during finalization. To add them to an existing scan independently:

```bash
hypothesis-helm-report-figures .cache/path/to/scan.json --report docs/reports/bitnami \
    --source-root third_party/bitnami-charts --repository bitnami --jobs 6
```

The source checkout must match the scan's recorded Git revision. Use `--max-mutations`, `--seed`, and `--time-limit` to change the sample.
Final PNGs go to `studies/chart-topologies/`; raw measurements and an enriched report JSON stay under `.cache/report-figures/`.
The command requires Matplotlib, included in the project's normal installation.

## Findings versus testing limitations

`E001`, `E002`, and subsequent numbers identify diagnostics within one report. They are not stable finding codes for configuration.
Unsupported-schema and unexecuted-work records do not receive these numbers by default. Their status and explanation remain visible
as testing limitations, so an untested chart is not presented as passing. Actual findings retain their `HH` codes and numbered entries.
