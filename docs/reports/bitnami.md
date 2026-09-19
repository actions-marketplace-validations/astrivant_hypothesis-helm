# Local Helm chart tests

<!-- toc:start -->
<details>
<summary>Table of contents</summary>

- [Overview](#overview)
- [Scan summary](#scan-summary)
- [Status counts](#status-counts)
- [Settings](#settings)
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
Started (Unix epoch): 1789843116
Elapsed (wall clock): 81.24 seconds
Chart testing: 73.10 seconds
Dependency preparation: 7.28 seconds (excluded from testing budgets)
Charts discovered: 115
Scan status: interrupted
Discovery complete: True
Unstarted charts: 114

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

1 interrupted; 114 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: HH2006

## Charts

### bitnami/airflow

Overview cell: 01

Status: interrupted | Attempts: 43

Audit findings: 1282. Full paths and template references are retained in the JSON report.

- `HH2001` at `$[*][*]`: Undocumented values path
- `HH2004` at `$[*][*]`: No supplied default for a values path
- `HH2001` at `$[*][*][*]`: Undocumented values path
- `HH2004` at `$[*][*][*]`: No supplied default for a values path
- `HH2001` at `$[*][*][*][*]`: Undocumented values path
- `HH2004` at `$[*][*][*][*]`: No supplied default for a values path
- 1276 additional audit findings in JSON.

[Chart artifacts](<bitnami-runs/bitnami-charts_1789843116/0000>)

### bitnami/apache

Overview cell: 02

Status: pending | Attempts: N/A

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
