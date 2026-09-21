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
Started (Unix epoch): 1789924640
Started (UTC): 2026-09-20T17:17:20.000+00:00
Finished (UTC): 2026-09-20T22:49:04.654+00:00
Run fingerprint (SHA-256): `515fd22d2ad755048f327a9c98b8234b57998c1124b58c46a76a9dc43c2ced0b`
Elapsed (wall clock): 19412.92 seconds
Chart testing: 18985.18 seconds
Dependency preparation: 420.21 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: interrupted
Discovery complete: True
Unstarted charts: 50

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

15 time-limit; 48 failed; 1 skipped-library; 1 interrupted; 50 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: [HH2006](#hh2006---opaque-object-schema)

## Errors

138 distinct diagnostics across 177 occurrences; 39 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### [bitnami/airflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/airflow>)

Overview cell: 01

Status: time-limit | Attempts: 94

Audit findings: 1190. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.fernetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0000>)

### [bitnami/apache](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apache>)

Overview cell: 02

Status: failed | Attempts: 212

Audit findings: 245. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 239 additional audit findings in JSON.

#### E020 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 179: found unexpected end of
stream
```

Phase: $.htdocsConfigMap | Status: failed

Changed overrides (used together):
- `$.htdocsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0001/paths/a84b1abe3a11000d364a/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0001>)

### [bitnami/apisix](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apisix>)

Overview cell: 03

Status: failed | Attempts: 126

Audit findings: 344. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.controlPlane.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controlPlane.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.vpa`: Missing values description (info)
- 338 additional audit findings in JSON.

#### E021 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0002/paths/0384c509a56911993ff8/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0002>)

### [bitnami/appsmith](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/appsmith>)

Overview cell: 04

Status: failed | Attempts: 107

Audit findings: 543. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.automountServiceAccountToken`: Undocumented values path (warning)
- 537 additional audit findings in JSON.

#### E019 ([HH1011](#hh1011---rendered-output-cannot-be-encoded-as-json))

**Rendered output cannot be encoded as JSON** (unclassified / diagnostic). Severity: **error**. Inspect YAML tags and parser support to
determine whether the failure comes from an unsupported value or a chart defect.

```text
[HH1011] The test tool could not convert a YAML-tagged value to JSON. See this chart's reproducing values. This diagnostic alone does not
establish a chart defect.
```

Phase: $.mongodb.persistence | Status: failed

Changed overrides (used together):
- `$.mongodb.persistence.subPath = "!rj'Q"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0003/paths/41d6ae6f8aea08087045/report.json>)

#### E124 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on appsmith/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0003/paths/afbbf9ab6c6be5d414aa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0003>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0004>)

### [bitnami/argo-workflows](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-workflows>)

Overview cell: 06

Status: failed | Attempts: 169

Audit findings: 452. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.automountServiceAccountToken`: Undocumented values path (warning)
- 446 additional audit findings in JSON.

#### E016 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0005/paths/1c25c32c569a13118399/report.json>)

#### E022 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on argo-workflows/templates/controller/clusterrolebinding.yaml: error converting YAML to JSON: yaml: line
23: did not find expected alphabetic or numeric character
```

Phase: $.controller.workflowNamespaces[*] | Status: failed

Changed overrides (used together):
- `$.controller.workflowNamespaces = ["&\n"]`
Absent from overrides: $.controller.workflowNamespaces["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0005/paths/d21976126c873fdee7bc/report.json>)

#### E125 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on argo-workflows/templates/controller/workflow-serviceaccount.yaml: error unmarshaling JSON: while
decoding JSON: json: cannot unmarshal object into Go struct field .metadata.annotations.\a4Za of type string
```

Phase: $.workflows.serviceAccount | Status: failed

Changed overrides (used together):
- `$.workflows.serviceAccount.annotations.max_dependency_depth = null`
- `$.workflows.serviceAccount.annotations.E = null`
- `$.workflows.serviceAccount.annotations["\n"] = null`
- `$.workflows.serviceAccount.annotations.a3Ma = "aaaaaa!a'aVa"`
- `$.workflows.serviceAccount.annotations["aa5'Zc~FDasi"] = [[]]`
- `$.workflows.serviceAccount.annotations["rRaU[aaz'apa"] = {}`
- 5 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0005/paths/c246ccf3c22f11e34d43/report.json>)

#### E131 ([HH3001](#hh3001---template-accesses-a-missing-object))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0005/paths/cd1b3bd14efaf6a86788/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0005>)

### [bitnami/aspnet-core](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/aspnet-core>)

Overview cell: 07

Status: failed | Attempts: 100

Audit findings: 224. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC.existingClaim`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExistingPVC`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appFromExternalRepo.clone.depth`: Undocumented values path (warning)
- 218 additional audit findings in JSON.

#### E023 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on aspnet-core/templates/deployment.yaml: error converting YAML to JSON: yaml: line 66: mapping values are
not allowed in this context
```

Phase: $.appFromExternalRepo.publish.image.tag | Status: failed

Changed overrides (used together):
- `$.appFromExternalRepo.publish.image.tag = "" (was "9.0.304-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0006/paths/6f16a3fce30f040bbbba/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0006>)

### [bitnami/cadvisor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cadvisor>)

Overview cell: 08

Status: failed | Attempts: 192

Audit findings: 192. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.clusterDomain`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- 186 additional audit findings in JSON.

#### E024 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cadvisor/templates/daemonset.yaml: error converting YAML to JSON: yaml: line 60: found character that
cannot start any token
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.digest = "N^"`
- `$.image.registry = ""`
- `$.image.repository = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0007/paths/8e79b7dd85a286cfaddb/observed-failure.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0007>)

### [bitnami/cassandra](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cassandra>)

Overview cell: 09

Status: failed | Attempts: 140

Audit findings: 309. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.clientEncryption`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.datacenter`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cluster.enableUDF`: Undocumented values path (warning)
- 303 additional audit findings in JSON.

#### E025 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 204: found unexpected
end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0008/paths/bc81b51736a9cdc4eda3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0008>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0009>)

### [bitnami/chainloop](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/chainloop>)

Overview cell: 11

Status: failed | Attempts: 169

Audit findings: 643. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 637 additional audit findings in JSON.

#### E026 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on chainloop/templates/controlplane/deployment.yaml: error converting YAML to JSON: yaml: line 166: found
unexpected end of stream
```

Phase: $.controlplane.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.controlplane.terminationGracePeriodSeconds = "'\n" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0010/paths/94d51abc8b5003c3268d/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0010>)

### [bitnami/cilium](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cilium>)

Overview cell: 12

Status: failed | Attempts: 263

Audit findings: 1163. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.agent.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling.vpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.autoscaling.vpa.annotations`: Undocumented values path (warning)
- 1157 additional audit findings in JSON.

#### E116 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0011/paths/0384c509a56911993ff8/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0011>)

### [bitnami/clickhouse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse>)

Overview cell: 13

Status: failed | Attempts: 285

Audit findings: 507. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 501 additional audit findings in JSON.

#### E028 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse/templates/keeper/statefulset.yaml: error converting YAML to JSON: yaml: line 167: found
unexpected end of stream
```

Phase: $.keeper.persistence.storageClass | Status: failed

Changed overrides (used together):
- `$.keeper.persistence.storageClass = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0012/paths/f422c3354af3ff9d853e/report.json>)

#### E029 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 177: found unexpected
end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0012/paths/bc81b51736a9cdc4eda3/report.json>)

#### E030 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse/templates/usersd-configmap.yaml: error converting YAML to JSON: yaml: line 14: did not find
expected key
```

Phase: $.usersdFiles | Status: failed

Changed overrides (used together):
- `$.usersdFiles[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0012/paths/638458d117473394e4a1/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0012>)

### [bitnami/clickhouse-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse-operator>)

Overview cell: 14

Status: failed | Attempts: 211

Audit findings: 276. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.username`: Undocumented values path (warning)
- 270 additional audit findings in JSON.

