# Local Helm chart tests

<!-- toc:start -->
**Table of contents**

- [Overview](#overview)
- [Scan summary](#scan-summary)
- [Status counts](#status-counts)
- [Settings](#settings)
- [Errors](#errors)
- [Charts](#charts)
  - [airflow](#airflow)
  - [apache](#apache)
  - [apisix](#apisix)
<!-- toc:end -->

## Overview

![Chart severity and scan-time matrices](<bitnami-compiler-review-overview.png>)

Each cell is one chart; both grids follow chart-section order. Click a cell in the PDF for details. Colors show the highest observed finding
kind, not a security or business-impact score. Hatching marks unfinished or unavailable testing, even when a finding was recorded. No
findings means none in the completed sample, not exhaustive coverage. Testing time excludes dependency preparation.

## Scan summary

Git comparison: HEAD^ (ba7b5abc108e60d97302618dbcf21b2dc7d0b924); 0 cached chart successes reused.

Directory: /Users/emmadoyle/projects/personal/hypothesis-helm/.cache/bitnami-compiler-review-1789844100/charts
Started (Unix epoch): 1789844180
Elapsed (wall clock): 778.49 seconds
Chart testing: 777.82 seconds
Dependency preparation: 0.00 seconds (excluded from testing budgets)
Charts discovered: 3
Scan status: completed
Discovery complete: True
Unstarted charts: 0

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

1 time-limit; 2 failed.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: HH2006

## Errors

31 distinct diagnostics across 56 occurrences; 25 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### airflow

Overview cell: 01

Status: time-limit | Attempts: 341

Audit findings: 1282. Full paths and template references are retained in the JSON report.

- `HH2001` at `$[*][*]`: Undocumented values path
- `HH2004` at `$[*][*]`: No supplied default for a values path
- `HH2001` at `$[*][*][*]`: Undocumented values path
- `HH2004` at `$[*][*][*]`: No supplied default for a values path
- `HH2001` at `$[*][*][*][*]`: Undocumented values path
- `HH2004` at `$[*][*][*][*]`: No supplied default for a values path
- 1276 additional audit findings in JSON.

[Chart artifacts](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0000>)

### apache

Overview cell: 02

Status: failed | Attempts: 3916

Audit findings: 270. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.affinity`: Undocumented values path
- `HH2001` at `$.args`: Undocumented values path
- `HH2001` at `$.automountServiceAccountToken`: Undocumented values path
- `HH2001` at `$.autoscaling.enabled`: Undocumented values path
- `HH2001` at `$.autoscaling.maxReplicas`: Undocumented values path
- `HH2001` at `$.autoscaling.minReplicas`: Undocumented values path
- 264 additional audit findings in JSON.

#### E001 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on apache/templates/deployment.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.commonAnnotations | Status: failed

Changed overrides (used together):
- `$.commonAnnotations[""] = []`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/672041fcfe26907bc14c>)

#### E002 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on apache/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/90454abd7e30d38b69ee>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/fbfea8b96e1bf6abb6fc>)

#### E003 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on apache/templates/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/840a8a2bc50327388c2a>)

Phase: $.serviceAccount | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/7a010717afb4691aaeb8>)

#### E004 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on apache/templates/svc.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal array
into Go struct field .metadata.annotations. of type string
```

Phase: $.service.annotations | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = []`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/98a2bca1991be60ae38a>)

Phase: $.service | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = []`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/da628aa79e50e022e4ff>)

#### E005 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
execution error at (apache/templates/NOTES.txt:45:4): VALUES VALIDATION: apache: htdocs-git-repository You did not specify a git repository
to clone. Please set cloneHtdocsFromGit.repository apache: htdocs-git-branch You did not specify a branch to checkout in the git repository.
Please set cloneHtdocsFromGit.branch
```

Phase: $.cloneHtdocsFromGit.enabled | Status: failed

Changed overrides (used together):
- `$.cloneHtdocsFromGit.enabled = true (was false)`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/2442d14cba32517cdd3b>)

#### E006 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... kely to cause degraded security and performance, broken chart features, and missing
environment variables. Unrecognized images: - 00/bitnami/apache-exporter:1.0.10-debian-12-r55 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.metrics | Status: failed

Changed overrides (used together):
- `$.metrics.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/17d970eb96f24f23c2d5>)

Phase: $.metrics.image.registry | Status: failed

Changed overrides (used together):
- `$.metrics.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/c96ecbfa425836596f7f>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E007 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ormance, broken chart features, and missing environment variables. Unrecognized images: -
00/bitnami/apache:2.4.65-debian-12-r2 - 00/bitnami/apache-exporter:1.0.10-debian-12-r55 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/fa90b40f46c6c70d8821>)

Phase: $.global | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/a8d13bfa12806deaf76c>)

#### E008 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/apache:2.4.65-debian-12-r2 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.registry | Status: failed

Changed overrides (used together):
- `$.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/488624c1bd95bbae6f8b>)

#### E009 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ntainers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - docker.io/00:1.0.10-debian-12-r55 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.metrics.image.repository | Status: failed

Changed overrides (used together):
- `$.metrics.image.repository = "00" (was "bitnami/apache-exporter")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/4c4a07eb1c5214b3a409>)

#### E010 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:2.4.65-debian-12-r2 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/apache")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/3f7165f1837241716c3c>)

#### E011 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 173: found unexpected end of
stream
```

Phase: $.readinessProbe.path | Status: failed

Changed overrides (used together):
- `$.readinessProbe.path = "'" (was "/")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/6e63684264db9d622def>)

Phase: $.livenessProbe | Status: failed

Changed overrides (used together):
- `$.livenessProbe.port = "'" (was "http")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/4205bc059f894025d23f>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E012 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 174: found unexpected end of
stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/57504c968732d9714f10>)

#### E013 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 175: found unexpected end of
stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/e4b1fa53526f192b7184>)

Phase: $.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/95d9e80fea15aed87f2a>)

#### E014 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 178: found unexpected end of
stream
```

Phase: $.vhostsConfigMap | Status: failed

Changed overrides (used together):
- `$.vhostsConfigMap = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/be14993fbd1c228c36ce>)

#### E015 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 179: found unexpected end of
stream
```

Phase: $.htdocsConfigMap | Status: failed

Changed overrides (used together):
- `$.htdocsConfigMap = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/a84b1abe3a11000d364a>)

Phase: $.htdocsPVC | Status: failed

Changed overrides (used together):
- `$.htdocsPVC = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/8fd174ce0cd7f4de3220>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E016 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null, []]]`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/097f6358a00dddbcdd83>)

