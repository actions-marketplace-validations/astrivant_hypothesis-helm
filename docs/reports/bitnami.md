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
  - [HH1001 - Unclassified template failure](#hh1001---unclassified-template-failure)
  - [HH1011 - Rendered output cannot be encoded as JSON](#hh1011---rendered-output-cannot-be-encoded-as-json)
  - [HH1101 - Invalid YAML in rendered output](#hh1101---invalid-yaml-in-rendered-output)
  - [HH1102 - Manifest document is not an object](#hh1102---manifest-document-is-not-an-object)
  - [HH1103 - Missing resource API version or kind](#hh1103---missing-resource-api-version-or-kind)
  - [HH1105 - Missing resource name](#hh1105---missing-resource-name)
  - [HH1106 - Duplicate resource identity](#hh1106---duplicate-resource-identity)
  - [HH1107 - Empty resource bundle](#hh1107---empty-resource-bundle)
  - [HH1108 - Kubernetes schema validation failed](#hh1108---kubernetes-schema-validation-failed)
  - [HH1109 - Invalid manifest field type](#hh1109---invalid-manifest-field-type)
  - [HH2001 - Undocumented values path](#hh2001---undocumented-values-path)
  - [HH2002 - Unspecified values type](#hh2002---unspecified-values-type)
  - [HH2003 - Missing values description](#hh2003---missing-values-description)
  - [HH2004 - No supplied default for a values path](#hh2004---no-supplied-default-for-a-values-path)
  - [HH2006 - Opaque object schema](#hh2006---opaque-object-schema)
  - [HH3001 - Template accesses a missing object](#hh3001---template-accesses-a-missing-object)
  - [HH3002 - Incompatible value type in template](#hh3002---incompatible-value-type-in-template)
  - [HH3003 - Undefined named template](#hh3003---undefined-named-template)

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
Started (Unix epoch): 1789870241
Started (UTC): 2026-09-20T02:10:41.000+00:00
Finished (UTC): 2026-09-20T13:14:59.619+00:00
Run fingerprint (SHA-256): `b8b9cd5915b50a4485d0a39dff3399f3b51066808ccf7dc2a32f63c4e2d2dae6`
Elapsed (wall clock): 35486.07 seconds
Chart testing: 34711.57 seconds
Dependency preparation: 759.56 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: completed
Discovery complete: True
Unstarted charts: 0

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

101 failed; 13 time-limit; 1 skipped-library.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: [HH2006](#hh2006---opaque-object-schema)

## Errors

605 distinct diagnostics across 934 occurrences; 329 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### [bitnami/airflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/airflow>)

Overview cell: 01

Status: failed | Attempts: 105

Audit findings: 1190. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.fernetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in JSON.

#### E535 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on airflow/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations.Nx_[[ of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations["Nx_[["] = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0000/paths/afbbf9ab6c6be5d414aa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0000>)

### [bitnami/apache](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apache>)

Overview cell: 02

Status: failed | Attempts: 512

Audit findings: 245. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 239 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E083 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 179: found unexpected end of
stream
```

Phase: $.htdocsConfigMap | Status: failed

Changed overrides (used together):
- `$.htdocsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0001/paths/a84b1abe3a11000d364a/report.json>)

#### E084 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0001/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0001/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E085 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0001/paths/8e79b7dd85a286cfaddb/report.json>)

#### E086 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0001/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0001>)

### [bitnami/apisix](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apisix>)

Overview cell: 03

Status: failed | Attempts: 109

Audit findings: 344. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.controlPlane.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controlPlane.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.vpa`: Missing values description (info)
- 338 additional audit findings in JSON.

#### E087 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apisix/charts/etcd/templates/svc-headless.yaml: error converting YAML to JSON: yaml: line 14: did not
find expected key
```

Phase: $.etcd.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.etcd.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.etcd.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0002/paths/0384c509a56911993ff8/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0002>)

### [bitnami/appsmith](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/appsmith>)

Overview cell: 04

Status: failed | Attempts: 151

Audit findings: 543. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.automountServiceAccountToken`: Undocumented values path (warning)
- 537 additional audit findings in JSON.

#### E082 ([HH1011](#hh1011---rendered-output-cannot-be-encoded-as-json))

**Rendered output cannot be encoded as JSON** (unclassified / diagnostic). Severity: **error**. Inspect YAML tags and parser support to
determine whether the failure comes from an unsupported value or a chart defect.

```text
[HH1011] The test tool could not convert a YAML-tagged value to JSON. See this chart's reproducing values. This diagnostic alone does not
establish a chart defect.
```

Phase: $.mongodb.persistence | Status: failed

Changed overrides (used together):
- `$.mongodb.persistence.subPath = "!r"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0003/paths/41d6ae6f8aea08087045/report.json>)

#### E536 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on appsmith/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0003/paths/afbbf9ab6c6be5d414aa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0003>)

### [bitnami/argo-cd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-cd>)

Overview cell: 05

Status: time-limit | Attempts: 1

Audit findings: 1251. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterAdminAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterRoleRules`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.containerPorts`: Undocumented values path (warning)
- 1245 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0004>)

### [bitnami/argo-workflows](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-workflows>)

Overview cell: 06

Status: failed | Attempts: 204

Audit findings: 452. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.automountServiceAccountToken`: Undocumented values path (warning)
- 446 additional audit findings in JSON.

#### E033 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0005/paths/1c25c32c569a13118399/report.json>)

#### E088 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on argo-workflows/templates/controller/clusterrolebinding.yaml: error converting YAML to JSON: yaml: line
24: found unexpected end of stream
```

Phase: $.controller.workflowNamespaces[*] | Status: failed

Changed overrides (used together):
- `$.controller.workflowNamespaces = ["'"]`
Absent from overrides: $.controller.workflowNamespaces["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0005/paths/d21976126c873fdee7bc/report.json>)

#### E537 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on argo-workflows/templates/controller/workflow-serviceaccount.yaml: error unmarshaling JSON: while
decoding JSON: json: cannot unmarshal object into Go struct field .metadata.annotations.\a4Za of type string
```

Phase: $.workflows.serviceAccount | Status: failed

Changed overrides (used together):
- `$.workflows.serviceAccount.annotations.max_repair_attempts = null`
- `$.workflows.serviceAccount.annotations.E = null`
- `$.workflows.serviceAccount.annotations["\n"] = null`
- `$.workflows.serviceAccount.annotations.a3Ma = null`
- `$.workflows.serviceAccount.annotations["aa5'Zc~FDasi"] = null`
- `$.workflows.serviceAccount.annotations["rRaU[aaz'apa"] = {}`
- 5 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0005/paths/c246ccf3c22f11e34d43/report.json>)

#### E564 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: argo-workflows/charts/mysql/templates/networkpolicy.yaml:72:69 executing
"argo-workflows/charts/mysql/templates/networkpolicy.yaml" at <$value.port>: nil pointer evaluating interface {}.port
```

Phase: $.mysql.primary.service.extraPorts | Status: failed

Changed overrides (used together):
- `$.mysql.enabled = true (was false)`
- `$.mysql.primary.service.extraPorts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0005/paths/cd1b3bd14efaf6a86788/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0005>)

### [bitnami/aspnet-core](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/aspnet-core>)

Overview cell: 07

Status: failed | Attempts: 643

Audit findings: 224. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.existingClaim`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone.depth`: Undocumented values path (warning)
- 218 additional audit findings in JSON.

Configuration rejections: 0 excluded; 25 adjusted and tested; 25 Helm verification renders (separate from manifest-test attempts).

#### E089 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.appFromExternalRepo.clone.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0006/paths/5a7bb70f23ca77d7dde5/report.json>)

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0006/paths/a4a0ea6ab697189bb963/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E090 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 55: could not find
expected ':'
```

Phase: $.appFromExternalRepo.clone.image.registry | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.appFromExternalRepo.clone.image.registry = "\r" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0006/paths/8cfc2368ac94f1308380/report.json>)

#### E091 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 66: mapping values are
not allowed in this context
```

Phase: $.appFromExternalRepo.publish.image.tag | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.tag = "" (was "9.0.304-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0006/paths/6f16a3fce30f040bbbba/report.json>)

#### E092 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 76: could not find
expected ':'
```

Phase: $.appFromExternalRepo.publish.extraFlags | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.extraFlags = [{"\r": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0006/paths/d6d30e52dda638aa651d/report.json>)

Phase: $.appFromExternalRepo.publish.subFolder | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.subFolder = "\n0" (was "aspnetcore/performance/caching/output/samples/8.x/")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0006/paths/d6eb74839ecc6561f2a6/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E093 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 83: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.0.8-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0006/paths/8e79b7dd85a286cfaddb/report.json>)

#### E094 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0006/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0006>)

### [bitnami/cadvisor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cadvisor>)

Overview cell: 08

Status: failed | Attempts: 583

Audit findings: 192. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.clusterDomain`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 186 additional audit findings in JSON.

Configuration rejections: 0 excluded; 19 adjusted and tested; 19 Helm verification renders (separate from manifest-test attempts).

#### E095 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 144: found unexpected end
of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0007/paths/57504c968732d9714f10/report.json>)

#### E096 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 35: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0007/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0007/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E097 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 60: found character that
cannot start any token
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.digest = "0" (was "")`
- `$.image.registry = "" (was "docker.io")`
- `$.image.repository = "" (was "bitnami/cadvisor")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0007/paths/8e79b7dd85a286cfaddb/report.json>)

#### E098 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/service.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0007/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0007>)

### [bitnami/cassandra](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cassandra>)

Overview cell: 09

Status: failed | Attempts: 360

Audit findings: 309. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.clientEncryption`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.datacenter`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.enableUDF`: Undocumented values path (warning)
- 303 additional audit findings in JSON.

Configuration rejections: 0 excluded; 21 adjusted and tested; 21 Helm verification renders (separate from manifest-test attempts).

#### E099 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 204: found unexpected
end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0008/paths/bc81b51736a9cdc4eda3/report.json>)

#### E100 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 31: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0008/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0008/paths/097f6358a00dddbcdd83/report.json>)

#### E101 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 68: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "5.0.5-debian-12-r7")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0008/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0008>)

### [bitnami/cert-manager](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cert-manager>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0009>)

### [bitnami/chainloop](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/chainloop>)

Overview cell: 11

Status: failed | Attempts: 163

Audit findings: 643. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 637 additional audit findings in JSON.

#### E102 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on chainloop/templates/controlplane/deployment.yaml: error converting YAML to JSON: yaml: line 60: did not
find expected alphabetic or numeric character
```

Phase: $.controlplane.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.controlplane.terminationGracePeriodSeconds = "&\n" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0010/paths/94d51abc8b5003c3268d/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0010>)

### [bitnami/cilium](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cilium>)

Overview cell: 12

Status: failed | Attempts: 277

Audit findings: 1163. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.agent.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling.vpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling.vpa.annotations`: Undocumented values path (warning)
- 1157 additional audit findings in JSON.

#### E518 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] level=INFO msg="warning: skipped value for etcd.configuration: Not a table." Error: YAML parse error on
cilium/charts/etcd/templates/svc-headless.yaml: error converting YAML to JSON: yaml: line 14: did not find expected key
```

Phase: $.etcd.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.etcd.enabled = true (was false)`
- `$.etcd.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.etcd.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0011/paths/0384c509a56911993ff8/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0011>)

### [bitnami/clickhouse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse>)

Overview cell: 13

Status: failed | Attempts: 482

Audit findings: 507. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 501 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E108 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse/templates/keeper/statefulset.yaml: error converting YAML to JSON: yaml: line 167: found
unexpected end of stream
```

Phase: $.keeper.persistence.storageClass | Status: failed

Changed overrides (used together):
- `$.keeper.persistence.storageClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0012/paths/f422c3354af3ff9d853e/report.json>)

#### E109 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse/templates/keeper/statefulset.yaml: error converting YAML to JSON: yaml: line 40: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0012/paths/a4a0ea6ab697189bb963/report.json>)

#### E110 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 177: found unexpected
end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0012/paths/bc81b51736a9cdc4eda3/report.json>)

#### E111 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 69: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "25.7.5-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0012/paths/8e79b7dd85a286cfaddb/report.json>)

#### E112 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse/templates/usersd-configmap.yaml: error converting YAML to JSON: yaml: line 14: did not find
expected key
```

Phase: $.usersdFiles | Status: failed

Changed overrides (used together):
- `$.usersdFiles[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0012/paths/638458d117473394e4a1/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0012>)

### [bitnami/clickhouse-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse-operator>)

Overview cell: 14

Status: failed | Attempts: 919

Audit findings: 276. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.username`: Undocumented values path (warning)
- 270 additional audit findings in JSON.

Configuration rejections: 0 excluded; 22 adjusted and tested; 22 Helm verification renders (separate from manifest-test attempts).

#### E103 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 33: did not
find expected key
```

Phase: $.podAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.podAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.podAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0013/paths/f8f1a4bfc6ad2b63681d/report.json>)

#### E104 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 35: did not
find expected key
```

Phase: $.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0013/paths/5996bd948f4d6447c879/report.json>)

#### E105 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 44: block
sequence entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0013/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0013/paths/097f6358a00dddbcdd83/report.json>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E106 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 68: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "0.25.3-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0013/paths/8e79b7dd85a286cfaddb/report.json>)

#### E107 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 70: could not
find expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/clickhouse-operator")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0013/paths/3f7165f1837241716c3c/report.json>)

#### E526 ([HH1106](#hh1106---duplicate-resource-identity))

**Duplicate resource identity** (manifest / violation). Severity: **error**. Give the resources distinct names or make their activation
conditions exclusive.

```text
[HH1106] duplicate resource: ('rbac.authorization.k8s.io/v1', 'Role', None, 'hypothesis-clickhouse-operator')
```

Phase: $.watchNamespaces | Status: failed

Changed overrides (used together):
- `$.watchNamespaces = [null, null]`

Manifest changes from rendered defaults (document and list order preserved):
- `$[11].metadata.namespace: "default" -> null`
- `$[12].kind: "RoleBinding" -> "Role"`
- `$[12].metadata.namespace: "default" -> null`
- `$[12].roleRef: {"apiGroup": "rbac.authorization.k8s.io", "kind": "Role", "name": "hypothesis-clickhouse-operator"} -> <absent>`
- `$[12].rules: <absent> -> [{"apiGroups": [""], "resources": ["configmaps", "services", "persistentvolumeclaims", "secrets"], "verbs": ["get", "lis... [value shortened]`
- `$[12].subjects: [{"kind": "ServiceAccount", "name": "hypothesis-clickhouse-operator", "namespace": "default"}] -> <absent>`
- 10 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0013/paths/b5cb98c4aed110d96476/report.json>)

#### E580 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: clickhouse-operator/templates/vpa.yaml:6:12 executing "clickhouse-operator/templates/vpa.yaml" at <include
"common.capabilities.apiVersions.has" (dict "version" "autoscaling.k8s.io/v1/VerticalPodAutoscaler" "context" .)>: error calling include:
template: no template "common.capabilities.apiVersions.has" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0013/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0013>)

### [bitnami/cloudnative-pg](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cloudnative-pg>)

Overview cell: 15

Status: failed | Attempts: 913

Audit findings: 423. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.extraDeploy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.fullnameOverride`: Undocumented values path (warning)
- 417 additional audit findings in JSON.

Configuration rejections: 0 excluded; 27 adjusted and tested; 29 Helm verification renders (separate from manifest-test attempts).

#### E076 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: cloudnative-pg 1.0.13 / templates/_helpers.tpl

```text
template: cloudnative-pg/templates/_helpers.tpl:20:11: executing "cloudnative-pg.operator.imagePullSecret" at <index
$pullSecretsYaml.imagePullSecrets 0>: error calling index: index of untyped nil
```

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/097f6358a00dddbcdd83/report.json>)

#### E113 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/deployment.yaml: error converting YAML to JSON: yaml: line 36: did not
find expected ',' or ']'
```

Phase: $.operator.postgresqlImage.pullSecrets | Status: failed

Changed overrides (used together):
- `$.operator.postgresqlImage.pullSecrets[""] = [null, []]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/3dcf6694cf8ac36c2d08/report.json>)

#### E114 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping
values are not allowed in this context
```

Phase: $.operator.image | Status: failed

Changed overrides (used together):
- `$.operator.image.tag = "" (was "1.27.0-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/b30a4eb2066aeb5f26ef/report.json>)

#### E115 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/deployment.yaml: error converting YAML to JSON: yaml: line 85: mapping
values are not allowed in this context
```

Phase: $.operator.postgresqlImage | Status: failed

Changed overrides (used together):
- `$.operator.postgresqlImage.tag = "" (was "17.6.0-debian-12-r4")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/b203e5d642851e3e429d/report.json>)

#### E116 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/deployment.yaml: error converting YAML to JSON: yaml: line 87: could
not find expected ':'
```

Phase: $.operator.postgresqlImage.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.operator.postgresqlImage.repository = "\r" (was "bitnami/postgresql")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/b18ff9103e270cddd433/report.json>)

#### E117 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/mutatingwebhookconfiguration.yaml: error converting YAML to JSON:
yaml: line 24: block sequence entries are not allowed in this context
```

Phase: $.operator.webhook | Status: failed

Changed overrides (used together):
- `$.operator.webhook.mutating.failurePolicy = "-" (was "Fail")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/95c373847fa437516b05/report.json>)

#### E118 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/validatingwebhookconfiguration.yaml: error converting YAML to JSON:
yaml: line 24: block sequence entries are not allowed in this context
```

Phase: $.operator.webhook.validating | Status: failed

Changed overrides (used together):
- `$.operator.webhook.validating.failurePolicy = "-" (was "Fail")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/8c104b857ff9d8b97822/report.json>)

#### E119 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/plugin-barman-cloud/deployment.yaml: error converting YAML to JSON: yaml: line
60: mapping values are not allowed in this context
```

Phase: $.pluginBarmanCloud.image.tag | Status: failed

Changed overrides (used together):
- `$.pluginBarmanCloud.image.tag = "" (was "0.6.0-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/53f5ef13d371739d3149/report.json>)

#### E120 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/plugin-barman-cloud/service.yaml: error converting YAML to JSON: yaml: line 18:
did not find expected key
```

Phase: $.pluginBarmanCloud.service.annotations[*] | Status: failed

Changed overrides (used together):
- `$.pluginBarmanCloud.service.annotations.__hypothesis_key__ = null`
Absent from overrides: $.pluginBarmanCloud.service.annotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/ab50764a40516f71fbfc/report.json>)

Phase: $.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/5996bd948f4d6447c879/report.json>)

#### E121 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/plugin-barman-cloud/service.yaml: error converting YAML to JSON: yaml: line 32:
found unexpected end of stream
```

Phase: $.pluginBarmanCloud.service.type | Status: failed

Changed overrides (used together):
- `$.pluginBarmanCloud.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/9e4dc7b804f2b964330c/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.operator.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.operator.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[13].subjects[0].name: "hypothesis-cloudnative-pg-operator" -> 0`
- `$[21].spec.template.spec.serviceAccountName: "hypothesis-cloudnative-pg-operator" -> 0`
- `$[4].metadata.name: "hypothesis-cloudnative-pg-operator" -> 0`
- `$[6].data["tls.crt"]: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURqRENDQW5TZ0F3SUJBZ0lSQUpqU2VQRktZblVkaVBST0RXNTd3Mmd3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURqRENDQW5TZ0F3SUJBZ0lSQU1RckdzUlREZStoSklnOFM2Z3k4ek13RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- `$[6].data["tls.key"]: "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBMk9DWThXd0IrdUFxc2dTTnFvNlZHN0E3aGZwQVkvRDlPK2p3K1NaRWJ... [value shortened] -> "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBMDlZalBjall2ek55WGNKNC9FbUEybVhZWSs5NWxXSU9uUnh3Z1lqU04... [value shortened]`
- `$[7].data["tls.crt"]: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURqRENDQW5TZ0F3SUJBZ0lSQUxRRTR5bm40Uzc1TWgvSDFyRzNsMFV3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURqRENDQW5TZ0F3SUJBZ0lSQU55ckp5MVJ2MHM3TGtRSGdrSXV3UTR3RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- 1 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0014/paths/2f03c3ff17482abfe351/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0014>)

### [bitnami/common](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/common>)

Overview cell: 16

Status: skipped-library | Attempts: N/A

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0015>)

### [bitnami/concourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/concourse>)

Overview cell: 17

Status: failed | Attempts: 490

Audit findings: 470. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 464 additional audit findings in JSON.

#### E010 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: concourse 5.1.47 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - abVb<aP/bitnami/concourse:e^a If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.r1gistry = null`
- `$.image.pullPolicy = "\\}a!*6@" (was "IfNotPresent")`
- `$.image.tag = "e^a\r" (was "7.13.2-debian-12-r12")`
- `$.image.registry = "abVb<aP" (was "docker.io")`
- `$.image[""] = [[], 185, {}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0016/paths/8e79b7dd85a286cfaddb/report.json>)

#### E122 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on concourse/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml:
line 187: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0016/paths/a0cdb2ba618083d9a8df/report.json>)

#### E123 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on concourse/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON: yaml:
line 17: could not find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0016/paths/91bb86cdd8574ec43d3d/report.json>)

#### E538 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on concourse/charts/postgresql/templates/primary/networkpolicy.yaml: error unmarshaling JSON: while
decoding JSON: json: cannot unmarshal array into Go struct field .metadata.name of type string
```

Phase: $.global.postgresql.auth | Status: failed

Changed overrides (used together):
- `$.global.postgresql.fullnameOverride = [null]`
- `$.global.postgresql.auth = {}`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0016/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0016>)

### [bitnami/consul](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/consul>)

Overview cell: 18

Status: failed | Attempts: 525

Audit findings: 255. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 249 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E124 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on consul/templates/service.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0017/paths/6e931799d09f8182f34b/report.json>)

#### E125 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on consul/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0017/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0017/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E126 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on consul/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 55: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.21.4-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0017/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0017>)

### [bitnami/contour](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/contour>)

Overview cell: 19

Status: failed | Attempts: 395

Audit findings: 591. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline["accesslog-format"]`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.disablePermitInsecure`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.tls`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.tls["fallback-certificate"]`: Undocumented values path (warning)
- 585 additional audit findings in JSON.

#### E539 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on contour/templates/contour/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.contour.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.contour.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0018/paths/850a7f073270a85899ed/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0018>)

### [bitnami/deepspeed](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/deepspeed>)

Overview cell: 20

Status: failed | Attempts: 204

Audit findings: 166. Full paths and template references are retained in the JSON report.

- [HH2002](#hh2002---unspecified-values-type) at `$.client.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.client.persistence.mountPath`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.client.client.persistence.mountPath`: No supplied default for a values
  path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.client.command[*]`: Unspecified values type (warning)
- [HH2003](#hh2003---missing-values-description) at `$.client.containerSecurityContext`: Missing values description (info)
- 160 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E011 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: deepspeed 2.3.51 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... tainers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/git:2.51.0-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.gitImage.registry | Status: failed

Changed overrides (used together):
- `$.gitImage.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0019/paths/47ebf688d3d510a9ed52/report.json>)

#### E012 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: deepspeed 2.3.51 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:0.17.5-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/deepspeed")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0019/paths/8e79b7dd85a286cfaddb/report.json>)

#### E127 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on deepspeed/templates/client/client-dep-job.yaml: error converting YAML to JSON: yaml: line 40: did not
find expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [null, {"": ""}, {"$h\"a5aaaaWaa": -4.443506336905391e+16, "K": null, "aaaaaa+\"*aa": 5640915261960171.0}, [{}, {}], {}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0019/paths/a4a0ea6ab697189bb963/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0019>)

### [bitnami/discourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/discourse>)

Overview cell: 21

Status: failed | Attempts: 138

Audit findings: 346. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.email`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.username`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth`: Undocumented values path (warning)
- 340 additional audit findings in JSON.

#### E540 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on discourse/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0020/paths/afbbf9ab6c6be5d414aa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0020>)

### [bitnami/dremio](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/dremio>)

Overview cell: 22

Status: failed | Attempts: 141

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

#### E013 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: dremio 3.1.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/dremio:26.0.0-debian-12-r5 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.dremio.image.registry | Status: failed

Changed overrides (used together):
- `$.dremio.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0021/paths/c5408860d7e66fba867d/report.json>)

#### E128 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on dremio/templates/bootstrap-user/job.yaml: error converting YAML to JSON: yaml: line 121: did not find
expected key
```

Phase: $.dremio.auth.username | Status: failed

Changed overrides (used together):
- `$.dremio.auth.username = "\r" (was "user")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0021/paths/7e3ba2e9db7688fe1f85/report.json>)

#### E129 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on dremio/templates/bootstrap-user/job.yaml: error converting YAML to JSON: yaml: line 143: did not find
expected alphabetic or numeric character
```

Phase: $.bootstrapUserJob.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.bootstrapUserJob.extraEnvVarsCM = "&\n" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0021/paths/5e487f511969b2a6049b/report.json>)

#### E130 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on dremio/templates/coordinator/statefulset.yaml: error converting YAML to JSON: yaml: line 371: did not
find expected alphabetic or numeric character
```

Phase: $.defaultInitContainers.generateConf.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.defaultInitContainers.generateConf.extraEnvVarsCM = "I\n&" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0021/paths/35af5d126ee937a46af9/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0021>)

### [bitnami/drupal](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/drupal>)

Overview cell: 23

Status: failed | Attempts: 464

Audit findings: 319. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.command`: Undocumented values path (warning)
- 313 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E021 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
execution error at (mariadb/templates/NOTES.txt:74:4): VALUES VALIDATION: mariadb: architecture Invalid architecture selected. Valid values
are "standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.mariadb.architecture | Status: failed

Changed overrides (used together):
- `$.mariadb.architecture = "" (was "standalone")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0022/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E022 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.registry = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0022/paths/3a6df6c30eb21f3e500a/report.json>)

#### E023 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0022/paths/e9b2bd06f74a17778834/report.json>)

#### E131 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on drupal/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 39:
did not find expected ',' or ']'
```

Phase: $.mariadb.volumePermissions.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0022/paths/1a4166aed8b35c7751ed/report.json>)

Phase: $.mariadb.metrics.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.metrics.image.pullSecrets = [[{"aaaaaaaaa\n0": "a", "discover": "a", "aaaaaaE": [100480376, true, true]}], {"": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0022/paths/f3c891b2fda1d97f28f1/report.json>)

#### E132 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on drupal/templates/deployment.yaml: error converting YAML to JSON: yaml: line 228: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0022/paths/bc81b51736a9cdc4eda3/report.json>)

#### E133 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on drupal/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image["JaaoUQ+c}\"p"] = null`
- `$.image[""] = null`
- `$.image.pullPolicy = "" (was "IfNotPresent")`
- `$.image.tag = "" (was "11.2.3-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0022/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0022>)

### [bitnami/ejbca](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ejbca>)

Overview cell: 24

Status: failed | Attempts: 562

Audit findings: 224. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- 218 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E014 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: ejbca 19.0.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - docker.io/ kL&%aa:9.1.1-debian-12-r12 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.ta = null`
- `$.image.int32[""]["aTaa-\\aaaaaaaa"] = [1.7976931348623157e+308, "O"]`
- `$.image.int32[""].aa = [true]`
- `$.image.int32[""].aaaaa = ["", false]`
- `$.image.int32.aaaaaa = []`
- `$.image.repository = "\nkL&%aa" (was "bitnami/ejbca")`
- 7 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0023/paths/8e79b7dd85a286cfaddb/report.json>)

