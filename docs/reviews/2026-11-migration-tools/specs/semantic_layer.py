import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# Semantic layer

Finance says March revenue was 935.50. The sales dashboard says 1,265.50. The product team's notebook says
1,155.50. Nobody made an arithmetic error: each wrote its own SQL, one subtracting refunds, one counting cancelled
orders, one excluding tax. A **semantic layer** defines each metric once, with its filters, joins and allowed
dimensions, and generates the SQL for every tool that asks.

This lesson builds a tiny semantic layer over DuckDB: metric definitions as data, a compiler that turns a request
("revenue by region by month") into SQL, ratio and distinct-count metrics that aggregate correctly, a guard against
join fan-out, and tests that keep definitions honest. It ends with how dbt's MetricFlow, Cube, LookML and warehouse
semantic views express the same ideas.

*Last reviewed: November 2026, against the dbt Semantic Layer (MetricFlow) and Cube documentation.*

**Prerequisites:** [Data modeling 9: testing, metrics and change](../data-modeling/data-modeling-09-testing-metrics-and-change.ipynb)
and [Data modeling 4: relationships and double counting](../data-modeling/data-modeling-04-relationships-and-double-counting.ipynb).
%% code
# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
!pip install -q duckdb~=2.0
%% md
## Setup and sample data

The cell creates a small star schema: `fct_orders` (one row per order, with gross amount, tax, refund and status),
`dim_customers` (one row per customer, with region and segment) and `fct_order_items` (one row per item on an
order), which is used later to show what goes wrong with a one-to-many join.
%% code
import duckdb

con = duckdb.connect()
con.sql("""
create table dim_customers as select * from (values
    ('C1', 'North', 'smb'), ('C2', 'South', 'enterprise'), ('C3', 'North', 'enterprise'), ('C4', 'West', 'smb')
) t(customer_id, region, segment);

create table fct_orders as select * from (values
    (1, 'C1', date '2026-03-02', 'complete',  120.00, 20.00,  0.00),
    (2, 'C2', date '2026-03-05', 'complete',  300.00, 50.00, 40.00),
    (3, 'C1', date '2026-03-11', 'cancelled', 110.00, 10.00,  0.00),
    (4, 'C3', date '2026-03-18', 'complete',  250.00, 30.00,  0.00),
    (5, 'C4', date '2026-03-27', 'complete',  485.50, 50.00, 30.00),
    (6, 'C2', date '2026-04-03', 'complete',  200.00, 25.00,  0.00),
    (7, 'C1', date '2026-04-09', 'complete',   90.00, 10.00, 80.00)
) t(order_id, customer_id, order_date, status, gross_amount, tax, refund);

create table fct_order_items as select * from (values
    (1, 'mug', 2), (1, 'tea', 1), (2, 'coffee', 5), (4, 'kettle', 1), (4, 'mug', 4), (5, 'coffee', 10), (6, 'tea', 3), (7, 'mug', 1)
) t(order_id, product, quantity);
""")
con.sql("select * from fct_orders order by order_id").show()
%% md
## One metric, three answers

Without a shared definition, every query re-decides what "revenue" means: gross or net of tax, before or after
refunds, with or without cancelled orders, by order date or payment date. Each choice is defensible; mixing them
across dashboards destroys trust.

**Where it matters**
- Any metric reported by more than one team or tool: revenue, active users, churn, margin.

**Watch out for**
- A definition that lives only in a dashboard's SQL: nobody can find it, test it or reuse it.
%% md
### Ask three teams for March revenue

Each query is reasonable on its own.
%% code
queries = {
    "sales (gross, all orders)": "select sum(gross_amount) from fct_orders where order_date between '2026-03-01' and '2026-03-31'",
    "product (gross, complete)": "select sum(gross_amount) from fct_orders where status = 'complete' and order_date between '2026-03-01' and '2026-03-31'",
    "finance (net of tax and refunds)": "select sum(gross_amount - tax - refund) from fct_orders where status = 'complete' and order_date between '2026-03-01' and '2026-03-31'",
}
for team, sql in queries.items():
    print(f"{team:34} {con.sql(sql).fetchall()[0][0]:>9}")
%% md
**What to notice:** Three different numbers for the same month: 1,265.50 including the cancelled order, 1,155.50
without it, and 935.50 net of tax and refunds. The layer's job is to give each of these a name (`gross_bookings`,
`net_revenue`) and one definition, so a dashboard can say which one it shows.
%% md
## Metrics as definitions, not queries