#### E027 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on clickhouse-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 68: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0013/paths/8e79b7dd85a286cfaddb/observed-failure.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0013>)

### [bitnami/cloudnative-pg](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cloudnative-pg>)

Overview cell: 15

Status: failed | Attempts: 876

Audit findings: 423. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.extraDeploy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.fullnameOverride`: Undocumented values path (warning)
- 417 additional audit findings in JSON.

Configuration rejections: 0 excluded; 27 adjusted and tested; 29 Helm verification renders (separate from manifest-test attempts).

#### E018 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/097f6358a00dddbcdd83/report.json>)

#### E031 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/deployment.yaml: error converting YAML to JSON: yaml: line 36: did not
find expected ',' or ']'
```

Phase: $.operator.postgresqlImage.pullSecrets | Status: failed

Changed overrides (used together):
- `$.operator.postgresqlImage.pullSecrets[""] = [null, []]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/3dcf6694cf8ac36c2d08/report.json>)

#### E032 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping
values are not allowed in this context
```

Phase: $.operator.image | Status: failed

Changed overrides (used together):
- `$.operator.image.tag = "" (was "1.27.0-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/b30a4eb2066aeb5f26ef/report.json>)

#### E033 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/deployment.yaml: error converting YAML to JSON: yaml: line 85: mapping
values are not allowed in this context
```

Phase: $.operator.postgresqlImage | Status: failed

Changed overrides (used together):
- `$.operator.postgresqlImage.tag = "" (was "17.6.0-debian-12-r4")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/b203e5d642851e3e429d/report.json>)

#### E034 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/b18ff9103e270cddd433/report.json>)

#### E035 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/mutatingwebhookconfiguration.yaml: error converting YAML to JSON:
yaml: line 24: block sequence entries are not allowed in this context
```

Phase: $.operator.webhook | Status: failed

Changed overrides (used together):
- `$.operator.webhook.mutating.failurePolicy = "-" (was "Fail")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/95c373847fa437516b05/report.json>)

#### E036 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/operator/validatingwebhookconfiguration.yaml: error converting YAML to JSON:
yaml: line 24: block sequence entries are not allowed in this context
```

Phase: $.operator.webhook.validating | Status: failed

Changed overrides (used together):
- `$.operator.webhook.validating.failurePolicy = "-" (was "Fail")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/8c104b857ff9d8b97822/report.json>)

#### E037 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on cloudnative-pg/templates/plugin-barman-cloud/deployment.yaml: error converting YAML to JSON: yaml: line
60: mapping values are not allowed in this context
```

Phase: $.pluginBarmanCloud.image.tag | Status: failed

Changed overrides (used together):
- `$.pluginBarmanCloud.image.tag = "" (was "0.6.0-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/53f5ef13d371739d3149/report.json>)

#### E038 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/ab50764a40516f71fbfc/report.json>)

Phase: $.commonAnnotations[*] | Status: failed

Changed overrides (used together):
- `$.commonAnnotations.__hypothesis_key__ = null`
Absent from overrides: $.commonAnnotations["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/5996bd948f4d6447c879/report.json>)

#### E117 ([HH1105](#hh1105---missing-resource-name))

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
- `$[6].data["tls.crt"]: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURqRENDQW5TZ0F3SUJBZ0lSQUtHdWt4MitLY0NSdmtDbFpyRjVyUTR3RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURpekNDQW5PZ0F3SUJBZ0lRVUJvdlBSeHVTUjFPNVoxOWZBZ3BSVEFOQmdrcWhraUc5dzBCQVFzRkF... [value shortened]`
- `$[6].data["tls.key"]: "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBc1ErTml6d245WlR5eURwRFk2WVJIMnFwdTAvWlFOY0gxMUVRMjBKblg... [value shortened] -> "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBbDRXNWw3V2V0dnFxcDBKRzdGb04rRkVzMk1vVnVnTExtbk13RWtOOEV... [value shortened]`
- `$[7].data["tls.crt"]: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURqRENDQW5TZ0F3SUJBZ0lSQU1nazN6WmpmUUNQSWNRdmVLRThFdW93RFFZSktvWklodmNOQVFFTEJ... [value shortened] -> "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURqRENDQW5TZ0F3SUJBZ0lSQUtZM2VQOXN1VHBVNmtVYllIZU9OS3N3RFFZSktvWklodmNOQVFFTEJ... [value shortened]`
- 1 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0014/paths/2f03c3ff17482abfe351/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0014>)

### [bitnami/common](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/common>)

Overview cell: 16

Status: skipped-library | Attempts: N/A

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0015>)

### [bitnami/concourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/concourse>)

Overview cell: 17

Status: failed | Attempts: 486

Audit findings: 470. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 464 additional audit findings in JSON.

#### E002 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: concourse 5.1.47 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... ers is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - A/c;CaNMC*:|'a#).:7.13.2-debian-12-r12 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.pegistpy = null`
- `$.image["Ua6*-kV"]["Maa<Laaaaaadaaaa,"] = {}`
- `$.image["Ua6*-kV"].aaaaaaaaa = []`
- `$.image["Ua6*-kV"].a = -2.6554551002088387e-171`
- `$.image.registry = "A" (was "docker.io")`
- `$.image.repository = "c;CaNMC*:|'a#)." (was "bitnami/concourse")`
- 1 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0016/paths/8e79b7dd85a286cfaddb/report.json>)

#### E039 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on concourse/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml:
line 187: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0016/paths/a0cdb2ba618083d9a8df/report.json>)

#### E040 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on concourse/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON: yaml:
line 17: could not find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0016/paths/91bb86cdd8574ec43d3d/report.json>)

#### E126 ([HH1109](#hh1109---invalid-manifest-field-type))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0016/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0016>)

### [bitnami/consul](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/consul>)

Overview cell: 18

Status: time-limit | Attempts: 165

Audit findings: 255. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 249 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0017>)

### [bitnami/contour](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/contour>)

Overview cell: 19

Status: failed | Attempts: 422

Audit findings: 591. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline["accesslog-format"]`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.disablePermitInsecure`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.tls`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.configInline.tls["fallback-certificate"]`: Undocumented values path (warning)
- 585 additional audit findings in JSON.

#### E127 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on contour/templates/contour/serviceaccount.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.contour.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.contour.serviceAccount.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0018/paths/850a7f073270a85899ed/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0018>)

### [bitnami/deepspeed](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/deepspeed>)

Overview cell: 20

Status: failed | Attempts: 185

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

#### E003 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: deepspeed 2.3.51 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... s is likely to cause degraded security and performance, broken chart features, and
missing environment variables. Unrecognized images: - 00/bitnami/deepspeed:0.17.5-debian-12-r0 If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.registry = "00"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0019/paths/8e79b7dd85a286cfaddb/observed-failure.json>)

#### E004 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0019/paths/47ebf688d3d510a9ed52/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0019>)

### [bitnami/discourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/discourse>)

Overview cell: 21

Status: failed | Attempts: 173

Audit findings: 346. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.email`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.username`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth`: Undocumented values path (warning)
- 340 additional audit findings in JSON.

#### E041 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on discourse/charts/redis/templates/master/application.yaml: error converting YAML to JSON: yaml: line 143:
did not find expected alphabetic or numeric character
```

Phase: $.redis.master.persistence.subPath | Status: failed

Changed overrides (used together):
- `$.redis.master.persistence.subPath = "I\n&"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0020/paths/03223810de42d02290b1/report.json>)

#### E128 ([HH1109](#hh1109---invalid-manifest-field-type))

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on discourse/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = []`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0020/paths/afbbf9ab6c6be5d414aa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0020>)

### [bitnami/dremio](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/dremio>)

Overview cell: 22

Status: failed | Attempts: 157

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