#### E021 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
execution error at (mariadb/templates/NOTES.txt:74:4): VALUES VALIDATION: mariadb: architecture Invalid architecture selected. Valid values
are "standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.mariadb.architecture | Status: failed

Changed overrides (used together):
- `$.mariadb.architecture = "" (was "standalone")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0023/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E022 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.registry = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0023/paths/3a6df6c30eb21f3e500a/report.json>)

#### E023 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0023/paths/e9b2bd06f74a17778834/report.json>)

#### E134 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on ejbca/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 39:
did not find expected ',' or ']'
```

Phase: $.mariadb.volumePermissions.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0023/paths/1a4166aed8b35c7751ed/report.json>)

#### E135 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on ejbca/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 40:
did not find expected ',' or ']'
```

Phase: $.mariadb.metrics.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.metrics.image.pullSecrets = [null, [{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0023/paths/f3c891b2fda1d97f28f1/report.json>)

#### E136 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on ejbca/templates/deployment.yaml: error converting YAML to JSON: yaml: line 207: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0023/paths/bc81b51736a9cdc4eda3/report.json>)

#### E137 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on ejbca/templates/deployment.yaml: error converting YAML to JSON: yaml: line 32: did not find expected ','
or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [null, [{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0023/paths/a4a0ea6ab697189bb963/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0023>)

### [bitnami/elasticsearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/elasticsearch>)

Overview cell: 25

Status: failed | Attempts: 894

Audit findings: 814. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.config`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.containerPorts.restAPI`: Undocumented values path (warning)
- 808 additional audit findings in JSON.

Configuration rejections: 4 excluded; 10 adjusted and tested; 14 Helm verification renders (separate from manifest-test attempts).

#### E138 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/coordinating/statefulset.yaml: error converting YAML to JSON: yaml: line 234:
found unexpected end of stream
```

Phase: $.coordinating.schedulerName | Status: failed

Changed overrides (used together):
- `$.coordinating.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0024/paths/c725fa76dfbd1561269f/report.json>)

#### E139 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/coordinating/statefulset.yaml: error converting YAML to JSON: yaml: line 41:
block sequence entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0024/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.sysctlImage.pullSecrets[*] | Status: failed

Changed overrides (used together):
- `$.sysctlImage.pullSecrets = [[null]]`
Absent from overrides: $.sysctlImage.pullSecrets["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0024/paths/e326e771561b22095185/report.json>)

#### E140 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/ingest/statefulset.yaml: error converting YAML to JSON: yaml: line 25: could not
find expected ':'
```

Phase: $.ingest.nameOverride | Status: failed

Changed overrides (used together):
- `$.ingest.nameOverride = "\r" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0024/paths/9ad325076d817833ec6e/report.json>)

#### E141 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 245: found
unexpected end of stream
```

Phase: $.master.schedulerName | Status: failed

Changed overrides (used together):
- `$.master.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0024/paths/b3f60a0cb2adae0e1a9b/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.coordinating.fullnameOverride | Status: failed

Changed overrides (used together):
- `$.coordinating.fullnameOverride = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[0].metadata.name: "hypothesis-elasticsearch-coordinating" -> 0`
- `$[12].metadata.name: "hypothesis-elasticsearch-coordinating-hl" -> "0-hl"`
- `$[17].metadata.name: "hypothesis-elasticsearch-coordinating" -> 0`
- `$[17].spec.serviceName: "hypothesis-elasticsearch-coordinating-hl" -> "0-hl"`
- `$[17].spec.template.spec.containers[0].env[11].value: "$(MY_POD_NAME).hypothesis-elasticsearch-coordinating-hl.default.svc.cluster.local" -> "$(MY_POD_NAME).0-hl.default.svc.cluster.local"`
- `$[17].spec.template.spec.containers[0].env[7].value: "hypothesis-elasticsearch-master-hl.default.svc.cluster.local,hypothesis-elasticsearch-coordinating-hl.default.svc.clust... [value shortened] -> "hypothesis-elasticsearch-master-hl.default.svc.cluster.local,0-hl.default.svc.cluster.local,hypothesis-elasticsearch-da... [value shortened]`
- 6 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0024/paths/b8432c270c9ae0524afb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0024>)

### [bitnami/envoy-gateway](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/envoy-gateway>)

Overview cell: 26

Status: failed | Attempts: 400

Audit findings: 325. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 319 additional audit findings in JSON.

Configuration rejections: 0 excluded; 9 adjusted and tested; 9 Helm verification renders (separate from manifest-test attempts).

#### E142 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on envoy-gateway/templates/certgen/job.yaml: error converting YAML to JSON: yaml: line 33: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0025/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0025/paths/097f6358a00dddbcdd83/report.json>)

#### E143 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on envoy-gateway/templates/certgen/job.yaml: error converting YAML to JSON: yaml: line 41: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.5.0-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0025/paths/8e79b7dd85a286cfaddb/report.json>)

#### E144 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on envoy-gateway/templates/deployment.yaml: error converting YAML to JSON: yaml: line 93: could not find
expected ':'
```

Phase: $.ratelimitImage.digest | Status: failed

Changed overrides (used together):
- `$.ratelimitImage.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0025/paths/b56da783b3819637831b/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.certgen.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.certgen.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[11].spec.template.spec.serviceAccountName: "hypothesis-envoy-gateway-certgen" -> 0`
- `$[2].metadata.name: "hypothesis-envoy-gateway-certgen" -> 0`
- `$[5].subjects[0].name: "hypothesis-envoy-gateway-certgen" -> 0`
- `$[8].subjects[0].name: "hypothesis-envoy-gateway-certgen" -> 0`
- `$[9].subjects[0].name: "hypothesis-envoy-gateway-certgen" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0025/paths/3bafd983ae0b309b29cf/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0025>)

### [bitnami/etcd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/etcd>)

Overview cell: 27

Status: failed | Attempts: 292

Audit findings: 407. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.caFilename`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.certFilename`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.certKeyFilename`: Undocumented values path (warning)
- 401 additional audit findings in JSON.

Configuration rejections: 0 excluded; 5 adjusted and tested; 5 Helm verification renders (separate from manifest-test attempts).

#### E145 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on etcd/templates/preupgrade-hook-job.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0026/paths/a4a0ea6ab697189bb963/report.json>)

#### E146 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on etcd/templates/preupgrade-hook-job.yaml: error converting YAML to JSON: yaml: line 30: did not find
expected ',' or ']'
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image["000"] = null`
- `$.image.pullPolicy = "C\"8" (was "IfNotPresent")`
- ``$.image.registry = "a`C.%_qhq" (was "docker.io")``
- `$.image["5Ba"].Nas = []`
- `$.image["TtX_taQa(au|,J\"-a)"] = [[{"aa": []}, {}, [-16369, [], []]], {}, {"aaaa": "iaaaaaaa", "aaaxcaataasaaaa": true, "a*": null}]`
- 4 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0026/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0026>)

### [bitnami/external-dns](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/external-dns>)

Overview cell: 28

Status: failed | Attempts: 3274

Audit findings: 402. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.accessToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.clientSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.clientToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.host`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.secretName`: Undocumented values path (warning)
- 396 additional audit findings in JSON.

Configuration rejections: 0 excluded; 39 adjusted and tested; 39 Helm verification renders (separate from manifest-test attempts).

#### E015 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: external-dns 9.0.4 / templates/NOTES.txt

```text
execution error at (external-dns/templates/NOTES.txt:15:3): VALUES VALIDATION: external-dns: aws.assumeRoleArn The AWS Role to assume must
follow ARN format: `arn:aws:iam::123455567:role/external-dns` Ref:
https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html Please set a valid ARN (--set aws.assumeRoleARN="xxxx")
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.registry = "00" (was "docker.io")`
- `$.aws.assumeRoleArn = "example" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/8e79b7dd85a286cfaddb/report.json>)

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/external-dns")`
- `$.aws.assumeRoleArn = "example" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/3f7165f1837241716c3c/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E147 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/clusterrole.yaml: error converting YAML to JSON: yaml: line 123: did not find
expected alphabetic or numeric character
```

Phase: $.crd | Status: failed

Changed overrides (used together):
- `$.crd.apiversion = "&" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/774f347224e7442777b5/report.json>)

#### E148 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/clusterrole.yaml: error converting YAML to JSON: yaml: line 3: could not find
expected ':'
```

Phase: $.rbac.apiVersion | Status: failed

Changed overrides (used together):
- `$.rbac.apiVersion = "\n0" (was "v1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/e69069cd1d9fee6d24d5/report.json>)

#### E149 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/clusterrole.yaml: error converting YAML to JSON: yaml: line 6: could not find
expected ':'
```

Phase: $.namespaceOverride | Status: failed

Changed overrides (used together):
- `$.namespaceOverride = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/835d62e0a3e46b72c904/report.json>)

#### E150 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 125: found unexpected
end of stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/e4b1fa53526f192b7184/report.json>)

Phase: $.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/95d9e80fea15aed87f2a/report.json>)

#### E151 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 131: found unexpected
end of stream
```

Phase: $.aws.credentials.secretName | Status: failed

Changed overrides (used together):
- `$.aws.credentials.secretName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/9066c81ede4ae0ccf541/report.json>)

#### E152 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 28: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E153 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 59: did not find
expected key
```

Phase: $.excludeDomains | Status: failed

Changed overrides (used together):
- `$.excludeDomains = [[null, null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/b2d23655889f85d3952a/report.json>)

Phase: $.domainFilters | Status: failed

Changed overrides (used together):
- `$.domainFilters = [[null, null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/9740f35c2d5e35eba0d4/report.json>)

#### E154 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 66: could not find
expected ':'
```

Phase: $.logFormat | Status: failed

Changed overrides (used together):
- `$.logFormat = "\n0" (was "text")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/699f2b0cffa1417e6453/report.json>)

Phase: $.sources[*] | Status: failed

Changed overrides (used together):
- `$.sources = ["\n0", "ingress"]`
Absent from overrides: $.sources["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/cefe885437789bb081ba/report.json>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E155 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 67: could not find
expected ':'
```

Phase: $.zoneIdFilters[*] | Status: failed

Changed overrides (used together):
- `$.zoneIdFilters = ["\r0"]`
Absent from overrides: $.zoneIdFilters["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/af94618389499c220e76/report.json>)

Phase: $.regexDomainExclusion | Status: failed

Changed overrides (used together):
- `$.regexDomainExclusion = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/edeac4f78ac58c423cf1/report.json>)

11 additional occurrences are retained in the JSON report and chart artifacts.

#### E156 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 70: could not find
expected ':'
```

Phase: $.aws.zoneType | Status: failed

Changed overrides (used together):
- `$.aws.zoneType = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/52d21d658a5ad58923e4/report.json>)

#### E157 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 71: could not find
expected ':'
```

Phase: $.aws.zoneTags | Status: failed

Changed overrides (used together):
- `$.aws.zoneTags = [{"\r": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/798e8da1c0646feefff7/report.json>)

Phase: $.aws.dynamodbTable | Status: failed

Changed overrides (used together):
- `$.aws.dynamodbTable = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/c9b1ab3f25fd120432ec/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E158 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 72: could not find
expected ':'
```

Phase: $.extraArgs | Status: failed

Changed overrides (used together):
- `$.extraArgs["\n0"] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/6b07fe5f61f90919fc2a/report.json>)

#### E159 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 79: mapping keys are
not allowed in this context
```

Phase: $.txtEncrypt | Status: failed

Changed overrides (used together):
- `$.txtEncrypt.enabled = true (was false)`
- `$.txtEncrypt.secretName = "?" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/72339094c76ae22a3bae/report.json>)

#### E160 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/service.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end
of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/6e931799d09f8182f34b/report.json>)

#### E519 ([HH1102](#hh1102---manifest-document-is-not-an-object))

**Manifest document is not an object** (manifest / violation). Severity: **error**. Emit a resource mapping or remove the stray document.

```text
[HH1102] Error: YAML parse error on external-dns/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/90454abd7e30d38b69ee/report.json>)

#### E533 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.googleapis.com/v1/PodMonitoring requires an explicit JSON schema in resource_schemas
```

Phase: $.metrics | Status: failed

Changed overrides (used together):
- `$.metrics.enabled = true (was false)`
- `$.metrics.googlePodMonitor.enabled = true (was false)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[7]: <absent> -> {"apiVersion": "monitoring.googleapis.com/v1", "kind": "PodMonitoring", "metadata": {"name": "hypothesis-external-dns", ... [value shortened]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/17d970eb96f24f23c2d5/report.json>)

#### E581 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: external-dns/templates/_helpers.tpl:716:16 executing "external-dns.serviceAccountName" at <include "common.names.fullname"
.>: error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0027/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0027>)

### [bitnami/flink](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flink>)

Overview cell: 29

Status: failed | Attempts: 583

Audit findings: 281. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 275 additional audit findings in JSON.

Configuration rejections: 0 excluded; 21 adjusted and tested; 21 Helm verification renders (separate from manifest-test attempts).

#### E161 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on flink/templates/jobmanager/deployment.yaml: error converting YAML to JSON: yaml: line 36: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`
- `$.jobmanager.updateStrategy.rollingUpdate = null (was null)`
- `$.taskmanager.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0028/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`
- `$.jobmanager.updateStrategy.rollingUpdate = null (was null)`
- `$.taskmanager.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0028/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E162 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on flink/templates/jobmanager/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.1.0-debian-12-r1")`
- `$.jobmanager.updateStrategy.rollingUpdate = null (was null)`
- `$.taskmanager.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0028/paths/8e79b7dd85a286cfaddb/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.taskmanager.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.jobmanager.updateStrategy.rollingUpdate = null (was null)`
- `$.taskmanager.serviceAccount.name = "0" (was "")`
- `$.taskmanager.updateStrategy.rollingUpdate = null (was null)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[10].spec.updateStrategy.rollingUpdate: <absent> -> null`
- `$[5].metadata.name: "hypothesis-flink-taskmanager" -> 0`
- `$[9].spec.strategy.rollingUpdate: <absent> -> null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0028/paths/7af610caee367f12c985/report.json>)

#### E541 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on flink/templates/taskmanager/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.taskmanager.serviceAccount | Status: failed

Changed overrides (used together):
- `$.jobmanager.updateStrategy.rollingUpdate = null (was null)`
- `$.taskmanager.serviceAccount.annotations[""] = []`
- `$.taskmanager.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0028/paths/067a3a5b55160a73e780/report.json>)

Phase: $.taskmanager.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.jobmanager.updateStrategy.rollingUpdate = null (was null)`
- `$.taskmanager.serviceAccount.annotations[""] = []`
- `$.taskmanager.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0028/paths/87333782ef85d7076304/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0028>)

### [bitnami/fluent-bit](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluent-bit>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0029>)

### [bitnami/fluentd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluentd>)

Overview cell: 31

Status: time-limit | Attempts: 1

Audit findings: 427. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.aggregator.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.autoscaling`: Undocumented values path (warning)
- 421 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0030>)

### [bitnami/flux](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flux>)

Overview cell: 32

Status: time-limit | Attempts: 1

Audit findings: 1042. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 1036 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0031>)

### [bitnami/ghost](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ghost>)

Overview cell: 33

Status: failed | Attempts: 520

Audit findings: 262. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 256 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E016 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: ghost 25.0.5 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ...  chart with non-standard containers is likely to cause degraded security and performance,
broken chart features, and missing environment variables. Unrecognized images: - ;Zja/: If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image[""] = null`
- ``$.image["`aa"]["f%aaa~"] = [{"&aaaaaaa": "", "t": -2.220446049250313e-16, "a": null}, {"&%a,ap": false}, {"": 1.7976931348623157e+308,
  "aaa+": "|",... [value shortened]``
- `$.image.tag = "" (was "6.0.5-debian-12-r0")`
- `$.image[":Gosa%af<a"] = []`
- `$.image.pullSecrets = [{"3aa9\"aaaaaaaqaZ": [], "aaa": {"aa|HBa": -8541762688464932.0, "aayagaaaaa": ["", false, "aa8a."], "a^!)aaa": [false]}... [value shortened]`
- `$.image.registry = ";Zja" (was "docker.io")`
- 6 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0032/paths/8e79b7dd85a286cfaddb/report.json>)

#### E031 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mysql 14.0.3 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... kely to cause degraded security and performance, broken chart features, and missing
environment variables. Unrecognized images: - 00/bitnami/mysqld-exporter:0.17.2-debian-12-r16 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mysql.metrics.image | Status: failed

Changed overrides (used together):
- `$.mysql.metrics.image.registry = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0032/paths/5590c72bafc403304bea/report.json>)

#### E032 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mysql 14.0.3 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mysql.volumePermissions | Status: failed

Changed overrides (used together):
- `$.mysql.volumePermissions.image.registry = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0032/paths/006198abce843ffa5be2/report.json>)

#### E034 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mysql 14.0.3 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mysql.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.mysql.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0032/paths/1c25c32c569a13118399/report.json>)

#### E163 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on ghost/charts/mysql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 40: did
not find expected ',' or ']'
```

Phase: $.mysql.volumePermissions.image.pullSecrets[*] | Status: failed

Changed overrides (used together):
- `$.mysql.volumePermissions.image.pullSecrets = [[{}]]`
Absent from overrides: $.mysql.volumePermissions.image.pullSecrets["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0032/paths/25e1b252cef0182d6d1d/report.json>)

#### E565 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: ghost/charts/mysql/templates/networkpolicy.yaml:72:69 executing "ghost/charts/mysql/templates/networkpolicy.yaml" at
<$value.port>: nil pointer evaluating interface {}.port
```

Phase: $.mysql.primary.service.extraPorts | Status: failed

Changed overrides (used together):
- `$.mysql.primary.service.extraPorts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0032/paths/cd1b3bd14efaf6a86788/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0032>)

### [bitnami/gitea](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitea>)

Overview cell: 34

Status: failed | Attempts: 363

Audit findings: 241. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminUsername`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- 235 additional audit findings in JSON.

#### E017 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: gitea 3.2.23 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ...  with non-standard containers is likely to cause degraded security and performance,
broken chart features, and missing environment variables. Unrecognized images: - K/`a:TC!o<?a If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tg = null`
- `$.image[""] = [{"&": {"9aa?Vaaa": 134217727, "algorithm": -1040, "a": true}, "2a": {"aaAa.": null}, "": -2769514357177432.0}, [{"azaaa... [value shortened]`
- `$.image.tag = "TC!o<?a" (was "1.24.5-debian-12-r0")`
- `$.image[";b"][""].ak = {}`
- `$.image[";b"][""]["aaaaaF8aaaa]a"] = [false, {"": "", "a": null, ")aaa1a6aaa": false}]`
- `$.image[";b"][""].aa = [[-316], [true, -193422, true]]`
- 17 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0033/paths/8e79b7dd85a286cfaddb/report.json>)

#### E164 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitea/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON: yaml:
line 17: could not find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0033/paths/91bb86cdd8574ec43d3d/report.json>)

#### E165 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitea/templates/deployment.yaml: error converting YAML to JSON: yaml: line 202: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0033/paths/bc81b51736a9cdc4eda3/report.json>)

#### E574 ([HH3002](#hh3002---incompatible-value-type-in-template))

**Incompatible value type in template** (template / violation). Severity: **error**. Align the template operation with the accepted input
types, or narrow the schema.

```text
[HH3002] Error: gitea/charts/postgresql/templates/primary/statefulset.yaml:259:20 executing
"gitea/charts/postgresql/templates/primary/statefulset.yaml" at <include "postgresql.v1.database" .>: error calling include:
gitea/charts/postgresql/templates/_helpers.tpl:93:32 executing "postgresql.v1.database" at <.Values.global.postgresql.auth.database>: wrong
type for value; expected string; got float64
```

Phase: $.global.postgresql.auth | Status: failed

Changed overrides (used together):
- `$.global.postgresql.auth.database = 1`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0033/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0033>)

### [bitnami/gitlab-runner](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitlab-runner>)

Overview cell: 35

Status: failed | Attempts: 1900

Audit findings: 266. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 260 additional audit findings in JSON.

#### E166 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap-scripts.yaml: error converting YAML to JSON: yaml: line 143: could not
find expected ':'
```

Phase: $.preEntrypointScript | Status: failed

Changed overrides (used together):
- `$.preEntrypointScript = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/de7b54942a225a4ee446/report.json>)

#### E167 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 27: could not find
expected ':'
```

Phase: $.extraConfig | Status: failed

Changed overrides (used together):
- `$.extraConfig = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/d8ec1a80ed2510a23238/report.json>)

#### E168 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 29: could not find
expected ':'
```

Phase: $.runners.config | Status: failed

Changed overrides (used together):
- `$.runners.config = "\r0" (was "[[runners]]\n  [runners.kubernetes]\n    namespace = \"{{ include \"common.names.namespace\" . }}\"\n    image = \"{{ i... [value shortened])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/6a52673273db836d0a2b/report.json>)

Phase: $.connectionMaxAge | Status: failed

Changed overrides (used together):
- `$.connectionMaxAge = "\r" (was "15m")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/8b70cd8a98eac5050023/report.json>)

#### E169 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 30: could not find
expected ':'
```

Phase: $.namespaceOverride | Status: failed

Changed overrides (used together):
- `$.namespaceOverride = "\r" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/835d62e0a3e46b72c904/report.json>)

#### E170 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 31: could not find
expected ':'
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.digest = "\r" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/8e79b7dd85a286cfaddb/report.json>)

Phase: $.image.digest | Status: failed

Changed overrides (used together):
- `$.image.digest = "\r" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/10293d402dd6d1dd34f5/report.json>)

#### E171 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 32: could not find
expected ':'
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/fa90b40f46c6c70d8821/report.json>)

#### E172 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 35: could not find
expected ':'
```

Phase: $.helperImage.repository | Status: failed

Changed overrides (used together):
- `$.helperImage.repository = "\r" (was "bitnami/gitlab-runner-helper")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/1009129d047c87cec347/report.json>)

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "\r" (was "bitnami/gitlab-runner")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/3f7165f1837241716c3c/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E173 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 35: found unexpected
end of stream
```

Phase: $.helperImage.tag | Status: failed

Changed overrides (used together):
- `$.helperImage.tag = "\r" (was "18.3.0-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/bcb677a15437afb18f64/report.json>)

Phase: $.helperImage | Status: failed

Changed overrides (used together):
- `$.helperImage.digest = "\r" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/d30ab4b5dad27735101f/report.json>)

#### E174 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/session-server-ingress.yaml: error converting YAML to JSON: yaml: line 23: could
not find expected ':'
```

Phase: $.sessionServer | Status: failed

Changed overrides (used together):
- `$.sessionServer.enabled = true`
- `$.sessionServer.ingress.apiVersion = "aQ<gai>h5QD"`
- `$.sessionServer.ingress.enabled = true`
- `$.sessionServer.ingress.extraPaths = [{".": null}, null]`
- `$.sessionServer.ingress.path = "79c>a\nyJa3O{y"`
- `$.sessionServer.ingress.extraTls = [[]]`
- 1 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/c937e5032274cef11be2/observed-failure.json>)

#### E520 ([HH1102](#hh1102---manifest-document-is-not-an-object))

**Manifest document is not an object** (manifest / violation). Severity: **error**. Emit a resource mapping or remove the stray document.

```text
[HH1102] Error: YAML parse error on gitlab-runner/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/90454abd7e30d38b69ee/report.json>)

#### E582 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: gitlab-runner/templates/vpa.yaml:6:12 executing "gitlab-runner/templates/vpa.yaml" at <include
"common.capabilities.apiVersions.has" (dict "version" "autoscaling.k8s.io/v1/VerticalPodAutoscaler" "context" .)>: error calling include:
template: no template "common.capabilities.apiVersions.has" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0034/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0034>)

### [bitnami/grafana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana>)

Overview cell: 36

Status: failed | Attempts: 2568

Audit findings: 306. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.admin.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.user`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alerting.configMapName`: Undocumented values path (warning)
- 300 additional audit findings in JSON.

Configuration rejections: 298 excluded; 50 adjusted and tested; 349 Helm verification renders (separate from manifest-test attempts).

#### E079 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: grafana 12.1.9 / templates/_helpers.tpl

```text
template: grafana/templates/_helpers.tpl:133:10: executing "grafana.ldap.config" at <index (splitList ":" $hostPort) 1>: error calling
index: reflect: slice index out of range
```

Phase: $.ldap.enabled | Status: failed

Changed overrides (used together):
- `$.ldap.enabled = true (was false)`
- `$.ldap.uri = "example" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/7c7aed9d9832decc8a78/report.json>)

#### E181 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 142: found unexpected end
of stream
```

Phase: $.admin.existingSecret | Status: failed

Changed overrides (used together):
- `$.admin.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/545c0fac32c63b2ba504/report.json>)

#### E182 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 143: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/bc81b51736a9cdc4eda3/report.json>)

Phase: $.grafana.readinessProbe.path | Status: failed

Changed overrides (used together):
- `$.grafana.readinessProbe.path = "'" (was "/api/health")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/ba82d645e8d1de532a57/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E183 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 147: block sequence
entries are not allowed in this context
```

Phase: $.ldap.tls | Status: failed

Changed overrides (used together):
- `$.ldap.tls.certificatesSecret = "-" (was "")`
- `$.ldap.tls.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/2f1a6c3b04b1e1844c99/report.json>)

#### E184 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 147: mapping keys are not
allowed in this context
```

Phase: $.datasources | Status: failed

Changed overrides (used together):
- `$.datasources.secretName = "?" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/55aa3934a0f0892e931e/report.json>)

#### E185 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 148: found unexpected end
of stream
```

Phase: $.alerting | Status: failed

Changed overrides (used together):
- `$.alerting.configMapName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/95ff5d8789d2a3fdf062/report.json>)

Phase: $.notifiers | Status: failed

Changed overrides (used together):
- `$.notifiers.configMapName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/581f2a3411830ddd2aa7/report.json>)

4 additional occurrences are retained in the JSON report and chart artifacts.

#### E186 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 37: block sequence entries
are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E187 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 63: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "12.1.1-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/8e79b7dd85a286cfaddb/report.json>)

Phase: $.image.tag | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "12.1.1-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/7e365cc9986c8fb6c4ad/report.json>)

#### E188 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 65: could not find
expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/grafana")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/3f7165f1837241716c3c/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/fa90b40f46c6c70d8821/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E189 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/pvc.yaml: error converting YAML to JSON: yaml: line 19: found unexpected end of stream
```

Phase: $.global.defaultStorageClass | Status: failed

Changed overrides (used together):
- `$.global.defaultStorageClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/15f109ff720b0b1591be/report.json>)

#### E190 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/service.yaml: error converting YAML to JSON: yaml: line 25: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/6e931799d09f8182f34b/report.json>)

#### E521 ([HH1102](#hh1102---manifest-document-is-not-an-object))

**Manifest document is not an object** (manifest / violation). Severity: **error**. Emit a resource mapping or remove the stray document.

```text
[HH1102] Error: YAML parse error on grafana/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/90454abd7e30d38b69ee/report.json>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/fbfea8b96e1bf6abb6fc/report.json>)

#### E542 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on grafana/templates/pvc.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal array
into Go struct field .metadata.annotations. of type string
```

Phase: $.persistence.annotations | Status: failed

