# hypothesis-helm-benchmarking

<!-- toc:start -->
**Table of contents**

- [Install](#install)
- [Develop and publish](#develop-and-publish)
<!-- toc:end -->

An optional, separately published companion to `hypothesis-helm`. It contains the shared benchmark chart, studies,
plotting tools and repository refresh commands. The core linter does not import this package.

## Install

```sh
pip install hypothesis-helm-benchmarking
# Or install the core package with its optional companion:
pip install 'hypothesis-helm[benchmarking]'
```

`hypothesis-helm-benchmark --help` lists individual studies. `hypothesis-helm-refresh` runs the repository refresh from a checkout.
The `symbolic` extra adds PySR. Helm 4 and GNU Parallel remain external executables.

## Develop and publish

From the repository root, `poetry install --extras benchmarking` uses this directory as an editable dependency.
The built core wheel references the published package name, without a local filesystem dependency.

Build this distribution independently:

```sh
poetry -C pkg/hypothesis_helm_benchmarking build
```

Its version and release lifecycle are independent of the core package. Set its version before publishing;
the core PyPI workflow publishes only the core distribution.