#### E005 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0021/paths/c5408860d7e66fba867d/report.json>)

#### E042 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on dremio/templates/bootstrap-user/job.yaml: error converting YAML to JSON: yaml: line 121: did not find
expected key
```

Phase: $.dremio.auth.username | Status: failed

Changed overrides (used together):
- `$.dremio.auth.username = "\r" (was "user")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0021/paths/7e3ba2e9db7688fe1f85/report.json>)

#### E043 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on dremio/templates/bootstrap-user/job.yaml: error converting YAML to JSON: yaml: line 143: did not find
expected alphabetic or numeric character
```

Phase: $.bootstrapUserJob.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.bootstrapUserJob.extraEnvVarsCM = "&\n" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0021/paths/5e487f511969b2a6049b/report.json>)

#### E044 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on dremio/templates/coordinator/statefulset.yaml: error converting YAML to JSON: yaml: line 370: did not
find expected alphabetic or numeric character
```

Phase: $.defaultInitContainers.generateConf.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.defaultInitContainers.generateConf.extraEnvVarsCM = "&\n" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0021/paths/35af5d126ee937a46af9/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0021>)

### [bitnami/drupal](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/drupal>)

Overview cell: 23

Status: failed | Attempts: 456

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

#### E011 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0022/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E012 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0022/paths/3a6df6c30eb21f3e500a/report.json>)

#### E013 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0022/paths/e9b2bd06f74a17778834/report.json>)

#### E045 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on drupal/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 39:
did not find expected ',' or ']'
```

Phase: $.mariadb.volumePermissions.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0022/paths/1a4166aed8b35c7751ed/report.json>)

#### E046 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on drupal/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 40:
did not find expected ',' or ']'
```

Phase: $.mariadb.metrics.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.metrics.image.pullSecrets = [null, [{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0022/paths/f3c891b2fda1d97f28f1/report.json>)

#### E047 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on drupal/templates/deployment.yaml: error converting YAML to JSON: yaml: line 228: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0022/paths/bc81b51736a9cdc4eda3/report.json>)

#### E138

```text
[Diagnostic shortened; full text in artifacts] ... nalProperties': {'$dynamicRef': '#meta'}}}, '$defs': {'anchorString': {'type': 'string',
'pattern': '^[A-Za-z_][-A-Za-z0-9._]*$'}, 'uriString': {'type': 'string', 'format': 'uri'}, 'uriReferenceString': {'type': 'string',
'format': 'uri-reference'}}} On
schema['allOf'][317]['properties']['certificates']['properties']['image']['properties']['pullSecrets']['items']: [{'properties': {'name':
{'const': None}}, 'required': ['name'], 'type': 'object'}]
```

Phase: $.certificates.image.pullSecrets[*].name | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.certificates.image.pullSecrets["*"].name. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0022/paths/521d1448570bba0f3fec/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0022>)

### [bitnami/ejbca](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ejbca>)

Overview cell: 24

Status: failed | Attempts: 499

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

#### E011 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0023/paths/1ff74c0fd3bc5bc52c04/report.json>)

#### E012 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0023/paths/3a6df6c30eb21f3e500a/report.json>)

#### E013 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0023/paths/e9b2bd06f74a17778834/report.json>)

#### E048 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on ejbca/charts/mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 39:
did not find expected ',' or ']'
```

Phase: $.mariadb.volumePermissions.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.volumePermissions.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0023/paths/1a4166aed8b35c7751ed/report.json>)

Phase: $.mariadb.metrics.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.mariadb.metrics.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0023/paths/f3c891b2fda1d97f28f1/report.json>)

#### E049 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on ejbca/templates/deployment.yaml: error converting YAML to JSON: yaml: line 207: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0023/paths/bc81b51736a9cdc4eda3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0023>)

### [bitnami/elasticsearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/elasticsearch>)

Overview cell: 25

Status: failed | Attempts: 1020

Audit findings: 814. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.config`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.containerPorts.restAPI`: Undocumented values path (warning)
- 808 additional audit findings in JSON.

Configuration rejections: 4 excluded; 10 adjusted and tested; 14 Helm verification renders (separate from manifest-test attempts).

#### E050 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/coordinating/statefulset.yaml: error converting YAML to JSON: yaml: line 234:
found unexpected end of stream
```

Phase: $.coordinating.schedulerName | Status: failed

Changed overrides (used together):
- `$.coordinating.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0024/paths/c725fa76dfbd1561269f/report.json>)

#### E051 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/coordinating/statefulset.yaml: error converting YAML to JSON: yaml: line 41:
block sequence entries are not allowed in this context
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0024/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.sysctlImage.pullSecrets[*] | Status: failed

Changed overrides (used together):
- `$.sysctlImage.pullSecrets = [[null]]`
Absent from overrides: $.sysctlImage.pullSecrets["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0024/paths/e326e771561b22095185/report.json>)

#### E052 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/ingest/statefulset.yaml: error converting YAML to JSON: yaml: line 25: could not
find expected ':'
```

Phase: $.ingest.nameOverride | Status: failed

Changed overrides (used together):
- `$.ingest.nameOverride = "\r" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0024/paths/9ad325076d817833ec6e/report.json>)

#### E053 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/master/pdb.yaml: error converting YAML to JSON: yaml: line 14: did not find
expected ',' or ']'
```

Phase: $.master.pdb | Status: failed

Changed overrides (used together):
- `$.master.pdb.minAvailable = "[Ma" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0024/paths/e57d4678169e24abedfb/report.json>)

#### E054 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on elasticsearch/templates/master/statefulset.yaml: error converting YAML to JSON: yaml: line 245: found
unexpected end of stream
```

Phase: $.master.schedulerName | Status: failed

Changed overrides (used together):
- `$.master.schedulerName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0024/paths/b3f60a0cb2adae0e1a9b/report.json>)

#### E117 ([HH1105](#hh1105---missing-resource-name))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0024/paths/b8432c270c9ae0524afb/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0024>)

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

#### E055 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on envoy-gateway/templates/certgen/job.yaml: error converting YAML to JSON: yaml: line 33: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0025/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0025/paths/097f6358a00dddbcdd83/report.json>)

#### E056 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on envoy-gateway/templates/certgen/job.yaml: error converting YAML to JSON: yaml: line 41: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.5.0-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0025/paths/8e79b7dd85a286cfaddb/report.json>)

#### E057 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on envoy-gateway/templates/deployment.yaml: error converting YAML to JSON: yaml: line 93: could not find
expected ':'
```

Phase: $.ratelimitImage.digest | Status: failed

Changed overrides (used together):
- `$.ratelimitImage.digest = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0025/paths/b56da783b3819637831b/report.json>)

#### E117 ([HH1105](#hh1105---missing-resource-name))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0025/paths/3bafd983ae0b309b29cf/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0025>)

### [bitnami/etcd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/etcd>)

Overview cell: 27

Status: time-limit | Attempts: 175

Audit findings: 407. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.caFilename`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.certFilename`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.client.certKeyFilename`: Undocumented values path (warning)
- 401 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0026>)

### [bitnami/external-dns](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/external-dns>)

Overview cell: 28

Status: failed | Attempts: 2590

Audit findings: 402. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.accessToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.clientSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.clientToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.host`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.akamai.secretName`: Undocumented values path (warning)
- 396 additional audit findings in JSON.

Configuration rejections: 0 excluded; 39 adjusted and tested; 39 Helm verification renders (separate from manifest-test attempts).

#### E006 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/8e79b7dd85a286cfaddb/report.json>)

Phase: $.image.repository | Status: failed

Changed overrides (used together):
- `$.image.repository = "00" (was "bitnami/external-dns")`
- `$.aws.assumeRoleArn = "example" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/3f7165f1837241716c3c/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E058 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/clusterrole.yaml: error converting YAML to JSON: yaml: line 123: did not find
expected alphabetic or numeric character
```

