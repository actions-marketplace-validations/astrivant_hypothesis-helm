"""
Verify chart-grouped diagnostics retain exact triggering paths and joint values.
"""

import base64
import copy
import gzip
import json
import re
import zlib
from pathlib import Path

import pytest

from hypothesis_helm.reporting.evidence.errors import deduplicate_errors
from hypothesis_helm.reporting.evidence.reproductions import changed_values, failing_input, input_summary
from hypothesis_helm.reporting.reports.links import Publication, linked_prose, publish_links
from hypothesis_helm.reporting.reports.repository import artifact_link, write_reports
from hypothesis_helm.schemas.contracts import mapping, sequence


@pytest.mark.parametrize(
    "diagnostic",
    [
        '[HH1101] while constructing a mapping\n  in "<unicode string>", line 1574, column 3:\n'
        '    containers: ^ (line: 1574)\nfound duplicate key "containers"\n'
        "To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys",
        "[HH1101] Error: YAML parse error on demo/templates/deployment.yaml: "
        "error converting YAML to JSON: yaml: line 29: did not find expected ',' or ']'",
    ],
)
def test_parser_diagnostics_stay_in_data_not_human_reports(tmp_path: Path, diagnostic: str) -> None:
    """
    Keep parser failures and inputs visible without repeating parser excerpts or suppression advice.

    Args:
        tmp_path (Path): Markdown and PDF report destination.
        diagnostic (str): Detailed diagnostic from either the YAML parser or Helm.

    Returns:
        None: Human reports show the status and values; saved evidence and finding counts remain intact.
    """
    chart: dict[str, object] = {
        "chart": "demo",
        "status": "failed",
        "error": diagnostic,
        "path": ["extraPodSpec", "containers"],
        "values": {"extraPodSpec": {"containers": []}},
        "input_changes": {"$.extraPodSpec.containers": []},
    }
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1,
        "elapsed_seconds": 1,
        "charts_discovered": 1,
        "counts": {"failed": 1},
        "settings": {},
        "charts": [chart],
    }
    markdown, pdf = write_reports(report, tmp_path / "report", artifact_links=False)
    text = markdown.read_text()
    assert "HH1101" in text and "Invalid YAML in rendered output" in text
    assert "Status: failed | Phase:" in text
    assert "$.extraPodSpec.containers = []" in text
    assert "```text" not in text
    forbidden = ("To suppress this check", "Duplicate_keys", "containers: ^", "line 1574", "error converting YAML to JSON")
    for fragment in forbidden:
        assert fragment not in text
    streams = []
    for body in re.findall(rb"\d+ 0 obj\s*(.*?)\s*endobj", pdf.read_bytes(), re.DOTALL):
        if b"/Subtype /Image" in body:
            continue
        if b"/Filter [ /ASCII85Decode /FlateDecode ]" in body and (match := re.search(rb"stream\s*\n(.*?)endstream", body, re.DOTALL)):
            streams.append(zlib.decompress(base64.a85decode(match[1].strip(), adobe=True)))
    drawn = b"\n".join(streams)
    assert b"Status: failed" in drawn and b"$.extraPodSpec.containers" in drawn
    for fragment in forbidden:
        assert fragment.encode() not in drawn
    assert report["counts"] == {"failed": 1}
    assert mapping(report["error_summary"])["unique_errors"] == 1
    group = mapping(sequence(report["error_groups"])[0])
    assert group["code"] == "HH1101" and group["error"] == diagnostic
    assert chart["error"] == diagnostic
    assert mapping(mapping(sequence(group["occurrences"])[0])["input"])["changes"] == {"$.extraPodSpec.containers": []}


