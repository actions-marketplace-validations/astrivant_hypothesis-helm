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
Started (Unix epoch): 1789784049
Elapsed (wall clock): 2160.39 seconds
Chart testing: 1925.31 seconds
Dependency preparation: 229.67 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: interrupted
Discovery complete: True
Unstarted charts: 89

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

7 failed; 17 error; 1 skipped-library; 1 interrupted; 89 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: HH2006

## Errors

92 distinct diagnostics across 156 occurrences; 64 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### bitnami/airflow

Overview cell: 01

Status: failed | Attempts: 614

Audit findings: 2943. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.apiVersions`: Undocumented values path
- `HH2001` at `$.auth.existingSecret`: Undocumented values path
- `HH2001` at `$.auth.fernetKey`: Undocumented values path
- `HH2001` at `$.auth.jwtSecretKey`: Undocumented values path
- `HH2001` at `$.auth.password`: Undocumented values path
- `HH2001` at `$.auth.secretKey`: Undocumented values path
- 2937 additional audit findings in JSON.

#### E036 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: redis 22.0.4 / templates/NOTES.txt

```text
execution error at (redis/templates/NOTES.txt:202:4): VALUES VALIDATION: redis: sentinel.masterService.enabled In order to redirect requests
only to the master pod via the service, you also need to create rbac and serviceAccount. In addition, you need to enable
replica.automountServiceAccountToken.
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.createMaster = true`
- `$.redis.sentinel.service.headless = {}`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0000/paths/afbbf9ab6c6be5d414aa>)

#### E038 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: redis 22.0.4 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.redis.sysctl.image.pullPolicy | Status: failed

Changed overrides (used together):
- `$.redis.sysctl.image.registry = "00"`
- `$.redis.sysctl.image.pullPolicy = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0000/paths/99aa1dfe44b5013eb347>)

#### E040 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on airflow/charts/redis/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 27: could
not find expected ':'
```

Phase: $.redis.networkPolicy.extraIngress | Status: failed

Changed overrides (used together):
- `$.redis.networkPolicy.extraIngress = "0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0000/paths/60062ef473cd803bdad3>)

#### E041 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on airflow/templates/scheduler/poddisruptionbudget.yaml: error converting YAML to JSON: yaml: line 20:
found unexpected end of stream
```

Phase: $.scheduler.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.scheduler.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0000/paths/3a214421b729662a77e2>)

#### E042 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on airflow/templates/worker/poddisruptionbudget.yaml: error converting YAML to JSON: yaml: line 14: block
sequence entries are not allowed in this context
```

Phase: $.worker.pdb | Status: failed

Changed overrides (used together):
- `$.worker.pdb.maxUnavailable = "-" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0000/paths/7b3233b72c7ae2177a76>)

#### E043 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on airflow/templates/worker/statefulset.yaml: error converting YAML to JSON: yaml: line 343: did not find
expected ',' or ']'
```

Phase: $.worker.extraEnvVarsSecrets | Status: failed

Changed overrides (used together):
- `$.worker.extraEnvVarsSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0000/paths/46c228e5cc6f6ce31bc5>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0000>)

### bitnami/apache

Overview cell: 02

Status: failed | Attempts: 3356

Audit findings: 522. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.affinity`: Undocumented values path
- `HH2001` at `$.args`: Undocumented values path
- `HH2001` at `$.automountServiceAccountToken`: Undocumented values path
- `HH2001` at `$.autoscaling.enabled`: Undocumented values path
- `HH2001` at `$.autoscaling.maxReplicas`: Undocumented values path
- `HH2001` at `$.autoscaling.minReplicas`: Undocumented values path
- 516 additional audit findings in JSON.

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/672041fcfe26907bc14c>)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/90454abd7e30d38b69ee>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/fbfea8b96e1bf6abb6fc>)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/840a8a2bc50327388c2a>)

Phase: $.serviceAccount | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/7a010717afb4691aaeb8>)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/98a2bca1991be60ae38a>)

