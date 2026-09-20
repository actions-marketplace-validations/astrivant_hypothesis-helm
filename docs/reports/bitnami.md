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
findings means none in the completed sample, not exhaustive coverage. Testing time excludes dependency preparation.

## Scan summary

Git comparison unavailable; no charts skipped using previous test results.

Directory: /Users/emmadoyle/projects/personal/hypothesis-helm/third_party/bitnami-charts
Started (Unix epoch): 1789863671
Started (UTC): 2026-09-20T00:21:11.000+00:00
Finished (UTC): 2026-09-20T01:12:18.252+00:00 (estimated from recorded timing)
Run fingerprint (SHA-256): `251863348dfd60092c4726cde7b96b1d61e7fa756650e2ddf3feaaedd251ea4f`
Elapsed (wall clock): 3067.25 seconds
Chart testing: 2974.70 seconds
Dependency preparation: 90.30 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: interrupted
Discovery complete: True
Unstarted charts: 105

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

8 failed; 1 time-limit; 1 interrupted; 105 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: [HH2006](#hh2006---opaque-object-schema)

## Errors

25 distinct diagnostics across 35 occurrences; 10 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### [bitnami/airflow](<https://github.com/bitnami/charts/tree/main/bitnami/airflow>)

Overview cell: 01

Status: failed | Attempts: 113

Audit findings: 1190. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.fernetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in JSON.

#### E022 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on airflow/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal object into Go struct field .metadata.annotations.x_[[ of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = false`
- `$.redis.sentinel.service.headless.annotations["x_[["][""] = []`
- `$.redis.sentinel.service.headless.extraPorts = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0000/paths/afbbf9ab6c6be5d414aa>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0000>)

### [bitnami/apache](<https://github.com/bitnami/charts/tree/main/bitnami/apache>)

Overview cell: 02

Status: failed | Attempts: 601

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

#### E003 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 179: found unexpected end of
stream
```

Phase: $.htdocsConfigMap | Status: failed

Changed overrides (used together):
- `$.htdocsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0001/paths/a84b1abe3a11000d364a>)

#### E004 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0001/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0001/paths/097f6358a00dddbcdd83>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E005 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0001/paths/8e79b7dd85a286cfaddb>)

#### E006 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0001/paths/6e931799d09f8182f34b>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0001>)

### [bitnami/apisix](<https://github.com/bitnami/charts/tree/main/bitnami/apisix>)

Overview cell: 03

Status: failed | Attempts: 130

Audit findings: 344. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.controlPlane.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controlPlane.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.vpa`: Missing values description (info)
- 338 additional audit findings in JSON.

#### E007 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0002/paths/0384c509a56911993ff8>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0002>)

### [bitnami/appsmith](<https://github.com/bitnami/charts/tree/main/bitnami/appsmith>)

Overview cell: 04

Status: failed | Attempts: 114

Audit findings: 543. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.automountServiceAccountToken`: Undocumented values path (warning)
- 537 additional audit findings in JSON.

#### E002 ([HH1011](#hh1011---rendered-output-cannot-be-encoded-as-json))

**Rendered output cannot be encoded as JSON** (unclassified / diagnostic). Severity: **error**. Inspect YAML tags and parser support to
determine whether the failure comes from an unsupported value or a chart defect.

```text
[HH1011] The test tool could not convert a YAML-tagged value to JSON. See this chart's reproducing values. This diagnostic alone does not
establish a chart defect.
```

Phase: $.mongodb.persistence | Status: failed

Changed overrides (used together):
- `$.mongodb.persistence.subPath = "!rj'Q"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0003/paths/41d6ae6f8aea08087045>)