4 additional occurrences are retained in the JSON report and chart artifacts.

#### E017 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/8e79b7dd85a286cfaddb>)

Phase: $.image.tag | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/7e365cc9986c8fb6c4ad>)

#### E018 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 64: could not find expected
':'
```

Phase: $.image.digest | Status: failed

Changed overrides (used together):
- `$.image.digest = "\n0" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/10293d402dd6d1dd34f5>)

#### E019 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 6: could not find expected
':'
```

Phase: $.nameOverride | Status: failed

Changed overrides (used together):
- `$.nameOverride = "\n0" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/0ce120cfa523ba37df61>)

#### E020 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/pdb.yaml: error converting YAML to JSON: yaml: line 13: block sequence entries are not
allowed in this context
```

Phase: $.pdb | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "-" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/fcc268f7f5d701449828>)

#### E021 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/pdb.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of stream
```

Phase: $.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/d6baed3b8998a068f471>)

Phase: $.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.pdb.minAvailable = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/07d4854a45a9e7c1eb04>)

#### E022 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 15: did not find expected ',' or
']'
```

Phase: $.service.loadBalancerSourceRanges[*] | Status: failed

Changed overrides (used together):
- `$.service.loadBalancerSourceRanges = [{}]`
Absent from overrides: $.service.loadBalancerSourceRanges["*"]. Defaults may still apply.

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/964773c98a041f080dd4>)

Phase: $.service.loadBalancerSourceRanges | Status: failed

Changed overrides (used together):
- `$.service.loadBalancerSourceRanges = [{}]`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/60903c8f6383b493cf31>)

#### E023 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/6e931799d09f8182f34b>)

#### E024 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 29: found unexpected end of stream
```

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/12b3c4a215648c1d6dd7>)

