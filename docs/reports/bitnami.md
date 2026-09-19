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
Started (Unix epoch): 1789764684
Elapsed (wall clock): 723.57 seconds
Chart testing: 510.43 seconds
Dependency preparation: 211.34 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: interrupted
Discovery complete: True
Unstarted charts: 106

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

6 timeout; 2 failed; 1 interrupted; 106 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: HH2006

## Errors

95 distinct diagnostics across 167 occurrences; 72 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### bitnami/airflow

Overview cell: 01

Status: timeout | Attempts: N/A

#### E092

```text
Command '['helm', 'dependency', 'build', '/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/hypothesis-helm-scan-baiklh1p/chart']' timed out
after 30 seconds
```

Phase: chart | Status: timeout

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0000>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0000>)

### bitnami/apache

Overview cell: 02

Status: timeout | Attempts: N/A

#### E091

```text
Command '['helm', 'dependency', 'build', '/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/hypothesis-helm-scan-ba4in1eu/chart']' timed out
after 30 seconds
```

Phase: chart | Status: timeout

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0001>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0001>)

### bitnami/apisix

Overview cell: 03

Status: timeout | Attempts: N/A

#### E094

```text
Command '['helm', 'dependency', 'build', '/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/hypothesis-helm-scan-xuu93kfc/chart']' timed out
after 30 seconds
```

Phase: chart | Status: timeout

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0002>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0002>)

### bitnami/appsmith

Overview cell: 04

Status: timeout | Attempts: N/A

#### E090

```text
Command '['helm', 'dependency', 'build', '/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/hypothesis-helm-scan-34eb2if3/chart']' timed out
after 30 seconds
```

Phase: chart | Status: timeout

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0003>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0003>)

### bitnami/argo-cd

Overview cell: 05

Status: timeout | Attempts: N/A

#### E093

```text
Command '['helm', 'dependency', 'build', '/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/hypothesis-helm-scan-kcykcp1h/chart']' timed out
after 30 seconds
```

Phase: chart | Status: timeout

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0004>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0004>)

### bitnami/argo-workflows

Overview cell: 06

Status: timeout | Attempts: N/A

#### E095

```text
Command '['helm', 'dependency', 'build', '/var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/hypothesis-helm-scan-zcub7olm/chart']' timed out
after 30 seconds
```

Phase: chart | Status: timeout

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0005>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0005>)

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

#### E001 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.commonAnnotations | Status: failed

Changed overrides (used together):
- `$.commonAnnotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/672041fcfe26907bc14c>)

#### E002 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/90454abd7e30d38b69ee>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/fbfea8b96e1bf6abb6fc>)

#### E003 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/94ed38bb417a953196c3>)

#### E004 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/840a8a2bc50327388c2a>)

Phase: $.serviceAccount | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/7a010717afb4691aaeb8>)

#### E005 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on aspnet-core/templates/svc.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.service.annotations | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/98a2bca1991be60ae38a>)

#### E016 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/fa90b40f46c6c70d8821>)

#### E017 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/488624c1bd95bbae6f8b>)

#### E018 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/335895cd5b1c23c13141>)

Phase: $.appFromExternalRepo.publish.image.registry | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/29b5ba41dc3346bc78b7>)

#### E019 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/8cfc2368ac94f1308380>)

Phase: $.appFromExternalRepo | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/e59382d74bc7986ca8d9>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E020 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/a8d13bfa12806deaf76c>)

#### E021 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/ce8fb8d6a12771e1474d>)

#### E022 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/bf662098c8d0dde087b7>)

#### E023 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/3f7165f1837241716c3c>)

#### E024 (HH1001)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/e4dc47b72a56eb9b1ac6>)

#### E040 (HH1101)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/c85b95ba4b2b42c8b4a0>)

#### E041 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.appFromExternalRepo.clone.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/5a7bb70f23ca77d7dde5>)

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/a4a0ea6ab697189bb963>)

6 additional occurrences are retained in the JSON report and chart artifacts.

#### E042 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 53: mapping values are
not allowed in this context
```