A semantic layer separates **what** a metric is from **how** a particular question is answered. A definition says:
the table it comes from, the expression and aggregation, the filters that always apply, the time column, and the
dimensions it can be sliced by (and through which joins). A compiler then builds the SQL for any allowed
combination of metric, dimensions, time grain and filters.

**Where it matters**
- Serving the same numbers to BI tools, notebooks, spreadsheets and AI assistants through one API.

**Watch out for**
- Pushing every report-specific tweak into the layer: keep it to shared, governed definitions.
%% md
### Define metrics and dimensions as data

Two simple metrics, the dimensions they can use, and the join that reaches each dimension.
%% code
SEMANTIC_MODEL = {
    "table": "fct_orders",
    "time_column": "order_date",
    "joins": {"dim_customers": {"on": "fct_orders.customer_id = dim_customers.customer_id", "relationship": "many_to_one"}},
    "dimensions": {"region": "dim_customers.region", "segment": "dim_customers.segment", "status": "fct_orders.status"},
    "metrics": {
        "gross_bookings": {"agg": "sum", "expr": "gross_amount", "filter": None},
        "net_revenue": {"agg": "sum", "expr": "gross_amount - tax - refund", "filter": "status = 'complete'"},
        "orders": {"agg": "count", "expr": "order_id", "filter": "status = 'complete'"},
    },
}
for name, metric in SEMANTIC_MODEL["metrics"].items():
    print(f"{name:15} {metric['agg']}({metric['expr']})  where {metric['filter']}")
%% md
**What to notice:** The definitions hold no dimension and no date range: those belong to each question. The filter
on `status` is part of `net_revenue` itself, so no query can forget it.
%% md
### Compile a request into SQL

`compile_query` builds the SQL for one or more simple metrics, a time grain and dimensions. Each metric's filter
becomes a `filter (where ...)` clause on its own aggregate, so metrics with different filters can share a query.
%% code
def compile_query(metrics, dimensions=(), grain=None, where=None, model=SEMANTIC_MODEL):
    select, group, joins = [], [], set()
    if grain:
        select.append(f"date_trunc('{grain}', {model['time_column']})::date as {grain}")
        group.append(grain)
    for dim in dimensions:
        column = model["dimensions"][dim]
        table = column.split(".")[0]
        if table != model["table"]:
            joins.add(table)
        select.append(f"{column} as {dim}")
        group.append(dim)
    for name in metrics:
        metric = model["metrics"][name]
        aggregate = f"{metric['agg']}({metric['expr']})"
        if metric["filter"]:
            aggregate += f" filter (where {metric['filter']})"
        select.append(f"{aggregate} as {name}")
    sql = f"select {', '.join(select)}\nfrom {model['table']}"
    for table in sorted(joins):
        sql += f"\njoin {table} on {model['joins'][table]['on']}"
    if where:
        sql += f"\nwhere {where}"
    if group:
        sql += f"\ngroup by {', '.join(group)}\norder by {', '.join(group)}"
    return sql


sql = compile_query(["gross_bookings", "net_revenue"], dimensions=["region"], grain="month")
print(sql)
con.sql(sql).show()
%% md
**What to notice:** One request produced a query that joins the customer dimension only because `region` was asked
for, and gives each metric its own filter. March totals across regions are 1,265.50 gross and 935.50 net, the same as
the sales and finance numbers above, but now both are named and come from one definition. North's net revenue in
April is 0.00: order 7's refund cancelled its whole net amount.
%% md
## Ratios and distinct counts

Some metrics cannot be summed from smaller pieces:

- A **ratio** such as average order value is `sum(net_revenue) / count(orders)` at the requested grain. Averaging
  per-region averages weights a region with one order the same as a region with a hundred.
- A **distinct count** such as active customers cannot be added across days or regions: a customer active on two
  days is one customer for the month.

The layer defines these as **derived** metrics over simple ones and always recomputes them from the base rows at the
requested grain.

**Where it matters**
- Conversion rates, averages, margins, active users: the metrics most often reported wrong.

**Watch out for**
- Pre-aggregated tables of ratios or distinct counts: they cannot be rolled up further.
%% md
### Compute average order value two ways