Phase: $.service | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/da628aa79e50e022e4ff>)

#### E015 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/2442d14cba32517cdd3b>)

Phase: $.cloneHtdocsFromGit | Status: failed

Changed overrides (used together):
- `$.cloneHtdocsFromGit.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/3955e2d362e4106c6c9c>)

#### E016 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... kely to cause degraded security and performance, broken chart features, and missing
environment variables. Unrecognized images: - 00/bitnami/apache-exporter:1.0.10-debian-12-r55 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.metrics.image.registry | Status: failed

Changed overrides (used together):
- `$.metrics.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/c96ecbfa425836596f7f>)

Phase: $.metrics.image | Status: failed

Changed overrides (used together):
- `$.metrics.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/d5a06b22eab6d6a5f7fd>)

#### E017 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/fa90b40f46c6c70d8821>)

#### E018 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/488624c1bd95bbae6f8b>)

#### E019 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... rformance, broken chart features, and missing environment variables. Unrecognized images:
- 3/bitnami/apache:2.4.65-debian-12-r2 - 3/bitnami/apache-exporter:1.0.10-debian-12-r55 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "3" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/a8d13bfa12806deaf76c>)

#### E020 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/4c4a07eb1c5214b3a409>)

#### E021 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/3f7165f1837241716c3c>)

#### E022 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/deployment.yaml

```text
execution error at (apache/templates/deployment.yaml:310:25): ERROR: Preset key '' invalid. Allowed values are
xlarge,2xlarge,nano,micro,small,medium,large
```

Phase: $.metrics | Status: failed

Changed overrides (used together):
- `$.metrics.enabled = true (was false)`
- `$.metrics.resourcesPreset = "" (was "none")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/17d970eb96f24f23c2d5>)

#### E023 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: apache 11.4.30 / templates/deployment.yaml

```text
execution error at (apache/templates/deployment.yaml:82:25): ERROR: Preset key '' invalid. Allowed values are
xlarge,2xlarge,nano,micro,small,medium,large
```

Phase: $.resourcesPreset | Status: failed

Changed overrides (used together):
- `$.resourcesPreset = "" (was "nano")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/e4dc47b72a56eb9b1ac6>)

#### E044 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 173: found unexpected end of
stream
```

Phase: $.readinessProbe.path | Status: failed

Changed overrides (used together):
- `$.readinessProbe.path = "'" (was "/")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/6e63684264db9d622def>)

Phase: $.livenessProbe | Status: failed

Changed overrides (used together):
- `$.livenessProbe.port = "'" (was "http")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/4205bc059f894025d23f>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E045 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 174: found unexpected end of
stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/57504c968732d9714f10>)

#### E046 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 175: found unexpected end of
stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/e4b1fa53526f192b7184>)

Phase: $.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/95d9e80fea15aed87f2a>)

#### E047 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 178: found unexpected end of
stream
```

Phase: $.vhostsConfigMap | Status: failed

Changed overrides (used together):
- `$.vhostsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/be14993fbd1c228c36ce>)

#### E048 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 179: found unexpected end of
stream
```

Phase: $.htdocsConfigMap | Status: failed

Changed overrides (used together):
- `$.htdocsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/a84b1abe3a11000d364a>)

Phase: $.htdocsPVC | Status: failed

Changed overrides (used together):
- `$.htdocsPVC = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/8fd174ce0cd7f4de3220>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E049 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/097f6358a00dddbcdd83>)

4 additional occurrences are retained in the JSON report and chart artifacts.

#### E050 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/8e79b7dd85a286cfaddb>)

Phase: $.image.tag | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/7e365cc9986c8fb6c4ad>)

#### E051 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 64: could not find expected
':'
```

Phase: $.image.digest | Status: failed

Changed overrides (used together):
- `$.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/10293d402dd6d1dd34f5>)

#### E052 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 6: could not find expected
':'
```