Changed overrides (used together):
- `$.persistence.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/10c7de62033351bf9ff1/report.json>)

#### E566 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: grafana/templates/application.yaml:225:72 executing "grafana/templates/application.yaml" at <.configMapName>: nil pointer
evaluating interface {}.configMapName
```

Phase: $.dashboardsConfigMaps[*] | Status: failed

Changed overrides (used together):
- `$.dashboardsConfigMaps = [null]`
Absent from overrides: $.dashboardsConfigMaps["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/5992333b51b6104e08ca/report.json>)

#### E567 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: grafana/templates/application.yaml:255:71 executing "grafana/templates/application.yaml" at <.name>: nil pointer evaluating
interface {}.name
```

Phase: $.grafana.extraConfigmaps | Status: failed

Changed overrides (used together):
- `$.grafana.extraConfigmaps = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/1c0b7d849095a07ac8ec/report.json>)

Phase: $.grafana.extraConfigmaps[*] | Status: failed

Changed overrides (used together):
- `$.grafana.extraConfigmaps = [null]`
Absent from overrides: $.grafana.extraConfigmaps["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/15d801a994a67336d282/report.json>)

#### E584 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: grafana/templates/serviceaccount.yaml:10:11 executing "grafana/templates/serviceaccount.yaml" at <include
"grafana.serviceAccountName" .>: error calling include: grafana/templates/_helpers.tpl:118:20 executing "grafana.serviceAccountName" at
<include "common.names.fullname" .>: error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/e2cac8a5225634937910/report.json>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0035/paths/2ff2aa2642f40d7be0f3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0035>)

### [bitnami/grafana-alloy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-alloy>)

Overview cell: 37

Status: time-limit | Attempts: 1

Audit findings: 292. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.name`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.portName`: Undocumented values path (warning)
- 286 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0036>)

### [bitnami/grafana-k6-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-k6-operator>)

Overview cell: 38

Status: failed | Attempts: 721

Audit findings: 195. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 189 additional audit findings in JSON.

Configuration rejections: 0 excluded; 36 adjusted and tested; 36 Helm verification renders (separate from manifest-test attempts).

#### E175 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-k6-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 36: did not
find expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0037/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0037/paths/097f6358a00dddbcdd83/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E176 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-k6-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "0.0.23-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0037/paths/8e79b7dd85a286cfaddb/report.json>)

#### E177 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-k6-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: could not
find expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/grafana-k6-operator")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0037/paths/3f7165f1837241716c3c/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0037/paths/fa90b40f46c6c70d8821/report.json>)

#### E178 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-k6-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 82: mapping
values are not allowed in this context
```

Phase: $.runnerImage.tag | Status: failed

Changed overrides (used together):
- `$.runnerImage.tag = "" (was "1.2.3-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0037/paths/ec2699463ba169ce5fd5/report.json>)

#### E179 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-k6-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 84: could not
find expected ':'
```

Phase: $.runnerImage.registry | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.runnerImage.registry = "\r" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0037/paths/43da1bc246e2f89450ac/report.json>)

#### E583 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: grafana-k6-operator/templates/vpa.yaml:6:12 executing "grafana-k6-operator/templates/vpa.yaml" at <include
"common.capabilities.apiVersions.has" (dict "version" "autoscaling.k8s.io/v1/VerticalPodAutoscaler" "context" .)>: error calling include:
template: no template "common.capabilities.apiVersions.has" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0037/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0037>)

### [bitnami/grafana-loki](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-loki>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0038>)

### [bitnami/grafana-mimir](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-mimir>)

Overview cell: 40

Status: time-limit | Attempts: 77

Audit findings: 1540. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage.backend`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage.config`: Undocumented values path (warning)
- 1534 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0039>)

### [bitnami/grafana-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-operator>)

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

#### E529 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource grafana.integreatly.org/v1beta1/Grafana requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0040/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0040>)

### [bitnami/grafana-tempo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-tempo>)

Overview cell: 42

Status: failed | Attempts: 166

Audit findings: 999. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.automountServiceAccountToken`: Undocumented values path (warning)
- 993 additional audit findings in JSON.

#### E180 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-tempo/templates/distributor/service.yaml: error converting YAML to JSON: yaml: line 40: found
unexpected end of stream
```

Phase: $.distributor.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.distributor.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0041/paths/9aef6208a1e363e5cf41/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0041>)

### [bitnami/haproxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/haproxy>)

Overview cell: 43

Status: failed | Attempts: 360

Audit findings: 186. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 180 additional audit findings in JSON.

Configuration rejections: 0 excluded; 9 adjusted and tested; 9 Helm verification renders (separate from manifest-test attempts).

#### E191 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on haproxy/templates/deployment.yaml: error converting YAML to JSON: yaml: line 35: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0042/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0042/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E192 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on haproxy/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "3.2.4-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0042/paths/8e79b7dd85a286cfaddb/report.json>)

#### E193 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on haproxy/templates/service.yaml: error converting YAML to JSON: yaml: line 25: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0042/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0042>)

### [bitnami/harbor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/harbor>)

Overview cell: 44

Status: failed | Attempts: 77

Audit findings: 1499. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache.expireHours`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificateVolume.resources`: Undocumented values path (warning)
- 1493 additional audit findings in JSON.

#### E543 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on harbor/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal object into Go struct field .metadata.annotations.Nx_[[ of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations["Nx_[["][""] = []`
- `$.redis.sentinel.service.headless.extraPorts = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0043/paths/afbbf9ab6c6be5d414aa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0043>)

### [bitnami/influxdb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/influxdb>)

Overview cell: 45

Status: failed | Attempts: 2138

Audit findings: 345. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.createAdminToken`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.createAdminToken`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- 339 additional audit findings in JSON.

Configuration rejections: 0 excluded; 51 adjusted and tested; 51 Helm verification renders (separate from manifest-test attempts).

#### E194 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on influxdb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 125: found unexpected end
of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/57504c968732d9714f10/report.json>)

#### E195 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on influxdb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 127: found unexpected end
of stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/e4b1fa53526f192b7184/report.json>)

#### E196 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on influxdb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 129: found unexpected end
of stream
```

Phase: $.initdbScriptsSecret | Status: failed

Changed overrides (used together):
- `$.initdbScriptsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/508ddee1274e004fe8b5/report.json>)

Phase: $.initdbScriptsCM | Status: failed

Changed overrides (used together):
- `$.initdbScriptsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/3252b1d9c3f1886ed39b/report.json>)

#### E197 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on influxdb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 36: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.defaultInitContainers.volumePermissions | Status: failed

Changed overrides (used together):
- `$.defaultInitContainers.volumePermissions.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/ba7812df7b1bf1a4d2b2/report.json>)

4 additional occurrences are retained in the JSON report and chart artifacts.

#### E198 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on influxdb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "3.4.1-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/8e79b7dd85a286cfaddb/report.json>)

#### E199 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on influxdb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 64: could not find
expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/influxdb")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/3f7165f1837241716c3c/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/fa90b40f46c6c70d8821/report.json>)

#### E200 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on influxdb/templates/service.yaml: error converting YAML to JSON: yaml: line 29: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/6e931799d09f8182f34b/report.json>)

#### E585 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: influxdb/templates/vpa.yaml:6:12 executing "influxdb/templates/vpa.yaml" at <include "common.capabilities.apiVersions.has"
(dict "version" "autoscaling.k8s.io/v1/VerticalPodAutoscaler" "context" .)>: error calling include: template: no template
"common.capabilities.apiVersions.has" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0044/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0044>)

### [bitnami/jaeger](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jaeger>)

Overview cell: 46

Status: time-limit | Attempts: 1

Audit findings: 404. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.cluster`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.cluster.datacenter`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cassandra.dbUser.user`: Undocumented values path (warning)
- 398 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0045>)

### [bitnami/janusgraph](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/janusgraph>)

Overview cell: 47

Status: failed | Attempts: 620

Audit findings: 328. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- 322 additional audit findings in JSON.

Configuration rejections: 6 excluded; 10 adjusted and tested; 16 Helm verification renders (separate from manifest-test attempts).

#### E009 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: cassandra 12.3.11 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.cassandra.dynamicSeedDiscovery.image.repository | Status: failed

Changed overrides (used together):
- `$.cassandra.dynamicSeedDiscovery.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0046/paths/c40b667a5f96c213ecf1/report.json>)

#### E201 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on janusgraph/charts/cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 204:
block sequence entries are not allowed in this context
```

Phase: $.cassandra.tls | Status: failed

Changed overrides (used together):
- `$.cassandra.tls.passwordsSecret = "-"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0046/paths/a077a8f76c5331673254/report.json>)

#### E202 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on janusgraph/charts/cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 232:
found unexpected end of stream
```

Phase: $.cassandra.persistence.commitLogMountPath | Status: failed

Changed overrides (used together):
- `$.cassandra.persistence.commitLogMountPath = "'"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0046/paths/12b50ce698cb59db09df/report.json>)

#### E203 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on janusgraph/templates/deployment.yaml: error converting YAML to JSON: yaml: line 39: block sequence
entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0046/paths/a4a0ea6ab697189bb963/report.json>)

#### E204 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on janusgraph/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.1.0-debian-12-r21")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0046/paths/8e79b7dd85a286cfaddb/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.cassandra.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.cassandra.serviceAccount.name = "0"`

Manifest changes from rendered defaults (document and list order preserved):
- `$[13].spec.template.spec.serviceAccountName: "hypothesis-cassandra" -> 0`
- `$[4].metadata.name: "hypothesis-cassandra" -> 0`
- `$[6].data["cassandra-password"]: "T0VGblhHdUtpSQ==" -> "cWZxdnNTRUF1OA=="`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0046/paths/d24e471a96b8372c3d8a/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0046>)

### [bitnami/jenkins](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jenkins>)

Overview cell: 48

Status: failed | Attempts: 465

Audit findings: 348. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.containerExtraEnvVars`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.containerSecurityContext`: Undocumented values path (warning)
- 342 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E205 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jenkins/templates/controller-svc.yaml: error converting YAML to JSON: yaml: line 28: found unexpected
end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0047/paths/6e931799d09f8182f34b/report.json>)

#### E206 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jenkins/templates/deployment.yaml: error converting YAML to JSON: yaml: line 162: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0047/paths/bc81b51736a9cdc4eda3/report.json>)

#### E207 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jenkins/templates/deployment.yaml: error converting YAML to JSON: yaml: line 34: block sequence entries
are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0047/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0047/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E208 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jenkins/templates/deployment.yaml: error converting YAML to JSON: yaml: line 57: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.516.2-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0047/paths/8e79b7dd85a286cfaddb/report.json>)

#### E209 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jenkins/templates/pvc.yaml: error converting YAML to JSON: yaml: line 13: did not find expected key
```

Phase: $.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0047/paths/5996bd948f4d6447c879/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0047>)

### [bitnami/jupyterhub](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jupyterhub>)

Overview cell: 49

Status: failed | Attempts: 433

Audit findings: 625. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.pullPolicy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.pullSecrets`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.registry`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.repository`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.tag`: Undocumented values path (warning)
- 619 additional audit findings in JSON.

#### E006 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: unable to detect chart at /var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/hypothesis-helm-scan-q651t4qz/chart/Chart.yaml:
open /var/folders/dd/pd400p1j4vgf5gv6qp6zfx000000gn/T/hypothesis-helm-scan-q651t4qz/chart/Chart.yaml: no such file or directory
```

Phase: $.proxy.service.public.loadBalancerIP | Status: failed

Changed overrides (used together):
- `$.proxy.service.public.loadBalancerIP = "0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0048/paths/b8ce65881d65d695d140/report.json>)

Phase: $.hub.image.pullPolicy | Status: failed

Changed overrides (used together):
- `$.hub.image.pullPolicy = "0" (was "IfNotPresent")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0048/paths/e5effc76fd5f5680e1fa/report.json>)

84 additional occurrences are retained in the JSON report and chart artifacts.

#### E532 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.coreos.com/v1/ServiceMonitor requires an explicit JSON schema in resource_schemas
```

Phase: $.hub.metrics.serviceMonitor | Status: failed

Changed overrides (used together):
- `$.hub.metrics.serviceMonitor.enabled = true (was false)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[13].data.password: "RXh0MldPbjlqWQ==" -> "dWJWdkVkd0xueA=="`
- `$[13].data["postgres-password"]: "WExlaVl5RU4wQQ==" -> "akh6UGNZWmxwZQ=="`
- `$[14].data["hub.config.CryptKeeper.keys"]: "YTNlYjAyZTBlMzljZGZmNWE2OGMyOWYyYWFiYWVmNTdmYTNkYmQzYjAzMzg2YmQ3YjdmMThhNWIxMzhkOTcyYQ==" -> "MDQ3OGQzNzU5MDIxMzZiNDM0ZDBmYmJmNGVmNzJhMzJlMGM4NTcwM2VhOWJiMzY1YWNhNzkzMDNjNGM0ZDNkYw=="`
- `$[14].data["hub.config.JupyterHub.cookie_secret"]: "YTU2YmFiMGEwOTQ1OWFlMjdkZTEzYzJkZDllYWE2NjA2NWViZDZhZjI5ODZhMmEyNDA3ZmFmODEyMDE1ZjQyYg==" -> "YmI2YzY0MDAwMTVjMmFjYjhkOTQxNjA0ZmU3ZWM2OWVkZDQyMmFmY2I1ZjM1MGZlN2RjOWM5MTBmZjRkODNhNg=="`
- `$[14].data["proxy-token"]: "TnRVQndodlhCVlkxNHVOSW1lakpWMjc2NHV0WWw3a2M=" -> "TlUwTllTZVJveGE3dlZncURhQ1JoUHFkd3hsbldvU0s="`
- `$[14].data["values.yaml"]: "Q2hhcnQ6CiAgTmFtZToganVweXRlcmh1YgogIFZlcnNpb246IDEwLjAuNgpSZWxlYXNlOgogIE5hbWU6IGh5cG90aGVzaXMKICBOYW1lc3BhY2U6IGRlZmF... [value shortened] -> "Q2hhcnQ6CiAgTmFtZToganVweXRlcmh1YgogIFZlcnNpb246IDEwLjAuNgpSZWxlYXNlOgogIE5hbWU6IGh5cG90aGVzaXMKICBOYW1lc3BhY2U6IGRlZmF... [value shortened]`
- 4 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0048/paths/373db267daac756f7747/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0048>)

### [bitnami/kafka](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kafka>)

Overview cell: 50

Status: failed | Attempts: 714

Audit findings: 790. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$[""]`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$[""]`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.automountServiceAccountToken`: Undocumented values path (warning)
- 784 additional audit findings in JSON.

Configuration rejections: 49 excluded; 11 adjusted and tested; 61 Helm verification renders (separate from manifest-test attempts).

#### E210 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kafka/templates/controller-eligible/statefulset.yaml: error converting YAML to JSON: yaml: line 105: did
not find expected key
```

Phase: $.controller.topologyKey | Status: failed

Changed overrides (used together):
- `$.controller.topologyKey = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0049/paths/96bdd08b814a4c59648f/report.json>)

#### E211 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kafka/templates/controller-eligible/statefulset.yaml: error converting YAML to JSON: yaml: line 106: did
not find expected key
```

Phase: $.controller.runtimeClassName | Status: failed

Changed overrides (used together):
- `$.controller.runtimeClassName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0049/paths/f82d28e2c30ee5985d85/report.json>)

#### E212 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kafka/templates/controller-eligible/statefulset.yaml: error converting YAML to JSON: yaml: line 40: did
not find expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0049/paths/a4a0ea6ab697189bb963/report.json>)

#### E213 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kafka/templates/controller-eligible/statefulset.yaml: error converting YAML to JSON: yaml: line 71:
mapping values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "4.0.0-debian-12-r10")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0049/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0049>)

### [bitnami/keycloak](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keycloak>)

Overview cell: 51

Status: failed | Attempts: 403

Audit findings: 448. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminRealm`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminUser`: Undocumented values path (warning)
- 442 additional audit findings in JSON.

Configuration rejections: 0 excluded; 27 adjusted and tested; 27 Helm verification renders (separate from manifest-test attempts).

#### E515 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] level=INFO msg="warning: destination for postgresql.tls.autoGenerated is a table. Ignoring non-table value (false)" Error: YAML
parse error on keycloak/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 189: found
unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0050/paths/a0cdb2ba618083d9a8df/report.json>)

#### E516 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] level=INFO msg="warning: destination for postgresql.tls.autoGenerated is a table. Ignoring non-table value (false)" Error: YAML
parse error on keycloak/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON: yaml: line 17: could not
find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0050/paths/91bb86cdd8574ec43d3d/report.json>)

#### E517 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] level=INFO msg="warning: destination for postgresql.tls.autoGenerated is a table. Ignoring non-table value (false)" Error: YAML
parse error on keycloak/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 43: block sequence entries are not allowed in
this context
```

Phase: $.keycloakConfigCli | Status: failed

Changed overrides (used together):
- `$.keycloakConfigCli.image.digest = "YaaVa+aWCaa>K@" (was "")`
- `$.keycloakConfigCli.image.Scunthorpe = [null, false]`
- `$.keycloakConfigCli.image.pullPolicy = "" (was "IfNotPresent")`
- `$.keycloakConfigCli.image.registry = "" (was "docker.io")`
- `$.keycloakConfigCli.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0050/paths/833e1ce85b0d7e5a8ef8/report.json>)

#### E563 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] level=INFO msg="warning: destination for postgresql.tls.autoGenerated is a table. Ignoring non-table value (false)" Error: YAML
parse error on keycloak/charts/postgresql/templates/primary/networkpolicy.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.name of type string
```

Phase: $.global.postgresql.auth | Status: failed

Changed overrides (used together):
- `$.global.postgresql.fullnameOverride = [null]`
- `$.global.postgresql.auth = {}`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0050/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0050>)

### [bitnami/keydb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keydb>)

Overview cell: 52

Status: failed | Attempts: 1696

Audit findings: 499. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 493 additional audit findings in JSON.

Configuration rejections: 0 excluded; 39 adjusted and tested; 39 Helm verification renders (separate from manifest-test attempts).

#### E214 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/master/configmap.yaml: error converting YAML to JSON: yaml: line 26: did not find
expected key
```

Phase: $.master.disableCommands | Status: failed

Changed overrides (used together):
- `$.master.disableCommands = ["\r"]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/ae04aa76885c44fa960f/report.json>)

#### E215 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 157: did not find
expected node content
```

Phase: $.auth | Status: failed

Changed overrides (used together):
- `$.auth.existingSecret = "{" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/9add85c17048305af4de/report.json>)

#### E216 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 169: found unexpected
end of stream
```

Phase: $.master.existingConfigmap | Status: failed

Changed overrides (used together):
- `$.master.existingConfigmap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/c2930e17c4b06f467ab5/report.json>)

#### E217 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 170: found unexpected
end of stream
```

Phase: $.master.persistence.storageClass | Status: failed

Changed overrides (used together):
- `$.master.persistence.storageClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/8b1730de40416f0c86e2/report.json>)

#### E218 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 40: block sequence
entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/097f6358a00dddbcdd83/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E219 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 61: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "6.3.4-debian-12-r24")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/8e79b7dd85a286cfaddb/report.json>)

#### E220 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 63: could not find
expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.diagnosticMode.enabled = true (was false)`
- `$.image.repository = "\r" (was "bitnami/keydb")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/3f7165f1837241716c3c/report.json>)

#### E221 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/configmap.yaml: error converting YAML to JSON: yaml: line 27: did not find
expected key
```

Phase: $.replica.disableCommands | Status: failed

Changed overrides (used together):
- `$.replica.disableCommands = ["\r"]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/9ab33350907009275568/report.json>)

#### E222 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/networkpolicy.yaml: error converting YAML to JSON: yaml: line 39: mapping values
are not allowed in this context
```

Phase: $.replica.networkPolicy | Status: failed

Changed overrides (used together):
- `$.replica.networkPolicy.allowExternalEgress = false (was true)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/ead96de3dd100ee4f6d1/report.json>)

#### E223 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/service.yaml: error converting YAML to JSON: yaml: line 28: found unexpected end
of stream
```

Phase: $.replica.service.clusterIP | Status: failed

Changed overrides (used together):
- `$.replica.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/c472c95b8d817657b6a5/report.json>)

#### E224 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/statefulset.yaml: error converting YAML to JSON: yaml: line 167: found
unexpected end of stream
```

Phase: $.replica.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.replica.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/6779164cb76c2dbb83a8/report.json>)

#### E225 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/statefulset.yaml: error converting YAML to JSON: yaml: line 175: found
unexpected end of stream
```

Phase: $.replica.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.replica.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/dadf473ae2669113900c/report.json>)

#### E226 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/statefulset.yaml: error converting YAML to JSON: yaml: line 177: found
unexpected end of stream
```

Phase: $.replica.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.replica.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/b71ec3b23bacb342be46/report.json>)

Phase: $.replica.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.replica.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/f76951b7203d44d5892f/report.json>)

#### E586 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: keydb/templates/replica/vpa.yaml:6:52 executing "keydb/templates/replica/vpa.yaml" at <include
"common.capabilities.apiVersions.has" (dict "version" "autoscaling.k8s.io/v1/VerticalPodAutoscaler" "context" .)>: error calling include:
template: no template "common.capabilities.apiVersions.has" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0051/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0051>)

### [bitnami/kibana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kibana>)

Overview cell: 53

Status: failed | Attempts: 3157

Audit findings: 257. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 251 additional audit findings in JSON.

Configuration rejections: 2 excluded; 54 adjusted and tested; 56 Helm verification renders (separate from manifest-test attempts).

#### E227 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kibana/templates/plugins-configmap.yaml: error converting YAML to JSON: yaml: line 19: could not find
expected ':'
```

Phase: $.plugins[*] | Status: failed

Changed overrides (used together):
- `$.plugins = ["\r"]`
Absent from overrides: $.plugins["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/c35a8623255cf085a701/report.json>)

#### E228 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kibana/templates/plugins-configmap.yaml: error converting YAML to JSON: yaml: line 20: could not find
expected ':'
```

Phase: $.plugins | Status: failed

Changed overrides (used together):
- `$.plugins = [{"\r": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/57bb848b585779b7d79f/report.json>)

#### E229 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kibana/templates/pvc.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of stream
```

Phase: $.global.defaultStorageClass | Status: failed

Changed overrides (used together):
- `$.global.defaultStorageClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/15f109ff720b0b1591be/report.json>)

Phase: $.global.storageClass | Status: failed

Changed overrides (used together):
- `$.global.storageClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/1b2b179e28bf79ae3d32/report.json>)

#### E230 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kibana/templates/saved-objects-configmap.yaml: error converting YAML to JSON: yaml: line 21: could not
find expected ':'
```

Phase: $.savedObjects.urls[*] | Status: failed

Changed overrides (used together):
- `$.savedObjects.urls = ["\r"]`
Absent from overrides: $.savedObjects.urls["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/a6f6f9ef6baebdcdc45a/report.json>)

#### E231 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kibana/templates/saved-objects-configmap.yaml: error converting YAML to JSON: yaml: line 23: could not
find expected ':'
```

Phase: $.savedObjects.urls | Status: failed

Changed overrides (used together):
- `$.savedObjects.urls = [{"\r": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/7353f861890968cecbe7/report.json>)

Phase: $.savedObjects | Status: failed

Changed overrides (used together):
- `$.savedObjects.urls = [{"\n": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/2d9e0e00b743a087b7d3/report.json>)

#### E232 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kibana/templates/service.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/6e931799d09f8182f34b/report.json>)

#### E233 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kibana/templates/service.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end of
stream
```

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/12b3c4a215648c1d6dd7/report.json>)

#### E234 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kibana/templates/service.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end of
stream
```

Phase: $.service.clusterIP | Status: failed

Changed overrides (used together):
- `$.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/dbb776e6ea555257fb86/report.json>)

#### E522 ([HH1102](#hh1102---manifest-document-is-not-an-object))

**Manifest document is not an object** (manifest / violation). Severity: **error**. Emit a resource mapping or remove the stray document.

```text
[HH1102] Error: YAML parse error on kibana/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/90454abd7e30d38b69ee/report.json>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/fbfea8b96e1bf6abb6fc/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[1].metadata.name: "hypothesis-kibana" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/815bf9b751b356e044f0/report.json>)

Phase: $.fullnameOverride | Status: failed

Changed overrides (used together):
- `$.fullnameOverride = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[0].metadata.name: "hypothesis-kibana" -> 0`
- `$[1].metadata.name: "hypothesis-kibana" -> 0`
- `$[2].metadata.name: "hypothesis-kibana" -> 0`
- `$[3].metadata.name: "hypothesis-kibana" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/e2f7761f901d86846684/report.json>)

#### E575 ([HH3002](#hh3002---incompatible-value-type-in-template))

**Incompatible value type in template** (template / violation). Severity: **error**. Align the template operation with the accepted input
types, or narrow the schema.

```text
[HH3002] Error: kibana/templates/deployment.yaml:158:24 executing "kibana/templates/deployment.yaml" at <include "kibana.elasticsearch.url"
.>: error calling include: kibana/templates/_helpers.tpl:46:17 executing "kibana.elasticsearch.url" at <$hostTemplate>: wrong type for
value; expected string; got interface {}
```

Phase: $.elasticsearch | Status: failed

Changed overrides (used together):
- `$.elasticsearch.port = "0" (was "")`
- `$.elasticsearch.hosts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/ad5df332ced8cb7aace5/report.json>)

#### E576 ([HH3002](#hh3002---incompatible-value-type-in-template))

**Incompatible value type in template** (template / violation). Severity: **error**. Align the template operation with the accepted input
types, or narrow the schema.

```text
[HH3002] Error: kibana/templates/serviceaccount.yaml:11:16 executing "kibana/templates/serviceaccount.yaml" at <include
"common.names.namespace" .>: error calling include: kibana/charts/common/templates/_names.tpl:64:65 executing "common.names.namespace" at
<63>: wrong type for value; expected string; got []interface {}
```

Phase: $.namespaceOverride | Status: failed

Changed overrides (used together):
- `$.namespaceOverride = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/835d62e0a3e46b72c904/report.json>)

#### E587 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: kibana/templates/_helpers.tpl:267:16 executing "kibana.serviceAccountName" at <include "common.names.fullname" .>: error
calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/e2cac8a5225634937910/report.json>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0052/paths/2ff2aa2642f40d7be0f3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0052>)

### [bitnami/kong](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kong>)

Overview cell: 54

Status: failed | Attempts: 383

Audit findings: 390. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.metrics`: Undocumented values path (warning)
- 384 additional audit findings in JSON.

#### E235 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kong/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line
189: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0053/paths/a0cdb2ba618083d9a8df/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0053>)

### [bitnami/kube-arangodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-arangodb>)

Overview cell: 55

Status: failed | Attempts: 295

Audit findings: 324. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowChaos`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arangodbImage.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arangodbImage.pullSecrets`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.arangodbImage.pullSecrets`: No supplied default for a values path
  (warning)
- 318 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E236 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-arangodb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 38: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0054/paths/a4a0ea6ab697189bb963/report.json>)

#### E237 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-arangodb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.3.0-debian-12-r4")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0054/paths/8e79b7dd85a286cfaddb/report.json>)

#### E238 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-arangodb/templates/service.yaml: error converting YAML to JSON: yaml: line 39: found unexpected end
of stream
```

Phase: $.service.nodePorts.apiGrpc | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.apiGrpc = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0054/paths/5e977ce661c5834a77a0/report.json>)

