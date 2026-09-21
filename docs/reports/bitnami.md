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
  - [HH1101 - Invalid YAML in rendered output](#hh1101---invalid-yaml-in-rendered-output)
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
Started (Unix epoch): 1789959424
Started (UTC): 2026-09-21T02:57:04.000+00:00
Finished (UTC): 2026-09-21T03:53:35.253+00:00
Run fingerprint (SHA-256): `f4ff5b809c922f7de0763582ba899a95883c56c2b5d6850ed1f435f7cf2dd927`
Elapsed (wall clock): 3390.34 seconds
Chart testing: 3302.63 seconds
Dependency preparation: 85.70 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: interrupted
Discovery complete: True
Unstarted charts: 104

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

8 time-limit; 2 failed; 1 interrupted; 104 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: [HH2006](#hh2006---opaque-object-schema)

## Errors

14 distinct diagnostics across 14 occurrences; 0 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### [bitnami/airflow](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/airflow>)

Overview cell: 01

Status: time-limit | Attempts: 41

Audit findings: 1190. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.existingSecret`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.fernetKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.password`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0000>)

### [bitnami/apache](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apache>)

Overview cell: 02

Status: failed | Attempts: 45

Audit findings: 245. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.enabled`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 239 additional audit findings in JSON.

#### E001 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... ity': None, 'podAntiAffinity': {'preferredDuringSchedulingIgnoredDuringExecution':
[{'podAffinityTerm': {'labelSelector': {'matchLabels': {'app.kubernetes.io/instance': 'hypothesis', 'app.kubernetes.io/name': 'apache'}},
'topologyKey': 'kubernetes.io/hostname'}, 'weight': 1}]}, 'nodeAffinity': None}") in "<unicode string>", line 268, column 7: affinity: ^
(line: 268) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[*].preference | Status: failed

Changed overrides (used together):
- `$.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution.__hypothesis_key__.preference = {}`
Absent from overrides: $.extraPodSpec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution["*"].preference. Defaults may
still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/f9f902f5f6531d89a05d/report.json>)

#### E002 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... bash\n\n. /opt/bitnami/scripts/libfs.sh\n# We copy the logs folder because it has
symlinks to stdout and stderr\nif ! is_dir_empty /opt/bitnami/apache/logs; then\n cp -r /opt/bitnami/apache/logs
/emptydir/app-logs-dir\nfi\n'], 'volumeMounts': [{'name': 'empty-dir', 'mountPath': '/emptydir'}]}]") in "<unicode string>", line 268,
column 7: initContainers: ^ (line: 268) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.extraPodSpec.initContainers[*].envFrom[*].configMapRef.name | Status: failed

Changed overrides (used together):
- `$.extraPodSpec.initContainers.__hypothesis_key__.envFrom.__hypothesis_key__.configMapRef.name = null`
Absent from overrides: $.extraPodSpec.initContainers["*"].envFrom["*"].configMapRef.name. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/841e430e1fc6dd3d3813/report.json>)

#### E003 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... bash\n\n. /opt/bitnami/scripts/libfs.sh\n# We copy the logs folder because it has
symlinks to stdout and stderr\nif ! is_dir_empty /opt/bitnami/apache/logs; then\n cp -r /opt/bitnami/apache/logs
/emptydir/app-logs-dir\nfi\n'], 'volumeMounts': [{'name': 'empty-dir', 'mountPath': '/emptydir'}]}]") in "<unicode string>", line 268,
column 7: initContainers: ^ (line: 268) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.extraPodSpec.initContainers[*].lifecycle.preStop.httpGet.host | Status: failed

Changed overrides (used together):
- `$.extraPodSpec.initContainers.__hypothesis_key__.lifecycle.preStop.httpGet.host = null`
Absent from overrides: $.extraPodSpec.initContainers["*"].lifecycle.preStop.httpGet.host. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/2dd9691d68a24b9508d7/report.json>)

#### E004 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ... g in "<unicode string>", line 127, column 7: automountServiceAccountToken: false ^ (line:
127) found duplicate key "volumes" with value "{'__hypothesis_key__': {'projected': {'sources': {'__hypothesis_key__': {'configMap':
{'name': None}}}}}}" (original value: "[{'name': 'empty-dir', 'emptyDir': {}}]") in "<unicode string>", line 268, column 7: volumes: ^
(line: 268) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.extraPodSpec.volumes[*].projected.sources[*].configMap.name | Status: failed

Changed overrides (used together):
- `$.extraPodSpec.volumes.__hypothesis_key__.projected.sources.__hypothesis_key__.configMap.name = null`
Absent from overrides: $.extraPodSpec.volumes["*"].projected.sources["*"].configMap.name. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/4b92694ee19913118205/report.json>)

#### E006

```text
[Diagnostic shortened; full text in artifacts] ... ing'}, '$defs': {'type': 'object', 'additionalProperties': {'$dynamicRef': '#meta'}}},
'$defs': {'anchorString': {'type': 'string', 'pattern': '^[A-Za-z_][-A-Za-z0-9._]*$'}, 'uriString': {'type': 'string', 'format': 'uri'},
'uriReferenceString': {'type': 'string', 'format': 'uri-reference'}}} On schema['allOf'][87]['properties']['extraVolumes']['items']:
[{'properties': {'configMap': {'const': None}}, 'required': ['configMap'], 'type': 'object'}]
```

Phase: $.extraVolumes[*].configMap | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.extraVolumes["*"].configMap. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/cc5529fbbf92a7fdaf55/report.json>)

#### E007

```text
[Diagnostic shortened; full text in artifacts] ... [87]['properties']['initContainers']['items']: [{'properties': {'env': {'properties':
{'__hypothesis_key__': {'properties': {'valueFrom': {'properties': {'fieldRef': {'properties': {'apiVersion': {'const': None}}, 'required':
['apiVersion'], 'type': 'object'}}, 'required': ['fieldRef'], 'type': 'object'}}, 'required': ['valueFrom'], 'type': 'object'}}, 'required':
['__hypothesis_key__'], 'type': 'object'}}, 'required': ['env'], 'type': 'object'}]
```

Phase: $.initContainers[*].env[*].valueFrom.fieldRef.apiVersion | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.initContainers["*"].env["*"].valueFrom.fieldRef.apiVersion. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/195c3729323762c13f6e/report.json>)

#### E008

```text
[Diagnostic shortened; full text in artifacts] ... g': {'type': 'string', 'format': 'uri-reference'}}} On
schema['allOf'][87]['properties']['initContainers']['items']: [{'properties': {'env': {'properties': {'__hypothesis_key__': {'properties':
{'valueFrom': {'properties': {'secretKeyRef': {'const': None}}, 'required': ['secretKeyRef'], 'type': 'object'}}, 'required': ['valueFrom'],
'type': 'object'}}, 'required': ['__hypothesis_key__'], 'type': 'object'}}, 'required': ['env'], 'type': 'object'}]
```

Phase: $.initContainers[*].env[*].valueFrom.secretKeyRef | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.initContainers["*"].env["*"].valueFrom.secretKeyRef. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/b637fcd9a4553ad4343e/report.json>)

#### E009

```text
[Diagnostic shortened; full text in artifacts] ... es']['items']: [{'properties': {'ephemeral': {'properties': {'volumeClaimTemplate':
{'properties': {'metadata': {'properties': {'finalizers': {'properties': {'__hypothesis_key__': {'const': None}}, 'required':
['__hypothesis_key__'], 'type': 'object'}}, 'required': ['finalizers'], 'type': 'object'}}, 'required': ['metadata'], 'type': 'object'}},
'required': ['volumeClaimTemplate'], 'type': 'object'}}, 'required': ['ephemeral'], 'type': 'object'}]
```

Phase: $.extraVolumes[*].ephemeral.volumeClaimTemplate.metadata.finalizers[*] | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.extraVolumes["*"].ephemeral.volumeClaimTemplate.metadata.finalizers["*"]. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/84b7cbef4727fbe2b5ed/report.json>)

#### E010

```text
[Diagnostic shortened; full text in artifacts] ... : {'type': 'object', 'additionalProperties': {'$dynamicRef': '#meta'}}}, '$defs':
{'anchorString': {'type': 'string', 'pattern': '^[A-Za-z_][-A-Za-z0-9._]*$'}, 'uriString': {'type': 'string', 'format': 'uri'},
'uriReferenceString': {'type': 'string', 'format': 'uri-reference'}}} On schema['allOf'][87]['properties']['initContainers']['items']:
[{'properties': {'imagePullPolicy': {'const': None}}, 'required': ['imagePullPolicy'], 'type': 'object'}]
```

Phase: $.initContainers[*].imagePullPolicy | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.initContainers["*"].imagePullPolicy. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/fb2ffabaed483f0be9db/report.json>)

#### E011

```text
[Diagnostic shortened; full text in artifacts] ... tring': {'type': 'string', 'format': 'uri-reference'}}} On
schema['allOf'][87]['properties']['initContainers']['items']: [{'properties': {'resources': {'properties': {'claims': {'properties':
{'__hypothesis_key__': {'properties': {'request': {'const': None}}, 'required': ['request'], 'type': 'object'}}, 'required':
['__hypothesis_key__'], 'type': 'object'}}, 'required': ['claims'], 'type': 'object'}}, 'required': ['resources'], 'type': 'object'}]
```

Phase: $.initContainers[*].resources.claims[*].request | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.initContainers["*"].resources.claims["*"].request. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/5e0d1ac851d13111f0bc/report.json>)

#### E012

```text
[Diagnostic shortened; full text in artifacts] ... ring': {'type': 'string', 'format': 'uri'}, 'uriReferenceString': {'type': 'string',
'format': 'uri-reference'}}} On schema['allOf'][87]['properties']['initContainers']['items']: [{'properties': {'securityContext':
{'properties': {'windowsOptions': {'properties': {'hostProcess': {'const': None}}, 'required': ['hostProcess'], 'type': 'object'}},
'required': ['windowsOptions'], 'type': 'object'}}, 'required': ['securityContext'], 'type': 'object'}]
```

Phase: $.initContainers[*].securityContext.windowsOptions.hostProcess | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.initContainers["*"].securityContext.windowsOptions.hostProcess. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/459a1fa1201a37f10093/report.json>)

#### E013

```text
[Diagnostic shortened; full text in artifacts] ... $defs': {'anchorString': {'type': 'string', 'pattern': '^[A-Za-z_][-A-Za-z0-9._]*$'},
'uriString': {'type': 'string', 'format': 'uri'}, 'uriReferenceString': {'type': 'string', 'format': 'uri-reference'}}} On
schema['allOf'][87]['properties']['extraEnvVars']['items']: [{'properties': {'valueFrom': {'properties': {'configMapKeyRef': {'const':
None}}, 'required': ['configMapKeyRef'], 'type': 'object'}}, 'required': ['valueFrom'], 'type': 'object'}]
```

Phase: $.extraEnvVars[*].valueFrom.configMapKeyRef | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.extraEnvVars["*"].valueFrom.configMapKeyRef. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/50595b7a670999624853/report.json>)

#### E014

```text
[Diagnostic shortened; full text in artifacts] ... '}, 'uriString': {'type': 'string', 'format': 'uri'}, 'uriReferenceString': {'type':
'string', 'format': 'uri-reference'}}} On schema['allOf'][87]['properties']['sidecars']['items']: [{'properties': {'volumeMounts':
{'properties': {'__hypothesis_key__': {'properties': {'readOnly': {'const': None}}, 'required': ['readOnly'], 'type': 'object'}},
'required': ['__hypothesis_key__'], 'type': 'object'}}, 'required': ['volumeMounts'], 'type': 'object'}]
```

Phase: $.sidecars[*].volumeMounts[*].readOnly | Status: generation-error

Changed overrides (used together):
- No changed overrides.
Absent from overrides: $.sidecars["*"].volumeMounts["*"].readOnly. Defaults may still apply.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0001/paths/4228d4239dad6ef1fafa/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0001>)

### [bitnami/apisix](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/apisix>)

Overview cell: 03

Status: time-limit | Attempts: 11

Audit findings: 344. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2002](#hh2002---unspecified-values-type) at `$.controlPlane.args[*]`: Unspecified values type (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controlPlane.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.hpa`: Missing values description (info)
- [HH2003](#hh2003---missing-values-description) at `$.controlPlane.autoscaling.vpa`: Missing values description (info)
- 338 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0002>)