Phase: $.nameOverride | Status: failed

Changed overrides (used together):
- `$.nameOverride = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/0ce120cfa523ba37df61>)

#### E053 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/pdb.yaml: error converting YAML to JSON: yaml: line 13: block sequence entries are not
allowed in this context
```

Phase: $.pdb | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "-" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/fcc268f7f5d701449828>)

#### E054 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/pdb.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of stream
```

Phase: $.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/d6baed3b8998a068f471>)

Phase: $.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.pdb.minAvailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/07d4854a45a9e7c1eb04>)

#### E055 (HH1101)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/964773c98a041f080dd4>)

Phase: $.service.loadBalancerSourceRanges | Status: failed

Changed overrides (used together):
- `$.service.loadBalancerSourceRanges = [{}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/60903c8f6383b493cf31>)

#### E056 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/6e931799d09f8182f34b>)

#### E057 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 29: found unexpected end of stream
```

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/12b3c4a215648c1d6dd7>)

#### E058 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 30: found unexpected end of stream
```

Phase: $.service.nodePorts.http | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/c91d7fbded4704da55d3>)

Phase: $.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/afbac7d295ec4c0a2908>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E087 (HH1105)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/815bf9b751b356e044f0>)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/e2f7761f901d86846684>)

#### E089 (HH3003)

**Undefined named template** (template / violation). Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: apache/templates/svc.yaml:9:11 executing "apache/templates/svc.yaml" at <include "common.names.fullname" .>: error calling
include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/e2cac8a5225634937910>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0001/paths/2ff2aa2642f40d7be0f3>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0001>)

### bitnami/apisix

Overview cell: 03

Status: failed | Attempts: 308

Audit findings: 1390. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.apiVersions`: Undocumented values path
- `HH2002` at `$.controlPlane.args[*]`: Unspecified values type
- `HH2001` at `$.controlPlane.automountServiceAccountToken`: Undocumented values path
- `HH2003` at `$.controlPlane.autoscaling`: Missing values description
- `HH2003` at `$.controlPlane.autoscaling.hpa`: Missing values description
- `HH2003` at `$.controlPlane.autoscaling.vpa`: Missing values description
- 1384 additional audit findings in JSON.

#### E059 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apisix/charts/etcd/templates/pdb.yaml: error converting YAML to JSON: yaml: line 15: block sequence
entries are not allowed in this context
```

Phase: $.etcd.pdb | Status: failed

Changed overrides (used together):
- `$.etcd.pdb.maxUnavailable = "-"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0002/paths/aaadbc44a6ff4d313d85>)

#### E060 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on apisix/templates/control-plane/dep-ds.yaml: error converting YAML to JSON: yaml: line 335: found
unexpected end of stream
```

Phase: $.controlPlane.extraConfigExistingConfigMap | Status: failed

Changed overrides (used together):
- `$.controlPlane.extraConfigExistingConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0002/paths/98c9de7170b4f8fa32cd>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0002>)

### bitnami/appsmith

Overview cell: 04

Status: failed | Attempts: 403

Audit findings: 1137. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.backend.adminEmail`: Undocumented values path
- `HH2001` at `$.backend.adminPassword`: Undocumented values path
- `HH2001` at `$.backend.adminUser`: Undocumented values path
- `HH2001` at `$.backend.affinity`: Undocumented values path
- `HH2001` at `$.backend.args`: Undocumented values path
- `HH2001` at `$.backend.automountServiceAccountToken`: Undocumented values path
- 1131 additional audit findings in JSON.

#### E033 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: mongodb 16.5.40 / templates/NOTES.txt

```text
execution error at (mongodb/templates/NOTES.txt:173:4): VALUES VALIDATION: mongodb: .Values.externalAccess.service.loadBalancerIPs,
.Values.externalAccess.service.publicNames externalAccess.service.loadBalancerIPs, externalAccess.service.publicNames or
externalAccess.autoDiscovery.enabled are required when externalAccess is enabled.
```

