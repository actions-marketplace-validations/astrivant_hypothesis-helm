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
- [Appendix: finding codes](#appendix-finding-codes)
  - [HH2001 - Undocumented values path](#hh2001---undocumented-values-path)
  - [HH2002 - Unspecified values type](#hh2002---unspecified-values-type)
  - [HH2003 - Missing values description](#hh2003---missing-values-description)
  - [HH2004 - No supplied default for a values path](#hh2004---no-supplied-default-for-a-values-path)
  - [HH2006 - Opaque object schema](#hh2006---opaque-object-schema)

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
Started (Unix epoch): 1790023254
Started (UTC): 2026-09-21T20:40:54.000+00:00
Finished (UTC): 2026-09-21T20:58:10.038+00:00
Run fingerprint (SHA-256): `07cdade5dc97c59ccee41b82b9f9e77d6dd466cf850568346970ae063cdc4fe2`
Elapsed (wall clock): 1035.22 seconds
Chart testing: 112.22 seconds
Dependency preparation: 910.26 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: completed
Discovery complete: True
Unstarted charts: 0

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

114 unsupported-schema; 1 skipped-library.

## Settings

Filtering: True | Seed: 0 | Traversal: sensitivity-first
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: [HH2006](#hh2006---opaque-object-schema)

## Errors

1 distinct diagnostics across 114 occurrences; 113 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### [bitnami/airflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/airflow>)

Overview cell: 01

Status: unsupported-schema | Attempts: N/A

Audit findings: 1190. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.fernetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0000>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0000>)

### [bitnami/apache](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apache>)

Overview cell: 02

Status: unsupported-schema | Attempts: N/A

Audit findings: 245. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 239 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0001>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0001>)

### [bitnami/apisix](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apisix>)

Overview cell: 03

Status: unsupported-schema | Attempts: N/A

Audit findings: 344. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.controlPlane.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controlPlane.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.vpa`: Missing values description (info)
- 338 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0002>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0002>)

### [bitnami/appsmith](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/appsmith>)

Overview cell: 04

Status: unsupported-schema | Attempts: N/A

Audit findings: 543. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.automountServiceAccountToken`: Undocumented values path (warning)
- 537 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0003>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0003>)

### [bitnami/argo-cd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-cd>)

Overview cell: 05

Status: unsupported-schema | Attempts: N/A

Audit findings: 1251. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterAdminAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterRoleRules`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.containerPorts`: Undocumented values path (warning)
- 1245 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0004>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0004>)

### [bitnami/argo-workflows](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-workflows>)

Overview cell: 06

Status: unsupported-schema | Attempts: N/A

Audit findings: 452. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.automountServiceAccountToken`: Undocumented values path (warning)
- 446 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0005>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0005>)

### [bitnami/aspnet-core](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/aspnet-core>)

Overview cell: 07

Status: unsupported-schema | Attempts: N/A

Audit findings: 224. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.existingClaim`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone.depth`: Undocumented values path (warning)
- 218 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0006>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0006>)

### [bitnami/cadvisor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cadvisor>)

Overview cell: 08

Status: unsupported-schema | Attempts: N/A

Audit findings: 192. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.clusterDomain`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 186 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0007>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0007>)

### [bitnami/cassandra](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cassandra>)

Overview cell: 09

Status: unsupported-schema | Attempts: N/A

Audit findings: 309. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.clientEncryption`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.datacenter`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.enableUDF`: Undocumented values path (warning)
- 303 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0008>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0008>)

### [bitnami/cert-manager](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cert-manager>)

Overview cell: 10

Status: unsupported-schema | Attempts: N/A

Audit findings: 404. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.containerSecurityContext`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.containerSecurityContext.allowPrivilegeEscalation`: Undocumented values path
  (warning)
- 398 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0009>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0009>)

### [bitnami/chainloop](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/chainloop>)

Overview cell: 11

Status: unsupported-schema | Attempts: N/A

Audit findings: 643. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 637 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0010>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0010>)

### [bitnami/cilium](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cilium>)

Overview cell: 12

Status: unsupported-schema | Attempts: N/A

Audit findings: 1163. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.agent.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling.vpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling.vpa.annotations`: Undocumented values path (warning)
- 1157 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0011>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0011>)

### [bitnami/clickhouse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse>)

Overview cell: 13

Status: unsupported-schema | Attempts: N/A

Audit findings: 507. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 501 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0012>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0012>)