Phase: $.crd | Status: failed

Changed overrides (used together):
- `$.crd.apiversion = "&" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/774f347224e7442777b5/report.json>)

#### E059 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/clusterrole.yaml: error converting YAML to JSON: yaml: line 3: could not find
expected ':'
```

Phase: $.rbac.apiVersion | Status: failed

Changed overrides (used together):
- `$.rbac.apiVersion = "\n0" (was "v1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/e69069cd1d9fee6d24d5/report.json>)

#### E060 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/clusterrole.yaml: error converting YAML to JSON: yaml: line 6: could not find
expected ':'
```

Phase: $.namespaceOverride | Status: failed

Changed overrides (used together):
- `$.namespaceOverride = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/835d62e0a3e46b72c904/report.json>)

#### E061 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 125: found unexpected
end of stream
```

Phase: $.extraEnvVarsSecret | Status: failed

Changed overrides (used together):
- `$.extraEnvVarsSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/e4b1fa53526f192b7184/report.json>)

#### E062 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 131: found unexpected
end of stream
```

Phase: $.aws.credentials.secretName | Status: failed

Changed overrides (used together):
- `$.aws.credentials.secretName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/9066c81ede4ae0ccf541/report.json>)

#### E063 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 28: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/097f6358a00dddbcdd83/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E064 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 59: did not find
expected key
```

Phase: $.excludeDomains | Status: failed

Changed overrides (used together):
- `$.excludeDomains = [[null, null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/b2d23655889f85d3952a/report.json>)

Phase: $.domainFilters | Status: failed

Changed overrides (used together):
- `$.domainFilters = [[null, null]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/9740f35c2d5e35eba0d4/report.json>)

#### E065 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 66: could not find
expected ':'
```

Phase: $.logFormat | Status: failed

Changed overrides (used together):
- `$.logFormat = "\n0" (was "text")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/699f2b0cffa1417e6453/report.json>)

Phase: $.sources[*] | Status: failed

Changed overrides (used together):
- `$.sources = ["\n0", "ingress"]`
Absent from overrides: $.sources["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/cefe885437789bb081ba/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E066 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/af94618389499c220e76/report.json>)

Phase: $.regexDomainExclusion | Status: failed

Changed overrides (used together):
- `$.regexDomainExclusion = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/edeac4f78ac58c423cf1/report.json>)

9 additional occurrences are retained in the JSON report and chart artifacts.

#### E067 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 71: could not find
expected ':'
```

Phase: $.aws.zoneTags | Status: failed

Changed overrides (used together):
- `$.aws.zoneTags = [{"\r": null}]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/798e8da1c0646feefff7/report.json>)

Phase: $.aws.dynamodbTable | Status: failed

Changed overrides (used together):
- `$.aws.dynamodbTable = "\n0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/c9b1ab3f25fd120432ec/report.json>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E068 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on external-dns/templates/deployment.yaml: error converting YAML to JSON: yaml: line 72: could not find
expected ':'
```

Phase: $.extraArgs | Status: failed

Changed overrides (used together):
- `$.extraArgs["\n0"] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/6b07fe5f61f90919fc2a/report.json>)

#### E122 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/17d970eb96f24f23c2d5/report.json>)

#### E135 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: external-dns/templates/_helpers.tpl:716:16 executing "external-dns.serviceAccountName" at <include "common.names.fullname"
.>: error calling include: template: no template "common.names.fullname" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0027/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0027>)

### [bitnami/flink](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flink>)

Overview cell: 29

Status: failed | Attempts: 341

Audit findings: 281. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.diagnosticMode.enabled`: Undocumented values path (warning)
- 275 additional audit findings in JSON.

Configuration rejections: 0 excluded; 10 adjusted and tested; 10 Helm verification renders (separate from manifest-test attempts).

#### E117 ([HH1105](#hh1105---missing-resource-name))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0028/paths/7af610caee367f12c985/report.json>)

#### E129 ([HH1109](#hh1109---invalid-manifest-field-type))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0028/paths/067a3a5b55160a73e780/report.json>)

Phase: $.taskmanager.serviceAccount.annotations | Status: failed

Changed overrides (used together):
- `$.jobmanager.updateStrategy.rollingUpdate = null (was null)`
- `$.taskmanager.serviceAccount.annotations[""] = []`
- `$.taskmanager.updateStrategy.rollingUpdate = null (was null)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0028/paths/87333782ef85d7076304/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0028>)

### [bitnami/fluent-bit](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluent-bit>)

Overview cell: 30

Status: time-limit | Attempts: 119

Audit findings: 240. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.annotations`: Undocumented values path (warning)
- 234 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0029>)

### [bitnami/fluentd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluentd>)

Overview cell: 31

Status: failed | Attempts: 175

Audit findings: 427. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.aggregator.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.aggregator.autoscaling`: Undocumented values path (warning)
- 421 additional audit findings in JSON.

#### E069 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on fluentd/templates/aggregator-statefulset.yaml: error converting YAML to JSON: yaml: line 173: found
unexpected end of stream
```

Phase: $.aggregator.readinessProbe.httpGet.port | Status: failed

Changed overrides (used together):
- `$.aggregator.readinessProbe.httpGet.port = "'" (was "http")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0030/paths/2476afe480f996e899c7/report.json>)

#### E070 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on fluentd/templates/forwarder-daemonset.yaml: error converting YAML to JSON: yaml: line 168: found
unexpected end of stream
```

Phase: $.forwarder.livenessProbe.tcpSocket.port | Status: failed

Changed overrides (used together):
- `$.forwarder.livenessProbe.tcpSocket.port = "'" (was "http")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0030/paths/25b567cc42066c51ab36/report.json>)

#### E117 ([HH1105](#hh1105---missing-resource-name))

**Missing resource name** (manifest / violation). Severity: **error**. Provide a name in each resource branch; ignore this check if your
workflow intentionally uses generated names.

```text
[HH1105] resource has no metadata.name
```

Phase: $.forwarder.serviceAccount.name | Status: failed

Changed overrides (used together):
- `$.forwarder.serviceAccount.name = "0" (was "")`

Manifest changes from rendered defaults (document and list order preserved):
- `$[12].spec.template.spec.serviceAccountName: "hypothesis-fluentd-forwarder" -> 0`
- `$[3].metadata.name: "hypothesis-fluentd-forwarder" -> 0`
- `$[8].subjects[0].name: "hypothesis-fluentd-forwarder" -> 0`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0030/paths/ca943a97983f240fc389/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0030>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0031>)

### [bitnami/ghost](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ghost>)

Overview cell: 33

Status: failed | Attempts: 540

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

#### E007 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: ghost 25.0.5 / templates/NOTES.txt

```text
[Diagnostic shortened; full text in artifacts] ... standard containers is likely to cause degraded security and performance, broken chart
features, and missing environment variables. Unrecognized images: - a`C.%_qhq/qh,:YvIa!gqe If you are sure you want to proceed with
non-standard containers, you can skip container image verification by setting the global parameter 'global.security.allowInsecureImages' to
true. Further information can be obtained at https://github.com/bitnami/charts/issues/30850
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image["00000000"] = null`
- `$.image.pullPolicy = "C\"8" (was "IfNotPresent")`
- ``$.image.registry = "a`C.%_qhq" (was "docker.io")``
- `$.image["5Ba"].Nas = []`
- `$.image["TtX_taQa(au|,J\"-a)"] = [[{"aa": []}, {}, [-16369, [], []]], {}, {"aaaa": "iaaaaaaa", "aaaxcaataasaaaa": true, "a*": null}]`
- `$.image.pullSecrets = [{"": {"aaarma": "a", "": "aaaaayarap", "a": -1.1015563147463898e+106}, "aaaaaaaa+a[*aaaaaa": [true, -4.0060410845671934... [value shortened]`
- 3 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0032/paths/8e79b7dd85a286cfaddb/report.json>)