#### E023 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on appsmith/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations.x_[[ of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = false`
- `$.redis.sentinel.service.headless.annotations["x_[["] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0003/paths/afbbf9ab6c6be5d414aa>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0003>)

### [bitnami/argo-cd](<https://github.com/bitnami/charts/tree/main/bitnami/argo-cd>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0004>)

### [bitnami/argo-workflows](<https://github.com/bitnami/charts/tree/main/bitnami/argo-workflows>)

Overview cell: 06

Status: failed | Attempts: 131

Audit findings: 452. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.automountServiceAccountToken`: Undocumented values path (warning)
- 446 additional audit findings in JSON.

#### E001 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0005/paths/1c25c32c569a13118399>)

#### E008 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on argo-workflows/templates/controller/clusterrolebinding.yaml: error converting YAML to JSON: yaml: line
24: did not find expected alphabetic or numeric character
```

Phase: $.controller.workflowNamespaces[*] | Status: failed

Changed overrides (used together):
- `$.controller.workflowNamespaces = ["\n&"]`
Absent from overrides: $.controller.workflowNamespaces["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0005/paths/d21976126c873fdee7bc>)

#### E024 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on argo-workflows/templates/controller/workflow-serviceaccount.yaml: error unmarshaling JSON: while
decoding JSON: json: cannot unmarshal object into Go struct field .metadata.annotations. of type string
```

Phase: $.workflows.serviceAccount | Status: failed

Changed overrides (used together):
- `$.workflows.serviceAccount.annotations["selection-limit"] = null`
- `$.workflows.serviceAccount.annotations[""] = {}`
- `$.workflows.serviceAccount.annotations.X["a!a'aVa"] = [[[], {}, true]]`
- `$.workflows.serviceAccount.annotations["UP/xa2"] = []`
- `$.workflows.serviceAccount.name = "audit"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0005/paths/c246ccf3c22f11e34d43>)

#### E025 ([HH3001](#hh3001---template-accesses-a-missing-object))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0005/paths/cd1b3bd14efaf6a86788>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0005>)

### [bitnami/aspnet-core](<https://github.com/bitnami/charts/tree/main/bitnami/aspnet-core>)

Overview cell: 07

Status: failed | Attempts: 851

Audit findings: 224. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.existingClaim`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone.depth`: Undocumented values path (warning)
- 218 additional audit findings in JSON.

Configuration rejections: 0 excluded; 20 adjusted and tested; 20 Helm verification renders (separate from manifest-test attempts).

#### E009 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 29: did not find
expected ',' or ']'
```

Phase: $.appFromExternalRepo.clone.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.clone.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0006/paths/5a7bb70f23ca77d7dde5>)

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0006/paths/a4a0ea6ab697189bb963>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E010 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0006/paths/8cfc2368ac94f1308380>)

#### E011 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 66: mapping values are
not allowed in this context
```

Phase: $.appFromExternalRepo.publish.image.tag | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.tag = "" (was "9.0.304-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0006/paths/6f16a3fce30f040bbbba>)

#### E012 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 76: could not find
expected ':'
```

Phase: $.appFromExternalRepo.publish.extraFlags | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.extraFlags = [{"\r": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0006/paths/d6d30e52dda638aa651d>)

Phase: $.appFromExternalRepo.publish.subFolder | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.subFolder = "\n0" (was "aspnetcore/performance/caching/output/samples/8.x/")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0006/paths/d6eb74839ecc6561f2a6>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E013 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 83: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "9.0.8-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0006/paths/8e79b7dd85a286cfaddb>)

#### E014 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/svc.yaml: error converting YAML to JSON: yaml: line 22: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0006/paths/6e931799d09f8182f34b>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0006>)

### [bitnami/cadvisor](<https://github.com/bitnami/charts/tree/main/bitnami/cadvisor>)

Overview cell: 08

Status: failed | Attempts: 678

Audit findings: 192. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.clusterDomain`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 186 additional audit findings in JSON.

Configuration rejections: 0 excluded; 21 adjusted and tested; 21 Helm verification renders (separate from manifest-test attempts).

#### E015 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 144: found unexpected end
of stream
```

Phase: $.schedulerName | Status: failed

Changed overrides (used together):
- `$.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0007/paths/57504c968732d9714f10>)

#### E016 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 35: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0007/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0007/paths/097f6358a00dddbcdd83>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E017 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0007/paths/8e79b7dd85a286cfaddb>)

#### E018 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/service.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of
stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "ClusterIP")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0007/paths/6e931799d09f8182f34b>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0007>)

### [bitnami/cassandra](<https://github.com/bitnami/charts/tree/main/bitnami/cassandra>)

Overview cell: 09

Status: failed | Attempts: 449

Audit findings: 309. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.clientEncryption`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.datacenter`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.enableUDF`: Undocumented values path (warning)
- 303 additional audit findings in JSON.

Configuration rejections: 0 excluded; 21 adjusted and tested; 21 Helm verification renders (separate from manifest-test attempts).

#### E019 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 204: found unexpected
end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0008/paths/bc81b51736a9cdc4eda3>)