Phase: $.appFromExternalRepo.clone.image.tag | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.tag = "" (was "2.51.0-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/0bcd1f06d8408824711a>)

#### E043 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 55: could not find
expected ':'
```

Phase: $.appFromExternalRepo.clone.image.digest | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/ee7e111c9a45f29550ad>)

#### E044 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: did not find
expected key
```

Phase: $.appFromExternalRepo.clone.repository | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.repository = "\r" (was "https://github.com/dotnet/AspNetCore.Docs.git")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/049a3ecef1d046587065>)

Phase: $.appFromExternalRepo.clone | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.repository = "\n" (was "https://github.com/dotnet/AspNetCore.Docs.git")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/6e3a16a1ebdd1b7e7e4d>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E045 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 66: mapping values are
not allowed in this context
```

Phase: $.appFromExternalRepo.publish.image.tag | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.tag = "" (was "9.0.304-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/6f16a3fce30f040bbbba>)

#### E046 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 68: could not find
expected ':'
```

Phase: $.appFromExternalRepo.publish.image.digest | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/6bc4878f99d5361f4d00>)

#### E047 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 6: could not find
expected ':'
```

Phase: $.nameOverride | Status: failed

Changed overrides (used together):
- `$.nameOverride = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/0ce120cfa523ba37df61>)

#### E048 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 76: could not find
expected ':'
```

Phase: $.appFromExternalRepo.publish.extraFlags | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.extraFlags = [{"\r": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/d6d30e52dda638aa651d>)

Phase: $.appFromExternalRepo.publish.subFolder | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.subFolder = "\n0" (was "aspnetcore/performance/caching/output/samples/8.x/")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/d6eb74839ecc6561f2a6>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E049 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 83: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.0.8-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/8e79b7dd85a286cfaddb>)

Phase: $.image.tag | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.0.8-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/7e365cc9986c8fb6c4ad>)

#### E050 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 85: could not find
expected ':'
```

Phase: $.image.digest | Status: failed

Changed overrides (used together):
- `$.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/10293d402dd6d1dd34f5>)

#### E051 (HH1101)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/d188de8900bd3c38377a>)

#### E052 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 24: did not find
expected ',' or ']'
```

Phase: $.extraContainerPorts | Status: failed

Changed overrides (used together):
- `$.extraContainerPorts = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/f7f8700baed516b2f5dc>)

Phase: $.extraContainerPorts[*] | Status: failed

Changed overrides (used together):
- `$.extraContainerPorts = [[{}]]`
Absent from overrides: $.extraContainerPorts["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/a734f2883f305d7ad187>)

#### E053 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/pdb.yaml: error converting YAML to JSON: yaml: line 13: block sequence entries are
not allowed in this context
```

Phase: $.pdb | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "-" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/fcc268f7f5d701449828>)

#### E054 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/pdb.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of
stream
```

Phase: $.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/d6baed3b8998a068f471>)

Phase: $.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.pdb.minAvailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/07d4854a45a9e7c1eb04>)

#### E055 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 14: mapping keys are not
allowed in this context
```

Phase: $.service | Status: failed

Changed overrides (used together):
- `$.service.clusterIP = "?" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/da628aa79e50e022e4ff>)

#### E056 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/6e931799d09f8182f34b>)

#### E057 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end of
stream
```

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/12b3c4a215648c1d6dd7>)

#### E058 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end of
stream
```

Phase: $.service.clusterIP | Status: failed

Changed overrides (used together):
- `$.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/dbb776e6ea555257fb86>)

#### E086 (HH1105)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/815bf9b751b356e044f0>)

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/e2f7761f901d86846684>)

#### E088 (HH3003)

**Undefined named template** (template / violation). Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: aspnet-core/templates/svc.yaml:9:11 executing "aspnet-core/templates/svc.yaml" at <include "common.names.fullname" .>: error
calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/e2cac8a5225634937910>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0006/paths/2ff2aa2642f40d7be0f3>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0006>)

### bitnami/cadvisor

Overview cell: 08

Status: failed | Attempts: 2651

