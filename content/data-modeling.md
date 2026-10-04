## [Main title](../README.md)
### [Interview questions](full.md)

# Data Modeling

**Notebook:** [`notebooks/topics/data-modeling.ipynb`](../notebooks/topics/data-modeling.ipynb) - runnable version of this topic with self-checking exercises.

Data modeling is where most analytics problems are actually decided. A warehouse can be fast and still give the wrong revenue number if the grain, keys, or history handling are wrong. The questions below cover the Kimball vocabulary that interviewers expect (facts, dimensions, grain, SCD, bridges, conformed dimensions), the SQL and PySpark that implements it, and the trade-offs that decide between a star schema, a snowflake, and a Data Vault.

+ [What is data modeling in analytics and why does it matter?](#What-is-data-modeling-in-analytics-and-why-does-it-matter)
+ [What is grain and why is it the first question to answer?](#What-is-grain-and-why-is-it-the-first-question-to-answer)
+ [What is the difference between fact and dimension tables?](#What-is-the-difference-between-fact-and-dimension-tables)
+ [What is a star schema and what are its benefits?](#What-is-a-star-schema-and-what-are-its-benefits)
+ [Star schema vs snowflake schema: what are the trade-offs?](#Star-schema-vs-snowflake-schema-what-are-the-trade-offs)
+ [What are the main types of fact tables?](#What-are-the-main-types-of-fact-tables)
+ [What is a surrogate key and when should you use it?](#What-is-a-surrogate-key-and-when-should-you-use-it)
+ [What is a conformed dimension?](#What-is-a-conformed-dimension)
+ [What is SCD (Slowly Changing Dimension)?](#What-is-SCD-Slowly-Changing-Dimension)
+ [How do you implement SCD Type 2?](#How-do-you-implement-SCD-Type-2)
+ [What is a factless fact table?](#What-is-a-factless-fact-table)
+ [What is a bridge table and when do you need it?](#What-is-a-bridge-table-and-when-do-you-need-it)
+ [What are degenerate dimensions?](#What-are-degenerate-dimensions)
+ [How do you prevent double counting in analytical models?](#How-do-you-prevent-double-counting-in-analytical-models)
+ [How do you validate a data model after changes?](#How-do-you-validate-a-data-model-after-changes)
+ [How do you choose the grain for a fact table?](#How-do-you-choose-the-grain-for-a-fact-table)
+ [What does an SCD Type 2 table look like in practice?](#What-does-an-SCD-Type-2-table-look-like-in-practice)
+ [How do you model many-to-many relationships without breaking metrics?](#How-do-you-model-many-to-many-relationships-without-breaking-metrics)
+ [What is a metric definition layer and why does it matter?](#What-is-a-metric-definition-layer-and-why-does-it-matter)
+ [What is a Data Vault model?](#What-is-a-Data-Vault-model)
+ [How do you handle SCD Type 1 and Type 3?](#How-do-you-handle-SCD-Type-1-and-Type-3)
+ [How do you handle late-arriving dimensions and facts?](#How-do-you-handle-late-arriving-dimensions-and-facts)
+ [What is a date dimension and a role-playing dimension?](#What-is-a-date-dimension-and-a-role-playing-dimension)
+ [Kimball vs Inmon: which modeling approach should you use?](#Kimball-vs-Inmon-which-modeling-approach-should-you-use)
+ [Real world use cases for data modeling](#Real-world-use-cases-for-data-modeling)

## What is data modeling in analytics and why does it matter?

Data modeling in analytics is the process of structuring data so it can be queried reliably and efficiently for business questions. A good model makes metrics consistent, reduces complexity for consumers, and improves performance by aligning storage with query patterns. A bad model leads to inconsistent KPIs, confusing joins, and expensive queries.

The usual layered shape of a modern warehouse is:

```text
sources (OLTP, APIs, events, files)
        |
        v
staging / bronze      raw, append-only, one table per source
        |
        v
integration / silver  cleaned, conformed, deduplicated entities
        |
        v
marts / gold          facts + dimensions at a defined grain, documented metrics
        |
        v
BI, notebooks, reverse ETL, feature stores
```

Three decisions recur at every layer:

1. **Grain** - what does one row represent?
2. **Keys** - natural, surrogate, or composite, and how they join.
3. **Change handling** - overwrite (SCD1), version history (SCD2), or append-only events.

Kimball-style dimensional modeling puts facts and dimensions in the gold layer; Inmon-style modeling normalizes the integration layer first. Most practical warehouses borrow from both: normalized staging, dimensional marts.

Why it matters in interviews: a candidate who starts with "what is the grain and what does the business call a customer?" is showing modeling discipline; a candidate who starts writing `JOIN`s is showing SQL knowledge but not design judgment.

[Table of Contents](#Data-Modeling)

## What is grain and why is it the first question to answer?

Grain is the level of detail of a table, for example "one row per order line" or "one row per user per day". It determines which metrics are additive, how joins behave, and what can be uniquely identified. If grain is unclear, you will get duplicates, incorrect aggregations, and ambiguous keys.

Write the grain as an English sentence before writing any DDL, then encode it as a uniqueness test:

```sql
-- grain: one row per order line
select order_id, line_number, count(*) as c
from fact_order_line
group by order_id, line_number
having count(*) > 1;
```

```sql
-- grain: one row per account per day
select account_id, snapshot_date, count(*) as c
from fact_account_balance_daily
group by account_id, snapshot_date
having count(*) > 1;
```

Common grain mistakes:

+ Storing order-level values (shipping, tax) on every order-line row, then summing them.
+ Mixing snapshot grain with event grain in one table so a `sum` silently multiplies.
+ Using a table with no declared primary key, so nothing prevents duplicate loads.

Interview tip: grain and the primary key are the same statement expressed twice. If the key and the grain disagree, the model is wrong.

[Table of Contents](#Data-Modeling)

## What is the difference between fact and dimension tables?

Facts store measurable events (orders, payments, clicks) and typically contain foreign keys to dimensions. Dimensions store descriptive attributes (user, product, date) that provide context for slicing and filtering. Facts answer "what happened", dimensions answer "who/what/where/when".

```sql
create table dim_customer (
  customer_sk   bigint      primary key,
  customer_id   varchar(50) not null,
  customer_name varchar(200),
  segment       varchar(50),
  country_code  char(2)
);

create table fact_order_line (
  order_line_sk  bigint primary key,
  order_id       varchar(50) not null,   -- degenerate dimension
  customer_sk    bigint references dim_customer (customer_sk),
  product_sk     bigint references dim_product (product_sk),
  order_date_sk  int    references dim_date (date_sk),
  quantity       int,
  gross_amount   numeric(14, 2),
  discount_amount numeric(14, 2)
);
```

Practical rules:

+ Facts are usually narrow, long, and partitioned by date; dimensions are wide, short, and replicated.
+ Numeric columns in a fact table should be additive or semi-additive measures, not codes.
+ Descriptive text belongs in dimensions, not in the fact, unless it is a degenerate dimension such as `order_id`.

[Table of Contents](#Data-Modeling)

## What is a star schema and what are its benefits?

A star schema has a central fact table connected to multiple dimension tables. Benefits include simpler queries, clear join paths, and good performance because joins are typically fact-to-dimension (many-to-one). It also encourages consistent definitions of metrics and attributes.

```text
        dim_date
           |
dim_product -- fact_order_line -- dim_customer
           |
        dim_store
```

```sql
select d.year_month,
       p.category,
       sum(f.gross_amount - f.discount_amount) as net_revenue,
       sum(f.quantity)                          as units
from fact_order_line f
join dim_date    d on d.date_sk = f.order_date_sk
join dim_product p on p.product_sk = f.product_sk
where d.year_month = '2026-10'
group by d.year_month, p.category;
```

Why BI tools like stars: every dimension joins to the fact on a single surrogate key, so the tool can infer the join graph, generate `GROUP BY` correctly, and avoid fan-out. Snowflaked dimensions force the tool (and the analyst) through several hops, which increases the chance of a wrong aggregate.

[Table of Contents](#Data-Modeling)

## Star schema vs snowflake schema: what are the trade-offs?

Snowflake schema normalizes dimensions into multiple related tables. It can reduce redundancy and improve dimension maintainability, but it increases join complexity and can hurt performance. Star schemas are usually preferred for BI and ad-hoc analytics because they are easier for users and tools.

Snowflaked product dimension:

```sql
create table dim_product (
  product_sk  bigint primary key,
  product_id  varchar(50),
  product_name varchar(200),
  category_sk bigint references dim_category (category_sk),
  brand_sk    bigint references dim_brand (brand_sk)
);

create table dim_category (
  category_sk bigint primary key,
  category_name varchar(100),
  department_sk bigint references dim_department (department_sk)
);
```

The same information flattened for a star:

```sql
create table dim_product (
  product_sk     bigint primary key,
  product_id     varchar(50),
  product_name   varchar(200),
  category_name  varchar(100),
  department_name varchar(100),
  brand_name     varchar(100)
);
```

| Aspect | Star | Snowflake |
|---|---|---|
| Join count for a report | 1 hop per dimension | multiple hops |
| Storage | more redundancy | less redundancy |
| Ease for BI users | high | lower |
| Dimension maintenance | rewrite a wide row | update a small table |
| Query performance | usually better | usually worse |
| Best fit | BI marts, self-service | very large, shared dimensions with many consumers |

Interview answer: use a star for the consumption layer. Snowflake the dimension only when a sub-attribute is genuinely shared by many dimensions (for example a global geography or cost-center hierarchy) or when the dimension is so large that redundant text is a real cost. Many teams keep a snowflake in the warehouse and publish flattened views or semantic-layer datasets on top.

[Table of Contents](#Data-Modeling)

## What are the main types of fact tables?

Common types are:

+ transactional: one row per business event (order, payment)
+ periodic snapshot: one row per entity per period (daily account balance)
+ accumulating snapshot: one row that is updated as a process progresses (order lifecycle)

```sql
-- transactional
create table fact_payment (
  payment_sk bigint primary key,
  customer_sk bigint,
  payment_date_sk int,
  amount numeric(14, 2)
);

-- periodic snapshot: one row per account per day
create table fact_account_balance_daily (
  account_sk bigint,
  snapshot_date_sk int,
  closing_balance numeric(18, 2),
  primary key (account_sk, snapshot_date_sk)
);

-- accumulating snapshot: one row per order, milestones updated in place
create table fact_order_fulfillment (
  order_sk bigint primary key,
  ordered_date_sk int,
  packed_date_sk int,
  shipped_date_sk int,
  delivered_date_sk int,
  days_to_ship int
);
```

Choosing the right type depends on the questions you need to answer. Activity questions ("how many?") want a transactional fact; balance and state questions ("how many were open?") want a periodic snapshot; process questions ("how long did each stage take?") want an accumulating snapshot.

[Table of Contents](#Data-Modeling)

## What is a surrogate key and when should you use it?

A surrogate key is a synthetic identifier used instead of a natural key. It is useful when natural keys are not stable, when you need SCD history, or when integrating multiple sources with different key systems. Surrogate keys also allow consistent joins even if source keys change.

```sql
-- deterministic surrogate key built from the natural key(s)
select
  abs(xxhash64(cast(customer_id as varchar))) as customer_sk,
  customer_id,
  customer_name
from stg_customer;
```

```python
# map a natural key to a stable integer surrogate key in PySpark
from pyspark.sql import functions as F

customers = (
    customers
    .withColumn("customer_sk", F.abs(F.xxhash64("source_system", "customer_id")))
)
```

Design notes:

+ Use a hash (deterministic, parallel-safe) or an identity/sequence (compact, but requires a lookup). Hash keys are easier in distributed loads because there is no coordination.
+ A type-2 dimension needs a *new* surrogate key per version; the natural key stays the same across versions.
+ Keep surrogate keys meaningless - never encode business meaning into digits of the key.
+ Do not use natural keys as the physical primary key of a large fact table: they are wide, and source systems sometimes reuse or recycle them.

[Table of Contents](#Data-Modeling)

## What is a conformed dimension?

A conformed dimension is a dimension shared consistently across multiple fact tables or data marts. For example, the same "customer" dimension used for orders and support tickets. Conformed dimensions enable consistent reporting and cross-domain analysis.

```text
dim_customer
   |             |
fact_order    fact_support_ticket
```

Rules that keep a dimension conformed:

+ One owner and one definition per attribute. "Customer" cannot mean "billing account" in one mart and "user" in another.
+ Identical surrogate keys and column names wherever the dimension is published.
+ Conformed dimensions are what make drill-across (`order revenue` vs `ticket count` by customer segment) trustworthy.
+ Date is the most common conformed dimension and should always be shared.

[Table of Contents](#Data-Modeling)

## What is SCD (Slowly Changing Dimension)?

SCD describes how you handle changes in dimension attributes over time (for example a user changing address). Type 1 overwrites history, Type 2 tracks history with multiple rows and effective dates, and Type 3 keeps limited history in additional columns. The choice depends on whether "as-of" reporting is required.

| Type | Behavior | Keeps history | Typical use |
|---|---|---|---|
| 0 | never changes | attribute frozen | immutable codes |
| 1 | overwrite in place | no | fixing typos, corrections |
| 2 | new row + effective dates | full | segment, address, plan, ownership |
| 3 | previous value in an extra column | one prior value | simple "before/after" reporting |
| 4 | separate history table | full, outside main dim | audit-heavy, huge dimensions |
| 6 | 2 + 3 hybrid | full + current column on every row | power-user reporting |

Interview guidance: pick the type per attribute, not per table. A `customer_name` correction is SCD1; a `customer_segment` change that affects historical revenue attribution is SCD2.

[Table of Contents](#Data-Modeling)

## How do you implement SCD Type 2?

SCD2 typically stores:

+ a surrogate key
+ the natural/business key
+ effective_start and effective_end timestamps (or end_date)
+ a current_flag

On change, you "close" the previous record and insert a new version. You must define how to detect changes and handle late arriving updates.

Implementation checklist:

1. Stage the incoming snapshot and deduplicate it on the natural key (keep the latest per key).
2. Compare tracked attributes against the current dimension row with a null-safe comparison.
3. Close changed rows: set `effective_end_at = now()` and `is_current = false`.
4. Insert changed rows plus brand-new keys with `effective_start_at = now()`, `effective_end_at = '9999-12-31'`, `is_current = true`.
5. Do it in one transaction or one `MERGE` so readers never see two current rows for a key.

Use a sentinel `9999-12-31` end date rather than `NULL` so range joins and `between` predicates behave the same on every engine, and use a null-safe comparison (`<=>` in Snowflake/MySQL, `IS DISTINCT FROM` in Postgres/Trino) so a `NULL -> value` change is detected.

[Table of Contents](#Data-Modeling)

## What is a factless fact table?

A factless fact table records events that do not have numeric measures, for example "student attended class" or "user is eligible for campaign". The fact itself can be counted, and the table is useful for coverage, eligibility, and relationship tracking.

```sql
-- coverage: which products were on promotion in which store on which day
create table fact_promotion_coverage (
  store_sk bigint,
  product_sk bigint,
  promotion_sk bigint,
  date_sk int,
  primary key (store_sk, product_sk, promotion_sk, date_sk)
);

-- "products that sold" vs "products that were available":
select count(distinct p.product_sk) as products_on_promotion
from fact_promotion_coverage p
join dim_date d on d.date_sk = p.date_sk
where d.year_month = '2026-10';
```

Factless facts are also how you answer "what did *not* happen" - for example, stores that had no sales on a day require a coverage fact joined against the sales fact.

[Table of Contents](#Data-Modeling)

## What is a bridge table and when do you need it?

A bridge table resolves many-to-many relationships, for example products belonging to multiple categories or users having multiple roles. It can also store weights for allocation (for example revenue split). Without a bridge table, joins can explode row counts and break aggregations.

```sql
create table bridge_order_promotion (
  order_sk     bigint,
  promotion_sk bigint,
  allocation_weight numeric(5, 4),
  primary key (order_sk, promotion_sk)
);

-- weighted revenue by promotion, without double counting
select p.promotion_name,
       sum(f.revenue * b.allocation_weight) as attributed_revenue
from fact_order f
join bridge_order_promotion b on b.order_sk = f.order_sk
join dim_promotion p          on p.promotion_sk = b.promotion_sk
group by p.promotion_name;
```

Design points:

+ The weights for one order should sum to 1 (or the allocation is explicitly documented as unweighted).
+ Add a "primary" flag when one relationship should win for simple reports.
+ A bridge is also a conformed dimension helper: it lets two facts meet without a direct many-to-many join.

[Table of Contents](#Data-Modeling)

## What are degenerate dimensions?

Degenerate dimensions are identifiers stored in the fact table without a separate dimension table, such as order_id or invoice_number. They are useful for drill-through and filtering while avoiding unnecessary dimension tables.

```sql
select order_id,            -- degenerate dimension
       sum(gross_amount) as order_total
from fact_order_line
group by order_id
having sum(gross_amount) > 10000;
```

Use degenerate dimensions when the identifier has no descriptive attributes of its own, when it is at the grain of the fact, and when its cardinality is too high to justify a dimension table. Keep it in the fact, index it if drill-through is frequent, and do not build a dimension that contains only the id.

[Table of Contents](#Data-Modeling)

## How do you prevent double counting in analytical models?

You prevent double counting by enforcing correct grain, using proper join keys (many-to-one), and avoiding many-to-many joins without a bridge table. You also define metric rules (sum vs distinct count vs last value) and test them with reconciliation queries.

The classic fan-out bug: joining a fact to a dimension that has more than one matching row per fact row multiplies the measure.

```sql
-- wrong: a customer with two addresses doubles every order amount
select sum(o.order_amount)
from fact_order o
join dim_customer_address a on a.customer_sk = o.customer_sk;

-- right: aggregate the dimension first, or filter to the primary address
select sum(o.order_amount)
from fact_order o
join (select customer_sk, min(address_sk) as address_sk
      from dim_customer_address
      group by customer_sk) a
  on a.customer_sk = o.customer_sk;
```

Other guards:

+ Prefer joining to the current dimension row (`is_current = true`) for point-in-time-insensitive reports, and to the versioned row for as-of reports.
+ Never join two facts on a common key unless one is aggregated to the same grain first.
+ For semi-additive measures such as balances, use `max` or `avg` over time, not `sum`.
+ Add a reconciliation test that compares the mart total to the source total; alert on drift above a threshold.

[Table of Contents](#Data-Modeling)

## How do you validate a data model after changes?

Typical validation includes:

+ row count and key uniqueness checks at each layer
+ reconciliation of totals against source systems
+ sampling and drill-through checks on known entities
+ regression tests for key business metrics

This catches subtle issues like join duplication or missing late data.

```sql
-- uniqueness + not-null tests, in the style of dbt tests
select customer_id, count(*) as c
from dim_customer
where is_current
group by customer_id
having count(*) > 1;

-- exactly one open version per key
select customer_id, count(*) as open_versions
from dim_customer
where effective_end_at = date '9999-12-31'
group by customer_id
having count(*) <> 1;

-- referential integrity
select count(*) as orphan_facts
from fact_order_line f
left join dim_product p on p.product_sk = f.product_sk
where p.product_sk is null;
```

Make the tests part of the pipeline, not a manual step: fail the run when a test returns rows, and store the result next to the table so a reviewer can see what was checked.

[Table of Contents](#Data-Modeling)

## How do you choose the grain for a fact table?

Start with the business process and write the grain as a sentence before naming columns. Good examples are "one row per order line", "one row per payment transaction", or "one row per account per day". Once the grain is fixed, every measure and dimension key must fit that level of detail.

Example:

+ `fact_order_line`: one row per order line item; measures include quantity, gross_amount, discount_amount
+ `fact_order`: one row per order; measures include order_total and shipping_amount
+ `fact_customer_day`: one row per customer per day; measures include daily_active_flag and session_count

The common mistake is mixing grains in one table, such as storing order-level shipping cost on every order line. That causes double counting unless you allocate the value or keep it in a separate order-grain fact.

```text
If the business asks for X and the answer needs Y detail,
model at Y and aggregate up - never the reverse.
```

When two candidate grains are valid, prefer the lowest granular one that still answers the main questions, because you can always aggregate up but you cannot split an aggregated row back into detail.

[Table of Contents](#Data-Modeling)

## What does an SCD Type 2 table look like in practice?

An SCD Type 2 dimension stores multiple versions of a business entity so historical facts can join to the correct version "as of" the event date. It usually has a surrogate key, the natural key, tracked attributes, effective dates, and a current flag.

Example:

```sql
create table dim_customer (
  customer_sk bigint,
  customer_id varchar(50),
  email varchar(255),
  customer_segment varchar(50),
  effective_start_at timestamp,
  effective_end_at timestamp,
  is_current boolean
);
```

If customer `C123` moves from `standard` to `enterprise`, close the old row by setting `effective_end_at`, then insert a new row with a new `customer_sk`. Facts can either store the resolved `customer_sk` at load time or join by `customer_id` and event timestamp.

The same change expressed as one idempotent `MERGE` on a Snowflake-style warehouse:

```sql
merge into dim_customer as tgt
using (
  select customer_id, email, customer_segment
  from stg_customer
  qualify row_number() over (partition by customer_id order by updated_at desc) = 1
) as src
on tgt.customer_id = src.customer_id
   and tgt.is_current
when matched and (
       tgt.email            is distinct from src.email
    or tgt.customer_segment is distinct from src.customer_segment
) then update set
       tgt.effective_end_at = current_timestamp(),
       tgt.is_current       = false;

-- insert the new versions (and brand-new customers)
insert into dim_customer (
  customer_sk, customer_id, email, customer_segment,
  effective_start_at, effective_end_at, is_current
)
select
  abs(hash(src.customer_id || current_timestamp()::varchar)),
  src.customer_id,
  src.email,
  src.customer_segment,
  current_timestamp(),
  '9999-12-31'::timestamp,
  true
from stg_customer src
left join dim_customer tgt
  on tgt.customer_id = src.customer_id
 and tgt.is_current
where tgt.customer_id is null
   or tgt.email            is distinct from src.email
   or tgt.customer_segment is distinct from src.customer_segment;
```

A PySpark implementation that does the same work as two DataFrame operations:

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

staged = (
    spark.table("stg_customer")
    .withColumn("rn", F.row_number().over(
        Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc())
    ))
    .where(F.col("rn") == 1)
    .drop("rn")
)

current = spark.table("dim_customer").where(F.col("is_current"))

changed = (
    current.alias("c")
    .join(staged.alias("s"), "customer_id")
    .where(
        (F.col("c.email") != F.col("s.email"))
        | (F.col("c.customer_segment") != F.col("s.customer_segment"))
    )
    .select("c.customer_sk")
)

changed_ids = [row.customer_sk for row in changed.collect()]
```

Interview guidance: the important part is not the exact hash function. It is that the update (close old versions), the insert (open new versions), and the current-flag invariant happen atomically, and that rerunning the job for the same source snapshot produces the same dimension.

[Table of Contents](#Data-Modeling)

## How do you model many-to-many relationships without breaking metrics?

Use a bridge table instead of joining dimensions directly in a way that multiplies fact rows. The bridge stores one row per relationship, and sometimes an allocation weight when measures need to be split.

Example:

```text
fact_order
  order_id, revenue

bridge_order_promotion
  order_id, promotion_id, allocation_weight

dim_promotion
  promotion_id, promotion_name
```

If one order has two promotions and revenue is 100, a weighted bridge might store two rows with `allocation_weight = 0.5`. Then promotion revenue is calculated as `sum(revenue * allocation_weight)`, avoiding accidental double counting.

Alternative pattern when weights are unknown: report "orders influenced by promotion" as a distinct count on the bridge instead of a revenue sum.

```sql
select p.promotion_name,
       count(distinct b.order_id) as influenced_orders
from bridge_order_promotion b
join dim_promotion p on p.promotion_sk = b.promotion_sk
group by p.promotion_name;
```

[Table of Contents](#Data-Modeling)

## What is a metric definition layer and why does it matter?

A metric definition layer centralizes how business metrics are calculated so dashboards, notebooks, and data products do not invent competing formulas. It defines the numerator, denominator, filters, grain, time dimension, and allowed dimensions.

Example:

```yaml
metric: net_revenue
base_table: fact_order_line
expression: sum(gross_amount - discount_amount - refund_amount)
time_dimension: order_date
allowed_dimensions:
  - dim_customer.customer_segment
  - dim_product.category
```

This matters because most metric disputes are modeling problems, not SQL syntax problems. Clear metric contracts also make refactoring safer because tests can compare old and new outputs for key slices.

A more complete contract also states the grain, the default time window, the owner, and what is explicitly excluded:

```yaml
metric: net_revenue
owner: finance-analytics
base_table: gold.fact_order_line
grain: order_line
expression: sum(gross_amount - discount_amount - refund_amount)
filters:
  - order_status <> 'cancelled'
time_dimension: order_date
default_window: last_28_days
allowed_dimensions:
  - dim_customer.customer_segment
  - dim_customer.country_code
  - dim_product.category
currency: USD
```

Whether you implement it with dbt metrics, a semantic layer (Cube, Looker, AtScale), or a table of pre-aggregated metrics, the contract is what stops three dashboards from shipping three revenue numbers.

[Table of Contents](#Data-Modeling)

## What is a Data Vault model?

Data Vault 2.0 is an insert-only modeling approach built from three constructs:

+ **Hubs** - the unique business keys (customer, product, order).
+ **Links** - the relationships between hubs (order -> customer).
+ **Satellites** - the descriptive attributes and their history, attached to a hub or link.

It is designed for large, multi-source, auditable warehouses where ingestion must be parallel and repeatable. Every table is insert-only, loads are idempotent by hash key, and history is preserved without the SCD bookkeeping of a dimensional model.

```sql
-- hub: one row per business key ever seen
create table hub_customer (
  customer_hk  binary(16) primary key,   -- hash of the business key
  customer_id  varchar(50) not null,
  load_ts      timestamp,
  record_source varchar(50)
);

-- link: relationship between hubs
create table link_order_customer (
  link_hk      binary(16) primary key,
  order_hk     binary(16),
  customer_hk  binary(16),
  load_ts      timestamp,
  record_source varchar(50)
);

-- satellite: attributes with full history
create table sat_customer_details (
  customer_hk  binary(16),
  load_ts      timestamp,
  hash_diff    binary(16),   -- hash of the tracked attributes
  customer_name varchar(200),
  segment      varchar(50),
  load_end_ts  timestamp,
  primary key (customer_hk, load_ts)
);
```

```python
# hub load: keep the first occurrence of each business key
from pyspark.sql import functions as F

incoming = spark.table("stg_customer").select("customer_id", "load_ts", "record_source")
incoming = incoming.withColumn("customer_hk", F.md5(F.concat_ws("||", "customer_id")))

new_keys = incoming.join(
    spark.table("hub_customer").select("customer_hk"), "customer_hk", "left_anti"
)

new_keys.write.mode("append").insertInto("hub_customer")
```

Trade-offs:

+ **For**: parallel loads, full audit history, easy multi-source integration, resilient to source changes.
+ **Against**: many tables and joins, poor for direct BI consumption, needs a dimensional or wide mart layer on top. Data Vault is an integration pattern, not a reporting model.

[Table of Contents](#Data-Modeling)

## How do you handle SCD Type 1 and Type 3?

**Type 1** overwrites the value and keeps no history. It is right for corrections and non-analytical attributes (typos, formatting, phone numbers) where the old value has no reporting value.

```sql
update dim_customer as tgt
set customer_name = src.customer_name,
    email         = src.email
from stg_customer src
where src.customer_id = tgt.customer_id
  and tgt.is_current;
```

**Type 3** keeps a limited history in extra columns, usually "current" and "previous". It is right when the business only ever compares the last change.

```sql
alter table dim_customer
  add column previous_segment varchar(50),
  add column segment_changed_at timestamp;

update dim_customer as tgt
set previous_segment   = tgt.customer_segment,
    customer_segment   = src.customer_segment,
    segment_changed_at = current_timestamp()
from stg_customer src
where src.customer_id = tgt.customer_id
  and tgt.is_current
  and tgt.customer_segment is distinct from src.customer_segment;
```

Guidance:

+ Type 1 is cheap but destroys as-of reporting; once history is gone it usually cannot be reconstructed.
+ Type 3 answers "what was it before?" only for one step; it cannot answer "what was it in March?".
+ If the business cannot state the retention requirement, default to Type 2 for analytical attributes and Type 1 for corrections.

[Table of Contents](#Data-Modeling)

## How do you handle late-arriving dimensions and facts?

Late-arriving data is normal in batch warehouses: a fact for 2026-09-15 lands on 2026-10-04, or a new customer first appears in a sales file before the customer feed has it.

For **late-arriving facts**, keep the event date in the fact and load into the correct partition. The dimension join must resolve "as of" the event date, not "as of" the load date:

```sql
select f.order_id,
       coalesce(d.customer_segment, 'UNKNOWN') as customer_segment,
       f.gross_amount
from fact_order f
left join dim_customer d
  on d.customer_id = f.customer_id
 and f.order_ts >= d.effective_start_at
 and f.order_ts <  d.effective_end_at;
```

For **late-arriving dimensions**, create an inferred or placeholder row at fact-load time (a "UNKNOWN" member keyed by the natural key), then update that row when the real description arrives:

```sql
-- inferred member: facts can join immediately, attributes filled in later
insert into dim_customer (customer_sk, customer_id, customer_name, is_current,
                          effective_start_at, effective_end_at, is_inferred)
select abs(hash(customer_id)), customer_id, 'UNKNOWN', true,
       timestamp '1900-01-01', timestamp '9999-12-31', true
from (select distinct customer_id from stg_order) s
where not exists (
  select 1 from dim_customer d where d.customer_id = s.customer_id
);
```

Then run the SCD2 merge when the real customer record arrives; because the placeholder used the same natural key, facts already loaded will join to the corrected version. Document that inferred rows are temporary, and add a metric for how many rows are still inferred so the gap is visible.

[Table of Contents](#Data-Modeling)

## What is a date dimension and a role-playing dimension?

A **date dimension** is one row per calendar day with pre-computed attributes: fiscal periods, week numbers, is_weekend, is_holiday, year-over-year comparison dates. It is the most common conformed dimension and it prevents every analyst from re-deriving fiscal calendars differently.

```sql
create table dim_date (
  date_sk       int primary key,      -- 20261004
  date_value    date not null,
  day_name      varchar(10),
  week_of_year  int,
  month_name    varchar(10),
  year_month    char(7),              -- 2026-10
  fiscal_quarter varchar(10),
  is_weekend    boolean,
  is_holiday    boolean,
  same_day_last_year date
);
```

A **role-playing dimension** is the same physical dimension used several times in one fact with different meanings. Classic examples: `order_date`, `ship_date`, and `delivery_date` all point at `dim_date`; `origin_airport` and `destination_airport` both point at `dim_airport`.

```sql
select dd.year_month as order_month,
       ds.year_month as ship_month,
       count(*)      as orders
from fact_order f
join dim_date dd on dd.date_sk = f.order_date_sk
join dim_date ds on ds.date_sk = f.ship_date_sk
group by 1, 2;
```

Implementation options: join the same table with aliases (simple, what BI tools expect), or publish views named `dim_order_date`, `dim_ship_date`. Prefer aliases and document the roles in the semantic layer; do not physically duplicate the date dimension.

[Table of Contents](#Data-Modeling)

## Kimball vs Inmon: which modeling approach should you use?

| Aspect | Kimball (bottom-up) | Inmon (top-down) |
|---|---|---|
| Starting point | business processes and marts | enterprise-wide normalized model |
| Core structure | facts and dimensions | 3NF integration layer |
| Time to first value | fast (one mart) | slow (enterprise model first) |
| Consistency | conformed dimensions and bus matrix | enforced by the central model |
| Storage | some redundancy in dimensions | minimal redundancy |
| Best fit | BI-led, iterative delivery | large regulated enterprises with many sources |

A pragmatic hybrid is the most common answer in interviews:

1. Land raw data (bronze).
2. Normalize and conform in an integration layer (silver) - Inmon's discipline.
3. Publish dimensional marts (gold) with a bus matrix of conformed dimensions - Kimball's delivery model.

The **bus matrix** is the artifact that ties them together: rows are business processes, columns are conformed dimensions, and every cell marks whether a process captures that dimension. If a dashboard needs a slice that no cell provides, that is a modeling gap, not a SQL problem.

```text
                 dim_date  dim_customer  dim_product  dim_store
fact_order_line     X          X             X            X
fact_payment        X          X                          X
fact_inventory      X                        X            X
```

[Table of Contents](#Data-Modeling)

## Real world use cases for data modeling

### 1. Retail: order-line star with weighted promotion attribution

A retailer with ~40M order lines/month in Postgres needs margin reporting by category, store, and promotion. Order data is one row per line; promotions are many-to-many with orders and need revenue attribution.

```sql
create table fact_order_line (
  order_line_sk bigint primary key,
  order_id      varchar(50),
  customer_sk   bigint,
  product_sk    bigint,
  store_sk      bigint,
  order_date_sk int,
  quantity      int,
  gross_amount  numeric(14,2),
  discount_amount numeric(14,2),
  cost_amount   numeric(14,2)
);

-- attributed revenue: one order can have several promotions
select p.promotion_name,
       sum((f.gross_amount - f.discount_amount) * b.allocation_weight) as net_revenue
from fact_order_line f
join bridge_order_promotion b on b.order_id = f.order_id
join dim_promotion p          on p.promotion_sk = b.promotion_sk
join dim_date d               on d.date_sk = f.order_date_sk
where d.year_month = '2026-09'
group by p.promotion_name;
```

Why: the bridge keeps promotion revenue from double counting, the conformed date and product dimensions let margin roll up, and the star keeps the BI query to three joins.

### 2. Fintech: SCD2 customer dimension for regulator reporting

A payments company must report a customer's risk tier **as of** each transaction date, with a 7-year audit requirement. Customer attributes change a few thousand times a day across 12M customers.

```sql
select t.transaction_id,
       c.customer_segment   as segment_at_transaction,
       c.risk_tier          as risk_tier_at_transaction,
       t.amount
from fact_transaction t
join dim_customer c
  on c.customer_id = t.customer_id
 and t.transaction_ts >= c.effective_start_at
 and t.transaction_ts <  c.effective_end_at;
```

Why SCD2: reproducing a historical report requires the attribute values that were true then. Type 1 would silently rewrite history and fail the audit; the range join is the price of correctness.

### 3. SaaS: multi-tenant fact with tenant-scoped dimensions

A B2B SaaS platform serves 2,000 tenants and must never leak one tenant's data into another's dashboard. Every fact and dimension carries `tenant_sk`, and row-level security filters on it.

```sql
create table fact_usage_daily (
  tenant_sk bigint,
  account_sk bigint,
  usage_date_sk int,
  api_calls bigint,
  storage_gb numeric(12,2),
  primary key (tenant_sk, account_sk, usage_date_sk)
);

-- the tenant predicate is mandatory on every query
select d.usage_date, sum(f.api_calls)
from fact_usage_daily f
join dim_date d on d.date_sk = f.usage_date_sk
where f.tenant_sk = current_setting('app.tenant_sk')::bigint
group by d.usage_date;
```

Why: putting the tenant key at the lowest grain keeps the partition-pruning and row-level-security story simple, and it prevents cross-tenant joins from ever matching.

### 4. Marketing: factless coverage fact for campaign eligibility

A marketing team needs to answer "which customers were eligible for a campaign but did not convert?" Eligibility is not a numeric event, so it is modeled as a factless fact joined against conversions.

```sql
create table fact_campaign_eligibility (
  campaign_sk bigint,
  customer_sk bigint,
  date_sk     int
);

select count(distinct e.customer_sk) as eligible,
       count(distinct c.customer_sk) as converted
from fact_campaign_eligibility e
left join fact_conversion c
  on c.customer_sk = e.customer_sk
 and c.campaign_sk = e.campaign_sk
where e.campaign_sk = 42;
```

Why factless: there is no measure to sum, only the existence of a relationship. A factless fact is the cleanest way to store coverage and answer "what did not happen".

### 5. Logistics: accumulating snapshot for shipment milestones

A logistics company tracks each shipment from booking to delivery and reports stage durations daily. The process has a fixed set of milestones, so an accumulating snapshot updates one row per shipment as each milestone is reached.

```sql
update fact_shipment
set picked_up_date_sk  = 20261004,
    delivered_date_sk  = case when delivered_at is not null then 20261005 else delivered_date_sk end,
    days_in_transit    = datediff(day, booked_at, delivered_at)
where shipment_id = 'SHP-9001';
```

Why: accumulating snapshots make process-duration and pipeline-lag questions cheap (`avg(days_in_transit)`) without scanning an event stream, at the cost of in-place updates that must be idempotent.

[Table of Contents](#Data-Modeling)