### [bitnami/clickhouse-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse-operator>)

Overview cell: 14

Status: unsupported-schema | Attempts: N/A

Audit findings: 276. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.username`: Undocumented values path (warning)
- 270 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0013>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0013>)

### [bitnami/cloudnative-pg](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cloudnative-pg>)

Overview cell: 15

Status: unsupported-schema | Attempts: N/A

Audit findings: 423. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.extraDeploy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.fullnameOverride`: Undocumented values path (warning)
- 417 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0014>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0014>)

### [bitnami/common](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/common>)

Overview cell: 16

Status: skipped-library | Attempts: N/A

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0015>)

### [bitnami/concourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/concourse>)

Overview cell: 17

Status: unsupported-schema | Attempts: N/A

Audit findings: 470. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 464 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0016>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0016>)

### [bitnami/consul](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/consul>)

Overview cell: 18

Status: unsupported-schema | Attempts: N/A

Audit findings: 255. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 249 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0017>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0017>)

### [bitnami/contour](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/contour>)

Overview cell: 19

Status: unsupported-schema | Attempts: N/A

Audit findings: 591. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline["accesslog-format"]`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.disablePermitInsecure`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.tls`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.tls["fallback-certificate"]`: Undocumented values path (warning)
- 585 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0018>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0018>)

### [bitnami/deepspeed](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/deepspeed>)

Overview cell: 20

Status: unsupported-schema | Attempts: N/A

Audit findings: 166. Full paths and template references are retained in the JSON report.

- [HH2002](#hh2002---unspecified-values-type) at `$.client.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.client.persistence.mountPath`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.client.client.persistence.mountPath`: No supplied default for a values
  path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.client.command[*]`: Unspecified values type (warning)
- [HH2003](#hh2003---missing-values-description) at `$.client.containerSecurityContext`: Missing values description (info)
- 160 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0019>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0019>)

### [bitnami/discourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/discourse>)

Overview cell: 21

Status: unsupported-schema | Attempts: N/A

Audit findings: 346. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.email`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.username`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth`: Undocumented values path (warning)
- 340 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0020>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0020>)

### [bitnami/dremio](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/dremio>)

Overview cell: 22

Status: unsupported-schema | Attempts: N/A

Audit findings: 1181. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bootstrapUserJob.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bootstrapUserJob.annotations["helm.sh/hook"]`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bootstrapUserJob.annotations["helm.sh/hook-delete-policy"]`: Undocumented values path
  (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bootstrapUserJob.annotations["helm.sh/hook-weight"]`: Undocumented values path
  (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bootstrapUserJob.automountServiceAccountToken`: Undocumented values path (warning)
- 1175 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0021>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0021>)

### [bitnami/drupal](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/drupal>)

Overview cell: 23

Status: unsupported-schema | Attempts: N/A

Audit findings: 319. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.command`: Undocumented values path (warning)
- 313 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0022>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0022>)

### [bitnami/ejbca](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ejbca>)

Overview cell: 24

Status: unsupported-schema | Attempts: N/A

Audit findings: 224. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- 218 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0023>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0023>)

### [bitnami/elasticsearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/elasticsearch>)

Overview cell: 25

Status: unsupported-schema | Attempts: N/A

Audit findings: 814. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.config`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.containerPorts.restAPI`: Undocumented values path (warning)
- 808 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0024>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0024>)

### [bitnami/envoy-gateway](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/envoy-gateway>)

Overview cell: 26

Status: unsupported-schema | Attempts: N/A

Audit findings: 325. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 319 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0025>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0025>)

### [bitnami/etcd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/etcd>)

Overview cell: 27

Status: unsupported-schema | Attempts: N/A

Audit findings: 407. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.caFilename`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.certFilename`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.certKeyFilename`: Undocumented values path (warning)
- 401 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0026>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0026>)