Audit findings: 397. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.affinity`: Undocumented values path
- `HH2001` at `$.args`: Undocumented values path
- `HH2001` at `$.automountServiceAccountToken`: Undocumented values path
- `HH2001` at `$.clusterDomain`: Undocumented values path
- `HH2004` at `$.clusterDomain`: No supplied default for a values path
- `HH2001` at `$.command`: Undocumented values path
- 391 additional audit findings in JSON.

#### E006 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.commonAnnotations | Status: failed

Changed overrides (used together):
- `$.commonAnnotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/672041fcfe26907bc14c>)

#### E007 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cadvisor/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/90454abd7e30d38b69ee>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/fbfea8b96e1bf6abb6fc>)

#### E008 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cadvisor/templates/service-account.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/840a8a2bc50327388c2a>)

Phase: $.serviceAccount | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/7a010717afb4691aaeb8>)

#### E009 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cadvisor/templates/service.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.metrics | Status: failed

Changed overrides (used together):
- `$.metrics.annotations[""] = []`
- `$.metrics.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/17d970eb96f24f23c2d5>)

#### E015 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: cadvisor/templates/service.yaml:10:20 executing "cadvisor/templates/service.yaml" at <{{template "common.names.fullname"
.}}>: template "common.names.fullname" not defined
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/e2cac8a5225634937910>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/2ff2aa2642f40d7be0f3>)

#### E025 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cadvisor 0.1.14 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... rs is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/cadvisor:0.53.0-debian-12-r9 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/8e79b7dd85a286cfaddb>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/fa90b40f46c6c70d8821>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E026 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cadvisor 0.1.14 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - ;/bitnami/cadvisor:0.53.0-debian-12-r9 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = ";" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/a8d13bfa12806deaf76c>)

#### E027 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cadvisor 0.1.14 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:0.53.0-debian-12-r9 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/cadvisor")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/3f7165f1837241716c3c>)

#### E028 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cadvisor 0.1.14 / templates/daemonset.yaml

```text
execution error at (cadvisor/templates/daemonset.yaml:155:25): ERROR: Preset key '' invalid. Allowed values are
nano,micro,small,medium,large,xlarge,2xlarge
```

Phase: $.resourcesPreset | Status: failed

Changed overrides (used together):
- `$.resourcesPreset = "" (was "small")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/e4dc47b72a56eb9b1ac6>)

#### E059 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 144: found unexpected end
of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/57504c968732d9714f10>)

#### E060 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 145: found unexpected end
of stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/e4b1fa53526f192b7184>)

Phase: $.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/95d9e80fea15aed87f2a>)

#### E061 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 35: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/097f6358a00dddbcdd83>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E062 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 60: mapping values are not
allowed in this context
```

Phase: $.image.tag | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "0.53.0-debian-12-r9")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/7e365cc9986c8fb6c4ad>)

#### E063 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 62: could not find expected
':'
```

Phase: $.image.digest | Status: failed

Changed overrides (used together):
- `$.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/10293d402dd6d1dd34f5>)

#### E064 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 6: could not find expected
':'
```

Phase: $.nameOverride | Status: failed

Changed overrides (used together):
- `$.nameOverride = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/0ce120cfa523ba37df61>)

#### E065 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 27: did not find
expected ',' or ']'
```

Phase: $.extraContainerPorts | Status: failed

Changed overrides (used together):
- `$.extraContainerPorts = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/f7f8700baed516b2f5dc>)

Phase: $.extraContainerPorts[*] | Status: failed

Changed overrides (used together):
- `$.extraContainerPorts = [[{}]]`
Absent from overrides: $.extraContainerPorts["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/a734f2883f305d7ad187>)

#### E066 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 40: found unexpected
end of stream
```

Phase: $.namespaceOverride | Status: failed

Changed overrides (used together):
- `$.namespaceOverride = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/835d62e0a3e46b72c904>)

#### E067 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/service.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/6e931799d09f8182f34b>)

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/12b3c4a215648c1d6dd7>)

#### E068 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/service.yaml: error converting YAML to JSON: yaml: line 27: found unexpected end of
stream
```

Phase: $.service.clusterIP | Status: failed

Changed overrides (used together):
- `$.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/dbb776e6ea555257fb86>)

Phase: $.service | Status: failed

Changed overrides (used together):
- `$.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/da628aa79e50e022e4ff>)