#### E014 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0032/paths/5590c72bafc403304bea/report.json>)

#### E015 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0032/paths/006198abce843ffa5be2/report.json>)

#### E017 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0032/paths/1c25c32c569a13118399/report.json>)

#### E071 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0032/paths/25e1b252cef0182d6d1d/report.json>)

#### E132 ([HH3001](#hh3001---template-accesses-a-missing-object))

**Template accesses a missing object** (template / violation). Severity: **error**. Guard or default the parent object, or require it in the
values schema.

```text
[HH3001] Error: ghost/charts/mysql/templates/networkpolicy.yaml:72:69 executing "ghost/charts/mysql/templates/networkpolicy.yaml" at
<$value.port>: nil pointer evaluating interface {}.port
```

Phase: $.mysql.primary.service.extraPorts | Status: failed

Changed overrides (used together):
- `$.mysql.primary.service.extraPorts = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0032/paths/cd1b3bd14efaf6a86788/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0032>)

### [bitnami/gitea](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitea>)

Overview cell: 34

Status: failed | Attempts: 309

Audit findings: 241. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.adminUsername`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.appName`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- 235 additional audit findings in JSON.

#### E072 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitea/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON: yaml:
line 17: could not find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0033/paths/91bb86cdd8574ec43d3d/report.json>)

#### E073 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitea/templates/deployment.yaml: error converting YAML to JSON: yaml: line 202: found unexpected end of
stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0033/paths/bc81b51736a9cdc4eda3/report.json>)

#### E133 ([HH3002](#hh3002---incompatible-value-type-in-template))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0033/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0033>)

### [bitnami/gitlab-runner](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitlab-runner>)

Overview cell: 35

Status: failed | Attempts: 576

Audit findings: 266. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 260 additional audit findings in JSON.

#### E074 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 27: could not find
expected ':'
```

Phase: $.extraConfig | Status: failed

Changed overrides (used together):
- `$.extraConfig = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0034/paths/d8ec1a80ed2510a23238/report.json>)

#### E075 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 29: could not find
expected ':'
```

Phase: $.runners.config | Status: failed

Changed overrides (used together):
- `$.runners.config = "\r0" (was "[[runners]]\n  [runners.kubernetes]\n    namespace = \"{{ include \"common.names.namespace\" . }}\"\n    image = \"{{ i... [value shortened])`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0034/paths/6a52673273db836d0a2b/report.json>)

#### E076 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 31: could not find
expected ':'
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.digest = "\r" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0034/paths/8e79b7dd85a286cfaddb/report.json>)

#### E077 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on gitlab-runner/templates/configmap.yaml: error converting YAML to JSON: yaml: line 35: could not find
expected ':'
```

Phase: $.helperImage.repository | Status: failed

Changed overrides (used together):
- `$.helperImage.repository = "\r" (was "bitnami/gitlab-runner-helper")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0034/paths/1009129d047c87cec347/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0034>)

### [bitnami/grafana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana>)

Overview cell: 36

Status: failed | Attempts: 208

Audit findings: 306. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.admin.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin.user`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.admin`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alerting.configMapName`: Undocumented values path (warning)
- 300 additional audit findings in JSON.

Configuration rejections: 3 excluded; 0 adjusted and tested; 3 Helm verification renders (separate from manifest-test attempts).

#### E083 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 143: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0035/paths/bc81b51736a9cdc4eda3/report.json>)

#### E084 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana/templates/application.yaml: error converting YAML to JSON: yaml: line 63: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0035/paths/8e79b7dd85a286cfaddb/observed-failure.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0035>)

### [bitnami/grafana-alloy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-alloy>)

Overview cell: 37

Status: time-limit | Attempts: 85

Audit findings: 292. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.name`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alloy.clustering.portName`: Undocumented values path (warning)
- 286 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0036>)

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

#### E078 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-k6-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 36: did not
find expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0037/paths/a4a0ea6ab697189bb963/report.json>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0037/paths/097f6358a00dddbcdd83/report.json>)

2 additional occurrences are retained in the JSON report and chart artifacts.

#### E079 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-k6-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "0.0.23-debian-12-r1")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0037/paths/8e79b7dd85a286cfaddb/report.json>)

#### E080 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0037/paths/3f7165f1837241716c3c/report.json>)

Phase: $.global.imageRegistry | Status: failed

Changed overrides (used together):
- `$.global.imageRegistry = "\r" (was "")`
- `$.global.security.allowInsecureImages = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0037/paths/fa90b40f46c6c70d8821/report.json>)

#### E081 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on grafana-k6-operator/templates/deployment.yaml: error converting YAML to JSON: yaml: line 82: mapping
values are not allowed in this context
```

Phase: $.runnerImage.tag | Status: failed

Changed overrides (used together):
- `$.runnerImage.tag = "" (was "1.2.3-debian-12-r0")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0037/paths/ec2699463ba169ce5fd5/report.json>)

#### E082 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0037/paths/43da1bc246e2f89450ac/report.json>)

#### E136 ([HH3003](#hh3003---undefined-named-template))

**Undefined named template** (template / violation). Severity: **error**. Check the helper name, its definition and dependency availability.

```text
[HH3003] Error: grafana-k6-operator/templates/vpa.yaml:6:12 executing "grafana-k6-operator/templates/vpa.yaml" at <include
"common.capabilities.apiVersions.has" (dict "version" "autoscaling.k8s.io/v1/VerticalPodAutoscaler" "context" .)>: error calling include:
template: no template "common.capabilities.apiVersions.has" associated with template "gotpl"
```

Phase: $.tags | Status: failed

Changed overrides (used together):
- `$.tags["bitnami-common"] = false`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0037/paths/e2cac8a5225634937910/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0037>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0038>)

### [bitnami/grafana-mimir](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-mimir>)

Overview cell: 40

Status: time-limit | Attempts: 78

Audit findings: 1540. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage.backend`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.alertmanager.blockStorage.config`: Undocumented values path (warning)
- 1534 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0039>)

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

#### E119 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource grafana.integreatly.org/v1beta1/Grafana requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0040/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0040>)

### [bitnami/grafana-tempo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-tempo>)

Overview cell: 42

Status: time-limit | Attempts: 127

Audit findings: 999. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.compactor.automountServiceAccountToken`: Undocumented values path (warning)
- 993 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0041>)

### [bitnami/haproxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/haproxy>)

Overview cell: 43

Status: failed | Attempts: 127

Audit findings: 186. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 180 additional audit findings in JSON.

#### E085 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on haproxy/templates/deployment.yaml: error converting YAML to JSON: yaml: line 60: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0042/paths/8e79b7dd85a286cfaddb/observed-failure.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0042>)

### [bitnami/harbor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/harbor>)

Overview cell: 44

Status: failed | Attempts: 66

Audit findings: 1499. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache.expireHours`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cache`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.certificateVolume.resources`: Undocumented values path (warning)
- 1493 additional audit findings in JSON.

#### E130 ([HH1109](#hh1109---invalid-manifest-field-type))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0043/paths/afbbf9ab6c6be5d414aa/observed-failure.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0043>)

### [bitnami/influxdb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/influxdb>)

Overview cell: 45

Status: time-limit | Attempts: 1

Audit findings: 345. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.createAdminToken`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.auth.createAdminToken`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- 339 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0044>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0045>)

### [bitnami/janusgraph](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/janusgraph>)

Overview cell: 47

Status: failed | Attempts: 431

Audit findings: 328. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- 322 additional audit findings in JSON.

Configuration rejections: 6 excluded; 10 adjusted and tested; 16 Helm verification renders (separate from manifest-test attempts).

#### E001 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0046/paths/c40b667a5f96c213ecf1/report.json>)

