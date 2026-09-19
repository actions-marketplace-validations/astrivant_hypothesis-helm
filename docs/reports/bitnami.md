# Local Helm chart tests

<!-- toc:start -->
<details>
<summary>Table of contents</summary>

- [Overview](#overview)
- [Scan summary](#scan-summary)
- [Status counts](#status-counts)
- [Settings](#settings)
- [Errors](#errors)
- [Charts](#charts)
  - [bitnami/airflow](#bitnamiairflow)
  - [bitnami/apache](#bitnamiapache)
  - [bitnami/apisix](#bitnamiapisix)
  - [bitnami/appsmith](#bitnamiappsmith)
  - [bitnami/argo-cd](#bitnamiargo-cd)
  - [bitnami/argo-workflows](#bitnamiargo-workflows)
  - [bitnami/aspnet-core](#bitnamiaspnet-core)
  - [bitnami/cadvisor](#bitnamicadvisor)
  - [bitnami/cassandra](#bitnamicassandra)
  - [bitnami/cert-manager](#bitnamicert-manager)
  - [bitnami/chainloop](#bitnamichainloop)
  - [bitnami/cilium](#bitnamicilium)
  - [bitnami/clickhouse](#bitnamiclickhouse)
  - [bitnami/clickhouse-operator](#bitnamiclickhouse-operator)
  - [bitnami/cloudnative-pg](#bitnamicloudnative-pg)
  - [bitnami/common](#bitnamicommon)
  - [bitnami/concourse](#bitnamiconcourse)
  - [bitnami/consul](#bitnamiconsul)
  - [bitnami/contour](#bitnamicontour)
  - [bitnami/deepspeed](#bitnamideepspeed)
  - [bitnami/discourse](#bitnamidiscourse)
  - [bitnami/dremio](#bitnamidremio)
  - [bitnami/drupal](#bitnamidrupal)
  - [bitnami/ejbca](#bitnamiejbca)
  - [bitnami/elasticsearch](#bitnamielasticsearch)
  - [bitnami/envoy-gateway](#bitnamienvoy-gateway)
  - [bitnami/etcd](#bitnamietcd)
  - [bitnami/external-dns](#bitnamiexternal-dns)
  - [bitnami/flink](#bitnamiflink)
  - [bitnami/fluent-bit](#bitnamifluent-bit)
  - [bitnami/fluentd](#bitnamifluentd)
  - [bitnami/flux](#bitnamiflux)
  - [bitnami/ghost](#bitnamighost)
  - [bitnami/gitea](#bitnamigitea)
  - [bitnami/gitlab-runner](#bitnamigitlab-runner)
  - [bitnami/grafana](#bitnamigrafana)
  - [bitnami/grafana-alloy](#bitnamigrafana-alloy)
  - [bitnami/grafana-k6-operator](#bitnamigrafana-k6-operator)
  - [bitnami/grafana-loki](#bitnamigrafana-loki)
  - [bitnami/grafana-mimir](#bitnamigrafana-mimir)
  - [bitnami/grafana-operator](#bitnamigrafana-operator)
  - [bitnami/grafana-tempo](#bitnamigrafana-tempo)
  - [bitnami/haproxy](#bitnamihaproxy)
  - [bitnami/harbor](#bitnamiharbor)
  - [bitnami/influxdb](#bitnamiinfluxdb)
  - [bitnami/jaeger](#bitnamijaeger)
  - [bitnami/janusgraph](#bitnamijanusgraph)
  - [bitnami/jenkins](#bitnamijenkins)
  - [bitnami/jupyterhub](#bitnamijupyterhub)
  - [bitnami/kafka](#bitnamikafka)
  - [bitnami/keycloak](#bitnamikeycloak)
  - [bitnami/keydb](#bitnamikeydb)
  - [bitnami/kibana](#bitnamikibana)
  - [bitnami/kong](#bitnamikong)
  - [bitnami/kube-arangodb](#bitnamikube-arangodb)
  - [bitnami/kube-prometheus](#bitnamikube-prometheus)
  - [bitnami/kube-prometheus/charts/kube-prometheus-crds](#bitnamikube-prometheuschartskube-prometheus-crds)
  - [bitnami/kube-state-metrics](#bitnamikube-state-metrics)
  - [bitnami/kuberay](#bitnamikuberay)
  - [bitnami/kubernetes-event-exporter](#bitnamikubernetes-event-exporter)
  - [bitnami/logstash](#bitnamilogstash)
  - [bitnami/mariadb](#bitnamimariadb)
  - [bitnami/mariadb-galera](#bitnamimariadb-galera)
  - [bitnami/mastodon](#bitnamimastodon)
  - [bitnami/matomo](#bitnamimatomo)
  - [bitnami/memcached](#bitnamimemcached)
  - [bitnami/metallb](#bitnamimetallb)
  - [bitnami/metrics-server](#bitnamimetrics-server)
  - [bitnami/milvus](#bitnamimilvus)
  - [bitnami/mlflow](#bitnamimlflow)
  - [bitnami/mongodb](#bitnamimongodb)
  - [bitnami/mongodb-sharded](#bitnamimongodb-sharded)
  - [bitnami/moodle](#bitnamimoodle)
  - [bitnami/multus-cni](#bitnamimultus-cni)
  - [bitnami/mysql](#bitnamimysql)
  - [bitnami/nats](#bitnaminats)
  - [bitnami/neo4j](#bitnamineo4j)
  - [bitnami/nessie](#bitnaminessie)
  - [bitnami/nginx](#bitnaminginx)
  - [bitnami/node-exporter](#bitnaminode-exporter)
  - [bitnami/oauth2-proxy](#bitnamioauth2-proxy)
  - [bitnami/odoo](#bitnamiodoo)
  - [bitnami/opensearch](#bitnamiopensearch)
  - [bitnami/parse](#bitnamiparse)
  - [bitnami/phpmyadmin](#bitnamiphpmyadmin)
  - [bitnami/pinniped](#bitnamipinniped)
  - [bitnami/postgresql](#bitnamipostgresql)
  - [bitnami/postgresql-ha](#bitnamipostgresql-ha)
  - [bitnami/prometheus](#bitnamiprometheus)
  - [bitnami/pytorch](#bitnamipytorch)
  - [bitnami/rabbitmq](#bitnamirabbitmq)
  - [bitnami/rabbitmq-cluster-operator](#bitnamirabbitmq-cluster-operator)
  - [bitnami/redis](#bitnamiredis)
  - [bitnami/redis-cluster](#bitnamiredis-cluster)
  - [bitnami/redmine](#bitnamiredmine)
  - [bitnami/schema-registry](#bitnamischema-registry)
  - [bitnami/scylladb](#bitnamiscylladb)
  - [bitnami/sealed-secrets](#bitnamisealed-secrets)
  - [bitnami/seaweedfs](#bitnamiseaweedfs)
  - [bitnami/solr](#bitnamisolr)
  - [bitnami/sonarqube](#bitnamisonarqube)
  - [bitnami/spark](#bitnamispark)
  - [bitnami/superset](#bitnamisuperset)
  - [bitnami/tensorflow-resnet](#bitnamitensorflow-resnet)
  - [bitnami/thanos](#bitnamithanos)
  - [bitnami/tomcat](#bitnamitomcat)
  - [bitnami/valkey](#bitnamivalkey)
  - [bitnami/valkey-cluster](#bitnamivalkey-cluster)
  - [bitnami/vault](#bitnamivault)
  - [bitnami/victoriametrics](#bitnamivictoriametrics)
  - [bitnami/whereabouts](#bitnamiwhereabouts)
  - [bitnami/wildfly](#bitnamiwildfly)
  - [bitnami/wordpress](#bitnamiwordpress)
  - [bitnami/zipkin](#bitnamizipkin)
  - [bitnami/zookeeper](#bitnamizookeeper)

</details>
<!-- toc:end -->

## Overview

![Chart severity and scan-time matrices](<bitnami-overview.png>)

Each cell is one chart; both grids follow chart-section order. Click a cell in the PDF for details. Colors show the highest observed finding
kind, not a security or business-impact score. Hatching marks unfinished or unavailable testing, even when a finding was recorded. No
findings means none in the completed sample, not exhaustive coverage. Testing time excludes dependency preparation.

## Scan summary

Git comparison unavailable; no charts skipped using previous test results.

Directory: /Users/emmadoyle/projects/personal/hypothesis-helm/third_party/bitnami-charts
Started (Unix epoch): 1789854946
Elapsed (wall clock): 658.39 seconds
Chart testing: 634.74 seconds
Dependency preparation: 22.46 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: interrupted
Discovery complete: True
Unstarted charts: 112

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

2 failed; 1 interrupted; 112 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: HH2006

## Errors

36 distinct diagnostics across 61 occurrences; 25 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### bitnami/airflow

Overview cell: 01

Status: failed | Attempts: 146

Audit findings: 1190. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.apiVersions`: Undocumented values path (warning)
- `HH2001` at `$.auth.existingSecret`: Undocumented values path (warning)
- `HH2001` at `$.auth.fernetKey`: Undocumented values path (warning)
- `HH2001` at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- `HH2001` at `$.auth.password`: Undocumented values path (warning)
- `HH2001` at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E013 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 22.0.4 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ...  with non-standard containers is likely to cause degraded security and performance,
broken chart features, and missing environment variables. Unrecognized images: - /)Xrjk;@X|:E If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.redis.metrics.containerPorts | Status: failed

Changed overrides (used together):
- `$.redis.metrics.resourcesPreset = "ks[Ma"`
- `$.redis.metrics.containerSecurityContext.privileged = [null, null, null]`
- `$.redis.metrics.startupProbe.failureThreshold = -3.642006609759936e+54`
- `$.redis.metrics.startupProbe.enabled = false`
- `$.redis.metrics.startupProbe.initialDelaySeconds = -2527976481271112.0`
- `$.redis.metrics.startupProbe.timeoutSeconds = 5343706709371922.0`
- 9 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0000/paths/f78bb11087b66fe7a49f>)

#### E014 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 22.0.4 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... rd containers is likely to cause degraded security and performance, broken chart
features, and missing environment variables. Unrecognized images: - QNx_[[/ XTAhaL\S>S(g}K:aaLcv If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.extraVolumeMounts = "["`
- `$.redis.sentinel.failoverTimeout = 6.204452962310167e+16`
- `$.redis.sentinel.enabled = false`
- `$.redis.sentinel.extraEnvVarsSecret = "ac"`
- `$.redis.sentinel.annotations = "apiVersion"`
- `$.redis.sentinel.externalAccess = {}`
- 17 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0000/paths/afbbf9ab6c6be5d414aa>)

#### E015 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 22.0.4 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/OX:1.75.0-debian-12-r1 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.redis.metrics.livenessProbe.periodSeconds | Status: failed

Changed overrides (used together):
- `$.redis.metrics.customStartupProbe["[Ma"].OaUaaaO = [true, null, {}]`
- `$.redis.metrics.customStartupProbe["[Ma"][""] = {}`
- `$.redis.metrics.customStartupProbe["[Ma"]["aaaaGaaaaaaaaa\n0"][""] = null`
- `$.redis.metrics.customStartupProbe["3j$0"] = [[null, 1e-06], [[1.6367801640519733e+83]]]`
- `$.redis.metrics.customStartupProbe.u_ = [[null], false, []]`
- `$.redis.metrics.customStartupProbe["\raK{aMmaW"] = []`
- 43 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0000/paths/ca2ac8630025cdc22374>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789854946/0000>)

### bitnami/apache

Overview cell: 02

Status: failed | Attempts: 3928

Audit findings: 245. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.affinity`: Undocumented values path (warning)
- `HH2001` at `$.args`: Undocumented values path (warning)
- `HH2001` at `$.automountServiceAccountToken`: Undocumented values path (warning)
- `HH2001` at `$.autoscaling.enabled`: Undocumented values path (warning)
- `HH2001` at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- `HH2001` at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 239 additional audit findings in JSON.

Configuration rejections: 0 excluded; 10 adjusted and tested; 10 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E001 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: YAML parse error on apache/templates/deployment.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.commonAnnotations | Status: failed

Changed overrides (used together):
- `$.commonAnnotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/672041fcfe26907bc14c>)

#### E002 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: YAML parse error on apache/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/90454abd7e30d38b69ee>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/fbfea8b96e1bf6abb6fc>)

#### E003 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: YAML parse error on apache/templates/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/840a8a2bc50327388c2a>)

Phase: $.serviceAccount | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/7a010717afb4691aaeb8>)

#### E004 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: YAML parse error on apache/templates/svc.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal array
into Go struct field .metadata.annotations. of type string
```

Phase: $.service.annotations | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/98a2bca1991be60ae38a>)

Phase: $.service | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/da628aa79e50e022e4ff>)

#### E005 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
execution error at (apache/templates/NOTES.txt:45:4): VALUES VALIDATION: apache: htdocs-git-repository You did not specify a git repository
to clone. Please set cloneHtdocsFromGit.repository apache: htdocs-git-branch You did not specify a branch to checkout in the git repository.
Please set cloneHtdocsFromGit.branch
```

Phase: $.cloneHtdocsFromGit.enabled | Status: failed

Changed overrides (used together):
- `$.cloneHtdocsFromGit.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/2442d14cba32517cdd3b>)

#### E006 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/17d970eb96f24f23c2d5>)

Phase: $.metrics.image.registry | Status: failed

Changed overrides (used together):
- `$.metrics.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/c96ecbfa425836596f7f>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E007 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/fa90b40f46c6c70d8821>)

Phase: $.global | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/a8d13bfa12806deaf76c>)

#### E008 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/488624c1bd95bbae6f8b>)

#### E009 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/4c4a07eb1c5214b3a409>)

#### E010 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/3f7165f1837241716c3c>)

#### E016 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 173: found unexpected end of
stream
```

Phase: $.readinessProbe.path | Status: failed

Changed overrides (used together):
- `$.readinessProbe.path = "'" (was "/")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/6e63684264db9d622def>)

Phase: $.livenessProbe | Status: failed

Changed overrides (used together):
- `$.livenessProbe.port = "'" (was "http")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/4205bc059f894025d23f>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E017 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 174: found unexpected end of
stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/57504c968732d9714f10>)

#### E018 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 175: found unexpected end of
stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/e4b1fa53526f192b7184>)

Phase: $.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/95d9e80fea15aed87f2a>)

#### E019 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 178: found unexpected end of
stream
```

Phase: $.vhostsConfigMap | Status: failed

Changed overrides (used together):
- `$.vhostsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/be14993fbd1c228c36ce>)

#### E020 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 179: found unexpected end of
stream
```

Phase: $.htdocsConfigMap | Status: failed

Changed overrides (used together):
- `$.htdocsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/a84b1abe3a11000d364a>)

Phase: $.htdocsPVC | Status: failed

Changed overrides (used together):
- `$.htdocsPVC = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/8fd174ce0cd7f4de3220>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E021 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/097f6358a00dddbcdd83>)

4 additional occurrences are retained in the JSON report and chart artifacts.

#### E022 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/8e79b7dd85a286cfaddb>)

Phase: $.image.tag | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/7e365cc9986c8fb6c4ad>)

#### E023 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 64: could not find expected
':'
```

Phase: $.image.digest | Status: failed

Changed overrides (used together):
- `$.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/10293d402dd6d1dd34f5>)

#### E024 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 6: could not find expected
':'
```

Phase: $.nameOverride | Status: failed

Changed overrides (used together):
- `$.nameOverride = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/0ce120cfa523ba37df61>)

#### E025 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/pdb.yaml: error converting YAML to JSON: yaml: line 13: block sequence entries are not
allowed in this context
```

Phase: $.pdb | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "-" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/fcc268f7f5d701449828>)

#### E026 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/pdb.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of stream
```

Phase: $.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/d6baed3b8998a068f471>)

Phase: $.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.pdb.minAvailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/07d4854a45a9e7c1eb04>)

#### E027 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 15: did not find expected ',' or
']'
```

Phase: $.service.loadBalancerSourceRanges[*] | Status: failed

Changed overrides (used together):
- `$.service.loadBalancerSourceRanges = [{}]`
Absent from overrides: $.service.loadBalancerSourceRanges["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/964773c98a041f080dd4>)

Phase: $.service.loadBalancerSourceRanges | Status: failed

Changed overrides (used together):
- `$.service.loadBalancerSourceRanges = [{}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/60903c8f6383b493cf31>)

#### E028 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/6e931799d09f8182f34b>)

#### E029 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 29: found unexpected end of stream
```

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/12b3c4a215648c1d6dd7>)

#### E030 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 30: found unexpected end of stream
```

Phase: $.service.nodePorts.http | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/c91d7fbded4704da55d3>)

Phase: $.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/afbac7d295ec4c0a2908>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E033 (HH1105)

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[2].metadata.name: "hypothesis-apache" -> 0`
- `$[4].spec.template.spec.serviceAccountName: "hypothesis-apache" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/815bf9b751b356e044f0>)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/e2f7761f901d86846684>)

#### E034 (HH3001)

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: apache/templates/ingress.yaml:34:15 executing "apache/templates/ingress.yaml" at <.name>: nil pointer evaluating interface
{}.name
```

Phase: $.ingress | Status: failed

Changed overrides (used together):
- `$.ingress.enabled = true (was false)`
- `$.ingress.extraHosts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/94ed38bb417a953196c3>)

#### E035 (HH3002)

**Incompatible value type in template** (template / violation). Severity: **error**. Align the template operation with the accepted input
types, or narrow the schema.

```text
[HH3002] Error: apache/templates/networkpolicy.yaml:11:16 executing "apache/templates/networkpolicy.yaml" at <include
"common.names.namespace" .>: error calling include: apache/charts/common/templates/_names.tpl:64:65 executing "common.names.namespace" at
<63>: wrong type for value; expected string; got []interface {}
```

Phase: $.namespaceOverride | Status: failed

Changed overrides (used together):
- `$.namespaceOverride = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/835d62e0a3e46b72c904>)

#### E036 (HH3003)

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: apache/templates/svc.yaml:9:11 executing "apache/templates/svc.yaml" at <include "common.names.fullname" .>: error calling
include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/e2cac8a5225634937910>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0001/paths/2ff2aa2642f40d7be0f3>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789854946/0001>)

### bitnami/apisix

Overview cell: 03

Status: interrupted | Attempts: 98

Audit findings: 344. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.apiVersions`: Undocumented values path (warning)
- `HH2002` at `$.controlPlane.args[*]`: Unspecified values type (warning)
- `HH2001` at `$.controlPlane.automountServiceAccountToken`: Undocumented values path (warning)
- `HH2003` at `$.controlPlane.autoscaling`: Missing values description (info)
- `HH2003` at `$.controlPlane.autoscaling.hpa`: Missing values description (info)
- `HH2003` at `$.controlPlane.autoscaling.vpa`: Missing values description (info)
- 338 additional audit findings in JSON.

#### E011 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: etcd 12.0.18 / templates/cronjob-snapshotter.yaml

```text
execution error at (etcd/templates/cronjob-snapshotter.yaml:132:29): ERROR: Preset key '%5a0aka9aaafo|n' invalid. Allowed values are
nano,micro,small,medium,large,xlarge,2xlarge
```

Phase: $.etcd.disasterRecovery.cronjob.containerSecurityContext | Status: interrupted

Changed overrides (used together):
- `$.etcd.disasterRecovery.enabled = true`
- `$.etcd.disasterRecovery.pvc.subPath = "9a"`
- `$.etcd.disasterRecovery.pvc.storageClassName = ""`
- `$.etcd.disasterRecovery.cronjob.tolerations = [{"]aaaaaaE": -6.296829526392782e+172, "4aaaaaz": "aaaaa", "": null}, false, {"aaa": {"aa\raa": {"g4aa": null, "/Qaaa": ... [value shortened]`
- `$.etcd.disasterRecovery.cronjob.podLabels.a["aaaaaapha_a.aaaaFaaabaa"][""].azUaaaaaaaa = -22529`
- `$.etcd.disasterRecovery.cronjob.podLabels.a["aaaaaapha_a.aaaaFaaabaa"][""]["av(o3Ia"] = false`
- 54 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0002/paths/7ace770b9f7e97b3eaab>)

#### E012 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: etcd 12.0.18 / templates/cronjob-snapshotter.yaml

```text
execution error at (etcd/templates/cronjob-snapshotter.yaml:132:29): ERROR: Preset key 'PLL' invalid. Allowed values are
nano,micro,small,medium,large,xlarge,2xlarge
```

Phase: $.etcd.disasterRecovery.cronjob.replicaCount | Status: interrupted

Changed overrides (used together):
- `$.etcd.disasterRecovery.enabled = true`
- `$.etcd.disasterRecovery.cronjob.podAnnotations["\"B*N^"] = [{"aSaaaa": "aaa"}]`
- `$.etcd.disasterRecovery.cronjob.podAnnotations["W3D;R{aQcD)Xrjk;@X|"] = false`
- `$.etcd.disasterRecovery.cronjob.podAnnotations[""] = {}`
- `$.etcd.disasterRecovery.cronjob.command = []`
- `$.etcd.disasterRecovery.cronjob.tolerations = [{"]aaaaaaE": -6.296829526392782e+172, "4aaaaaz": "aaaaa", "": null}, false, {"aaa": {"aa\raa": {"g4aa": null, "/Qaaa": ... [value shortened]`
- 37 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0002/paths/ec3a3876a481222d9bc3>)

#### E031 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apisix/charts/etcd/templates/pdb.yaml: error converting YAML to JSON: yaml: line 14: did not find
expected ',' or ']'
```

Phase: $.etcd.pdb | Status: interrupted

Changed overrides (used together):
- `$.etcd.pdb.minAvailable = ""`
- `$.etcd.pdb.maxUnavailable = "[Ma"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0002/paths/aaadbc44a6ff4d313d85>)

#### E032 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apisix/templates/control-plane/dep-ds.yaml: error converting YAML to JSON: yaml: line 336: found
unexpected end of stream
```

Phase: $.controlPlane.extraConfigExistingConfigMap | Status: interrupted

Changed overrides (used together):
- `$.controlPlane.extraConfigExistingConfigMap = "'\n"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789854946/0002/paths/98c9de7170b4f8fa32cd>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789854946/0002>)

### bitnami/appsmith

Overview cell: 04

Status: pending | Attempts: N/A

### bitnami/argo-cd

Overview cell: 05

Status: pending | Attempts: N/A

### bitnami/argo-workflows

Overview cell: 06

Status: pending | Attempts: N/A

### bitnami/aspnet-core

Overview cell: 07

Status: pending | Attempts: N/A

### bitnami/cadvisor

Overview cell: 08

Status: pending | Attempts: N/A

### bitnami/cassandra

Overview cell: 09

Status: pending | Attempts: N/A

### bitnami/cert-manager

Overview cell: 10

Status: pending | Attempts: N/A

### bitnami/chainloop

Overview cell: 11

Status: pending | Attempts: N/A

### bitnami/cilium

Overview cell: 12

Status: pending | Attempts: N/A

### bitnami/clickhouse

Overview cell: 13

Status: pending | Attempts: N/A

### bitnami/clickhouse-operator

Overview cell: 14

Status: pending | Attempts: N/A

### bitnami/cloudnative-pg

Overview cell: 15

Status: pending | Attempts: N/A

### bitnami/common

Overview cell: 16

Status: pending | Attempts: N/A

### bitnami/concourse

Overview cell: 17

Status: pending | Attempts: N/A

### bitnami/consul

Overview cell: 18

Status: pending | Attempts: N/A

### bitnami/contour

Overview cell: 19

Status: pending | Attempts: N/A

### bitnami/deepspeed

Overview cell: 20

Status: pending | Attempts: N/A

### bitnami/discourse

Overview cell: 21

Status: pending | Attempts: N/A

### bitnami/dremio

Overview cell: 22

Status: pending | Attempts: N/A

### bitnami/drupal

Overview cell: 23

Status: pending | Attempts: N/A

### bitnami/ejbca

Overview cell: 24

Status: pending | Attempts: N/A

### bitnami/elasticsearch

Overview cell: 25

Status: pending | Attempts: N/A

### bitnami/envoy-gateway

Overview cell: 26

Status: pending | Attempts: N/A

### bitnami/etcd

Overview cell: 27

Status: pending | Attempts: N/A

### bitnami/external-dns

Overview cell: 28

Status: pending | Attempts: N/A

### bitnami/flink

Overview cell: 29

Status: pending | Attempts: N/A

### bitnami/fluent-bit

Overview cell: 30

Status: pending | Attempts: N/A

### bitnami/fluentd

Overview cell: 31

Status: pending | Attempts: N/A

### bitnami/flux

Overview cell: 32

Status: pending | Attempts: N/A

### bitnami/ghost

Overview cell: 33

Status: pending | Attempts: N/A

### bitnami/gitea

Overview cell: 34

Status: pending | Attempts: N/A

### bitnami/gitlab-runner

Overview cell: 35

Status: pending | Attempts: N/A

### bitnami/grafana

Overview cell: 36

Status: pending | Attempts: N/A

### bitnami/grafana-alloy

Overview cell: 37

Status: pending | Attempts: N/A

### bitnami/grafana-k6-operator

Overview cell: 38

Status: pending | Attempts: N/A

### bitnami/grafana-loki

Overview cell: 39

Status: pending | Attempts: N/A

### bitnami/grafana-mimir

Overview cell: 40

Status: pending | Attempts: N/A

### bitnami/grafana-operator

Overview cell: 41

Status: pending | Attempts: N/A

### bitnami/grafana-tempo

Overview cell: 42

Status: pending | Attempts: N/A

### bitnami/haproxy

Overview cell: 43

Status: pending | Attempts: N/A

### bitnami/harbor

Overview cell: 44

Status: pending | Attempts: N/A

### bitnami/influxdb

Overview cell: 45

Status: pending | Attempts: N/A

### bitnami/jaeger

Overview cell: 46

Status: pending | Attempts: N/A

### bitnami/janusgraph

Overview cell: 47

Status: pending | Attempts: N/A

### bitnami/jenkins

Overview cell: 48

Status: pending | Attempts: N/A

### bitnami/jupyterhub

Overview cell: 49

Status: pending | Attempts: N/A

### bitnami/kafka

Overview cell: 50

Status: pending | Attempts: N/A

### bitnami/keycloak

Overview cell: 51

Status: pending | Attempts: N/A

### bitnami/keydb

Overview cell: 52

Status: pending | Attempts: N/A

### bitnami/kibana

Overview cell: 53

Status: pending | Attempts: N/A

### bitnami/kong

Overview cell: 54

Status: pending | Attempts: N/A

### bitnami/kube-arangodb

Overview cell: 55

Status: pending | Attempts: N/A

### bitnami/kube-prometheus

Overview cell: 56

Status: pending | Attempts: N/A

### bitnami/kube-prometheus/charts/kube-prometheus-crds

Overview cell: 57

Status: pending | Attempts: N/A

### bitnami/kube-state-metrics

Overview cell: 58

Status: pending | Attempts: N/A

### bitnami/kuberay

Overview cell: 59

Status: pending | Attempts: N/A

### bitnami/kubernetes-event-exporter

Overview cell: 60

Status: pending | Attempts: N/A

### bitnami/logstash

Overview cell: 61

Status: pending | Attempts: N/A

### bitnami/mariadb

Overview cell: 62

Status: pending | Attempts: N/A

### bitnami/mariadb-galera

Overview cell: 63

Status: pending | Attempts: N/A

### bitnami/mastodon

Overview cell: 64

Status: pending | Attempts: N/A

### bitnami/matomo

Overview cell: 65

Status: pending | Attempts: N/A

### bitnami/memcached

Overview cell: 66

Status: pending | Attempts: N/A

### bitnami/metallb

Overview cell: 67

Status: pending | Attempts: N/A

### bitnami/metrics-server

Overview cell: 68

Status: pending | Attempts: N/A

### bitnami/milvus

Overview cell: 69

Status: pending | Attempts: N/A

### bitnami/mlflow

Overview cell: 70

Status: pending | Attempts: N/A

### bitnami/mongodb

Overview cell: 71

Status: pending | Attempts: N/A

### bitnami/mongodb-sharded

Overview cell: 72

Status: pending | Attempts: N/A

### bitnami/moodle

Overview cell: 73

Status: pending | Attempts: N/A

### bitnami/multus-cni

Overview cell: 74

Status: pending | Attempts: N/A

### bitnami/mysql

Overview cell: 75

Status: pending | Attempts: N/A

### bitnami/nats

Overview cell: 76

Status: pending | Attempts: N/A

### bitnami/neo4j

Overview cell: 77

Status: pending | Attempts: N/A

### bitnami/nessie

Overview cell: 78

Status: pending | Attempts: N/A

### bitnami/nginx

Overview cell: 79

Status: pending | Attempts: N/A

### bitnami/node-exporter

Overview cell: 80

Status: pending | Attempts: N/A

### bitnami/oauth2-proxy

Overview cell: 81

Status: pending | Attempts: N/A

### bitnami/odoo

Overview cell: 82

Status: pending | Attempts: N/A

### bitnami/opensearch

Overview cell: 83

Status: pending | Attempts: N/A

### bitnami/parse

Overview cell: 84

Status: pending | Attempts: N/A

### bitnami/phpmyadmin

Overview cell: 85

Status: pending | Attempts: N/A

### bitnami/pinniped

Overview cell: 86

Status: pending | Attempts: N/A

### bitnami/postgresql

Overview cell: 87

Status: pending | Attempts: N/A

### bitnami/postgresql-ha

Overview cell: 88

Status: pending | Attempts: N/A

### bitnami/prometheus

Overview cell: 89

Status: pending | Attempts: N/A

### bitnami/pytorch

Overview cell: 90

Status: pending | Attempts: N/A

### bitnami/rabbitmq

Overview cell: 91

Status: pending | Attempts: N/A

### bitnami/rabbitmq-cluster-operator

Overview cell: 92

Status: pending | Attempts: N/A

### bitnami/redis

Overview cell: 93

Status: pending | Attempts: N/A

### bitnami/redis-cluster

Overview cell: 94

Status: pending | Attempts: N/A

### bitnami/redmine

Overview cell: 95

Status: pending | Attempts: N/A

### bitnami/schema-registry

Overview cell: 96

Status: pending | Attempts: N/A

### bitnami/scylladb

Overview cell: 97

Status: pending | Attempts: N/A

### bitnami/sealed-secrets

Overview cell: 98

Status: pending | Attempts: N/A

### bitnami/seaweedfs

Overview cell: 99

Status: pending | Attempts: N/A

### bitnami/solr

Overview cell: 100

Status: pending | Attempts: N/A

### bitnami/sonarqube

Overview cell: 101

Status: pending | Attempts: N/A

### bitnami/spark

Overview cell: 102

Status: pending | Attempts: N/A

### bitnami/superset

Overview cell: 103

Status: pending | Attempts: N/A

### bitnami/tensorflow-resnet

Overview cell: 104

Status: pending | Attempts: N/A

### bitnami/thanos

Overview cell: 105

Status: pending | Attempts: N/A

### bitnami/tomcat

Overview cell: 106

Status: pending | Attempts: N/A

### bitnami/valkey

Overview cell: 107

Status: pending | Attempts: N/A

### bitnami/valkey-cluster

Overview cell: 108

Status: pending | Attempts: N/A

### bitnami/vault

Overview cell: 109

Status: pending | Attempts: N/A

### bitnami/victoriametrics

Overview cell: 110

Status: pending | Attempts: N/A

### bitnami/whereabouts

Overview cell: 111

Status: pending | Attempts: N/A

### bitnami/wildfly

Overview cell: 112

Status: pending | Attempts: N/A

### bitnami/wordpress

Overview cell: 113

Status: pending | Attempts: N/A

### bitnami/zipkin

Overview cell: 114

Status: pending | Attempts: N/A

### bitnami/zookeeper

Overview cell: 115

Status: pending | Attempts: N/A
