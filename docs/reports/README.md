# Reports

<!-- toc:start -->
**Table of contents**

- [Reports](#reports)
<!-- toc:end -->

Final chart scan reports are published here. Benchmark studies and their plots live in top-level `studies/`.
Chart headings are larger than individual diagnostic headings. Finding codes link to an appendix at the end of each Markdown and PDF report,
with their meaning, default severity, and suggested action. The PDF appendix starts on a new page.
Chart names link to the recorded Git revision or the source URL declared in `Chart.yaml`, falling back to run artifacts when available.
Contents and overview links stay inside the report. Standalone reports omit links to unpublished artifacts.
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
