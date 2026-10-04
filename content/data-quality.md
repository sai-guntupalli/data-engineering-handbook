## [Main title](../README.md)
### [Interview questions](full.md)

# Data Quality

**Notebook:** [`notebooks/topics/data-quality.ipynb`](../notebooks/topics/data-quality.ipynb) - runnable version of this topic with self-checking exercises.

Data quality means data is fit for its intended use. Good pipelines assert what "correct" means, fail or quarantine when it is violated, and leave evidence that lets an engineer explain why a number changed.

The toolkit is layered: **contracts** define what producers promise, **tests** assert those promises on every build, **reconciliation** proves the target matches an independent source of truth, **monitoring** catches drift that static rules cannot express, and **quarantine** isolates bad records instead of corrupting the curated layer.

+ [What does data quality mean in data engineering?](#What-does-data-quality-mean-in-data-engineering)
+ [What are common data quality dimensions?](#What-are-common-data-quality-dimensions)
+ [How do you implement data quality checks in pipelines?](#How-do-you-implement-data-quality-checks-in-pipelines)
+ [What are common dimensions of data quality?](#What-are-common-dimensions-of-data-quality)
+ [What is data freshness and how do you measure it?](#What-is-data-freshness-and-how-do-you-measure-it)
+ [What is the difference between data validation and data reconciliation?](#What-is-the-difference-between-data-validation-and-data-reconciliation)
+ [What are row-level checks and aggregate checks?](#What-are-row-level-checks-and-aggregate-checks)
+ [How do you design quality checks for incremental pipelines?](#How-do-you-design-quality-checks-for-incremental-pipelines)
+ [How do you handle late arriving data from a quality perspective?](#How-do-you-handle-late-arriving-data-from-a-quality-perspective)
+ [How do you detect schema drift and breaking changes?](#How-do-you-detect-schema-drift-and-breaking-changes)
+ [What are data contracts?](#What-are-data-contracts)
+ [How do you avoid noisy alerts (false positives) in data quality monitoring?](#How-do-you-avoid-noisy-alerts-false-positives-in-data-quality-monitoring)
+ [What is anomaly detection for metrics and when is it useful?](#What-is-anomaly-detection-for-metrics-and-when-is-it-useful)
+ [How do you quarantine bad data without blocking the entire pipeline?](#How-do-you-quarantine-bad-data-without-blocking-the-entire-pipeline)
+ [How do you test data transformations?](#How-do-you-test-data-transformations)
+ [What is the minimum set of checks you would add to every table?](#What-is-the-minimum-set-of-checks-you-would-add-to-every-table)
+ [What are common data quality failure modes?](#What-are-common-data-quality-failure-modes)
+ [Real world use cases for Data Quality](#Real-world-use-cases-for-Data-Quality)

## What does data quality mean in data engineering?

Data quality means the data is fit for its intended use: correct, complete, consistent, timely, and well-defined so downstream consumers can trust metrics. It is both a technical problem (pipelines) and a product problem (definitions and contracts).

Interviewers listen for **specific, business-anchored rules**. "We check quality" is not an answer; "every order must reconcile to exactly one payment within 24 hours, and we block the revenue mart if the delta is non-zero" is.

```sql
-- A quality result table makes the loop auditable and reproducible
CREATE TABLE IF NOT EXISTS platform.dq_results (
    check_id STRING, dataset STRING, partition DATE, check_name STRING, severity STRING, status STRING, failed_rows INT64, run_at TIMESTAMP
);
```

Store the query alongside the result so a failure can be re-run against that exact partition instead of becoming archaeology.

[Table of Contents](#Data-Quality)

## What are common data quality dimensions?

Common dimensions include completeness, uniqueness, validity, consistency, timeliness, accuracy, and referential integrity. Interview answers should include examples because quality is only meaningful when tied to a business rule.

Examples:

+ completeness: `customer_id` is not null
+ uniqueness: one current row per `customer_id`
+ validity: `order_status` is in the allowed status list
+ timeliness: daily table arrives before 7 AM
+ referential integrity: every `orders.customer_id` exists in `customers`

Good data quality systems track both failures and trends, such as a sudden null-rate jump from 1 percent to 20 percent. Start with the dimensions whose failure actually caused incidents in the last year; that is where the business value is measurable.

[Table of Contents](#Data-Quality)

## How do you implement data quality checks in pipelines?

Run checks close to the data they protect and fail fast for critical rules. Use warnings for non-critical anomalies and hard failures for rules that would corrupt downstream reporting. Store check results with run id, dataset, rule name, status, and sample failed records.

```sql
-- SQL assertion: a non-zero count lets the orchestrator block the publish
SELECT COUNTIF(amount < 0 OR order_id IS NULL) AS invalid_rows
FROM curated.fct_orders
WHERE order_date = DATE '2026-10-04';
```

The same rules as a version-controlled Great Expectations suite:

```yaml
# great_expectations/expectations/orders_suite.yml
expectation_suite_name: orders_suite
expectations:
  - expectation_type: expect_column_values_to_not_be_null
    kwargs: {column: order_id}
  - expectation_type: expect_column_values_to_be_unique
    kwargs: {column: order_id}
  - expectation_type: expect_column_values_to_be_between
    kwargs: {column: amount, min_value: 0, max_value: 1000000}
  - expectation_type: expect_column_values_to_be_in_set
    kwargs:
      column: status
      value_set: [placed, paid, shipped, cancelled, refunded]
meta:
  owner: revenue-data
  severity: error
```

For dbt, declarative tests run on every build and appear in the lineage graph: `tests: [unique, not_null]` on the key column, `accepted_values` on enums, and `relationships` on foreign keys.

**Failure mode:** putting every check in the critical path. Classify severity when you write the check, not during the incident.

[Table of Contents](#Data-Quality)

## What are common dimensions of data quality?

Common dimensions include:

+ completeness (missing rows/fields)
+ validity (values in allowed ranges/domains)
+ accuracy (matches real-world or source truth)
+ consistency (no contradictions across tables)
+ timeliness/freshness (arrives within SLA)
+ uniqueness (no duplicates where keys should be unique)

These map onto where a check should run: schema, validity, and freshness at the producer; completeness and format at landing; uniqueness, casting, and referential integrity in staging; reconciliation and distribution in marts; and definition-level checks in the semantic layer.

Checking at the wrong layer is a common miss: a `not_null` on the mart is too late, while referential integrity on raw data is premature if the dimension loads afterwards. Put each rule where it can fire early and be fixed, and note that dimensions are **relative to a consumer** - a raw event stream may tolerate 2% missing device ids while a billing mart tolerates zero.

[Table of Contents](#Data-Quality)

## What is data freshness and how do you measure it?

Freshness is how recently data was updated relative to expected cadence. You can measure it by comparing the maximum event/ingestion timestamp in a table to current time, and alert when it exceeds an SLA threshold. Freshness should be defined per dataset because "daily" and "real-time" pipelines differ.

Measure three things, because they fail independently: **data freshness** (`now - max(event_time)`), **load freshness** (`now - max(ingested_at)`, catching a source that stopped producing), and **publish freshness** (`now - max(published_at)`, catching a late transform).

```sql
SELECT
    MAX(event_time) AS latest_event,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(event_time), MINUTE)   AS event_lag_min,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(ingested_at), MINUTE)  AS load_lag_min,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(published_at), MINUTE) AS publish_lag_min
FROM curated.orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY);
```

For dbt sources, freshness is declarative (`loaded_at_field` plus `warn_after`/`error_after` under `freshness:`) and shows up on the lineage graph.

**Failure mode:** measuring freshness only on the global max timestamp. If one region stopped loading while another kept writing, the check stays green. Measure per partition and per key dimension, and add a partition-gap check (generate the expected calendar and left-join actual partitions).

[Table of Contents](#Data-Quality)

## What is the difference between data validation and data reconciliation?

Validation checks whether a dataset satisfies rules (types, constraints, ranges). Reconciliation compares datasets to ensure they match expected totals or invariants (for example source row count vs target row count, or sum(amount) in source vs warehouse). Reconciliation is important when multiple systems can drift.

Validation compares one dataset to a rule, so it detects malformed rows and bad values but is blind to silently dropped rows. Reconciliation compares two systems, needs an independent source of truth, and is what catches drift and double-counts.

```sql
-- Reconciliation returns a non-empty result when counts or totals disagree
SELECT
    src.biz_date,
    src.src_rows - tgt.tgt_rows AS row_delta,
    src.src_total - tgt.tgt_total AS amount_delta_cents
FROM (
    SELECT DATE(created_at) AS biz_date, COUNT(*) AS src_rows, SUM(amount_cents) AS src_total
    FROM ledger.transactions GROUP BY biz_date
) AS src
FULL OUTER JOIN (
    SELECT DATE(created_at) AS biz_date, COUNT(*) AS tgt_rows, SUM(amount_cents) AS tgt_total
    FROM warehouse.transactions GROUP BY biz_date
) AS tgt USING (biz_date)
WHERE src.src_rows <> tgt.tgt_rows OR src.src_total <> tgt.tgt_total;
```

Validation catches a broken row; reconciliation catches a broken **pipeline**. A pipeline can pass every row-level check and still lose 10% of rows in a join, which only reconciliation will see.

[Table of Contents](#Data-Quality)

## What are row-level checks and aggregate checks?

Row-level checks validate each record (for example `not_null`, regex, range constraints). Aggregate checks validate the dataset as a whole (row counts, distinct counts, distribution checks, totals). Aggregate checks often catch issues that row-level rules miss, like missing partitions.

```python
# PySpark: one pass emits both the invalid sample and aggregate guardrails
from pyspark.sql import functions as F

orders = spark.read.parquet("s3://acme-curated/orders/ds=2026-10-04/")

invalid = orders.filter(F.col("order_id").isNull() | (F.col("amount") < 0))
summary = orders.agg(
    F.count("*").alias("rows"),
    F.countDistinct("customer_id").alias("customers"),
    F.avg("amount").alias("avg_amount"),
    (F.count_if(F.col("order_id").isNull()) / F.count("*")).alias("null_rate"),
)
invalid.limit(100).show(truncate=False)
summary.show()
```

Use both: row-level checks give you the sample and the ability to quarantine specific records; aggregate checks guard against a whole partition disappearing.

[Table of Contents](#Data-Quality)

## How do you design quality checks for incremental pipelines?

Checks should be scoped to the incremental window and also protect the full table invariants. For example, validate uniqueness on the keys in the new batch, validate that the batch size is within expected bounds, and validate that total counts change consistently. You also need idempotency checks to detect duplicates on retries.

Three classes matter: **batch checks** (the new window: nulls, ranges, row-count bounds), **merge checks** (no duplicate keys, deletes handled), and **invariant checks** (the whole table still satisfies its grain and totals).

```sql
-- Batch bound: today's slice within 40% of the trailing median
WITH today AS (
    SELECT COUNT(*) AS n FROM curated.fct_orders WHERE order_date = DATE '2026-10-04'
),
baseline AS (
    SELECT APPROX_QUANTILES(n, 2)[OFFSET(1)] AS median_n
    FROM (
        SELECT order_date, COUNT(*) AS n FROM curated.fct_orders
        WHERE order_date BETWEEN DATE '2026-09-27' AND DATE '2026-10-03'
        GROUP BY order_date
    )
)
SELECT t.n, b.median_n, ABS(t.n - b.median_n) / b.median_n AS deviation
FROM today AS t CROSS JOIN baseline AS b
WHERE ABS(t.n - b.median_n) / b.median_n > 0.4;
```

**Failure mode:** checking only the batch. A merge with a stale `unique_key` can leave duplicates from previous runs that the new batch never touches, so always run a full-table key-uniqueness check after an incremental merge, even if it is slower and less frequent.

[Table of Contents](#Data-Quality)

## How do you handle late arriving data from a quality perspective?

You define allowed lateness (for example 7 days), track completeness by event time, and implement backfills to "close" historical partitions. Quality checks should consider both ingestion time and event time so you can detect gaps in past periods.

State the policy explicitly, because every consumer depends on it: events are accepted up to 7 days late; a day is "closed" once it is 7 days old; closed days are immutable; late events for closed days raise an alert and are routed to a correction table for a controlled backfill.

```sql
-- Detect a burst of late data arriving for already-closed partitions
SELECT DATE(event_time) AS event_date, COUNT(*) AS late_events
FROM raw.events
WHERE ingested_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND DATE(event_time) < DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY event_date
ORDER BY late_events DESC;
```

Corrections use an idempotent merge so replays are safe, and the watermark lives in orchestration so a partition is not reprocessed forever.

**Failure mode:** treating late data as a quality failure. Late events are normal in mobile and IoT; the quality decision is when a partition becomes immutable, and enforcing it. Without a closed-partition rule, backfills and live writes fight over the same day forever.

[Table of Contents](#Data-Quality)

## How do you detect schema drift and breaking changes?

You compare incoming schemas to an expected contract (column names, types, nullability) and alert on changes. Additive changes can be allowed with policy, but breaking changes (rename/type change) should fail fast. Many teams use CI checks and schema registries to enforce compatibility.

| Change | Compatibility | Action |
|---|---|---|
| New nullable column | backward compatible | allow, update contract |
| New non-null column | may break writers/readers | coordinate, default value |
| Column dropped | breaking | block, deprecate first |
| Type widened (int -> long) | usually safe | allow with review |
| Type changed/narrowed | breaking | block |
| Rename | breaking (looks like drop + add) | version the column |

```python
# Contract check: compare a live Parquet schema to a committed contract
import json
from pathlib import Path

import pyarrow.parquet as pq

contract = json.loads(Path("contracts/orders.json").read_text())
expected = {col["name"]: col["type"] for col in contract["columns"]}
actual = {f.name: str(f.type) for f in pq.read_schema("s3://acme-curated/orders/ds=2026-10-04/part-00000.parquet")}

removed = {k: v for k, v in expected.items() if k not in actual}
type_changed = {k: {"expected": expected[k], "actual": actual[k]}
                for k in expected.keys() & actual.keys() if expected[k] != actual[k]}

if removed or type_changed:
    raise ValueError(f"Breaking schema change: removed={removed} changed={type_changed}")
```

For streaming producers, enforce compatibility at the registry (`POST /compatibility/subjects/<topic>-value/versions/latest`) rather than after the fact. When a breaking change is unavoidable, publish a new table or version and migrate consumers - never silently mutate the meaning of an existing column.

[Table of Contents](#Data-Quality)

## What are data contracts?

Data contracts are explicit agreements between producers and consumers about schema, semantics, SLAs, and ownership. Contracts reduce surprises by defining what can change and what cannot, and they enable automated validation. A contract can live as code (YAML/JSON) and be enforced in CI/CD.

A useful contract covers schema, semantics (units, enums, timezone), freshness/SLA, volume bounds, ownership, and change policy.

```yaml
# contracts/orders.yaml (excerpt)
contract_version: 2.1.0
dataset: raw.orders
owner: {team: orders-platform, contact: orders-platform@acme.io}
schema:
  - {name: order_id,     type: string,    nullable: false, key: true}
  - {name: amount_cents, type: int64,     nullable: false, unit: cents, min: 0}
  - {name: status,       type: string,    nullable: false, enum: [placed, paid, shipped, cancelled]}
  - {name: ordered_at,   type: timestamp, nullable: false, timezone: UTC}
sla: {cadence: hourly, max_lateness_minutes: 30, publish_by: "00:45 UTC"}
volume: {expected_rows_per_day: {min: 800000, max: 1400000}}
change_policy: {additive: allowed_with_notice, breaking: 30 days notice}
```

**Failure mode:** contracts nobody enforces. A YAML file in a wiki is documentation; it becomes a contract only when a pipeline or CI job fails on violation. Start with one high-value producer-consumer pair, then expand.

[Table of Contents](#Data-Quality)

## How do you avoid noisy alerts (false positives) in data quality monitoring?

Use dynamic thresholds, seasonality-aware baselines, and multi-signal alerts (freshness + volume + error rate). Also route alerts by severity and dataset criticality, and suppress alerts during known maintenance windows. Good alerting includes a runbook and clear ownership.

Four techniques reduce false positives: **baselines, not constants** (compare to the same weekday over 4-6 weeks); **robust statistics** (median and MAD resist outliers); **corroboration** (alert only if freshness and volume are both off, or a check fails twice); and **tiering** (not every dataset deserves a page).

```sql
-- Robust volume anomaly: flag when today is more than 3.5 MADs from the median
WITH history AS (
    SELECT order_date, COUNT(*) AS n FROM curated.fct_orders
    WHERE order_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 42 DAY)
                         AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    GROUP BY order_date
),
median_n AS (
    SELECT APPROX_QUANTILES(n, 2)[OFFSET(1)] AS median_n FROM history
),
deviation AS (
    SELECT ABS(h.n - m.median_n) AS abs_dev
    FROM history AS h CROSS JOIN median_n AS m
),
mad AS (
    SELECT APPROX_QUANTILES(abs_dev, 2)[OFFSET(1)] AS mad FROM deviation
),
stats AS (SELECT median_n.median_n, mad.mad FROM median_n CROSS JOIN mad),
today AS (SELECT COUNT(*) AS n FROM curated.fct_orders WHERE order_date = CURRENT_DATE() - 1)
SELECT t.n, s.median_n, ABS(t.n - s.median_n) / NULLIF(s.mad, 0) AS robust_z
FROM today AS t CROSS JOIN stats AS s
WHERE ABS(t.n - s.median_n) / NULLIF(s.mad, 0) > 3.5;
```

Track how often each alert fires and how often it was actionable, and delete or retune anything with a low actionability ratio.

[Table of Contents](#Data-Quality)

## What is anomaly detection for metrics and when is it useful?

Anomaly detection flags unusual changes in metrics (spikes/drops) that may indicate pipeline issues or business events. It is useful for detecting silent failures where data still arrives but is wrong. It should be combined with context (releases, campaigns) to avoid alert fatigue.

It fits when the **shape** is stable but the exact value is not - daily row counts, null rates, average order value - and fits poorly when a hard rule already exists (a key is unique or it is not).

```python
# Robust z-score with guardrails for small samples and zero MAD
from statistics import median


def robust_z(value: float, history: list[float]) -> float:
    if len(history) < 8:
        return 0.0
    med = median(history)
    mad = median([abs(x - med) for x in history]) or 1e-9
    return 0.6745 * (value - med) / mad


def check_metric(value: float, history: list[float], threshold: float = 3.5) -> bool:
    return abs(robust_z(value, history)) > threshold
```

Attach context before paging: a 40% spike on a campaign launch day is expected; a 40% drop in a normal week is not. Feed the detector a calendar of known events, and pair it with a business-metric monitor - if revenue, orders, and sessions move together, the change is probably real.

**Failure mode:** anomaly detection as the only layer. It cannot explain *why*, needs a warm-up period, and can miss a structural failure that looks valid under a new normal. Keep hard contract tests for invariants.

[Table of Contents](#Data-Quality)

## How do you quarantine bad data without blocking the entire pipeline?

A common pattern is to split data into "good" and "quarantine" outputs based on validation rules. You can store bad rows with error reasons for debugging while allowing the pipeline to continue for valid data. For critical datasets, you may still block publishing to marts while keeping raw ingestion running.

Choose a policy per dataset: **block** for financial/regulatory totals, **quarantine and continue** for high-volume event data, and **warn only** for low-impact exploratory data.

```python
# Split valid and invalid records, write both, and enforce a rate threshold
from pyspark.sql import functions as F

orders = spark.read.parquet("s3://acme-raw/orders/ds=2026-10-04/")
reasons = (
    F.when(F.col("order_id").isNull(), "null_order_id")
     .when(F.col("amount") < 0, "negative_amount")
     .when(~F.col("status").isin("placed", "paid", "shipped", "cancelled"), "bad_status")
)
classified = orders.withColumn("dq_reason", reasons)
classified.filter(F.col("dq_reason").isNull()).drop("dq_reason") \
    .write.mode("overwrite").parquet("s3://acme-curated/orders/ds=2026-10-04/")
classified.filter(F.col("dq_reason").isNotNull()) \
    .write.mode("overwrite").parquet("s3://acme-quarantine/orders/ds=2026-10-04/")

total = classified.count()
bad = classified.filter(F.col("dq_reason").isNotNull()).count()
if total and bad / total > 0.05:
    raise RuntimeError(f"Quarantine rate {bad / total:.1%} exceeds 5% threshold")
```

Keep a quarantine table with source path, offset, payload, error reason, and pipeline version so records can be replayed after the producer fix.

**Failure mode:** quarantining forever. A quarantine table nobody reviews is a data-loss table with extra steps. Add a retention policy, a dashboard of quarantine rate by reason, and a replay path.

[Table of Contents](#Data-Quality)

## How do you test data transformations?

You can test transformations by:

+ unit-like tests on small fixtures (golden datasets)
+ property tests (invariants like non-negative totals)
+ reconciliation tests against known sources
+ regression tests on key metrics

In dbt-style workflows, tests often run in the warehouse as SQL assertions.

| Layer | Speed | What it proves | Tool |
|---|---|---|---|
| Unit (fixtures) | ms | transformation logic | pytest + pandas/PySpark local |
| Property | ms | invariants for any input | hypothesis |
| Contract | seconds | schema and semantics | schema registry, JSON contract |
| Integration | minutes | connectors, SQL, warehouse | dbt tests, ephemeral schemas |

```python
# pytest golden fixture for a pure transformation
import pandas as pd

from pipelines.orders import add_tax


def test_add_tax_applies_rate():
    df = pd.DataFrame({"amount_cents": [1000, 2000], "country": ["DE", "US"]})
    out = add_tax(df, rates={"DE": 0.19, "US": 0.0})
    assert out["amount_cents"].tolist() == [1190, 2000]
```

**Failure mode:** change-detector tests that assert the current output rather than the intended behavior. Write assertions that encode a business rule, and keep fixtures small enough to verify by hand. In dbt, the same invariant is a "singular test" SQL file that must return zero rows.

[Table of Contents](#Data-Quality)

## What is the minimum set of checks you would add to every table?

Minimum checks often include:

+ freshness (max timestamp within SLA)
+ row count / volume sanity check
+ primary key uniqueness (if applicable)
+ not_null checks on critical columns
+ referential integrity for key joins (where applicable)

```sql
-- A ready-to-apply baseline for any new table
SELECT TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(updated_at), MINUTE) AS minutes_stale
FROM curated.new_table;                                       -- freshness

SELECT COUNT(*) AS rows FROM curated.new_table
WHERE ds = CURRENT_DATE() - 1;                                -- volume

SELECT COUNT(*) AS duplicates
FROM (SELECT pk, COUNT(*) AS c FROM curated.new_table GROUP BY pk HAVING c > 1);  -- uniqueness

SELECT COUNT(*) AS orphans
FROM curated.new_table AS t
LEFT JOIN curated.dim_parent AS p USING (parent_id)
WHERE p.parent_id IS NULL;                                    -- referential integrity
```

```yaml
# The same baseline as dbt tests per model
models:
  - name: new_table
    columns:
      - name: pk
        tests: [unique, not_null]
      - name: created_at
        tests: [not_null]
      - name: parent_id
        tests:
          - relationships: {to: ref('dim_parent'), field: parent_id}
    tests:
      - dbt_utils.recency: {datepart: hour, field: updated_at, interval: 24}
```

Two additions are cheap and disproportionately valuable: a **row count of zero** check (many silent failures publish an empty table successfully) and a **natural-key duplicate check at the target grain**.

[Table of Contents](#Data-Quality)

## What are common data quality failure modes?

Common failures include:

+ missing partitions or partial loads
+ duplicates due to retries/reprocessing
+ schema drift and type coercion issues
+ timezone and date boundary bugs
+ silent truncation or rounding changes
+ incorrect joins causing duplication

| Failure | Root cause | Detection |
|---|---|---|
| Missing partition | upstream late, filter bug | calendar-vs-actual gap check |
| Partial load | task failed mid-write | row count vs baseline |
| Duplicates | retry without idempotency | key uniqueness check |
| Schema drift | unannounced producer change | contract diff |
| Timezone bug | naive timestamps, UTC/local mix | volume by hour of day |
| Join fan-out | many-to-many, missing grain | fan-out guard |

Two checks catch a surprising share of these on their own: a **key-uniqueness check** (duplicates, fan-out) and a **day-over-day total reconciliation** (partial loads, truncation, definition drift).

```python
# Guard the most damaging failure explicitly: fact inflation from a bad join
fact = spark.read.parquet("s3://acme-curated/fct_orders/")
dim = spark.read.parquet("s3://acme-curated/dim_customers/")

joined = fact.join(dim, "customer_id")
before, after = fact.count(), joined.count()
if after != before:
    raise RuntimeError(f"Join inflated rows: {before} -> {after}")
```

**Failure mode:** assuming a green DAG means good data. The most expensive incidents are the ones where everything succeeded and the number is quietly wrong.

[Table of Contents](#Data-Quality)

## Real world use cases for Data Quality

### 1. E-commerce: blocking a revenue mart on a fan-out guard

A retailer's nightly pipeline joined orders to a customer dimension that had duplicate `customer_id` rows (a slowly-changing-dimension bug). Revenue doubled for three days because every task succeeded.

```sql
-- Pre-publish guard: the join must not change the fact grain
SELECT
    (SELECT COUNT(*) FROM curated.fct_orders WHERE order_date = DATE '2026-10-04') AS fact_rows,
    (SELECT COUNT(*) FROM curated.fct_orders AS f
       JOIN curated.dim_customers AS c USING (customer_id)
     WHERE f.order_date = DATE '2026-10-04') AS joined_rows
HAVING fact_rows <> joined_rows;
```

**Why this design:** the failure was a broken assumption (a 1:1 join), not a broken value, so row-level checks would never catch it. The guard runs on every build and blocks the publish, while an upstream uniqueness test prevents the duplicate dimension from being created again.

### 2. Fintech: daily reconciliation gate before the regulatory close

A payments company must prove the warehouse ledger equals the core ledger to the cent before the daily close, or the close is blocked. Volume is ~120M transactions/day.

```python
# Orchestrator: fail closed on any non-zero delta, page the on-call
def close_gate(ds: str, tolerance_cents: int = 0) -> None:
    delta = query_scalar(f"SELECT delta_cents FROM recon WHERE settle_date = '{ds}'")
    if delta not in (0, None) and abs(delta) > tolerance_cents:
        raise RuntimeError(f"Close blocked for {ds}: delta={delta} cents")
```

**Why this design:** the ledger is the independent source of truth, so reconciliation is the only check that can prove correctness. The pipeline fails closed because a wrong regulatory number is worse than a late one, and the delta itself is logged for audit.

### 3. Multi-tenant SaaS: per-tenant quality scoring

A B2B platform ingests metadata from 3,000 integrations at ~2 TB/day. One tenant's malformed payload once broke the shared parse, so the team now scores quality per tenant and quarantines individual tenants instead of the whole run.

```python
# Per-tenant quality score with a quarantine decision
from collections import defaultdict

THRESHOLDS = {"error": 0.05, "quarantine": 0.20}


def score_batch(records: list[dict]) -> dict[str, dict]:
    stats: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "bad": 0})
    for record in records:
        tenant = record.get("tenant_id", "unknown")
        stats[tenant]["total"] += 1
        if not is_valid(record):
            stats[tenant]["bad"] += 1

    scores = {}
    for tenant, s in stats.items():
        rate = s["bad"] / s["total"] if s["total"] else 0.0
        decision = ("quarantine_tenant" if rate >= THRESHOLDS["quarantine"]
                    else "alert" if rate >= THRESHOLDS["error"] else "ok")
        scores[tenant] = {"bad_rate": round(rate, 4), "decision": decision}
    return scores
```

**Why this design:** in a shared pipeline, aggregation hides per-tenant problems. Scoring by tenant lets the platform alert the specific integration owner and isolate bad payloads while everyone else keeps flowing.

### 4. ML feature platform: distribution drift as a quality check

A recommendation model consumes 600 features refreshed every 6 hours for 40M users. Features were timely, but a broken upstream join shifted the distribution of `click_through_rate_7d` and silently degraded recommendations.

```python
# Population Stability Index: flag a feature whose distribution moved materially
import numpy as np


def psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    breakpoints = np.quantile(expected, np.linspace(0, 1, buckets + 1))
    breakpoints[0], breakpoints[-1] = -np.inf, np.inf
    exp_counts = np.histogram(expected, bins=breakpoints)[0] / len(expected)
    act_counts = np.histogram(actual, bins=breakpoints)[0] / len(actual)
    exp_counts = np.clip(exp_counts, 1e-6, None)
    act_counts = np.clip(act_counts, 1e-6, None)
    return float(np.sum((act_counts - exp_counts) * np.log(act_counts / exp_counts)))


def check_feature_drift(reference: np.ndarray, today: np.ndarray, threshold: float = 0.2) -> bool:
    return psi(reference, today) > threshold
```

**Why this design:** row-level validation passed because every value was a valid float; the problem was the *distribution*. PSI is cheap enough to run on every materialization, so it sits alongside freshness as a first-class ML quality check.

[Table of Contents](#Data-Quality)
