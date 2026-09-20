"""
Keep embedded CLI tests independent of their parent CI runner's shard identity.
"""

from collections.abc import Iterator

import pytest

from hypothesis_helm.environment import refresh_env


@pytest.fixture(autouse=True)
def isolated_ci_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """
    Clear external node coordinates; CI detection tests explicitly supply their own.

    Args:
        monkeypatch (pytest.MonkeyPatch): Fixture restoring caller environment variables.

    Yields:
        None: Tests cannot inherit the pipeline's partition or a preceding test's environment snapshot.
    """
    for key in (
        "CIRCLE_NODE_INDEX",
        "CIRCLE_NODE_TOTAL",
        "CI_NODE_INDEX",
        "CI_NODE_TOTAL",
        "HYPOTHESIS_HELM_JOB_INDEX",
        "HYPOTHESIS_HELM_JOB_TOTAL",
        "HH_CHART",
        "HH_SHARD",
        "HH_ARTIFACT_DIR",
        "HH_MATCH",
        "HH_VALIDATE_SCHEMAS",
        "HH_KUBESEC",
        "HH_KUBESEC_JOBS",
        "HH_KUBESEC_SCORE_MINIMUM",
        "HH_KUBESEC_BINARY",
        "GITHUB_STEP_SUMMARY",
        "HH_SCHEMA_VERSION",
        "HH_SCHEMA_CACHE_DIR",
        "HH_SCHEMA_OFFLINE",
        "HYPOTHESIS_HELM_CONFORMITY",
        "HH_CACHE",
        "HH_CACHE_DIR",
        "HH_RERUN",
        "HH_INCREMENTAL",
        "HH_BASE_REF",
        "CI",
        "GITHUB_ACTIONS",
        "GITHUB_REF",
        "GITHUB_REF_TYPE",
        "CI_COMMIT_TAG",
        "CIRCLE_TAG",
        "GITLAB_CI",
        "CIRCLECI",
    ):
        monkeypatch.delenv(key, raising=False)
    refresh_env()
    try:
        yield
    finally:
        monkeypatch.undo()
        refresh_env()