Phase: $.mongodb.externalAccess.dnsCheck.image.pullPolicy | Status: failed

Changed overrides (used together):
- `$.mongodb.externalAccess.dnsCheck.image.pullPolicy = ""`
- `$.mongodb.externalAccess.enabled = true`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0003/paths/b41fced0af41b3f275f5>)

#### E061 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on appsmith/charts/mongodb/templates/replicaset/statefulset.yaml: error converting YAML to JSON: yaml: line
245: found unexpected end of stream
```

Phase: $.mongodb.persistence | Status: failed

Changed overrides (used together):
- `$.mongodb.persistence.storageClass = "\""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0003/paths/41d6ae6f8aea08087045>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0003>)

### bitnami/argo-cd

Overview cell: 05

Status: failed | Attempts: 740

Audit findings: 2695. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.applicationSet.affinity`: Undocumented values path
- `HH2001` at `$.applicationSet.args`: Undocumented values path
- `HH2001` at `$.applicationSet.clusterAdminAccess`: Undocumented values path
- `HH2001` at `$.applicationSet.clusterRoleRules`: Undocumented values path
- `HH2001` at `$.applicationSet.command`: Undocumented values path
- `HH2001` at `$.applicationSet.containerPorts`: Undocumented values path
- 2689 additional audit findings in JSON.

#### E005 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on argo-cd/charts/redis/templates/master/application.yaml: error unmarshaling JSON: while decoding JSON:
json: cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.redis.master.containerSecurityContext.capabilities | Status: failed

Changed overrides (used together):
- `$.redis.master.annotations[""] = []`
- `$.redis.master.containerSecurityContext.capabilities = {}`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0004/paths/b1f1ec661abb570633fe>)

#### E006 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on argo-cd/templates/argocd-secret.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.config.secret.annotations | Status: failed

Changed overrides (used together):
- `$.config.secret.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0004/paths/37a65c14821d2cb3dc89>)

#### E007 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on argo-cd/templates/server/ingress-grcp.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.server.ingressGrpc | Status: failed

Changed overrides (used together):
- `$.server.ingressGrpc.enabled = true (was false)`
- `$.server.ingressGrpc.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0004/paths/13e1a098996e33c7f121>)

#### E037 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: redis 22.0.6 / templates/NOTES.txt

```text
execution error at (redis/templates/NOTES.txt:202:4): VALUES VALIDATION: redis: sentinel.masterService.enabled In order to redirect requests
only to the master pod via the service, you also need to create rbac and serviceAccount. In addition, you need to enable
replica.automountServiceAccountToken.
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.createMaster = true`
- `$.redis.sentinel.service.headless = {}`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0004/paths/afbbf9ab6c6be5d414aa>)

#### E039 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: redis 22.0.6 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r51 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.redis.sysctl.image.pullPolicy | Status: failed

Changed overrides (used together):
- `$.redis.sysctl.image.registry = "00"`
- `$.redis.sysctl.image.pullPolicy = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0004/paths/99aa1dfe44b5013eb347>)

#### E062 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on argo-cd/charts/redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 144:
could not find expected ':'
```

Phase: $.redis.master.persistence.subPath | Status: failed

Changed overrides (used together):
- `$.redis.master.persistence.subPath = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0004/paths/03223810de42d02290b1>)

#### E063 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on argo-cd/charts/redis/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 27: could
not find expected ':'
```

Phase: $.redis.networkPolicy.extraIngress | Status: failed

Changed overrides (used together):
- `$.redis.networkPolicy.extraIngress = "0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0004/paths/60062ef473cd803bdad3>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0004>)

### bitnami/argo-workflows

Overview cell: 06

Status: failed | Attempts: 707