### [bitnami/external-dns](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/external-dns>)

Overview cell: 28

Status: unsupported-schema | Attempts: N/A

Audit findings: 402. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.accessToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.clientSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.clientToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.host`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.secretName`: Undocumented values path (warning)
- 396 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0027>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0027>)

### [bitnami/flink](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flink>)

Overview cell: 29

Status: unsupported-schema | Attempts: N/A

Audit findings: 281. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 275 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0028>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0028>)

### [bitnami/fluent-bit](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluent-bit>)

Overview cell: 30

Status: unsupported-schema | Attempts: N/A

Audit findings: 240. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.annotations`: Undocumented values path (warning)
- 234 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0029>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0029>)

### [bitnami/fluentd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluentd>)

Overview cell: 31

Status: unsupported-schema | Attempts: N/A

Audit findings: 427. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.aggregator.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.autoscaling`: Undocumented values path (warning)
- 421 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0030>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0030>)

### [bitnami/flux](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flux>)

Overview cell: 32

Status: unsupported-schema | Attempts: N/A

Audit findings: 1042. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 1036 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0031>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0031>)

### [bitnami/ghost](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ghost>)

Overview cell: 33

Status: unsupported-schema | Attempts: N/A

Audit findings: 262. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 256 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0032>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0032>)

### [bitnami/gitea](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitea>)

Overview cell: 34

Status: unsupported-schema | Attempts: N/A

Audit findings: 241. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminUsername`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- 235 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0033>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0033>)

### [bitnami/gitlab-runner](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitlab-runner>)

Overview cell: 35

Status: unsupported-schema | Attempts: N/A

Audit findings: 266. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 260 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0034>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0034>)

### [bitnami/grafana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana>)

Overview cell: 36

Status: unsupported-schema | Attempts: N/A

Audit findings: 306. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.admin.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.user`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alerting.configMapName`: Undocumented values path (warning)
- 300 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0035>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0035>)

### [bitnami/grafana-alloy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-alloy>)

Overview cell: 37

Status: unsupported-schema | Attempts: N/A

Audit findings: 292. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.name`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.portName`: Undocumented values path (warning)
- 286 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0036>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0036>)

### [bitnami/grafana-k6-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-k6-operator>)

Overview cell: 38

Status: unsupported-schema | Attempts: N/A

Audit findings: 195. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 189 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0037>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0037>)

### [bitnami/grafana-loki](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-loki>)

Overview cell: 39

Status: unsupported-schema | Attempts: N/A

Audit findings: 1386. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.automountServiceAccountToken`: Undocumented values path (warning)
- 1380 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0038>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0038>)

### [bitnami/grafana-mimir](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-mimir>)

Overview cell: 40

Status: unsupported-schema | Attempts: N/A

Audit findings: 1540. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage.backend`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage.config`: Undocumented values path (warning)
- 1534 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0039>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0039>)

### [bitnami/grafana-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-operator>)

Overview cell: 41

Status: unsupported-schema | Attempts: N/A

Audit findings: 277. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.extraDeploy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.fullnameOverride`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.global.compatibility`: Undocumented values path (warning)
- 271 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0040>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0040>)

### [bitnami/grafana-tempo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-tempo>)

Overview cell: 42

Status: unsupported-schema | Attempts: N/A