#### E086 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on janusgraph/charts/cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 204:
block sequence entries are not allowed in this context
```

Phase: $.cassandra.tls | Status: failed

Changed overrides (used together):
- `$.cassandra.tls.passwordsSecret = "-"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0046/paths/a077a8f76c5331673254/report.json>)

#### E087 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on janusgraph/charts/cassandra/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 232:
found unexpected end of stream
```

Phase: $.cassandra.persistence.commitLogMountPath | Status: failed

Changed overrides (used together):
- `$.cassandra.persistence.commitLogMountPath = "'"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0046/paths/12b50ce698cb59db09df/report.json>)

#### E117 ([HH1105](#hh1105---missing-resource-name))

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
- `$[6].data["cassandra-password"]: "T0VpUXdxRzlwcw==" -> "UG1RQ1ZHeE1TNw=="`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0046/paths/d24e471a96b8372c3d8a/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0046>)

### [bitnami/jenkins](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jenkins>)

Overview cell: 48

Status: failed | Attempts: 204

Audit findings: 348. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.annotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.containerExtraEnvVars`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.agent.containerSecurityContext`: Undocumented values path (warning)
- 342 additional audit findings in JSON.

#### E088 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jenkins/templates/deployment.yaml: error converting YAML to JSON: yaml: line 162: found unexpected end
of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0047/paths/bc81b51736a9cdc4eda3/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0047>)

### [bitnami/jupyterhub](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jupyterhub>)

Overview cell: 49

Status: failed | Attempts: 416

Audit findings: 625. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.digest`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.pullPolicy`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.pullSecrets`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.registry`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.repository`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auxiliaryImage.tag`: Undocumented values path (warning)
- 619 additional audit findings in JSON.

#### E008 ([HH1001](#hh1001---unclassified-template-failure))

**Unclassified template failure** (unclassified / diagnostic). Severity: **error**. Inspect the Helm diagnostic and reproducer; the exit
alone does not establish a chart defect.

Source: jupyterhub 10.0.6 / templates/proxy/deployment.yaml

```text
execution error at (jupyterhub/templates/proxy/deployment.yaml:32:32): ERROR: Preset key '' invalid. Allowed values are
medium,large,xlarge,2xlarge,nano,micro,small
```

Phase: $.singleuser.resourcesPreset | Status: failed

Changed overrides (used together):
- `$.singleuser.resourcesPreset = "" (was "small")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0048/paths/6cdbd337aff10ffe4fbd/report.json>)

#### E089 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jupyterhub/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml:
line 189: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0048/paths/a0cdb2ba618083d9a8df/report.json>)

#### E090 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jupyterhub/charts/postgresql/templates/read/extended-configmap.yaml: error converting YAML to JSON:
yaml: line 17: could not find expected ':'
```

Phase: $.postgresql.readReplicas.extendedConfiguration | Status: failed

Changed overrides (used together):
- `$.postgresql.readReplicas.extendedConfiguration = "\r0"`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0048/paths/91bb86cdd8574ec43d3d/report.json>)

#### E091 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jupyterhub/templates/hub/deployment.yaml: error converting YAML to JSON: yaml: line 227: found
unexpected end of stream
```

Phase: $.hub.image.pullPolicy | Status: failed

Changed overrides (used together):
- `$.hub.image.pullPolicy = "'" (was "IfNotPresent")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0048/paths/e5effc76fd5f5680e1fa/report.json>)

#### E092 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jupyterhub/templates/proxy/deployment.yaml: error converting YAML to JSON: yaml: line 61: mapping values
are not allowed in this context
```

Phase: $.proxy.image.tag | Status: failed

Changed overrides (used together):
- `$.proxy.image.tag = "" (was "5.0.1-debian-12-r21")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0048/paths/6ac111f0dfafe8288da8/report.json>)

#### E093 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on jupyterhub/templates/proxy/service-public.yaml: error converting YAML to JSON: yaml: line 27: found
unexpected end of stream
```

Phase: $.proxy.service.public.loadBalancerIP | Status: failed

Changed overrides (used together):
- `$.proxy.service.public.loadBalancerIP = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0048/paths/b8ce65881d65d695d140/report.json>)

#### E121 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.coreos.com/v1/ServiceMonitor requires an explicit JSON schema in resource_schemas
```

Phase: $.hub.metrics.serviceMonitor | Status: failed

Changed overrides (used together):
- `$.hub.metrics.serviceMonitor.enabled = true (was false)`

Manifest changes from rendered defaults (document and list order preserved):
- `$[13].data.password: "OGdzY0NjMTVUYQ==" -> "TlJZZzk3ckNUUA=="`
- `$[13].data["postgres-password"]: "N0ZNN1hkbjA1cg==" -> "SGN3UHVERFNudw=="`
- `$[14].data["hub.config.CryptKeeper.keys"]: "MDQyZTU2NjFlYzc1MTg2OGVjZTMxZjlmNmI0YjY4MmU0NjAxNDEzODkzYzU0ZWJiYzA4NmJkZDRmMzZkYjQ3Mw==" -> "M2U5NTllY2YyNTkwNDk5NmU3NjZmOWE1NDgzYmE5NDM0MjBhZDgzNjUxZjVkOWI5MjE0ZmE0MTJlMDI5YTlhYg=="`
- `$[14].data["hub.config.JupyterHub.cookie_secret"]: "NDU1MTc1N2Y4YTY2NjlkNjNlMTZiN2Q2OWUxNGMxYjE0YjQxYzAxZjYzMDRkMGVjMzcxODI4MGVlZmU3ZjA2NA==" -> "ZGNmMWM5YzUzOWM4YTE2NzliMjYxMDk1MTZmN2U0ODdhNDAwNWY3MmYzMjdjZWRiMTAzNzcwNjM5MDI2MDU5OA=="`
- `$[14].data["proxy-token"]: "NG5HU09wblFnUGYzVUNVaDhTSzgzelFZZGpsNzNHRWc=" -> "YmZhS0E4a2dYeXE2Um9xbEFsVHJmeW5mRUVUNHd1QUU="`
- `$[14].data["values.yaml"]: "Q2hhcnQ6CiAgTmFtZToganVweXRlcmh1YgogIFZlcnNpb246IDEwLjAuNgpSZWxlYXNlOgogIE5hbWU6IGh5cG90aGVzaXMKICBOYW1lc3BhY2U6IGRlZmF... [value shortened] -> "Q2hhcnQ6CiAgTmFtZToganVweXRlcmh1YgogIFZlcnNpb246IDEwLjAuNgpSZWxlYXNlOgogIE5hbWU6IGh5cG90aGVzaXMKICBOYW1lc3BhY2U6IGRlZmF... [value shortened]`
- 4 more changes; see JSON artifacts.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0048/paths/373db267daac756f7747/report.json>)

#### E134 ([HH3002](#hh3002---incompatible-value-type-in-template))

**Incompatible value type in template** (template / violation). Severity: **error**. Align the template operation with the accepted input
types, or narrow the schema.

```text
[HH3002] Error: jupyterhub/charts/postgresql/templates/primary/statefulset.yaml:621:27 executing
"jupyterhub/charts/postgresql/templates/primary/statefulset.yaml" at <include "postgresql.v1.secretName" .>: error calling include:
jupyterhub/charts/postgresql/templates/_helpers.tpl:104:32 executing "postgresql.v1.secretName" at
<.Values.global.postgresql.auth.existingSecret>: wrong type for value; expected string; got []interface {}
```

Phase: $.global.postgresql.auth | Status: failed

Changed overrides (used together):
- `$.global.postgresql.auth.database = null`
- `$.global.postgresql.auth["0a n"] = true`
- `$.global.postgresql.auth[""] = null`
- `$.global.postgresql.auth.existingSecret = [null]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0048/paths/537424102b6e359c83d6/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0048>)

### [bitnami/kafka](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kafka>)

Overview cell: 50

Status: failed | Attempts: 429