#### E512 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] invalid rendered YAML: while constructing a mapping in "<unicode string>", line 1010, column 3: namespace: "default" ^ (line: 1010)
found duplicate key "namespace" with value "default" (original value: "default") in "<unicode string>", line 1011, column 3: namespace:
"default" ^ (line: 1011) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.autoscaling.hpa.enabled | Status: failed

Changed overrides (used together):
- `$.autoscaling.hpa.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0054/paths/d461ce5afe144683ffee/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.serviceAccount.operator.name | Status: failed

Changed overrides (used together):
- `$.serviceAccount.operator.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[10].subjects[0].name: "hypothesis-kube-arangodb" -> 0`
- `$[11].subjects[0].name: "hypothesis-kube-arangodb" -> 0`
- `$[12].subjects[0].name: "hypothesis-kube-arangodb" -> 0`
- `$[13].subjects[0].name: "hypothesis-kube-arangodb" -> 0`
- `$[14].subjects[0].name: "hypothesis-kube-arangodb" -> 0`
- `$[15].subjects[0].name: "hypothesis-kube-arangodb" -> 0`
- 9 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0054/paths/95bc8b2087be846a7d07/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0054>)

### [bitnami/kube-prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus>)

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

#### E530 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.coreos.com/v1/Alertmanager requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0055/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0055>)

### [bitnami/kube-prometheus/charts/kube-prometheus-crds](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus/charts/kube-prometheus-crds>)

Overview cell: 57

Status: failed | Attempts: 1

Audit findings: 1. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.exampleValue`: Undocumented values path (warning)

#### E527 ([HH1107](#hh1107---empty-resource-bundle))

**Empty resource bundle** (manifest / violation). Severity: **error**. Check resource activation; ignore this contract if an empty chart is
intentional.

```text
[HH1107] chart rendered no resources
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0056/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0056>)

### [bitnami/kube-state-metrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-state-metrics>)

Overview cell: 58

Status: failed | Attempts: 367

Audit findings: 208. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- 202 additional audit findings in JSON.

Configuration rejections: 0 excluded; 9 adjusted and tested; 9 Helm verification renders (separate from manifest-test attempts).

#### E239 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-state-metrics/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: block
sequence entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0057/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0057/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E240 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-state-metrics/templates/deployment.yaml: error converting YAML to JSON: yaml: line 55: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.16.0-debian-12-r5")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0057/paths/8e79b7dd85a286cfaddb/report.json>)

#### E241 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-state-metrics/templates/service.yaml: error converting YAML to JSON: yaml: line 14: did not find
expected key
```

Phase: $.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0057/paths/5996bd948f4d6447c879/report.json>)

#### E242 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-state-metrics/templates/service.yaml: error converting YAML to JSON: yaml: line 26: found
unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0057/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0057>)

### [bitnami/kuberay](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kuberay>)

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

#### E534 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource ray.io/v1/RayCluster requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0058/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0058>)

### [bitnami/kubernetes-event-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kubernetes-event-exporter>)

Overview cell: 60

Status: failed | Attempts: 615

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.vpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.vpa.annotations`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

Configuration rejections: 0 excluded; 18 adjusted and tested; 18 Helm verification renders (separate from manifest-test attempts).

#### E243 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kubernetes-event-exporter/templates/deployment.yaml: error converting YAML to JSON: yaml: line 115:
found unexpected end of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0059/paths/57504c968732d9714f10/report.json>)

#### E244 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kubernetes-event-exporter/templates/deployment.yaml: error converting YAML to JSON: yaml: line 27: did
not find expected key
```

Phase: $.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0059/paths/5996bd948f4d6447c879/report.json>)

#### E245 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kubernetes-event-exporter/templates/deployment.yaml: error converting YAML to JSON: yaml: line 35: did
not find expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0059/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0059/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E246 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kubernetes-event-exporter/templates/deployment.yaml: error converting YAML to JSON: yaml: line 59:
mapping values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.7.0-debian-12-r46")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0059/paths/8e79b7dd85a286cfaddb/report.json>)

#### E247 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kubernetes-event-exporter/templates/deployment.yaml: error converting YAML to JSON: yaml: line 61: could
not find expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/kubernetes-event-exporter")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0059/paths/3f7165f1837241716c3c/report.json>)

#### E588 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: kubernetes-event-exporter/templates/vpa.yaml:6:12 executing "kubernetes-event-exporter/templates/vpa.yaml" at <include
"common.capabilities.apiVersions.has" (dict "version" "autoscaling.k8s.io/v1/VerticalPodAutoscaler" "context" .)>: error calling include:
template: no template "common.capabilities.apiVersions.has" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0059/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0059>)

### [bitnami/logstash](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/logstash>)

Overview cell: 61

Status: failed | Attempts: 630

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E248 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/configuration-cm.yaml: error converting YAML to JSON: yaml: line 31: could not find
expected ':'
```

Phase: $.filter | Status: failed

Changed overrides (used together):
- `$.filter = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0060/paths/0e1e9caa4953f85afca2/report.json>)

#### E249 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 25: block sequence
entries are not allowed in this context
```

Phase: $.containerPorts[*] | Status: failed

Changed overrides (used together):
- `$.containerPorts = [{"protocol": "-"}]`
Absent from overrides: $.containerPorts["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0060/paths/f06f7a6cb7546d67e970/report.json>)

#### E250 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 26: did not find
expected '-' indicator
```

Phase: $.networkPolicy.customRules | Status: failed

Changed overrides (used together):
- `$.networkPolicy.customRules[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0060/paths/1d6a5faf6612f0fc5d5a/report.json>)

#### E251 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/sts.yaml: error converting YAML to JSON: yaml: line 141: found unexpected end of
stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0060/paths/57504c968732d9714f10/report.json>)

#### E252 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/sts.yaml: error converting YAML to JSON: yaml: line 34: block sequence entries are
not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0060/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0060/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E253 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/sts.yaml: error converting YAML to JSON: yaml: line 58: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.1.2-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0060/paths/8e79b7dd85a286cfaddb/report.json>)

#### E254 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/svc.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0060/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0060>)

### [bitnami/mariadb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb>)

Overview cell: 62

Status: failed | Attempts: 559

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

#### E262 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 208: found
unexpected end of stream
```

Phase: $.primary.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.primary.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0061/paths/9500a72d3c4e020c37bd/report.json>)

#### E263 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 220: found
unexpected end of stream
```

Phase: $.primary.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.primary.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0061/paths/af9a77b4b696ef0a07df/report.json>)

#### E264 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 39: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0061/paths/a4a0ea6ab697189bb963/report.json>)

#### E265 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 64: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "12.0.2-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0061/paths/8e79b7dd85a286cfaddb/report.json>)

#### E266 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb/templates/primary/svc.yaml: error converting YAML to JSON: yaml: line 28: found unexpected end
of stream
```

Phase: $.primary.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.primary.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0061/paths/3e795faedefc2f10ac72/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0061>)

### [bitnami/mariadb-galera](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb-galera>)

Overview cell: 63

Status: failed | Attempts: 633

Audit findings: 303. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- 297 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E019 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb-galera 16.0.2 / templates/NOTES.txt

```text
execution error at (mariadb-galera/templates/NOTES.txt:90:3): VALUES VALIDATION: mariadb-galera: galera.mariabackup.password A MariaBackup
Password is required ("galera.mariabackup.forcePassword=true" is set) Please set a password (--set galera.mariabackup.password="xxxx")
```

Phase: $.galera.mariabackup.forcePassword | Status: failed

Changed overrides (used together):
- `$.galera.mariabackup.forcePassword = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/374c3045cc99de520f56/report.json>)

#### E020 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb-galera 16.0.2 / templates/NOTES.txt

```text
execution error at (mariadb-galera/templates/NOTES.txt:90:3): VALUES VALIDATION: mariadb-galera: rootUser.password A MariaDB Database Root
Password is required ("rootUser.forcePassword=true" is set) Please set a password (--set rootUser.password="xxxx")
```

Phase: $.rootUser | Status: failed

Changed overrides (used together):
- `$.rootUser.forcePassword = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/9bfb61fcd2895ab39c7d/report.json>)

#### E255 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 27: did not find
expected '-' indicator
```

Phase: $.networkPolicy.customRules | Status: failed

Changed overrides (used together):
- `$.networkPolicy.customRules[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/1d6a5faf6612f0fc5d5a/report.json>)

#### E256 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/pdb.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of
stream
```

Phase: $.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/d6baed3b8998a068f471/report.json>)

#### E257 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 236: found
unexpected end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/bc81b51736a9cdc4eda3/report.json>)

#### E258 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 247: found
unexpected end of stream
```

Phase: $.updateStrategy | Status: failed

Changed overrides (used together):
- `$.updateStrategy.type = "'" (was "RollingUpdate")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/dd21b70e90c3f6adcf0d/report.json>)

#### E259 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 33: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E260 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 57: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "12.0.2-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/8e79b7dd85a286cfaddb/report.json>)

#### E261 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/svc.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/6e931799d09f8182f34b/report.json>)

#### E605

```text
[Diagnostic shortened; full text in artifacts] ... ': 'object', 'additionalProperties': {'$dynamicRef': '#meta'}}}, '$defs':
{'anchorString': {'type': 'string', 'pattern': '^[A-Za-z_][-A-Za-z0-9._]*$'}, 'uriString': {'type': 'string', 'format': 'uri'},
'uriReferenceString': {'type': 'string', 'format': 'uri-reference'}}} On schema['allOf'][120]['properties']['extraVolumeMounts']['items']:
[{'properties': {'recursiveReadOnly': {'const': None}}, 'required': ['recursiveReadOnly'], 'type': 'object'}]
```

Phase: $.extraVolumeMounts[*].recursiveReadOnly | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.extraVolumeMounts["*"].recursiveReadOnly. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0062/paths/c60c675742c8e72d7494/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0062>)

### [bitnami/mastodon](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mastodon>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0063>)

### [bitnami/matomo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/matomo>)

Overview cell: 65

Status: failed | Attempts: 593

Audit findings: 357. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificates.command`: Undocumented values path (warning)
- 351 additional audit findings in JSON.

Configuration rejections: 0 excluded; 8 adjusted and tested; 9 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E021 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
execution error at (mariadb/templates/NOTES.txt:74:4): VALUES VALIDATION: mariadb: architecture Invalid architecture selected. Valid values
are "standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.mariadb.architecture | Status: failed

Changed overrides (used together):
- `$.mariadb.architecture = "" (was "standalone")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E022 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.registry = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/3a6df6c30eb21f3e500a/report.json>)

#### E023 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/e9b2bd06f74a17778834/report.json>)

#### E267 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on matomo/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 39:
did not find expected ',' or ']'
```

Phase: $.mariadb.volumePermissions.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/1a4166aed8b35c7751ed/report.json>)

Phase: $.mariadb.metrics.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.metrics.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/f3c891b2fda1d97f28f1/report.json>)

#### E268 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on matomo/templates/cronjob.yaml: error converting YAML to JSON: yaml: line 29: did not find expected ','
or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/a4a0ea6ab697189bb963/report.json>)

#### E269 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on matomo/templates/cronjob.yaml: error converting YAML to JSON: yaml: line 44: could not find expected ':'
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.ta = null`
- `$.image.int32[""]["aTaa-\\aaaaaaaa"] = [1.7976931348623157e+308, "O"]`
- `$.image.int32[""].aa = [true]`
- `$.image.int32[""].aaaaa = ["", false]`
- `$.image.int32.aaaaaa = []`
- 8 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/8e79b7dd85a286cfaddb/report.json>)

#### E270 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on matomo/templates/deployment.yaml: error converting YAML to JSON: yaml: line 156: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/bc81b51736a9cdc4eda3/report.json>)

#### E568 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: matomo/templates/deployment.yaml:328:34 executing "matomo/templates/deployment.yaml" at <$customCA.secret>: nil pointer
evaluating interface {}.secret
```

Phase: $.certificates.customCAs[*] | Status: failed

Changed overrides (used together):
- `$.certificates.customCAs = [null]`
Absent from overrides: $.certificates.customCAs["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0064/paths/f0b38f929a3c18847f6b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0064>)

### [bitnami/memcached](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/memcached>)

Overview cell: 66

Status: failed | Attempts: 659

Audit findings: 276. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingPasswordSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 270 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E271 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on memcached/templates/deployment.yaml: error converting YAML to JSON: yaml: line 117: found unexpected end
of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0065/paths/57504c968732d9714f10/report.json>)

#### E272 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on memcached/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0065/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0065/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E273 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on memcached/templates/deployment.yaml: error converting YAML to JSON: yaml: line 56: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.6.39-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0065/paths/8e79b7dd85a286cfaddb/report.json>)

#### E274 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on memcached/templates/service.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0065/paths/6e931799d09f8182f34b/report.json>)

#### E275 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on memcached/templates/service.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end of
stream
```

Phase: $.service.trafficDistribution | Status: failed

Changed overrides (used together):
- `$.service.trafficDistribution = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0065/paths/76c21b9e4a991e167280/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0065>)

### [bitnami/metallb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metallb>)

Overview cell: 67

Status: failed | Attempts: 850

Audit findings: 395. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.configInline`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- 389 additional audit findings in JSON.

Configuration rejections: 1 excluded; 18 adjusted and tested; 19 Helm verification renders (separate from manifest-test attempts).

#### E276 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metallb/templates/controller/deployment.yaml: error converting YAML to JSON: yaml: line 126: found
unexpected end of stream
```

Phase: $.controller.image.pullPolicy | Status: failed

Changed overrides (used together):
- `$.controller.image.pullPolicy = "'" (was "IfNotPresent")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0066/paths/f06a5f2314df3f7c54f4/report.json>)

#### E277 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metallb/templates/controller/deployment.yaml: error converting YAML to JSON: yaml: line 34: block
sequence entries are not allowed in this context
```

Phase: $.speaker.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.speaker.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0066/paths/5ab2d3186d90225b4cbe/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0066/paths/097f6358a00dddbcdd83/report.json>)

#### E278 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metallb/templates/controller/deployment.yaml: error converting YAML to JSON: yaml: line 62: could not
find expected ':'
```

Phase: $.controller.image.registry | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.controller.image.registry = "\r" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0066/paths/f6e22abffac7f4e2b52a/report.json>)

#### E279 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metallb/templates/controller/deployment.yaml: error converting YAML to JSON: yaml: line 81: could not
find expected ':'
```

Phase: $.controller.tlsCipherSuites | Status: failed

Changed overrides (used together):
- `$.controller.tlsCipherSuites = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0066/paths/72836b950c2bd4e8a37d/report.json>)

#### E280 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metallb/templates/speaker/daemonset.yaml: error converting YAML to JSON: yaml: line 62: could not find
expected ':'
```

Phase: $.speaker.image.registry | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.speaker.image.registry = "\r" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0066/paths/8d62fcf885ca304a17c9/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0066>)

### [bitnami/metrics-server](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metrics-server>)

Overview cell: 68

Status: failed | Attempts: 676

Audit findings: 159. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.caBundle`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.create`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService.insecureSkipTLSVerify`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiService`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- 153 additional audit findings in JSON.

Configuration rejections: 0 excluded; 37 adjusted and tested; 37 Helm verification renders (separate from manifest-test attempts).

#### E001 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: metrics-server/templates/svc.yaml:9:20 executing "metrics-server/templates/svc.yaml" at <{{template "common.names.fullname"
.}}>: template "common.names.fullname" not defined
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0067/paths/e2cac8a5225634937910/report.json>)

#### E281 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metrics-server/templates/deployment.yaml: error converting YAML to JSON: yaml: line 30: block sequence
entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0067/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0067/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E282 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metrics-server/templates/deployment.yaml: error converting YAML to JSON: yaml: line 54: found character
that cannot start any token
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.digest = "0" (was "")`
- `$.image.registry = "" (was "docker.io")`
- `$.image.repository = "" (was "bitnami/metrics-server")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0067/paths/8e79b7dd85a286cfaddb/report.json>)

#### E283 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metrics-server/templates/deployment.yaml: error converting YAML to JSON: yaml: line 56: could not find
expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/metrics-server")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0067/paths/3f7165f1837241716c3c/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0067/paths/fa90b40f46c6c70d8821/report.json>)

#### E284 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on metrics-server/templates/svc.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0067/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0067>)

### [bitnami/milvus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/milvus>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0068>)

### [bitnami/mlflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mlflow>)

Overview cell: 70

Status: time-limit | Attempts: 1

Audit findings: 332. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.database`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.database`: No supplied default for a values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode.args[*]`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode.command[*]`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.diagnosticMode`: Missing values description (info)
- 326 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0069>)

### [bitnami/mongodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb>)

Overview cell: 71

Status: failed | Attempts: 1917

Audit findings: 794. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.arbiter.automountServiceAccountToken`: Undocumented values path (warning)
- 788 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E025 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mongodb 17.0.2 / templates/NOTES.txt

```text
execution error at (mongodb/templates/NOTES.txt:173:4): VALUES VALIDATION: mongodb: auth.usernames, auth.databases Both auth.usernames and
auth.databases arrays should have the same length
```

Phase: $.auth.databases[*] | Status: failed

Changed overrides (used together):
- `$.auth.databases = [null]`
Absent from overrides: $.auth.databases["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/5248d0d9e3b4c9294b08/report.json>)

#### E026 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mongodb 17.0.2 / templates/NOTES.txt

```text
execution error at (mongodb/templates/NOTES.txt:173:4): VALUES VALIDATION: mongodb: auth.usernames, auth.databases Both auth.usernames and
auth.databases must be provided to create custom users and databases during 1st initialization. Please set both of them (--set
auth.usernames[0]="xxxx",auth.databases[0]="yyyy") mongodb: auth.usernames, auth.databases Both auth.usernames and auth.databases arrays
should have the same length
```

Phase: $.auth | Status: failed

Changed overrides (used together):
- `$.auth.dtabase = null`
- `$.auth["("] = []`
- `$.auth.databases = [[{"a,aa": ["H"]}, [-0.5]], [false, "classname", 3.2836876998328024e+16], [], {"BaaaBaaa": {"aabayaaVaawanaa": {}}, "O":... [value shortened]`
- `$.auth[""] = []`
- `$.auth["iau^6aQ"].a7aaEa = null`
- `$.auth["iau^6aQ"].INF = true`
- 6 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/9add85c17048305af4de/observed-failure.json>)

#### E027 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mongodb 17.0.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/kubectl:1.33.4-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.externalAccess | Status: failed

Changed overrides (used together):
- `$.externalAccess.autoDiscovery.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/dee969bb5b679bbcd05e/report.json>)

#### E028 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mongodb 17.0.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:1.29.1-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.tls.image.repository | Status: failed

Changed overrides (used together):
- `$.tls.image.repository = "00" (was "bitnami/nginx")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/a864d9521a69cfd3d7e2/report.json>)

#### E029 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mongodb 17.0.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r51 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.externalAccess.dnsCheck.image.repository | Status: failed

Changed overrides (used together):
- `$.externalAccess.dnsCheck.image.repository = "00" (was "bitnami/os-shell")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/d651d492cb2b73abb488/report.json>)

#### E030 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mongodb 17.0.2 / templates/update-password/new-secret.yaml

```text
execution error at (mongodb/templates/update-password/new-secret.yaml:25:28): The new root password is required!
```

Phase: $.passwordUpdateJob.enabled | Status: failed

Changed overrides (used together):
- `$.passwordUpdateJob.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/d2a199b91d47bb696ab7/report.json>)

#### E293 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 26: did not find
expected '-' indicator
```

Phase: $.networkPolicy.customRules | Status: failed

Changed overrides (used together):
- `$.networkPolicy.customRules[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/1d6a5faf6612f0fc5d5a/report.json>)

#### E294 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb/templates/standalone/dep-sts.yaml: error converting YAML to JSON: yaml: line 200: found
unexpected end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/bc81b51736a9cdc4eda3/report.json>)

Phase: $.topologyKey | Status: failed

Changed overrides (used together):
- `$.topologyKey = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/bc40cb09cdb4ddbb0fec/report.json>)

#### E295 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb/templates/standalone/dep-sts.yaml: error converting YAML to JSON: yaml: line 33: block sequence
entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E296 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb/templates/standalone/dep-sts.yaml: error converting YAML to JSON: yaml: line 60: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "8.0.13-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/8e79b7dd85a286cfaddb/report.json>)

#### E297 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb/templates/standalone/svc.yaml: error converting YAML to JSON: yaml: line 25: found unexpected
end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0070/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0070>)

### [bitnami/mongodb-sharded](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb-sharded>)

Overview cell: 72

Status: failed | Attempts: 1448

Audit findings: 647. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.replicaSetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.rootPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.rootUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFiles`: Undocumented values path (warning)
- 641 additional audit findings in JSON.

Configuration rejections: 8 excluded; 5 adjusted and tested; 13 Helm verification renders (separate from manifest-test attempts).

#### E285 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb-sharded/templates/config-server/config-server-configmap.yaml: error converting YAML to JSON:
yaml: line 17: could not find expected ':'
```

Phase: $.configsvr.config | Status: failed

Changed overrides (used together):
- `$.configsvr.config = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/b793c5f071ede0536973/report.json>)

#### E286 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb-sharded/templates/config-server/config-server-statefulset.yaml: error converting YAML to JSON:
yaml: line 173: did not find expected key
```

Phase: $.configsvr.podManagementPolicy | Status: failed

Changed overrides (used together):
- `$.configsvr.podManagementPolicy = "'" (was "OrderedReady")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/31b5e6e1c0df26c243fd/report.json>)

#### E287 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb-sharded/templates/config-server/config-server-statefulset.yaml: error converting YAML to JSON:
yaml: line 235: found unexpected end of stream
```

Phase: $.configsvr.persistence.storageClass | Status: failed

Changed overrides (used together):
- `$.configsvr.persistence.storageClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/3ed894f5869907195add/report.json>)

#### E288 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb-sharded/templates/config-server/config-server-statefulset.yaml: error converting YAML to JSON:
yaml: line 56: did not find expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E289 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb-sharded/templates/mongos/mongos-service.yaml: error converting YAML to JSON: yaml: line 24:
found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/6e931799d09f8182f34b/report.json>)

#### E290 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb-sharded/templates/shard/shard-data-statefulset.yaml: error converting YAML to JSON: yaml: line
179: did not find expected key
```

Phase: $.shardsvr.dataNode.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.shardsvr.dataNode.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/081fe11c022e35388c5a/report.json>)

#### E291 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb-sharded/templates/shard/shard-data-statefulset.yaml: error converting YAML to JSON: yaml: line
181: did not find expected key
```

Phase: $.shardsvr.dataNode.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.shardsvr.dataNode.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/b0d45fc48260a68b6fd8/report.json>)

#### E292 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mongodb-sharded/templates/shard/shard-data-statefulset.yaml: error converting YAML to JSON: yaml: line
233: found unexpected end of stream
```

Phase: $.shardsvr.persistence.subPath | Status: failed

Changed overrides (used together):
- `$.shardsvr.persistence.subPath = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/ce04d24153e2429a27fe/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.service.name | Status: failed

Changed overrides (used together):
- `$.service.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[10].data["mongodb-replica-set-key"]: "SVJEQzNFN1Jvaw==" -> "dEtUTWRSRXdxTw=="`
- `$[10].data["mongodb-root-password"]: "SjAxaVM3UjZTZQ==" -> "WDhXaVNSbEdxTA=="`
- `$[13].metadata.name: "hypothesis-mongodb-sharded" -> 0`
- `$[16].spec.template.spec.containers[0].env[9].value: "hypothesis-mongodb-sharded" -> 0`
- `$[17].spec.template.spec.containers[0].env[9].value: "hypothesis-mongodb-sharded" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/16e8b0ef40bb4622d909/report.json>)

#### E544 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on mongodb-sharded/templates/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.common.serviceAccount | Status: failed

Changed overrides (used together):
- `$.common.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0071/paths/f3032ffd214939407616/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0071>)

### [bitnami/moodle](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/moodle>)

Overview cell: 73

Status: failed | Attempts: 712

Audit findings: 300. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 294 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E021 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
execution error at (mariadb/templates/NOTES.txt:74:4): VALUES VALIDATION: mariadb: architecture Invalid architecture selected. Valid values
are "standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.mariadb.architecture | Status: failed

Changed overrides (used together):
- `$.mariadb.architecture = "" (was "standalone")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E022 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.registry = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/3a6df6c30eb21f3e500a/report.json>)

#### E023 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/e9b2bd06f74a17778834/report.json>)

#### E024 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/secrets.yaml

```text
execution error at (mariadb/templates/secrets.yaml:31:28): A MariaDB Root Password is required!
```

Phase: $.mariadb.auth.forcePassword | Status: failed

Changed overrides (used together):
- `$.mariadb.auth.forcePassword = true`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/ad4227a5f322f2d32cce/report.json>)

#### E298 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on moodle/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 39:
did not find expected ',' or ']'
```

Phase: $.mariadb.volumePermissions.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/1a4166aed8b35c7751ed/report.json>)

Phase: $.mariadb.metrics.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.metrics.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/f3c891b2fda1d97f28f1/report.json>)

#### E299 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on moodle/templates/deployment.yaml: error converting YAML to JSON: yaml: line 108: could not find expected
':'
```

Phase: $.lifecycleHooks | Status: failed

Changed overrides (used together):
- `$.lifecycleHooks = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/f43b61ad2b3dc983dbd6/report.json>)

#### E300 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on moodle/templates/deployment.yaml: error converting YAML to JSON: yaml: line 156: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/bc81b51736a9cdc4eda3/report.json>)

#### E301 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on moodle/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: block sequence entries
are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/a4a0ea6ab697189bb963/report.json>)

#### E302 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on moodle/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "5.0.2-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0072/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0072>)

### [bitnami/multus-cni](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/multus-cni>)

Overview cell: 74

Status: failed | Attempts: 409

Audit findings: 135. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.CNIMountPath`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.CNIVersion`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 129 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E303 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on multus-cni/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 173: found unexpected end
of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0073/paths/57504c968732d9714f10/report.json>)

#### E304 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on multus-cni/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 28: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0073/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0073/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E305 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on multus-cni/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 54: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "4.2.2-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0073/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0073>)

### [bitnami/mysql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mysql>)

Overview cell: 75

Status: failed | Attempts: 1381

Audit findings: 512. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.authenticationPolicy`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.auth.createDatabase`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.replicator`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.customPasswordFiles.replicator`: No supplied default for a values
  path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.customPasswordFiles.root`: Undocumented values path (warning)
- 506 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E035 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mysql 14.0.5 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:9.4.0-debian-12-r1 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/mysql")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/3f7165f1837241716c3c/report.json>)

#### E036 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mysql 14.0.5 / templates/update-password/new-secret.yaml

```text
execution error at (mysql/templates/update-password/new-secret.yaml:22:26): The new root password is required!
```

Phase: $.passwordUpdateJob.enabled | Status: failed

Changed overrides (used together):
- `$.passwordUpdateJob.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/d2a199b91d47bb696ab7/report.json>)

#### E306 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mysql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 128: did not find
expected key
```

Phase: $.primary.extraFlags | Status: failed

Changed overrides (used together):
- `$.primary.extraFlags = "\"" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/d0a68fa7dda521709a69/report.json>)

#### E307 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mysql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 226: found
unexpected end of stream
```

Phase: $.primary.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.primary.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/9500a72d3c4e020c37bd/report.json>)

#### E308 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mysql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 238: found
unexpected end of stream
```