Audit findings: 999. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.automountServiceAccountToken`: Undocumented values path (warning)
- 993 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0041>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0041>)

### [bitnami/haproxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/haproxy>)

Overview cell: 43

Status: unsupported-schema | Attempts: N/A

Audit findings: 186. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 180 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0042>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0042>)

### [bitnami/harbor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/harbor>)

Overview cell: 44

Status: unsupported-schema | Attempts: N/A

Audit findings: 1499. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache.expireHours`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificateVolume.resources`: Undocumented values path (warning)
- 1493 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0043>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0043>)

### [bitnami/influxdb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/influxdb>)

Overview cell: 45

Status: unsupported-schema | Attempts: N/A

Audit findings: 345. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.createAdminToken`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.createAdminToken`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- 339 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0044>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0044>)

### [bitnami/jaeger](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jaeger>)

Overview cell: 46

Status: unsupported-schema | Attempts: N/A

Audit findings: 404. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.cluster`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.cluster.datacenter`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.user`: Undocumented values path (warning)
- 398 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0045>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0045>)

### [bitnami/janusgraph](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/janusgraph>)

Overview cell: 47

Status: unsupported-schema | Attempts: N/A

Audit findings: 328. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- 322 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0046>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0046>)

### [bitnami/jenkins](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jenkins>)

Overview cell: 48

Status: unsupported-schema | Attempts: N/A

Audit findings: 348. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.containerExtraEnvVars`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.containerSecurityContext`: Undocumented values path (warning)
- 342 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0047>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0047>)

### [bitnami/jupyterhub](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jupyterhub>)

Overview cell: 49

Status: unsupported-schema | Attempts: N/A

Audit findings: 625. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.pullPolicy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.pullSecrets`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.registry`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.repository`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.tag`: Undocumented values path (warning)
- 619 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0048>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0048>)

### [bitnami/kafka](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kafka>)

Overview cell: 50

Status: unsupported-schema | Attempts: N/A

Audit findings: 790. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$[""]`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$[""]`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.automountServiceAccountToken`: Undocumented values path (warning)
- 784 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0049>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0049>)

### [bitnami/keycloak](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keycloak>)

Overview cell: 51

Status: unsupported-schema | Attempts: N/A

Audit findings: 448. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminRealm`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminUser`: Undocumented values path (warning)
- 442 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0050>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0050>)

### [bitnami/keydb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keydb>)

Overview cell: 52

Status: unsupported-schema | Attempts: N/A

Audit findings: 499. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 493 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0051>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0051>)

### [bitnami/kibana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kibana>)

Overview cell: 53

Status: unsupported-schema | Attempts: N/A

Audit findings: 257. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 251 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0052>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0052>)

### [bitnami/kong](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kong>)

Overview cell: 54

Status: unsupported-schema | Attempts: N/A

Audit findings: 390. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.metrics`: Undocumented values path (warning)
- 384 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0053>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0053>)

### [bitnami/kube-arangodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-arangodb>)

Overview cell: 55

Status: unsupported-schema | Attempts: N/A

Audit findings: 324. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowChaos`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arangodbImage.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arangodbImage.pullSecrets`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.arangodbImage.pullSecrets`: No supplied default for a values path
  (warning)
- 318 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0054>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0054>)

### [bitnami/kube-prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus>)

Overview cell: 56

Status: unsupported-schema | Attempts: N/A

Audit findings: 1172. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.additionalPeers`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.config`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.config.global`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.config.global.resolve_timeout`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.config.receivers`: Undocumented values path (warning)
- 1166 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0055>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0055>)

### [bitnami/kube-prometheus/charts/kube-prometheus-crds](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus/charts/kube-prometheus-crds>)

Overview cell: 57

Status: unsupported-schema | Attempts: N/A

Audit findings: 1. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.exampleValue`: Undocumented values path (warning)

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0056>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0056>)

### [bitnami/kube-state-metrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-state-metrics>)

Overview cell: 58

Status: unsupported-schema | Attempts: N/A

Audit findings: 208. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- 202 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0057>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0057>)

### [bitnami/kuberay](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kuberay>)

Overview cell: 59

Status: unsupported-schema | Attempts: N/A

Audit findings: 550. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.autoscaling.hpa`: Undocumented values path (warning)
- 544 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0058>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0058>)

### [bitnami/kubernetes-event-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kubernetes-event-exporter>)

Overview cell: 60