### [bitnami/appsmith](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/appsmith>)

Overview cell: 04

Status: time-limit | Attempts: 24

Audit findings: 543. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminEmail`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminPassword`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.adminUser`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.backend.automountServiceAccountToken`: Undocumented values path (warning)
- 537 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0003>)

### [bitnami/argo-cd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-cd>)

Overview cell: 05

Status: time-limit | Attempts: 21

Audit findings: 1251. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterAdminAccess`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.clusterRoleRules`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.command`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.applicationSet.containerPorts`: Undocumented values path (warning)
- 1245 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0004>)

### [bitnami/argo-workflows](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/argo-workflows>)

Overview cell: 06

Status: failed | Attempts: 68

Audit findings: 452. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.clusterDomain`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonAnnotations`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.commonLabels`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.args`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.controller.automountServiceAccountToken`: Undocumented values path (warning)
- 446 additional audit findings in JSON.

#### E005 ([HH1101](#hh1101---invalid-yaml-in-rendered-output))

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[Diagnostic shortened; full text in artifacts] ...  a mapping in "<unicode string>", line 1511, column 7: securityContext: ^ (line: 1511)
found duplicate key "securityContext" with value "{'fsGroup': 1001, 'fsGroupChangePolicy': 'Always', 'supplementalGroups': [], 'sysctls':
[]}" (original value: "{'windowsOptions': {'runAsUserName': None}}") in "<unicode string>", line 1531, column 7: securityContext: ^ (line:
1531) To suppress this check see: https://yaml.dev/doc/ruamel.yaml/api/#Duplicate_keys
```