#### E020 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 31: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0008/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0008/paths/097f6358a00dddbcdd83>)

#### E021 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 68: mapping values are
not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "5.0.5-debian-12-r7")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789863671/0008/paths/8e79b7dd85a286cfaddb>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0008>)

### [bitnami/cert-manager](<https://github.com/bitnami/charts/tree/main/bitnami/cert-manager>)

Overview cell: 10

Status: interrupted | Attempts: 1

Audit findings: 404. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.containerSecurityContext`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cainjector.containerSecurityContext.allowPrivilegeEscalation`: Undocumented values path
  (warning)
- 398 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789863671/0009>)

### [bitnami/chainloop](<https://github.com/bitnami/charts/tree/main/bitnami/chainloop>)

Overview cell: 11

Status: pending | Attempts: N/A

### [bitnami/cilium](<https://github.com/bitnami/charts/tree/main/bitnami/cilium>)

Overview cell: 12

Status: pending | Attempts: N/A

### [bitnami/clickhouse](<https://github.com/bitnami/charts/tree/main/bitnami/clickhouse>)

Overview cell: 13

Status: pending | Attempts: N/A

### [bitnami/clickhouse-operator](<https://github.com/bitnami/charts/tree/main/bitnami/clickhouse-operator>)

Overview cell: 14

Status: pending | Attempts: N/A

### [bitnami/cloudnative-pg](<https://github.com/bitnami/charts/tree/main/bitnami/cloudnative-pg>)

Overview cell: 15

Status: pending | Attempts: N/A

### [bitnami/common](<https://github.com/bitnami/charts/tree/main/bitnami/common>)

Overview cell: 16

Status: pending | Attempts: N/A

### [bitnami/concourse](<https://github.com/bitnami/charts/tree/main/bitnami/concourse>)

Overview cell: 17

Status: pending | Attempts: N/A

### [bitnami/consul](<https://github.com/bitnami/charts/tree/main/bitnami/consul>)

Overview cell: 18

Status: pending | Attempts: N/A

### [bitnami/contour](<https://github.com/bitnami/charts/tree/main/bitnami/contour>)

Overview cell: 19

Status: pending | Attempts: N/A

### [bitnami/deepspeed](<https://github.com/bitnami/charts/tree/main/bitnami/deepspeed>)

Overview cell: 20

Status: pending | Attempts: N/A

### [bitnami/discourse](<https://github.com/bitnami/charts/tree/main/bitnami/discourse>)

Overview cell: 21

Status: pending | Attempts: N/A

### [bitnami/dremio](<https://github.com/bitnami/charts/tree/main/bitnami/dremio>)

Overview cell: 22

Status: pending | Attempts: N/A

### [bitnami/drupal](<https://github.com/bitnami/charts/tree/main/bitnami/drupal>)

Overview cell: 23

Status: pending | Attempts: N/A

### [bitnami/ejbca](<https://github.com/bitnami/charts/tree/main/bitnami/ejbca>)

Overview cell: 24

Status: pending | Attempts: N/A

### [bitnami/elasticsearch](<https://github.com/bitnami/charts/tree/main/bitnami/elasticsearch>)