Status: unsupported-schema | Attempts: N/A

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.vpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.vpa.annotations`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0059>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0059>)

### [bitnami/logstash](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/logstash>)

Overview cell: 61

Status: unsupported-schema | Attempts: N/A

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0060>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0060>)

### [bitnami/mariadb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb>)

Overview cell: 62

Status: unsupported-schema | Attempts: N/A

Audit findings: 232. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.replicator`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.customPasswordFiles.replicator`: No supplied default for a values
  path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.root`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.customPasswordFiles.root`: No supplied default for a values path
  (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.user`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.customPasswordFiles.user`: No supplied default for a values path
  (warning)
- 226 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0061>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0061>)

### [bitnami/mariadb-galera](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb-galera>)

Overview cell: 63

Status: unsupported-schema | Attempts: N/A

Audit findings: 303. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- 297 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0062>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0062>)

### [bitnami/mastodon](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mastodon>)

Overview cell: 64

Status: unsupported-schema | Attempts: N/A

Audit findings: 752. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.activeRecordEncryptionDeterministicKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.activeRecordEncryptionKeyDerivationSalt`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.activeRecordEncryptionPrimaryKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminUser`: Undocumented values path (warning)
- 746 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0063>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0063>)

### [bitnami/matomo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/matomo>)

Overview cell: 65

Status: unsupported-schema | Attempts: N/A

Audit findings: 357. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.command`: Undocumented values path (warning)
- 351 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0064>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0064>)

### [bitnami/memcached](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/memcached>)

Overview cell: 66

Status: unsupported-schema | Attempts: N/A

Audit findings: 276. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingPasswordSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 270 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0065>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0065>)

### [bitnami/metallb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metallb>)

Overview cell: 67

Status: unsupported-schema | Attempts: N/A

Audit findings: 395. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.configInline`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- 389 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0066>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0066>)

### [bitnami/metrics-server](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metrics-server>)

Overview cell: 68

Status: unsupported-schema | Attempts: N/A

Audit findings: 159. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.caBundle`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.create`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.insecureSkipTLSVerify`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- 153 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0067>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0067>)

### [bitnami/milvus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/milvus>)

Overview cell: 69

Status: unsupported-schema | Attempts: N/A

Audit findings: 716. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.attu.args[*]`: Unspecified values type (warning)
- [HH2003](#hh2003---missing-values-description) at `$.attu.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.attu.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.attu.autoscaling.vpa`: Missing values description (info)
- [HH2002](#hh2002---unspecified-values-type) at `$.attu.autoscaling.vpa.controlledResources[*]`: Unspecified values type (warning)
- 710 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0068>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0068>)

### [bitnami/mlflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mlflow>)

Overview cell: 70

Status: unsupported-schema | Attempts: N/A

Audit findings: 332. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.database`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.database`: No supplied default for a values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode.args[*]`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode.command[*]`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode`: Missing values description (info)
- 326 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0069>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0069>)

### [bitnami/mongodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb>)

Overview cell: 71

Status: unsupported-schema | Attempts: N/A

Audit findings: 794. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.automountServiceAccountToken`: Undocumented values path (warning)
- 788 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0070>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0070>)

### [bitnami/mongodb-sharded](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb-sharded>)

Overview cell: 72

Status: unsupported-schema | Attempts: N/A

Audit findings: 647. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.replicaSetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.rootPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.rootUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFiles`: Undocumented values path (warning)
- 641 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0071>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0071>)

### [bitnami/moodle](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/moodle>)

Overview cell: 73

Status: unsupported-schema | Attempts: N/A

Audit findings: 300. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 294 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0072>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0072>)

### [bitnami/multus-cni](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/multus-cni>)

Overview cell: 74

Status: unsupported-schema | Attempts: N/A

Audit findings: 135. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.CNIMountPath`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.CNIVersion`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 129 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0073>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0073>)

### [bitnami/mysql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mysql>)

Overview cell: 75

Status: unsupported-schema | Attempts: N/A