Phase: $.primary.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.primary.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/af9a77b4b696ef0a07df/report.json>)

#### E309 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mysql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 40: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/097f6358a00dddbcdd83/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E310 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mysql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 63: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.4.0-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/8e79b7dd85a286cfaddb/report.json>)

#### E311 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mysql/templates/primary/svc.yaml: error converting YAML to JSON: yaml: line 28: found unexpected end of
stream
```

Phase: $.primary.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.primary.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/3e795faedefc2f10ac72/report.json>)

#### E569 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: mysql/templates/networkpolicy.yaml:72:69 executing "mysql/templates/networkpolicy.yaml" at <$value.port>: nil pointer
evaluating interface {}.port
```

Phase: $.primary.service.extraPorts | Status: failed

Changed overrides (used together):
- `$.primary.service.extraPorts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/933f7e6a3ed28af0fce9/report.json>)

#### E570 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: mysql/templates/networkpolicy.yaml:77:69 executing "mysql/templates/networkpolicy.yaml" at <$value.containerPort>: nil
pointer evaluating interface {}.containerPort
```

Phase: $.secondary.extraPorts[*] | Status: failed

Changed overrides (used together):
- `$.secondary.extraPorts = [null]`
Absent from overrides: $.secondary.extraPorts["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/e81138b0da9ace2ca837/report.json>)

Phase: $.secondary.extraPorts | Status: failed

Changed overrides (used together):
- `$.secondary.extraPorts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/45d9011d20dedf406df6/report.json>)

#### E589 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: mysql/templates/primary/svc.yaml:9:11 executing "mysql/templates/primary/svc.yaml" at <include "mysql.primary.fullname" .>:
error calling include: mysql/templates/_helpers.tpl:12:4 executing "mysql.primary.fullname" at <include "common.names.fullname" .>: error
calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/e2cac8a5225634937910/report.json>)

#### E604

```text
[Diagnostic shortened; full text in artifacts] ... }, '$comment': {'type': 'string'}, '$defs': {'type': 'object', 'additionalProperties':
{'$dynamicRef': '#meta'}}}, '$defs': {'anchorString': {'type': 'string', 'pattern': '^[A-Za-z_][-A-Za-z0-9._]*$'}, 'uriString': {'type':
'string', 'format': 'uri'}, 'uriReferenceString': {'type': 'string', 'format': 'uri-reference'}}} On
schema['allOf'][202]['properties']['primary']['properties']['service']['properties']['externalIPs']['items']: [{'const': []}]
```

Phase: $.primary.service.externalIPs[*] | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.primary.service.externalIPs["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0074/paths/8c7e1becbd34de0c6823/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0074>)

### [bitnami/nats](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nats>)

Overview cell: 76

Status: failed | Attempts: 989

Audit findings: 307. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials[*].password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.credentials[*].user`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- 301 additional audit findings in JSON.

Configuration rejections: 0 excluded; 25 adjusted and tested; 25 Helm verification renders (separate from manifest-test attempts).

#### E037 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nats 9.0.29 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ...  performance, broken chart features, and missing environment variables. Unrecognized
images: - 00/bitnami/nats:2.11.8-debian-12-r0 - 00/bitnami/nats-exporter:0.17.3-debian-12-r8 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`
- `$.tls.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/fa90b40f46c6c70d8821/report.json>)

#### E038 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nats 9.0.29 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:2.11.8-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/nats")`
- `$.tls.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/3f7165f1837241716c3c/report.json>)

#### E039 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nats 9.0.29 / templates/NOTES.txt

```text
execution error at (nats/templates/NOTES.txt:176:4): VALUES VALIDATION: nats: jetstream Invalid configuration selected. Enabling JetStream
requires enabling persistence and using a StatefulSet (--set persistence.enabled=true,resourceType="statefulset")
```

Phase: $.jetstream | Status: failed

Changed overrides (used together):
- `$.tls.enabled = true (was false)`
- `$.jetstream.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/6cf86d162ba8d24d656c/report.json>)

Phase: $.jetstream.enabled | Status: failed

Changed overrides (used together):
- `$.tls.enabled = true (was false)`
- `$.jetstream.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/f3959e35f738651ecbdc/report.json>)

#### E312 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nats/templates/application.yaml: error converting YAML to JSON: yaml: line 128: found unexpected end of
stream
```

Phase: $.existingSecret | Status: failed

Changed overrides (used together):
- `$.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/bf7372b3862550c529f3/report.json>)

#### E313 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nats/templates/application.yaml: error converting YAML to JSON: yaml: line 33: did not find expected ','
or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/097f6358a00dddbcdd83/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E314 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nats/templates/application.yaml: error converting YAML to JSON: yaml: line 57: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.11.8-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/8e79b7dd85a286cfaddb/report.json>)

#### E315 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nats/templates/service.yaml: error converting YAML to JSON: yaml: line 28: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/6e931799d09f8182f34b/report.json>)

#### E590 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: nats/templates/serviceaccount.yaml:10:11 executing "nats/templates/serviceaccount.yaml" at <include
"nats.serviceAccountName" .>: error calling include: nats/templates/_helpers.tpl:42:16 executing "nats.serviceAccountName" at <include
"common.names.fullname" .>: error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0075/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0075>)

### [bitnami/neo4j](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/neo4j>)

Overview cell: 77

Status: failed | Attempts: 2716

Audit findings: 251. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.advertisedHost`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apocConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- 245 additional audit findings in JSON.

Configuration rejections: 1 excluded; 50 adjusted and tested; 52 Helm verification renders (separate from manifest-test attempts).

#### E077 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: common 2.31.4 / templates/_capabilities.tpl

```text
template: common/templates/_capabilities.tpl:24:12: executing "common.capabilities.apiVersions.has" at <has .version $providedAPIVersions>:
error calling has: Cannot find has on type bool
```

Phase: $.global | Status: failed

Changed overrides (used together):
- `$.global.apiVersions = true`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/a8d13bfa12806deaf76c/report.json>)

#### E078 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: common 2.31.4 / templates/_capabilities.tpl

```text
template: common/templates/_capabilities.tpl:24:12: executing "common.capabilities.apiVersions.has" at <has .version $providedAPIVersions>:
error calling has: Cannot find has on type map
```

Phase: $.global.apiVersions | Status: failed

Changed overrides (used together):
- `$.global.apiVersions[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/bf831d44fafae718f0f6/report.json>)

#### E316 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on neo4j/templates/configmap.yaml: error converting YAML to JSON: yaml: line 17: could not find expected
':'
```

Phase: $.configuration | Status: failed

Changed overrides (used together):
- `$.configuration = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/8ca25117bb2b80f3ff5d/report.json>)

Phase: $.apocConfiguration | Status: failed

Changed overrides (used together):
- `$.apocConfiguration = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/9381cc0b3caa89e5413e/report.json>)

#### E317 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on neo4j/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 6: could not find expected
':'
```

Phase: $.nameOverride | Status: failed

Changed overrides (used together):
- `$.nameOverride = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/0ce120cfa523ba37df61/report.json>)

#### E318 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on neo4j/templates/service.yaml: error converting YAML to JSON: yaml: line 16: did not find expected ',' or
']'
```

Phase: $.service.loadBalancerSourceRanges[*] | Status: failed

Changed overrides (used together):
- `$.service.loadBalancerSourceRanges = [{}]`
Absent from overrides: $.service.loadBalancerSourceRanges["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/964773c98a041f080dd4/report.json>)

Phase: $.service.loadBalancerSourceRanges | Status: failed

Changed overrides (used together):
- `$.service.loadBalancerSourceRanges = [{}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/60903c8f6383b493cf31/report.json>)

#### E319 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on neo4j/templates/service.yaml: error converting YAML to JSON: yaml: line 27: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/6e931799d09f8182f34b/report.json>)

#### E320 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on neo4j/templates/service.yaml: error converting YAML to JSON: yaml: line 28: found unexpected end of
stream
```

Phase: $.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/12b3c4a215648c1d6dd7/report.json>)

#### E321 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on neo4j/templates/service.yaml: error converting YAML to JSON: yaml: line 29: found unexpected end of
stream
```

Phase: $.service.nodePorts.http | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/c91d7fbded4704da55d3/report.json>)

Phase: $.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.bolt = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/afbac7d295ec4c0a2908/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E523 ([HH1102](#hh1102---manifest-document-is-not-an-object))

**Manifest document is not an object** (manifest / violation). Severity: **error**. Emit a resource mapping or remove the stray document.

```text
[HH1102] Error: YAML parse error on neo4j/templates/extra-list.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go value of type util.SimpleHead
```

Phase: $.extraDeploy | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/90454abd7e30d38b69ee/report.json>)

Phase: $.extraDeploy[*] | Status: failed

Changed overrides (used together):
- `$.extraDeploy = [[]]`
Absent from overrides: $.extraDeploy["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/fbfea8b96e1bf6abb6fc/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[1].metadata.name: "hypothesis-neo4j" -> 0`
- `$[2].data.password: "VDQ4UjljWGlLYXFkQlQ0NA==" -> "VkttTjFROFNTVTFXaFUzQQ=="`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/815bf9b751b356e044f0/report.json>)

Phase: $.fullnameOverride | Status: failed

Changed overrides (used together):
- `$.fullnameOverride = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[0].metadata.name: "hypothesis-neo4j" -> 0`
- `$[1].metadata.name: "hypothesis-neo4j" -> 0`
- `$[2].data.password: "VDQ4UjljWGlLYXFkQlQ0NA==" -> "NXRmZWkyVGpqRkx5QkdSeg=="`
- `$[2].metadata.name: "hypothesis-neo4j" -> 0`
- `$[3].metadata.name: "hypothesis-neo4j" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/e2f7761f901d86846684/report.json>)

#### E571 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: neo4j/templates/networkpolicy.yaml:47:19 executing "neo4j/templates/networkpolicy.yaml" at <.containerPort>: nil pointer
evaluating interface {}.containerPort
```

Phase: $.extraContainerPorts | Status: failed

Changed overrides (used together):
- `$.extraContainerPorts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/f7f8700baed516b2f5dc/report.json>)

Phase: $.extraContainerPorts[*] | Status: failed

Changed overrides (used together):
- `$.extraContainerPorts = [null]`
Absent from overrides: $.extraContainerPorts["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/a734f2883f305d7ad187/report.json>)

#### E591 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: neo4j/templates/rbac/service-account.yaml:10:11 executing "neo4j/templates/rbac/service-account.yaml" at <include
"neo4j.serviceAccountName" .>: error calling include: neo4j/templates/_helpers.tpl:32:16 executing "neo4j.serviceAccountName" at <include
"common.names.fullname" .>: error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/e2cac8a5225634937910/report.json>)

Phase: $.tags["bitnami-common"] | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0076/paths/2ff2aa2642f40d7be0f3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0076>)

### [bitnami/nessie](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nessie>)

Overview cell: 78

Status: failed | Attempts: 429

Audit findings: 332. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- 326 additional audit findings in JSON.

Configuration rejections: 0 excluded; 8 adjusted and tested; 8 Helm verification renders (separate from manifest-test attempts).

#### E322 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nessie/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line
189: found unexpected end of stream
```

Phase: $.postgresql.primary.persistence.mountPath | Status: failed

Changed overrides (used together):
- `$.postgresql.primary.persistence.mountPath = "'"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0077/paths/0284bb67db05bfe310ba/report.json>)

#### E323 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nessie/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON: yaml:
line 17: could not find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0077/paths/91bb86cdd8574ec43d3d/report.json>)

#### E324 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nessie/templates/deployment.yaml: error converting YAML to JSON: yaml: line 139: could not find expected
':'
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.ta = null`
- `$.image.int32[""]["aTaa-\\aaaaaaaa"] = [1.7976931348623157e+308, "O"]`
- `$.image.int32[""].aa = [true]`
- `$.image.int32[""].aaaaa = ["", false]`
- `$.image.int32.aaaaaa = []`
- 8 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0077/paths/8e79b7dd85a286cfaddb/report.json>)

#### E325 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nessie/templates/deployment.yaml: error converting YAML to JSON: yaml: line 39: block sequence entries
are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0077/paths/a4a0ea6ab697189bb963/report.json>)

#### E577 ([HH3002](#hh3002---incompatible-value-type-in-template))

**Incompatible value type in template** (template / violation). Severity: **error**. Align the template operation with the accepted input
types, or narrow the schema.

```text
[HH3002] Error: nessie/charts/postgresql/templates/primary/statefulset.yaml:259:20 executing
"nessie/charts/postgresql/templates/primary/statefulset.yaml" at <include "postgresql.v1.database" .>: error calling include:
nessie/charts/postgresql/templates/_helpers.tpl:93:32 executing "postgresql.v1.database" at <.Values.global.postgresql.auth.database>: wrong
type for value; expected string; got float64
```

Phase: $.global.postgresql.auth | Status: failed

Changed overrides (used together):
- `$.global.postgresql.auth.database = 1`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0077/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0077>)

### [bitnami/nginx](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nginx>)

Overview cell: 79

Status: failed | Attempts: 1859

Audit findings: 321. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 315 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E040 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nginx 22.1.1 / templates/NOTES.txt

```text
execution error at (nginx/templates/NOTES.txt:75:4): VALUES VALIDATION: nginx: missing-extra-volume-mounts You specified extra volumes but
not mount points for them. Please set the extraVolumeMounts value or use them in sidecars
```

Phase: $.extraVolumes | Status: failed

Changed overrides (used together):
- `$.extraVolumes = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/0b94c6f90deb62ef8b9d/report.json>)

#### E041 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nginx 22.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... tainers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/git:2.51.0-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.cloneStaticSiteFromGit.image | Status: failed

Changed overrides (used together):
- `$.cloneStaticSiteFromGit.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/5da41d783cf829a943d5/report.json>)

#### E042 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nginx 22.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... nd missing environment variables. Unrecognized images: -
00/bitnami/nginx:1.29.1-debian-12-r0 - 00/bitnami/git:2.51.0-debian-12-r0 - 00/bitnami/nginx-exporter:1.4.2-debian-12-r9 If you are sure you
want to proceed with non-standard containers, you can skip container image verification by setting the global parameter
'global.security.allowInsecureImages' to true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/fa90b40f46c6c70d8821/report.json>)

#### E043 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nginx 22.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:1.29.1-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/nginx")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/3f7165f1837241716c3c/report.json>)

#### E044 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nginx 22.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:1.4.2-debian-12-r9 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.metrics.image.repository | Status: failed

Changed overrides (used together):
- `$.metrics.image.repository = "00" (was "bitnami/nginx-exporter")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/4c4a07eb1c5214b3a409/report.json>)

#### E045 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nginx 22.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:2.51.0-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.cloneStaticSiteFromGit.image.repository | Status: failed

Changed overrides (used together):
- `$.cloneStaticSiteFromGit.image.repository = "00" (was "bitnami/git")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/12e30b837b1cc5491b66/report.json>)

#### E046 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: nginx 22.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... h non-standard containers is likely to cause degraded security and performance, broken
chart features, and missing environment variables. Unrecognized images: - docker.io/}:L)gE If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.metrics | Status: failed

Changed overrides (used together):
- `$.metrics.securityContext.tQaWqa = null`
- `$.metrics["\\"] = null`
- `$.metrics["9r!"] = null`
- ``$.metrics.customLivenessProbe["N`aZ"] = {}``
- `$.metrics.customLivenessProbe["Ca#s"] = []`
- `$.metrics.customLivenessProbe["<"] = null`
- 36 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/17d970eb96f24f23c2d5/observed-failure.json>)

#### E326 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/context-includes-configmap.yaml: error converting YAML to JSON: yaml: line 16: could not
find expected ':'
```

Phase: $.contextIncludes.main | Status: failed

Changed overrides (used together):
- `$.contextIncludes.main = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/1ea114c98761af6fd8de/report.json>)

Phase: $.contextIncludes.events | Status: failed

Changed overrides (used together):
- `$.contextIncludes.events = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/5e6c83e5fa96fb54dad4/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E327 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/deployment.yaml: error converting YAML to JSON: yaml: line 179: found unexpected end of
stream
```

Phase: $.readinessProbe.path | Status: failed

Changed overrides (used together):
- `$.readinessProbe.path = "'" (was "/")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/6e63684264db9d622def/report.json>)

#### E328 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/deployment.yaml: error converting YAML to JSON: yaml: line 180: found unexpected end of
stream
```

Phase: $.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/6ba7d997c0ad5ab2417b/report.json>)

#### E329 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/deployment.yaml: error converting YAML to JSON: yaml: line 181: found unexpected end of
stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/e4b1fa53526f192b7184/report.json>)

#### E330 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/deployment.yaml: error converting YAML to JSON: yaml: line 184: found unexpected end of
stream
```

Phase: $.existingContextEventsConfigmaps[*] | Status: failed

Changed overrides (used together):
- `$.existingContextEventsConfigmaps = ["'"]`
Absent from overrides: $.existingContextEventsConfigmaps["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/d3a4ba9b3aa8276f735b/report.json>)

Phase: $.existingContextHttpConfigmaps | Status: failed

Changed overrides (used together):
- `$.existingContextHttpConfigmaps = ["\""]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/70fff6af8ba5e53e56ff/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E331 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/deployment.yaml: error converting YAML to JSON: yaml: line 185: found unexpected end of
stream
```

Phase: $.staticSitePVC | Status: failed

Changed overrides (used together):
- `$.staticSitePVC = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/fedafd50625ec0edfe65/report.json>)

#### E332 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/deployment.yaml: error converting YAML to JSON: yaml: line 186: found unexpected end of
stream
```

Phase: $.existingStreamServerBlockConfigmap | Status: failed

Changed overrides (used together):
- `$.existingStreamServerBlockConfigmap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/d4c28e96673fe55ac939/report.json>)

#### E333 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/deployment.yaml: error converting YAML to JSON: yaml: line 33: block sequence entries
are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/097f6358a00dddbcdd83/report.json>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E334 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/deployment.yaml: error converting YAML to JSON: yaml: line 59: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.29.1-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/8e79b7dd85a286cfaddb/report.json>)

#### E335 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/svc.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/6e931799d09f8182f34b/report.json>)

#### E336 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/svc.yaml: error converting YAML to JSON: yaml: line 28: found unexpected end of stream
```

Phase: $.service.nodePorts.http | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/c91d7fbded4704da55d3/report.json>)

Phase: $.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/afbac7d295ec4c0a2908/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E337 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/tls-secret.yaml: error converting YAML to JSON: yaml: line 13: did not find expected key
```

Phase: $.tls.certFilename | Status: failed

Changed overrides (used together):
- `$.tls.certFilename = "" (was "tls.crt")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/b5ad58d24237401fa5a2/report.json>)

#### E338 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on nginx/templates/tls-secret.yaml: error converting YAML to JSON: yaml: line 14: did not find expected key
```

Phase: $.tls.certKeyFilename | Status: failed

Changed overrides (used together):
- `$.tls.certKeyFilename = "" (was "tls.key")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/9ef2ee7ffb2a0d0efec3/report.json>)

#### E592 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: nginx/templates/tls-secret.yaml:11:28 executing "nginx/templates/tls-secret.yaml" at <include "common.names.fullname" .>:
error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/e2cac8a5225634937910/report.json>)

#### E603

```text
[Diagnostic shortened; full text in artifacts] ... ': 'boolean'}}, '$comment': {'type': 'string'}, '$defs': {'type': 'object',
'additionalProperties': {'$dynamicRef': '#meta'}}}, '$defs': {'anchorString': {'type': 'string', 'pattern': '^[A-Za-z_][-A-Za-z0-9._]*$'},
'uriString': {'type': 'string', 'format': 'uri'}, 'uriReferenceString': {'type': 'string', 'format': 'uri-reference'}}} On
schema['allOf'][38]['properties']['service']['properties']['loadBalancerSourceRanges']['items']: [{'const': []}]
```

Phase: $.service.loadBalancerSourceRanges[*] | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.service.loadBalancerSourceRanges["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0078/paths/964773c98a041f080dd4/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0078>)

### [bitnami/node-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/node-exporter>)

Overview cell: 80

Status: failed | Attempts: 983

Audit findings: 180. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 174 additional audit findings in JSON.

Configuration rejections: 0 excluded; 29 adjusted and tested; 29 Helm verification renders (separate from manifest-test attempts).

#### E339 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on node-exporter/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 126: found unexpected
end of stream
```

Phase: $.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/6ba7d997c0ad5ab2417b/report.json>)

#### E340 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on node-exporter/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 32: block sequence
entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E341 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on node-exporter/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 55: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.9.1-debian-12-r14")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/8e79b7dd85a286cfaddb/report.json>)

#### E342 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on node-exporter/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 57: could not find
expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/node-exporter")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/3f7165f1837241716c3c/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/fa90b40f46c6c70d8821/report.json>)

#### E343 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on node-exporter/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 76: could not find
expected ':'
```

Phase: $.extraArgs | Status: failed

Changed overrides (used together):
- `$.extraArgs["\n0"] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/6b07fe5f61f90919fc2a/report.json>)

#### E344 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on node-exporter/templates/service.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end
of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/6e931799d09f8182f34b/report.json>)

#### E345 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on node-exporter/templates/service.yaml: error converting YAML to JSON: yaml: line 7: did not find expected
key
```

Phase: $.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/5996bd948f4d6447c879/report.json>)

Phase: $.service.annotations | Status: failed

Changed overrides (used together):
- `$.service.annotations[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/98a2bca1991be60ae38a/report.json>)

#### E532 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.coreos.com/v1/ServiceMonitor requires an explicit JSON schema in resource_schemas
```

Phase: $.serviceMonitor.enabled | Status: failed

Changed overrides (used together):
- `$.serviceMonitor.enabled = true (was false)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[4]: <absent> -> {"apiVersion": "monitoring.coreos.com/v1", "kind": "ServiceMonitor", "metadata": {"name": "hypothesis-node-exporter", "n... [value shortened]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/f2145ebd54549f220190/report.json>)

#### E593 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: node-exporter/templates/_helpers.tpl:27:16 executing "node-exporter.serviceAccountName" at <include "common.names.fullname"
.>: error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0079/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0079>)

### [bitnami/oauth2-proxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/oauth2-proxy>)

Overview cell: 81

Status: failed | Attempts: 389

Audit findings: 223. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 217 additional audit findings in JSON.

#### E346 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on oauth2-proxy/charts/redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line
188: found unexpected end of stream
```

Phase: $.redis.master.persistence.subPath | Status: failed

Changed overrides (used together):
- `$.redis.master.persistence.subPath = "'"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0080/paths/03223810de42d02290b1/report.json>)

#### E347 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on oauth2-proxy/charts/redis/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 27:
could not find expected ':'
```

Phase: $.redis.networkPolicy.extraIngress | Status: failed

Changed overrides (used together):
- `$.redis.networkPolicy.extraIngress = "0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0080/paths/60062ef473cd803bdad3/report.json>)

#### E545 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on oauth2-proxy/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON:
json: cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0080/paths/afbbf9ab6c6be5d414aa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0080>)

### [bitnami/odoo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/odoo>)

Overview cell: 82

Status: failed | Attempts: 531

Audit findings: 271. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 265 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E348 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on odoo/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line
189: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.updateStrategy.rollingUpdate = null (was null)`
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0081/paths/a0cdb2ba618083d9a8df/report.json>)

#### E349 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on odoo/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON: yaml: line
17: could not find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.updateStrategy.rollingUpdate = null (was null)`
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0081/paths/91bb86cdd8574ec43d3d/report.json>)

#### E350 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on odoo/templates/deployment.yaml: error converting YAML to JSON: yaml: line 147: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.updateStrategy.rollingUpdate = null (was null)`
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0081/paths/bc81b51736a9cdc4eda3/report.json>)

#### E351 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on odoo/templates/deployment.yaml: error converting YAML to JSON: yaml: line 30: did not find expected ','
or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{"aaaaaaaaa\n0": "a", "discover": "a", "aaaaaaE": [100480376, true, true]}], {"": null}]`
- `$.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0081/paths/a4a0ea6ab697189bb963/report.json>)

#### E352 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on odoo/templates/deployment.yaml: error converting YAML to JSON: yaml: line 54: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "18.0.20250805-debian-12-r8")`
- `$.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0081/paths/8e79b7dd85a286cfaddb/report.json>)

#### E546 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on odoo/charts/postgresql/templates/primary/networkpolicy.yaml: error unmarshaling JSON: while decoding
JSON: json: cannot unmarshal array into Go struct field .metadata.name of type string
```

Phase: $.global.postgresql.auth | Status: failed

Changed overrides (used together):
- `$.global.postgresql.fullnameOverride = [null]`
- `$.global.postgresql.auth = {}`
- `$.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0081/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0081>)

### [bitnami/opensearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/opensearch>)

Overview cell: 83

Status: failed | Attempts: 2750

Audit findings: 1111. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.config`: Undocumented values path (warning)
- 1105 additional audit findings in JSON.

Configuration rejections: 64 excluded; 30 adjusted and tested; 95 Helm verification renders (separate from manifest-test attempts).

#### E353 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/coordinating/statefulset.yaml: error converting YAML to JSON: yaml: line 237: found
unexpected end of stream
```

Phase: $.coordinating.schedulerName | Status: failed

Changed overrides (used together):
- `$.coordinating.schedulerName = "'" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/c725fa76dfbd1561269f/report.json>)

#### E354 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/coordinating/statefulset.yaml: error converting YAML to JSON: yaml: line 241: found
unexpected end of stream
```

Phase: $.initScriptsCM | Status: failed

Changed overrides (used together):
- `$.initScriptsCM = "'" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/53fc8d8ab406399fe0bb/report.json>)

#### E355 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/coordinating/statefulset.yaml: error converting YAML to JSON: yaml: line 41: block
sequence entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.sysctlImage.pullSecrets[*] | Status: failed

Changed overrides (used together):
- `$.sysctlImage.pullSecrets = [[null]]`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`
Absent from overrides: $.sysctlImage.pullSecrets["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/e326e771561b22095185/report.json>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E356 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/data/pdb.yaml: error converting YAML to JSON: yaml: line 20: found unexpected end
of stream
```

Phase: $.data.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.data.pdb.maxUnavailable = "'" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/f916e56e9a17a88ae463/report.json>)

#### E357 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/data/statefulset.yaml: error converting YAML to JSON: yaml: line 247: found
unexpected end of stream
```

Phase: $.data.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.data.terminationGracePeriodSeconds = "'" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/c5896537f2bf0d754037/report.json>)

Phase: $.data.schedulerName | Status: failed

Changed overrides (used together):
- `$.data.schedulerName = "'" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/5f8e5fba5fa5b7f79c0c/report.json>)

#### E358 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/ingest/pdb.yaml: error converting YAML to JSON: yaml: line 20: found unexpected end
of stream
```

Phase: $.ingest.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.ingest.pdb.minAvailable = "'" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/26816296ad75a6d675e0/report.json>)

#### E359 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/ingest/statefulset.yaml: error converting YAML to JSON: yaml: line 25: could not
find expected ':'
```

Phase: $.ingest.nameOverride | Status: failed

Changed overrides (used together):
- `$.ingest.nameOverride = "\r" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/9ad325076d817833ec6e/report.json>)

#### E360 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/master/pdb.yaml: error converting YAML to JSON: yaml: line 14: block sequence
entries are not allowed in this context
```

Phase: $.master.pdb | Status: failed