#### E025 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 30: found unexpected end of stream
```

Phase: $.service.nodePorts.http | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/c91d7fbded4704da55d3>)

Phase: $.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/afbac7d295ec4c0a2908>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E028 (HH1105)

**Missing resource name** (manifest / violation). Provide a name in each resource branch; ignore this check if your workflow intentionally
uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[2].metadata.name: "hypothesis-apache" -> 0`
- `$[4].spec.template.spec.serviceAccountName: "hypothesis-apache" -> 0`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/815bf9b751b356e044f0>)

Phase: $.fullnameOverride | Status: failed

Changed overrides (used together):
- `$.fullnameOverride = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[0].metadata.name: "hypothesis-apache" -> 0`
- `$[1].metadata.name: "hypothesis-apache" -> 0`
- `$[2].metadata.name: "hypothesis-apache" -> 0`
- `$[3].metadata.name: "hypothesis-apache" -> 0`
- `$[4].metadata.name: "hypothesis-apache" -> 0`
- `$[4].spec.template.spec.serviceAccountName: "hypothesis-apache" -> 0`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/e2f7761f901d86846684>)

#### E029 (HH3001)

**Template accesses a missing object** (template / violation). Guard or default the parent object, or require it in the values schema.

```text
[HH3001] Error: apache/templates/ingress.yaml:34:15 executing "apache/templates/ingress.yaml" at <.name>: nil pointer evaluating interface
{}.name
```

Phase: $.ingress | Status: failed

Changed overrides (used together):
- `$.ingress.enabled = true (was false)`
- `$.ingress.extraHosts = [null]`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/94ed38bb417a953196c3>)

#### E030 (HH3002)

**Incompatible value type in template** (template / violation). Align the template operation with the accepted input types, or narrow the
schema.

```text
[HH3002] Error: apache/templates/networkpolicy.yaml:11:16 executing "apache/templates/networkpolicy.yaml" at <include
"common.names.namespace" .>: error calling include: apache/charts/common/templates/_names.tpl:64:65 executing "common.names.namespace" at
<63>: wrong type for value; expected string; got []interface {}
```

Phase: $.namespaceOverride | Status: failed

Changed overrides (used together):
- `$.namespaceOverride = [null]`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/835d62e0a3e46b72c904>)

#### E031 (HH3003)

**Undefined named template** (template / violation). Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: apache/templates/svc.yaml:9:11 executing "apache/templates/svc.yaml" at <include "common.names.fullname" .>: error calling
include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/e2cac8a5225634937910>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001/paths/2ff2aa2642f40d7be0f3>)

[Chart artifacts](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0001>)

### apisix

Overview cell: 03

Status: failed | Attempts: 261

Audit findings: 410. Full paths and template references are retained in the JSON report.

- `HH2001` at `$[*][*]`: Undocumented values path
- `HH2004` at `$[*][*]`: No supplied default for a values path
- `HH2001` at `$[*][*][*]`: Undocumented values path
- `HH2004` at `$[*][*][*]`: No supplied default for a values path
- `HH2001` at `$[*][*][*][*]`: Undocumented values path
- `HH2004` at `$[*][*][*][*]`: No supplied default for a values path
- 404 additional audit findings in JSON.

#### E026 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apisix/charts/etcd/templates/pdb.yaml: error converting YAML to JSON: yaml: line 15: block sequence
entries are not allowed in this context
```

Phase: $.etcd.pdb | Status: failed

Changed overrides (used together):
- `$.etcd.pdb.maxUnavailable = "-"`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0002/paths/aaadbc44a6ff4d313d85>)

#### E027 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apisix/templates/control-plane/dep-ds.yaml: error converting YAML to JSON: yaml: line 335: found
unexpected end of stream
```

Phase: $.controlPlane.extraConfigExistingConfigMap | Status: failed

Changed overrides (used together):
- `$.controlPlane.extraConfigExistingConfigMap = "'" (was "")`

[Full input and diagnostic](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0002/paths/98c9de7170b4f8fa32cd>)

[Chart artifacts](<../../.cache/bitnami-compiler-review-1789844100/artifacts/charts_1789844180/0002>)
