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
  - [HH2001 - Undocumented values path](#hh2001---undocumented-values-path)
  - [HH2002 - Unspecified values type](#hh2002---unspecified-values-type)
  - [HH2003 - Missing values description](#hh2003---missing-values-description)
  - [HH2006 - Opaque object schema](#hh2006---opaque-object-schema)

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
Started (Unix epoch): 1790106931
Started (UTC): 2026-09-22T19:55:31.000+00:00
Finished (UTC): 2026-09-22T20:49:27.508+00:00
Run fingerprint (SHA-256): `b6d745ce2c5ecbe79f5e09e2f28080005484bf99f02419b2978b75fe1e89b668`
Versions: Hypothesis 6.168.0; hypothesis-helm 0.1.0
Elapsed (wall clock): 3235.60 seconds
Chart testing: 3181.60 seconds
Dependency preparation: 49.63 seconds (excluded from testing budgets)
Charts discovered: 115
Manifest test attempts: 208
Scan status: interrupted
Discovery complete: True
Unstarted charts: 110

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

3 time-limit; 1 failed; 1 interrupted; 110 pending.

## Settings

Filtering: False | Seed: 0 | Traversal: random
Chart timeout: 600.0 seconds | Workers: 8
Complete settings are retained in the JSON report.

Command working directory: `/Users/emmadoyle/projects/personal/hypothesis-helm`

Scan command:

```bash
hypothesis-helm test third_party/bitnami-charts --jobs 8 --chart-timeout 10m --max-examples 10 --seed 0 --no-cache --shard none --artifact-dir docs/reports/bitnami-runs --report docs/reports/bitnami.md --log-color
```

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: [HH2006](#hh2006---opaque-object-schema)

## Errors

2 distinct diagnostics across 2 occurrences; 0 repeats grouped.
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

Status: time-limit | Attempts: 83

Coverage: generated path tests. Finite interaction coverage was unavailable: Cannot enumerate the input domain: permutations need closed
objects at (); set additionalProperties: false. The sampled paths do not establish N-way coverage.

Audit findings: 1190. Full paths and template references: [JSON](<bitnami-data/0001.audit.json.gz>).

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.fernetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in [JSON](<bitnami-data/0001.audit.json.gz>).

### [bitnami/apache](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apache>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/apache](<../../studies/chart-topologies/bitnami/apache/topology.png>) | ![Sensitivity: bitnami/apache](<../../studies/chart-topologies/bitnami/apache/sensitivity.png>) |

[Sensitivity field key](#bitnamiapache-1).

Overview cell: 02

Status: failed | Attempts: 29

Coverage: generated path tests. Finite interaction coverage was unavailable: Cannot enumerate the input domain: permutations need closed
objects at (); set additionalProperties: false. The sampled paths do not establish N-way coverage.

Audit findings: 245. Full paths and template references: [JSON](<bitnami-data/0002.audit.json.gz>).

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 239 additional audit findings in [JSON](<bitnami-data/0002.audit.json.gz>).

#### E001 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

#### E002 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... bash\n\n. /opt/bitnami/scripts/libfs.sh\n# We copy the logs folder because it has
symlinks to stdout and stderr\nif ! is_dir_empty /opt/bitnami/apache/logs; then\n cp -r /opt/bitnami/apache/logs
/emptydir/app-logs-dir\nfi\n'], 'volumeMounts': [{'name': 'empty-dir', 'mountPath': '/emptydir'}]}]") in "<unicode string>", line 265,
column 7: initContainers: ^ (line: 265) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.extraPodSpec.initContainers[*].envFrom[*].configMapRef.name | Status: failed

Changed overrides (used together):
- `$.extraPodSpec.initContainers.__hypothesis_key__.envFrom.__hypothesis_key__.configMapRef.name = null`
Absent from overrides: $.extraPodSpec.initContainers["*"].envFrom["*"].configMapRef.name. Defaults may still apply.

Renderer random inputs (replay tape in artifacts):

### [bitnami/apisix](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apisix>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/apisix](<../../studies/chart-topologies/bitnami/apisix/topology.png>) | ![Sensitivity: bitnami/apisix](<../../studies/chart-topologies/bitnami/apisix/sensitivity.png>) |

Overview cell: 03

Status: time-limit | Attempts: 21

Coverage: generated path tests. Finite interaction coverage was unavailable: Cannot enumerate the input domain: permutations need closed
objects at (); set additionalProperties: false. The sampled paths do not establish N-way coverage.

Audit findings: 344. Full paths and template references: [JSON](<bitnami-data/0003.audit.json.gz>).

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.controlPlane.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controlPlane.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.vpa`: Missing values description (info)
- 338 additional audit findings in [JSON](<bitnami-data/0003.audit.json.gz>).

### [bitnami/appsmith](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/appsmith>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/appsmith](<../../studies/chart-topologies/bitnami/appsmith/topology.png>) | ![Sensitivity: bitnami/appsmith](<../../studies/chart-topologies/bitnami/appsmith/sensitivity.png>) |

Overview cell: 04

Status: time-limit | Attempts: 54

Coverage: generated path tests. Finite interaction coverage was unavailable: Cannot enumerate the input domain: permutations need closed
objects at (); set additionalProperties: false. The sampled paths do not establish N-way coverage.

Audit findings: 543. Full paths and template references: [JSON](<bitnami-data/0004.audit.json.gz>).

- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.automountServiceAccountToken`: Undocumented values path (warning)
- 537 additional audit findings in [JSON](<bitnami-data/0004.audit.json.gz>).

### [bitnami/argo-cd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-cd>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/argo-cd](<../../studies/chart-topologies/bitnami/argo-cd/topology.png>) | ![Sensitivity: bitnami/argo-cd](<../../studies/chart-topologies/bitnami/argo-cd/sensitivity.png>) |

Overview cell: 05

Status: interrupted | Attempts: 21

Coverage: generated path tests. Finite interaction coverage was unavailable: Cannot enumerate the input domain: permutations need closed
objects at (); set additionalProperties: false. The sampled paths do not establish N-way coverage.

Audit findings: 1251. Full paths and template references: [JSON](<bitnami-data/0005.audit.json.gz>).

- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterAdminAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterRoleRules`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.containerPorts`: Undocumented values path (warning)
- 1245 additional audit findings in [JSON](<bitnami-data/0005.audit.json.gz>).

### [bitnami/argo-workflows](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-workflows>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/argo-workflows](<../../studies/chart-topologies/bitnami/argo-workflows/topology.png>) | ![Sensitivity: bitnami/argo-workflows](<../../studies/chart-topologies/bitnami/argo-workflows/sensitivity.png>) |

Overview cell: 06

Status: pending | Attempts: N/A

### [bitnami/aspnet-core](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/aspnet-core>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/aspnet-core](<../../studies/chart-topologies/bitnami/aspnet-core/topology.png>) | ![Sensitivity: bitnami/aspnet-core](<../../studies/chart-topologies/bitnami/aspnet-core/sensitivity.png>) |

[Sensitivity field key](#bitnamiaspnet-core-1).

Overview cell: 07

Status: pending | Attempts: N/A

### [bitnami/cadvisor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cadvisor>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cadvisor](<../../studies/chart-topologies/bitnami/cadvisor/topology.png>) | ![Sensitivity: bitnami/cadvisor](<../../studies/chart-topologies/bitnami/cadvisor/sensitivity.png>) |

[Sensitivity field key](#bitnamicadvisor-1).

Overview cell: 08

Status: pending | Attempts: N/A

### [bitnami/cassandra](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cassandra>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cassandra](<../../studies/chart-topologies/bitnami/cassandra/topology.png>) | ![Sensitivity: bitnami/cassandra](<../../studies/chart-topologies/bitnami/cassandra/sensitivity.png>) |

Overview cell: 09

Status: pending | Attempts: N/A

### [bitnami/cert-manager](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cert-manager>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cert-manager](<../../studies/chart-topologies/bitnami/cert-manager/topology.png>) | ![Sensitivity: bitnami/cert-manager](<../../studies/chart-topologies/bitnami/cert-manager/sensitivity.png>) |

[Sensitivity field key](#bitnamicert-manager-1).

Overview cell: 10

Status: pending | Attempts: N/A

### [bitnami/chainloop](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/chainloop>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/chainloop](<../../studies/chart-topologies/bitnami/chainloop/topology.png>) | ![Sensitivity: bitnami/chainloop](<../../studies/chart-topologies/bitnami/chainloop/sensitivity.png>) |

Overview cell: 11

Status: pending | Attempts: N/A

### [bitnami/cilium](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cilium>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cilium](<../../studies/chart-topologies/bitnami/cilium/topology.png>) | ![Sensitivity: bitnami/cilium](<../../studies/chart-topologies/bitnami/cilium/sensitivity.png>) |

Overview cell: 12

Status: pending | Attempts: N/A

### [bitnami/clickhouse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/clickhouse](<../../studies/chart-topologies/bitnami/clickhouse/topology.png>) | ![Sensitivity: bitnami/clickhouse](<../../studies/chart-topologies/bitnami/clickhouse/sensitivity.png>) |

Overview cell: 13

Status: pending | Attempts: N/A

### [bitnami/clickhouse-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse-operator>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/clickhouse-operator](<../../studies/chart-topologies/bitnami/clickhouse-operator/topology.png>) | ![Sensitivity: bitnami/clickhouse-operator](<../../studies/chart-topologies/bitnami/clickhouse-operator/sensitivity.png>) |

Overview cell: 14

Status: pending | Attempts: N/A

### [bitnami/cloudnative-pg](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cloudnative-pg>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/cloudnative-pg](<../../studies/chart-topologies/bitnami/cloudnative-pg/topology.png>) | ![Sensitivity: bitnami/cloudnative-pg](<../../studies/chart-topologies/bitnami/cloudnative-pg/sensitivity.png>) |

Overview cell: 15

Status: pending | Attempts: N/A

### [bitnami/common](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/common>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/common](<../../studies/chart-topologies/bitnami/common/topology.png>) | ![Sensitivity: bitnami/common](<../../studies/chart-topologies/bitnami/common/sensitivity.png>) |

Overview cell: 16

Status: pending | Attempts: N/A

### [bitnami/concourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/concourse>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/concourse](<../../studies/chart-topologies/bitnami/concourse/topology.png>) | ![Sensitivity: bitnami/concourse](<../../studies/chart-topologies/bitnami/concourse/sensitivity.png>) |

Overview cell: 17

Status: pending | Attempts: N/A

### [bitnami/consul](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/consul>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/consul](<../../studies/chart-topologies/bitnami/consul/topology.png>) | ![Sensitivity: bitnami/consul](<../../studies/chart-topologies/bitnami/consul/sensitivity.png>) |

[Sensitivity field key](#bitnamiconsul-1).

Overview cell: 18

Status: pending | Attempts: N/A

### [bitnami/contour](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/contour>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/contour](<../../studies/chart-topologies/bitnami/contour/topology.png>) | ![Sensitivity: bitnami/contour](<../../studies/chart-topologies/bitnami/contour/sensitivity.png>) |

[Sensitivity field key](#bitnamicontour-1).

Overview cell: 19

Status: pending | Attempts: N/A

### [bitnami/deepspeed](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/deepspeed>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/deepspeed](<../../studies/chart-topologies/bitnami/deepspeed/topology.png>) | ![Sensitivity: bitnami/deepspeed](<../../studies/chart-topologies/bitnami/deepspeed/sensitivity.png>) |

Overview cell: 20

Status: pending | Attempts: N/A

### [bitnami/discourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/discourse>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/discourse](<../../studies/chart-topologies/bitnami/discourse/topology.png>) | ![Sensitivity: bitnami/discourse](<../../studies/chart-topologies/bitnami/discourse/sensitivity.png>) |

Overview cell: 21

Status: pending | Attempts: N/A

### [bitnami/dremio](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/dremio>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/dremio](<../../studies/chart-topologies/bitnami/dremio/topology.png>) | ![Sensitivity: bitnami/dremio](<../../studies/chart-topologies/bitnami/dremio/sensitivity.png>) |

Overview cell: 22

Status: pending | Attempts: N/A

### [bitnami/drupal](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/drupal>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/drupal](<../../studies/chart-topologies/bitnami/drupal/topology.png>) | ![Sensitivity: bitnami/drupal](<../../studies/chart-topologies/bitnami/drupal/sensitivity.png>) |

Overview cell: 23

Status: pending | Attempts: N/A

### [bitnami/ejbca](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ejbca>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/ejbca](<../../studies/chart-topologies/bitnami/ejbca/topology.png>) | ![Sensitivity: bitnami/ejbca](<../../studies/chart-topologies/bitnami/ejbca/sensitivity.png>) |

Overview cell: 24

Status: pending | Attempts: N/A

### [bitnami/elasticsearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/elasticsearch>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/elasticsearch](<../../studies/chart-topologies/bitnami/elasticsearch/topology.png>) | ![Sensitivity: bitnami/elasticsearch](<../../studies/chart-topologies/bitnami/elasticsearch/sensitivity.png>) |

[Sensitivity field key](#bitnamielasticsearch-1).

Overview cell: 25

Status: pending | Attempts: N/A

### [bitnami/envoy-gateway](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/envoy-gateway>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/envoy-gateway](<../../studies/chart-topologies/bitnami/envoy-gateway/topology.png>) | ![Sensitivity: bitnami/envoy-gateway](<../../studies/chart-topologies/bitnami/envoy-gateway/sensitivity.png>) |

[Sensitivity field key](#bitnamienvoy-gateway-1).

Overview cell: 26

Status: pending | Attempts: N/A

### [bitnami/etcd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/etcd>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/etcd](<../../studies/chart-topologies/bitnami/etcd/topology.png>) | ![Sensitivity: bitnami/etcd](<../../studies/chart-topologies/bitnami/etcd/sensitivity.png>) |

Overview cell: 27

Status: pending | Attempts: N/A

### [bitnami/external-dns](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/external-dns>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/external-dns](<../../studies/chart-topologies/bitnami/external-dns/topology.png>) | ![Sensitivity: bitnami/external-dns](<../../studies/chart-topologies/bitnami/external-dns/sensitivity.png>) |

[Sensitivity field key](#bitnamiexternal-dns-1).

Overview cell: 28

Status: pending | Attempts: N/A

### [bitnami/flink](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flink>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/flink](<../../studies/chart-topologies/bitnami/flink/topology.png>) | ![Sensitivity: bitnami/flink](<../../studies/chart-topologies/bitnami/flink/sensitivity.png>) |

[Sensitivity field key](#bitnamiflink-1).

Overview cell: 29

Status: pending | Attempts: N/A

### [bitnami/fluent-bit](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluent-bit>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/fluent-bit](<../../studies/chart-topologies/bitnami/fluent-bit/topology.png>) | ![Sensitivity: bitnami/fluent-bit](<../../studies/chart-topologies/bitnami/fluent-bit/sensitivity.png>) |

[Sensitivity field key](#bitnamifluent-bit-1).

Overview cell: 30

Status: pending | Attempts: N/A

### [bitnami/fluentd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluentd>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/fluentd](<../../studies/chart-topologies/bitnami/fluentd/topology.png>) | ![Sensitivity: bitnami/fluentd](<../../studies/chart-topologies/bitnami/fluentd/sensitivity.png>) |

[Sensitivity field key](#bitnamifluentd-1).

Overview cell: 31

Status: pending | Attempts: N/A

### [bitnami/flux](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flux>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/flux](<../../studies/chart-topologies/bitnami/flux/topology.png>) | ![Sensitivity: bitnami/flux](<../../studies/chart-topologies/bitnami/flux/sensitivity.png>) |

[Sensitivity field key](#bitnamiflux-1).

Overview cell: 32

Status: pending | Attempts: N/A

### [bitnami/ghost](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ghost>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/ghost](<../../studies/chart-topologies/bitnami/ghost/topology.png>) | ![Sensitivity: bitnami/ghost](<../../studies/chart-topologies/bitnami/ghost/sensitivity.png>) |

Overview cell: 33

Status: pending | Attempts: N/A

### [bitnami/gitea](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitea>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/gitea](<../../studies/chart-topologies/bitnami/gitea/topology.png>) | ![Sensitivity: bitnami/gitea](<../../studies/chart-topologies/bitnami/gitea/sensitivity.png>) |

Overview cell: 34

Status: pending | Attempts: N/A

### [bitnami/gitlab-runner](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitlab-runner>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/gitlab-runner](<../../studies/chart-topologies/bitnami/gitlab-runner/topology.png>) | ![Sensitivity: bitnami/gitlab-runner](<../../studies/chart-topologies/bitnami/gitlab-runner/sensitivity.png>) |

Overview cell: 35

Status: pending | Attempts: N/A

### [bitnami/grafana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana](<../../studies/chart-topologies/bitnami/grafana/topology.png>) | ![Sensitivity: bitnami/grafana](<../../studies/chart-topologies/bitnami/grafana/sensitivity.png>) |

Overview cell: 36

Status: pending | Attempts: N/A

### [bitnami/grafana-alloy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-alloy>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-alloy](<../../studies/chart-topologies/bitnami/grafana-alloy/topology.png>) | ![Sensitivity: bitnami/grafana-alloy](<../../studies/chart-topologies/bitnami/grafana-alloy/sensitivity.png>) |

[Sensitivity field key](#bitnamigrafana-alloy-1).

Overview cell: 37

Status: pending | Attempts: N/A

### [bitnami/grafana-k6-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-k6-operator>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-k6-operator](<../../studies/chart-topologies/bitnami/grafana-k6-operator/topology.png>) | ![Sensitivity: bitnami/grafana-k6-operator](<../../studies/chart-topologies/bitnami/grafana-k6-operator/sensitivity.png>) |

[Sensitivity field key](#bitnamigrafana-k6-operator-1).

Overview cell: 38

Status: pending | Attempts: N/A

### [bitnami/grafana-loki](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-loki>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-loki](<../../studies/chart-topologies/bitnami/grafana-loki/topology.png>) | ![Sensitivity: bitnami/grafana-loki](<../../studies/chart-topologies/bitnami/grafana-loki/sensitivity.png>) |

[Sensitivity field key](#bitnamigrafana-loki-1).

Overview cell: 39

Status: pending | Attempts: N/A

### [bitnami/grafana-mimir](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-mimir>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-mimir](<../../studies/chart-topologies/bitnami/grafana-mimir/topology.png>) | ![Sensitivity: bitnami/grafana-mimir](<../../studies/chart-topologies/bitnami/grafana-mimir/sensitivity.png>) |

Overview cell: 40

Status: pending | Attempts: N/A

### [bitnami/grafana-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-operator>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-operator](<../../studies/chart-topologies/bitnami/grafana-operator/topology.png>) | ![Sensitivity: bitnami/grafana-operator](<../../studies/chart-topologies/bitnami/grafana-operator/sensitivity.png>) |

Overview cell: 41

Status: pending | Attempts: N/A

### [bitnami/grafana-tempo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-tempo>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/grafana-tempo](<../../studies/chart-topologies/bitnami/grafana-tempo/topology.png>) | ![Sensitivity: bitnami/grafana-tempo](<../../studies/chart-topologies/bitnami/grafana-tempo/sensitivity.png>) |

[Sensitivity field key](#bitnamigrafana-tempo-1).

Overview cell: 42

Status: pending | Attempts: N/A

### [bitnami/haproxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/haproxy>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/haproxy](<../../studies/chart-topologies/bitnami/haproxy/topology.png>) | ![Sensitivity: bitnami/haproxy](<../../studies/chart-topologies/bitnami/haproxy/sensitivity.png>) |

[Sensitivity field key](#bitnamihaproxy-1).

Overview cell: 43

Status: pending | Attempts: N/A

### [bitnami/harbor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/harbor>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/harbor](<../../studies/chart-topologies/bitnami/harbor/topology.png>) | ![Sensitivity: bitnami/harbor](<../../studies/chart-topologies/bitnami/harbor/sensitivity.png>) |

Overview cell: 44

Status: pending | Attempts: N/A

### [bitnami/influxdb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/influxdb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/influxdb](<../../studies/chart-topologies/bitnami/influxdb/topology.png>) | ![Sensitivity: bitnami/influxdb](<../../studies/chart-topologies/bitnami/influxdb/sensitivity.png>) |

[Sensitivity field key](#bitnamiinfluxdb-1).

Overview cell: 45

Status: pending | Attempts: N/A

### [bitnami/jaeger](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jaeger>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/jaeger](<../../studies/chart-topologies/bitnami/jaeger/topology.png>) | ![Sensitivity: bitnami/jaeger](<../../studies/chart-topologies/bitnami/jaeger/sensitivity.png>) |

Overview cell: 46

Status: pending | Attempts: N/A

### [bitnami/janusgraph](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/janusgraph>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/janusgraph](<../../studies/chart-topologies/bitnami/janusgraph/topology.png>) | ![Sensitivity: bitnami/janusgraph](<../../studies/chart-topologies/bitnami/janusgraph/sensitivity.png>) |

Overview cell: 47

Status: pending | Attempts: N/A

### [bitnami/jenkins](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jenkins>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/jenkins](<../../studies/chart-topologies/bitnami/jenkins/topology.png>) | ![Sensitivity: bitnami/jenkins](<../../studies/chart-topologies/bitnami/jenkins/sensitivity.png>) |

Overview cell: 48

Status: pending | Attempts: N/A

### [bitnami/jupyterhub](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jupyterhub>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/jupyterhub](<../../studies/chart-topologies/bitnami/jupyterhub/topology.png>) | ![Sensitivity: bitnami/jupyterhub](<../../studies/chart-topologies/bitnami/jupyterhub/sensitivity.png>) |

Overview cell: 49

Status: pending | Attempts: N/A

### [bitnami/kafka](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kafka>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kafka](<../../studies/chart-topologies/bitnami/kafka/topology.png>) | ![Sensitivity: bitnami/kafka](<../../studies/chart-topologies/bitnami/kafka/sensitivity.png>) |

Overview cell: 50

Status: pending | Attempts: N/A

### [bitnami/keycloak](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keycloak>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/keycloak](<../../studies/chart-topologies/bitnami/keycloak/topology.png>) | ![Sensitivity: bitnami/keycloak](<../../studies/chart-topologies/bitnami/keycloak/sensitivity.png>) |

Overview cell: 51

Status: pending | Attempts: N/A

### [bitnami/keydb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keydb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/keydb](<../../studies/chart-topologies/bitnami/keydb/topology.png>) | ![Sensitivity: bitnami/keydb](<../../studies/chart-topologies/bitnami/keydb/sensitivity.png>) |

Overview cell: 52

Status: pending | Attempts: N/A

### [bitnami/kibana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kibana>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kibana](<../../studies/chart-topologies/bitnami/kibana/topology.png>) | ![Sensitivity: bitnami/kibana](<../../studies/chart-topologies/bitnami/kibana/sensitivity.png>) |

[Sensitivity field key](#bitnamikibana-1).

Overview cell: 53

Status: pending | Attempts: N/A

### [bitnami/kong](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kong>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kong](<../../studies/chart-topologies/bitnami/kong/topology.png>) | ![Sensitivity: bitnami/kong](<../../studies/chart-topologies/bitnami/kong/sensitivity.png>) |

Overview cell: 54

Status: pending | Attempts: N/A

### [bitnami/kube-arangodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-arangodb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kube-arangodb](<../../studies/chart-topologies/bitnami/kube-arangodb/topology.png>) | ![Sensitivity: bitnami/kube-arangodb](<../../studies/chart-topologies/bitnami/kube-arangodb/sensitivity.png>) |

Overview cell: 55

Status: pending | Attempts: N/A

### [bitnami/kube-prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kube-prometheus](<../../studies/chart-topologies/bitnami/kube-prometheus/topology.png>) | ![Sensitivity: bitnami/kube-prometheus](<../../studies/chart-topologies/bitnami/kube-prometheus/sensitivity.png>) |

Overview cell: 56

Status: pending | Attempts: N/A

### [bitnami/kube-prometheus/charts/kube-prometheus-crds](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus/charts/kube-prometheus-crds>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kube-prometheus/charts/kube-prometheus-crds](<../../studies/chart-topologies/bitnami/kube-prometheus/charts/kube-prometheus-crds/topology.png>) | ![Sensitivity: bitnami/kube-prometheus/charts/kube-prometheus-crds](<../../studies/chart-topologies/bitnami/kube-prometheus/charts/kube-prometheus-crds/sensitivity.png>) |

Overview cell: 57

Status: pending | Attempts: N/A

### [bitnami/kube-state-metrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-state-metrics>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kube-state-metrics](<../../studies/chart-topologies/bitnami/kube-state-metrics/topology.png>) | ![Sensitivity: bitnami/kube-state-metrics](<../../studies/chart-topologies/bitnami/kube-state-metrics/sensitivity.png>) |

[Sensitivity field key](#bitnamikube-state-metrics-1).

Overview cell: 58

Status: pending | Attempts: N/A

### [bitnami/kuberay](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kuberay>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kuberay](<../../studies/chart-topologies/bitnami/kuberay/topology.png>) | ![Sensitivity: bitnami/kuberay](<../../studies/chart-topologies/bitnami/kuberay/sensitivity.png>) |

Overview cell: 59

Status: pending | Attempts: N/A

### [bitnami/kubernetes-event-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kubernetes-event-exporter>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/kubernetes-event-exporter](<../../studies/chart-topologies/bitnami/kubernetes-event-exporter/topology.png>) | ![Sensitivity: bitnami/kubernetes-event-exporter](<../../studies/chart-topologies/bitnami/kubernetes-event-exporter/sensitivity.png>) |

[Sensitivity field key](#bitnamikubernetes-event-exporter-1).

Overview cell: 60

Status: pending | Attempts: N/A

### [bitnami/logstash](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/logstash>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/logstash](<../../studies/chart-topologies/bitnami/logstash/topology.png>) | ![Sensitivity: bitnami/logstash](<../../studies/chart-topologies/bitnami/logstash/sensitivity.png>) |

[Sensitivity field key](#bitnamilogstash-1).

Overview cell: 61

Status: pending | Attempts: N/A

### [bitnami/mariadb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mariadb](<../../studies/chart-topologies/bitnami/mariadb/topology.png>) | ![Sensitivity: bitnami/mariadb](<../../studies/chart-topologies/bitnami/mariadb/sensitivity.png>) |

Overview cell: 62

Status: pending | Attempts: N/A

### [bitnami/mariadb-galera](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb-galera>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mariadb-galera](<../../studies/chart-topologies/bitnami/mariadb-galera/topology.png>) | ![Sensitivity: bitnami/mariadb-galera](<../../studies/chart-topologies/bitnami/mariadb-galera/sensitivity.png>) |

[Sensitivity field key](#bitnamimariadb-galera-1).

Overview cell: 63

Status: pending | Attempts: N/A

### [bitnami/mastodon](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mastodon>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mastodon](<../../studies/chart-topologies/bitnami/mastodon/topology.png>) | ![Sensitivity: bitnami/mastodon](<../../studies/chart-topologies/bitnami/mastodon/sensitivity.png>) |

Overview cell: 64

Status: pending | Attempts: N/A

### [bitnami/matomo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/matomo>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/matomo](<../../studies/chart-topologies/bitnami/matomo/topology.png>) | ![Sensitivity: bitnami/matomo](<../../studies/chart-topologies/bitnami/matomo/sensitivity.png>) |

Overview cell: 65

Status: pending | Attempts: N/A

### [bitnami/memcached](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/memcached>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/memcached](<../../studies/chart-topologies/bitnami/memcached/topology.png>) | ![Sensitivity: bitnami/memcached](<../../studies/chart-topologies/bitnami/memcached/sensitivity.png>) |

[Sensitivity field key](#bitnamimemcached-1).

Overview cell: 66

Status: pending | Attempts: N/A

### [bitnami/metallb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metallb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/metallb](<../../studies/chart-topologies/bitnami/metallb/topology.png>) | ![Sensitivity: bitnami/metallb](<../../studies/chart-topologies/bitnami/metallb/sensitivity.png>) |

Overview cell: 67

Status: pending | Attempts: N/A

### [bitnami/metrics-server](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metrics-server>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/metrics-server](<../../studies/chart-topologies/bitnami/metrics-server/topology.png>) | ![Sensitivity: bitnami/metrics-server](<../../studies/chart-topologies/bitnami/metrics-server/sensitivity.png>) |

[Sensitivity field key](#bitnamimetrics-server-1).

Overview cell: 68

Status: pending | Attempts: N/A

### [bitnami/milvus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/milvus>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/milvus](<../../studies/chart-topologies/bitnami/milvus/topology.png>) | ![Sensitivity: bitnami/milvus](<../../studies/chart-topologies/bitnami/milvus/sensitivity.png>) |

Overview cell: 69

Status: pending | Attempts: N/A

### [bitnami/mlflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mlflow>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mlflow](<../../studies/chart-topologies/bitnami/mlflow/topology.png>) | ![Sensitivity: bitnami/mlflow](<../../studies/chart-topologies/bitnami/mlflow/sensitivity.png>) |

Overview cell: 70

Status: pending | Attempts: N/A

### [bitnami/mongodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mongodb](<../../studies/chart-topologies/bitnami/mongodb/topology.png>) | ![Sensitivity: bitnami/mongodb](<../../studies/chart-topologies/bitnami/mongodb/sensitivity.png>) |

Overview cell: 71

Status: pending | Attempts: N/A

### [bitnami/mongodb-sharded](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb-sharded>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mongodb-sharded](<../../studies/chart-topologies/bitnami/mongodb-sharded/topology.png>) | ![Sensitivity: bitnami/mongodb-sharded](<../../studies/chart-topologies/bitnami/mongodb-sharded/sensitivity.png>) |

Overview cell: 72

Status: pending | Attempts: N/A

### [bitnami/moodle](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/moodle>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/moodle](<../../studies/chart-topologies/bitnami/moodle/topology.png>) | ![Sensitivity: bitnami/moodle](<../../studies/chart-topologies/bitnami/moodle/sensitivity.png>) |

Overview cell: 73

Status: pending | Attempts: N/A

### [bitnami/multus-cni](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/multus-cni>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/multus-cni](<../../studies/chart-topologies/bitnami/multus-cni/topology.png>) | ![Sensitivity: bitnami/multus-cni](<../../studies/chart-topologies/bitnami/multus-cni/sensitivity.png>) |

[Sensitivity field key](#bitnamimultus-cni-1).

Overview cell: 74

Status: pending | Attempts: N/A

### [bitnami/mysql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mysql>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/mysql](<../../studies/chart-topologies/bitnami/mysql/topology.png>) | ![Sensitivity: bitnami/mysql](<../../studies/chart-topologies/bitnami/mysql/sensitivity.png>) |

Overview cell: 75

Status: pending | Attempts: N/A

### [bitnami/nats](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nats>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/nats](<../../studies/chart-topologies/bitnami/nats/topology.png>) | ![Sensitivity: bitnami/nats](<../../studies/chart-topologies/bitnami/nats/sensitivity.png>) |

Overview cell: 76

Status: pending | Attempts: N/A

### [bitnami/neo4j](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/neo4j>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/neo4j](<../../studies/chart-topologies/bitnami/neo4j/topology.png>) | ![Sensitivity: bitnami/neo4j](<../../studies/chart-topologies/bitnami/neo4j/sensitivity.png>) |

Overview cell: 77

Status: pending | Attempts: N/A

### [bitnami/nessie](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nessie>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/nessie](<../../studies/chart-topologies/bitnami/nessie/topology.png>) | ![Sensitivity: bitnami/nessie](<../../studies/chart-topologies/bitnami/nessie/sensitivity.png>) |

Overview cell: 78

Status: pending | Attempts: N/A

### [bitnami/nginx](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nginx>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/nginx](<../../studies/chart-topologies/bitnami/nginx/topology.png>) | ![Sensitivity: bitnami/nginx](<../../studies/chart-topologies/bitnami/nginx/sensitivity.png>) |

Overview cell: 79

Status: pending | Attempts: N/A

### [bitnami/node-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/node-exporter>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/node-exporter](<../../studies/chart-topologies/bitnami/node-exporter/topology.png>) | ![Sensitivity: bitnami/node-exporter](<../../studies/chart-topologies/bitnami/node-exporter/sensitivity.png>) |

[Sensitivity field key](#bitnaminode-exporter-1).

Overview cell: 80

Status: pending | Attempts: N/A

### [bitnami/oauth2-proxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/oauth2-proxy>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/oauth2-proxy](<../../studies/chart-topologies/bitnami/oauth2-proxy/topology.png>) | ![Sensitivity: bitnami/oauth2-proxy](<../../studies/chart-topologies/bitnami/oauth2-proxy/sensitivity.png>) |

Overview cell: 81

Status: pending | Attempts: N/A

### [bitnami/odoo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/odoo>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/odoo](<../../studies/chart-topologies/bitnami/odoo/topology.png>) | ![Sensitivity: bitnami/odoo](<../../studies/chart-topologies/bitnami/odoo/sensitivity.png>) |

Overview cell: 82

Status: pending | Attempts: N/A

### [bitnami/opensearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/opensearch>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/opensearch](<../../studies/chart-topologies/bitnami/opensearch/topology.png>) | ![Sensitivity: bitnami/opensearch](<../../studies/chart-topologies/bitnami/opensearch/sensitivity.png>) |

[Sensitivity field key](#bitnamiopensearch-1).

Overview cell: 83

Status: pending | Attempts: N/A

### [bitnami/parse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/parse>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/parse](<../../studies/chart-topologies/bitnami/parse/topology.png>) | ![Sensitivity: bitnami/parse](<../../studies/chart-topologies/bitnami/parse/sensitivity.png>) |

Overview cell: 84

Status: pending | Attempts: N/A

### [bitnami/phpmyadmin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/phpmyadmin>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/phpmyadmin](<../../studies/chart-topologies/bitnami/phpmyadmin/topology.png>) | ![Sensitivity: bitnami/phpmyadmin](<../../studies/chart-topologies/bitnami/phpmyadmin/sensitivity.png>) |

[Sensitivity field key](#bitnamiphpmyadmin-1).

Overview cell: 85

Status: pending | Attempts: N/A

### [bitnami/pinniped](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pinniped>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/pinniped](<../../studies/chart-topologies/bitnami/pinniped/topology.png>) | ![Sensitivity: bitnami/pinniped](<../../studies/chart-topologies/bitnami/pinniped/sensitivity.png>) |

Overview cell: 86

Status: pending | Attempts: N/A

### [bitnami/postgresql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/postgresql](<../../studies/chart-topologies/bitnami/postgresql/topology.png>) | ![Sensitivity: bitnami/postgresql](<../../studies/chart-topologies/bitnami/postgresql/sensitivity.png>) |

Overview cell: 87

Status: pending | Attempts: N/A

### [bitnami/postgresql-ha](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql-ha>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/postgresql-ha](<../../studies/chart-topologies/bitnami/postgresql-ha/topology.png>) | ![Sensitivity: bitnami/postgresql-ha](<../../studies/chart-topologies/bitnami/postgresql-ha/sensitivity.png>) |

Overview cell: 88

Status: pending | Attempts: N/A

### [bitnami/prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/prometheus>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/prometheus](<../../studies/chart-topologies/bitnami/prometheus/topology.png>) | ![Sensitivity: bitnami/prometheus](<../../studies/chart-topologies/bitnami/prometheus/sensitivity.png>) |

[Sensitivity field key](#bitnamiprometheus-1).

Overview cell: 89

Status: pending | Attempts: N/A

### [bitnami/pytorch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pytorch>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/pytorch](<../../studies/chart-topologies/bitnami/pytorch/topology.png>) | ![Sensitivity: bitnami/pytorch](<../../studies/chart-topologies/bitnami/pytorch/sensitivity.png>) |

[Sensitivity field key](#bitnamipytorch-1).

Overview cell: 90

Status: pending | Attempts: N/A

### [bitnami/rabbitmq](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/rabbitmq](<../../studies/chart-topologies/bitnami/rabbitmq/topology.png>) | ![Sensitivity: bitnami/rabbitmq](<../../studies/chart-topologies/bitnami/rabbitmq/sensitivity.png>) |

Overview cell: 91

Status: pending | Attempts: N/A

### [bitnami/rabbitmq-cluster-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq-cluster-operator>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/rabbitmq-cluster-operator](<../../studies/chart-topologies/bitnami/rabbitmq-cluster-operator/topology.png>) | ![Sensitivity: bitnami/rabbitmq-cluster-operator](<../../studies/chart-topologies/bitnami/rabbitmq-cluster-operator/sensitivity.png>) |

Overview cell: 92

Status: pending | Attempts: N/A

### [bitnami/redis](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/redis](<../../studies/chart-topologies/bitnami/redis/topology.png>) | ![Sensitivity: bitnami/redis](<../../studies/chart-topologies/bitnami/redis/sensitivity.png>) |

Overview cell: 93

Status: pending | Attempts: N/A

### [bitnami/redis-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis-cluster>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/redis-cluster](<../../studies/chart-topologies/bitnami/redis-cluster/topology.png>) | ![Sensitivity: bitnami/redis-cluster](<../../studies/chart-topologies/bitnami/redis-cluster/sensitivity.png>) |

[Sensitivity field key](#bitnamiredis-cluster-1).

Overview cell: 94

Status: pending | Attempts: N/A

### [bitnami/redmine](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redmine>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/redmine](<../../studies/chart-topologies/bitnami/redmine/topology.png>) | ![Sensitivity: bitnami/redmine](<../../studies/chart-topologies/bitnami/redmine/sensitivity.png>) |

Overview cell: 95

Status: pending | Attempts: N/A

### [bitnami/schema-registry](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/schema-registry>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/schema-registry](<../../studies/chart-topologies/bitnami/schema-registry/topology.png>) | ![Sensitivity: bitnami/schema-registry](<../../studies/chart-topologies/bitnami/schema-registry/sensitivity.png>) |

Overview cell: 96

Status: pending | Attempts: N/A

### [bitnami/scylladb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/scylladb>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/scylladb](<../../studies/chart-topologies/bitnami/scylladb/topology.png>) | ![Sensitivity: bitnami/scylladb](<../../studies/chart-topologies/bitnami/scylladb/sensitivity.png>) |

Overview cell: 97

Status: pending | Attempts: N/A

### [bitnami/sealed-secrets](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sealed-secrets>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/sealed-secrets](<../../studies/chart-topologies/bitnami/sealed-secrets/topology.png>) | ![Sensitivity: bitnami/sealed-secrets](<../../studies/chart-topologies/bitnami/sealed-secrets/sensitivity.png>) |

[Sensitivity field key](#bitnamisealed-secrets-1).

Overview cell: 98

Status: pending | Attempts: N/A

### [bitnami/seaweedfs](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/seaweedfs>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/seaweedfs](<../../studies/chart-topologies/bitnami/seaweedfs/topology.png>) | ![Sensitivity: bitnami/seaweedfs](<../../studies/chart-topologies/bitnami/seaweedfs/sensitivity.png>) |

Overview cell: 99

Status: pending | Attempts: N/A

### [bitnami/solr](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/solr>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/solr](<../../studies/chart-topologies/bitnami/solr/topology.png>) | ![Sensitivity: bitnami/solr](<../../studies/chart-topologies/bitnami/solr/sensitivity.png>) |

Overview cell: 100

Status: pending | Attempts: N/A

### [bitnami/sonarqube](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sonarqube>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/sonarqube](<../../studies/chart-topologies/bitnami/sonarqube/topology.png>) | ![Sensitivity: bitnami/sonarqube](<../../studies/chart-topologies/bitnami/sonarqube/sensitivity.png>) |

Overview cell: 101

Status: pending | Attempts: N/A

### [bitnami/spark](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/spark>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/spark](<../../studies/chart-topologies/bitnami/spark/topology.png>) | ![Sensitivity: bitnami/spark](<../../studies/chart-topologies/bitnami/spark/sensitivity.png>) |

[Sensitivity field key](#bitnamispark-1).

Overview cell: 102

Status: pending | Attempts: N/A

### [bitnami/superset](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/superset>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/superset](<../../studies/chart-topologies/bitnami/superset/topology.png>) | ![Sensitivity: bitnami/superset](<../../studies/chart-topologies/bitnami/superset/sensitivity.png>) |

Overview cell: 103

Status: pending | Attempts: N/A

### [bitnami/tensorflow-resnet](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tensorflow-resnet>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/tensorflow-resnet](<../../studies/chart-topologies/bitnami/tensorflow-resnet/topology.png>) | ![Sensitivity: bitnami/tensorflow-resnet](<../../studies/chart-topologies/bitnami/tensorflow-resnet/sensitivity.png>) |

[Sensitivity field key](#bitnamitensorflow-resnet-1).

Overview cell: 104

Status: pending | Attempts: N/A

### [bitnami/thanos](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/thanos>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/thanos](<../../studies/chart-topologies/bitnami/thanos/topology.png>) | ![Sensitivity: bitnami/thanos](<../../studies/chart-topologies/bitnami/thanos/sensitivity.png>) |

Overview cell: 105

Status: pending | Attempts: N/A

### [bitnami/tomcat](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tomcat>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/tomcat](<../../studies/chart-topologies/bitnami/tomcat/topology.png>) | ![Sensitivity: bitnami/tomcat](<../../studies/chart-topologies/bitnami/tomcat/sensitivity.png>) |

Overview cell: 106

Status: pending | Attempts: N/A

### [bitnami/valkey](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/valkey](<../../studies/chart-topologies/bitnami/valkey/topology.png>) | ![Sensitivity: bitnami/valkey](<../../studies/chart-topologies/bitnami/valkey/sensitivity.png>) |

Overview cell: 107

Status: pending | Attempts: N/A

### [bitnami/valkey-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey-cluster>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/valkey-cluster](<../../studies/chart-topologies/bitnami/valkey-cluster/topology.png>) | ![Sensitivity: bitnami/valkey-cluster](<../../studies/chart-topologies/bitnami/valkey-cluster/sensitivity.png>) |

[Sensitivity field key](#bitnamivalkey-cluster-1).

Overview cell: 108

Status: pending | Attempts: N/A

### [bitnami/vault](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/vault>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/vault](<../../studies/chart-topologies/bitnami/vault/topology.png>) | ![Sensitivity: bitnami/vault](<../../studies/chart-topologies/bitnami/vault/sensitivity.png>) |

[Sensitivity field key](#bitnamivault-1).

Overview cell: 109

Status: pending | Attempts: N/A

### [bitnami/victoriametrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/victoriametrics>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/victoriametrics](<../../studies/chart-topologies/bitnami/victoriametrics/topology.png>) | ![Sensitivity: bitnami/victoriametrics](<../../studies/chart-topologies/bitnami/victoriametrics/sensitivity.png>) |

[Sensitivity field key](#bitnamivictoriametrics-1).

Overview cell: 110

Status: pending | Attempts: N/A

### [bitnami/whereabouts](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/whereabouts>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/whereabouts](<../../studies/chart-topologies/bitnami/whereabouts/topology.png>) | ![Sensitivity: bitnami/whereabouts](<../../studies/chart-topologies/bitnami/whereabouts/sensitivity.png>) |

[Sensitivity field key](#bitnamiwhereabouts-1).

Overview cell: 111

Status: pending | Attempts: N/A

### [bitnami/wildfly](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wildfly>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/wildfly](<../../studies/chart-topologies/bitnami/wildfly/topology.png>) | ![Sensitivity: bitnami/wildfly](<../../studies/chart-topologies/bitnami/wildfly/sensitivity.png>) |

[Sensitivity field key](#bitnamiwildfly-1).

Overview cell: 112

Status: pending | Attempts: N/A

### [bitnami/wordpress](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wordpress>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/wordpress](<../../studies/chart-topologies/bitnami/wordpress/topology.png>) | ![Sensitivity: bitnami/wordpress](<../../studies/chart-topologies/bitnami/wordpress/sensitivity.png>) |

Overview cell: 113

Status: pending | Attempts: N/A

### [bitnami/zipkin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zipkin>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/zipkin](<../../studies/chart-topologies/bitnami/zipkin/topology.png>) | ![Sensitivity: bitnami/zipkin](<../../studies/chart-topologies/bitnami/zipkin/sensitivity.png>) |

Overview cell: 114

Status: pending | Attempts: N/A

### [bitnami/zookeeper](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zookeeper>)

| Chart topology | Mutation sensitivity |
| --- | --- |
| ![Topology: bitnami/zookeeper](<../../studies/chart-topologies/bitnami/zookeeper/topology.png>) | ![Sensitivity: bitnami/zookeeper](<../../studies/chart-topologies/bitnami/zookeeper/sensitivity.png>) |

[Sensitivity field key](#bitnamizookeeper-1).

Overview cell: 115

Status: pending | Attempts: N/A

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

### HH2006 - Opaque object schema

Default severity: **warning** | Category: values | Evidence type: warning

An object permits unspecified entries without named fields, patterned fields or a typed map-value schema.

Suggested action: Describe fields with properties, patternProperties or typed additionalProperties. Ignore
[HH2006](#hh2006---opaque-object-schema) for intentional free-form configuration; tests still sample those values.