Add a ratio metric and a distinct-count metric, then compare the correct total with an average of averages.
%% code
SEMANTIC_MODEL["metrics"]["customers"] = {"agg": "count", "expr": "distinct fct_orders.customer_id", "filter": "status = 'complete'"}
SEMANTIC_MODEL["derived"] = {"avg_order_value": ("net_revenue", "orders")}


def compile_derived(name, dimensions=(), grain=None):
    numerator, denominator = SEMANTIC_MODEL["derived"][name]
    inner = compile_query([numerator, denominator], dimensions, grain)
    keys = ([grain] if grain else []) + list(dimensions)
    cols = ", ".join(keys + [f"round({numerator} / nullif({denominator}, 0), 2) as {name}"])
    return f"select {cols} from ({inner})"


by_region = con.sql(compile_derived("avg_order_value", ["region"])).fetchall()
print("AOV by region:", by_region)
print("AOV overall (correct):", con.sql(compile_derived("avg_order_value")).fetchall()[0][0])
print("average of regional AOVs:", round(sum(r[1] for r in by_region) / len(by_region), 2))
print("customers per month:", con.sql(compile_query(["customers"], grain="month")).fetchall())
print("customers in total: ", con.sql(compile_query(["customers"])).fetchall()[0][0])
%% md
**What to notice:** The correct average order value is 185.08 (1,110.50 of net revenue over 6 complete orders).
Averaging the three regional values gives 234.89, because West's single large order counts as much as North's three
smaller ones. Distinct customers are 4 in March and 2 in April, but 4 in total, not 6: C1 and C2 ordered in both
months.
%% md
## Guard against join fan-out

A metric defined on `fct_orders` is only correct if every join adds **at most one row per order**. Joining to
`dim_customers` is many-to-one and safe. Joining to `fct_order_items` (one-to-many) repeats each order once per item
and inflates every sum. A semantic layer records the relationship of each join and refuses, or rewrites, a request
that would fan out.

**Where it matters**
- Letting business users combine any dimension with any metric without knowing the joins.

**Watch out for**
- Tools that silently allow one-to-many joins; Looker's symmetric aggregates and MetricFlow's entity joins exist to
  prevent exactly this.
%% md
### Slice revenue by product, naively and with a guard

Add `product` as a dimension through the items table, run the naive query, then let the compiler check the
relationship first.
%% code
SEMANTIC_MODEL["joins"]["fct_order_items"] = {"on": "fct_orders.order_id = fct_order_items.order_id", "relationship": "one_to_many"}
SEMANTIC_MODEL["dimensions"]["product"] = "fct_order_items.product"

naive = compile_query(["net_revenue"], where="order_date < '2026-04-01'")
naive_by_product = compile_query(["net_revenue"], dimensions=["product"], where="order_date < '2026-04-01'")
print("March net revenue:", con.sql(naive).fetchall()[0][0])
print("summed over products:", sum(r[1] or 0 for r in con.sql(naive_by_product).fetchall()))


def checked_compile(metrics, dimensions=(), **kwargs):
    for dim in dimensions:
        table = SEMANTIC_MODEL["dimensions"][dim].split(".")[0]
        join = SEMANTIC_MODEL["joins"].get(table)
        if join and join["relationship"] != "many_to_one":
            raise ValueError(f"{dim!r} is reached through a {join['relationship']} join: {metrics} would be counted once per row of {table}")
    return compile_query(metrics, dimensions, **kwargs)


try:
    checked_compile(["net_revenue"], ["product"])
except ValueError as error:
    print("refused:", error)
%% md
**What to notice:** March net revenue is 935.50, but summing the naive per-product rows gives 1,255.50: orders 1
and 4 have two items each, so their net revenue (100.00 and 220.00) was counted twice. The checked compiler refuses
the request and says why. To report revenue by product correctly you need a metric defined at the item grain (item
revenue), not the order metric pushed through a one-to-many join.
%% md
## Test the definitions

Metric definitions are code and need tests: a fixture with known answers, and consistency checks such as "the sum
over regions equals the total" for additive metrics. Run them in CI when a definition changes, and publish the
definitions where people can read them.

**Where it matters**
- Changing a definition (excluding a new order status) without breaking every dashboard silently.

**Watch out for**
- Consistency checks applied to non-additive metrics: distinct counts per region legitimately sum to more than the
  total.
%% md
### Check additivity and known values