Overview cell: 25

Status: pending | Attempts: N/A

### [bitnami/envoy-gateway](<https://github.com/bitnami/charts/tree/main/bitnami/envoy-gateway>)

Overview cell: 26

Status: pending | Attempts: N/A

### [bitnami/etcd](<https://github.com/bitnami/charts/tree/main/bitnami/etcd>)

Overview cell: 27

Status: pending | Attempts: N/A

### [bitnami/external-dns](<https://github.com/bitnami/charts/tree/main/bitnami/external-dns>)

Overview cell: 28

Status: pending | Attempts: N/A

### [bitnami/flink](<https://github.com/bitnami/charts/tree/main/bitnami/flink>)

Overview cell: 29

Status: pending | Attempts: N/A

### [bitnami/fluent-bit](<https://github.com/bitnami/charts/tree/main/bitnami/fluent-bit>)

Overview cell: 30

Status: pending | Attempts: N/A

### [bitnami/fluentd](<https://github.com/bitnami/charts/tree/main/bitnami/fluentd>)

Overview cell: 31

Status: pending | Attempts: N/A

### [bitnami/flux](<https://github.com/bitnami/charts/tree/main/bitnami/flux>)

Overview cell: 32

Status: pending | Attempts: N/A

### [bitnami/ghost](<https://github.com/bitnami/charts/tree/main/bitnami/ghost>)

Overview cell: 33

Status: pending | Attempts: N/A

### [bitnami/gitea](<https://github.com/bitnami/charts/tree/main/bitnami/gitea>)

Overview cell: 34

Status: pending | Attempts: N/A

### [bitnami/gitlab-runner](<https://github.com/bitnami/charts/tree/main/bitnami/gitlab-runner>)

Overview cell: 35

Status: pending | Attempts: N/A

### [bitnami/grafana](<https://github.com/bitnami/charts/tree/main/bitnami/grafana>)

Overview cell: 36

Status: pending | Attempts: N/A

### [bitnami/grafana-alloy](<https://github.com/bitnami/charts/tree/main/bitnami/grafana-alloy>)

Overview cell: 37

Status: pending | Attempts: N/A

### [bitnami/grafana-k6-operator](<https://github.com/bitnami/charts/tree/main/bitnami/grafana-k6-operator>)

Overview cell: 38

Status: pending | Attempts: N/A

### [bitnami/grafana-loki](<https://github.com/bitnami/charts/tree/main/bitnami/grafana-loki>)

Overview cell: 39

Status: pending | Attempts: N/A

### [bitnami/grafana-mimir](<https://github.com/bitnami/charts/tree/main/bitnami/grafana-mimir>)

Overview cell: 40

Status: pending | Attempts: N/A

### [bitnami/grafana-operator](<https://github.com/bitnami/charts/tree/main/bitnami/grafana-operator>)

Overview cell: 41

Status: pending | Attempts: N/A

### [bitnami/grafana-tempo](<https://github.com/bitnami/charts/tree/main/bitnami/grafana-tempo>)

Overview cell: 42

Status: pending | Attempts: N/A

### [bitnami/haproxy](<https://github.com/bitnami/charts/tree/main/bitnami/haproxy>)

Overview cell: 43

Status: pending | Attempts: N/A

### [bitnami/harbor](<https://github.com/bitnami/charts/tree/main/bitnami/harbor>)

Overview cell: 44

Status: pending | Attempts: N/A

### [bitnami/influxdb](<https://github.com/bitnami/charts/tree/main/bitnami/influxdb>)

Overview cell: 45

Status: pending | Attempts: N/A

### [bitnami/jaeger](<https://github.com/bitnami/charts/tree/main/bitnami/jaeger>)

Overview cell: 46

Status: pending | Attempts: N/A

### [bitnami/janusgraph](<https://github.com/bitnami/charts/tree/main/bitnami/janusgraph>)

Overview cell: 47

