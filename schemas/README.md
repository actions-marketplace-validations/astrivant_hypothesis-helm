# Kubernetes schema cache

<!-- toc:start -->
**Table of contents**

- [Prepare schemas](#prepare-schemas)
- [Rebuild generation constraints](#rebuild-generation-constraints)
- [Cache in CI](#cache-in-ci)
<!-- toc:end -->

This directory holds rebuildable Kubernetes schemas, source checkouts and catalog data.
Everything except this README is ignored by Git. Each schema snapshot is identified by its Git tree hash and Kubernetes version.

## Prepare schemas

```sh
helm hypothesis schemas --schema-version 1.35.0
helm hypothesis test ./chart --validate-schemas --schema-version 1.35.0 --schema-offline
```

The first command uses a sparse checkout. The second validates rendered resources in Python using the cached strict schemas.
No separate API validator binary is installed or invoked. Unknown custom resources still require an explicit
[resource schema](../docs/input-domains/README.md#custom-resources).

Use `--schema-cache-dir /another/directory` to choose a different cache. Offline preparation requires a previously populated cache.
The optional Kubesec wrapper uses the same schema snapshot for its security checks.

## Rebuild generation constraints

```sh
bash scripts/setup-dev.sh --schemas
```

With development tools already installed:

```sh
hypothesis-helm-catalog --cache-dir schemas
```

This fetches the pinned Kubernetes source, extracts supported constraints, checks generated boundary cases against the actual Go validators,
and writes `schemas/catalogs/1.35.0/input-domains.json`. Go 1.25+ is needed for this rebuild, not for ordinary Python validation.
Use `--offline` after both source and Go dependency caches have been populated.
See [catalog rebuilding](../docs/input-domains/README.md#rebuilding-the-catalog-before-release) for release publication and source limitations.

## Cache in CI

Cache the entire `schemas/` directory with the selected Kubernetes version in the cache key.
The GitHub, GitLab and CircleCI examples do this by default. Their normal preparation downloads schema files only;
rebuilding the source-derived catalog is a separate development/release operation.
Parallel local users serialize checkout updates with a file lock and read immutable snapshots. CI jobs restore their own cache copies.
For reproducible runs, select an exact version and use `--schema-offline` after preparation.