Audit findings: 942. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.clusterDomain`: Undocumented values path
- `HH2001` at `$.commonAnnotations`: Undocumented values path
- `HH2001` at `$.commonLabels`: Undocumented values path
- `HH2001` at `$.controller.affinity`: Undocumented values path
- `HH2001` at `$.controller.args`: Undocumented values path
- `HH2001` at `$.controller.automountServiceAccountToken`: Undocumented values path
- 936 additional audit findings in JSON.

#### E008 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on argo-workflows/charts/mysql/templates/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON:
json: cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.mysql.serviceAccount.create | Status: failed

Changed overrides (used together):
- `$.mysql.enabled = true (was false)`
- `$.mysql.serviceAccount.annotations[""] = []`
- `$.mysql.serviceAccount.create = true`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/4adc4cb4abcc9fd8f917>)

#### E009 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on argo-workflows/templates/controller/workflow-serviceaccount.yaml: error unmarshaling JSON: while
decoding JSON: json: cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.workflows.serviceAccount | Status: failed

Changed overrides (used together):
- `$.workflows.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/c246ccf3c22f11e34d43>)

#### E034 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: mysql 14.0.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mysql.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.mysql.enabled = true (was false)`
- `$.mysql.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/1c25c32c569a13118399>)

#### E035 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: postgresql 16.7.24 / templates/backup/cronjob.yaml

```text
execution error at (postgresql/templates/backup/cronjob.yaml:113:27): ERROR: Preset key '' invalid. Allowed values are
nano,micro,small,medium,large,xlarge,2xlarge
```

Phase: $.postgresql.backup.cronjob.resourcesPreset | Status: failed

Changed overrides (used together):
- `$.postgresql.backup.enabled = true`
- `$.postgresql.backup.cronjob.resourcesPreset = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/b9537445a73ab0ff0555>)

#### E064 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on argo-workflows/charts/mysql/templates/primary/pdb.yaml: error converting YAML to JSON: yaml: line 15:
block sequence entries are not allowed in this context
```

Phase: $.mysql.primary.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.mysql.enabled = true (was false)`
- `$.mysql.primary.pdb.minAvailable = "-"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/dc987487fbeb235e6486>)

#### E065 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on argo-workflows/charts/mysql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml:
line 229: block sequence entries are not allowed in this context
```

Phase: $.mysql.primary.persistentVolumeClaimRetentionPolicy.whenScaled | Status: failed

Changed overrides (used together):
- `$.mysql.enabled = true (was false)`
- `$.mysql.primary.persistentVolumeClaimRetentionPolicy.enabled = true`
- `$.mysql.primary.persistentVolumeClaimRetentionPolicy.whenScaled = "-"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/fc54925f8705724aa0dd>)

#### E066 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on argo-workflows/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON:
yaml: line 185: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/a0cdb2ba618083d9a8df>)

Phase: $.postgresql.global.security.allowInsecureImages | Status: failed

Changed overrides (used together):
- `$.postgresql.global.storageClass = "\""`
- `$.postgresql.global.security.allowInsecureImages = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/219997b4dc4d973903ad>)

#### E067 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on argo-workflows/templates/controller/clusterrolebinding.yaml: error converting YAML to JSON: yaml: line
24: found unexpected end of stream
```

Phase: $.controller.workflowNamespaces[*] | Status: failed

Changed overrides (used together):
- `$.controller.workflowNamespaces = ["'"]`
Absent from overrides: $.controller.workflowNamespaces["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/d21976126c873fdee7bc>)

#### E088 (HH3001)

**Template accesses a missing object** (template / violation). Guard or default the parent object, or require it in the values schema.

```text
[HH3001] Error: argo-workflows/charts/mysql/templates/networkpolicy.yaml:72:69 executing
"argo-workflows/charts/mysql/templates/networkpolicy.yaml" at <$value.port>: nil pointer evaluating interface {}.port
```

Phase: $.mysql.primary.service.extraPorts | Status: failed

Changed overrides (used together):
- `$.mysql.enabled = true (was false)`
- `$.mysql.primary.service.extraPorts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0005/paths/cd1b3bd14efaf6a86788>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0005>)