Status: pending | Attempts: N/A

### [bitnami/jenkins](<https://github.com/bitnami/charts/tree/main/bitnami/jenkins>)

Overview cell: 48

Status: pending | Attempts: N/A

### [bitnami/jupyterhub](<https://github.com/bitnami/charts/tree/main/bitnami/jupyterhub>)

Overview cell: 49

Status: pending | Attempts: N/A

### [bitnami/kafka](<https://github.com/bitnami/charts/tree/main/bitnami/kafka>)

Overview cell: 50

Status: pending | Attempts: N/A

### [bitnami/keycloak](<https://github.com/bitnami/charts/tree/main/bitnami/keycloak>)

Overview cell: 51

Status: pending | Attempts: N/A

### [bitnami/keydb](<https://github.com/bitnami/charts/tree/main/bitnami/keydb>)

Overview cell: 52

Status: pending | Attempts: N/A

### [bitnami/kibana](<https://github.com/bitnami/charts/tree/main/bitnami/kibana>)

Overview cell: 53

Status: pending | Attempts: N/A

### [bitnami/kong](<https://github.com/bitnami/charts/tree/main/bitnami/kong>)

Overview cell: 54

Status: pending | Attempts: N/A

### [bitnami/kube-arangodb](<https://github.com/bitnami/charts/tree/main/bitnami/kube-arangodb>)

Overview cell: 55

Status: pending | Attempts: N/A

### [bitnami/kube-prometheus](<https://github.com/bitnami/charts/tree/main/bitnami/kube-prometheus>)

Overview cell: 56

Status: pending | Attempts: N/A

### [bitnami/kube-prometheus/charts/kube-prometheus-crds](<https://github.com/bitnami/charts/tree/main/bitnami/kube-prometheus/charts/kube-prometheus-crds>)

Overview cell: 57

Status: pending | Attempts: N/A

### [bitnami/kube-state-metrics](<https://github.com/bitnami/charts/tree/main/bitnami/kube-state-metrics>)

Overview cell: 58

Status: pending | Attempts: N/A

### [bitnami/kuberay](<https://github.com/bitnami/charts/tree/main/bitnami/kuberay>)

Overview cell: 59

Status: pending | Attempts: N/A

### [bitnami/kubernetes-event-exporter](<https://github.com/bitnami/charts/tree/main/bitnami/kubernetes-event-exporter>)

Overview cell: 60

Status: pending | Attempts: N/A

### [bitnami/logstash](<https://github.com/bitnami/charts/tree/main/bitnami/logstash>)

Overview cell: 61

Status: pending | Attempts: N/A

### [bitnami/mariadb](<https://github.com/bitnami/charts/tree/main/bitnami/mariadb>)

Overview cell: 62

Status: pending | Attempts: N/A

### [bitnami/mariadb-galera](<https://github.com/bitnami/charts/tree/main/bitnami/mariadb-galera>)

Overview cell: 63

Status: pending | Attempts: N/A

### [bitnami/mastodon](<https://github.com/bitnami/charts/tree/main/bitnami/mastodon>)

Overview cell: 64

Status: pending | Attempts: N/A

### [bitnami/matomo](<https://github.com/bitnami/charts/tree/main/bitnami/matomo>)

Overview cell: 65

Status: pending | Attempts: N/A

### [bitnami/memcached](<https://github.com/bitnami/charts/tree/main/bitnami/memcached>)

Overview cell: 66

Status: pending | Attempts: N/A

### [bitnami/metallb](<https://github.com/bitnami/charts/tree/main/bitnami/metallb>)

Overview cell: 67

Status: pending | Attempts: N/A

### [bitnami/metrics-server](<https://github.com/bitnami/charts/tree/main/bitnami/metrics-server>)

Overview cell: 68

Status: pending | Attempts: N/A

### [bitnami/milvus](<https://github.com/bitnami/charts/tree/main/bitnami/milvus>)

Overview cell: 69

Status: pending | Attempts: N/A