@pytest.mark.parametrize("published", [False, True])
def test_audit_json_links_have_complete_portable_data(tmp_path: Path, published: bool) -> None:
    """
    Make abbreviated audit summaries open the actual chart data in Markdown and PDF.

    Args:
        tmp_path (Path): Report publication directory, without any raw run artifacts.
        published (bool): Whether attachments use public URLs or local report-relative paths.

    Returns:
        None: Both formats link existing, complete chart-specific JSON with the correct run identity.
    """
    findings = [
        {"code": "HH2001", "path": [f"field{index}"], "references": [{"file": "templates/deployment.yaml", "line": index + 1}]}
        for index in range(6)
    ]
    unresolved = [{"code": "HH2005", "path": [], "file": "templates/_helpers.tpl", "line": 10}]
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1,
        "elapsed_seconds": 1,
        "charts_discovered": 3,
        "counts": {"passed": 3},
        "settings": {},
        "charts": [
            {"chart": "one/demo", "status": "passed", "audit": {"findings": findings, "unresolved": unresolved}},
            {"chart": "two/demo", "status": "passed", "audit": {"findings": findings[:1]}},
            {"chart": "empty", "status": "passed", "audit": {}},
        ],
    }
    directory = tmp_path / "reports with spaces"
    publication = Publication(tmp_path, "https://github.com/example/reports", "main") if published else None
    markdown, pdf = write_reports(report, directory / "scan.md", publication=publication, artifact_links=False)
    data = directory / "scan-data" / "0001.audit.json.gz"
    document = json.loads(gzip.decompress(data.read_bytes()))
    assert document == {
        "chart": "one/demo",
        "run_hash": report["run_hash"],
        "started_at": report["started_at"],
        "finished_at": report["finished_at"],
        "findings": findings,
        "unresolved": unresolved,
    }
    other = json.loads(gzip.decompress((data.parent / "0002.audit.json.gz").read_bytes()))
    assert other["chart"] == "two/demo"
    assert other["findings"] == findings[:1]
    assert len(list(data.parent.iterdir())) == 2
    relative = "scan-data/0001.audit.json.gz"
    target = publication.url(relative, markdown) if publication else relative
    assert f"1 additional audit findings in [JSON](<{target}>)." in " ".join(markdown.read_text().split())
    uri = target if publication else data.resolve().as_uri()
    assert uri.encode() in re.findall(rb"/URI\s*\(([^)]+)\)", pdf.read_bytes())
    if published:
        assert b"file:" not in pdf.read_bytes()


def test_exact_input_paths_and_empty_values() -> None:
    """
    Preserve literal keys, indexed lists, false, zero, empty strings, containers, and null.

    Returns:
        None: Flattened paths retain distinct keys and every supplied leaf value.
    """
    source: dict[str, object] = {"values": {"a.b": False, "a": {"b": 0}, "*": "", "list": [None, {}, []]}}
    assert failing_input(source)["paths"] == {
        '$["a.b"]': False,
        "$.a.b": 0,
        '$["*"]': "",
        "$.list[0]": None,
        "$.list[1]": {},
        "$.list[2]": [],
    }
    selected = failing_input({**source, "paths": [["a", "b"], ["list", 0], ["missing"]]})
    assert selected["paths"] == failing_input(source)["paths"]
    assert list(mapping(selected["paths"]))[:2] == ["$.a.b", "$.list[0]"]
    assert selected["absent_paths"] == ["$.missing"]
    assert failing_input({}) == {"recorded": False}
    assert failing_input({"values": {}})["paths"] == {"$": {}}


def test_reports_group_errors_and_inputs_by_chart(tmp_path: Path) -> None:
    """
    Keep diagnostics shared in JSON while showing chart-specific joint inputs inline.

    Args:
        tmp_path (Path): Markdown and PDF report destination.

    Returns:
        None: Each chart section includes its diagnostic and the values used together.
    """
    error = "incompatible ingress and service\nUse --debug flag to render out invalid YAML"
    phases = [
        {
            "phase": "permutations",
            "status": "failed",
            "error": error,
            "values": {"ingress": {"enabled": True}, "service": {"type": "ExternalName", "externalName": ""}},
        },
        {
            "phase": "$.service.port",
            "path": ["service", "port"],
            "status": "failed",
            "error": error,
            "values": {"service": {"port": 0}, "dependentSibling": "required context"},
            "artifacts": "second/paths/port",
        },
    ]
    report: dict[str, object] = {
        "directory": "/charts",
        "started_epoch": 1,
        "elapsed_seconds": 1,
        "charts_discovered": 2,
        "counts": {"failed": 2},
        "settings": {},
        "charts": [
            {"chart": "first", "status": "failed", "phases": [phases[0]], "artifacts": "first"},
            {"chart": "second", "status": "failed", "phases": [phases[1]], "artifacts": "second"},
        ],
    }
    original = copy.deepcopy(phases)
    markdown, pdf = write_reports(report, tmp_path / "report")
    first, second = markdown.read_text().split("### first\n", 1)[1].split("### second\n", 1)
    assert "incompatible ingress and service" in first and "incompatible ingress and service" in second
    assert "$.ingress.enabled = true" in first
    assert '$.service.type = "ExternalName"' in first
    assert '$.service.externalName = ""' in first
    assert "$.service.port = 0" in second
    assert "Full input and diagnostic" not in second
    assert "Chart artifacts" not in second
    assert "required context" not in second
    assert "Selected fields (full context in artifacts)" in second
    assert "--debug" not in markdown.read_text()
    assert "used together" in first
    assert report["error_summary"] == {"unique_errors": 1, "occurrences": 2, "duplicates": 1}
    assert phases == original
    assert pdf.read_bytes().startswith(b"%PDF")
    snapshot = copy.deepcopy(report)
    deduplicate_errors(report)
    assert report == snapshot