Audit findings: 512. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.authenticationPolicy`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.auth.createDatabase`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.replicator`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.customPasswordFiles.replicator`: No supplied default for a values
  path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.root`: Undocumented values path (warning)
- 506 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0074>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0074>)

### [bitnami/nats](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nats>)

Overview cell: 76

Status: unsupported-schema | Attempts: N/A

Audit findings: 307. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials[*].password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials[*].user`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- 301 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0075>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0075>)

### [bitnami/neo4j](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/neo4j>)

Overview cell: 77

Status: unsupported-schema | Attempts: N/A

Audit findings: 251. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.advertisedHost`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apocConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- 245 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0076>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0076>)

### [bitnami/nessie](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nessie>)

Overview cell: 78

Status: unsupported-schema | Attempts: N/A

Audit findings: 332. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- 326 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0077>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0077>)

### [bitnami/nginx](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nginx>)

Overview cell: 79

Status: unsupported-schema | Attempts: N/A

Audit findings: 321. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 315 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0078>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0078>)

### [bitnami/node-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/node-exporter>)

Overview cell: 80

Status: unsupported-schema | Attempts: N/A

Audit findings: 180. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 174 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0079>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0079>)

### [bitnami/oauth2-proxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/oauth2-proxy>)

Overview cell: 81

Status: unsupported-schema | Attempts: N/A

Audit findings: 223. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 217 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0080>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0080>)

### [bitnami/odoo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/odoo>)

Overview cell: 82

Status: unsupported-schema | Attempts: N/A

Audit findings: 271. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 265 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0081>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0081>)

### [bitnami/opensearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/opensearch>)

Overview cell: 83

Status: unsupported-schema | Attempts: N/A

Audit findings: 1111. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.config`: Undocumented values path (warning)
- 1105 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0082>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0082>)

### [bitnami/parse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/parse>)

Overview cell: 84

Status: unsupported-schema | Attempts: N/A

Audit findings: 379. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.appName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.automountServiceAccountToken`: Undocumented values path (warning)
- 373 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0083>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0083>)

### [bitnami/phpmyadmin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/phpmyadmin>)

Overview cell: 85

Status: unsupported-schema | Attempts: N/A

Audit findings: 246. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 240 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0084>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0084>)

### [bitnami/pinniped](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pinniped>)

Overview cell: 86

Status: unsupported-schema | Attempts: N/A

Audit findings: 327. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.concierge.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.concierge.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.concierge.automountServiceAccountToken`: Undocumented values path (warning)
- 321 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0085>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0085>)

### [bitnami/postgresql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql>)

Overview cell: 87

Status: unsupported-schema | Attempts: N/A

Audit findings: 674. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.audit.clientMinMessages`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logConnections`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logDisconnections`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logHostname`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logLinePrefix`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logTimezone`: Undocumented values path (warning)
- 668 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0086>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0086>)

### [bitnami/postgresql-ha](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql-ha>)

Overview cell: 88

Status: unsupported-schema | Attempts: N/A

Audit findings: 732. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.concurrencyPolicy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.containerSecurityContext`: Undocumented values path (warning)
- 726 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0087>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0087>)

### [bitnami/prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/prometheus>)

Overview cell: 89

Status: unsupported-schema | Attempts: N/A

Audit findings: 193. Full paths and template references are retained in the JSON report.

- [HH2002](#hh2002---unspecified-values-type) at `$.alertmanager.args[*]`: Unspecified values type (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.alertmanager.command[*]`: Unspecified values type (warning)
- [HH2003](#hh2003---missing-values-description) at `$.alertmanager.containerPorts`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.alertmanager.containerSecurityContext`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.alertmanager.containerSecurityContext.capabilities`: Missing values description
  (info)
- [HH2003](#hh2003---missing-values-description) at `$.alertmanager.containerSecurityContext.capabilities.drop[*]`: Missing values
  description (info)
- 187 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0088>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0088>)

### [bitnami/pytorch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pytorch>)

Overview cell: 90

Status: unsupported-schema | Attempts: N/A

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cloneFilesFromGit.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cloneFilesFromGit.extraVolumeMounts`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0089>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0089>)

### [bitnami/rabbitmq](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq>)

Overview cell: 91

Status: unsupported-schema | Attempts: N/A

Audit findings: 407. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.advancedConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.advancedConfigurationExistingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enableLoopbackUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.erlangCookie`: Undocumented values path (warning)
- 401 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0090>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0090>)