Phase: $.mysql.primary.extraPodSpec.securityContext.windowsOptions.runAsUserName | Status: failed

Changed overrides (used together):
- `$.mysql.enabled = true (was false)`
- `$.mysql.primary.extraPodSpec.securityContext.windowsOptions.runAsUserName = null`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789959424/0005/paths/a11d0d0528bfd4989a4c/report.json>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0005>)

### [bitnami/aspnet-core](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/aspnet-core>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0006>)

### [bitnami/cadvisor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cadvisor>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0007>)

### [bitnami/cassandra](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cassandra>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0008>)

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

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0009>)

### [bitnami/chainloop](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/chainloop>)

Overview cell: 11

Status: interrupted | Attempts: 1

Audit findings: 643. Full paths and template references are retained in the JSON report.

- [HH2001](#hh2001---undocumented-values-path) at `$.apiVersions`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.affinity`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.automountServiceAccountToken`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa`: Undocumented values path (warning)
- [HH2001](#hh2001---undocumented-values-path) at `$.cas.autoscaling.hpa.enabled`: Undocumented values path (warning)
- 637 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789959424/0010>)

### [bitnami/cilium](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cilium>)

Overview cell: 12

Status: pending | Attempts: N/A

### [bitnami/clickhouse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse>)

Overview cell: 13

Status: pending | Attempts: N/A

### [bitnami/clickhouse-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/clickhouse-operator>)

Overview cell: 14

Status: pending | Attempts: N/A

### [bitnami/cloudnative-pg](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/cloudnative-pg>)

Overview cell: 15

Status: pending | Attempts: N/A

### [bitnami/common](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/common>)

Overview cell: 16

Status: pending | Attempts: N/A

### [bitnami/concourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/concourse>)

Overview cell: 17

Status: pending | Attempts: N/A

### [bitnami/consul](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/consul>)

Overview cell: 18

Status: pending | Attempts: N/A

### [bitnami/contour](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/contour>)

Overview cell: 19

Status: pending | Attempts: N/A

### [bitnami/deepspeed](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/deepspeed>)

Overview cell: 20

Status: pending | Attempts: N/A

### [bitnami/discourse](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/discourse>)

Overview cell: 21

Status: pending | Attempts: N/A

### [bitnami/dremio](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/dremio>)

Overview cell: 22

Status: pending | Attempts: N/A

### [bitnami/drupal](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/drupal>)

Overview cell: 23

Status: pending | Attempts: N/A

### [bitnami/ejbca](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ejbca>)

Overview cell: 24

Status: pending | Attempts: N/A

### [bitnami/elasticsearch](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/elasticsearch>)

Overview cell: 25

Status: pending | Attempts: N/A

### [bitnami/envoy-gateway](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/envoy-gateway>)

Overview cell: 26

Status: pending | Attempts: N/A

### [bitnami/etcd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/etcd>)

Overview cell: 27

Status: pending | Attempts: N/A

### [bitnami/external-dns](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/external-dns>)

Overview cell: 28

Status: pending | Attempts: N/A

### [bitnami/flink](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flink>)

Overview cell: 29

Status: pending | Attempts: N/A

### [bitnami/fluent-bit](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluent-bit>)

Overview cell: 30

Status: pending | Attempts: N/A

### [bitnami/fluentd](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/fluentd>)

Overview cell: 31

Status: pending | Attempts: N/A

### [bitnami/flux](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/flux>)

Overview cell: 32

Status: pending | Attempts: N/A

### [bitnami/ghost](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/ghost>)

Overview cell: 33

Status: pending | Attempts: N/A

### [bitnami/gitea](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitea>)

Overview cell: 34

Status: pending | Attempts: N/A

### [bitnami/gitlab-runner](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/gitlab-runner>)

Overview cell: 35

Status: pending | Attempts: N/A

### [bitnami/grafana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana>)

Overview cell: 36

Status: pending | Attempts: N/A

### [bitnami/grafana-alloy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-alloy>)

Overview cell: 37

Status: pending | Attempts: N/A

### [bitnami/grafana-k6-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-k6-operator>)

Overview cell: 38

Status: pending | Attempts: N/A

### [bitnami/grafana-loki](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-loki>)

Overview cell: 39

Status: pending | Attempts: N/A

### [bitnami/grafana-mimir](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-mimir>)

Overview cell: 40

Status: pending | Attempts: N/A

### [bitnami/grafana-operator](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-operator>)

Overview cell: 41

Status: pending | Attempts: N/A

### [bitnami/grafana-tempo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/grafana-tempo>)

Overview cell: 42

Status: pending | Attempts: N/A

### [bitnami/haproxy](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/haproxy>)

Overview cell: 43

Status: pending | Attempts: N/A

### [bitnami/harbor](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/harbor>)

Overview cell: 44

Status: pending | Attempts: N/A

### [bitnami/influxdb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/influxdb>)

Overview cell: 45

Status: pending | Attempts: N/A

### [bitnami/jaeger](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jaeger>)

Overview cell: 46

Status: pending | Attempts: N/A

### [bitnami/janusgraph](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/janusgraph>)

Overview cell: 47

Status: pending | Attempts: N/A

### [bitnami/jenkins](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jenkins>)

Overview cell: 48

Status: pending | Attempts: N/A

### [bitnami/jupyterhub](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/jupyterhub>)

Overview cell: 49

Status: pending | Attempts: N/A

### [bitnami/kafka](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kafka>)

Overview cell: 50

Status: pending | Attempts: N/A

### [bitnami/keycloak](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keycloak>)

Overview cell: 51

Status: pending | Attempts: N/A

### [bitnami/keydb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/keydb>)

Overview cell: 52

Status: pending | Attempts: N/A

### [bitnami/kibana](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kibana>)

Overview cell: 53

Status: pending | Attempts: N/A

### [bitnami/kong](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kong>)

Overview cell: 54

Status: pending | Attempts: N/A

### [bitnami/kube-arangodb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-arangodb>)

Overview cell: 55

Status: pending | Attempts: N/A

### [bitnami/kube-prometheus](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus>)

Overview cell: 56

Status: pending | Attempts: N/A

### [bitnami/kube-prometheus/charts/kube-prometheus-crds](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-prometheus/charts/kube-prometheus-crds>)

Overview cell: 57

Status: pending | Attempts: N/A

### [bitnami/kube-state-metrics](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kube-state-metrics>)

Overview cell: 58

Status: pending | Attempts: N/A

### [bitnami/kuberay](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kuberay>)

Overview cell: 59

Status: pending | Attempts: N/A

### [bitnami/kubernetes-event-exporter](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/kubernetes-event-exporter>)

Overview cell: 60

Status: pending | Attempts: N/A

### [bitnami/logstash](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/logstash>)

Overview cell: 61

Status: pending | Attempts: N/A

### [bitnami/mariadb](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb>)

Overview cell: 62

Status: pending | Attempts: N/A

### [bitnami/mariadb-galera](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mariadb-galera>)

Overview cell: 63

Status: pending | Attempts: N/A

### [bitnami/mastodon](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/mastodon>)

Overview cell: 64

Status: pending | Attempts: N/A

### [bitnami/matomo](<https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami/matomo>)

Overview cell: 65

Status: pending | Attempts: N/A

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