#### E086 (HH1105)

**Missing resource name** (manifest / violation). Provide a name in each resource branch; ignore this check if your workflow intentionally
uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[1].metadata.name: "hypothesis-cadvisor" -> 0`
- `$[3].spec.template.spec.serviceAccountName: "hypothesis-cadvisor" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/815bf9b751b356e044f0>)

Phase: $.fullnameOverride | Status: failed

Changed overrides (used together):
- `$.fullnameOverride = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[0].metadata.name: "hypothesis-cadvisor" -> 0`
- `$[0].spec.ingress[0].from[2].podSelector.matchLabels["0-client"]: <absent> -> "true"`
- `$[0].spec.ingress[0].from[2].podSelector.matchLabels["hypothesis-cadvisor-client"]: "true" -> <absent>`
- `$[1].metadata.name: "hypothesis-cadvisor" -> 0`
- `$[2].metadata.name: "hypothesis-cadvisor" -> 0`
- `$[3].metadata.name: "hypothesis-cadvisor" -> 0`
- 1 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/e2f7761f901d86846684>)

#### E087 (HH3001)

**Template accesses a missing object** (template / violation). Guard or default the parent object, or require it in the values schema.

```text
[HH3001] Error: cadvisor/templates/ingress.yaml:45:15 executing "cadvisor/templates/ingress.yaml" at <.name>: nil pointer evaluating
interface {}.name
```

Phase: $.ingress | Status: failed

Changed overrides (used together):
- `$.ingress.enabled = true (was false)`
- `$.ingress.extraHosts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0007/paths/94ed38bb417a953196c3>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0007>)

### bitnami/cassandra

Overview cell: 09

Status: interrupted | Attempts: 3818

Audit findings: 713. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.affinity`: Undocumented values path
- `HH2001` at `$.args`: Undocumented values path
- `HH2001` at `$.automountServiceAccountToken`: Undocumented values path
- `HH2001` at `$.cluster.clientEncryption`: Undocumented values path
- `HH2001` at `$.cluster.datacenter`: Undocumented values path
- `HH2001` at `$.cluster.enableUDF`: Undocumented values path
- 707 additional audit findings in JSON.

#### E010 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cassandra/templates/cassandra-secret.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.commonAnnotations | Status: failed

Changed overrides (used together):
- `$.commonAnnotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/672041fcfe26907bc14c>)

#### E011 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cassandra/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/90454abd7e30d38b69ee>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/fbfea8b96e1bf6abb6fc>)

#### E012 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cassandra/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.service.headless | Status: failed

Changed overrides (used together):
- `$.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/080cc1bcf6b1359ec69f>)

Phase: $.service.headless.annotations | Status: failed

Changed overrides (used together):
- `$.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/80250531f5bc656abc1c>)

#### E013 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cassandra/templates/service.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.service.annotations | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/98a2bca1991be60ae38a>)

#### E014 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

```text
[HH1001] Error: YAML parse error on cassandra/templates/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/840a8a2bc50327388c2a>)

#### E029 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
execution error at (cassandra/templates/NOTES.txt:95:4): VALUES VALIDATION: cassandra: cluster.seedCount Number of seed nodes must be
greater or equal than 1 and less or equal to `replicaCount`.
```

Phase: $.cluster.seedCount | Status: failed

Changed overrides (used together):
- `$.cluster.seedCount = 0 (was 1)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/3a1f210c8f82798cf797>)

Phase: $.replicaCount | Status: failed

Changed overrides (used together):
- `$.replicaCount = 0 (was 1)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/2fc729398ad8da25e389>)

#### E030 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ly to cause degraded security and performance, broken chart features, and missing
environment variables. Unrecognized images: - 00/bitnami/cassandra-exporter:2.3.8-debian-12-r51 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.metrics.image.registry | Status: failed

Changed overrides (used together):
- `$.metrics.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/c96ecbfa425836596f7f>)

#### E031 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ages: - 00/bitnami/cassandra:5.0.5-debian-12-r7 - 00/bitnami/os-shell:12-debian-12-r50 -
00/bitnami/cassandra-exporter:2.3.8-debian-12-r51 - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/fa90b40f46c6c70d8821>)