### bitnami/aspnet-core

Overview cell: 07

Status: failed | Attempts: 3785

Audit findings: 455. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.affinity`: Undocumented values path
- `HH2001` at `$.appFromExistingPVC.enabled`: Undocumented values path
- `HH2001` at `$.appFromExistingPVC.existingClaim`: Undocumented values path
- `HH2001` at `$.appFromExistingPVC`: Undocumented values path
- `HH2001` at `$.appFromExternalRepo.clone`: Undocumented values path
- `HH2001` at `$.appFromExternalRepo.clone.depth`: Undocumented values path
- 449 additional audit findings in JSON.

#### E010 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.commonAnnotations | Status: failed

Changed overrides (used together):
- `$.commonAnnotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/672041fcfe26907bc14c>)

#### E011 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/90454abd7e30d38b69ee>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/fbfea8b96e1bf6abb6fc>)

#### E012 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/ingress.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.ingress | Status: failed

Changed overrides (used together):
- `$.ingress.annotations[""] = []`
- `$.ingress.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/94ed38bb417a953196c3>)

#### E013 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/840a8a2bc50327388c2a>)

Phase: $.serviceAccount | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/7a010717afb4691aaeb8>)

#### E014 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/svc.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.service.annotations | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/98a2bca1991be60ae38a>)

#### E024 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... missing environment variables. Unrecognized images: -
00/bitnami/aspnet-core:9.0.8-debian-12-r1 - 00/bitnami/git:2.51.0-debian-12-r0 - 00/bitnami/dotnet-sdk:9.0.304-debian-12-r1 If you are sure
you want to proceed with non-standard containers, you can skip container image verification by setting the global parameter
'global.security.allowInsecureImages' to true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/fa90b40f46c6c70d8821>)

#### E025 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ...  is likely to cause degraded security and performance, broken chart features, and missing
environment variables. Unrecognized images: - 00/bitnami/aspnet-core:9.0.8-debian-12-r1 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.registry | Status: failed

Changed overrides (used together):
- `$.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/488624c1bd95bbae6f8b>)

#### E026 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... is likely to cause degraded security and performance, broken chart features, and missing
environment variables. Unrecognized images: - 00/bitnami/dotnet-sdk:9.0.304-debian-12-r1 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.appFromExternalRepo.publish.image | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/335895cd5b1c23c13141>)

Phase: $.appFromExternalRepo.publish.image.registry | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/29b5ba41dc3346bc78b7>)

#### E027 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... tainers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/git:2.51.0-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.appFromExternalRepo.clone.image.registry | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/8cfc2368ac94f1308380>)

Phase: $.appFromExternalRepo | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/e59382d74bc7986ca8d9>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E028 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... nd missing environment variables. Unrecognized images: -
;/bitnami/aspnet-core:9.0.8-debian-12-r1 - ;/bitnami/git:2.51.0-debian-12-r0 - ;/bitnami/dotnet-sdk:9.0.304-debian-12-r1 If you are sure you
want to proceed with non-standard containers, you can skip container image verification by setting the global parameter
'global.security.allowInsecureImages' to true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = ";" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/a8d13bfa12806deaf76c>)

#### E029 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:2.51.0-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.appFromExternalRepo.clone.image.repository | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.repository = "00" (was "bitnami/git")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/ce8fb8d6a12771e1474d>)

#### E030 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ntainers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - docker.io/00:9.0.304-debian-12-r1 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.appFromExternalRepo.publish.image.repository | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.repository = "00" (was "bitnami/dotnet-sdk")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/bf662098c8d0dde087b7>)

#### E031 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:9.0.8-debian-12-r1 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/aspnet-core")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/3f7165f1837241716c3c>)

#### E032 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: aspnet-core 8.0.0 / templates/deployment.yaml

```text
execution error at (aspnet-core/templates/deployment.yaml:192:25): ERROR: Preset key '' invalid. Allowed values are
xlarge,2xlarge,nano,micro,small,medium,large
```

