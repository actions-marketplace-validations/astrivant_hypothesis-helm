# Scan results: github.com/bitnami/charts

<!-- toc:start -->
<details>
<summary>Table of contents</summary>

- [Overview](#overview)
- [Graph structure](#graph-structure)
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
- [Appendix: plot guide](#appendix-plot-guide)
  - [Overview matrices](#overview-matrices)
  - [Chart topology](#chart-topology)
  - [Field interactions](#field-interactions)
  - [Graph structure metrics](#graph-structure-metrics)
- [Appendix: sensitivity field keys](#appendix-sensitivity-field-keys)
  - [bitnami/apache](#bitnamiapache-1)
  - [bitnami/aspnet-core](#bitnamiaspnet-core-1)
  - [bitnami/cadvisor](#bitnamicadvisor-1)
  - [bitnami/cert-manager](#bitnamicert-manager-1)
  - [bitnami/consul](#bitnamiconsul-1)
  - [bitnami/contour](#bitnamicontour-1)
  - [bitnami/elasticsearch](#bitnamielasticsearch-1)
  - [bitnami/envoy-gateway](#bitnamienvoy-gateway-1)
  - [bitnami/external-dns](#bitnamiexternal-dns-1)
  - [bitnami/flink](#bitnamiflink-1)
  - [bitnami/fluent-bit](#bitnamifluent-bit-1)
  - [bitnami/fluentd](#bitnamifluentd-1)
  - [bitnami/flux](#bitnamiflux-1)
  - [bitnami/grafana-alloy](#bitnamigrafana-alloy-1)
  - [bitnami/grafana-k6-operator](#bitnamigrafana-k6-operator-1)
  - [bitnami/grafana-loki](#bitnamigrafana-loki-1)
  - [bitnami/grafana-tempo](#bitnamigrafana-tempo-1)
  - [bitnami/haproxy](#bitnamihaproxy-1)
  - [bitnami/influxdb](#bitnamiinfluxdb-1)
  - [bitnami/kibana](#bitnamikibana-1)
  - [bitnami/kube-state-metrics](#bitnamikube-state-metrics-1)
  - [bitnami/kubernetes-event-exporter](#bitnamikubernetes-event-exporter-1)
  - [bitnami/logstash](#bitnamilogstash-1)
  - [bitnami/mariadb-galera](#bitnamimariadb-galera-1)
  - [bitnami/memcached](#bitnamimemcached-1)
  - [bitnami/metrics-server](#bitnamimetrics-server-1)
  - [bitnami/multus-cni](#bitnamimultus-cni-1)
  - [bitnami/node-exporter](#bitnaminode-exporter-1)
  - [bitnami/opensearch](#bitnamiopensearch-1)
  - [bitnami/phpmyadmin](#bitnamiphpmyadmin-1)
  - [bitnami/prometheus](#bitnamiprometheus-1)
  - [bitnami/pytorch](#bitnamipytorch-1)
  - [bitnami/redis-cluster](#bitnamiredis-cluster-1)
  - [bitnami/sealed-secrets](#bitnamisealed-secrets-1)
  - [bitnami/spark](#bitnamispark-1)
  - [bitnami/tensorflow-resnet](#bitnamitensorflow-resnet-1)
  - [bitnami/valkey-cluster](#bitnamivalkey-cluster-1)
  - [bitnami/vault](#bitnamivault-1)
  - [bitnami/victoriametrics](#bitnamivictoriametrics-1)
  - [bitnami/whereabouts](#bitnamiwhereabouts-1)
  - [bitnami/wildfly](#bitnamiwildfly-1)
  - [bitnami/zookeeper](#bitnamizookeeper-1)
- [Appendix: finding codes](#appendix-finding-codes)
  - [HH1101 - Invalid YAML in rendered output](#hh1101---invalid-yaml-in-rendered-output)
  - [HH1105 - Missing resource name](#hh1105---missing-resource-name)
  - [HH1107 - Empty resource bundle](#hh1107---empty-resource-bundle)
  - [HH1108 - Kubernetes schema validation failed](#hh1108---kubernetes-schema-validation-failed)
  - [HH1109 - Invalid manifest field type](#hh1109---invalid-manifest-field-type)
  - [HH2001 - Undocumented values path](#hh2001---undocumented-values-path)
  - [HH2002 - Unspecified values type](#hh2002---unspecified-values-type)
  - [HH2003 - Missing values description](#hh2003---missing-values-description)
  - [HH2004 - No supplied default for a values path](#hh2004---no-supplied-default-for-a-values-path)
  - [HH2006 - Opaque object schema](#hh2006---opaque-object-schema)
  - [HH3001 - Template accesses a missing object](#hh3001---template-accesses-a-missing-object)

</details>
<!-- toc:end -->

## Overview

![Chart severity and scan-time matrices](<bitnami-overview.png>)

Each cell is one chart; both grids follow chart-section order. Click a cell in the PDF for details. Colors show the highest observed finding
kind, not a security or business-impact score. Hatching marks unfinished or unavailable testing, even when a finding was recorded. No
findings means none in the completed sample, not exhaustive coverage. Testing time excludes dependency preparation. Plot guide:
[Overview matrices](#overview-matrices).

## Graph structure

![Published compiler graph invariants](<bitnami-topology.png>)

Published graph measurements are available for 115 of 115 report charts. Vertices represent inputs, conditions, templates and manifest
fields; edges connect them. The right panel counts independent loops after ignoring edge direction; C is the number of disconnected groups.
Parallel edges count separately. These are structural measurements from the published chart diagrams, not bug counts. Plot guide:
[Graph structure metrics](#graph-structure-metrics).

## Scan summary

Git comparison unavailable; no charts skipped using previous test results.

Directory: /Users/emmadoyle/projects/personal/hypothesis-helm/third_party/bitnami-charts
Started (Unix epoch): 1790039844
Started (UTC): 2026-09-22T01:17:24.000+00:00
Finished (UTC): 2026-09-22T03:55:21.600+00:00
Run fingerprint (SHA-256): `b00a713d4f1271b6a08ecb68952fc23253daf7344f5ac0c4e4ed86ab175cca77`
Versions: Hypothesis not recorded; hypothesis-helm not recorded
Elapsed (wall clock): 9418.10 seconds
Chart testing: 8615.48 seconds
Dependency preparation: 790.53 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: completed
Discovery complete: True
Unstarted charts: 0

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

93 time-limit; 18 failed; 1 skipped-library; 3 error.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 60.0 seconds | Workers: 6
Complete settings are retained in the JSON report.

Scan command: Not recorded for this run

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: [HH2006](#hh2006---opaque-object-schema)

## Errors

34 distinct diagnostics across 39 occurrences; 5 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### [bitnami/airflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/airflow>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/airflow](<../../studies/chart-topologies/bitnami/airflow/topology.png>) | ![Sensitivity: bitnami/airflow](<../../studies/chart-topologies/bitnami/airflow/sensitivity.png>) |

Overview cell: 01

Status: time-limit | Attempts: 5

Audit findings: 1190. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.fernetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in JSON.

### [bitnami/apache](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apache>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/apache](<../../studies/chart-topologies/bitnami/apache/topology.png>) | ![Sensitivity: bitnami/apache](<../../studies/chart-topologies/bitnami/apache/sensitivity.png>) |

[Sensitivity field key](#bitnamiapache-1).

Overview cell: 02

Status: failed | Attempts: 24

Audit findings: 245. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 239 additional audit findings in JSON.

#### E015 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... ity': None, 'podAntiAffinity': {'preferredDuringSchedulingIgnoredDuringExecution':
[{'podAffinityTerm': {'labelSelector': {'matchLabels': {'app.kubernetes.io/instance': 'hypothesis', 'app.kubernetes.io/name': 'apache'}},
'topologyKey': 'kubernetes.io/hostname'}, 'weight': 1}]}, 'nodeAffinity': None}") in "<unicode string>", line 265, column 7: affinity: ^
(line: 265) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[*].preference | Status: failed

Changed overrides (used together):
- `$.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution.__hypothesis_key__.preference = {}`
Absent from overrides: $.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution["*"].preference. Defaults may
still apply.

Renderer random inputs (replay tape in artifacts):

### [bitnami/apisix](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apisix>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/apisix](<../../studies/chart-topologies/bitnami/apisix/topology.png>) | ![Sensitivity: bitnami/apisix](<../../studies/chart-topologies/bitnami/apisix/sensitivity.png>) |

Overview cell: 03

Status: time-limit | Attempts: 5

Audit findings: 344. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.controlPlane.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controlPlane.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.vpa`: Missing values description (info)
- 338 additional audit findings in JSON.

### [bitnami/appsmith](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/appsmith>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/appsmith](<../../studies/chart-topologies/bitnami/appsmith/topology.png>) | ![Sensitivity: bitnami/appsmith](<../../studies/chart-topologies/bitnami/appsmith/sensitivity.png>) |

Overview cell: 04

Status: time-limit | Attempts: 3

Audit findings: 543. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.automountServiceAccountToken`: Undocumented values path (warning)
- 537 additional audit findings in JSON.

### [bitnami/argo-cd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-cd>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/argo-cd](<../../studies/chart-topologies/bitnami/argo-cd/topology.png>) | ![Sensitivity: bitnami/argo-cd](<../../studies/chart-topologies/bitnami/argo-cd/sensitivity.png>) |

Overview cell: 05

Status: time-limit | Attempts: 2

Audit findings: 1251. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterAdminAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterRoleRules`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.containerPorts`: Undocumented values path (warning)
- 1245 additional audit findings in JSON.

### [bitnami/argo-workflows](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-workflows>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/argo-workflows](<../../studies/chart-topologies/bitnami/argo-workflows/topology.png>) | ![Sensitivity: bitnami/argo-workflows](<../../studies/chart-topologies/bitnami/argo-workflows/sensitivity.png>) |

Overview cell: 06

Status: time-limit | Attempts: 4

Audit findings: 452. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.automountServiceAccountToken`: Undocumented values path (warning)
- 446 additional audit findings in JSON.

### [bitnami/aspnet-core](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/aspnet-core>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/aspnet-core](<../../studies/chart-topologies/bitnami/aspnet-core/topology.png>) | ![Sensitivity: bitnami/aspnet-core](<../../studies/chart-topologies/bitnami/aspnet-core/sensitivity.png>) |

[Sensitivity field key](#bitnamiaspnet-core-1).

Overview cell: 07

Status: time-limit | Attempts: 13

Audit findings: 224. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.existingClaim`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone.depth`: Undocumented values path (warning)
- 218 additional audit findings in JSON.

### [bitnami/cadvisor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cadvisor>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cadvisor](<../../studies/chart-topologies/bitnami/cadvisor/topology.png>) | ![Sensitivity: bitnami/cadvisor](<../../studies/chart-topologies/bitnami/cadvisor/sensitivity.png>) |

[Sensitivity field key](#bitnamicadvisor-1).

Overview cell: 08

Status: time-limit | Attempts: 21

Audit findings: 192. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.clusterDomain`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 186 additional audit findings in JSON.

### [bitnami/cassandra](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cassandra>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cassandra](<../../studies/chart-topologies/bitnami/cassandra/topology.png>) | ![Sensitivity: bitnami/cassandra](<../../studies/chart-topologies/bitnami/cassandra/sensitivity.png>) |

Overview cell: 09

Status: time-limit | Attempts: 13

Audit findings: 309. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.clientEncryption`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.datacenter`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.enableUDF`: Undocumented values path (warning)
- 303 additional audit findings in JSON.

### [bitnami/cert-manager](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cert-manager>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cert-manager](<../../studies/chart-topologies/bitnami/cert-manager/topology.png>) | ![Sensitivity: bitnami/cert-manager](<../../studies/chart-topologies/bitnami/cert-manager/sensitivity.png>) |

[Sensitivity field key](#bitnamicert-manager-1).

Overview cell: 10

Status: time-limit | Attempts: 1

Audit findings: 404. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.containerSecurityContext`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.containerSecurityContext.allowPrivilegeEscalation`: Undocumented values path
  (warning)
- 398 additional audit findings in JSON.

### [bitnami/chainloop](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/chainloop>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/chainloop](<../../studies/chart-topologies/bitnami/chainloop/topology.png>) | ![Sensitivity: bitnami/chainloop](<../../studies/chart-topologies/bitnami/chainloop/sensitivity.png>) |

Overview cell: 11

Status: time-limit | Attempts: 7

Audit findings: 643. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 637 additional audit findings in JSON.

### [bitnami/cilium](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cilium>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cilium](<../../studies/chart-topologies/bitnami/cilium/topology.png>) | ![Sensitivity: bitnami/cilium](<../../studies/chart-topologies/bitnami/cilium/sensitivity.png>) |

Overview cell: 12

Status: time-limit | Attempts: 1

Audit findings: 1163. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.agent.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling.vpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling.vpa.annotations`: Undocumented values path (warning)
- 1157 additional audit findings in JSON.

### [bitnami/clickhouse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/clickhouse](<../../studies/chart-topologies/bitnami/clickhouse/topology.png>) | ![Sensitivity: bitnami/clickhouse](<../../studies/chart-topologies/bitnami/clickhouse/sensitivity.png>) |

Overview cell: 13

Status: time-limit | Attempts: 5

Audit findings: 507. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 501 additional audit findings in JSON.

### [bitnami/clickhouse-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse-operator>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/clickhouse-operator](<../../studies/chart-topologies/bitnami/clickhouse-operator/topology.png>) | ![Sensitivity: bitnami/clickhouse-operator](<../../studies/chart-topologies/bitnami/clickhouse-operator/sensitivity.png>) |

Overview cell: 14

Status: time-limit | Attempts: 13

Audit findings: 276. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.username`: Undocumented values path (warning)
- 270 additional audit findings in JSON.

### [bitnami/cloudnative-pg](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cloudnative-pg>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cloudnative-pg](<../../studies/chart-topologies/bitnami/cloudnative-pg/topology.png>) | ![Sensitivity: bitnami/cloudnative-pg](<../../studies/chart-topologies/bitnami/cloudnative-pg/sensitivity.png>) |

Overview cell: 15

Status: time-limit | Attempts: 43

Audit findings: 423. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.extraDeploy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.fullnameOverride`: Undocumented values path (warning)
- 417 additional audit findings in JSON.

### [bitnami/common](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/common>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/common](<../../studies/chart-topologies/bitnami/common/topology.png>) | ![Sensitivity: bitnami/common](<../../studies/chart-topologies/bitnami/common/sensitivity.png>) |

Overview cell: 16

Status: skipped-library | Attempts: N/A

### [bitnami/concourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/concourse>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/concourse](<../../studies/chart-topologies/bitnami/concourse/topology.png>) | ![Sensitivity: bitnami/concourse](<../../studies/chart-topologies/bitnami/concourse/sensitivity.png>) |

Overview cell: 17

Status: time-limit | Attempts: 11

Audit findings: 470. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 464 additional audit findings in JSON.

### [bitnami/consul](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/consul>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/consul](<../../studies/chart-topologies/bitnami/consul/topology.png>) | ![Sensitivity: bitnami/consul](<../../studies/chart-topologies/bitnami/consul/sensitivity.png>) |

[Sensitivity field key](#bitnamiconsul-1).

Overview cell: 18

Status: time-limit | Attempts: 1

Audit findings: 255. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 249 additional audit findings in JSON.

### [bitnami/contour](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/contour>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/contour](<../../studies/chart-topologies/bitnami/contour/topology.png>) | ![Sensitivity: bitnami/contour](<../../studies/chart-topologies/bitnami/contour/sensitivity.png>) |

[Sensitivity field key](#bitnamicontour-1).

Overview cell: 19

Status: time-limit | Attempts: 21

Audit findings: 591. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline["accesslog-format"]`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.disablePermitInsecure`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.tls`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.tls["fallback-certificate"]`: Undocumented values path (warning)
- 585 additional audit findings in JSON.

### [bitnami/deepspeed](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/deepspeed>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/deepspeed](<../../studies/chart-topologies/bitnami/deepspeed/topology.png>) | ![Sensitivity: bitnami/deepspeed](<../../studies/chart-topologies/bitnami/deepspeed/sensitivity.png>) |

Overview cell: 20

Status: time-limit | Attempts: 1

Audit findings: 166. Full paths and template references are retained in the JSON report.

- [HH2002](#hh2002---unspecified-values-type) at `$.client.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.client.persistence.mountPath`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.client.client.persistence.mountPath`: No supplied default for a values
  path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.client.command[*]`: Unspecified values type (warning)
- [HH2003](#hh2003---missing-values-description) at `$.client.containerSecurityContext`: Missing values description (info)
- 160 additional audit findings in JSON.

### [bitnami/discourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/discourse>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/discourse](<../../studies/chart-topologies/bitnami/discourse/topology.png>) | ![Sensitivity: bitnami/discourse](<../../studies/chart-topologies/bitnami/discourse/sensitivity.png>) |

Overview cell: 21

Status: error | Attempts: N/A

#### E032

```text
Path worker exited with status 1; see
/Users/emmadoyle/projects/personal/hypothesis-helm/docs/reports/bitnami-runs/bitnami-charts_1790039844/0020/path-workers-j061t2vq/queue
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

### [bitnami/dremio](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/dremio>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/dremio](<../../studies/chart-topologies/bitnami/dremio/topology.png>) | ![Sensitivity: bitnami/dremio](<../../studies/chart-topologies/bitnami/dremio/sensitivity.png>) |

Overview cell: 22

Status: error | Attempts: N/A

#### E033

```text
Path worker exited with status 1; see
/Users/emmadoyle/projects/personal/hypothesis-helm/docs/reports/bitnami-runs/bitnami-charts_1790039844/0021/path-workers-_7l15_nd/queue
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

### [bitnami/drupal](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/drupal>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/drupal](<../../studies/chart-topologies/bitnami/drupal/topology.png>) | ![Sensitivity: bitnami/drupal](<../../studies/chart-topologies/bitnami/drupal/sensitivity.png>) |

Overview cell: 23

Status: error | Attempts: N/A

#### E034

```text
Path worker exited with status 1; see
/Users/emmadoyle/projects/personal/hypothesis-helm/docs/reports/bitnami-runs/bitnami-charts_1790039844/0022/path-workers-fuy59jh1/queue
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

### [bitnami/ejbca](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ejbca>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/ejbca](<../../studies/chart-topologies/bitnami/ejbca/topology.png>) | ![Sensitivity: bitnami/ejbca](<../../studies/chart-topologies/bitnami/ejbca/sensitivity.png>) |

Overview cell: 24

Status: time-limit | Attempts: 21

Audit findings: 224. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- 218 additional audit findings in JSON.

### [bitnami/elasticsearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/elasticsearch>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/elasticsearch](<../../studies/chart-topologies/bitnami/elasticsearch/topology.png>) | ![Sensitivity: bitnami/elasticsearch](<../../studies/chart-topologies/bitnami/elasticsearch/sensitivity.png>) |

[Sensitivity field key](#bitnamielasticsearch-1).

Overview cell: 25

Status: time-limit | Attempts: 11

Audit findings: 814. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.config`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.containerPorts.restAPI`: Undocumented values path (warning)
- 808 additional audit findings in JSON.

### [bitnami/envoy-gateway](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/envoy-gateway>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/envoy-gateway](<../../studies/chart-topologies/bitnami/envoy-gateway/topology.png>) | ![Sensitivity: bitnami/envoy-gateway](<../../studies/chart-topologies/bitnami/envoy-gateway/sensitivity.png>) |

[Sensitivity field key](#bitnamienvoy-gateway-1).

Overview cell: 26

Status: failed | Attempts: 33

Audit findings: 325. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 319 additional audit findings in JSON.

#### E023 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.certgen.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.certgen.serviceAccount.name = "0" (was "")`

Renderer random inputs (replay tape in artifacts):

Manifest changes from rendered defaults (document and list order preserved):
- `$[11].spec.template.spec.serviceAccountName: "hypothesis-envoy-gateway-certgen" -> 0`
- `$[2].metadata.name: "hypothesis-envoy-gateway-certgen" -> 0`
- `$[5].subjects[0].name: "hypothesis-envoy-gateway-certgen" -> 0`
- `$[8].subjects[0].name: "hypothesis-envoy-gateway-certgen" -> 0`
- `$[9].subjects[0].name: "hypothesis-envoy-gateway-certgen" -> 0`

### [bitnami/etcd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/etcd>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/etcd](<../../studies/chart-topologies/bitnami/etcd/topology.png>) | ![Sensitivity: bitnami/etcd](<../../studies/chart-topologies/bitnami/etcd/sensitivity.png>) |

Overview cell: 27

Status: time-limit | Attempts: 13

Audit findings: 407. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.caFilename`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.certFilename`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.certKeyFilename`: Undocumented values path (warning)
- 401 additional audit findings in JSON.

### [bitnami/external-dns](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/external-dns>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/external-dns](<../../studies/chart-topologies/bitnami/external-dns/topology.png>) | ![Sensitivity: bitnami/external-dns](<../../studies/chart-topologies/bitnami/external-dns/sensitivity.png>) |

[Sensitivity field key](#bitnamiexternal-dns-1).

Overview cell: 28

Status: failed | Attempts: 659

Audit findings: 402. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.accessToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.clientSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.clientToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.host`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.secretName`: Undocumented values path (warning)
- 396 additional audit findings in JSON.

Configuration rejections: 0 excluded; 2 adjusted and tested; 2 Helm verification renders (separate from manifest-test attempts).

#### E004 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 28: did not find expected ','
or ']'
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.digest = "0" (was "")`
- `$.image.registry = "" (was "docker.io")`
- `$.image["0000000000"] = null`
- `$.image.repository = "" (was "bitnami/external-dns")`
- `$.image.pullSecrets = [[[{}, 6.2841568821697656e+16, {}]], [], {"aaaaaaaaZ": [], "": {"aXaaaagaa$kaaaa;a": {}, "aaaaza": false}}, {}, {"a;aaaa... [value shortened]`
- `$.image["(@%8_$!"]["("] = -333`
- 7 more paths; see full input.

Renderer random inputs (replay tape in artifacts):

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

Renderer random inputs (replay tape in artifacts):

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E005 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 67: could not find expected
':'
```

Phase: $.zoneIdFilters[*] | Status: failed

Changed overrides (used together):
- `$.zoneIdFilters = [[{"\r": null}]]`
Absent from overrides: $.zoneIdFilters["*"]. Defaults may still apply.

Renderer random inputs (replay tape in artifacts):

Phase: $.regexDomainExclusion | Status: failed

Changed overrides (used together):
- `$.regexDomainExclusion = "\n0" (was "")`

Renderer random inputs (replay tape in artifacts):

#### E006 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 71: could not find expected
':'
```

Phase: $.aws.zoneTags | Status: failed

Changed overrides (used together):
- `$.aws.zoneTags = [{"aa-,a)": null, "ha": {"aa2": 1.0914998582626766e+16, "aaaaQaacaaaa\raa.aaal,aaa>ialaaa": null, "a9aaVbaaaaaa\na": tru... [value shortened]`

Renderer random inputs (replay tape in artifacts):

### [bitnami/flink](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flink>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/flink](<../../studies/chart-topologies/bitnami/flink/topology.png>) | ![Sensitivity: bitnami/flink](<../../studies/chart-topologies/bitnami/flink/sensitivity.png>) |

[Sensitivity field key](#bitnamiflink-1).

Overview cell: 29

Status: time-limit | Attempts: 11

Audit findings: 281. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 275 additional audit findings in JSON.

### [bitnami/fluent-bit](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluent-bit>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/fluent-bit](<../../studies/chart-topologies/bitnami/fluent-bit/topology.png>) | ![Sensitivity: bitnami/fluent-bit](<../../studies/chart-topologies/bitnami/fluent-bit/sensitivity.png>) |

[Sensitivity field key](#bitnamifluent-bit-1).

Overview cell: 30

Status: time-limit | Attempts: 1

Audit findings: 240. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.annotations`: Undocumented values path (warning)
- 234 additional audit findings in JSON.

### [bitnami/fluentd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluentd>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/fluentd](<../../studies/chart-topologies/bitnami/fluentd/topology.png>) | ![Sensitivity: bitnami/fluentd](<../../studies/chart-topologies/bitnami/fluentd/sensitivity.png>) |

[Sensitivity field key](#bitnamifluentd-1).

Overview cell: 31

Status: time-limit | Attempts: 31

Audit findings: 427. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.aggregator.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.autoscaling`: Undocumented values path (warning)
- 421 additional audit findings in JSON.

### [bitnami/flux](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flux>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/flux](<../../studies/chart-topologies/bitnami/flux/topology.png>) | ![Sensitivity: bitnami/flux](<../../studies/chart-topologies/bitnami/flux/sensitivity.png>) |

[Sensitivity field key](#bitnamiflux-1).

Overview cell: 32

Status: time-limit | Attempts: 3

Audit findings: 1042. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 1036 additional audit findings in JSON.

### [bitnami/ghost](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ghost>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/ghost](<../../studies/chart-topologies/bitnami/ghost/topology.png>) | ![Sensitivity: bitnami/ghost](<../../studies/chart-topologies/bitnami/ghost/sensitivity.png>) |

Overview cell: 33

Status: failed | Attempts: 86

Audit findings: 262. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 256 additional audit findings in JSON.

#### E019 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... ath': 'app-tmp-dir'}, {'name': 'empty-dir', 'mountPath': '/opt/bitnami/mysql/logs',
'subPath': 'app-logs-dir'}, {'name': 'config', 'mountPath': '/opt/bitnami/mysql/conf/my.cnf', 'subPath': 'my.cnf'}, {'name':
'mysql-credentials', 'mountPath': '/opt/bitnami/mysql/secrets/'}]}]" (original value: "[]") in "<unicode string>", line 412, column 7:
containers: ^ (line: 412) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.mysql.primary.extraPodSpec.containers | Status: failed

Changed overrides (used together):
- `$.mysql.primary.extraPodSpec.containers = []`

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

#### E020 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... gs', 'subPath': 'app-logs-dir'}, {'name': 'config', 'mountPath':
'/opt/bitnami/mysql/conf/my.cnf', 'subPath': 'my.cnf'}, {'name': 'mysql-credentials', 'mountPath': '/opt/bitnami/mysql/secrets/'}]}]"
(original value: "{'__hypothesis_key__': {'lifecycle': {'postStart': {'exec': {'command': None}}}}}") in "<unicode string>", line 417,
column 7: containers: ^ (line: 417) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.mysql.primary.extraPodSpec.containers[*].lifecycle.postStart.exec.command | Status: failed

Changed overrides (used together):
- `$.mysql.primary.extraPodSpec.containers.__hypothesis_key__.lifecycle.postStart.exec.command = null`
Absent from overrides: $.mysql.primary.extraPodSpec.containers["*"].lifecycle.postStart.exec.command. Defaults may still apply.

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

#### E021 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... ting a mapping in "<unicode string>", line 349, column 7: securityContext: ^ (line: 349)
found duplicate key "securityContext" with value "{'fsGroup': 1001, 'fsGroupChangePolicy': 'Always', 'supplementalGroups': [], 'sysctls':
[]}" (original value: "{'windowsOptions': {'runAsUserName': None}}") in "<unicode string>", line 369, column 7: securityContext: ^ (line:
369) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.mysql.primary.extraPodSpec.securityContext.windowsOptions.runAsUserName | Status: failed

Changed overrides (used together):
- `$.mysql.primary.extraPodSpec.securityContext.windowsOptions.runAsUserName = null`

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

#### E022 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... is-mysql', 'items': [{'key': 'mysql-root-password', 'path': 'mysql-root-password'},
{'key': 'mysql-password', 'path': 'mysql-password'}]}}, {'name': 'empty-dir', 'emptyDir': {}}]" (original value: "{'__hypothesis_key__':
{'projected': {'sources': {'__hypothesis_key__': {'secret': {'items': None}}}}}}") in "<unicode string>", line 530, column 7: volumes: ^
(line: 530) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.mysql.primary.extraPodSpec.volumes[*].projected.sources[*].secret.items | Status: failed

Changed overrides (used together):
- `$.mysql.primary.extraPodSpec.volumes.__hypothesis_key__.projected.sources.__hypothesis_key__.secret.items = null`
Absent from overrides: $.mysql.primary.extraPodSpec.volumes["*"].projected.sources["*"].secret.items. Defaults may still apply.

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

#### E030 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: ghost/charts/mysql/templates/networkpolicy.yaml:72:69 executing "ghost/charts/mysql/templates/networkpolicy.yaml" at
<$value.port>: nil pointer evaluating interface {}.port
```

Phase: $.mysql.primary.service.extraPorts | Status: failed

Changed overrides (used together):
- `$.mysql.primary.service.extraPorts = [null]`

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

### [bitnami/gitea](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitea>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/gitea](<../../studies/chart-topologies/bitnami/gitea/topology.png>) | ![Sensitivity: bitnami/gitea](<../../studies/chart-topologies/bitnami/gitea/sensitivity.png>) |

Overview cell: 34

Status: time-limit | Attempts: 33

Audit findings: 241. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminUsername`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- 235 additional audit findings in JSON.

### [bitnami/gitlab-runner](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitlab-runner>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/gitlab-runner](<../../studies/chart-topologies/bitnami/gitlab-runner/topology.png>) | ![Sensitivity: bitnami/gitlab-runner](<../../studies/chart-topologies/bitnami/gitlab-runner/sensitivity.png>) |

Overview cell: 35

Status: time-limit | Attempts: 33

Audit findings: 266. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 260 additional audit findings in JSON.

### [bitnami/grafana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana](<../../studies/chart-topologies/bitnami/grafana/topology.png>) | ![Sensitivity: bitnami/grafana](<../../studies/chart-topologies/bitnami/grafana/sensitivity.png>) |

Overview cell: 36

Status: time-limit | Attempts: 23

Audit findings: 306. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.admin.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.user`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alerting.configMapName`: Undocumented values path (warning)
- 300 additional audit findings in JSON.

### [bitnami/grafana-alloy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-alloy>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-alloy](<../../studies/chart-topologies/bitnami/grafana-alloy/topology.png>) | ![Sensitivity: bitnami/grafana-alloy](<../../studies/chart-topologies/bitnami/grafana-alloy/sensitivity.png>) |

[Sensitivity field key](#bitnamigrafana-alloy-1).

Overview cell: 37

Status: time-limit | Attempts: 13

Audit findings: 292. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.name`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.portName`: Undocumented values path (warning)
- 286 additional audit findings in JSON.

### [bitnami/grafana-k6-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-k6-operator>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-k6-operator](<../../studies/chart-topologies/bitnami/grafana-k6-operator/topology.png>) | ![Sensitivity: bitnami/grafana-k6-operator](<../../studies/chart-topologies/bitnami/grafana-k6-operator/sensitivity.png>) |

[Sensitivity field key](#bitnamigrafana-k6-operator-1).

Overview cell: 38

Status: time-limit | Attempts: 13

Audit findings: 195. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 189 additional audit findings in JSON.

### [bitnami/grafana-loki](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-loki>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-loki](<../../studies/chart-topologies/bitnami/grafana-loki/topology.png>) | ![Sensitivity: bitnami/grafana-loki](<../../studies/chart-topologies/bitnami/grafana-loki/sensitivity.png>) |

[Sensitivity field key](#bitnamigrafana-loki-1).

Overview cell: 39

Status: time-limit | Attempts: 1

Audit findings: 1386. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.automountServiceAccountToken`: Undocumented values path (warning)
- 1380 additional audit findings in JSON.

### [bitnami/grafana-mimir](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-mimir>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-mimir](<../../studies/chart-topologies/bitnami/grafana-mimir/topology.png>) | ![Sensitivity: bitnami/grafana-mimir](<../../studies/chart-topologies/bitnami/grafana-mimir/sensitivity.png>) |

Overview cell: 40

Status: time-limit | Attempts: 1

Audit findings: 1540. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage.backend`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage.config`: Undocumented values path (warning)
- 1534 additional audit findings in JSON.

### [bitnami/grafana-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-operator>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-operator](<../../studies/chart-topologies/bitnami/grafana-operator/topology.png>) | ![Sensitivity: bitnami/grafana-operator](<../../studies/chart-topologies/bitnami/grafana-operator/sensitivity.png>) |

Overview cell: 41

Status: failed | Attempts: 1

Audit findings: 277. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.extraDeploy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.fullnameOverride`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.global.compatibility`: Undocumented values path (warning)
- 271 additional audit findings in JSON.

#### E026 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource grafana.integreatly.org/v1beta1/Grafana requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

### [bitnami/grafana-tempo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-tempo>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-tempo](<../../studies/chart-topologies/bitnami/grafana-tempo/topology.png>) | ![Sensitivity: bitnami/grafana-tempo](<../../studies/chart-topologies/bitnami/grafana-tempo/sensitivity.png>) |

[Sensitivity field key](#bitnamigrafana-tempo-1).

Overview cell: 42

Status: time-limit | Attempts: 5

Audit findings: 999. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.automountServiceAccountToken`: Undocumented values path (warning)
- 993 additional audit findings in JSON.

### [bitnami/haproxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/haproxy>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/haproxy](<../../studies/chart-topologies/bitnami/haproxy/topology.png>) | ![Sensitivity: bitnami/haproxy](<../../studies/chart-topologies/bitnami/haproxy/sensitivity.png>) |

[Sensitivity field key](#bitnamihaproxy-1).

Overview cell: 43

Status: time-limit | Attempts: 13

Audit findings: 186. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 180 additional audit findings in JSON.

### [bitnami/harbor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/harbor>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/harbor](<../../studies/chart-topologies/bitnami/harbor/topology.png>) | ![Sensitivity: bitnami/harbor](<../../studies/chart-topologies/bitnami/harbor/sensitivity.png>) |

Overview cell: 44

Status: time-limit | Attempts: 2

Audit findings: 1499. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache.expireHours`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificateVolume.resources`: Undocumented values path (warning)
- 1493 additional audit findings in JSON.

### [bitnami/influxdb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/influxdb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/influxdb](<../../studies/chart-topologies/bitnami/influxdb/topology.png>) | ![Sensitivity: bitnami/influxdb](<../../studies/chart-topologies/bitnami/influxdb/sensitivity.png>) |

[Sensitivity field key](#bitnamiinfluxdb-1).

Overview cell: 45

Status: failed | Attempts: 425

Audit findings: 345. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.createAdminToken`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.createAdminToken`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- 339 additional audit findings in JSON.

Configuration rejections: 0 excluded; 14 adjusted and tested; 14 Helm verification renders (separate from manifest-test attempts).

#### E007 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on influxdb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 36: did not find expected ',' or
']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

Renderer random inputs (replay tape in artifacts):

#### E008 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on influxdb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: did not find expected node
content
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.t1g = null`
- `$.image.pullSecrets = [[]]`
- `$.image.pullPolicy = "aUaI" (was "IfNotPresent")`
- `$.image.registry = "," (was "docker.io")`
- `$.image.approximation = false`
- 11 more paths; see full input.

Renderer random inputs (replay tape in artifacts):

### [bitnami/jaeger](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jaeger>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/jaeger](<../../studies/chart-topologies/bitnami/jaeger/topology.png>) | ![Sensitivity: bitnami/jaeger](<../../studies/chart-topologies/bitnami/jaeger/sensitivity.png>) |

Overview cell: 46

Status: time-limit | Attempts: 11

Audit findings: 404. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.cluster`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.cluster.datacenter`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.user`: Undocumented values path (warning)
- 398 additional audit findings in JSON.

### [bitnami/janusgraph](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/janusgraph>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/janusgraph](<../../studies/chart-topologies/bitnami/janusgraph/topology.png>) | ![Sensitivity: bitnami/janusgraph](<../../studies/chart-topologies/bitnami/janusgraph/sensitivity.png>) |

Overview cell: 47

Status: time-limit | Attempts: 31

Audit findings: 328. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- 322 additional audit findings in JSON.

### [bitnami/jenkins](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jenkins>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/jenkins](<../../studies/chart-topologies/bitnami/jenkins/topology.png>) | ![Sensitivity: bitnami/jenkins](<../../studies/chart-topologies/bitnami/jenkins/sensitivity.png>) |

Overview cell: 48

Status: time-limit | Attempts: 13

Audit findings: 348. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.containerExtraEnvVars`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.containerSecurityContext`: Undocumented values path (warning)
- 342 additional audit findings in JSON.

### [bitnami/jupyterhub](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jupyterhub>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/jupyterhub](<../../studies/chart-topologies/bitnami/jupyterhub/topology.png>) | ![Sensitivity: bitnami/jupyterhub](<../../studies/chart-topologies/bitnami/jupyterhub/sensitivity.png>) |

Overview cell: 49

Status: time-limit | Attempts: 21

Audit findings: 625. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.pullPolicy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.pullSecrets`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.registry`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.repository`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.tag`: Undocumented values path (warning)
- 619 additional audit findings in JSON.

### [bitnami/kafka](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kafka>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kafka](<../../studies/chart-topologies/bitnami/kafka/topology.png>) | ![Sensitivity: bitnami/kafka](<../../studies/chart-topologies/bitnami/kafka/sensitivity.png>) |

Overview cell: 50

Status: time-limit | Attempts: 9

Audit findings: 790. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$[""]`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$[""]`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.automountServiceAccountToken`: Undocumented values path (warning)
- 784 additional audit findings in JSON.

### [bitnami/keycloak](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keycloak>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/keycloak](<../../studies/chart-topologies/bitnami/keycloak/topology.png>) | ![Sensitivity: bitnami/keycloak](<../../studies/chart-topologies/bitnami/keycloak/sensitivity.png>) |

Overview cell: 51

Status: time-limit | Attempts: 26

Audit findings: 448. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminRealm`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminUser`: Undocumented values path (warning)
- 442 additional audit findings in JSON.

### [bitnami/keydb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keydb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/keydb](<../../studies/chart-topologies/bitnami/keydb/topology.png>) | ![Sensitivity: bitnami/keydb](<../../studies/chart-topologies/bitnami/keydb/sensitivity.png>) |

Overview cell: 52

Status: time-limit | Attempts: 11

Audit findings: 499. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 493 additional audit findings in JSON.

### [bitnami/kibana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kibana>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kibana](<../../studies/chart-topologies/bitnami/kibana/topology.png>) | ![Sensitivity: bitnami/kibana](<../../studies/chart-topologies/bitnami/kibana/sensitivity.png>) |

[Sensitivity field key](#bitnamikibana-1).

Overview cell: 53

Status: time-limit | Attempts: 33

Audit findings: 257. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 251 additional audit findings in JSON.

### [bitnami/kong](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kong>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kong](<../../studies/chart-topologies/bitnami/kong/topology.png>) | ![Sensitivity: bitnami/kong](<../../studies/chart-topologies/bitnami/kong/sensitivity.png>) |

Overview cell: 54

Status: time-limit | Attempts: 28

Audit findings: 390. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.metrics`: Undocumented values path (warning)
- 384 additional audit findings in JSON.

### [bitnami/kube-arangodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-arangodb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kube-arangodb](<../../studies/chart-topologies/bitnami/kube-arangodb/topology.png>) | ![Sensitivity: bitnami/kube-arangodb](<../../studies/chart-topologies/bitnami/kube-arangodb/sensitivity.png>) |

Overview cell: 55

Status: time-limit | Attempts: 23

Audit findings: 324. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowChaos`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arangodbImage.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arangodbImage.pullSecrets`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.arangodbImage.pullSecrets`: No supplied default for a values path
  (warning)
- 318 additional audit findings in JSON.

### [bitnami/kube-prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kube-prometheus](<../../studies/chart-topologies/bitnami/kube-prometheus/topology.png>) | ![Sensitivity: bitnami/kube-prometheus](<../../studies/chart-topologies/bitnami/kube-prometheus/sensitivity.png>) |

Overview cell: 56

Status: failed | Attempts: 1

Audit findings: 1172. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.additionalPeers`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.config`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.config.global`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.config.global.resolve_timeout`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.config.receivers`: Undocumented values path (warning)
- 1166 additional audit findings in JSON.

#### E027 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.coreos.com/v1/Alertmanager requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

### [bitnami/kube-prometheus/charts/kube-prometheus-crds](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus/charts/kube-prometheus-crds>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kube-prometheus/charts/kube-prometheus-crds](<../../studies/chart-topologies/bitnami/kube-prometheus/charts/kube-prometheus-crds/topology.png>) | ![Sensitivity: bitnami/kube-prometheus/charts/kube-prometheus-crds](<../../studies/chart-topologies/bitnami/kube-prometheus/charts/kube-prometheus-crds/sensitivity.png>) |

Overview cell: 57

Status: failed | Attempts: 1

Audit findings: 1. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.exampleValue`: Undocumented values path (warning)

#### E024 ([HH1107](#hh1107---empty-resource-bundle))

**Empty resource bundle** (manifest / violation). Severity: **error**. Check resource activation; ignore this contract if an empty chart is
intentional.

```text
[HH1107] chart rendered no resources
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

### [bitnami/kube-state-metrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-state-metrics>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kube-state-metrics](<../../studies/chart-topologies/bitnami/kube-state-metrics/topology.png>) | ![Sensitivity: bitnami/kube-state-metrics](<../../studies/chart-topologies/bitnami/kube-state-metrics/sensitivity.png>) |

[Sensitivity field key](#bitnamikube-state-metrics-1).

Overview cell: 58

Status: time-limit | Attempts: 13

Audit findings: 208. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- 202 additional audit findings in JSON.

### [bitnami/kuberay](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kuberay>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kuberay](<../../studies/chart-topologies/bitnami/kuberay/topology.png>) | ![Sensitivity: bitnami/kuberay](<../../studies/chart-topologies/bitnami/kuberay/sensitivity.png>) |

Overview cell: 59

Status: failed | Attempts: 1

Audit findings: 550. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiserver.autoscaling.hpa`: Undocumented values path (warning)
- 544 additional audit findings in JSON.

#### E028 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource ray.io/v1/RayCluster requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

### [bitnami/kubernetes-event-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kubernetes-event-exporter>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kubernetes-event-exporter](<../../studies/chart-topologies/bitnami/kubernetes-event-exporter/topology.png>) | ![Sensitivity: bitnami/kubernetes-event-exporter](<../../studies/chart-topologies/bitnami/kubernetes-event-exporter/sensitivity.png>) |

[Sensitivity field key](#bitnamikubernetes-event-exporter-1).

Overview cell: 60

Status: time-limit | Attempts: 33

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.vpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.vpa.annotations`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

### [bitnami/logstash](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/logstash>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/logstash](<../../studies/chart-topologies/bitnami/logstash/topology.png>) | ![Sensitivity: bitnami/logstash](<../../studies/chart-topologies/bitnami/logstash/sensitivity.png>) |

[Sensitivity field key](#bitnamilogstash-1).

Overview cell: 61

Status: time-limit | Attempts: 13

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

### [bitnami/mariadb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mariadb](<../../studies/chart-topologies/bitnami/mariadb/topology.png>) | ![Sensitivity: bitnami/mariadb](<../../studies/chart-topologies/bitnami/mariadb/sensitivity.png>) |

Overview cell: 62

Status: time-limit | Attempts: 21

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

### [bitnami/mariadb-galera](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb-galera>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mariadb-galera](<../../studies/chart-topologies/bitnami/mariadb-galera/topology.png>) | ![Sensitivity: bitnami/mariadb-galera](<../../studies/chart-topologies/bitnami/mariadb-galera/sensitivity.png>) |

[Sensitivity field key](#bitnamimariadb-galera-1).

Overview cell: 63

Status: time-limit | Attempts: 31

Audit findings: 303. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- 297 additional audit findings in JSON.

### [bitnami/mastodon](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mastodon>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mastodon](<../../studies/chart-topologies/bitnami/mastodon/topology.png>) | ![Sensitivity: bitnami/mastodon](<../../studies/chart-topologies/bitnami/mastodon/sensitivity.png>) |

Overview cell: 64

Status: time-limit | Attempts: 1

Audit findings: 752. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.activeRecordEncryptionDeterministicKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.activeRecordEncryptionKeyDerivationSalt`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.activeRecordEncryptionPrimaryKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminUser`: Undocumented values path (warning)
- 746 additional audit findings in JSON.

### [bitnami/matomo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/matomo>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/matomo](<../../studies/chart-topologies/bitnami/matomo/topology.png>) | ![Sensitivity: bitnami/matomo](<../../studies/chart-topologies/bitnami/matomo/sensitivity.png>) |

Overview cell: 65

Status: time-limit | Attempts: 16

Audit findings: 357. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.command`: Undocumented values path (warning)
- 351 additional audit findings in JSON.

### [bitnami/memcached](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/memcached>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/memcached](<../../studies/chart-topologies/bitnami/memcached/topology.png>) | ![Sensitivity: bitnami/memcached](<../../studies/chart-topologies/bitnami/memcached/sensitivity.png>) |

[Sensitivity field key](#bitnamimemcached-1).

Overview cell: 66

Status: time-limit | Attempts: 23

Audit findings: 276. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingPasswordSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 270 additional audit findings in JSON.

### [bitnami/metallb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metallb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/metallb](<../../studies/chart-topologies/bitnami/metallb/topology.png>) | ![Sensitivity: bitnami/metallb](<../../studies/chart-topologies/bitnami/metallb/sensitivity.png>) |

Overview cell: 67

Status: time-limit | Attempts: 65

Audit findings: 395. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.configInline`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- 389 additional audit findings in JSON.

### [bitnami/metrics-server](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metrics-server>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/metrics-server](<../../studies/chart-topologies/bitnami/metrics-server/topology.png>) | ![Sensitivity: bitnami/metrics-server](<../../studies/chart-topologies/bitnami/metrics-server/sensitivity.png>) |

[Sensitivity field key](#bitnamimetrics-server-1).

Overview cell: 68

Status: time-limit | Attempts: 13

Audit findings: 159. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.caBundle`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.create`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.insecureSkipTLSVerify`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- 153 additional audit findings in JSON.

### [bitnami/milvus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/milvus>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/milvus](<../../studies/chart-topologies/bitnami/milvus/topology.png>) | ![Sensitivity: bitnami/milvus](<../../studies/chart-topologies/bitnami/milvus/sensitivity.png>) |

Overview cell: 69

Status: time-limit | Attempts: 1

Audit findings: 716. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.attu.args[*]`: Unspecified values type (warning)
- [HH2003](#hh2003---missing-values-description) at `$.attu.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.attu.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.attu.autoscaling.vpa`: Missing values description (info)
- [HH2002](#hh2002---unspecified-values-type) at `$.attu.autoscaling.vpa.controlledResources[*]`: Unspecified values type (warning)
- 710 additional audit findings in JSON.

### [bitnami/mlflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mlflow>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mlflow](<../../studies/chart-topologies/bitnami/mlflow/topology.png>) | ![Sensitivity: bitnami/mlflow](<../../studies/chart-topologies/bitnami/mlflow/sensitivity.png>) |

Overview cell: 70

Status: time-limit | Attempts: 8

Audit findings: 332. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.database`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.database`: No supplied default for a values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode.args[*]`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode.command[*]`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode`: Missing values description (info)
- 326 additional audit findings in JSON.

### [bitnami/mongodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mongodb](<../../studies/chart-topologies/bitnami/mongodb/topology.png>) | ![Sensitivity: bitnami/mongodb](<../../studies/chart-topologies/bitnami/mongodb/sensitivity.png>) |

Overview cell: 71

Status: time-limit | Attempts: 41

Audit findings: 794. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.automountServiceAccountToken`: Undocumented values path (warning)
- 788 additional audit findings in JSON.

### [bitnami/mongodb-sharded](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb-sharded>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mongodb-sharded](<../../studies/chart-topologies/bitnami/mongodb-sharded/topology.png>) | ![Sensitivity: bitnami/mongodb-sharded](<../../studies/chart-topologies/bitnami/mongodb-sharded/sensitivity.png>) |

Overview cell: 72

Status: time-limit | Attempts: 11

Audit findings: 647. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.replicaSetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.rootPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.rootUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFiles`: Undocumented values path (warning)
- 641 additional audit findings in JSON.

### [bitnami/moodle](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/moodle>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/moodle](<../../studies/chart-topologies/bitnami/moodle/topology.png>) | ![Sensitivity: bitnami/moodle](<../../studies/chart-topologies/bitnami/moodle/sensitivity.png>) |

Overview cell: 73

Status: time-limit | Attempts: 33

Audit findings: 300. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 294 additional audit findings in JSON.

### [bitnami/multus-cni](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/multus-cni>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/multus-cni](<../../studies/chart-topologies/bitnami/multus-cni/topology.png>) | ![Sensitivity: bitnami/multus-cni](<../../studies/chart-topologies/bitnami/multus-cni/sensitivity.png>) |

[Sensitivity field key](#bitnamimultus-cni-1).

Overview cell: 74

Status: time-limit | Attempts: 13

Audit findings: 135. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.CNIMountPath`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.CNIVersion`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 129 additional audit findings in JSON.

### [bitnami/mysql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mysql>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mysql](<../../studies/chart-topologies/bitnami/mysql/topology.png>) | ![Sensitivity: bitnami/mysql](<../../studies/chart-topologies/bitnami/mysql/sensitivity.png>) |

Overview cell: 75

Status: failed | Attempts: 44

Audit findings: 512. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.authenticationPolicy`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.auth.createDatabase`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.replicator`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.customPasswordFiles.replicator`: No supplied default for a values
  path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.root`: Undocumented values path (warning)
- 506 additional audit findings in JSON.

#### E018 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... ', 'subPath': 'app-logs-dir'}, {'name': 'config', 'mountPath':
'/opt/bitnami/mysql/conf/my.cnf', 'subPath': 'my.cnf'}, {'name': 'mysql-credentials', 'mountPath': '/opt/bitnami/mysql/secrets/'}]}]"
(original value: "{'__hypothesis_key__': {'volumeMounts': {'__hypothesis_key__': {'subPath': None}}}}") in "<unicode string>", line 305,
column 7: containers: ^ (line: 305) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.primary.extraPodSpec.containers[*].volumeMounts[*].subPath | Status: failed

Changed overrides (used together):
- `$.primary.extraPodSpec.containers.__hypothesis_key__.volumeMounts.__hypothesis_key__.subPath = null`
Absent from overrides: $.primary.extraPodSpec.containers["*"].volumeMounts["*"].subPath. Defaults may still apply.

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

### [bitnami/nats](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nats>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/nats](<../../studies/chart-topologies/bitnami/nats/topology.png>) | ![Sensitivity: bitnami/nats](<../../studies/chart-topologies/bitnami/nats/sensitivity.png>) |

Overview cell: 76

Status: time-limit | Attempts: 23

Audit findings: 307. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials[*].password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials[*].user`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- 301 additional audit findings in JSON.

### [bitnami/neo4j](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/neo4j>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/neo4j](<../../studies/chart-topologies/bitnami/neo4j/topology.png>) | ![Sensitivity: bitnami/neo4j](<../../studies/chart-topologies/bitnami/neo4j/sensitivity.png>) |

Overview cell: 77

Status: time-limit | Attempts: 127

Audit findings: 251. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.advertisedHost`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apocConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- 245 additional audit findings in JSON.

Configuration rejections: 0 excluded; 1 adjusted and tested; 1 Helm verification renders (separate from manifest-test attempts).

### [bitnami/nessie](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nessie>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/nessie](<../../studies/chart-topologies/bitnami/nessie/topology.png>) | ![Sensitivity: bitnami/nessie](<../../studies/chart-topologies/bitnami/nessie/sensitivity.png>) |

Overview cell: 78

Status: time-limit | Attempts: 33

Audit findings: 332. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- 326 additional audit findings in JSON.

### [bitnami/nginx](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nginx>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/nginx](<../../studies/chart-topologies/bitnami/nginx/topology.png>) | ![Sensitivity: bitnami/nginx](<../../studies/chart-topologies/bitnami/nginx/sensitivity.png>) |

Overview cell: 79

Status: time-limit | Attempts: 23

Audit findings: 321. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 315 additional audit findings in JSON.

### [bitnami/node-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/node-exporter>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/node-exporter](<../../studies/chart-topologies/bitnami/node-exporter/topology.png>) | ![Sensitivity: bitnami/node-exporter](<../../studies/chart-topologies/bitnami/node-exporter/sensitivity.png>) |

[Sensitivity field key](#bitnaminode-exporter-1).

Overview cell: 80

Status: time-limit | Attempts: 13

Audit findings: 180. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 174 additional audit findings in JSON.

### [bitnami/oauth2-proxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/oauth2-proxy>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/oauth2-proxy](<../../studies/chart-topologies/bitnami/oauth2-proxy/topology.png>) | ![Sensitivity: bitnami/oauth2-proxy](<../../studies/chart-topologies/bitnami/oauth2-proxy/sensitivity.png>) |

Overview cell: 81

Status: time-limit | Attempts: 33

Audit findings: 223. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 217 additional audit findings in JSON.

### [bitnami/odoo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/odoo>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/odoo](<../../studies/chart-topologies/bitnami/odoo/topology.png>) | ![Sensitivity: bitnami/odoo](<../../studies/chart-topologies/bitnami/odoo/sensitivity.png>) |

Overview cell: 82

Status: time-limit | Attempts: 1

Audit findings: 271. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 265 additional audit findings in JSON.

### [bitnami/opensearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/opensearch>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/opensearch](<../../studies/chart-topologies/bitnami/opensearch/topology.png>) | ![Sensitivity: bitnami/opensearch](<../../studies/chart-topologies/bitnami/opensearch/sensitivity.png>) |

[Sensitivity field key](#bitnamiopensearch-1).

Overview cell: 83

Status: time-limit | Attempts: 93

Audit findings: 1111. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.config`: Undocumented values path (warning)
- 1105 additional audit findings in JSON.

### [bitnami/parse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/parse>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/parse](<../../studies/chart-topologies/bitnami/parse/topology.png>) | ![Sensitivity: bitnami/parse](<../../studies/chart-topologies/bitnami/parse/sensitivity.png>) |

Overview cell: 84

Status: time-limit | Attempts: 1

Audit findings: 379. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.appName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.automountServiceAccountToken`: Undocumented values path (warning)
- 373 additional audit findings in JSON.

### [bitnami/phpmyadmin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/phpmyadmin>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/phpmyadmin](<../../studies/chart-topologies/bitnami/phpmyadmin/topology.png>) | ![Sensitivity: bitnami/phpmyadmin](<../../studies/chart-topologies/bitnami/phpmyadmin/sensitivity.png>) |

[Sensitivity field key](#bitnamiphpmyadmin-1).

Overview cell: 85

Status: time-limit | Attempts: 37

Audit findings: 246. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 240 additional audit findings in JSON.

### [bitnami/pinniped](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pinniped>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/pinniped](<../../studies/chart-topologies/bitnami/pinniped/topology.png>) | ![Sensitivity: bitnami/pinniped](<../../studies/chart-topologies/bitnami/pinniped/sensitivity.png>) |

Overview cell: 86

Status: failed | Attempts: 1

Audit findings: 327. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.concierge.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.concierge.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.concierge.automountServiceAccountToken`: Undocumented values path (warning)
- 321 additional audit findings in JSON.

#### E025 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource config.concierge.pinniped.dev/v1alpha1/CredentialIssuer requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

### [bitnami/postgresql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/postgresql](<../../studies/chart-topologies/bitnami/postgresql/topology.png>) | ![Sensitivity: bitnami/postgresql](<../../studies/chart-topologies/bitnami/postgresql/sensitivity.png>) |

Overview cell: 87

Status: failed | Attempts: 78

Audit findings: 674. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.audit.clientMinMessages`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logConnections`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logDisconnections`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logHostname`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logLinePrefix`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logTimezone`: Undocumented values path (warning)
- 668 additional audit findings in JSON.

#### E001 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 190: found
unexpected end of stream
```

Phase: $.primary.existingConfigmap | Status: failed

Changed overrides (used together):
- `$.primary.existingConfigmap = "'" (was "")`

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

### [bitnami/postgresql-ha](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql-ha>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/postgresql-ha](<../../studies/chart-topologies/bitnami/postgresql-ha/topology.png>) | ![Sensitivity: bitnami/postgresql-ha](<../../studies/chart-topologies/bitnami/postgresql-ha/sensitivity.png>) |

Overview cell: 88

Status: time-limit | Attempts: 10

Audit findings: 732. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.concurrencyPolicy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.containerSecurityContext`: Undocumented values path (warning)
- 726 additional audit findings in JSON.

### [bitnami/prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/prometheus>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/prometheus](<../../studies/chart-topologies/bitnami/prometheus/topology.png>) | ![Sensitivity: bitnami/prometheus](<../../studies/chart-topologies/bitnami/prometheus/sensitivity.png>) |

[Sensitivity field key](#bitnamiprometheus-1).

Overview cell: 89

Status: time-limit | Attempts: 1

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

### [bitnami/pytorch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pytorch>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/pytorch](<../../studies/chart-topologies/bitnami/pytorch/topology.png>) | ![Sensitivity: bitnami/pytorch](<../../studies/chart-topologies/bitnami/pytorch/sensitivity.png>) |

[Sensitivity field key](#bitnamipytorch-1).

Overview cell: 90

Status: failed | Attempts: 310

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cloneFilesFromGit.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cloneFilesFromGit.extraVolumeMounts`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

Configuration rejections: 0 excluded; 19 adjusted and tested; 19 Helm verification renders (separate from manifest-test attempts).

#### E009 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 32: did not find expected ',' or
']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

Renderer random inputs (replay tape in artifacts):

#### E010 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 57: found character that cannot
start any token
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.digest = "0" (was "")`
- `$.image.registry = "" (was "docker.io")`
- `$.image.repository = "" (was "bitnami/pytorch")`

Renderer random inputs (replay tape in artifacts):

### [bitnami/rabbitmq](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/rabbitmq](<../../studies/chart-topologies/bitnami/rabbitmq/topology.png>) | ![Sensitivity: bitnami/rabbitmq](<../../studies/chart-topologies/bitnami/rabbitmq/sensitivity.png>) |

Overview cell: 91

Status: time-limit | Attempts: 13

Audit findings: 407. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.advancedConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.advancedConfigurationExistingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enableLoopbackUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.erlangCookie`: Undocumented values path (warning)
- 401 additional audit findings in JSON.

### [bitnami/rabbitmq-cluster-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq-cluster-operator>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/rabbitmq-cluster-operator](<../../studies/chart-topologies/bitnami/rabbitmq-cluster-operator/topology.png>) | ![Sensitivity: bitnami/rabbitmq-cluster-operator](<../../studies/chart-topologies/bitnami/rabbitmq-cluster-operator/sensitivity.png>) |

Overview cell: 92

Status: failed | Attempts: 20

Audit findings: 387. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.containerPorts`: Undocumented values path (warning)
- 381 additional audit findings in JSON.

#### E029 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on rabbitmq-cluster-operator/templates/cluster-operator/service-account.yaml: error unmarshaling JSON:
while decoding JSON: json: cannot unmarshal object into Go struct field .metadata.annotations."2a}#^aZ[7 of type string
```

Phase: $.clusterOperator.serviceAccount | Status: failed

Changed overrides (used together):
- `$.clusterOperator.serviceAccount.annotations.http = null`
- `$.clusterOperator.serviceAccount.annotations.E = 1307674368000`
- `$.clusterOperator.serviceAccount.annotations["I("].a = ["aaE"]`
- `$.clusterOperator.serviceAccount.annotations["I("].ajaaBaaz = []`
- `$.clusterOperator.serviceAccount.annotations["I("].aaaa = {}`
- `$.clusterOperator.serviceAccount.annotations["\"2a}#^aZ[7"]["aa\raa"].g4aa = [4.363245697574542e-147, null, true]`
- 5 more paths; see full input.

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: genCA

### [bitnami/redis](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/redis](<../../studies/chart-topologies/bitnami/redis/topology.png>) | ![Sensitivity: bitnami/redis](<../../studies/chart-topologies/bitnami/redis/sensitivity.png>) |

Overview cell: 93

Status: failed | Attempts: 316

Audit findings: 317. Full paths and template references are retained in the JSON report.

- [HH2003](#hh2003---missing-values-description) at `$.auth.acl`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.acl.sentinel`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.acl.userSecret`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.auth.acl.users[*]`: Unspecified values type (warning)
- [HH2003](#hh2003---missing-values-description) at `$.auth`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.configmapChecksumAnnotations`: Undocumented values path (warning)
- 311 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E002 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 172: could not find
expected ':'
```

Phase: $.master.extraVolumes | Status: failed

Changed overrides (used together):
- `$.master.extraVolumes = "0" (was [])`

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

#### E003 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 66: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image["JaaoUQ+c}\"p"] = null`
- `$.image[""] = null`
- ``$.image.pullPolicy = "L`" (was "IfNotPresent")``
- `$.image["6"] = [null]`
- `$.image.tag = "" (was "8.2.1-debian-12-r0")`

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

#### E031 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: redis/templates/replicas/application.yaml:49:38 executing "redis/templates/replicas/application.yaml" at <include (print
$.Template.BasePath "/configmap.yaml") .>: error calling include: redis/templates/configmap.yaml:61:25 executing
"redis/templates/configmap.yaml" at <.password>: nil pointer evaluating interface {}.password
```

Phase: $.auth.acl | Status: failed

Changed overrides (used together):
- `$.auth.acl.enabled = true (was false)`
- `$.auth.acl.users = [null]`

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

### [bitnami/redis-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis-cluster>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/redis-cluster](<../../studies/chart-topologies/bitnami/redis-cluster/topology.png>) | ![Sensitivity: bitnami/redis-cluster](<../../studies/chart-topologies/bitnami/redis-cluster/sensitivity.png>) |

[Sensitivity field key](#bitnamiredis-cluster-1).

Overview cell: 94

Status: time-limit | Attempts: 21

Audit findings: 371. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.hostMode`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.disableLoadBalancerIP`: Undocumented values path
  (warning)
- 365 additional audit findings in JSON.

### [bitnami/redmine](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redmine>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/redmine](<../../studies/chart-topologies/bitnami/redmine/topology.png>) | ![Sensitivity: bitnami/redmine](<../../studies/chart-topologies/bitnami/redmine/sensitivity.png>) |

Overview cell: 95

Status: time-limit | Attempts: 18

Audit findings: 374. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 368 additional audit findings in JSON.

### [bitnami/schema-registry](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/schema-registry>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/schema-registry](<../../studies/chart-topologies/bitnami/schema-registry/topology.png>) | ![Sensitivity: bitnami/schema-registry](<../../studies/chart-topologies/bitnami/schema-registry/sensitivity.png>) |

Overview cell: 96

Status: time-limit | Attempts: 11

Audit findings: 277. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.jksSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.keystorePassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.saslMechanism`: Undocumented values path (warning)
- 271 additional audit findings in JSON.

### [bitnami/scylladb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/scylladb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/scylladb](<../../studies/chart-topologies/bitnami/scylladb/topology.png>) | ![Sensitivity: bitnami/scylladb](<../../studies/chart-topologies/bitnami/scylladb/sensitivity.png>) |

Overview cell: 97

Status: time-limit | Attempts: 13

Audit findings: 390. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.annotations`: Undocumented values path (warning)
- 384 additional audit findings in JSON.

### [bitnami/sealed-secrets](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sealed-secrets>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/sealed-secrets](<../../studies/chart-topologies/bitnami/sealed-secrets/topology.png>) | ![Sensitivity: bitnami/sealed-secrets](<../../studies/chart-topologies/bitnami/sealed-secrets/sensitivity.png>) |

[Sensitivity field key](#bitnamisealed-secrets-1).

Overview cell: 98

Status: failed | Attempts: 377

Audit findings: 213. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.additionalNamespaces`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 207 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E011 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on sealed-secrets/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

Renderer random inputs (replay tape in artifacts):

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

Renderer random inputs (replay tape in artifacts):

#### E012 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on sealed-secrets/templates/deployment.yaml: error converting YAML to JSON: yaml: line 52: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "0.31.0-debian-12-r0")`

Renderer random inputs (replay tape in artifacts):

#### E013 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] YAML parse error on sealed-secrets/templates/deployment.yaml: error converting YAML to JSON: yaml: line 69: did not find expected
key
```

Phase: $.image.pullSecrets[*] | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = ["\""]`
Absent from overrides: $.image.pullSecrets["*"]. Defaults may still apply.

Renderer random inputs (replay tape in artifacts):

### [bitnami/seaweedfs](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/seaweedfs>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/seaweedfs](<../../studies/chart-topologies/bitnami/seaweedfs/topology.png>) | ![Sensitivity: bitnami/seaweedfs](<../../studies/chart-topologies/bitnami/seaweedfs/sensitivity.png>) |

Overview cell: 99

Status: time-limit | Attempts: 2

Audit findings: 1241. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDefault`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- 1235 additional audit findings in JSON.

### [bitnami/solr](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/solr>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/solr](<../../studies/chart-topologies/bitnami/solr/topology.png>) | ![Sensitivity: bitnami/solr](<../../studies/chart-topologies/bitnami/solr/sensitivity.png>) |

Overview cell: 100

Status: time-limit | Attempts: 30

Audit findings: 411. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminUsername`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- 405 additional audit findings in JSON.

### [bitnami/sonarqube](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sonarqube>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/sonarqube](<../../studies/chart-topologies/bitnami/sonarqube/topology.png>) | ![Sensitivity: bitnami/sonarqube](<../../studies/chart-topologies/bitnami/sonarqube/sensitivity.png>) |

Overview cell: 101

Status: time-limit | Attempts: 33

Audit findings: 419. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 413 additional audit findings in JSON.

### [bitnami/spark](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/spark>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/spark](<../../studies/chart-topologies/bitnami/spark/topology.png>) | ![Sensitivity: bitnami/spark](<../../studies/chart-topologies/bitnami/spark/sensitivity.png>) |

[Sensitivity field key](#bitnamispark-1).

Overview cell: 102

Status: time-limit | Attempts: 83

Audit findings: 350. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 344 additional audit findings in JSON.

### [bitnami/superset](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/superset>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/superset](<../../studies/chart-topologies/bitnami/superset/topology.png>) | ![Sensitivity: bitnami/superset](<../../studies/chart-topologies/bitnami/superset/sensitivity.png>) |

Overview cell: 103

Status: time-limit | Attempts: 7

Audit findings: 752. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.email`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFiles`: Undocumented values path (warning)
- 746 additional audit findings in JSON.

### [bitnami/tensorflow-resnet](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tensorflow-resnet>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/tensorflow-resnet](<../../studies/chart-topologies/bitnami/tensorflow-resnet/topology.png>) | ![Sensitivity: bitnami/tensorflow-resnet](<../../studies/chart-topologies/bitnami/tensorflow-resnet/sensitivity.png>) |

[Sensitivity field key](#bitnamitensorflow-resnet-1).

Overview cell: 104

Status: time-limit | Attempts: 23

Audit findings: 172. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image.pullPolicy`: Undocumented values path (warning)
- 166 additional audit findings in JSON.

### [bitnami/thanos](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/thanos>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/thanos](<../../studies/chart-topologies/bitnami/thanos/topology.png>) | ![Sensitivity: bitnami/thanos](<../../studies/chart-topologies/bitnami/thanos/sensitivity.png>) |

Overview cell: 105

Status: time-limit | Attempts: 43

Audit findings: 1750. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.basicAuthUsers`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketCacheConfig`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.automountServiceAccountToken`: Undocumented values path (warning)
- 1744 additional audit findings in JSON.

### [bitnami/tomcat](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tomcat>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/tomcat](<../../studies/chart-topologies/bitnami/tomcat/topology.png>) | ![Sensitivity: bitnami/tomcat](<../../studies/chart-topologies/bitnami/tomcat/sensitivity.png>) |

Overview cell: 106

Status: failed | Attempts: 19

Audit findings: 266. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.catalinaOpts`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 260 additional audit findings in JSON.

#### E016 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... ity': None, 'podAntiAffinity': {'preferredDuringSchedulingIgnoredDuringExecution':
[{'podAffinityTerm': {'labelSelector': {'matchLabels': {'app.kubernetes.io/instance': 'hypothesis', 'app.kubernetes.io/name': 'tomcat'}},
'topologyKey': 'kubernetes.io/hostname'}, 'weight': 1}]}, 'nodeAffinity': None}") in "<unicode string>", line 266, column 7: affinity: ^
(line: 266) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[*].preference | Status: failed

Changed overrides (used together):
- `$.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution.__hypothesis_key__.preference = {}`
Absent from overrides: $.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution["*"].preference. Defaults may
still apply.

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

#### E017 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] invalid rendered YAML: ruamel: while constructing a mapping in "<unicode string>", line 156, column 7:
automountServiceAccountToken: false ^ (line: 156) found duplicate key "initContainers" with value "{'__hypothesis_key__': {'envFrom':
{'__hypothesis_key__': {'configMapRef': {'name': None}}}}}" (original value: "None") in "<unicode string>", line 266, column 7:
initContainers: ^ (line: 266) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.extraPodSpec.initContainers[*].envFrom[*].configMapRef.name | Status: failed

Changed overrides (used together):
- `$.extraPodSpec.initContainers.__hypothesis_key__.envFrom.__hypothesis_key__.configMapRef.name = null`
Absent from overrides: $.extraPodSpec.initContainers["*"].envFrom["*"].configMapRef.name. Defaults may still apply.

Native renderer fallback; exact random replay unavailable: controlled renderer does not support native effect: lookup

### [bitnami/valkey](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/valkey](<../../studies/chart-topologies/bitnami/valkey/topology.png>) | ![Sensitivity: bitnami/valkey](<../../studies/chart-topologies/bitnami/valkey/sensitivity.png>) |

Overview cell: 107

Status: time-limit | Attempts: 31

Audit findings: 686. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.auth.enabled`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.sentinel`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFileFromSecret`: Undocumented values path (warning)
- 680 additional audit findings in JSON.

### [bitnami/valkey-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey-cluster>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/valkey-cluster](<../../studies/chart-topologies/bitnami/valkey-cluster/topology.png>) | ![Sensitivity: bitnami/valkey-cluster](<../../studies/chart-topologies/bitnami/valkey-cluster/sensitivity.png>) |

[Sensitivity field key](#bitnamivalkey-cluster-1).

Overview cell: 108

Status: time-limit | Attempts: 41

Audit findings: 359. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.hostMode`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.disableLoadBalancerIP`: Undocumented values path
  (warning)
- 353 additional audit findings in JSON.

### [bitnami/vault](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/vault>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/vault](<../../studies/chart-topologies/bitnami/vault/topology.png>) | ![Sensitivity: bitnami/vault](<../../studies/chart-topologies/bitnami/vault/sensitivity.png>) |

[Sensitivity field key](#bitnamivault-1).

Overview cell: 109

Status: time-limit | Attempts: 1

Audit findings: 557. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.agent`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.agent.args`: Undocumented values path (warning)
- 551 additional audit findings in JSON.

### [bitnami/victoriametrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/victoriametrics>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/victoriametrics](<../../studies/chart-topologies/bitnami/victoriametrics/topology.png>) | ![Sensitivity: bitnami/victoriametrics](<../../studies/chart-topologies/bitnami/victoriametrics/sensitivity.png>) |

[Sensitivity field key](#bitnamivictoriametrics-1).

Overview cell: 110

Status: time-limit | Attempts: 8

Audit findings: 1110. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.defaultInitContainers.volumePermissions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.defaultInitContainers.volumePermissions.containerSecurityContext`: Undocumented values
  path (warning)
- 1104 additional audit findings in JSON.

### [bitnami/whereabouts](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/whereabouts>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/whereabouts](<../../studies/chart-topologies/bitnami/whereabouts/topology.png>) | ![Sensitivity: bitnami/whereabouts](<../../studies/chart-topologies/bitnami/whereabouts/sensitivity.png>) |

[Sensitivity field key](#bitnamiwhereabouts-1).

Overview cell: 111

Status: time-limit | Attempts: 11

Audit findings: 130. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.CNIMountPath`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 124 additional audit findings in JSON.

### [bitnami/wildfly](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wildfly>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/wildfly](<../../studies/chart-topologies/bitnami/wildfly/topology.png>) | ![Sensitivity: bitnami/wildfly](<../../studies/chart-topologies/bitnami/wildfly/sensitivity.png>) |

[Sensitivity field key](#bitnamiwildfly-1).

Overview cell: 112

Status: time-limit | Attempts: 31

Audit findings: 233. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 227 additional audit findings in JSON.

### [bitnami/wordpress](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wordpress>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/wordpress](<../../studies/chart-topologies/bitnami/wordpress/topology.png>) | ![Sensitivity: bitnami/wordpress](<../../studies/chart-topologies/bitnami/wordpress/sensitivity.png>) |

Overview cell: 113

Status: time-limit | Attempts: 24

Audit findings: 406. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowOverrideNone`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apacheConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- 400 additional audit findings in JSON.

### [bitnami/zipkin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zipkin>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/zipkin](<../../studies/chart-topologies/bitnami/zipkin/topology.png>) | ![Sensitivity: bitnami/zipkin](<../../studies/chart-topologies/bitnami/zipkin/sensitivity.png>) |

Overview cell: 114

Status: failed | Attempts: 1

Audit findings: 380. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- 374 additional audit findings in JSON.

#### E014 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] invalid rendered YAML: ruamel: more indented follow up line than first in a block scalar in "<unicode string>", line 474, column
15: set -o errexit ^ (line: 474)
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

### [bitnami/zookeeper](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zookeeper>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/zookeeper](<../../studies/chart-topologies/bitnami/zookeeper/topology.png>) | ![Sensitivity: bitnami/zookeeper](<../../studies/chart-topologies/bitnami/zookeeper/sensitivity.png>) |

[Sensitivity field key](#bitnamizookeeper-1).

Overview cell: 115

Status: time-limit | Attempts: 43

Audit findings: 319. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.clientPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.clientUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.enabled`: Undocumented values path (warning)
- 313 additional audit findings in JSON.

## Appendix: plot guide

### Overview matrices

Each numbered cell links to one chart. The left matrix shows findings or test status; the right shows recorded testing time. A dash means no
timing was recorded. Incomplete and untested charts have not passed.

### Chart topology

Vertices represent values paths, branch conditions, templates and manifest fields. Connections show the relationships the compiler could
establish between them. Rendered fields, when available, describe the measured baseline. An absent connection does not prove independence
when analysis is incomplete.

### Field interactions

Both axes use the field numbers in the chart's sensitivity appendix entry, linked from its plot caption. Each measured cell compares
changing two fields together with changing each separately from the same baseline. Manifests are encoded as path-and-value indicators,
including empty containers. The color measures the sum of absolute differences in f(ij) - f(i) - f(j) + f(0). A larger value means a
stronger interaction for those particular changes; zero means no interaction was measured. Blank cells are unmeasured, not zero. These
measurements describe sampled changes, not all possible field values or bug counts.

### Graph structure metrics

Each point represents one chart with published graph measurements. The left panel compares vertices with connections. The right counts
independent loops after ignoring connection direction: connections minus vertices plus disconnected groups. Parallel connections count
separately. The axes compress large values while retaining zero. These counts describe graph structure, not execution loops, runtime or the
number of defects.

## Appendix: sensitivity field keys

Both heatmap axes use the same field numbers for each chart.

### bitnami/apache

- **1**: `$.metrics.image.debug`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.cloneHtdocsFromGit.enabled`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamiapache)

### bitnami/aspnet-core

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.healthIngress.tls`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.healthIngress.enabled`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamiaspnet-core)

### bitnami/cadvisor

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.livenessProbe.initialDelaySeconds`
- **4**: `$.diagnosticMode.enabled`
- **5**: `$.livenessProbe.periodSeconds`
- **6**: `$.readinessProbe.timeoutSeconds`
- **7**: `$.readinessProbe.initialDelaySeconds`
- **8**: `$.livenessProbe.successThreshold`

[Back to chart](#bitnamicadvisor)

### bitnami/cert-manager

- **1**: `$.webhook.readinessProbe.timeoutSeconds`
- **2**: `$.controller.networkPolicy.kubeAPIServerPorts[2]`
- **3**: `$.cainjector.containerSecurityContext.privileged`
- **4**: `$.controller.livenessProbe.timeoutSeconds`
- **5**: `$.webhook.containerSecurityContext.runAsUser`
- **6**: `$.cainjector.startupProbe.periodSeconds`
- **7**: `$.controller.networkPolicy.allowExternal`
- **8**: `$.controller.acmesolver.image.debug`

[Back to chart](#bitnamicert-manager)

### bitnami/consul

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.diagnosticMode.enabled`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.readinessProbe.timeoutSeconds`
- **8**: `$.readinessProbe.initialDelaySeconds`

[Back to chart](#bitnamiconsul)

### bitnami/contour

- **1**: `$.contour.livenessProbe.initialDelaySeconds`
- **2**: `$.envoy.hostPorts.metrics`
- **3**: `$.contour.livenessProbe.enabled`
- **4**: `$.defaultBackend.containerSecurityContext.runAsUser`
- **5**: `$.envoy.containerPorts.metrics`
- **6**: `$.envoy.shutdownManager.startupProbe.successThreshold`
- **7**: `$.contour.readinessProbe.enabled`
- **8**: `$.envoy.service.exposeMetrics`

[Back to chart](#bitnamicontour)

### bitnami/elasticsearch

- **1**: `$.metrics.podSecurityContext.enabled`
- **2**: `$.master.podSecurityContext.fsGroup`
- **3**: `$.data.networkPolicy.allowExternalEgress`
- **4**: `$.coordinating.networkPolicy.allowExternalEgress`
- **5**: `$.ingest.autoscaling.minReplicas`
- **6**: `$.data.startupProbe.initialDelaySeconds`
- **7**: `$.master.livenessProbe.successThreshold`
- **8**: `$.data.autoscaling.minReplicas`

[Back to chart](#bitnamielasticsearch)

### bitnami/envoy-gateway

- **1**: `$.certgen.readinessProbe.periodSeconds`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.certgen.networkPolicy.kubeAPIServerPorts[1]`

[Back to chart](#bitnamienvoy-gateway)

### bitnami/external-dns

- **1**: `$.rbac.pspEnabled`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.readinessProbe.timeoutSeconds`
- **8**: `$.readinessProbe.initialDelaySeconds`

[Back to chart](#bitnamiexternal-dns)

### bitnami/flink

- **1**: `$.taskmanager.startupProbe.timeoutSeconds`
- **2**: `$.taskmanager.readinessProbe.successThreshold`
- **3**: `$.taskmanager.readinessProbe.failureThreshold`
- **4**: `$.jobmanager.readinessProbe.initialDelaySeconds`
- **5**: `$.jobmanager.readinessProbe.enabled`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.jobmanager.readinessProbe.successThreshold`
- **8**: `$.taskmanager.containerSecurityContext.runAsGroup`

[Back to chart](#bitnamiflink)

### bitnami/fluent-bit

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.diagnosticMode.enabled`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.autoscaling.hpa.targetCPUUtilizationPercentage`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamifluent-bit)

### bitnami/fluentd

- **1**: `$.aggregator.service.ports.http.port`
- **2**: `$.forwarder.podSecurityContext.enabled`
- **3**: `$.aggregator.startupProbe.enabled`
- **4**: `$.forwarder.containerSecurityContext.allowPrivilegeEscalation`
- **5**: `$.aggregator.port`
- **6**: `$.aggregator.startupProbe.periodSeconds`
- **7**: `$.aggregator.containerSecurityContext.runAsGroup`
- **8**: `$.diagnosticMode.enabled`

[Back to chart](#bitnamifluentd)

### bitnami/flux

- **1**: `$.imageAutomationController.readinessProbe.periodSeconds`
- **2**: `$.sourceController.metrics.service.ports.metrics`
- **3**: `$.imageReflectorController.startupProbe.timeoutSeconds`
- **4**: `$.kustomizeController.image.debug`
- **5**: `$.helmController.autoscaling.enabled`
- **6**: `$.sourceController.readinessProbe.failureThreshold`
- **7**: `$.sourceController.rbac.create`
- **8**: `$.imageAutomationController.serviceAccount.automountServiceAccountToken`

[Back to chart](#bitnamiflux)

### bitnami/grafana-alloy

- **1**: `$.alloy.livenessProbe.periodSeconds`
- **2**: `$.alloy.clustering.enabled`
- **3**: `$.configReloader.startupProbe.failureThreshold`
- **4**: `$.alloy.readinessProbe.successThreshold`
- **5**: `$.pdb.create`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.configReloader.livenessProbe.successThreshold`
- **8**: `$.alloy.startupProbe.periodSeconds`

[Back to chart](#bitnamigrafana-alloy)

### bitnami/grafana-k6-operator

- **1**: `$.containerPorts.health`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.readinessProbe.timeoutSeconds`
- **8**: `$.readinessProbe.initialDelaySeconds`

[Back to chart](#bitnamigrafana-k6-operator)

### bitnami/grafana-loki

- **1**: `$.ingester.readinessProbe.enabled`
- **2**: `$.loki.gossipRing.service.ports.http`
- **3**: `$.queryScheduler.networkPolicy.allowExternalEgress`
- **4**: `$.indexGateway.livenessProbe.successThreshold`
- **5**: `$.compactor.enableServiceLinks`
- **6**: `$.indexGateway.livenessProbe.enabled`
- **7**: `$.queryScheduler.startupProbe.timeoutSeconds`
- **8**: `$.queryScheduler.containerSecurityContext.privileged`

[Back to chart](#bitnamigrafana-loki)

### bitnami/grafana-tempo

- **1**: `$.memcached.auth.enabled`
- **2**: `$.queryFrontend.query.containerSecurityContext.runAsUser`
- **3**: `$.ingester.readinessProbe.enabled`
- **4**: `$.queryFrontend.query.containerSecurityContext.readOnlyRootFilesystem`
- **5**: `$.metricsGenerator.containerSecurityContext.allowPrivilegeEscalation`
- **6**: `$.vulture.readinessProbe.enabled`
- **7**: `$.compactor.enableServiceLinks`
- **8**: `$.distributor.livenessProbe.successThreshold`

[Back to chart](#bitnamigrafana-tempo)

### bitnami/haproxy

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.diagnosticMode.enabled`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.readinessProbe.timeoutSeconds`
- **8**: `$.readinessProbe.initialDelaySeconds`

[Back to chart](#bitnamihaproxy)

### bitnami/influxdb

- **1**: `$.createAdminTokenJob.containerSecurityContext.enabled`
- **2**: `$.useHelmHooks`
- **3**: `$.startupProbe.successThreshold`
- **4**: `$.automountServiceAccountToken`
- **5**: `$.pdb.create`
- **6**: `$.livenessProbe.initialDelaySeconds`
- **7**: `$.diagnosticMode.enabled`
- **8**: `$.defaultInitContainers.volumePermissions.containerSecurityContext.allowPrivilegeEscalation`

[Back to chart](#bitnamiinfluxdb)

### bitnami/kibana

- **1**: `$.elasticsearch.security.tls.usePemCerts`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamikibana)

### bitnami/kube-state-metrics

- **1**: `$.kubeResources.ingresses`
- **2**: `$.kubeResources.deployments`
- **3**: `$.kubeResources.services`
- **4**: `$.rbac.pspEnabled`
- **5**: `$.kubeResources.volumeattachments`
- **6**: `$.startupProbe.successThreshold`
- **7**: `$.automountServiceAccountToken`
- **8**: `$.pdb.create`

[Back to chart](#bitnamikube-state-metrics)

### bitnami/kubernetes-event-exporter

- **1**: `$.metrics.service.ports.http`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamikubernetes-event-exporter)

### bitnami/logstash

- **1**: `$.enableMonitoringAPI`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.monitoringAPIPort`
- **4**: `$.automountServiceAccountToken`
- **5**: `$.pdb.create`
- **6**: `$.livenessProbe.initialDelaySeconds`
- **7**: `$.diagnosticMode.enabled`
- **8**: `$.livenessProbe.periodSeconds`

[Back to chart](#bitnamilogstash)

### bitnami/mariadb-galera

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.diagnosticMode.enabled`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.readinessProbe.timeoutSeconds`
- **8**: `$.readinessProbe.initialDelaySeconds`

[Back to chart](#bitnamimariadb-galera)

### bitnami/memcached

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.diagnosticMode.enabled`
- **6**: `$.metrics.startupProbe.timeoutSeconds`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamimemcached)

### bitnami/metrics-server

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.diagnosticMode.enabled`
- **5**: `$.livenessProbe.periodSeconds`
- **6**: `$.networkPolicy.kubernetesPorts[3]`
- **7**: `$.readinessProbe.timeoutSeconds`
- **8**: `$.livenessProbe.successThreshold`

[Back to chart](#bitnamimetrics-server)

### bitnami/multus-cni

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.livenessProbe.initialDelaySeconds`
- **4**: `$.diagnosticMode.enabled`
- **5**: `$.livenessProbe.periodSeconds`
- **6**: `$.readinessProbe.timeoutSeconds`
- **7**: `$.readinessProbe.initialDelaySeconds`
- **8**: `$.livenessProbe.successThreshold`

[Back to chart](#bitnamimultus-cni)

### bitnami/node-exporter

- **1**: `$.rbac.pspEnabled`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnaminode-exporter)

### bitnami/opensearch

- **1**: `$.master.podSecurityContext.fsGroup`
- **2**: `$.data.networkPolicy.allowExternalEgress`
- **3**: `$.master.metrics.rules.enabled`
- **4**: `$.dashboards.image.debug`
- **5**: `$.dashboards.podSecurityContext.enabled`
- **6**: `$.coordinating.networkPolicy.allowExternalEgress`
- **7**: `$.data.autoscaling.hpa.enabled`
- **8**: `$.dashboards.livenessProbe.successThreshold`

[Back to chart](#bitnamiopensearch)

### bitnami/phpmyadmin

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.livenessProbe.periodSeconds`
- **6**: `$.readinessProbe.timeoutSeconds`
- **7**: `$.readinessProbe.initialDelaySeconds`
- **8**: `$.livenessProbe.successThreshold`

[Back to chart](#bitnamiphpmyadmin)

### bitnami/prometheus

- **1**: `$.server.containerSecurityContext.runAsNonRoot`
- **2**: `$.server.thanos.service.ports.grpc`
- **3**: `$.server.containerSecurityContext.runAsGroup`
- **4**: `$.server.startupProbe.timeoutSeconds`
- **5**: `$.server.ingress.tls`
- **6**: `$.server.startupProbe.enabled`
- **7**: `$.alertmanager.ingress.enabled`
- **8**: `$.server.networkPolicy.allowExternal`

[Back to chart](#bitnamiprometheus)

### bitnami/pytorch

- **1**: `$.service.ports.pytorch`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamipytorch)

### bitnami/redis-cluster

- **1**: `$.metrics.service.ports.http`
- **2**: `$.pdb.create`
- **3**: `$.diagnosticMode.enabled`
- **4**: `$.redis.readinessProbe.failureThreshold`
- **5**: `$.service.ports.redis`
- **6**: `$.volumePermissions.containerSecurityContext.enabled`
- **7**: `$.metrics.enabled`
- **8**: `$.metrics.containerSecurityContext.privileged`

[Back to chart](#bitnamiredis-cluster)

### bitnami/sealed-secrets

- **1**: `$.rbac.pspEnabled`
- **2**: `$.startupProbe.successThreshold`
- **3**: `$.automountServiceAccountToken`
- **4**: `$.pdb.create`
- **5**: `$.livenessProbe.initialDelaySeconds`
- **6**: `$.rbac.namespacedRoles`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamisealed-secrets)

### bitnami/spark

- **1**: `$.master.podSecurityContext.fsGroup`
- **2**: `$.master.enabled`
- **3**: `$.master.livenessProbe.successThreshold`
- **4**: `$.master.networkPolicy.allowExternal`
- **5**: `$.worker.readinessProbe.timeoutSeconds`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.worker.containerPorts.https`
- **8**: `$.master.livenessProbe.initialDelaySeconds`

[Back to chart](#bitnamispark)

### bitnami/tensorflow-resnet

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.diagnosticMode.enabled`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.readinessProbe.timeoutSeconds`
- **8**: `$.readinessProbe.initialDelaySeconds`

[Back to chart](#bitnamitensorflow-resnet)

### bitnami/valkey-cluster

- **1**: `$.valkey.containerPorts.bus`
- **2**: `$.metrics.service.ports.http`
- **3**: `$.pdb.create`
- **4**: `$.diagnosticMode.enabled`
- **5**: `$.volumePermissions.containerSecurityContext.enabled`
- **6**: `$.valkey.shareProcessNamespace`
- **7**: `$.metrics.enabled`
- **8**: `$.metrics.containerSecurityContext.privileged`

[Back to chart](#bitnamivalkey-cluster)

### bitnami/vault

- **1**: `$.server.containerSecurityContext.runAsNonRoot`
- **2**: `$.csiProvider.podSecurityContext.fsGroup`
- **3**: `$.csiProvider.provider.containerSecurityContext.runAsGroup`
- **4**: `$.server.containerSecurityContext.runAsGroup`
- **5**: `$.server.startupProbe.timeoutSeconds`
- **6**: `$.server.ingress.tls`
- **7**: `$.injector.networkPolicy.allowExternal`
- **8**: `$.server.startupProbe.enabled`

[Back to chart](#bitnamivault)

### bitnami/victoriametrics

- **1**: `$.vmalert.readinessProbe.timeoutSeconds`
- **2**: `$.vmagent.namespaced`
- **3**: `$.vmselect.containerSecurityContext.runAsUser`
- **4**: `$.vminsert.livenessProbe.enabled`
- **5**: `$.vmalert.networkPolicy.allowExternalEgress`
- **6**: `$.vmauth.livenessProbe.failureThreshold`
- **7**: `$.vmauth.startupProbe.timeoutSeconds`
- **8**: `$.vmagent.autoscaling.vpa.enabled`

[Back to chart](#bitnamivictoriametrics)

### bitnami/whereabouts

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.livenessProbe.initialDelaySeconds`
- **4**: `$.diagnosticMode.enabled`
- **5**: `$.livenessProbe.periodSeconds`
- **6**: `$.readinessProbe.timeoutSeconds`
- **7**: `$.readinessProbe.initialDelaySeconds`
- **8**: `$.livenessProbe.successThreshold`

[Back to chart](#bitnamiwhereabouts)

### bitnami/wildfly

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.diagnosticMode.enabled`
- **6**: `$.livenessProbe.periodSeconds`
- **7**: `$.readinessProbe.timeoutSeconds`
- **8**: `$.readinessProbe.initialDelaySeconds`

[Back to chart](#bitnamiwildfly)

### bitnami/zookeeper

- **1**: `$.startupProbe.successThreshold`
- **2**: `$.automountServiceAccountToken`
- **3**: `$.pdb.create`
- **4**: `$.livenessProbe.initialDelaySeconds`
- **5**: `$.service.ports.election`
- **6**: `$.diagnosticMode.enabled`
- **7**: `$.livenessProbe.periodSeconds`
- **8**: `$.readinessProbe.timeoutSeconds`

[Back to chart](#bitnamizookeeper)

## Appendix: finding codes

HH codes identify finding categories. Numbered E entries, when present, identify recorded diagnostics.
Severities below are defaults; configured overrides are shown with the findings above.

### HH1101 - Invalid YAML in rendered output

Default severity: **error** | Category: manifest | Evidence type: violation

The YAML parser rejects rendered output, or Helm reports a YAML parse error.

Suggested action: Inspect the failing YAML and template interpolation, including quoting and indentation.

### HH1105 - Missing resource name

Default severity: **error** | Category: manifest | Evidence type: violation

The resource fails the tool's nonempty metadata.name contract.

Suggested action: Provide a name in each resource branch; ignore this check if your workflow intentionally uses generated names.

### HH1107 - Empty resource bundle

Default severity: **error** | Category: manifest | Evidence type: violation

The active test requires resources but this configuration renders none.

Suggested action: Check resource activation; ignore this contract if an empty chart is intentional.

### HH1108 - Kubernetes schema validation failed

Default severity: **error** | Category: manifest | Evidence type: violation

The configured Kubernetes validator rejects the output.

Suggested action: Use the validator's field path and expected type to check the template and input schema.

### HH1109 - Invalid manifest field type

Default severity: **error** | Category: manifest | Evidence type: violation

Helm parses the YAML but cannot decode a field into its required manifest type.

Suggested action: Check the field named in Helm's decoding error and constrain its values to the required type.

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

### HH3001 - Template accesses a missing object

Default severity: **error** | Category: template | Evidence type: violation

Helm reports a nil pointer while evaluating a template field.

Suggested action: Guard or default the parent object, or require it in the values schema.
