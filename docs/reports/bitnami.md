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
Started (Unix epoch): 1789862984
Elapsed (wall clock): 603.13 seconds
Chart testing: 587.02 seconds
Dependency preparation: 15.25 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: interrupted
Discovery complete: True
Unstarted charts: 113

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

1 failed; 1 interrupted; 113 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: HH2006

## Errors

5 distinct diagnostics across 7 occurrences; 2 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### bitnami/airflow

Overview cell: 01

Status: failed | Attempts: 101

Audit findings: 1190. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.apiVersions`: Undocumented values path (warning)
- `HH2001` at `$.auth.existingSecret`: Undocumented values path (warning)
- `HH2001` at `$.auth.fernetKey`: Undocumented values path (warning)
- `HH2001` at `$.auth.jwtSecretKey`: Undocumented values path (warning)
- `HH2001` at `$.auth.password`: Undocumented values path (warning)
- `HH2001` at `$.auth.secretKey`: Undocumented values path (warning)
- 1184 additional audit findings in JSON.

#### E005 (HH1109)

**Invalid manifest field type** (manifest / violation). Severity: **error**. Check the field named in Helm's decoding error and constrain
its values to the required type.

```text
[HH1109] Error: YAML parse error on airflow/charts/redis/templates/headless-svc.yaml: error unmarshaling JSON: while decoding JSON: json:
cannot unmarshal array into Go struct field .metadata.annotations. of type string
```

Phase: $.redis.sentinel.service.headless | Status: failed

Changed overrides (used together):
- `$.redis.sentinel.service.headless.annotations[""] = [{"aaaa": [[null]], "a<": -60389, "a": [null]}]`
- `$.redis.sentinel.service.headless.annotations["+kQdBaTaE^>2a_x+aWr"]["aaaaaav;Daadaa"] = true`
- `$.redis.sentinel.service.headless.annotations["+kQdBaTaE^>2a_x+aWr"].aaaaaaaaJ = ["aa"]`
- `$.redis.sentinel.service.headless.annotations["aoaaoUQ+c}\"p"] = true`
- `$.redis.sentinel.service.headless.annotations[".aaa=n}ya=01me\"aEaa;Da'\rba"].relative_distance = {}`
- `$.redis.sentinel.service.headless.annotations[".aaa=n}ya=01me\"aEaa;Da'\rba"].aaaaa = [-15525, -177254, null]`
- 8 more paths; see full input.

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789862984/0000/paths/afbbf9ab6c6be5d414aa>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789862984/0000>)

### bitnami/apache

Overview cell: 02

Status: interrupted | Attempts: 601

Audit findings: 245. Full paths and template references are retained in the JSON report.

- `HH2001` at `$.affinity`: Undocumented values path (warning)
- `HH2001` at `$.args`: Undocumented values path (warning)
- `HH2001` at `$.automountServiceAccountToken`: Undocumented values path (warning)
- `HH2001` at `$.autoscaling.enabled`: Undocumented values path (warning)
- `HH2001` at `$.autoscaling.maxReplicas`: Undocumented values path (warning)
- `HH2001` at `$.autoscaling.minReplicas`: Undocumented values path (warning)
- 239 additional audit findings in JSON.

Configuration rejections: 0 excluded; 0 adjusted and tested; 0 Helm verification renders (separate from manifest-test attempts).

The template rejected inputs admitted by the declared values schema; these remain reported failures.

#### E001 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 179: found unexpected end of
stream
```

Phase: $.htdocsConfigMap | Status: failed

Changed overrides (used together):
- `$.htdocsConfigMap = "'" (was "")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789862984/0001/paths/a84b1abe3a11000d364a>)

#### E002 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 31: did not find expected
',' or ']'
```

Phase: $.image.pullSecrets | Status: failed

Changed overrides (used together):
- `$.image.pullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789862984/0001/paths/a4a0ea6ab697189bb963>)

Phase: $.global.imagePullSecrets | Status: failed

Changed overrides (used together):
- `$.global.imagePullSecrets = [[null, []]]`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789862984/0001/paths/097f6358a00dddbcdd83>)

1 additional occurrences are retained in the JSON report and chart artifacts.

#### E003 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/deployment.yaml: error converting YAML to JSON: yaml: line 62: mapping values are not
allowed in this context
```

Phase: $.image | Status: failed

Changed overrides (used together):
- `$.image.tag = "" (was "2.4.65-debian-12-r2")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789862984/0001/paths/8e79b7dd85a286cfaddb>)

#### E004 (HH1101)

**Invalid YAML in rendered output** (manifest / violation). Severity: **error**. Inspect the failing YAML and template interpolation,
including quoting and indentation.

```text
[HH1101] Error: YAML parse error on apache/templates/svc.yaml: error converting YAML to JSON: yaml: line 26: found unexpected end of stream
```

Phase: $.service.type | Status: failed

Changed overrides (used together):
- `$.service.type = "'" (was "LoadBalancer")`

[Full input and diagnostic](<bitnami-runs/bitnami-charts_1789862984/0001/paths/6e931799d09f8182f34b>)

[Chart artifacts](<bitnami-runs/bitnami-charts_1789862984/0001>)

### bitnami/apisix

Overview cell: 03

Status: pending | Attempts: N/A

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