Audit findings: 790. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$[""]`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$[""]`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.broker.automountServiceAccountToken`: Undocumented values path (warning)
- 784 additional audit findings in JSON.

Configuration rejections: 5 excluded; 0 adjusted and tested; 5 Helm verification renders (separate from manifest-test attempts).

#### E094 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kafka/templates/controller-eligible/statefulset.yaml: error converting YAML to JSON: yaml: line 105: did
not find expected key
```

Phase: $.controller.topologyKey | Status: failed

Changed overrides (used together):
- `$.controller.topologyKey = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0049/paths/96bdd08b814a4c59648f/report.json>)

#### E095 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kafka/templates/controller-eligible/statefulset.yaml: error converting YAML to JSON: yaml: line 106: did
not find expected key
```

Phase: $.controller.runtimeClassName | Status: failed

Changed overrides (used together):
- `$.controller.runtimeClassName = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0049/paths/f82d28e2c30ee5985d85/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0049>)

### [bitnami/keycloak](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keycloak>)

Overview cell: 51

Status: failed | Attempts: 301

Audit findings: 448. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.adminRealm`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.adminUser`: Undocumented values path (warning)
- 442 additional audit findings in JSON.

#### E114 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0050/paths/a0cdb2ba618083d9a8df/report.json>)

#### E115 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0050/paths/91bb86cdd8574ec43d3d/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0050>)

### [bitnami/keydb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keydb>)

Overview cell: 52

Status: failed | Attempts: 422

Audit findings: 499. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.architecture`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecretPasswordKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- 493 additional audit findings in JSON.

#### E096 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/configmap.yaml: error converting YAML to JSON: yaml: line 27: did not find
expected key
```

Phase: $.replica.disableCommands | Status: failed

Changed overrides (used together):
- `$.replica.disableCommands = ["\r"]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0051/paths/9ab33350907009275568/report.json>)

#### E097 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/networkpolicy.yaml: error converting YAML to JSON: yaml: line 39: mapping values
are not allowed in this context
```

Phase: $.replica.networkPolicy | Status: failed

Changed overrides (used together):
- `$.replica.networkPolicy.allowExternalEgress = false (was true)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0051/paths/ead96de3dd100ee4f6d1/report.json>)

#### E098 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/statefulset.yaml: error converting YAML to JSON: yaml: line 175: found
unexpected end of stream
```

Phase: $.replica.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.replica.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0051/paths/dadf473ae2669113900c/report.json>)

#### E099 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on keydb/templates/replica/statefulset.yaml: error converting YAML to JSON: yaml: line 177: found
unexpected end of stream
```

Phase: $.replica.extraEnvVarsCM | Status: failed

Changed overrides (used together):
- `$.replica.extraEnvVarsCM = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0051/paths/b71ec3b23bacb342be46/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0051>)

### [bitnami/kibana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kibana>)

Overview cell: 53

Status: time-limit | Attempts: 1

Audit findings: 257. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- 251 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0052>)

### [bitnami/kong](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kong>)

Overview cell: 54

Status: failed | Attempts: 371

Audit findings: 390. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.metrics`: Undocumented values path (warning)
- 384 additional audit findings in JSON.

#### E100 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kong/charts/postgresql/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line
189: found unexpected end of stream
```

Phase: $.postgresql.auth.existingSecret | Status: failed

Changed overrides (used together):
- `$.postgresql.auth.existingSecret = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0053/paths/a0cdb2ba618083d9a8df/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0053>)

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

#### E101 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-arangodb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 38: did not find
expected ',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[{}]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0054/paths/a4a0ea6ab697189bb963/report.json>)

#### E102 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-arangodb/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values
are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "1.3.0-debian-12-r4")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0054/paths/8e79b7dd85a286cfaddb/report.json>)

#### E103 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-arangodb/templates/service.yaml: error converting YAML to JSON: yaml: line 39: found unexpected end
of stream
```

Phase: $.service.nodePorts.apiGrpc | Status: failed

Changed overrides (used together):
- `$.service.nodePorts.apiGrpc = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0054/paths/5e977ce661c5834a77a0/report.json>)

#### E113 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] invalid rendered YAML: ruamel: while constructing a mapping in "<unicode string>", line 1010, column 3: namespace: "default" ^
(line: 1010) found duplicate key "namespace" with value "default" (original value: "default") in "<unicode string>", line 1011, column 3:
namespace: "default" ^ (line: 1011) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.autoscaling.hpa.enabled | Status: failed

Changed overrides (used together):
- `$.autoscaling.hpa.enabled = true (was false)`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0054/paths/d461ce5afe144683ffee/report.json>)

#### E117 ([HH1105](#hh1105---missing-resource-name))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0054/paths/95bc8b2087be846a7d07/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0054>)

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

#### E120 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource monitoring.coreos.com/v1/Alertmanager requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0055/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0055>)

### [bitnami/kube-prometheus/charts/kube-prometheus-crds](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus/charts/kube-prometheus-crds>)

Overview cell: 57

Status: failed | Attempts: 1

Audit findings: 1. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.exampleValue`: Undocumented values path (warning)

#### E118 ([HH1107](#hh1107---empty-resource-bundle))

**Empty resource bundle** (manifest / violation). Severity: **error**. Check resource activation; ignore this contract if an empty chart is
intentional.

```text
[HH1107] chart rendered no resources
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0056/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0056>)

### [bitnami/kube-state-metrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-state-metrics>)

Overview cell: 58

Status: failed | Attempts: 151

Audit findings: 208. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- 202 additional audit findings in JSON.

#### E104 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kube-state-metrics/templates/deployment.yaml: error converting YAML to JSON: yaml: line 55: mapping
values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0057/paths/8e79b7dd85a286cfaddb/observed-failure.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0057>)

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

#### E123 ([HH1108](#hh1108---kubernetes-schema-validation-failed))

**Kubernetes schema validation failed** (manifest / violation). Severity: **error**. Use the validator's field path and expected type to
check the template and input schema.

```text
[HH1108] Custom resource ray.io/v1/RayCluster requires an explicit JSON schema in resource_schemas
```

Phase: chart | Status: failed

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0058/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0058>)

### [bitnami/kubernetes-event-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kubernetes-event-exporter>)

Overview cell: 60

Status: failed | Attempts: 218

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.vpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.vpa.annotations`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

#### E105 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on kubernetes-event-exporter/templates/deployment.yaml: error converting YAML to JSON: yaml: line 59:
mapping values are not allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = ""`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0059/paths/8e79b7dd85a286cfaddb/observed-failure.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0059>)

### [bitnami/logstash](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/logstash>)

Overview cell: 61

Status: failed | Attempts: 216

Audit findings: 219. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.annotations`: Undocumented values path (warning)
- [HH2004](#hh2004---no-supplied-default-for-a-values-path) at `$.annotations`: No supplied default for a values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- 213 additional audit findings in JSON.

#### E106 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/configuration-cm.yaml: error converting YAML to JSON: yaml: line 31: could not find
expected ':'
```

Phase: $.filter | Status: failed

Changed overrides (used together):
- `$.filter = "\r0" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0060/paths/0e1e9caa4953f85afca2/report.json>)

#### E107 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on logstash/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 26: did not find
expected '-' indicator
```

Phase: $.networkPolicy.customRules | Status: failed

Changed overrides (used together):
- `$.networkPolicy.customRules[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0060/paths/1d6a5faf6612f0fc5d5a/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0060>)

### [bitnami/mariadb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb>)

Overview cell: 62

Status: failed | Attempts: 206

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

#### E112 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb/templates/primary/statefulset.yaml: error converting YAML to JSON: yaml: line 220: found
unexpected end of stream
```

Phase: $.primary.terminationGracePeriodSeconds | Status: failed