#### E032 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... rs is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/cassandra:5.0.5-debian-12-r7 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.registry | Status: failed

Changed overrides (used together):
- `$.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/488624c1bd95bbae6f8b>)

#### E033 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.volumePermissions.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/5356324f9a8a2798b69d>)

Phase: $.dynamicSeedDiscovery | Status: failed

Changed overrides (used together):
- `$.dynamicSeedDiscovery.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/82979909921faec20100>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E034 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d images: - 4/bitnami/cassandra:5.0.5-debian-12-r7 - 4/bitnami/os-shell:12-debian-12-r50
- 4/bitnami/cassandra-exporter:2.3.8-debian-12-r51 - 4/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "4" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/a8d13bfa12806deaf76c>)

#### E035 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ainers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 4/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.volumePermissions | Status: failed

Changed overrides (used together):
- `$.volumePermissions.image.registry = "4" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/4cf65bc6a2a5b08ed601>)

#### E036 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.dynamicSeedDiscovery.image.repository | Status: failed

Changed overrides (used together):
- `$.dynamicSeedDiscovery.image.repository = "00" (was "bitnami/os-shell")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/acae945d649aa18e9fa9>)

Phase: $.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.volumePermissions.image.repository = "00" (was "bitnami/os-shell")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/63637c9f211787d1e80b>)

#### E037 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:2.3.8-debian-12-r51 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.metrics.image.repository | Status: failed

Changed overrides (used together):
- `$.metrics.image.repository = "00" (was "bitnami/cassandra-exporter")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/4c4a07eb1c5214b3a409>)

#### E038 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:5.0.5-debian-12-r7 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/cassandra")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/3f7165f1837241716c3c>)

#### E039 (HH1001)

**Unclassified template failure** (unclassified / diagnostic). Inspect the Helm diagnostic and reproducer; the exit alone does not establish
a chart defect.

Source: cassandra 12.3.13 / templates/statefulset.yaml

```text
execution error at (cassandra/templates/statefulset.yaml:354:47): ERROR: Preset key '' invalid. Allowed values are
large,xlarge,2xlarge,nano,micro,small,medium
```

Phase: $.resourcesPreset | Status: failed

Changed overrides (used together):
- `$.resourcesPreset = "" (was "large")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/e4dc47b72a56eb9b1ac6>)

#### E069 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/metrics-secret.yaml: error converting YAML to JSON: yaml: line 18: could not find
expected ':'
```

Phase: $.metrics.configuration | Status: failed

Changed overrides (used together):
- `$.metrics.configuration = "\r0" (was "host: localhost:{{ .Values.containerPorts.jmx }}\nssl: False\nuser:\npassword:\nlistenPort: {{ .Values.metrics.containe... [value shortened])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/caf41e6602104795a7b8>)

#### E070 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/pdb.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of
stream
```

Phase: $.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/d6baed3b8998a068f471>)

Phase: $.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.pdb.minAvailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/07d4854a45a9e7c1eb04>)

#### E071 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/service.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/6e931799d09f8182f34b>)

#### E072 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/service.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end of
stream
```

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/12b3c4a215648c1d6dd7>)

#### E073 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/service.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end of
stream
```

Phase: $.service.clusterIP | Status: failed

Changed overrides (used together):
- `$.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/dbb776e6ea555257fb86>)

#### E074 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 198: mapping keys are
not allowed in this context
```

Phase: $.dbUser | Status: failed

Changed overrides (used together):
- `$.dbUser.existingSecret = "?" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/be708ea73ded5e91e5c3>)

#### E075 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 204: found unexpected
end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/bc81b51736a9cdc4eda3>)

#### E076 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 216: found unexpected
end of stream
```

Phase: $.cluster.name | Status: failed

Changed overrides (used together):
- `$.cluster.name = "'" (was "cassandra")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/997a544959269c83f96e>)

Phase: $.cluster.datacenter | Status: failed

Changed overrides (used together):
- `$.cluster.datacenter = "'" (was "dc1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/d62e4ddd0318de46f447>)

6 additional occurrences are retained in the JSON report and chart artifacts.

#### E077 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 217: found unexpected
end of stream
```