Changed overrides (used together):
- `$.master.pdb.maxUnavailable = "-" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/e57d4678169e24abedfb/report.json>)

#### E361 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 246: found
unexpected end of stream
```

Phase: $.master.persistence.storageClass | Status: failed

Changed overrides (used together):
- `$.master.persistence.storageClass = "'" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/8b1730de40416f0c86e2/report.json>)

#### E362 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 247: found
unexpected end of stream
```

Phase: $.master.schedulerName | Status: failed

Changed overrides (used together):
- `$.master.schedulerName = "'" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/b3f60a0cb2adae0e1a9b/report.json>)

#### E363 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on opensearch/templates/service.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/6e931799d09f8182f34b/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.coordinating.fullnameOverride | Status: failed

Changed overrides (used together):
- `$.coordinating.fullnameOverride = "0" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[0].metadata.name: "hypothesis-opensearch-coordinating" -> 0`
- `$[14].metadata.name: "hypothesis-opensearch-coordinating" -> 0`
- `$[14].spec.serviceName: "hypothesis-opensearch-coordinating-hl" -> "0-hl"`
- `$[14].spec.template.spec.containers[0].env[11].value: "$(MY_POD_NAME).hypothesis-opensearch-coordinating-hl.default.svc.cluster.local" -> "$(MY_POD_NAME).0-hl.default.svc.cluster.local"`
- `$[14].spec.template.spec.containers[0].env[7].value: "hypothesis-opensearch-master-hl.default.svc.cluster.local,hypothesis-opensearch-coordinating-hl.default.svc.cluster.loc... [value shortened] -> "hypothesis-opensearch-master-hl.default.svc.cluster.local,0-hl.default.svc.cluster.local,hypothesis-opensearch-data-hl.... [value shortened]`
- `$[15].spec.template.spec.containers[0].env[7].value: "hypothesis-opensearch-master-hl.default.svc.cluster.local,hypothesis-opensearch-coordinating-hl.default.svc.cluster.loc... [value shortened] -> "hypothesis-opensearch-master-hl.default.svc.cluster.local,0-hl.default.svc.cluster.local,hypothesis-opensearch-data-hl.... [value shortened]`
- 4 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/b8432c270c9ae0524afb/report.json>)

Phase: $.ingest.service.headless | Status: failed

Changed overrides (used together):
- `$.ingest.service.headless.nameOverride = "0" (was "")`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[11].metadata.name: "hypothesis-opensearch-ingest-hl" -> 0`
- `$[14].spec.template.spec.containers[0].env[7].value: "hypothesis-opensearch-master-hl.default.svc.cluster.local,hypothesis-opensearch-coordinating-hl.default.svc.cluster.loc... [value shortened] -> "hypothesis-opensearch-master-hl.default.svc.cluster.local,hypothesis-opensearch-coordinating-hl.default.svc.cluster.loc... [value shortened]`
- `$[15].spec.template.spec.containers[0].env[7].value: "hypothesis-opensearch-master-hl.default.svc.cluster.local,hypothesis-opensearch-coordinating-hl.default.svc.cluster.loc... [value shortened] -> "hypothesis-opensearch-master-hl.default.svc.cluster.local,hypothesis-opensearch-coordinating-hl.default.svc.cluster.loc... [value shortened]`
- `$[16].spec.serviceName: "hypothesis-opensearch-ingest-hl" -> 0`
- `$[16].spec.template.spec.containers[0].env[11].value: "$(MY_POD_NAME).hypothesis-opensearch-ingest-hl.default.svc.cluster.local" -> "$(MY_POD_NAME).0.default.svc.cluster.local"`
- `$[16].spec.template.spec.containers[0].env[7].value: "hypothesis-opensearch-master-hl.default.svc.cluster.local,hypothesis-opensearch-coordinating-hl.default.svc.cluster.loc... [value shortened] -> "hypothesis-opensearch-master-hl.default.svc.cluster.local,hypothesis-opensearch-coordinating-hl.default.svc.cluster.loc... [value shortened]`
- 1 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/d43df00aa9b94447cf44/report.json>)

#### E547 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on opensearch/templates/coordinating/svc-headless.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.coordinating.service | Status: failed

Changed overrides (used together):
- `$.coordinating.service.headless.annotations[""] = []`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/369651dcaa5482cbf3e8/report.json>)

Phase: $.coordinating.service.headless.annotations | Status: failed

Changed overrides (used together):
- `$.coordinating.service.headless.annotations[""] = []`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/eab2d30b559e541a9a50/report.json>)

#### E548 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on opensearch/templates/data/svc-headless.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.data.service.headless.annotations | Status: failed

Changed overrides (used together):
- `$.data.service.headless.annotations[""] = []`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/b9e8f9ccfa11a235f5fc/report.json>)

#### E549 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on opensearch/templates/ingest/svc-headless.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.ingest.service.headless.annotations | Status: failed

Changed overrides (used together):
- `$.ingest.service.headless.annotations[""] = []`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/11ffaad4e56d67587532/report.json>)

#### E550 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on opensearch/templates/master/statefulset.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.master.annotations | Status: failed

Changed overrides (used together):
- `$.master.annotations[""] = []`
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/0091d50a34ab71fa3525/report.json>)

#### E594 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: opensearch/templates/master/vpa.yaml:6:12 executing "opensearch/templates/master/vpa.yaml" at <include
"common.capabilities.apiVersions.has" (dict "version" "autoscaling.k8s.io/v1/VerticalPodAutoscaler" "context" .)>: error calling include:
template: no template "common.capabilities.apiVersions.has" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.snapshots.containerSecurityContext.seLinuxOptions = null (was null)`
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0082/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0082>)

### [bitnami/parse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/parse>)

Overview cell: 84

Status: failed | Attempts: 447

Audit findings: 379. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.appName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.dashboard.automountServiceAccountToken`: Undocumented values path (warning)
- 373 additional audit findings in JSON.

#### E364 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on parse/charts/mongodb/templates/standalone/dep-sts.yaml: error converting YAML to JSON: yaml: line 205:
mapping keys are not allowed in this context
```

Phase: $.mongodb.persistence | Status: failed

Changed overrides (used together):
- `$.mongodb.persistence.existingClaim = "?"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0083/paths/41d6ae6f8aea08087045/report.json>)

#### E365 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on parse/charts/mongodb/templates/standalone/dep-sts.yaml: error converting YAML to JSON: yaml: line 207:
found unexpected end of stream
```

Phase: $.mongodb.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.mongodb.terminationGracePeriodSeconds = "'"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0083/paths/17d8050752282d6ea738/report.json>)

#### E366 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on parse/templates/server-deployment.yaml: error converting YAML to JSON: yaml: line 204: found unexpected
end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0083/paths/bc81b51736a9cdc4eda3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0083>)

### [bitnami/phpmyadmin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/phpmyadmin>)

Overview cell: 85

Status: failed | Attempts: 709

Audit findings: 246. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 240 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E021 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
execution error at (mariadb/templates/NOTES.txt:74:4): VALUES VALIDATION: mariadb: architecture Invalid architecture selected. Valid values
are "standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.mariadb.architecture | Status: failed

Changed overrides (used together):
- `$.db.bundleTestDB = true (was false)`
- `$.mariadb.architecture = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0084/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E022 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.db.bundleTestDB = true (was false)`
- `$.mariadb.volumePermissions.image.registry = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0084/paths/3a6df6c30eb21f3e500a/report.json>)

#### E023 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.db.bundleTestDB = true (was false)`
- `$.mariadb.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0084/paths/e9b2bd06f74a17778834/report.json>)

#### E024 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/secrets.yaml

```text
execution error at (mariadb/templates/secrets.yaml:31:28): A MariaDB Root Password is required!
```

Phase: $.mariadb.auth.forcePassword | Status: failed

Changed overrides (used together):
- `$.db.bundleTestDB = true (was false)`
- `$.mariadb.auth.forcePassword = true`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0084/paths/ad4227a5f322f2d32cce/report.json>)

#### E367 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on phpmyadmin/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line
40: did not find expected ',' or ']'
```

Phase: $.mariadb.volumePermissions.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.db.bundleTestDB = true (was false)`
- `$.mariadb.volumePermissions.image.pullSecrets = [null, null, {"": null}, null, [null, null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0084/paths/1a4166aed8b35c7751ed/report.json>)

Phase: $.mariadb.metrics.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.db.bundleTestDB = true (was false)`
- `$.mariadb.metrics.image.pullSecrets = [null, null, {"aaaaaa": [null, false, null], "aaaaaa3aaaa": null, "aaaaoa aiaaaaanaaavaaaaaoaaaakaaaaaaaa ataaaaaaahaaaa... [value shortened]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0084/paths/f3c891b2fda1d97f28f1/report.json>)

#### E368 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on phpmyadmin/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0084/paths/a4a0ea6ab697189bb963/report.json>)

#### E369 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on phpmyadmin/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "5.2.2-debian-12-r22")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0084/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0084>)

### [bitnami/pinniped](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pinniped>)

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

#### E528 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource config.concierge.pinniped.dev/v1alpha1/CredentialIssuer requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0085/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0085>)

### [bitnami/postgresql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql>)

Overview cell: 87

Status: failed | Attempts: 2616

Audit findings: 674. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.audit.clientMinMessages`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logConnections`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logDisconnections`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logHostname`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logLinePrefix`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.audit.logTimezone`: Undocumented values path (warning)
- 668 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E047 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: postgresql 17.1.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r51 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.volumePermissions.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/5356324f9a8a2798b69d/report.json>)

#### E048 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: postgresql 17.1.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... nvironment variables. Unrecognized images: - 00/bitnami/postgresql:17.6.0-debian-12-r4 -
00/bitnami/os-shell:12-debian-12-r51 - 00/bitnami/postgres-exporter:0.17.1-debian-12-r16 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/fa90b40f46c6c70d8821/report.json>)

#### E049 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: postgresql 17.1.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:17.6.0-debian-12-r4 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/postgresql")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/3f7165f1837241716c3c/report.json>)

#### E050 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: postgresql 17.1.2 / templates/update-password/new-secret.yaml

```text
execution error at (postgresql/templates/update-password/new-secret.yaml:24:24): The new postgres password is required!
```

Phase: $.passwordUpdateJob.enabled | Status: failed

Changed overrides (used together):
- `$.passwordUpdateJob.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/d2a199b91d47bb696ab7/report.json>)

#### E376 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 176: found
unexpected end of stream
```

Phase: $.primary.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.primary.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/9500a72d3c4e020c37bd/report.json>)

#### E377 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 179: did not
find expected key
```

Phase: $.global.postgresql.auth | Status: failed

Changed overrides (used together):
- `$.global.postgresql.auth.existingSecret = "\"" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/537424102b6e359c83d6/report.json>)

Phase: $.auth | Status: failed

Changed overrides (used together):
- `$.auth.existingSecret = "\"" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/9add85c17048305af4de/report.json>)

#### E378 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 186: found
unexpected end of stream
```

Phase: $.primary.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.primary.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/af9a77b4b696ef0a07df/report.json>)

#### E379 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 190: found
unexpected end of stream
```

Phase: $.primary.existingConfigmap | Status: failed

Changed overrides (used together):
- `$.primary.existingConfigmap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/5840f42f3422db400ece/report.json>)

Phase: $.primary.initdb.scriptsConfigMap | Status: failed

Changed overrides (used together):
- `$.primary.initdb.scriptsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/6fe4fceed847dfc423e1/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E380 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 37: block
sequence entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/097f6358a00dddbcdd83/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E381 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 64: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "17.6.0-debian-12-r4")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/8e79b7dd85a286cfaddb/report.json>)

#### E382 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/svc-headless.yaml: error converting YAML to JSON: yaml: line 29: found
unexpected end of stream
```

Phase: $.global.postgresql.service.ports | Status: failed

Changed overrides (used together):
- `$.global.postgresql.service.ports.postgresql = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/d57b5ec01cb611bf6306/report.json>)

#### E383 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql/templates/primary/svc.yaml: error converting YAML to JSON: yaml: line 24: found unexpected
end of stream
```

Phase: $.primary.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.primary.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/3e795faedefc2f10ac72/report.json>)

#### E551 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on postgresql/templates/secrets.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.secretAnnotations | Status: failed

Changed overrides (used together):
- `$.secretAnnotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/f65a210cb498cc13774c/report.json>)

#### E595 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[Diagnostic shortened; full text in artifacts] ... l" at <include "postgresql.v1.primary.fullname" .>: error calling include:
postgresql/templates/_helpers.tpl:21:17 executing "postgresql.v1.primary.fullname" at <include "postgresql.v1.chart.fullname" .>: error
calling include: postgresql/templates/_helpers.tpl:13:13 executing "postgresql.v1.chart.fullname" at <include "common.names.fullname" .>:
error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0086/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0086>)

### [bitnami/postgresql-ha](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql-ha>)

Overview cell: 88

Status: failed | Attempts: 1294

Audit findings: 732. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.concurrencyPolicy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backup.cronjob.containerSecurityContext`: Undocumented values path (warning)
- 726 additional audit findings in JSON.

Configuration rejections: 0 excluded; 1 adjusted and tested; 1 Helm verification renders (separate from manifest-test attempts).

#### E370 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql-ha/templates/pgpool/deployment.yaml: error converting YAML to JSON: yaml: line 32: block
sequence entries are not allowed in this context
```

Phase: $.postgresql.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.postgresql.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0087/paths/cf30406f7641ac44b0a6/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0087/paths/097f6358a00dddbcdd83/report.json>)

#### E371 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql-ha/templates/pgpool/deployment.yaml: error converting YAML to JSON: yaml: line 57: mapping
values are not allowed in this context
```

Phase: $.pgpool.image | Status: failed

Changed overrides (used together):
- `$.pgpool.image.tag = "" (was "4.6.3-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0087/paths/2d1d6d1a7cab03c2e42e/report.json>)

#### E372 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql-ha/templates/pgpool/service.yaml: error converting YAML to JSON: yaml: line 25: found
unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0087/paths/6e931799d09f8182f34b/report.json>)

#### E373 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql-ha/templates/postgresql/extended-configmap.yaml: error converting YAML to JSON: yaml: line
17: could not find expected ':'
```

Phase: $.postgresql.extendedConf | Status: failed

Changed overrides (used together):
- `$.postgresql.extendedConf = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0087/paths/ec3d694da0ed2a1dba65/report.json>)

#### E374 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql-ha/templates/postgresql/statefulset.yaml: error converting YAML to JSON: yaml: line 267:
found unexpected end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0087/paths/bc81b51736a9cdc4eda3/report.json>)

#### E375 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on postgresql-ha/templates/postgresql/statefulset.yaml: error converting YAML to JSON: yaml: line 277:
found unexpected end of stream
```

Phase: $.postgresql.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.postgresql.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0087/paths/238f0bb666b95e5ab2d1/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0087>)

### [bitnami/prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/prometheus>)

Overview cell: 89

Status: failed | Attempts: 769

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

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E051 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: prometheus 2.3.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:0.39.2-debian-12-r2 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.server.thanos.image.repository | Status: failed

Changed overrides (used together):
- `$.server.thanos.image.repository = "00" (was "bitnami/thanos")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0088/paths/73c2db4d5d8c19ba7e0d/report.json>)

#### E384 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on prometheus/templates/alertmanager/service.yaml: error converting YAML to JSON: yaml: line 28: found
unexpected end of stream
```

Phase: $.alertmanager.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.alertmanager.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0088/paths/87a8ecf6ca2e97f16653/report.json>)

#### E385 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on prometheus/templates/alertmanager/service.yaml: error converting YAML to JSON: yaml: line 29: found
unexpected end of stream
```

Phase: $.alertmanager.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.alertmanager.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0088/paths/dd04407af6e436d9bda0/report.json>)

#### E386 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on prometheus/templates/alertmanager/statefulset.yaml: error converting YAML to JSON: yaml: line 143: found
unexpected end of stream
```

Phase: $.alertmanager.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.alertmanager.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0088/paths/7f7b602303e3a6989aa1/report.json>)

#### E387 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on prometheus/templates/alertmanager/statefulset.yaml: error converting YAML to JSON: yaml: line 39: block
sequence entries are not allowed in this context
```

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0088/paths/097f6358a00dddbcdd83/report.json>)

#### E388 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on prometheus/templates/server/dep-sts.yaml: error converting YAML to JSON: yaml: line 63: mapping values
are not allowed in this context
```

Phase: $.server.image.tag | Status: failed

Changed overrides (used together):
- `$.server.image.tag = "" (was "3.5.0-debian-12-r3")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0088/paths/80b6cb2f8dcf3d2dcb4b/report.json>)

#### E389 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on prometheus/templates/server/service.yaml: error converting YAML to JSON: yaml: line 29: found unexpected
end of stream
```

Phase: $.server.service.loadBalancerClass | Status: failed

Changed overrides (used together):
- `$.server.service.loadBalancerClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0088/paths/9f3f709f4d6da41f46a0/report.json>)

#### E552 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on prometheus/templates/alertmanager/ingress.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.alertmanager.ingress | Status: failed

Changed overrides (used together):
- `$.alertmanager.ingress.annotations[""] = []`
- `$.alertmanager.ingress.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0088/paths/82b5d52c41968360ec5e/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0088>)

### [bitnami/pytorch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pytorch>)

Overview cell: 90

Status: failed | Attempts: 1490

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cloneFilesFromGit.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cloneFilesFromGit.extraVolumeMounts`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

Configuration rejections: 773 excluded; 55 adjusted and tested; 829 Helm verification renders (separate from manifest-test attempts).

#### E002 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: pytorch/templates/deployment.yaml:91:30 executing "pytorch/templates/deployment.yaml" at <{{template
"mxnet.volumePermissions.image" .}}>: template "mxnet.volumePermissions.image" not defined
```

Phase: $.volumePermissions.enabled | Status: failed

Changed overrides (used together):
- `$.volumePermissions.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/3c69035ba1a84ddc221e/report.json>)

#### E052 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: pytorch 5.0.0 / templates/NOTES.txt

```text
execution error at (pytorch/templates/NOTES.txt:69:3): VALUES VALIDATION: pytorch: architecture Invalid architecture selected. Valid values
are "distributed" and "standalone". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.architecture | Status: failed

Changed overrides (used together):
- `$.architecture = "" (was "standalone")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/ced06016017c2e34a34d/report.json>)

#### E080 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: pytorch 5.0.0 / templates/statefulset.yaml

```text
template: pytorch/templates/statefulset.yaml:7:7: executing "pytorch/templates/statefulset.yaml" at <eq $architecture "distributed">: error
calling eq: incompatible types for comparison: []interface {} and string
```

Phase: $.mode | Status: failed

Changed overrides (used together):
- `$.mode = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/5c93d0208a4c764db7b3/report.json>)

#### E390 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 136: did not find expected
',' or ']'
```

Phase: $.configMap | Status: failed

Changed overrides (used together):
- `$.configMap = [{}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/9c10555e6847d48e7166/report.json>)

#### E391 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 139: found unexpected end
of stream
```

Phase: $.persistence.mountPath | Status: failed

Changed overrides (used together):
- `$.persistence.mountPath = "'" (was "/bitnami/pytorch")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/44140e4ff5fe576f8d1e/report.json>)

#### E392 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 140: found unexpected end
of stream
```

Phase: $.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/6ba7d997c0ad5ab2417b/report.json>)

#### E393 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 141: found unexpected end
of stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/e4b1fa53526f192b7184/report.json>)

Phase: $.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/95d9e80fea15aed87f2a/report.json>)

#### E394 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 32: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/097f6358a00dddbcdd83/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E395 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 57: found character that
cannot start any token
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.digest = "0" (was "")`
- `$.image.registry = "" (was "docker.io")`
- `$.image.repository = "" (was "bitnami/pytorch")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/8e79b7dd85a286cfaddb/report.json>)

#### E396 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 59: could not find expected
':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/pytorch")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/3f7165f1837241716c3c/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/fa90b40f46c6c70d8821/report.json>)

#### E397 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/deployment.yaml: error converting YAML to JSON: yaml: line 76: did not find expected
key
```

Phase: $.entrypoint | Status: failed

Changed overrides (used together):
- `$.entrypoint.file = "\r" (was "")`
- `$.entrypoint.args = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/cba2f2c92b4a1013a6b6/report.json>)

#### E398 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/service.yaml: error converting YAML to JSON: yaml: line 15: did not find expected ','
or ']'
```

Phase: $.service.port | Status: failed

Changed overrides (used together):
- `$.service.port = [{}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/8519a498beb325a2a1ea/report.json>)

#### E399 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on pytorch/templates/service.yaml: error converting YAML to JSON: yaml: line 23: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/6e931799d09f8182f34b/report.json>)

#### E578 ([HH3002](#hh3002---incompatible-value-type-in-template))

**Incompatible value type in template** (template / violation). Severity: **error**. Align the template operation with the accepted input
types, or narrow the schema.

```text
[HH3002] Error: pytorch/templates/service.yaml:10:16 executing "pytorch/templates/service.yaml" at <include "common.names.namespace" .>:
error calling include: pytorch/charts/common/templates/_names.tpl:64:65 executing "common.names.namespace" at <63>: wrong type for value;
expected string; got []interface {}
```

Phase: $.namespaceOverride | Status: failed

Changed overrides (used together):
- `$.namespaceOverride = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/835d62e0a3e46b72c904/report.json>)

#### E596 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: pytorch/templates/serviceaccount.yaml:10:11 executing "pytorch/templates/serviceaccount.yaml" at <include
"pytorch.serviceAccountName" .>: error calling include: pytorch/templates/_helpers.tpl:68:16 executing "pytorch.serviceAccountName" at
<include "common.names.fullname" .>: error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0089/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0089>)

### [bitnami/rabbitmq](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq>)

Overview cell: 91

Status: failed | Attempts: 1007

Audit findings: 407. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.advancedConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.advancedConfigurationExistingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enableLoopbackUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.erlangCookie`: Undocumented values path (warning)
- 401 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E053 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: rabbitmq 16.0.16 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:4.1.3-debian-12-r1 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/rabbitmq")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/3f7165f1837241716c3c/report.json>)

#### E054 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: rabbitmq 16.0.16 / templates/validation.yaml

```text
execution error at (rabbitmq/templates/validation.yaml:6:4): VALUES VALIDATION: rabbitmq: memoryHighWatermark.type Invalid Memory high
watermark type. Valid values are "absolute" and "relative". Please set a valid mode (--set memoryHighWatermark.type="xxxx")
```

Phase: $.memoryHighWatermark.type | Status: failed

Changed overrides (used together):
- `$.memoryHighWatermark.type = "" (was "relative")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/1add63f1953bb5cbc012/report.json>)

#### E401 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on rabbitmq/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 176: block sequence
entries are not allowed in this context
```

Phase: $.hostPorts | Status: failed

Changed overrides (used together):
- `$.hostPorts.amqp = "-" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/fcada9ae3b1f71ab92ef/report.json>)

#### E402 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on rabbitmq/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 258: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/bc81b51736a9cdc4eda3/report.json>)

#### E403 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on rabbitmq/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 35: block sequence
entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E404 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on rabbitmq/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 60: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "4.1.3-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/8e79b7dd85a286cfaddb/report.json>)

#### E405 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on rabbitmq/templates/svc-headless.yaml: error converting YAML to JSON: yaml: line 18: block sequence
entries are not allowed in this context
```

Phase: $.service.portNames | Status: failed

Changed overrides (used together):
- `$.service.portNames.amqp = "-" (was "amqp")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/ea2b8dbfc4cd2f1be35f/report.json>)

#### E406 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on rabbitmq/templates/svc-headless.yaml: error converting YAML to JSON: yaml: line 32: found unexpected end
of stream
```

Phase: $.service.trafficDistribution | Status: failed

Changed overrides (used together):
- `$.service.trafficDistribution = "'" (was "PreferClose")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/76c21b9e4a991e167280/report.json>)

Phase: $.service.portNames.amqp | Status: failed

Changed overrides (used together):
- `$.service.portNames.amqp = "'" (was "amqp")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/6e16dc727c16fae9b8b2/report.json>)

#### E407 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on rabbitmq/templates/svc.yaml: error converting YAML to JSON: yaml: line 31: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/6e931799d09f8182f34b/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.extraSecrets | Status: failed

Changed overrides (used together):
- `$.extraSecrets[""] = null`

Manifest changes from rendered defaults (document and list order preserved):
- `$[10]: <absent> -> {"apiVersion": "apps/v1", "kind": "StatefulSet", "metadata": {"name": "hypothesis-rabbitmq", "namespace": "default", "la... [value shortened]`
- `$[4].data["rabbitmq-erlang-cookie"]: "b1kyZHRFWm9JckExRjZram9PMnp6dmpTVUE5aWFaNWo=" -> "NWN4Nk1HV0hFek9UUkhyZWdtbDJwWXQyZ1ppbWQ4aTM="`
- `$[4].data["rabbitmq-password"]: "WVg5Zzl2TnlyNFQwR1AxMQ==" -> "eUNBNUZ1NENnSHU5bDM3bQ=="`
- `$[5].apiVersion: "rbac.authorization.k8s.io/v1" -> "v1"`
- `$[5].kind: "Role" -> "Secret"`
- `$[5].metadata.name: "hypothesis-rabbitmq-endpoint-reader" -> null`
- 43 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/8d5af7393100c8ad3b02/report.json>)

#### E597 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: rabbitmq/templates/svc.yaml:9:11 executing "rabbitmq/templates/svc.yaml" at <include "common.names.fullname" .>: error
calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0090/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0090>)

### [bitnami/rabbitmq-cluster-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq-cluster-operator>)

Overview cell: 92

Status: failed | Attempts: 124

Audit findings: 387. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterOperator.containerPorts`: Undocumented values path (warning)
- 381 additional audit findings in JSON.

#### E400 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on rabbitmq-cluster-operator/templates/messaging-topology-operator/deployment.yaml: error converting YAML
to JSON: yaml: line 134: found unexpected end of stream
```

Phase: $.msgTopologyOperator.hostNetwork | Status: failed

Changed overrides (used together):
- `$.msgTopologyOperator.hostNetwork = "'" (was "false")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0091/paths/2cd3ab168c8c9d9390a6/report.json>)

#### E531 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.coreos.com/v1/PodMonitor requires an explicit JSON schema in resource_schemas
```

Phase: $.msgTopologyOperator.metrics.podMonitor | Status: failed

Changed overrides (used together):
- `$.msgTopologyOperator.metrics.podMonitor.enabled = true (was false)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[24].webhooks[0].clientConfig.caBundle: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUpTenhTTFRjM1hsdmVuaFlROWsyODh3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUxibGthOFovTWJsd01TTUhmUGVXR2N3RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- `$[24].webhooks[10].clientConfig.caBundle: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUpTenhTTFRjM1hsdmVuaFlROWsyODh3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUxibGthOFovTWJsd01TTUhmUGVXR2N3RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- `$[24].webhooks[11].clientConfig.caBundle: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUpTenhTTFRjM1hsdmVuaFlROWsyODh3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUxibGthOFovTWJsd01TTUhmUGVXR2N3RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- `$[24].webhooks[12].clientConfig.caBundle: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUpTenhTTFRjM1hsdmVuaFlROWsyODh3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUxibGthOFovTWJsd01TTUhmUGVXR2N3RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- `$[24].webhooks[1].clientConfig.caBundle: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUpTenhTTFRjM1hsdmVuaFlROWsyODh3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUxibGthOFovTWJsd01TTUhmUGVXR2N3RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- `$[24].webhooks[2].clientConfig.caBundle: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUpTenhTTFRjM1hsdmVuaFlROWsyODh3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLRENDQWhDZ0F3SUJBZ0lSQUxibGthOFovTWJsd01TTUhmUGVXR2N3RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- 10 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0091/paths/f5b92e77a4a9ef1e0505/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0091>)