Compare each metric's total with the sum over regions, and check net revenue against a value finance signed off.
%% code
for metric in ["gross_bookings", "net_revenue", "orders", "customers"]:
    total = con.sql(compile_query([metric])).fetchall()[0][0]
    by_region = sum(r[1] for r in con.sql(compile_query([metric], ["region"])).fetchall())
    print(f"{metric:15} total {total:>9}  sum over regions {by_region:>9}  {'additive' if total == by_region else 'NOT additive'}")

march_net = con.sql(compile_query(["net_revenue"], where="order_date between '2026-03-01' and '2026-03-31'")).fetchall()[0][0]
signed_off = 935.50
print(f"net revenue March: {march_net} (finance signed off {signed_off}) -> {'ok' if march_net == signed_off else 'MISMATCH'}")
%% md
**What to notice:** Gross bookings, net revenue and orders add up across regions, as additive metrics must.
`customers` also matches here, but only because every customer belongs to exactly one region; across months it does
not add up (4 + 2 is not 4), so an additivity test must not be applied to it. The March value matches the
signed-off 935.50, so a change to the definition that moved it would fail this test.
%% md
## The tools

| Tool | How metrics are defined | Served to |
|---|---|---|
| dbt Semantic Layer (MetricFlow) | YAML: semantic models (entities, dimensions, measures) and metrics (simple, ratio, cumulative, derived) | BI tools and notebooks through APIs and integrations |
| Cube | JavaScript or YAML cubes with measures, dimensions and joins; caching with pre-aggregations | SQL, REST and GraphQL APIs |
| LookML (Looker) | Views and explores with dimensions, measures and join relationships | Looker, and other tools through its SQL interface |
| Warehouse-native | Snowflake semantic views, Databricks metric views | SQL clients and the platform's AI assistants |

```yaml
# dbt MetricFlow: the net_revenue metric above
semantic_models:
  - name: orders
    model: ref('fct_orders')
    defaults: {agg_time_dimension: order_date}
    entities:
      - {name: order, type: primary, expr: order_id}
      - {name: customer, type: foreign, expr: customer_id}
    dimensions:
      - {name: order_date, type: time, type_params: {time_granularity: day}}
      - {name: status, type: categorical}
    measures:
      - {name: net_amount, agg: sum, expr: "gross_amount - tax - refund"}
      - {name: order_count, agg: count, expr: order_id}
metrics:
  - name: net_revenue
    type: simple
    type_params: {measure: net_amount}
    filter: "{{ Dimension('order__status') }} = 'complete'"
```

**Where it matters**
- Choosing where definitions live: next to the transformations (dbt), in a serving layer (Cube), or in the BI tool.

**Watch out for**
- Defining the same metric in dbt and in the BI tool: two definitions drift apart again.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** What belongs in a metric's definition, and what belongs in a request?

**A.** The definition holds the source, expression, aggregation, always-on filters, time column and allowed dimensions. The request holds the dimensions, grain and ad hoc filters for one question.

**Q2.** Why is the average of regional averages different from the overall average order value?

**A.** It gives each region equal weight regardless of how many orders it has. The ratio must be computed as total revenue over total orders at the requested grain.

**Q3.** A dashboard shows monthly active customers per week and sums them for the month. What is wrong?

**A.** Distinct counts are not additive: a customer active in two weeks is counted twice. Compute the distinct count at the month grain from the base rows.

**Q4.** Why should a semantic layer know each join's relationship?

**A.** To refuse or rewrite requests that join a metric's table to a one-to-many table, which would repeat rows and inflate the metric.

**Q5.** How do you keep a metric definition from changing silently?

**A.** Keep it in version control, test it against fixtures with signed-off values and consistency checks in CI, and publish the definition where consumers can read it.
%% md
## Key takeaways

- A semantic layer defines each metric once, including its filters, and compiles SQL for every question and tool.
- Requests add dimensions, grains and filters; definitions never change per report.
- Ratios and distinct counts are recomputed from base rows at the requested grain, never summed or averaged.
- Record join relationships so the layer can refuse one-to-many fan-out.
- Test definitions against signed-off values and additivity, and keep them in one place.
%% md
**Next:** Continue with [Looker](../looker/looker.ipynb) for a BI tool built around a semantic layer, or
[dbt](../dbt/dbt.ipynb) for the transformations underneath.
'''

build("notebooks/topics/concepts/semantic-layer.ipynb", SPEC)