Phase: $.hostPorts | Status: failed

Changed overrides (used together):
- `$.hostPorts.cql = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/fcada9ae3b1f71ab92ef>)

Phase: $.hostPorts.intra | Status: failed

Changed overrides (used together):
- `$.hostPorts.intra = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/ff4247849433dbc1dc6b>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E078 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 218: found unexpected
end of stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/e4b1fa53526f192b7184>)

Phase: $.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/95d9e80fea15aed87f2a>)

#### E079 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 221: found unexpected
end of stream
```

Phase: $.initDBSecret | Status: failed

Changed overrides (used together):
- `$.initDBSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/54a61259d47f0b2947b0>)

Phase: $.existingConfiguration | Status: failed

Changed overrides (used together):
- `$.existingConfiguration = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/b8d26a67f31dafe2dd39>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E080 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 222: found unexpected
end of stream
```

Phase: $.tls.passwordsSecret | Status: failed

Changed overrides (used together):
- `$.tls.passwordsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/fd86875f7ea151e0d614>)

Phase: $.tls.tlsEncryptionSecretName | Status: failed

Changed overrides (used together):
- `$.tls.tlsEncryptionSecretName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/56340c110a9ba1e1ed76>)

#### E081 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 232: found unexpected
end of stream
```

Phase: $.persistence | Status: failed

Changed overrides (used together):
- `$.persistence.commitLogMountPath = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/d3b44e124b198b7372d7>)

Phase: $.persistence.commitLogMountPath | Status: failed

Changed overrides (used together):
- `$.persistence.commitLogMountPath = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/92249e1c342634368569>)

#### E082 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 282: found unexpected
end of stream
```

Phase: $.tls | Status: failed

Changed overrides (used together):
- `$.tls.existingSecret = "'" (was "")`
- `$.tls.internodeEncryption = "" (was "none")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/cc663bdc9e00d3d93c78>)

#### E083 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 31: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/097f6358a00dddbcdd83>)

6 additional occurrences are retained in the JSON report and chart artifacts.

#### E084 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 68: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "5.0.5-debian-12-r7")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/8e79b7dd85a286cfaddb>)

Phase: $.image.tag | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "5.0.5-debian-12-r7")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/7e365cc9986c8fb6c4ad>)

#### E085 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Inspect the failing YAML and template interpolation, including quoting and
indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 70: could not find
expected ':'
```

Phase: $.image.digest | Status: failed

Changed overrides (used together):
- `$.image.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/10293d402dd6d1dd34f5>)

#### E086 (HH1105)

**Missing resource name** (manifest / violation). Provide a name in each resource branch; ignore this check if your workflow intentionally
uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[2].metadata.name: "hypothesis-cassandra" -> 0`
- `$[3].data["cassandra-password"]: "eURpQWUyN0lKUQ==" -> "V2xRQ1pRcEJuRw=="`
- `$[7].spec.template.spec.serviceAccountName: "hypothesis-cassandra" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/815bf9b751b356e044f0>)

Phase: $.fullnameOverride | Status: failed

Changed overrides (used together):
- `$.fullnameOverride = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[0].metadata.name: "hypothesis-cassandra" -> 0`
- `$[1].metadata.name: "hypothesis-cassandra" -> 0`
- `$[2].metadata.name: "hypothesis-cassandra" -> 0`
- `$[3].data["cassandra-password"]: "eURpQWUyN0lKUQ==" -> "V1R6VmJBSjVvQg=="`
- `$[3].metadata.name: "hypothesis-cassandra" -> 0`
- `$[4].metadata.name: "hypothesis-cassandra-metrics-conf" -> "0-metrics-conf"`
- 8 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/e2f7761f901d86846684>)

#### E089 (HH3003)

**Undefined named template** (template / violation). Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: cassandra/templates/statefulset.yaml:6:15 executing "cassandra/templates/statefulset.yaml" at <include
"common.capabilities.statefulset.apiVersion" .>: error calling include: template: no template "common.capabilities.statefulset.apiVersion"
associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/e2cac8a5225634937910>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789764684/0008/paths/2ff2aa2642f40d7be0f3>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789764684/0008>)

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