### [bitnami/redis](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis>)

Overview cell: 93

Status: failed | Attempts: 3235

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

#### E004 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: redis/templates/replicas/application.yaml:52:36 executing "redis/templates/replicas/application.yaml" at <include (print
$.Template.BasePath "/scripts-configmap.yaml") .>: error calling include: redis/templates/scripts-configmap.yaml:997:27 executing
"redis/templates/scripts-configmap.yaml" at <4>: invalid value; expected string
```

Phase: $.replica.preExecCmds[*] | Status: failed

Changed overrides (used together):
- `$.replica.preExecCmds = [null]`
Absent from overrides: $.replica.preExecCmds["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/be395840f38a1a431dfc/report.json>)

#### E058 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 23.1.1 / templates/NOTES.txt

```text
execution error at (redis/templates/NOTES.txt:202:4): VALUES VALIDATION: redis: podSecurityPolicy.create In order to create
PodSecurityPolicy, you also need to enable podSecurityPolicy.enabled field
```

Phase: $.podSecurityPolicy | Status: failed

Changed overrides (used together):
- `$.podSecurityPolicy.create = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/2aa8d5f181a33c2db27f/report.json>)

#### E059 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 23.1.1 / templates/NOTES.txt

```text
execution error at (redis/templates/NOTES.txt:202:4): VALUES VALIDATION: redis: architecture Invalid architecture selected. Valid values are
"standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.architecture | Status: failed

Changed overrides (used together):
- `$.architecture = "" (was "replication")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/ced06016017c2e34a34d/report.json>)

#### E060 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 23.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r51 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.volumePermissions.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/5356324f9a8a2798b69d/report.json>)

Phase: $.sysctl.image.registry | Status: failed

Changed overrides (used together):
- `$.sysctl.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/164eb0cb42b29d26ea17/report.json>)

#### E061 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 23.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ...  likely to cause degraded security and performance, broken chart features, and missing
environment variables. Unrecognized images: - 00/bitnami/redis-sentinel:8.2.1-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.sentinel.image.registry | Status: failed

Changed overrides (used together):
- `$.sentinel.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/5a3852a59889fb38f858/report.json>)

#### E062 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 23.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... bian-12-r0 - 00/bitnami/redis-exporter:1.76.0-debian-12-r0 -
00/bitnami/os-shell:12-debian-12-r51 - 00/bitnami/kubectl:1.33.4-debian-12-r0 - 00/bitnami/os-shell:12-debian-12-r51 If you are sure you
want to proceed with non-standard containers, you can skip container image verification by setting the global parameter
'global.security.allowInsecureImages' to true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/fa90b40f46c6c70d8821/report.json>)

#### E063 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 23.1.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:8.2.1-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/redis")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/3f7165f1837241716c3c/report.json>)

#### E064 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis 23.1.1 / templates/master/application.yaml

```text
execution error at (redis/templates/master/application.yaml:241:25): ERROR: Preset key '' invalid. Allowed values are
xlarge,2xlarge,nano,micro,small,medium,large
```

Phase: $.master.resourcesPreset | Status: failed

Changed overrides (used together):
- `$.master.resourcesPreset = "" (was "nano")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/9f99d5510b4096f557ad/report.json>)

#### E414 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/configmap.yaml: error converting YAML to JSON: yaml: line 23: did not find expected key
```

Phase: $.master.disableCommands | Status: failed

Changed overrides (used together):
- `$.master.disableCommands = ["\r"]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/ae04aa76885c44fa960f/report.json>)

#### E415 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/configmap.yaml: error converting YAML to JSON: yaml: line 29: did not find expected key
```

Phase: $.replica.disableCommands | Status: failed

Changed overrides (used together):
- `$.replica.disableCommands = ["\r"]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/9ab33350907009275568/report.json>)

#### E416 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 100: did not find
expected alphabetic or numeric character
```

Phase: $.master.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.master.extraEnvVarsSecret = "&\n" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/ccefdbb7579095b420de/report.json>)

#### E417 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 151: could not find
expected ':'
```

Phase: $.master.sidecars | Status: failed

Changed overrides (used together):
- `$.master.sidecars = "0" (was [])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/c7403feeedefe030b388/report.json>)

#### E418 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 172: block sequence
entries are not allowed in this context
```

Phase: $.master.persistentVolumeClaimRetentionPolicy | Status: failed

Changed overrides (used together):
- `$.master.persistentVolumeClaimRetentionPolicy.enabled = true (was false)`
- `$.master.persistentVolumeClaimRetentionPolicy.whenDeleted = "-" (was "Retain")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/f7b4ee410da2b197fe30/report.json>)

#### E419 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 172: could not find
expected ':'
```

Phase: $.master.extraVolumes | Status: failed

Changed overrides (used together):
- `$.master.extraVolumes = "0" (was [])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/1d5abbc65ff6aafaa209/report.json>)

#### E420 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 174: found unexpected
end of stream
```

Phase: $.master.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.master.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/89b61466d9fa37c3d367/report.json>)

#### E421 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 187: found unexpected
end of stream
```

Phase: $.master.persistence.storageClass | Status: failed

Changed overrides (used together):
- `$.master.persistence.storageClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/8b1730de40416f0c86e2/report.json>)

#### E422 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 188: found unexpected
end of stream
```

Phase: $.master.persistence.subPathExpr | Status: failed

Changed overrides (used together):
- `$.master.persistence.subPathExpr = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/39a9588a7a1e4dfffc70/report.json>)

#### E423 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 40: block sequence
entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/097f6358a00dddbcdd83/report.json>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E424 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 66: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "8.2.1-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/8e79b7dd85a286cfaddb/report.json>)

#### E425 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 99: could not find
expected ':'
```

Phase: $.master | Status: failed

Changed overrides (used together):
- `$.master.extraEnvVars = "0" (was [])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/4566758e97e5febb1583/report.json>)

#### E426 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/service.yaml: error converting YAML to JSON: yaml: line 23: could not find
expected ':'
```

Phase: $.master.service.extraPorts | Status: failed

Changed overrides (used together):
- `$.master.service.extraPorts = "0" (was [])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/46d4cdd3516d8dd309b3/report.json>)

#### E427 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/master/service.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end
of stream
```

Phase: $.master.service.portNames | Status: failed

Changed overrides (used together):
- `$.master.service.portNames.redis = "'" (was "tcp-redis")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/a2c6f5f18c068189a8f3/report.json>)

#### E428 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 105: could not find
expected ':'
```

Phase: $.replica.extraEnvVars | Status: failed

Changed overrides (used together):
- `$.replica.extraEnvVars = "0" (was [])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/5cf5c11737caaf832285/report.json>)

#### E429 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 185: block sequence
entries are not allowed in this context
```

Phase: $.replica.persistentVolumeClaimRetentionPolicy | Status: failed

Changed overrides (used together):
- `$.replica.persistentVolumeClaimRetentionPolicy.enabled = true (was false)`
- `$.replica.persistentVolumeClaimRetentionPolicy.whenDeleted = "-" (was "Retain")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/512bb5d90a0179e7392a/report.json>)

#### E430 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 187: found
unexpected end of stream
```

Phase: $.replica.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.replica.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/6779164cb76c2dbb83a8/report.json>)

#### E431 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 203: found
unexpected end of stream
```

Phase: $.replica.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.replica.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/b71ec3b23bacb342be46/report.json>)

Phase: $.replica.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.replica.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/f76951b7203d44d5892f/report.json>)

#### E432 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/replicas/service.yaml: error converting YAML to JSON: yaml: line 23: could not find
expected ':'
```

Phase: $.replica.service | Status: failed

Changed overrides (used together):
- `$.replica.service.extraPorts = "0" (was [])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/26a0e89b5aead3761292/report.json>)

Phase: $.replica.service.extraPorts | Status: failed

Changed overrides (used together):
- `$.replica.service.extraPorts = "0" (was [])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/4d7a723a5158cf590361/report.json>)

#### E433 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/replicas/service.yaml: error converting YAML to JSON: yaml: line 27: found unexpected
end of stream
```

Phase: $.replica.service.clusterIP | Status: failed

Changed overrides (used together):
- `$.replica.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/c472c95b8d817657b6a5/report.json>)

#### E434 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/scripts-configmap.yaml: error converting YAML to JSON: yaml: line 31: did not find
expected key
```

Phase: $.master.command | Status: failed

Changed overrides (used together):
- `$.master.command = "\r" (was [])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/f165a41ec438e5ca329c/report.json>)

#### E435 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis/templates/scripts-configmap.yaml: error converting YAML to JSON: yaml: line 86: did not find
expected key
```

Phase: $.replica.command[*] | Status: failed

Changed overrides (used together):
- `$.replica.command = ["\r"]`
Absent from overrides: $.replica.command["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/9cb41778ee138755ba69/report.json>)

#### E513 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] level=INFO msg="warning: cannot overwrite table with non table for redis.replica.persistence.dataSource (map[])" level=INFO
msg="warning: cannot overwrite table with non table for redis.replica.persistence.dataSource (map[])" Error: YAML parse error on
redis/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 202: found unexpected end of stream
```

Phase: $.replica.persistence | Status: failed

Changed overrides (used together):
- `$.replica.persistence.dataSource = "\"" (was {})`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/d1ee9834ab168e5d5661/report.json>)

#### E514 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] level=INFO msg="warning: cannot overwrite table with non table for redis.replica.podAnnotations (map[])" level=INFO msg="warning:
cannot overwrite table with non table for redis.replica.podAnnotations (map[])" Error: YAML parse error on
redis/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 39: could not find expected ':'
```

Phase: $.replica.podAnnotations | Status: failed

Changed overrides (used together):
- `$.replica.podAnnotations = "0" (was {})`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/b22cf19fc751f99a2d84/report.json>)

#### E524 ([HH1103](#hh1103---missing-resource-api-version-or-kind))

**Missing resource API version or kind** (manifest / violation). Severity: **error**. Supply both resource identifiers in every branch that
emits a resource.

```text
[HH1103] resource has no nonempty kind
```

Phase: $.master.kind | Status: failed

Changed overrides (used together):
- `$.master.kind = "" (was "StatefulSet")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[12].metadata.labels["app.kubernetes.io/component"]: "master" -> "replica"`
- `$[12].metadata.name: "hypothesis-redis-master" -> "hypothesis-redis-replicas"`
- `$[12].spec.replicas: 1 -> 3`
- `$[12].spec.selector.matchLabels["app.kubernetes.io/component"]: "master" -> "replica"`
- `$[12].spec.template.metadata.annotations["checksum/secret"]: "b2bee6b8dea848aec0e96f938ef2100daa45a220a12bc86514303db57fe3599f" -> "8379b4784bc109613e43088ac4b136ef2194a74da82d938082c037139c64f955"`
- `$[12].spec.template.metadata.labels["app.kubernetes.io/component"]: "master" -> "replica"`
- 47 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/6825b84e4a3133e46b8f/report.json>)

Phase: $.replica.kind | Status: failed

Changed overrides (used together):
- `$.replica.kind = "" (was "StatefulSet")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[12].spec.template.metadata.annotations["checksum/secret"]: "b2bee6b8dea848aec0e96f938ef2100daa45a220a12bc86514303db57fe3599f" -> "4e098f47876ec8078dc6c8bcc170a890cd80bf471d41e6f13db78a7f7d71d1ff"`
- `$[13].kind: "StatefulSet" -> null`
- `$[13].spec.serviceName: "hypothesis-redis-headless" -> <absent>`
- `$[13].spec.template.metadata.annotations["checksum/secret"]: "b2bee6b8dea848aec0e96f938ef2100daa45a220a12bc86514303db57fe3599f" -> "4e098f47876ec8078dc6c8bcc170a890cd80bf471d41e6f13db78a7f7d71d1ff"`
- `$[13].spec.template.spec.volumes[5]: <absent> -> {"name": "redis-data", "emptyDir": {}}`
- `$[13].spec.volumeClaimTemplates: [{"apiVersion": "v1", "kind": "PersistentVolumeClaim", "metadata": {"name": "redis-data", "labels": {"app.kubernetes.io/... [value shortened] -> <absent>`
- 1 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/1ff1c084a415aaf5b427/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.replica.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.replica.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[12].spec.template.metadata.annotations["checksum/secret"]: "b2bee6b8dea848aec0e96f938ef2100daa45a220a12bc86514303db57fe3599f" -> "0e54063a941a904c6d7e7c714b5ad287420c7f7d781d0eb0278544eb8b6e72d6"`
- `$[13].spec.template.metadata.annotations["checksum/secret"]: "b2bee6b8dea848aec0e96f938ef2100daa45a220a12bc86514303db57fe3599f" -> "0e54063a941a904c6d7e7c714b5ad287420c7f7d781d0eb0278544eb8b6e72d6"`
- `$[13].spec.template.spec.serviceAccountName: "hypothesis-redis-replica" -> 0`
- `$[4].metadata.name: "hypothesis-redis-replica" -> 0`
- `$[5].data["redis-password"]: "VUYyUzAyOHZNNw==" -> "c2J1d200R2dXVA=="`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/4ab7f4deb73205f9fca5/report.json>)

#### E553 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.sentinel.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/150b8173cbcbd8d0e174/report.json>)

#### E554 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on redis/templates/master/application.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.master.annotations | Status: failed

Changed overrides (used together):
- `$.master.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/0091d50a34ab71fa3525/report.json>)

#### E555 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on redis/templates/replicas/application.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.replica.annotations | Status: failed

Changed overrides (used together):
- `$.replica.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/0fbae699259af70c93c1/report.json>)

#### E556 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on redis/templates/replicas/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.replica.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.replica.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/c85519e2d9e04d14f0b8/report.json>)

#### E557 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on redis/templates/secret.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal number
into Go struct field .metadata.annotations of type map[string]string
```

Phase: $.secretAnnotations | Status: failed

Changed overrides (used together):
- `$.secretAnnotations = "0" (was {})`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/f65a210cb498cc13774c/report.json>)

#### E558 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on redis/templates/svc-external.yaml: error unmarshaling JSON: while decoding JSON: json: cannot unmarshal
array into Go struct field .metadata.annotations. of type string
```

Phase: $.sentinel.externalAccess | Status: failed

Changed overrides (used together):
- `$.sentinel.externalAccess.enabled = true (was false)`
- `$.sentinel.externalAccess.service.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/d41c66d18464a11b6baa/report.json>)

#### E572 ([HH3001](#hh3001---template-accesses-a-missing-object))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/37081c129204c3c032e8/report.json>)

#### E598 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: redis/templates/_helpers.tpl:151:37 executing "redis.replicaServiceAccountName" at <include "common.names.fullname" .>:
error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0092/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0092>)

### [bitnami/redis-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis-cluster>)

Overview cell: 94

Status: failed | Attempts: 1417

Audit findings: 371. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.hostMode`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.disableLoadBalancerIP`: Undocumented values path
  (warning)
- 365 additional audit findings in JSON.

Configuration rejections: 0 excluded; 10 adjusted and tested; 10 Helm verification renders (separate from manifest-test attempts).

#### E003 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: redis-cluster/templates/secret.yaml:10:20 executing "redis-cluster/templates/secret.yaml" at <{{template
"common.names.fullname" .}}>: template "common.names.fullname" not defined
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/e2cac8a5225634937910/report.json>)

#### E055 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis-cluster 13.0.5 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r51 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.volumePermissions.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/5356324f9a8a2798b69d/report.json>)

#### E056 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis-cluster 13.0.5 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ages: - 00/bitnami/redis-cluster:8.2.1-debian-12-r0 -
00/bitnami/os-shell:12-debian-12-r51 - 00/bitnami/redis-exporter:1.76.0-debian-12-r0 - 00/bitnami/os-shell:12-debian-12-r51 If you are sure
you want to proceed with non-standard containers, you can skip container image verification by setting the global parameter
'global.security.allowInsecureImages' to true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/fa90b40f46c6c70d8821/report.json>)

#### E057 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: redis-cluster 13.0.5 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:8.2.1-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/redis-cluster")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/3f7165f1837241716c3c/report.json>)

#### E408 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis-cluster/templates/redis-statefulset.yaml: error converting YAML to JSON: yaml: line 201: found
unexpected end of stream
```

Phase: $.existingSecret | Status: failed

Changed overrides (used together):
- `$.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/bf7372b3862550c529f3/report.json>)

#### E409 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis-cluster/templates/redis-statefulset.yaml: error converting YAML to JSON: yaml: line 202: found
unexpected end of stream
```

Phase: $.persistence.path | Status: failed

Changed overrides (used together):
- `$.persistence.path = "'" (was "/bitnami/redis/data")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/909ebb7fe60c66c7c8df/report.json>)

#### E410 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis-cluster/templates/redis-statefulset.yaml: error converting YAML to JSON: yaml: line 39: did not
find expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/097f6358a00dddbcdd83/report.json>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E411 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis-cluster/templates/redis-statefulset.yaml: error converting YAML to JSON: yaml: line 64: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "8.2.1-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/8e79b7dd85a286cfaddb/report.json>)

#### E412 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis-cluster/templates/redis-statefulset.yaml: error converting YAML to JSON: yaml: line 78: did not
find expected key
```

Phase: $.redis.podManagementPolicy | Status: failed

Changed overrides (used together):
- `$.redis.podManagementPolicy = "'" (was "Parallel")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/5bb219882e7611d58704/report.json>)

#### E413 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redis-cluster/templates/redis-svc.yaml: error converting YAML to JSON: yaml: line 23: found unexpected
end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0093/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0093>)

### [bitnami/redmine](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redmine>)

Overview cell: 95

Status: failed | Attempts: 380

Audit findings: 374. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- 368 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E021 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
execution error at (mariadb/templates/NOTES.txt:74:4): VALUES VALIDATION: mariadb: architecture Invalid architecture selected. Valid values
are "standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.mariadb.architecture | Status: failed

Changed overrides (used together):
- `$.mariadb.architecture = "" (was "standalone")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0094/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E023 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0094/paths/e9b2bd06f74a17778834/report.json>)

#### E436 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redmine/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line
189: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0094/paths/a0cdb2ba618083d9a8df/report.json>)

#### E437 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on redmine/templates/deployment.yaml: error converting YAML to JSON: yaml: line 151: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0094/paths/bc81b51736a9cdc4eda3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0094>)

### [bitnami/schema-registry](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/schema-registry>)

Overview cell: 96

Status: failed | Attempts: 518

Audit findings: 277. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.jksSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.keystorePassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.kafka.saslMechanism`: Undocumented values path (warning)
- 271 additional audit findings in JSON.

#### E018 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: kafka 32.3.11 / templates/NOTES.txt

```text
execution error at (kafka/templates/NOTES.txt:340:4): VALUES VALIDATION: kafka: externalAccess.broker.service.type Available service type
for external access are NodePort, LoadBalancer or ClusterIP.
```

Phase: $.kafka.externalAccess.broker.service | Status: failed

Changed overrides (used together):
- `$.kafka.externalAccess.broker.service.type = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0095/paths/143256f1becb14c9530f/report.json>)

#### E438 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on schema-registry/charts/kafka/templates/controller-eligible/configmap.yaml: error converting YAML to
JSON: yaml: line 37: could not find expected ':'
```

Phase: $.kafka.controller.overrideConfiguration | Status: failed

Changed overrides (used together):
- `$.kafka.controller.overrideConfiguration["\r"] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0095/paths/118f580dd2a9a5d2f7b2/report.json>)

#### E439 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on schema-registry/charts/kafka/templates/controller-eligible/statefulset.yaml: error converting YAML to
JSON: yaml: line 285: did not find expected ',' or ']'
```

Phase: $.kafka.controller.logPersistence | Status: failed

Changed overrides (used together):
- `$.kafka.controller.logPersistence.mountPath = "[Ma"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0095/paths/6c7862f4d34ff3d72ede/observed-failure.json>)

#### E440 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on schema-registry/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 55: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- ``$.image["t`g"] = null``
- `$.image.tag = "" (was "8.0.0-debian-12-r4")`
- `$.image.pullPolicy = ":a#QaMoO@'XasaB0aa*agr<a" (was "IfNotPresent")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0095/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0095>)

### [bitnami/scylladb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/scylladb>)

Overview cell: 97

Status: failed | Attempts: 345

Audit findings: 390. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.annotations`: Undocumented values path (warning)
- 384 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E441 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on scylladb/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 198: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0096/paths/bc81b51736a9cdc4eda3/report.json>)

#### E442 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on scylladb/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 35: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0096/paths/a4a0ea6ab697189bb963/report.json>)

#### E443 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on scylladb/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 59: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2025.2.2-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0096/paths/8e79b7dd85a286cfaddb/report.json>)

#### E559 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on scylladb/templates/individual-svc.yaml: error unmarshaling JSON: while decoding JSON: json: cannot
unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.service.internal | Status: failed

Changed overrides (used together):
- `$.service.internal.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0096/paths/b768ca9fe0c4043c8f02/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0096>)

### [bitnami/sealed-secrets](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sealed-secrets>)

Overview cell: 98

Status: failed | Attempts: 934

Audit findings: 213. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.additionalNamespaces`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 207 additional audit findings in JSON.

Configuration rejections: 0 excluded; 29 adjusted and tested; 29 Helm verification renders (separate from manifest-test attempts).

#### E065 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: sealed-secrets 2.5.20 / templates/deployment.yaml

```text
execution error at (sealed-secrets/templates/deployment.yaml:120:19): Annotation values have to be strings
```

Phase: $.privateKeyAnnotations | Status: failed

Changed overrides (used together):
- `$.privateKeyAnnotations[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/9ecfe56523b14501b53f/report.json>)

#### E066 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: sealed-secrets 2.5.20 / templates/deployment.yaml

```text
execution error at (sealed-secrets/templates/deployment.yaml:131:19): Label values have to be strings
```

Phase: $.privateKeyLabels | Status: failed

Changed overrides (used together):
- `$.privateKeyLabels[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/651278c27cba1b79baca/report.json>)

#### E444 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on sealed-secrets/templates/deployment.yaml: error converting YAML to JSON: yaml: line 110: found
unexpected end of stream
```

Phase: $.revisionHistoryLimit | Status: failed

Changed overrides (used together):
- `$.revisionHistoryLimit = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/6ebbfa8871a0f66d1dde/report.json>)

#### E445 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on sealed-secrets/templates/deployment.yaml: error converting YAML to JSON: yaml: line 112: found
unexpected end of stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/e4b1fa53526f192b7184/report.json>)

#### E446 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on sealed-secrets/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E447 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on sealed-secrets/templates/deployment.yaml: error converting YAML to JSON: yaml: line 52: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "0.31.0-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/8e79b7dd85a286cfaddb/report.json>)

#### E448 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on sealed-secrets/templates/deployment.yaml: error converting YAML to JSON: yaml: line 54: could not find
expected ':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/sealed-secrets-controller")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/3f7165f1837241716c3c/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/fa90b40f46c6c70d8821/report.json>)

#### E449 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on sealed-secrets/templates/service.yaml: error converting YAML to JSON: yaml: line 23: found unexpected
end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/6e931799d09f8182f34b/report.json>)

#### E532 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.coreos.com/v1/ServiceMonitor requires an explicit JSON schema in resource_schemas
```

Phase: $.metrics.serviceMonitor | Status: failed

Changed overrides (used together):
- `$.metrics.serviceMonitor.enabled = true (was false)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[10]: <absent> -> {"apiVersion": "monitoring.coreos.com/v1", "kind": "ServiceMonitor", "metadata": {"name": "hypothesis-sealed-secrets", "... [value shortened]`
- `$[8].spec.ports[1]: <absent> -> {"port": 8081, "name": "metrics", "targetPort": 8081}`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/650f12c383805ab938cd/report.json>)

#### E599 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: sealed-secrets/templates/_helpers.tpl:25:16 executing "sealed-secrets.serviceAccountName" at <include
"common.names.fullname" .>: error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0097/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0097>)

### [bitnami/seaweedfs](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/seaweedfs>)

Overview cell: 99

Status: failed | Attempts: 228

Audit findings: 1241. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDefault`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- 1235 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E021 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
execution error at (mariadb/templates/NOTES.txt:74:4): VALUES VALIDATION: mariadb: architecture Invalid architecture selected. Valid values
are "standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.mariadb.architecture | Status: failed

Changed overrides (used together):
- `$.mariadb.architecture = "" (was "standalone")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0098/paths/1ff74c0fd3bc5bc52c04/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0098>)

### [bitnami/solr](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/solr>)

Overview cell: 100

Status: failed | Attempts: 518

Audit findings: 411. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminUsername`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- 405 additional audit findings in JSON.

#### E450 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on solr/charts/zookeeper/templates/scripts-configmap.yaml: error converting YAML to JSON: yaml: line 6:
could not find expected ':'
```

Phase: $.zookeeper.nameOverride | Status: failed

Changed overrides (used together):
- `$.zookeeper.nameOverride = "\r"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0099/paths/4090e5b9cd4a30941422/report.json>)

#### E451 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on solr/charts/zookeeper/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 123: could
not find expected ':'
```

Phase: $.zookeeper.clusterDomain | Status: failed

Changed overrides (used together):
- `$.zookeeper.clusterDomain = "\r"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0099/paths/ee0c36c64846751a6b3f/report.json>)

#### E452 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on solr/charts/zookeeper/templates/svc.yaml: error converting YAML to JSON: yaml: line 31: found unexpected
end of stream
```

Phase: $.zookeeper.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.zookeeper.service.sessionAffinity = "'"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0099/paths/c9fe0b377024171ff1fc/report.json>)

#### E453 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on solr/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 225: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0099/paths/bc81b51736a9cdc4eda3/report.json>)

#### E454 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on solr/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 39: did not find expected ','
or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0099/paths/a4a0ea6ab697189bb963/report.json>)

#### E455 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on solr/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 64: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.9.0-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0099/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0099>)

### [bitnami/sonarqube](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sonarqube>)

Overview cell: 101

Status: failed | Attempts: 441

Audit findings: 419. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 413 additional audit findings in JSON.

#### E067 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: sonarqube 8.1.18 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - A/c;CaNMC*:|'a#).:25.8.0-debian-12-r2 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.agt = null`
- `$.image.debug = true (was false)`
- `$.image["Ua6*-kV"]["Maa<Laaaaaadaaaa,"] = {}`
- `$.image["Ua6*-kV"].aaaaaaaaa = []`
- `$.image["Ua6*-kV"].a = -2.6554551002088387e-171`
- `$.image.registry = "A" (was "docker.io")`
- 2 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0100/paths/8e79b7dd85a286cfaddb/report.json>)

#### E456 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on sonarqube/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml:
line 189: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0100/paths/a0cdb2ba618083d9a8df/report.json>)

#### E457 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on sonarqube/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON: yaml:
line 17: could not find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0100/paths/91bb86cdd8574ec43d3d/report.json>)