### [bitnami/mlflow](<https://github.com/bitnami/charts/tree/main/bitnami/mlflow>)

Overview cell: 70

Status: pending | Attempts: N/A

### [bitnami/mongodb](<https://github.com/bitnami/charts/tree/main/bitnami/mongodb>)

Overview cell: 71

Status: pending | Attempts: N/A

### [bitnami/mongodb-sharded](<https://github.com/bitnami/charts/tree/main/bitnami/mongodb-sharded>)

Overview cell: 72

Status: pending | Attempts: N/A

### [bitnami/moodle](<https://github.com/bitnami/charts/tree/main/bitnami/moodle>)

Overview cell: 73

Status: pending | Attempts: N/A

### [bitnami/multus-cni](<https://github.com/bitnami/charts/tree/main/bitnami/multus-cni>)

Overview cell: 74

Status: pending | Attempts: N/A

### [bitnami/mysql](<https://github.com/bitnami/charts/tree/main/bitnami/mysql>)

Overview cell: 75

Status: pending | Attempts: N/A

### [bitnami/nats](<https://github.com/bitnami/charts/tree/main/bitnami/nats>)

Overview cell: 76

Status: pending | Attempts: N/A

### [bitnami/neo4j](<https://github.com/bitnami/charts/tree/main/bitnami/neo4j>)

Overview cell: 77

Status: pending | Attempts: N/A

### [bitnami/nessie](<https://github.com/bitnami/charts/tree/main/bitnami/nessie>)

Overview cell: 78

Status: pending | Attempts: N/A

### [bitnami/nginx](<https://github.com/bitnami/charts/tree/main/bitnami/nginx>)

Overview cell: 79

Status: pending | Attempts: N/A

### [bitnami/node-exporter](<https://github.com/bitnami/charts/tree/main/bitnami/node-exporter>)

Overview cell: 80

Status: pending | Attempts: N/A

### [bitnami/oauth2-proxy](<https://github.com/bitnami/charts/tree/main/bitnami/oauth2-proxy>)

Overview cell: 81

Status: pending | Attempts: N/A

### [bitnami/odoo](<https://github.com/bitnami/charts/tree/main/bitnami/odoo>)

Overview cell: 82

Status: pending | Attempts: N/A

### [bitnami/opensearch](<https://github.com/bitnami/charts/tree/main/bitnami/opensearch>)

Overview cell: 83

Status: pending | Attempts: N/A

### [bitnami/parse](<https://github.com/bitnami/charts/tree/main/bitnami/parse>)

Overview cell: 84

Status: pending | Attempts: N/A

### [bitnami/phpmyadmin](<https://github.com/bitnami/charts/tree/main/bitnami/phpmyadmin>)

Overview cell: 85

Status: pending | Attempts: N/A

### [bitnami/pinniped](<https://github.com/bitnami/charts/tree/main/bitnami/pinniped>)

Overview cell: 86

Status: pending | Attempts: N/A

### [bitnami/postgresql](<https://github.com/bitnami/charts/tree/main/bitnami/postgresql>)

Overview cell: 87

Status: pending | Attempts: N/A

### [bitnami/postgresql-ha](<https://github.com/bitnami/charts/tree/main/bitnami/postgresql-ha>)

Overview cell: 88

Status: pending | Attempts: N/A

### [bitnami/prometheus](<https://github.com/bitnami/charts/tree/main/bitnami/prometheus>)

Overview cell: 89

Status: pending | Attempts: N/A

### [bitnami/pytorch](<https://github.com/bitnami/charts/tree/main/bitnami/pytorch>)

Overview cell: 90

Status: pending | Attempts: N/A

### [bitnami/rabbitmq](<https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq>)

Overview cell: 91

Status: pending | Attempts: N/A

### [bitnami/rabbitmq-cluster-operator](<https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq-cluster-operator>)

Overview cell: 92

Status: pending | Attempts: N/A

