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
  - [charts/alertmanager](#chartsalertmanager)
  - [charts/alertmanager-snmp-notifier](#chartsalertmanager-snmp-notifier)
  - [charts/jiralert](#chartsjiralert)
  - [charts/kube-prometheus-stack](#chartskube-prometheus-stack)
  - [charts/kube-prometheus-stack/charts/crds](#chartskube-prometheus-stackchartscrds)
  - [charts/kube-state-metrics](#chartskube-state-metrics)
  - [charts/prom-label-proxy](#chartsprom-label-proxy)
  - [charts/prometheus](#chartsprometheus)
  - [charts/prometheus-adapter](#chartsprometheus-adapter)
  - [charts/prometheus-blackbox-exporter](#chartsprometheus-blackbox-exporter)
  - [charts/prometheus-cloudwatch-exporter](#chartsprometheus-cloudwatch-exporter)
  - [charts/prometheus-conntrack-stats-exporter](#chartsprometheus-conntrack-stats-exporter)
  - [charts/prometheus-consul-exporter](#chartsprometheus-consul-exporter)
  - [charts/prometheus-couchdb-exporter](#chartsprometheus-couchdb-exporter)
  - [charts/prometheus-druid-exporter](#chartsprometheus-druid-exporter)
  - [charts/prometheus-elasticsearch-exporter](#chartsprometheus-elasticsearch-exporter)
  - [charts/prometheus-fastly-exporter](#chartsprometheus-fastly-exporter)
  - [charts/prometheus-ipmi-exporter](#chartsprometheus-ipmi-exporter)
  - [charts/prometheus-json-exporter](#chartsprometheus-json-exporter)
  - [charts/prometheus-kafka-exporter](#chartsprometheus-kafka-exporter)
  - [charts/prometheus-memcached-exporter](#chartsprometheus-memcached-exporter)
  - [charts/prometheus-modbus-exporter](#chartsprometheus-modbus-exporter)
  - [charts/prometheus-mongodb-exporter](#chartsprometheus-mongodb-exporter)
  - [charts/prometheus-mysql-exporter](#chartsprometheus-mysql-exporter)
  - [charts/prometheus-nats-exporter](#chartsprometheus-nats-exporter)
  - [charts/prometheus-nginx-exporter](#chartsprometheus-nginx-exporter)
  - [charts/prometheus-node-exporter](#chartsprometheus-node-exporter)
  - [charts/prometheus-operator-admission-webhook](#chartsprometheus-operator-admission-webhook)
  - [charts/prometheus-operator-crds](#chartsprometheus-operator-crds)
  - [charts/prometheus-operator-crds/charts/crds](#chartsprometheus-operator-crdschartscrds)
  - [charts/prometheus-pgbouncer-exporter](#chartsprometheus-pgbouncer-exporter)
  - [charts/prometheus-pingdom-exporter](#chartsprometheus-pingdom-exporter)
  - [charts/prometheus-pingmesh-exporter](#chartsprometheus-pingmesh-exporter)
  - [charts/prometheus-postgres-exporter](#chartsprometheus-postgres-exporter)
  - [charts/prometheus-pushgateway](#chartsprometheus-pushgateway)
  - [charts/prometheus-rabbitmq-exporter](#chartsprometheus-rabbitmq-exporter)
  - [charts/prometheus-redis-exporter](#chartsprometheus-redis-exporter)
  - [charts/prometheus-smartctl-exporter](#chartsprometheus-smartctl-exporter)
  - [charts/prometheus-snmp-exporter](#chartsprometheus-snmp-exporter)
  - [charts/prometheus-sql-exporter](#chartsprometheus-sql-exporter)
  - [charts/prometheus-stackdriver-exporter](#chartsprometheus-stackdriver-exporter)
  - [charts/prometheus-statsd-exporter](#chartsprometheus-statsd-exporter)
  - [charts/prometheus-systemd-exporter](#chartsprometheus-systemd-exporter)
  - [charts/prometheus-to-sd](#chartsprometheus-to-sd)
  - [charts/prometheus-windows-exporter](#chartsprometheus-windows-exporter)
  - [charts/prometheus-yet-another-cloudwatch-exporter](#chartsprometheus-yet-another-cloudwatch-exporter)

</details>
<!-- toc:end -->

## Overview

![Chart severity and scan-time matrices](<https://github.com/astrivant/hypothesis-helm/raw/main/docs/reports/prometheus-overview.png>)

Each cell is one chart; both grids follow chart-section order. Click a cell in the PDF for details. Colors show the highest observed finding
kind, not a security or business-impact score. Hatching marks unfinished or unavailable testing, even when a finding was recorded. No
findings means none in the completed sample, not exhaustive coverage. Testing time excludes dependency preparation.

## Scan summary

Git comparison: HEAD^ (b2c38cff79e9f432a6194223beb1b172e8b7667f); 0 cached chart successes reused.

Directory: /Users/emmadoyle/projects/personal/hypothesis-helm/third_party/prometheus-community-helm-charts
Started (Unix epoch): 1789747367
Elapsed (wall clock): 1.77 seconds
Chart testing: 1.38 seconds
Dependency preparation: 0.14 seconds (excluded from testing budgets)
Charts discovered: 46
Scan status: interrupted
Discovery complete: True
Unstarted charts: 44

Results record outcomes for the tested sample and selected checks.
Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.

## Status counts

1 error; 1 interrupted; 44 pending.

## Settings

Filtering: True | Seed: 0 | Traversal: random
Chart timeout: 300.0 seconds | Workers: not recorded
Complete settings are retained in the JSON report.

Generated values use the configured input domains and any supported destination constraints. Coverage excludes inputs outside these domains;
supplied defaults are tested unchanged. The JSON report records constraints and unresolved mappings.

Disabled checks: HH2006

## Errors

2 distinct diagnostics across 2 occurrences; 0 repeats grouped.
Diagnostics and their triggering inputs are grouped under each chart below.
Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.
Full inputs, diagnostics, and remaining cases are retained in local run data.
Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.

## Charts

### charts/alertmanager

Overview cell: 01

Status: error | Attempts: N/A

#### E002

```text
recursive schema at ('config', 'route', 'routes', '*')
```

Phase: chart | Status: error

No triggering values were recorded for this diagnostic.

### charts/alertmanager-snmp-notifier

Overview cell: 02

Status: interrupted | Attempts: N/A

#### E001

```text
Interrupted by user
```

Phase: chart | Status: interrupted

No triggering values were recorded for this diagnostic.

### charts/jiralert

Overview cell: 03

Status: pending | Attempts: N/A

### charts/kube-prometheus-stack

Overview cell: 04

Status: pending | Attempts: N/A

### charts/kube-prometheus-stack/charts/crds

Overview cell: 05

Status: pending | Attempts: N/A

### charts/kube-state-metrics

Overview cell: 06

Status: pending | Attempts: N/A

### charts/prom-label-proxy

Overview cell: 07

Status: pending | Attempts: N/A

### charts/prometheus

Overview cell: 08

Status: pending | Attempts: N/A

### charts/prometheus-adapter

Overview cell: 09

Status: pending | Attempts: N/A

### charts/prometheus-blackbox-exporter

Overview cell: 10

Status: pending | Attempts: N/A

### charts/prometheus-cloudwatch-exporter

Overview cell: 11

Status: pending | Attempts: N/A

### charts/prometheus-conntrack-stats-exporter

Overview cell: 12

Status: pending | Attempts: N/A

### charts/prometheus-consul-exporter

Overview cell: 13

Status: pending | Attempts: N/A

### charts/prometheus-couchdb-exporter

Overview cell: 14

Status: pending | Attempts: N/A

### charts/prometheus-druid-exporter

Overview cell: 15

Status: pending | Attempts: N/A

### charts/prometheus-elasticsearch-exporter

Overview cell: 16

Status: pending | Attempts: N/A

### charts/prometheus-fastly-exporter

Overview cell: 17

Status: pending | Attempts: N/A

### charts/prometheus-ipmi-exporter

Overview cell: 18

Status: pending | Attempts: N/A

### charts/prometheus-json-exporter

Overview cell: 19

Status: pending | Attempts: N/A

### charts/prometheus-kafka-exporter

Overview cell: 20

Status: pending | Attempts: N/A

### charts/prometheus-memcached-exporter

Overview cell: 21

Status: pending | Attempts: N/A

### charts/prometheus-modbus-exporter

Overview cell: 22

Status: pending | Attempts: N/A

### charts/prometheus-mongodb-exporter

Overview cell: 23

Status: pending | Attempts: N/A

### charts/prometheus-mysql-exporter

Overview cell: 24

Status: pending | Attempts: N/A

### charts/prometheus-nats-exporter

Overview cell: 25

Status: pending | Attempts: N/A

### charts/prometheus-nginx-exporter

Overview cell: 26

Status: pending | Attempts: N/A

### charts/prometheus-node-exporter

Overview cell: 27

Status: pending | Attempts: N/A

### charts/prometheus-operator-admission-webhook

Overview cell: 28

Status: pending | Attempts: N/A

### charts/prometheus-operator-crds

Overview cell: 29

Status: pending | Attempts: N/A

### charts/prometheus-operator-crds/charts/crds

Overview cell: 30

Status: pending | Attempts: N/A

### charts/prometheus-pgbouncer-exporter

Overview cell: 31

Status: pending | Attempts: N/A

### charts/prometheus-pingdom-exporter

Overview cell: 32

Status: pending | Attempts: N/A

### charts/prometheus-pingmesh-exporter

Overview cell: 33

Status: pending | Attempts: N/A

### charts/prometheus-postgres-exporter

Overview cell: 34

Status: pending | Attempts: N/A

### charts/prometheus-pushgateway

Overview cell: 35

Status: pending | Attempts: N/A

### charts/prometheus-rabbitmq-exporter

Overview cell: 36

Status: pending | Attempts: N/A

### charts/prometheus-redis-exporter

Overview cell: 37

Status: pending | Attempts: N/A

### charts/prometheus-smartctl-exporter

Overview cell: 38

Status: pending | Attempts: N/A

### charts/prometheus-snmp-exporter

Overview cell: 39

Status: pending | Attempts: N/A

### charts/prometheus-sql-exporter

Overview cell: 40

Status: pending | Attempts: N/A

### charts/prometheus-stackdriver-exporter

Overview cell: 41

Status: pending | Attempts: N/A

### charts/prometheus-statsd-exporter

Overview cell: 42

Status: pending | Attempts: N/A

### charts/prometheus-systemd-exporter

Overview cell: 43

Status: pending | Attempts: N/A

### charts/prometheus-to-sd

Overview cell: 44

Status: pending | Attempts: N/A

### charts/prometheus-windows-exporter

Overview cell: 45

Status: pending | Attempts: N/A

### charts/prometheus-yet-another-cloudwatch-exporter

Overview cell: 46

Status: pending | Attempts: N/A
