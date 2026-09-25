"""
Verify reference pipelines restore isolated property and manifest caches before testing.
"""

from ruamel.yaml import YAML

from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.tests import PROJECT_ROOT


def test_gitlab_preserves_outcomes_with_full_history() -> None:
    """
    Keep the fourth GitLab cache isolated by chart job, API version and shard.

    Returns:
        None: History is complete and outcome data is saved even when a test fails.
    """
    root = PROJECT_ROOT
    document = mapping(YAML(typ="safe").load((root / "ci/gitlab.yml").read_text()))
    variables = mapping(document["variables"])
    assert variables["GIT_DEPTH"] == "0"
    assert variables["HH_INCREMENTAL"] == variables["HH_CACHE"] == "true"
    job = mapping(document["helm-properties"])
    caches = [mapping(cache) for cache in sequence(job["cache"])]
    assert len(caches) == 4
    outcomes = next(cache for cache in caches if "outcomes" in str(cache["key"]))
    for coordinate in ("CI_JOB_NAME_SLUG", "K8S_VERSION", "SHARD_INDEX", "SHARD_TOTAL"):
        assert coordinate in str(outcomes["key"])
    assert outcomes["policy"] == "pull-push" and outcomes["when"] == "always"
    assert outcomes["paths"] == ["${HH_CACHE_DIR}/"]


def test_circleci_outcome_cache_is_saved_before_failure_is_restored() -> None:
    """
    Isolate immutable CircleCI caches and preserve them after property or security failures.

    Returns:
        None: Cache saves occur between deferred testing and the final failure step.
    """
    root = PROJECT_ROOT
    document = mapping(YAML(typ="safe").load((root / "ci/circleci.yml").read_text()))
    job = mapping(mapping(document["jobs"])["test-chart"])
    parameters = mapping(job["parameters"])
    assert mapping(parameters["incremental"])["default"] is True
    assert mapping(parameters["cache"])["default"] is True
    steps = sequence(job["steps"])
    restore_index, save_index = -1, -1
    for index, raw in enumerate(steps):
        if not isinstance(raw, dict) or "when" not in raw:
            continue
        condition = mapping(raw["when"])
        if condition["condition"] != "<< parameters.cache >>":
            continue
        for child in sequence(condition["steps"]):
            child = mapping(child)
            if "restore_cache" in child:
                restore_index = index
                keys = sequence(mapping(child["restore_cache"])["keys"])
                assert len(keys) == 1
                prefix = str(keys[0])
                for coordinate in ("report-group", "schema-version", "CIRCLE_NODE_INDEX", "parallelism"):
                    assert coordinate in prefix
            else:
                save_index = index
                saved = mapping(child["save_cache"])
                assert str(saved["key"]).startswith(prefix)
                assert "CIRCLE_WORKFLOW_ID" in str(saved["key"]) and "CIRCLE_BUILD_NUM" in str(saved["key"])
                assert saved["paths"] == ["<< parameters.cache-dir >>"]
    test_index = next(index for index, step in enumerate(steps) if isinstance(step, dict) and "test" in step)
    assert mapping(mapping(steps[test_index])["test"])["defer-failure"] is True
    final_index = next(index for index, step in enumerate(steps) if "Preserve the test and validator exit status" in str(step))
    assert 0 < restore_index < test_index < save_index < final_index
    assert any("git fetch --unshallow origin" in str(step) for step in steps)


def test_github_reference_uses_remote_action_and_incremental_cache() -> None:
    """
    Keep the copyable workflow independent of local action sources and complete on tags.

    Returns:
        None: The reference restores caches, validates security and aggregates failed shards.
    """
    root = PROJECT_ROOT
    document = mapping(YAML(typ="safe").load((root / "ci/github.yml").read_text()))
    jobs = mapping(document["jobs"])
    steps = [mapping(step) for step in sequence(mapping(jobs["chart"])["steps"])]
    checkout = next(step for step in steps if str(step.get("uses", "")).startswith("actions/checkout@"))
    assert mapping(checkout["with"])["fetch-depth"] == 0
    action = next(step for step in steps if step.get("uses") == "astrivant/hypothesis-helm@main")
    settings = mapping(action["with"])
    assert settings["incremental"] == settings["kubesec"] == "true"
    assert "refs/tags/" in str(settings["rerun"])
    assert "always()" in str(mapping(jobs["report"])["if"])
    restore = next(step for step in steps if step.get("id") == "outcomes")
    assert mapping(restore["with"])["path"] == settings["cache-dir"]