def test_expansion_keeps_each_failing_permutation(tmp_path: Path) -> None:
    """
    Retain expansion failures without duplicating the primary counterexample.

    Args:
        tmp_path (Path): Joint-input report destination.

    Returns:
        None: Every failing configuration appears under its chart and shared diagnostic.
    """
    failures = [{"error": "bad pair", "values": {"enabled": True, "port": value}} for value in (0, 1)]
    report: dict[str, object] = {
        "directory": "/charts",
        "started_epoch": 1,
        "elapsed_seconds": 1,
        "charts_discovered": 1,
        "counts": {"failed": 1},
        "settings": {},
        "charts": [{"chart": "demo", "status": "failed", **failures[0], "failure_expansion": {"failures": failures}}],
    }
    markdown, _ = write_reports(report, tmp_path / "report")
    groups = sequence(report["error_groups"])
    assert len(groups) == 1
    occurrences = [mapping(item) for item in sequence(mapping(groups[0])["occurrences"])]
    assert len(occurrences) == 2
    assert [mapping(mapping(item["input"])["paths"])["$.port"] for item in occurrences] == [0, 1]
    text = markdown.read_text()
    assert text.count("bad pair") == 1
    assert "$.port = 0" in text and "$.port = 1" in text


def test_changed_overrides_and_bounded_previews(tmp_path: Path) -> None:
    """
    Keep changed siblings visible and bound large inputs without dropping stored cases.

    Args:
        tmp_path (Path): Compact report destination.

    Returns:
        None: Defaults disappear from summaries, while full inputs and cases remain available.
    """
    defaults = {"service": {"port": 80, "peers": ["a", "b"]}, "enabled": True, "untouched": "default"}
    values = {"service": {"port": 0, "peers": ["a"]}, "enabled": False, "untouched": "default", "new": None}
    changes = changed_values(values, defaults)
    assert changes == {"$.service.port": 0, "$.service.peers": ["a"], "$.enabled": False, "$.new": None}
    assert changed_values({}, defaults) == {}
    assert changed_values({"service": {}}, defaults) == {}
    assert changed_values({"x": None}, {"x": None}) == {"$.x": None}
    assert changed_values({"x": False}, {"x": 0}) == {"$.x": False}
    assert changed_values({"x": 1.0}, {"x": 1}) == {"$.x": 1.0}
    evidence = failing_input({"values": values, "path": ["service", "port"], "input_changes": changes})
    summary = "\n".join(input_summary(evidence))
    assert "$.enabled = false" in summary and "untouched" not in summary
    large = {f"field{i}": "x" * 10000 for i in range(1000)}
    failures = [{"values": large, "error": "bad input", "phase": str(index), "status": "failed"} for index in range(100)]
    report: dict[str, object] = {
        "directory": "/charts",
        "started_epoch": 1,
        "elapsed_seconds": 1,
        "charts_discovered": 1,
        "counts": {"failed": 1},
        "settings": {},
        "charts": [{"chart": "demo", "status": "failed", "phases": failures, "artifacts": "full-evidence"}],
    }
    markdown, pdf = write_reports(report, tmp_path / "brief")
    text = markdown.read_text()
    assert len(text) < 5000
    assert "98 additional occurrences" in text
    assert "994 more paths" in text
    assert "value shortened" in text
    assert "full-evidence" not in text
    assert mapping(sequence(report["charts"])[0])["artifacts"] == "full-evidence"
    assert b"/Subtype /Link" in pdf.read_bytes()
    assert mapping(report["error_summary"])["occurrences"] == 100
    assert mapping(sequence(report["charts"])[0])["phases"] == failures
    assert artifact_link("Input", tmp_path / "saved inputs", tmp_path / "report.md") == "[Input](<saved%20inputs>)"
    assert artifact_link("Input", "retained-run/inputs", tmp_path / "report.md") == "[Input](<retained-run/inputs>)"