Phase: $.resourcesPreset | Status: failed

Changed overrides (used together):
- `$.resourcesPreset = "" (was "micro")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/e4dc47b72a56eb9b1ac6>)

#### E068 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 116: block sequence
entries are not allowed in this context
```

Phase: $.appFromExistingPVC | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.enabled = false (was true)`
- `$.appFromExistingPVC.enabled = true (was false)`
- `$.appFromExistingPVC.existingClaim = "-" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/c85b95ba4b2b42c8b4a0>)

#### E069 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.appFromExternalRepo.clone.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/5a7bb70f23ca77d7dde5>)

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/a4a0ea6ab697189bb963>)

6 additional occurrences are retained in the JSON report and chart artifacts.

#### E070 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 53: mapping values are
not allowed in this context
```

Phase: $.appFromExternalRepo.clone.image.tag | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.tag = "" (was "2.51.0-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/0bcd1f06d8408824711a>)

#### E071 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 55: could not find
expected ':'
```

Phase: $.appFromExternalRepo.clone.image.digest | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/ee7e111c9a45f29550ad>)

#### E072 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: did not find
expected key
```

Phase: $.appFromExternalRepo.clone.repository | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.repository = "\r" (was "https://github.com/dotnet/AspNetCore.Docs.git")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/049a3ecef1d046587065>)

Phase: $.appFromExternalRepo.clone | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.repository = "\n" (was "https://github.com/dotnet/AspNetCore.Docs.git")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/6e3a16a1ebdd1b7e7e4d>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E073 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 66: mapping values are
not allowed in this context
```

Phase: $.appFromExternalRepo.publish.image.tag | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.tag = "" (was "9.0.304-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/6f16a3fce30f040bbbba>)

#### E074 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 68: could not find
expected ':'
```

Phase: $.appFromExternalRepo.publish.image.digest | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/6bc4878f99d5361f4d00>)

#### E075 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 6: could not find
expected ':'
```

Phase: $.nameOverride | Status: failed

Changed overrides (used together):
- `$.nameOverride = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/0ce120cfa523ba37df61>)

#### E076 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 76: could not find
expected ':'
```

Phase: $.appFromExternalRepo.publish.extraFlags | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.extraFlags = [{"\r": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/d6d30e52dda638aa651d>)

Phase: $.appFromExternalRepo.publish.subFolder | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.subFolder = "\n0" (was "aspnetcore/performance/caching/output/samples/8.x/")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/d6eb74839ecc6561f2a6>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E077 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 83: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.0.8-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/8e79b7dd85a286cfaddb>)

Phase: $.image.tag | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.0.8-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/7e365cc9986c8fb6c4ad>)

#### E078 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 85: could not find
expected ':'
```

Phase: $.image.digest | Status: failed

Changed overrides (used together):
- `$.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/10293d402dd6d1dd34f5>)

#### E079 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/health-ingress.yaml: error converting YAML to JSON: yaml: line 19: mapping values
are not allowed in this context
```

Phase: $.healthIngress | Status: failed

Changed overrides (used together):
- `$.healthIngress.enabled = true (was false)`
- `$.healthIngress.extraPaths = true`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/d188de8900bd3c38377a>)

#### E080 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 24: did not find
expected ',' or ']'
```

Phase: $.extraContainerPorts | Status: failed

Changed overrides (used together):
- `$.extraContainerPorts = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/f7f8700baed516b2f5dc>)

Phase: $.extraContainerPorts[*] | Status: failed

Changed overrides (used together):
- `$.extraContainerPorts = [[{}]]`
Absent from overrides: $.extraContainerPorts["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/a734f2883f305d7ad187>)

#### E081 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/pdb.yaml: error converting YAML to JSON: yaml: line 13: block sequence entries are
not allowed in this context
```

Phase: $.pdb | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "-" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/fcc268f7f5d701449828>)