Changed overrides (used together):
- `$.primary.terminationGracePeriodSeconds = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0061/paths/af9a77b4b696ef0a07df/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0061>)

### [bitnami/mariadb-galera](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb-galera>)

Overview cell: 63

Status: failed | Attempts: 271

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

#### E009 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0062/paths/374c3045cc99de520f56/report.json>)

#### E010 ([HH1001](#hh1001---unclassified-template-failure))

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

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0062/paths/9bfb61fcd2895ab39c7d/report.json>)

#### E108 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/networkpolicy.yaml: error converting YAML to JSON: yaml: line 27: did not find
expected '-' indicator
```

Phase: $.networkPolicy.customRules | Status: failed

Changed overrides (used together):
- `$.networkPolicy.customRules[""] = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0062/paths/1d6a5faf6612f0fc5d5a/report.json>)

#### E109 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/pdb.yaml: error converting YAML to JSON: yaml: line 18: found unexpected end of
stream
```

Phase: $.pdb.maxUnavailable | Status: failed

Changed overrides (used together):
- `$.pdb.maxUnavailable = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0062/paths/d6baed3b8998a068f471/report.json>)

#### E110 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 236: found
unexpected end of stream
```

Phase: $.persistence.existingClaim | Status: failed

Changed overrides (used together):
- `$.persistence.existingClaim = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0062/paths/bc81b51736a9cdc4eda3/report.json>)

#### E111 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on mariadb-galera/templates/statefulset.yaml: error converting YAML to JSON: yaml: line 247: found
unexpected end of stream
```

Phase: $.updateStrategy | Status: failed

Changed overrides (used together):
- `$.updateStrategy.type = "'" (was "RollingUpdate")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0062/paths/dd21b70e90c3f6adcf0d/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0062>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0063>)

### [bitnami/matomo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/matomo>)

Overview cell: 65

Status: interrupted | Attempts: N/A

#### E137

```text
Interrupted by user
```

Phase: chart | Status: interrupted

No triggering values were recorded for this diagnostic.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789924640/0064>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789924640/0064>)

### [bitnami/memcached](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/memcached>)

Overview cell: 66

Status: pending | Attempts: N/A

### [bitnami/metallb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metallb>)

Overview cell: 67

Status: pending | Attempts: N/A

### [bitnami/metrics-server](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/metrics-server>)

Overview cell: 68

Status: pending | Attempts: N/A

### [bitnami/milvus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/milvus>)

Overview cell: 69

Status: pending | Attempts: N/A

### [bitnami/mlflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mlflow>)

Overview cell: 70

Status: pending | Attempts: N/A

### [bitnami/mongodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb>)

Overview cell: 71

Status: pending | Attempts: N/A

### [bitnami/mongodb-sharded](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mongodb-sharded>)

Overview cell: 72

Status: pending | Attempts: N/A

### [bitnami/moodle](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/moodle>)

Overview cell: 73

Status: pending | Attempts: N/A

### [bitnami/multus-cni](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/multus-cni>)

Overview cell: 74

Status: pending | Attempts: N/A

### [bitnami/mysql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mysql>)

Overview cell: 75

Status: pending | Attempts: N/A

### [bitnami/nats](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nats>)

Overview cell: 76

Status: pending | Attempts: N/A

### [bitnami/neo4j](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/neo4j>)

Overview cell: 77

Status: pending | Attempts: N/A

### [bitnami/nessie](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nessie>)

Overview cell: 78

Status: pending | Attempts: N/A

### [bitnami/nginx](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/nginx>)

Overview cell: 79

Status: pending | Attempts: N/A

### [bitnami/node-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/node-exporter>)

Overview cell: 80

Status: pending | Attempts: N/A

### [bitnami/oauth2-proxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/oauth2-proxy>)

Overview cell: 81

Status: pending | Attempts: N/A

### [bitnami/odoo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/odoo>)

Overview cell: 82

Status: pending | Attempts: N/A

### [bitnami/opensearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/opensearch>)

Overview cell: 83

Status: pending | Attempts: N/A

### [bitnami/parse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/parse>)

Overview cell: 84

Status: pending | Attempts: N/A

### [bitnami/phpmyadmin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/phpmyadmin>)

Overview cell: 85

Status: pending | Attempts: N/A

### [bitnami/pinniped](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pinniped>)

Overview cell: 86

Status: pending | Attempts: N/A

### [bitnami/postgresql](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql>)

Overview cell: 87

Status: pending | Attempts: N/A

### [bitnami/postgresql-ha](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/postgresql-ha>)

Overview cell: 88

Status: pending | Attempts: N/A

### [bitnami/prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/prometheus>)

Overview cell: 89

Status: pending | Attempts: N/A

### [bitnami/pytorch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/pytorch>)

Overview cell: 90

Status: pending | Attempts: N/A

### [bitnami/rabbitmq](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq>)

Overview cell: 91

Status: pending | Attempts: N/A

### [bitnami/rabbitmq-cluster-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/rabbitmq-cluster-operator>)

Overview cell: 92

Status: pending | Attempts: N/A

### [bitnami/redis](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis>)

Overview cell: 93

Status: pending | Attempts: N/A

### [bitnami/redis-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redis-cluster>)

Overview cell: 94

Status: pending | Attempts: N/A

### [bitnami/redmine](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/redmine>)

Overview cell: 95

Status: pending | Attempts: N/A

### [bitnami/schema-registry](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/schema-registry>)

Overview cell: 96

Status: pending | Attempts: N/A

### [bitnami/scylladb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/scylladb>)

Overview cell: 97

Status: pending | Attempts: N/A

### [bitnami/sealed-secrets](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sealed-secrets>)

Overview cell: 98

Status: pending | Attempts: N/A

### [bitnami/seaweedfs](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/seaweedfs>)

Overview cell: 99

Status: pending | Attempts: N/A

### [bitnami/solr](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/solr>)

Overview cell: 100

Status: pending | Attempts: N/A

### [bitnami/sonarqube](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/sonarqube>)

Overview cell: 101

Status: pending | Attempts: N/A

### [bitnami/spark](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/spark>)

Overview cell: 102

Status: pending | Attempts: N/A

### [bitnami/superset](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/superset>)

Overview cell: 103

Status: pending | Attempts: N/A

### [bitnami/tensorflow-resnet](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tensorflow-resnet>)

Overview cell: 104

Status: pending | Attempts: N/A

### [bitnami/thanos](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/thanos>)

Overview cell: 105

Status: pending | Attempts: N/A

### [bitnami/tomcat](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/tomcat>)

Overview cell: 106

Status: pending | Attempts: N/A

### [bitnami/valkey](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey>)

Overview cell: 107

Status: pending | Attempts: N/A

### [bitnami/valkey-cluster](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/valkey-cluster>)

Overview cell: 108

Status: pending | Attempts: N/A

### [bitnami/vault](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/vault>)

Overview cell: 109

Status: pending | Attempts: N/A

### [bitnami/victoriametrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/victoriametrics>)

Overview cell: 110

Status: pending | Attempts: N/A

### [bitnami/whereabouts](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/whereabouts>)

Overview cell: 111

Status: pending | Attempts: N/A

### [bitnami/wildfly](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wildfly>)

Overview cell: 112

Status: pending | Attempts: N/A

### [bitnami/wordpress](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/wordpress>)

Overview cell: 113

Status: pending | Attempts: N/A

### [bitnami/zipkin](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zipkin>)

Overview cell: 114

Status: pending | Attempts: N/A

### [bitnami/zookeeper](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/zookeeper>)

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

### HH3002 - Incompatible value type in template

Default severity: **error** | Category: template | Evidence type: violation

Helm reports a wrong value type, a field unavailable on a type, or an unsupported range operand.

Suggested action: Align the template operation with the accepted input types, or narrow the schema.

### HH3003 - Undefined named template

Default severity: **error** | Category: template | Evidence type: violation

Helm reports that a called named template is not defined.

Suggested action: Check the helper name, its definition and dependency availability.