#### E560 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on sonarqube/charts/postgresql/templates/primary/networkpolicy.yaml: error unmarshaling JSON: while
decoding JSON: json: cannot unmarshal array into Go struct field .metadata.name of type string
```

Phase: $.global.postgresql.auth | Status: failed

Changed overrides (used together):
- `$.global.postgresql.fullnameOverride = [null]`
- `$.global.postgresql.auth = {}`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0100/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0100>)

### [bitnami/spark](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/spark>)

Overview cell: 102

Status: time-limit | Attempts: 1

Audit findings: 350. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 344 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0101>)

### [bitnami/superset](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/superset>)

Overview cell: 103

Status: failed | Attempts: 182

Audit findings: 752. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.email`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFiles`: Undocumented values path (warning)
- 746 additional audit findings in JSON.

#### E561 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on superset/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0102/paths/afbbf9ab6c6be5d414aa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0102>)

### [bitnami/tensorflow-resnet](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tensorflow-resnet>)

Overview cell: 104

Status: failed | Attempts: 632

Audit findings: 172. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.client.image.pullPolicy`: Undocumented values path (warning)
- 166 additional audit findings in JSON.

Configuration rejections: 0 excluded; 36 adjusted and tested; 36 Helm verification renders (separate from manifest-test attempts).

#### E458 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tensorflow-resnet/templates/deployment.yaml: error converting YAML to JSON: yaml: line 170: found
unexpected end of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/57504c968732d9714f10/report.json>)

#### E459 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tensorflow-resnet/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/097f6358a00dddbcdd83/report.json>)

Phase: $.server.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.server.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/7e6752d8aee9080df9cf/report.json>)

#### E460 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tensorflow-resnet/templates/deployment.yaml: error converting YAML to JSON: yaml: line 55: could not
find expected ':'
```

Phase: $.client.image.registry | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.client.image.registry = "\r" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/c7b0ad2c6e1b5f0ff3bc/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/fa90b40f46c6c70d8821/report.json>)

#### E461 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tensorflow-resnet/templates/deployment.yaml: error converting YAML to JSON: yaml: line 93: mapping
values are not allowed in this context
```

Phase: $.server.image.tag | Status: failed

Changed overrides (used together):
- `$.server.image.tag = "" (was "2.19.1-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/80b6cb2f8dcf3d2dcb4b/report.json>)

#### E462 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tensorflow-resnet/templates/deployment.yaml: error converting YAML to JSON: yaml: line 95: could not
find expected ':'
```

Phase: $.server.image.registry | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.server.image.registry = "\r" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/e2f467218b148f0e690b/report.json>)

Phase: $.server.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.server.image.repository = "\r" (was "bitnami/tensorflow-serving")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/5cc6aed3945d4ab1555e/report.json>)

#### E463 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tensorflow-resnet/templates/service.yaml: error converting YAML to JSON: yaml: line 25: found unexpected
end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/6e931799d09f8182f34b/report.json>)

#### E464 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tensorflow-resnet/templates/service.yaml: error converting YAML to JSON: yaml: line 27: found unexpected
end of stream
```

Phase: $.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.restApi = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/afbac7d295ec4c0a2908/report.json>)

#### E600 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: tensorflow-resnet/templates/serviceaccount.yaml:10:11 executing "tensorflow-resnet/templates/serviceaccount.yaml" at
<include "tensorflow-resnet.serviceAccountName" .>: error calling include: tensorflow-resnet/templates/_helpers.tpl:27:16 executing
"tensorflow-resnet.serviceAccountName" at <include "common.names.fullname" .>: error calling include: template: no template
"common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0103/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0103>)

### [bitnami/thanos](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/thanos>)

Overview cell: 105

Status: failed | Attempts: 709

Audit findings: 1750. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auth.basicAuthUsers`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketCacheConfig`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.bucketweb.automountServiceAccountToken`: Undocumented values path (warning)
- 1744 additional audit findings in JSON.

#### E562 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on thanos/templates/storegateway/ingress-grpc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations.a of type string
```

Phase: $.storegateway.ingress.grpc | Status: failed

Changed overrides (used together):
- `$.storegateway.ingress.grpc.annotations["aaaQa@a"] = null`
- `$.storegateway.ingress.grpc.annotations.a = []`
- `$.storegateway.ingress.grpc.annotations.extractor_sha256 = null`
- `$.storegateway.ingress.grpc.annotations[""] = null`
- `$.storegateway.ingress.grpc.annotations._ = null`
- `$.storegateway.ingress.grpc.annotations["kgq9a?aaaIaaa\r=a8usa"] = null`
- 3 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0104/paths/a9ea280c56b0f3c82224/report.json>)

#### E573 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: thanos/templates/receive/tls-secrets.yaml:21:14 executing "thanos/templates/receive/tls-secrets.yaml" at <.certificate>: nil
pointer evaluating interface {}.certificate
```

Phase: $.receive.ingress | Status: failed

Changed overrides (used together):
- `$.receive.ingress.apiVersion = "aa" (was "")`
- `$.receive.ingress.secrets = [null, null, true]`
- `$.receive.ingress.annotations["au6Ok^j\ra"][""].aaoa8 = [-2.220446049250313e-16, true, null]`
- `$.receive.ingress.annotations["au6Ok^j\ra"][""]["!"]["a\raa+aa5aaa"] = 1798827`
- `$.receive.ingress.annotations["au6Ok^j\ra"][""]["!"]["aaaafaT\n<aa}uaraaa"] = {}`
- `$.receive.ingress.annotations["au6Ok^j\ra"][""][""] = [["aaaaaaaaWaa"], -8.733577440645727e-178, ["~aaa", "aa,a", 54]]`
- 17 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0104/paths/ac282c5c8f7cf306df21/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0104>)

### [bitnami/tomcat](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tomcat>)

Overview cell: 106

Status: failed | Attempts: 1221

Audit findings: 266. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.catalinaOpts`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 260 additional audit findings in JSON.

Configuration rejections: 0 excluded; 39 adjusted and tested; 39 Helm verification renders (separate from manifest-test attempts).

#### E005 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: tomcat/templates/svc.yaml:9:20 executing "tomcat/templates/svc.yaml" at <{{template "common.names.fullname" .}}>: template
"common.names.fullname" not defined
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/e2cac8a5225634937910/report.json>)

#### E465 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tomcat/templates/deployment.yaml: error converting YAML to JSON: yaml: line 140: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/bc81b51736a9cdc4eda3/report.json>)

#### E466 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tomcat/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/097f6358a00dddbcdd83/report.json>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E467 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tomcat/templates/deployment.yaml: error converting YAML to JSON: yaml: line 54: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "11.0.10-debian-12-r4")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/8e79b7dd85a286cfaddb/report.json>)

#### E468 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tomcat/templates/deployment.yaml: error converting YAML to JSON: yaml: line 56: could not find expected
':'
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.image.repository = "\r" (was "bitnami/tomcat")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/3f7165f1837241716c3c/report.json>)

#### E469 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tomcat/templates/svc.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/6e931799d09f8182f34b/report.json>)

#### E470 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on tomcat/templates/svc.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end of stream
```

Phase: $.service.nodePorts.http | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/c91d7fbded4704da55d3/report.json>)

Phase: $.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0105/paths/afbac7d295ec4c0a2908/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0105>)

### [bitnami/valkey](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey>)

Overview cell: 107

Status: failed | Attempts: 2066

Audit findings: 686. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.auth.enabled`: Missing values description (info)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.sentinel`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.usePasswordFileFromSecret`: Undocumented values path (warning)
- 680 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E071 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: valkey 4.0.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... likely to cause degraded security and performance, broken chart features, and missing
environment variables. Unrecognized images: - 00/bitnami/valkey-sentinel:8.1.3-debian-12-r3 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.sentinel.image.registry | Status: failed

Changed overrides (used together):
- `$.sentinel.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/5a3852a59889fb38f858/report.json>)

#### E072 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: valkey 4.0.2 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:8.1.3-debian-12-r3 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/valkey")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/3f7165f1837241716c3c/report.json>)

#### E477 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/configmap.yaml: error converting YAML to JSON: yaml: line 30: did not find expected key
```

Phase: $.replica.disableCommands | Status: failed

Changed overrides (used together):
- `$.replica.disableCommands = ["\r"]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/9ab33350907009275568/report.json>)

#### E478 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/primary/application.yaml: error converting YAML to JSON: yaml: line 164: could not find
expected ':'
```

Phase: $.auth | Status: failed

Changed overrides (used together):
- `$.auth.existingSecret = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/9add85c17048305af4de/report.json>)

#### E479 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/primary/application.yaml: error converting YAML to JSON: yaml: line 174: found
unexpected end of stream
```

Phase: $.primary.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.primary.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/9500a72d3c4e020c37bd/report.json>)

#### E480 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/primary/application.yaml: error converting YAML to JSON: yaml: line 40: block sequence
entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/097f6358a00dddbcdd83/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E481 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/primary/application.yaml: error converting YAML to JSON: yaml: line 66: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "8.1.3-debian-12-r3")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/8e79b7dd85a286cfaddb/report.json>)

#### E482 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/primary/pdb.yaml: error converting YAML to JSON: yaml: line 20: found unexpected end of
stream
```

Phase: $.primary.pdb.minAvailable | Status: failed

Changed overrides (used together):
- `$.primary.pdb.minAvailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/5921565551850813576d/report.json>)

#### E483 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/primary/service.yaml: error converting YAML to JSON: yaml: line 27: found unexpected
end of stream
```

Phase: $.primary.service.sessionAffinity | Status: failed

Changed overrides (used together):
- `$.primary.service.sessionAffinity = "'" (was "None")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/3e795faedefc2f10ac72/report.json>)

#### E484 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 187: found
unexpected end of stream
```

Phase: $.replica.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.replica.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/6779164cb76c2dbb83a8/report.json>)

#### E485 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 189: could not
find expected ':'
```

Phase: $.replica.persistence | Status: failed

Changed overrides (used together):
- `$.replica.persistence.stoargeClass = null`
- `$.replica.persistence.selector["&KDaa"] = [{}, "aaaa-", [{}, [[], {}], {"ab": {"": "a", "a": -5.538738876083396e+16, "aaH": 7.562432741181185e-28}}]]`
- `$.replica.persistence.selector.a = -6.566947378002852e+16`
- `$.replica.persistence.selector["aqf'"] = []`
- `$.replica.persistence.selector["a+:in"] = [0.0, [], []]`
- `$.replica.persistence.selector["{-p.Ja"] = []`
- 16 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/d1ee9834ab168e5d5661/report.json>)

#### E486 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/replicas/application.yaml: error converting YAML to JSON: yaml: line 203: found
unexpected end of stream
```

Phase: $.replica.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.replica.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/b71ec3b23bacb342be46/report.json>)

Phase: $.replica.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.replica.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/f76951b7203d44d5892f/report.json>)

#### E487 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/replicas/service.yaml: error converting YAML to JSON: yaml: line 28: found unexpected
end of stream
```

Phase: $.replica.service.clusterIP | Status: failed

Changed overrides (used together):
- `$.replica.service.clusterIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/c472c95b8d817657b6a5/report.json>)

#### E488 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey/templates/scripts-configmap.yaml: error converting YAML to JSON: yaml: line 81: did not find
expected key
```

Phase: $.replica.command[*] | Status: failed

Changed overrides (used together):
- `$.replica.command = ["\r"]`
Absent from overrides: $.replica.command["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/9cb41778ee138755ba69/report.json>)

#### E525 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.replica.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.replica.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[12].spec.template.metadata.annotations["checksum/secret"]: "866989d56e55314c0d3aa4790fde3431302e9c3369d7b0ca7b0426b39b99e52a" -> "b3d7ed079344e81b4a75fd89e89170c0e96ce28a7fafa94193f8519594233c26"`
- `$[13].spec.template.metadata.annotations["checksum/secret"]: "24270ac3e453f668aebe0a7ac31913d1533e29df57ab348e9dd80d84ed85ec2e" -> "7a0c842aa885c890fe316f278f4d69cf7390eae983f726b4f1627892dcc54009"`
- `$[13].spec.template.spec.serviceAccountName: "hypothesis-valkey-replica" -> 0`
- `$[4].metadata.name: "hypothesis-valkey-replica" -> 0`
- `$[5].data["valkey-password"]: "NVhtYUJWVFBuOA==" -> "c2kycXl4UjhvbQ=="`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/4ab7f4deb73205f9fca5/report.json>)

#### E579 ([HH3002](#hh3002---incompatible-value-type-in-template))

**Incompatible value type in template** (template / violation). Severity: **error**. Align the template operation with the accepted input
types, or narrow the schema.

```text
[HH3002] Error: valkey/templates/replicas/application.yaml:50:36 executing "valkey/templates/replicas/application.yaml" at <include (print
$.Template.BasePath "/scripts-configmap.yaml") .>: error calling include: valkey/templates/scripts-configmap.yaml:758:45 executing
"valkey/templates/scripts-configmap.yaml" at <4>: wrong type for value; expected string; got []interface {}
```

Phase: $.replica.preExecCmds[*] | Status: failed

Changed overrides (used together):
- `$.replica.preExecCmds = [null]`
Absent from overrides: $.replica.preExecCmds["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/be395840f38a1a431dfc/report.json>)

#### E601 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: valkey/templates/secret-svcbind.yaml:15:17 executing "valkey/templates/secret-svcbind.yaml" at <include "valkey.password"
.>: error calling include: template: no template "valkey.password" associated with template "gotpl"
```

Phase: $.serviceBindings.enabled | Status: failed

Changed overrides (used together):
- `$.serviceBindings.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0106/paths/eb773f8c0e00f3388cf0/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0106>)

### [bitnami/valkey-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey-cluster>)

Overview cell: 108

Status: failed | Attempts: 1547

Audit findings: 359. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.hostMode`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.externalAccess.service.disableLoadBalancerIP`: Undocumented values path
  (warning)
- 353 additional audit findings in JSON.

Configuration rejections: 0 excluded; 1 adjusted and tested; 1 Helm verification renders (separate from manifest-test attempts).

#### E007 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: valkey-cluster/templates/valkey-svc.yaml:9:20 executing "valkey-cluster/templates/valkey-svc.yaml" at <{{template
"common.names.fullname" .}}>: template "common.names.fullname" not defined
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/e2cac8a5225634937910/report.json>)

#### E068 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: valkey-cluster 3.0.25 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r51 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.volumePermissions.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/5356324f9a8a2798b69d/report.json>)

#### E069 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: valkey-cluster 3.0.25 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ges: - 00/bitnami/valkey-cluster:8.1.3-debian-12-r3 -
00/bitnami/os-shell:12-debian-12-r51 - 00/bitnami/redis-exporter:1.76.0-debian-12-r0 - 00/bitnami/os-shell:12-debian-12-r51 If you are sure
you want to proceed with non-standard containers, you can skip container image verification by setting the global parameter
'global.security.allowInsecureImages' to true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/fa90b40f46c6c70d8821/report.json>)

#### E070 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: valkey-cluster 3.0.25 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:8.1.3-debian-12-r3 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/valkey-cluster")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/3f7165f1837241716c3c/report.json>)

#### E081 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: valkey-cluster 3.0.25 / templates/NOTES.txt

```text
template: valkey-cluster/templates/NOTES.txt:76:125: executing "valkey-cluster/templates/NOTES.txt" at <eq .Values.notEmptyString "">: error
calling eq: incompatible types for comparison: []interface {} and string
```

Phase: $.notEmptyString | Status: failed

Changed overrides (used together):
- `$.notEmptyString = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/f013198a494d488a60a9/report.json>)

#### E471 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey-cluster/templates/valkey-statefulset.yaml: error converting YAML to JSON: yaml: line 180: did not
find expected '-' indicator
```

Phase: $.existingSecret | Status: failed

Changed overrides (used together):
- `$.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/bf7372b3862550c529f3/report.json>)

#### E472 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey-cluster/templates/valkey-statefulset.yaml: error converting YAML to JSON: yaml: line 203: found
unexpected end of stream
```

Phase: $.persistence.path | Status: failed

Changed overrides (used together):
- `$.persistence.path = "'" (was "/bitnami/valkey/data")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/909ebb7fe60c66c7c8df/report.json>)

#### E473 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey-cluster/templates/valkey-statefulset.yaml: error converting YAML to JSON: yaml: line 206: found
unexpected end of stream
```

Phase: $.valkey.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.valkey.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/ec5865e9f8ddc5678b7d/report.json>)

#### E474 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey-cluster/templates/valkey-statefulset.yaml: error converting YAML to JSON: yaml: line 39: did not
find expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/097f6358a00dddbcdd83/report.json>)

3 additional occurrences are retained in the JSON report and chart artifacts.

#### E475 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey-cluster/templates/valkey-statefulset.yaml: error converting YAML to JSON: yaml: line 63: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "8.1.3-debian-12-r3")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/8e79b7dd85a286cfaddb/report.json>)

#### E476 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on valkey-cluster/templates/valkey-svc.yaml: error converting YAML to JSON: yaml: line 23: found unexpected
end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0107/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0107>)

### [bitnami/vault](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/vault>)

Overview cell: 109

Status: failed | Attempts: 1280

Audit findings: 557. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.agent`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.csiProvider.agent.args`: Undocumented values path (warning)
- 551 additional audit findings in JSON.

Configuration rejections: 0 excluded; 18 adjusted and tested; 18 Helm verification renders (separate from manifest-test attempts).

#### E489 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on vault/templates/injector/deployment.yaml: error converting YAML to JSON: yaml: line 37: block sequence
entries are not allowed in this context
```

Phase: $.injector.image.pullSecrets[*] | Status: failed

Changed overrides (used together):
- `$.injector.image.pullSecrets = [[null]]`
Absent from overrides: $.injector.image.pullSecrets["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0108/paths/4fd5fd30473c3b74ae4c/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0108/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E490 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on vault/templates/injector/deployment.yaml: error converting YAML to JSON: yaml: line 62: could not find
expected ':'
```

Phase: $.injector.image.repository | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.injector.image.repository = "\r" (was "bitnami/vault-k8s")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0108/paths/6320d7d6a74bb0ca3687/report.json>)

#### E491 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on vault/templates/injector/hpa.yaml: error converting YAML to JSON: yaml: line 18: block sequence entries
are not allowed in this context
```

Phase: $.injector.autoscaling | Status: failed

Changed overrides (used together):
- `$.injector.autoscaling.enabled = true (was false)`
- `$.injector.autoscaling.maxReplicas = "-" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0108/paths/4fcdc35d3efabc78f19e/report.json>)

#### E492 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on vault/templates/server/statefulset.yaml: error converting YAML to JSON: yaml: line 63: mapping values
are not allowed in this context
```

Phase: $.server.image.tag | Status: failed

Changed overrides (used together):
- `$.server.image.tag = "" (was "1.20.2-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0108/paths/80b6cb2f8dcf3d2dcb4b/report.json>)

#### E493 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on vault/templates/server/statefulset.yaml: error converting YAML to JSON: yaml: line 65: could not find
expected ':'
```

Phase: $.server.image.registry | Status: failed

Changed overrides (used together):
- `$.global.security.allowInsecureImages = true (was false)`
- `$.server.image.registry = "\r" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0108/paths/e2f467218b148f0e690b/report.json>)

#### E602 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: vault/templates/server/statefulset.yaml:7:15 executing "vault/templates/server/statefulset.yaml" at <include
"common.capabilities.statefulset.apiVersion" .>: error calling include: template: no template "common.capabilities.statefulset.apiVersion"
associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0108/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0108>)

### [bitnami/victoriametrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/victoriametrics>)

Overview cell: 110

Status: failed | Attempts: 298

Audit findings: 1110. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.defaultInitContainers.volumePermissions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.defaultInitContainers.volumePermissions.containerSecurityContext`: Undocumented values
  path (warning)
- 1104 additional audit findings in JSON.

#### E494 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on victoriametrics/templates/vmstorage/statefulset.yaml: error converting YAML to JSON: yaml: line 132: did
not find expected '-' indicator
```

Phase: $.vmstorage.persistence.dataSource | Status: failed

Changed overrides (used together):
- `$.vmstorage.persistence.dataSource[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0109/paths/5036f40926f21df80c6f/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0109>)

### [bitnami/whereabouts](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/whereabouts>)

Overview cell: 111

Status: failed | Attempts: 387

Audit findings: 130. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.CNIMountPath`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 124 additional audit findings in JSON.

Configuration rejections: 0 excluded; 11 adjusted and tested; 11 Helm verification renders (separate from manifest-test attempts).

#### E495 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on whereabouts/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 134: found unexpected
end of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0110/paths/57504c968732d9714f10/report.json>)

#### E496 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on whereabouts/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0110/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0110/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E497 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on whereabouts/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 56: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "0.9.2-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0110/paths/8e79b7dd85a286cfaddb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0110>)

### [bitnami/wildfly](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wildfly>)

Overview cell: 112

Status: failed | Attempts: 845

Audit findings: 233. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 227 additional audit findings in JSON.

#### E008 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

```text
[HH1001] Error: wildfly/templates/svc.yaml:9:20 executing "wildfly/templates/svc.yaml" at <{{template "common.names.fullname" .}}>: template
"common.names.fullname" not defined
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/e2cac8a5225634937910/report.json>)

#### E073 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: wildfly 25.0.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... iners is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.volumePermissions.image.registry | Status: failed

Changed overrides (used together):
- `$.volumePermissions.image.registry = "00" (was "docker.io")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/5356324f9a8a2798b69d/report.json>)

#### E074 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: wildfly 25.0.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... y and performance, broken chart features, and missing environment variables. Unrecognized
images: - 00/bitnami/wildfly:37.0.0-debian-12-r0 - 00/bitnami/os-shell:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "00" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/fa90b40f46c6c70d8821/report.json>)

#### E075 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: wildfly 25.0.1 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ontainers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:37.0.0-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/wildfly")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/3f7165f1837241716c3c/report.json>)

#### E498 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on wildfly/templates/deployment.yaml: error converting YAML to JSON: yaml: line 183: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/bc81b51736a9cdc4eda3/report.json>)

#### E499 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on wildfly/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E500 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on wildfly/templates/deployment.yaml: error converting YAML to JSON: yaml: line 68: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "37.0.0-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/8e79b7dd85a286cfaddb/report.json>)

#### E501 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on wildfly/templates/svc.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/6e931799d09f8182f34b/report.json>)

#### E502 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on wildfly/templates/svc.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end of stream
```

Phase: $.service.nodePorts.http | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/c91d7fbded4704da55d3/report.json>)

Phase: $.service.nodePorts | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.http = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0111/paths/afbac7d295ec4c0a2908/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0111>)

### [bitnami/wordpress](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wordpress>)

Overview cell: 113

Status: failed | Attempts: 278

Audit findings: 406. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowEmptyPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.allowOverrideNone`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apacheConfiguration`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- 400 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E021 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
execution error at (mariadb/templates/NOTES.txt:74:4): VALUES VALIDATION: mariadb: architecture Invalid architecture selected. Valid values
are "standalone" and "replication". Please set a valid architecture (--set architecture="xxxx")
```

Phase: $.mariadb.architecture | Status: failed

Changed overrides (used together):
- `$.mariadb.architecture = "" (was "standalone")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0112/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E023 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: mariadb 22.0.0 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... d containers is likely to cause degraded security and performance, broken chart features,
and missing environment variables. Unrecognized images: - docker.io/00:12-debian-12-r50 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.mariadb.volumePermissions.image.repository | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.repository = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0112/paths/e9b2bd06f74a17778834/report.json>)

#### E503 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on wordpress/templates/deployment.yaml: error converting YAML to JSON: yaml: line 257: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0112/paths/bc81b51736a9cdc4eda3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0112>)

### [bitnami/zipkin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zipkin>)

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

#### E511 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] invalid rendered YAML: more indented follow up line than first in a block scalar in "<unicode string>", line 474, column 15: set -o
errexit ^ (line: 474)
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0113/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0113>)

### [bitnami/zookeeper](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zookeeper>)

Overview cell: 115

Status: failed | Attempts: 751

Audit findings: 319. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.clientPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.clientUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.enabled`: Undocumented values path (warning)
- 313 additional audit findings in JSON.

Configuration rejections: 0 excluded; 12 adjusted and tested; 12 Helm verification renders (separate from manifest-test attempts).

#### E504 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on zookeeper/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 191: found unexpected
end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0114/paths/bc81b51736a9cdc4eda3/report.json>)

#### E505 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on zookeeper/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 200: found unexpected
end of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0114/paths/57504c968732d9714f10/report.json>)

#### E506 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on zookeeper/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 202: found unexpected
end of stream
```

Phase: $.persistence.dataLogDir | Status: failed

Changed overrides (used together):
- `$.persistence.dataLogDir.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0114/paths/cd88da17db57f0ffc104/report.json>)

#### E507 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on zookeeper/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 212: found unexpected
end of stream
```

Phase: $.dataLogDir | Status: failed

Changed overrides (used together):
- `$.dataLogDir = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0114/paths/fd389ff34ba607267419/report.json>)

#### E508 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on zookeeper/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 39: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0114/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0114/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E509 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on zookeeper/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 64: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "3.9.3-debian-12-r21")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0114/paths/8e79b7dd85a286cfaddb/report.json>)

#### E510 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on zookeeper/templates/svc.yaml: error converting YAML to JSON: yaml: line 24: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789870241/0114/paths/6e931799d09f8182f34b/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789870241/0114>)

## Appendix: finding codes

HH codes identify finding categories. E001-style numbers identify individual diagnostics within this report.
Severities below are defaults; configured overrides are shown with the findings above.

### HH1001 - Unclassified template failure

Default severity: **error** | Category: unclassified | Evidence type: diagnostic

Helm template exits unsuccessfully without a recognized diagnostic.

Suggested action: Inspect the Helm diagnostic and reproducer; the exit alone does not establish a chart defect.

### HH1011 - Rendered output cannot be encoded as JSON

Default severity: **error** | Category: unclassified | Evidence type: diagnostic

Manifest processing reports a JSON representation failure.

Suggested action: Inspect YAML tags and parser support to determine whether the failure comes from an unsupported value or a chart defect.

### HH1101 - Invalid YAML in rendered output

Default severity: **error** | Category: manifest | Evidence type: violation

The YAML parser rejects rendered output, or Helm reports a YAML parse error.

Suggested action: Inspect the failing YAML and template interpolation, including quoting and indentation.

### HH1102 - Manifest document is not an object

Default severity: **error** | Category: manifest | Evidence type: violation

A nonempty rendered document is a scalar or sequence instead of a mapping.

Suggested action: Emit a resource mapping or remove the stray document.

### HH1103 - Missing resource API version or kind

Default severity: **error** | Category: manifest | Evidence type: violation

A resource has no nonempty string apiVersion or kind.

Suggested action: Supply both resource identifiers in every branch that emits a resource.

### HH1105 - Missing resource name

Default severity: **error** | Category: manifest | Evidence type: violation

The resource fails the tool's nonempty metadata.name contract.

Suggested action: Provide a name in each resource branch; ignore this check if your workflow intentionally uses generated names.

### HH1106 - Duplicate resource identity

Default severity: **error** | Category: manifest | Evidence type: violation

Two resources in the checked bundle share apiVersion, kind, namespace and name.

Suggested action: Give the resources distinct names or make their activation conditions exclusive.

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

### HH3002 - Incompatible value type in template

Default severity: **error** | Category: template | Evidence type: violation

Helm reports a wrong value type, a field unavailable on a type, or an unsupported range operand.

Suggested action: Align the template operation with the accepted input types, or narrow the schema.

### HH3003 - Undefined named template

Default severity: **error** | Category: template | Evidence type: violation

Helm reports that a called named template is not defined.

Suggested action: Check the helper name, its definition and dependency availability.