def test_public_pdf_links(tmp_path: Path) -> None:
    """
    Render public links for files, folders, and multiple inline labels on main.

    Args:
        tmp_path (Path): Publication checkout containing retained inputs and reports.

    Returns:
        None: PDF annotations and Markdown targets agree and contain no local paths.
    """
    artifacts = tmp_path / "docs" / "saved inputs"
    artifacts.mkdir(parents=True)
    (artifacts / "values.json").write_text("{}")
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1,
        "elapsed_seconds": 1,
        "charts_discovered": 1,
        "counts": {"failed": 1},
        "settings": {},
        "summary": ["[Input & values](<saved%20inputs/values.json>) and [All inputs](<saved%20inputs>)"],
        "charts": [{"chart": "demo", "status": "failed", "error": "failure", "artifacts": str(artifacts)}],
    }
    publication = Publication(tmp_path, "https://github.com/example/charts", "main")
    markdown, pdf = write_reports(report, tmp_path / "docs" / "report", publication=publication)
    uris = re.findall(rb"/URI\s*\(([^)]+)\)", pdf.read_bytes())
    # The framework attribution is a PDF footer, separate from report evidence.
    uris = [uri for uri in uris if uri != b"https://github.com/HypothesisWorks/hypothesis/"]
    assert len(uris) == 5
    assert all(uri.startswith(b"https://github.com/example/charts/") for uri in uris)
    assert b"https://github.com/example/charts/blob/main/docs/saved%20inputs/values.json" in uris
    assert b"https://github.com/example/charts/tree/main/docs/saved%20inputs" in uris
    assert all(uri.decode() in markdown.read_text() for uri in uris)
    assert "### [demo](<https://github.com/example/charts/tree/main/docs/saved%20inputs>)" in markdown.read_text()
    assert str(tmp_path) not in markdown.read_text()
    assert publication.url("#charts", markdown) == "#charts"
    assert publish_links("[Charts](#charts)", markdown, publication) == "[Charts](<#charts>)"
    assert "https://github.com/example/charts/raw/main/docs/report-overview.png" in markdown.read_text()
    with pytest.raises(ValueError):
        publication.url("../../outside", markdown)
    with pytest.raises(ValueError):
        publication.url("file:///private/input.json", markdown)
    literal = '`$.input = "[literal](../../outside)"`'
    assert publish_links(literal, markdown, publication) == literal
    assert "<link " not in linked_prose(literal)


@pytest.mark.parametrize("filename", ["report.json", "observed-failure.json"])
@pytest.mark.parametrize("relative", [False, True])
def test_local_pdf_diagnostic_links_are_omitted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, filename: str, relative: bool) -> None:
    """
    Avoid publishing file links that PDF readers block or other machines cannot resolve.

    Args:
        tmp_path (Path): Report location with spaces and reserved characters in the artifact path.
        monkeypatch (pytest.MonkeyPatch): Run the writer from an unrelated directory.
        filename (str): Complete report or checkpoint left by an interrupted run.
        relative (bool): Whether the recorded artifact directory is report-relative or absolute.

    Returns:
        None: Reports omit local evidence links even when the files exist, preserving evidence on disk.
    """
    directory = tmp_path / "reports"
    artifacts = directory / "saved inputs (one) # café"
    artifacts.mkdir(parents=True)
    evidence = artifacts / filename
    evidence.write_text('{"values": {"enabled": true}, "error": "invalid output"}')
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1,
        "elapsed_seconds": 1,
        "charts_discovered": 1,
        "counts": {"failed": 1},
        "settings": {},
        "charts": [
            {
                "chart": "demo",
                "status": "failed",
                "error": "invalid output",
                "artifacts": artifacts.name if relative else str(artifacts),
            }
        ],
    }
    markdown, pdf = write_reports(report, directory / "report")
    assert "Full input and diagnostic" not in markdown.read_text()
    assert "Chart artifacts" not in markdown.read_text()
    uris = re.findall(rb"/URI\s*\(([^)]+)\)", pdf.read_bytes())
    assert not any(uri.startswith(b"file:") for uri in uris)
    assert evidence.is_file()
    assert b"/Dest" in pdf.read_bytes()
    assert str(tmp_path) not in markdown.read_text()