#### E082 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/pdb.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of
stream
```

Phase: $.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/d6baed3b8998a068f471>)

Phase: $.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.pdb.minAvailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/07d4854a45a9e7c1eb04>)

#### E083 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 14: mapping keys are not
allowed in this context
```

Phase: $.service | Status: failed

Changed overrides (used together):
- `$.service.clusterIP = "?" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/da628aa79e50e022e4ff>)

#### E084 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/6e931799d09f8182f34b>)

#### E085 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end of
stream
```

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/12b3c4a215648c1d6dd7>)

#### E086 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end of
stream
```

Phase: $.service.clusterIP | Status: failed

Changed overrides (used together):
- `$.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/dbb776e6ea555257fb86>)

#### E087 (HH1105)

**Missing resource name** (manifest / violation). Provide a name in each resource branch; ignore this check if your workflow intentionally
uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[2].metadata.name: "hypothesis-aspnet-core" -> 0`
- `$[4].spec.template.spec.serviceAccountName: "hypothesis-aspnet-core" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/815bf9b751b356e044f0>)

Phase: $.fullnameOverride | Status: failed

Changed overrides (used together):
- `$.fullnameOverride = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[0].metadata.name: "hypothesis-aspnet-core" -> 0`
- `$[1].metadata.name: "hypothesis-aspnet-core" -> 0`
- `$[2].metadata.name: "hypothesis-aspnet-core" -> 0`
- `$[3].metadata.name: "hypothesis-aspnet-core" -> 0`
- `$[4].metadata.name: "hypothesis-aspnet-core" -> 0`
- `$[4].spec.template.spec.serviceAccountName: "hypothesis-aspnet-core" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/e2f7761f901d86846684>)

#### E090 (HH3003)

**Undefined named template** (template / violation). Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: aspnet-core/templates/svc.yaml:9:11 executing "aspnet-core/templates/svc.yaml" at <include "common.names.fullname" .>: error
calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/e2cac8a5225634937910>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0006/paths/2ff2aa2642f40d7be0f3>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0006>)

### bitnami/cadvisor

Overview cell: 08

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0007>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0007>)

### bitnami/cassandra

Overview cell: 09

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0008>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0008>)

### bitnami/cert-manager

Overview cell: 10

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0009>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0009>)

### bitnami/chainloop

Overview cell: 11

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0010>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0010>)

### bitnami/cilium

Overview cell: 12

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0011>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0011>)

### bitnami/clickhouse

Overview cell: 13

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0012>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0012>)

### bitnami/clickhouse-operator

Overview cell: 14

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0013>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0013>)

### bitnami/cloudnative-pg

Overview cell: 15

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0014>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0014>)

### bitnami/common

Overview cell: 16

Status: skipped-library | Attempts: N/A

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0015>)

### bitnami/concourse

Overview cell: 17

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0016>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0016>)

### bitnami/consul

Overview cell: 18

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0017>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0017>)

### bitnami/contour

Overview cell: 19

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0018>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0018>)

### bitnami/deepspeed

Overview cell: 20

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0019>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0019>)

### bitnami/discourse

Overview cell: 21

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0020>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0020>)

### bitnami/dremio

Overview cell: 22

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0021>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0021>)

### bitnami/drupal

Overview cell: 23

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0022>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0022>)

### bitnami/ejbca

Overview cell: 24

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0023>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0023>)

### bitnami/elasticsearch

Overview cell: 25

Status: error | Attempts: N/A

#### E092

```text
[Errno 2] No such file or directory:
'/Users/emmadoyle/projects/personal/hypothesis-helm/pkg/hypothesis-helm-catalog/hypothesis_helm_catalog/data/chart-bindings.json'
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0024>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0024>)

### bitnami/envoy-gateway

Overview cell: 26

Status: interrupted | Attempts: N/A

#### E091

```text
Interrupted by user
```

Phase: chart | Status: interrupted

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789784049/0025>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789784049/0025>)

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