### [bitnami/redis](<https://github.com/bitnami/charts/tree/main/bitnami/redis>)

Overview cell: 93

Status: pending | Attempts: N/A

### [bitnami/redis-cluster](<https://github.com/bitnami/charts/tree/main/bitnami/redis-cluster>)

Overview cell: 94

Status: pending | Attempts: N/A

### [bitnami/redmine](<https://github.com/bitnami/charts/tree/main/bitnami/redmine>)

Overview cell: 95

Status: pending | Attempts: N/A

### [bitnami/schema-registry](<https://github.com/bitnami/charts/tree/main/bitnami/schema-registry>)

Overview cell: 96

Status: pending | Attempts: N/A

### [bitnami/scylladb](<https://github.com/bitnami/charts/tree/main/bitnami/scylladb>)

Overview cell: 97

Status: pending | Attempts: N/A

### [bitnami/sealed-secrets](<https://github.com/bitnami/charts/tree/main/bitnami/sealed-secrets>)

Overview cell: 98

Status: pending | Attempts: N/A

### [bitnami/seaweedfs](<https://github.com/bitnami/charts/tree/main/bitnami/seaweedfs>)

Overview cell: 99

Status: pending | Attempts: N/A

### [bitnami/solr](<https://github.com/bitnami/charts/tree/main/bitnami/solr>)

Overview cell: 100

Status: pending | Attempts: N/A

### [bitnami/sonarqube](<https://github.com/bitnami/charts/tree/main/bitnami/sonarqube>)

Overview cell: 101

Status: pending | Attempts: N/A

### [bitnami/spark](<https://github.com/bitnami/charts/tree/main/bitnami/spark>)

Overview cell: 102

Status: pending | Attempts: N/A

### [bitnami/superset](<https://github.com/bitnami/charts/tree/main/bitnami/superset>)

Overview cell: 103

Status: pending | Attempts: N/A

### [bitnami/tensorflow-resnet](<https://github.com/bitnami/charts/tree/main/bitnami/tensorflow-resnet>)

Overview cell: 104

Status: pending | Attempts: N/A

### [bitnami/thanos](<https://github.com/bitnami/charts/tree/main/bitnami/thanos>)

Overview cell: 105

Status: pending | Attempts: N/A

### [bitnami/tomcat](<https://github.com/bitnami/charts/tree/main/bitnami/tomcat>)

Overview cell: 106

Status: pending | Attempts: N/A

### [bitnami/valkey](<https://github.com/bitnami/charts/tree/main/bitnami/valkey>)

Overview cell: 107

Status: pending | Attempts: N/A

### [bitnami/valkey-cluster](<https://github.com/bitnami/charts/tree/main/bitnami/valkey-cluster>)

Overview cell: 108

Status: pending | Attempts: N/A

### [bitnami/vault](<https://github.com/bitnami/charts/tree/main/bitnami/vault>)

Overview cell: 109

Status: pending | Attempts: N/A

### [bitnami/victoriametrics](<https://github.com/bitnami/charts/tree/main/bitnami/victoriametrics>)

Overview cell: 110

Status: pending | Attempts: N/A

### [bitnami/whereabouts](<https://github.com/bitnami/charts/tree/main/bitnami/whereabouts>)

Overview cell: 111

Status: pending | Attempts: N/A

### [bitnami/wildfly](<https://github.com/bitnami/charts/tree/main/bitnami/wildfly>)

Overview cell: 112

Status: pending | Attempts: N/A

### [bitnami/wordpress](<https://github.com/bitnami/charts/tree/main/bitnami/wordpress>)

Overview cell: 113

Status: pending | Attempts: N/A

### [bitnami/zipkin](<https://github.com/bitnami/charts/tree/main/bitnami/zipkin>)

Overview cell: 114

Status: pending | Attempts: N/A

### [bitnami/zookeeper](<https://github.com/bitnami/charts/tree/main/bitnami/zookeeper>)

Overview cell: 115

Status: pending | Attempts: N/A

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
