## [Main title](../README.md)
### [Interview questions](full.md)

# Data Observability

Data observability is the practice of monitoring, alerting, and diagnosing the health of data and data pipelines. It focuses on whether datasets arrive on time, with the expected volume and values, and whether downstream consumers can trust them. Application monitoring tells you the job succeeded; data observability tells you the data is right.

The discipline is organized around five pillars: **freshness**, **volume**, **schema**, **quality**, and **lineage**. A useful framing for interviews is that observability is *metrics + logs + lineage + tests, joined by a common dataset and run identifier*.

+ [What is data observability?](#What-is-data-observability)
+ [What signals should you monitor for a data pipeline?](#What-signals-should-you-monitor-for-a-data-pipeline)
+ [How do you reduce noisy data alerts?](#How-do-you-reduce-noisy-data-alerts)
+ [How is data observability different from application observability?](#How-is-data-observability-different-from-application-observability)
+ [What are the key signals you monitor for data pipelines?](#What-are-the-key-signals-you-monitor-for-data-pipelines)
+ [How do you define and measure an end-to-end SLA for data?](#How-do-you-define-and-measure-an-end-to-end-SLA-for-data)
+ [What should you log for each pipeline run?](#What-should-you-log-for-each-pipeline-run)
+ [How do you detect silent failures?](#How-do-you-detect-silent-failures)
+ [What is lineage and how does it help during incidents?](#What-is-lineage-and-how-does-it-help-during-incidents)
+ [How do you monitor and debug a broken metric in BI?](#How-do-you-monitor-and-debug-a-broken-metric-in-BI)
+ [How do you design alerts to avoid alert fatigue?](#How-do-you-design-alerts-to-avoid-alert-fatigue)
+ [How do you approach backfills safely?](#How-do-you-approach-backfills-safely)
+ [What is a runbook and what should it contain?](#What-is-a-runbook-and-what-should-it-contain)
+ [What are common incident patterns in data platforms?](#What-are-common-incident-patterns-in-data-platforms)
+ [Real world use cases for Data Observability](#Real-world-use-cases-for-Data-Observability)

## What is data observability?

Data observability is the practice of monitoring, alerting, and diagnosing the health of data and data pipelines. It focuses on whether datasets are arriving on time, with correct volume and values, and whether downstream consumers can rely on them. The goal is to reduce "data downtime" and speed up root-cause analysis.

The minimum viable implementation is a control table that every run writes to, so any run can be reconstructed months later:

```sql
CREATE TABLE IF NOT EXISTS platform.pipeline_runs (
    run_id        STRING,
    pipeline      STRING,
    dataset       STRING,
    logical_date  DATE,
    started_at    TIMESTAMP,
    finished_at   TIMESTAMP,
    status        STRING,        -- success | failed | quarantined
    rows_read     BIGINT,
    rows_written  BIGINT,
    bytes_scanned BIGINT,
    error_message STRING,
    code_version  STRING
);

-- Freshness and volume for the latest run of each dataset
SELECT
    dataset,
    MAX(finished_at) AS last_success,
    SUM(rows_written) AS rows_today
FROM platform.pipeline_runs
WHERE logical_date = CURRENT_DATE() AND status = 'success'
GROUP BY dataset
ORDER BY last_success ASC;
```

Commercial tools (Monte Carlo, Bigeye, Soda, Elementary) automate the same checks; open-source stacks do it with dbt tests, Great Expectations, OpenLineage, and Prometheus. The tool matters less than having an owner, an SLA, and a runbook per critical dataset.

[Table of Contents](#Data-Observability)

## What signals should you monitor for a data pipeline?

Monitor freshness, volume, schema, quality, latency, cost, and failure rate. Infrastructure metrics are useful, but data-specific signals catch silent failures that compute metrics miss.

| Signal | Question it answers | Typical source |
|---|---|---|
| Freshness | Is the newest partition recent enough? | max(event_ts) vs SLA |
| Volume | Did row counts stay in range? | count(*) per partition |
| Schema | Did columns or types change? | information_schema diff |
| Quality | Are values valid and unique? | dbt tests, GE, SQL checks |
| Latency | How long from event to availability? | event_ts vs publish_ts |
| Reliability | Did the job fail, retry, or run late? | orchestrator metadata |

Expose these as time series so you can alert on trend, not just pass/fail:

```yaml
# prometheus/rules/data_pipeline.yml
groups:
  - name: data-pipeline
    rules:
      - alert: DatasetStale
        expr: time() - pipeline_last_success_timestamp_seconds > 7200
        for: 10m
        labels: {severity: page, team: data-platform}
        annotations:
          summary: "{{ $labels.dataset }} is more than 2h stale"
          runbook_url: "https://runbooks.acme.io/dataset-stale"
```

Emit the gauges from the pipeline itself or from an exporter that queries the control table, so alerts do not depend on someone reading a dashboard.

[Table of Contents](#Data-Observability)

## How do you reduce noisy data alerts?

Make alerts actionable and severity-based. Use thresholds with context, anomaly detection where useful, and alert only when a user-facing SLA or critical data contract is at risk. Non-critical checks can go to dashboards or daily reports.

```text
page:      gold revenue table is stale past 8 AM SLA
ticket:    staging null rate increased but downstream mart is unaffected
dashboard: row count changed within expected seasonality
```

Map every rule to one of three tiers and route it accordingly:

+ **page** - consumer-visible, SLA-breaching, one owner, runbook required.
+ **ticket** - real defect with a slower clock, no immediate user impact.
+ **dashboard-only** - informational; reviewed weekly, never wakes anyone.

In Prometheus, severity plus inhibition suppresses the downstream blast radius so one root cause produces one page:

```yaml
# prometheus/rules/inhibit.yml
inhibit_rules:
  - source_matchers: [severity="page", alertname="SourceFeedMissing"]
    target_matchers: [severity="page", alertname=~"DatasetStale|VolumeAnomaly"]
    equal: [domain]
```

A check that has never fired, or always fires and is ignored, should be deleted or downgraded. Noisy alerts train teams to ignore the system, so alert design is part of reliability.

[Table of Contents](#Data-Observability)

## How is data observability different from application observability?

Application observability focuses on service health (latency, error rates, traces) for request/response systems. Data observability focuses on dataset health and pipeline behavior over time (freshness, completeness, distribution shifts). Data issues can be silent, delayed, and cumulative, so you need different signals and baselines.

| Dimension | Application observability | Data observability |
|---|---|---|
| Unit of health | request / endpoint / pod | dataset / partition / column |
| Primary signals | latency, error rate, saturation | freshness, volume, schema, drift |
| Failure shape | usually loud and immediate | often silent until a metric drifts |
| Time horizon | seconds to minutes | hours to weeks (batch, seasonality) |
| "Correct" means | 200 OK, no exception | matches source and business rule |
| Tooling | Prometheus, Grafana, OTel | dbt tests, GE, Soda, OpenLineage |

They share plumbing: OpenTelemetry spans can carry the dataset and run id so one trace covers "task started -> file read -> table written":

```python
# Emitting a data-aware span from a pipeline task
from opentelemetry import trace

tracer = trace.get_tracer("acme.pipelines")


def load(ds: str, path: str) -> int:
    with tracer.start_as_current_span("load_orders") as span:
        span.set_attribute("data.dataset", "curated.orders")
        span.set_attribute("data.partition", ds)
        rows = write_parquet(path, ds)
        span.set_attribute("data.rows_written", rows)
        return rows
```

The key interview point: **a green pipeline run is not evidence that the data is right.** You need dataset-level assertions on top of task-level success.

[Table of Contents](#Data-Observability)

## What are the key signals you monitor for data pipelines?

Common signals include:

+ freshness (max event/ingestion time)
+ volume (row counts, bytes, partitions)
+ schema changes (added/removed/typed columns)
+ quality checks (null rates, uniqueness, referential integrity)
+ pipeline run status and duration
+ cost signals (query time, bytes scanned, cluster utilization)

For each one, define a threshold, an owner, and a query that can be run during an incident:

```sql
-- Freshness against a per-dataset SLA table, plus a volume comparison
WITH actual AS (
    SELECT 'curated.orders' AS dataset, MAX(updated_at) AS max_ts, COUNT(*) AS rows_today
    FROM curated.orders
    WHERE order_date = CURRENT_DATE() - 1
)
SELECT
    a.dataset,
    s.sla_minutes,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), a.max_ts, MINUTE) AS minutes_stale,
    a.rows_today,
    b.median_7d,
    SAFE_DIVIDE(a.rows_today, b.median_7d) AS volume_ratio
FROM actual AS a
JOIN platform.dataset_slas AS s USING (dataset)
LEFT JOIN (
    SELECT APPROX_QUANTILES(rows, 2)[OFFSET(1)] AS median_7d
    FROM (
        SELECT order_date, COUNT(*) AS rows FROM curated.orders
        WHERE order_date BETWEEN CURRENT_DATE() - 8 AND CURRENT_DATE() - 1
        GROUP BY order_date
    )
) AS b ON TRUE
WHERE TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), a.max_ts, MINUTE) > s.sla_minutes
   OR SAFE_DIVIDE(a.rows_today, b.median_7d) NOT BETWEEN 0.7 AND 1.3;
```

Alert on **rate of change**, not absolute values: a 30% volume drop on a holiday means something different than on a normal Tuesday, so baseline by weekday and compare against a trailing window.

[Table of Contents](#Data-Observability)

## How do you define and measure an end-to-end SLA for data?

You define the SLA from source event time to availability in the final dataset or BI metric. Measure it with timestamps at each stage (ingest, transform, publish) and compute percentiles (p50/p95) as well as breach counts. SLAs should reflect consumer needs and include ownership and escalation paths.

```text
event_time -> ingested_at -> transformed_at -> published_at -> dashboard_refreshed_at
             (ingest lag)    (transform lag)   (publish lag)
```

```sql
WITH staged AS (
    SELECT
        event_time,
        published_at,
        TIMESTAMP_DIFF(ingested_at, event_time, SECOND)   AS ingest_lag_s,
        TIMESTAMP_DIFF(published_at, ingested_at, SECOND) AS transform_lag_s,
        TIMESTAMP_DIFF(published_at, event_time, SECOND)  AS e2e_lag_s
    FROM curated.orders
    WHERE order_date >= CURRENT_DATE() - 30
)
SELECT
    DATE(published_at) AS publish_date,
    APPROX_QUANTILES(e2e_lag_s, 100)[OFFSET(50)] AS p50_s,
    APPROX_QUANTILES(e2e_lag_s, 100)[OFFSET(95)] AS p95_s,
    COUNTIF(e2e_lag_s > 4 * 3600) AS breaches_over_4h,
    COUNT(*) AS total_rows
FROM staged
GROUP BY publish_date
ORDER BY publish_date DESC;
```

Express the SLA as a contract with an owner, for example "99% of `curated.orders` rows with `event_time` before 23:59 UTC are queryable by 06:00 UTC, owned by the Orders Data team." Prefer a freshness SLO with an **error budget** to a hard promise, and measure freshness per partition, because a table can look fresh by max timestamp while one region partition silently stopped loading.

[Table of Contents](#Data-Observability)

## What should you log for each pipeline run?

At minimum:

+ inputs (source tables/partitions, offsets, watermarks)
+ outputs (target tables/partitions, row counts written)
+ runtime and resource usage
+ warnings/errors and retry attempts
+ data quality results summary

This makes runs reproducible and speeds up debugging. Log structured JSON with a stable run id so logs can be joined to the control table and to traces:

```python
import json
import logging
import time
import uuid

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("orders")


def run(ds: str, source: str, target: str) -> None:
    run_id = str(uuid.uuid4())
    started = time.time()
    log.info(json.dumps({
        "event": "run_start", "run_id": run_id, "dataset": "curated.orders",
        "partition": ds, "source": source, "code_version": "orders@2.4.1",
    }))
    rows = transform_and_write(source, target)
    log.info(json.dumps({
        "event": "run_end", "run_id": run_id, "dataset": "curated.orders",
        "partition": ds, "rows_written": rows,
        "duration_s": round(time.time() - started, 2), "status": "success",
    }))
```

For Airflow, enable remote logging so lines carry DAG, task, run id, and try number:

```yaml
# airflow.cfg (excerpt)
[logging]
remote_logging = True
remote_log_conn_id = s3_logs
log_format = [%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s
```

Never log secrets or full PII payloads, always include the partition/logical date, and log a **redacted sample of rejected records** rather than only a count.

[Table of Contents](#Data-Observability)

## How do you detect silent failures?

Silent failures happen when the job succeeds but data is wrong (missing subset, wrong join, truncation). Detect them with dataset-level checks: freshness, volume bounds, distribution checks, and reconciliations against sources. Monitoring key business KPIs for unexpected changes is also effective.

The strongest signal is a reconciliation invariant that must hold regardless of seasonality:

```sql
-- Orders and payments must reconcile: equal counts and equal totals for the day
SELECT
    COUNT(DISTINCT o.order_id) AS order_ids,
    COUNT(DISTINCT p.order_id) AS paid_order_ids,
    SUM(o.amount) - SUM(p.amount) AS amount_delta
FROM curated.orders AS o
FULL OUTER JOIN curated.payments AS p USING (order_id)
WHERE COALESCE(o.order_date, p.order_date) = DATE '2026-10-04';
```

Also add a fan-out guard (`COUNT(*)` must equal `COUNT(DISTINCT order_id)` after a join) to catch a many-to-many join before it inflates revenue. In dbt, encode the invariants so they run on every build:

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: customer_id
        tests:
          - not_null
          - relationships: {to: ref('dim_customers'), field: customer_id}
      - name: status
        tests:
          - accepted_values: {values: ['placed', 'paid', 'shipped', 'cancelled']}
```

Other cheap catches: null-rate jumps versus the trailing average, unexpected enum values, string truncation, and missing partitions found by left-joining an expected calendar.

[Table of Contents](#Data-Observability)

## What is lineage and how does it help during incidents?

Lineage describes upstream/downstream dependencies between datasets, jobs, and dashboards. During incidents, lineage helps you assess blast radius (which reports are impacted) and prioritize fixes. It also helps prevent regressions by making dependencies explicit.

Three useful levels: **table-level** (blast radius), **column-level** (metric drift debugging), and **run-level** (which specific run wrote the bad partition, for scoping a backfill). OpenLineage emits lineage as a side effect of running jobs so it stays current:

```python
# Emit dataset lineage from a pipeline task
from openlineage.client import OpenLineageClient
from openlineage.client.run import Dataset, RunEvent, RunState

client = OpenLineageClient(url="http://marquez:5000")


def emit_complete(run_id: str, job: str, inputs: list[str], outputs: list[str]) -> None:
    client.emit(RunEvent(
        eventType=RunState.COMPLETE,
        eventTime="2026-10-04T06:12:00Z",
        run=run_id,
        job=job,
        inputs=[Dataset(namespace="s3://acme-raw", name=n) for n in inputs],
        outputs=[Dataset(namespace="snowflake://acme", name=n) for n in outputs],
    ))
```

During an incident, walk lineage **upstream from the broken dashboard** until the data is correct, then **downstream from the bad table** to list every affected metric and owner. The second walk is the difference between a 30-minute and a 4-hour incident.

[Table of Contents](#Data-Observability)

## How do you monitor and debug a broken metric in BI?

You start from the metric definition and trace dependencies to the underlying tables. Then check data freshness and recent changes (deploys, schema changes, upstream outages). Use reconciliation queries and sampling to locate where the metric diverged, then confirm whether it is a data issue or a definition change.

A repeatable order that avoids guesswork: confirm the report (dashboard vs extract vs warehouse), check freshness, check volume, bisect the transformation layer by layer, check recent deploys, then reconcile against an independent source.

```sql
-- Bisect: compute the metric at every layer and find the first divergence
SELECT 'raw.orders'    AS layer, COUNT(*) AS n, SUM(amount) AS revenue FROM raw.orders      WHERE order_date = DATE '2026-10-03'
UNION ALL
SELECT 'stg_orders'    AS layer, COUNT(*) AS n, SUM(amount) AS revenue FROM staging.stg_orders WHERE order_date = DATE '2026-10-03'
UNION ALL
SELECT 'fct_orders'    AS layer, COUNT(*) AS n, SUM(amount) AS revenue FROM curated.fct_orders WHERE order_date = DATE '2026-10-03'
UNION ALL
SELECT 'revenue_daily' AS layer, COUNT(*) AS n, SUM(revenue) AS revenue FROM marts.revenue_daily WHERE order_date = DATE '2026-10-03'
ORDER BY layer;
```

Then sample the rows that differ to see the shape of the problem:

```sql
-- Rows present in staging but missing from the mart
SELECT s.order_id, s.amount, s.status
FROM staging.stg_orders AS s
LEFT JOIN curated.fct_orders AS f USING (order_id)
WHERE s.order_date = DATE '2026-10-03' AND f.order_id IS NULL
LIMIT 100;
```

Also compare the metric query in version control with what the BI tool currently executes; a dashboard-side filter or a changed semantic-layer join is a common cause that no data test catches.

[Table of Contents](#Data-Observability)

## How do you design alerts to avoid alert fatigue?

Alerts should be actionable, scoped, and owned. Use severity levels, suppression windows, and baselines that account for seasonality. Prefer multi-signal alerts (freshness + volume) over single noisy checks, and include runbooks with clear next steps.

Rules that work: one alert, one action; alert on symptoms rather than every cause; use `for:` durations so blips do not page; group and inhibit so one root cause produces one notification; baseline by season with robust statistics (median, MAD); route non-paging tiers to a queue; and review alert quality monthly.

A multi-signal rule fires only when freshness **and** volume are both wrong, which is far less noisy than either alone:

```yaml
# prometheus/rules/revenue_mart.yml
groups:
  - name: revenue-mart
    rules:
      - alert: RevenueMartDegraded
        expr: |
          (time() - mart_last_success_timestamp_seconds{dataset="marts.revenue_daily"} > 10800)
          and
          (abs(mart_rows_written_total{dataset="marts.revenue_daily"} - mart_rows_written_7d_median)
             > 0.4 * mart_rows_written_7d_median)
        for: 15m
        labels: {severity: page, team: revenue-data}
        annotations:
          summary: "revenue_daily is stale AND volume is off baseline"
          runbook_url: "https://runbooks.acme.io/revenue-mart-degraded"
```

Airflow-side alerting should distinguish **task failure** from an **SLA miss**, because a DAG can finish successfully while being hours late. Assign every critical dataset an owning team and keep the paging tier small; a platform where every dataset pages the same channel is one where nobody trusts the channel.

[Table of Contents](#Data-Observability)

## How do you approach backfills safely?

Backfills can be expensive and risky because they rewrite history and can change metrics. A safe approach includes running in smaller batches, validating each batch, and separating "raw" from "published" layers so you can rebuild derived tables without re-ingesting sources. You also communicate expected metric changes and schedule around peak usage.

Safe order: scope the affected partitions, estimate rows/bytes/wall-clock on a sample, freeze or annotate downstream dashboards, batch and validate per partition, make writes idempotent, observe freshness and volume, publish atomically, then record what ran.

```bash
# Airflow: bounded-concurrency backfill of a specific window
airflow dags backfill revenue_daily \
  --start-date 2026-09-01 --end-date 2026-09-30 \
  --max-active-runs 2 --reset-dagruns
```

```sql
-- Atomic, idempotent per-partition rebuild: a rerun replaces, never duplicates
MERGE INTO curated.orders AS t
USING staging.orders_rebuild AS s
  ON t.order_date = s.order_date AND t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

Always capture before/after volume so the backfill is auditable, and for backfills touching finance or ML training data require a review, a dry-run on one partition, and a written expected metric delta.

[Table of Contents](#Data-Observability)

## What is a runbook and what should it contain?

A runbook is a step-by-step guide for responding to an alert or incident. It should include impact assessment, common root causes, validation queries, mitigation steps, rollback/backfill steps, and escalation contacts. Good runbooks reduce time-to-recovery for on-call engineers.

A good runbook is short, specific, and executable:

```text
Alert: RevenueMartDegraded

Impact: marts.revenue_daily feeds the exec revenue dashboard and finance close.
First 5 minutes: check the Airflow run state; query freshness and volume;
  verify the upstream raw.orders partition exists.
Likely causes: late upstream extract; schema change breaking staging;
  warehouse contention causing a timeout; duplicate rows from a retried merge.
Validation: SELECT MAX(updated_at), COUNT(*) FROM marts.revenue_daily
  WHERE order_date = CURRENT_DATE() - 1;
Mitigation: if upstream is late, wait and re-run (do not force success);
  if schema broke, revert and redeploy; if duplicated, dedup then re-run.
Rollback/backfill: airflow dags backfill revenue_daily --start-date <d> --end-date <d>
Escalation: revenue-data on-call, then platform on-call, then vendor support.
Post-incident: open a ticket with timeline, root cause, and an owned action.
```

Store runbooks next to the code in the repo and link them from the alert annotation, so they are reviewed in the same pull request as the pipeline. A runbook that lives only in a wiki rots within a quarter.

[Table of Contents](#Data-Observability)

## What are common incident patterns in data platforms?

Common patterns include:

+ upstream outages and late data
+ schema changes breaking transforms
+ duplicates from retries/reprocessing
+ incorrect joins causing metric inflation
+ partition boundary/timezone bugs
+ cost spikes due to inefficient queries

| Pattern | Signature | Fast detection |
|---|---|---|
| Late source feed | freshness climbs, volume drops | max(event_ts) vs SLA |
| Schema change | job fails at parse, or nulls appear | schema contract diff |
| Retry duplicates | row counts exceed baseline | count(*) <> count(distinct pk) |
| Join fan-out | totals inflated | fan-out guard query |
| Timezone bug | a day has ~half or ~double volume | volume by hour of day |
| Runaway query | bytes scanned or spend spikes | query history cost ranking |
| Silent filter | a segment disappears | distinct-value count by dimension |

A timezone bug is invisible to row-level checks, so profile volume across the hours of a day:

```sql
SELECT order_date, EXTRACT(HOUR FROM event_ts) AS hour_of_day, COUNT(*) AS n
FROM raw.orders
WHERE event_ts >= TIMESTAMP '2026-10-03 00:00:00'
  AND event_ts <  TIMESTAMP '2026-10-05 00:00:00'
GROUP BY order_date, hour_of_day
ORDER BY order_date, hour_of_day;
```

**Failure-mode note:** observability itself can fail. A freshness check that queries the same warehouse that is down quietly stops reporting and looks green. Monitor the monitors: alert when a check has not reported within its expected interval, and keep critical probes independent of the pipelines they observe.

[Table of Contents](#Data-Observability)

## Real world use cases for Data Observability

### 1. E-commerce revenue mart with an 8 AM SLA

A retailer's executive revenue dashboard must be correct by 08:00 local time. The nightly ELT loads ~400M order events into Snowflake; the mart is 90 GB and feeds exec dashboards and finance.

```yaml
# dbt: freshness plus contract tests on the tier-1 source
sources:
  - name: raw
    database: RAW
    schema: PUBLIC
    loaded_at_field: ingested_at
    freshness:
      warn_after: {count: 30, period: minute}
      error_after: {count: 90, period: minute}
    tables:
      - name: orders
        columns:
          - name: order_id
            tests: [unique, not_null]
```

**Why this design:** one freshness SLO plus a join fan-out guard, because this company's revenue bugs historically came from double-counted refunds rather than missing rows. Priority is tied to the exec SLA; everything else is a ticket.

### 2. Fintech reconciliation between core ledger and warehouse

A payments company mirrors its ledger into Snowflake. Every day at 02:00 the warehouse totals must equal the ledger totals to the cent, or the regulatory close is blocked. Volume is ~120M transactions/day.

```sql
-- Reconciliation gate; a non-empty result fails the pipeline (fail closed)
SELECT
    SUM(t.amount_cents) - SUM(w.amount_cents) AS delta_cents
FROM ledger.transactions AS t
FULL OUTER JOIN warehouse.transactions AS w USING (txn_id)
WHERE DATE(t.settled_at) = DATE '2026-10-04'
   OR DATE(w.settled_at) = DATE '2026-10-04'
HAVING SUM(t.amount_cents) - SUM(w.amount_cents) <> 0;
```

**Why this design:** the ledger is an independent source of truth, so reconciliation is the only check that can prove correctness. The pipeline fails closed because a wrong regulatory number is worse than a late one.

### 3. Multi-tenant SaaS where one tenant breaks everyone

A B2B platform ingests events from 3,000 tenants into a shared lake (~2 TB/day). One tenant's malformed payload once broke the shared parse and stalled all tenants' dashboards.

```sql
-- Per-tenant freshness and volume so anomalies are attributed, not aggregated
SELECT
    tenant_id,
    MAX(event_ts) AS latest_event,
    COUNT(*) AS events_today,
    COUNT(*) * 1.0 / NULLIF(AVG(COUNT(*)) OVER (), 0) AS relative_volume
FROM raw.events
WHERE event_date = CURRENT_DATE() - 1
GROUP BY tenant_id
ORDER BY relative_volume ASC
LIMIT 50;
```

**Why this design:** checks are partitioned by `tenant_id` so an alert names the tenant, and bad payloads are quarantined per tenant rather than failing the shared DAG. This trades a little per-tenant latency for platform-wide availability.

### 4. ML feature store freshness as a first-class SLO

A recommendation system refreshes 600 features for 40M users every 6 hours. Stale features silently degrade click-through with no error, so freshness is the top metric.

```python
# Feature freshness probe, run after each materialization
from datetime import datetime, timedelta, timezone

SLA = timedelta(hours=6)


def check_feature_freshness(conn, feature_view: str, now: datetime | None = None) -> None:
    now = now or datetime.now(timezone.utc)
    row = conn.execute(f"SELECT MAX(event_ts) FROM feature_store.{feature_view}").fetchone()
    latest = row[0]
    if latest is None or (now - latest) > SLA:
        raise RuntimeError(f"{feature_view} stale: latest={latest} now={now}")
```

**Why this design:** freshness drives model quality, so it belongs in the same SLO framework as revenue data. Pairing it with a distribution-drift check catches the case where features are timely but shifted by a bad upstream join.

[Table of Contents](#Data-Observability)