### [bitnami/rabbitmq-cluster-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq-cluster-operator>)

Overview cell: 92

Status: unsupported-schema | Attempts: N/A

Audit findings: 387. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.containerPorts`: Undocumented values path (warning)
- 381 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0091>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0091>)

### [bitnami/redis](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis>)

Overview cell: 93

Status: unsupported-schema | Attempts: N/A

Audit findings: 317. Full paths and template references are retained in the JSON report.

- [HH2003](#hh2003---missing-values-description) at `$.auth.acl`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.acl.sentinel`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.acl.userSecret`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.auth.acl.users[*]`: Unspecified values type (warning)
- [HH2003](#hh2003---missing-values-description) at `$.auth`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.configmapChecksumAnnotations`: Undocumented values path (warning)
- 311 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0092>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0092>)

### [bitnami/redis-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis-cluster>)

Overview cell: 94

Status: unsupported-schema | Attempts: N/A

Audit findings: 371. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.hostMode`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.disableLoadBalancerIP`: Undocumented values path
  (warning)
- 365 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0093>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0093>)

### [bitnami/redmine](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redmine>)

Overview cell: 95

Status: unsupported-schema | Attempts: N/A

Audit findings: 374. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 368 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0094>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0094>)

### [bitnami/schema-registry](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/schema-registry>)

Overview cell: 96

Status: unsupported-schema | Attempts: N/A

Audit findings: 277. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.jksSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.keystorePassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.saslMechanism`: Undocumented values path (warning)
- 271 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0095>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0095>)

### [bitnami/scylladb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/scylladb>)

Overview cell: 97

Status: unsupported-schema | Attempts: N/A

Audit findings: 390. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.annotations`: Undocumented values path (warning)
- 384 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0096>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0096>)

### [bitnami/sealed-secrets](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sealed-secrets>)

Overview cell: 98

Status: unsupported-schema | Attempts: N/A

Audit findings: 213. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.additionalNamespaces`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 207 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0097>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0097>)

### [bitnami/seaweedfs](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/seaweedfs>)

Overview cell: 99

Status: unsupported-schema | Attempts: N/A

Audit findings: 1241. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDefault`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- 1235 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0098>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0098>)

### [bitnami/solr](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/solr>)

Overview cell: 100

Status: unsupported-schema | Attempts: N/A

Audit findings: 411. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminUsername`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- 405 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0099>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0099>)

### [bitnami/sonarqube](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sonarqube>)

Overview cell: 101

Status: unsupported-schema | Attempts: N/A

Audit findings: 419. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 413 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0100>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0100>)

### [bitnami/spark](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/spark>)

Overview cell: 102

Status: unsupported-schema | Attempts: N/A

Audit findings: 350. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 344 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0101>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0101>)

### [bitnami/superset](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/superset>)

Overview cell: 103

Status: unsupported-schema | Attempts: N/A

Audit findings: 752. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.email`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFiles`: Undocumented values path (warning)
- 746 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0102>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0102>)

### [bitnami/tensorflow-resnet](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tensorflow-resnet>)

Overview cell: 104

Status: unsupported-schema | Attempts: N/A

Audit findings: 172. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image.pullPolicy`: Undocumented values path (warning)
- 166 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0103>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0103>)

### [bitnami/thanos](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/thanos>)

Overview cell: 105

Status: unsupported-schema | Attempts: N/A

