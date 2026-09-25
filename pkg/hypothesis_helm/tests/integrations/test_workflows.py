"""
Verify workflow dependency graphs and the release artifact handoff after CI separation.
"""

from graphlib import TopologicalSorter
from pathlib import Path

from ruamel.yaml import YAML

from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.tests import PROJECT_ROOT

ROOT = PROJECT_ROOT


def workflows() -> dict[str, dict[str, object]]:
    """
    Read the maintained workflow definitions without interpreting YAML booleans as keys.

    Returns:
        dict[str, dict[str, object]]: Workflow filenames mapped to their definitions.
    """
    return {path.name: mapping(YAML(typ="safe").load(path.read_text())) for path in (ROOT / ".github/workflows").glob("*.yml")}


def test_workflow_references_and_dependencies() -> None:
    """
    Reject dangling local actions, missing job prerequisites and recursive workflow calls.

    Returns:
        None: Renamed workflows resolve, have distinct display names, and form valid job graphs.
    """
    documents = workflows()
    assert len({document["name"] for document in documents.values()}) == len(documents)
    calls: dict[str, set[str]] = {}
    for filename, document in documents.items():
        calls[filename] = set()
        jobs = mapping(document["jobs"])
        dependencies: dict[str, set[str]] = {}
        for job_id, raw in jobs.items():
            job = mapping(raw)
            assert job.get("name"), (filename, job_id)
            needs = job.get("needs", [])
            dependencies[job_id] = {needs} if isinstance(needs, str) else {str(item) for item in sequence(needs)}
            assert dependencies[job_id] <= jobs.keys(), (filename, job_id, dependencies[job_id])
            reference = str(job.get("uses", ""))
            if reference.startswith("./"):
                target = Path(reference).name
                assert (ROOT / reference).is_file(), reference
                assert "workflow_call" in mapping(documents[target]["on"]), reference
                calls[filename].add(target)
            for raw_step in sequence(job.get("steps", [])):
                action = str(mapping(raw_step).get("uses", ""))
                if action.startswith("./"):
                    assert (ROOT / action / "action.yml").is_file(), action
        assert set(TopologicalSorter(dependencies).static_order()) == jobs.keys()
    assert set(TopologicalSorter(calls).static_order()) == documents.keys()


def test_release_requires_all_verification_and_matching_artifacts() -> None:
    """
    Keep tag-only publishing behind every verification workflow and its exact built distributions.

    Returns:
        None: Release gates cannot be bypassed and the builder's artifact matches the publisher's download.
    """
    documents = workflows()
    release = documents["publish-pypi.yml"]
    assert release["on"] == {"push": {"tags": ["v[0-9]*"]}}
    jobs = {name: mapping(job) for name, job in mapping(release["jobs"]).items()}
    publish = jobs["publish"]
    assert set(sequence(publish["needs"])) == jobs.keys() - {"publish"}
    assert "if" not in publish  # GitHub's default success condition must reject failed or skipped gates.
    assert publish["environment"] == "pypi"
    targets = {str(job["uses"]) for name, job in jobs.items() if name != "publish"}
    assert targets == {
        "./.github/workflows/checks.yml",
        "./.github/workflows/chart-validation.yml",
        "./.github/workflows/package.yml",
        "./.github/workflows/benchmark-smoke.yml",
    }
    build = mapping(mapping(documents["package.yml"]["jobs"])["build"])
    build_steps = [mapping(step) for step in sequence(build["steps"])]
    publish_steps = [mapping(step) for step in sequence(publish["steps"])]
    upload = next(step for step in build_steps if str(step.get("uses", "")).startswith("actions/upload-artifact@"))
    download = next(step for step in publish_steps if str(step.get("uses", "")).startswith("actions/download-artifact@"))
    assert mapping(upload["with"])["name"] == mapping(download["with"])["name"]
    assert "package-version.outputs.version" in str(mapping(upload["with"])["name"])
    for steps in (build_steps, publish_steps):
        version = next(step for step in steps if step.get("id") == "package-version")
        assert "--tag" in str(version["run"])
    catalog = next(step for step in build_steps if "hypothesis-helm-catalog --check" in str(step.get("run", "")))
    assert catalog["if"] == "startsWith(github.ref, 'refs/tags/')"
    assert documents["benchmark-refresh.yml"]["on"] == {"workflow_dispatch": None}


def test_chart_workflow_restores_shard_caches_and_comparison_history() -> None:
    """
    Keep incremental CI, fresh security validation and tag release coverage wired together.

    Returns:
        None: Independent caches persist complete evidence and tags force new property tests.
    """
    job = mapping(mapping(workflows()["chart-validation.yml"]["jobs"])["sharded-chart"])
    steps = [mapping(step) for step in sequence(job["steps"])]
    checkout = next(step for step in steps if str(step.get("uses", "")).startswith("actions/checkout@"))
    assert mapping(checkout["with"])["fetch-depth"] == 0
    restore = next(step for step in steps if step.get("id") == "outcomes")
    settings = mapping(restore["with"])
    for coordinate in ("matrix.kubernetes", "matrix.shard", "runner.os", "runner.arch"):
        assert coordinate in str(settings["key"])
        assert coordinate in str(settings["restore-keys"])
    test = next(step for step in steps if step.get("id") == "hypothesis")
    options = mapping(test["with"])
    assert options["incremental"] == options["kubesec"] == "true"
    assert options["cache-dir"] == settings["path"]
    assert "refs/tags/" in str(options["rerun"]) and "'all'" in str(options["rerun"])
    save = next(step for step in steps if str(step.get("uses", "")).startswith("actions/cache/save@"))
    assert "always()" in str(save["if"])
    assert mapping(save["with"])["path"] == settings["path"]
