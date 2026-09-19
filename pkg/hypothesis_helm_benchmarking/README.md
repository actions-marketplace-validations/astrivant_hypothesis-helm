# hypothesis-helm-benchmarking

<!-- toc:start -->
**Table of contents**

- [Install](#install)
- [Develop and publish](#develop-and-publish)
- [Plot notation](#plot-notation)
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
Its `pyproject.toml` uses standard project metadata and the setuptools backend to map this flat directory to
the `hypothesis_helm_benchmarking` import package. Poetry still manages the repository environment and can invoke the build.

## Plot notation

Use Matplotlib mathtext alongside plain-language labels, for example `r"Interaction strength, $p$ (--permutations)"`.
Mathtext renders equations in PNG and SVG files without an external LaTeX installation.

Keep interaction strength ($p$) distinct from the number of test cases ($N$) and workers ($w$).
For repeated measurements, $\bar{x}$ is the mean and $s$ is the sample standard deviation;
bands at $\bar{x}\pm s$ and $\bar{x}\pm2s$ describe variation between runs, not confidence intervals.
Give each plot a short question beneath its title so readers can interpret the notation in context.