Audit findings: 1750. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.basicAuthUsers`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketCacheConfig`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.automountServiceAccountToken`: Undocumented values path (warning)
- 1744 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0104>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0104>)

### [bitnami/tomcat](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tomcat>)

Overview cell: 106

Status: unsupported-schema | Attempts: N/A

Audit findings: 266. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.catalinaOpts`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 260 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0105>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0105>)

### [bitnami/valkey](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey>)

Overview cell: 107

Status: unsupported-schema | Attempts: N/A

Audit findings: 686. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.auth.enabled`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.sentinel`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFileFromSecret`: Undocumented values path (warning)
- 680 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0106>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0106>)

### [bitnami/valkey-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey-cluster>)

Overview cell: 108

Status: unsupported-schema | Attempts: N/A

Audit findings: 359. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.hostMode`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.disableLoadBalancerIP`: Undocumented values path
  (warning)
- 353 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0107>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0107>)

### [bitnami/vault](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/vault>)

Overview cell: 109

Status: unsupported-schema | Attempts: N/A

Audit findings: 557. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.agent`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.agent.args`: Undocumented values path (warning)
- 551 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0108>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0108>)

### [bitnami/victoriametrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/victoriametrics>)

Overview cell: 110

Status: unsupported-schema | Attempts: N/A

Audit findings: 1110. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.defaultInitContainers.volumePermissions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.defaultInitContainers.volumePermissions.containerSecurityContext`: Undocumented values
  path (warning)
- 1104 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0109>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0109>)

### [bitnami/whereabouts](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/whereabouts>)

Overview cell: 111

Status: unsupported-schema | Attempts: N/A

Audit findings: 130. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.CNIMountPath`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 124 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0110>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0110>)

### [bitnami/wildfly](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wildfly>)

Overview cell: 112

Status: unsupported-schema | Attempts: N/A

Audit findings: 233. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 227 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0111>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0111>)

### [bitnami/wordpress](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wordpress>)

Overview cell: 113

Status: unsupported-schema | Attempts: N/A

Audit findings: 406. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowOverrideNone`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apacheConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- 400 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0112>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0112>)

### [bitnami/zipkin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zipkin>)

Overview cell: 114

Status: unsupported-schema | Attempts: N/A

Audit findings: 380. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- 374 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0113>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0113>)

### [bitnami/zookeeper](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zookeeper>)

Overview cell: 115

Status: unsupported-schema | Attempts: N/A

Audit findings: 319. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.clientPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.clientUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.enabled`: Undocumented values path (warning)
- 313 additional audit findings in JSON.

#### E001

```text
permutations need closed objects at (); set additionalProperties: false
```

Phase: chart | Status: unsupported-schema

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1790023254/0114>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1790023254/0114>)

## Appendix: finding codes

HH codes identify finding categories. E001-style numbers identify individual diagnostics within this report.
Severities below are defaults; configured overrides are shown with the findings above.

### HH2001 - Undocumented values path

Default severity: **warning** | Category: values | Evidence type: warning

The audit finds a values path with no matching schema declaration.

Suggested action: Document the path in values.schema.json, including its accepted values.

### HH2002 - Unspecified values type

Default severity: **warning** | Category: values | Evidence type: warning

A schema path declares no type, enum or const.

Suggested action: Declare the accepted type or a finite set of values.

### HH2003 - Missing values description

Default severity: **info** | Category: values | Evidence type: warning

A typed schema path has no description.

Suggested action: Describe the field's behavior and any requirements shared with other fields.

### HH2004 - No supplied default for a values path

Default severity: **warning** | Category: values | Evidence type: warning

A discovered path is absent from the original values file.

Suggested action: Supply a default or document when users must provide the field. Render the relevant configurations to check its
requirements.

### HH2006 - Opaque object schema

Default severity: **warning** | Category: values | Evidence type: warning

An object permits unspecified entries without named fields, patterned fields or a typed map-value schema.

Suggested action: Describe fields with properties, patternProperties or typed additionalProperties. Ignore
[HH2006](#hh2006---opaque-object-schema) for intentional free-form configuration; tests still sample those values.
