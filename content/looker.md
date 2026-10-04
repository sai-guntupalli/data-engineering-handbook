## [Main title](../README.md)
### [Interview questions](full.md)

# Looker

**Notebook:** [`notebooks/topics/looker.ipynb`](../notebooks/topics/looker.ipynb) - runnable version of this topic with self-checking exercises.

Looker (Google Cloud Looker) is a BI and embedded-analytics platform whose semantic layer, LookML, is version-controlled code: it defines views, explores, dimensions, measures, and access rules, and Looker generates SQL against the warehouse at query time.

+ [What is Looker?](#What-is-Looker)
+ [What is LookML and why does it matter?](#What-is-LookML-and-why-does-it-matter)
+ [How do you avoid fanout problems in Looker?](#How-do-you-avoid-fanout-problems-in-Looker)
+ [How does Looker handle data integration?](#How-does-Looker-handle-data-integration)
+ [Can you explain the concept of a LookML model in Looker?](#Can-you-explain-the-concept-of-a-LookML-model-in-Looker)
+ [What is a dimension in Looker?](#What-is-a-dimension-in-Looker)
+ [How can you create a calculated field in Looker?](#How-can-you-create-a-calculated-field-in-Looker)
+ [What is a Looker Explore?](#What-is-a-Looker-Explore)
+ [What is the purpose of a Looker dashboard?](#What-is-the-purpose-of-a-Looker-dashboard)
+ [Can Looker handle real-time data?](#Can-Looker-handle-real-time-data)
+ [How does Looker handle data security?](#How-does-Looker-handle-data-security)
+ [What is the purpose of a Looker filter?](#What-is-the-purpose-of-a-Looker-filter)
+ [Can you explain the concept of Looker PDTs (Persistent Derived Tables)?](#Can-you-explain-the-concept-of-Looker-PDTs-Persistent-Derived-Tables)
+ [How can you schedule data deliveries in Looker?](#How-can-you-schedule-data-deliveries-in-Looker)
+ [How does Looker handle data caching?](#How-does-Looker-handle-data-caching)
+ [Can Looker be used for data transformation and ETL processes?](#Can-Looker-be-used-for-data-transformation-and-ETL-processes)
+ [How does Looker handle data lineage and documentation?](#How-does-Looker-handle-data-lineage-and-documentation)
+ [What are some ways to optimize Looker performance?](#What-are-some-ways-to-optimize-Looker-performance)
+ [Can Looker connect to non-SQL data sources?](#Can-Looker-connect-to-non-SQL-data-sources)
+ [What is the purpose of Looker's Data Actions?](#What-is-the-purpose-of-Lookers-Data-Actions)
+ [Can Looker handle large-scale data processing?](#Can-Looker-handle-large-scale-data-processing)
+ [How does Looker support collaboration among team members?](#How-does-Looker-support-collaboration-among-team-members)
+ [What are some limitations of Looker?](#What-are-some-limitations-of-Looker)
+ [Can Looker handle unstructured or semi-structured data?](#Can-Looker-handle-unstructured-or-semi-structured-data)
+ [How does Looker handle data versioning and change management?](#How-does-Looker-handle-data-versioning-and-change-management)
+ [What is Looker's scheduling and alerting capability?](#What-is-Lookers-scheduling-and-alerting-capability)
+ [Can Looker be integrated with other BI tools or data visualization platforms?](#Can-Looker-be-integrated-with-other-BI-tools-or-data-visualization-platforms)
+ [What are some advantages of using Looker compared to traditional BI tools?](#What-are-some-advantages-of-using-Looker-compared-to-traditional-BI-tools)
+ [How can you create a custom visualization in Looker?](#How-can-you-create-a-custom-visualization-in-Looker)
+ [What is Looker's Explore API used for?](#What-is-Lookers-Explore-API-used-for)
+ [How does Looker handle data governance and compliance?](#How-does-Looker-handle-data-governance-and-compliance)
+ [Can Looker handle geospatial data analysis?](#Can-Looker-handle-geospatial-data-analysis)
+ [What is Looker's Explore Permissions feature?](#What-is-Lookers-Explore-Permissions-feature)
+ [Can Looker handle streaming data sources?](#Can-Looker-handle-streaming-data-sources)
+ [What are some best practices for optimizing Looker performance?](#What-are-some-best-practices-for-optimizing-Looker-performance)
+ [How does Looker handle data lineage and impact analysis?](#How-does-Looker-handle-data-lineage-and-impact-analysis)
+ [Can you explain Looker's dynamic time frame filters?](#Can-you-explain-Lookers-dynamic-time-frame-filters)
+ [How does Looker handle data security in a cloud-based environment?](#How-does-Looker-handle-data-security-in-a-cloud-based-environment)
+ [What are the advantages of using Looker's embedded analytics feature?](#What-are-the-advantages-of-using-Lookers-embedded-analytics-feature)
+ [Can Looker handle multi-tenant data environments?](#Can-Looker-handle-multi-tenant-data-environments)
+ [How does Looker handle data modeling for complex data structures?](#How-does-Looker-handle-data-modeling-for-complex-data-structures)
+ [Can Looker connect to cloud-based data warehouses like Amazon Redshift or Google BigQuery?](#Can-Looker-connect-to-cloud-based-data-warehouses-like-Amazon-Redshift-or-Google-BigQuery)
+ [How does Looker handle data governance in a self-service environment?](#How-does-Looker-handle-data-governance-in-a-self-service-environment)
+ [What are some advanced analytical capabilities offered by Looker?](#What-are-some-advanced-analytical-capabilities-offered-by-Looker)
+ [Can you explain Looker's data modeling best practices?](#Can-you-explain-Lookers-data-modeling-best-practices)
+ [How can Looker integrate with data orchestration tools like Apache Airflow?](#How-can-Looker-integrate-with-data-orchestration-tools-like-Apache-Airflow)
+ [Can Looker handle multi-language support for international users?](#Can-Looker-handle-multi-language-support-for-international-users)
+ [What is the purpose of Looker's SQL Runner?](#What-is-the-purpose-of-Lookers-SQL-Runner)
+ [How does Looker handle data replication and synchronization?](#How-does-Looker-handle-data-replication-and-synchronization)
+ [Can Looker generate alerts or notifications based on predefined conditions?](#Can-Looker-generate-alerts-or-notifications-based-on-predefined-conditions)
+ [What is the difference between Looker's explore and join types?](#What-is-the-difference-between-Lookers-explore-and-join-types)
+ [How does Looker handle data partitioning and sharding?](#How-does-Looker-handle-data-partitioning-and-sharding)
+ [Can you explain Looker's data permissions and access controls?](#Can-you-explain-Lookers-data-permissions-and-access-controls)
+ [How can Looker handle data lineage in a complex data ecosystem?](#How-can-Looker-handle-data-lineage-in-a-complex-data-ecosystem)
+ [Can Looker handle near real-time data analysis?](#Can-Looker-handle-near-real-time-data-analysis)
+ [How does Looker handle data quality and cleansing?](#How-does-Looker-handle-data-quality-and-cleansing)
+ [What is the purpose of Looker's content validation feature?](#What-is-the-purpose-of-Lookers-content-validation-feature)
+ [Can Looker integrate with external authentication providers?](#Can-Looker-integrate-with-external-authentication-providers)
+ [How does Looker handle data privacy and compliance requirements?](#How-does-Looker-handle-data-privacy-and-compliance-requirements)
+ [Can Looker perform predictive analytics or machine learning?](#Can-Looker-perform-predictive-analytics-or-machine-learning)
+ [What is the purpose of Looker's PDT (Persistent Derived Tables) Events?](#What-is-the-purpose-of-Lookers-PDT-Persistent-Derived-Tables-Events)
+ [How does Looker handle data virtualization?](#How-does-Looker-handle-data-virtualization)
+ [Can you explain Looker's dynamic data masking feature?](#Can-you-explain-Lookers-dynamic-data-masking-feature)
+ [How can Looker integrate with data governance tools?](#How-can-Looker-integrate-with-data-governance-tools)
+ [What is Looker's Explore Embed feature used for?](#What-is-Lookers-Explore-Embed-feature-used-for)
+ [How does Looker handle data lineage for derived or calculated fields?](#How-does-Looker-handle-data-lineage-for-derived-or-calculated-fields)
+ [Can Looker handle data visualization in real-time dashboards?](#Can-Looker-handle-data-visualization-in-real-time-dashboards)
+ [What is the purpose of Looker's Action Hub?](#What-is-the-purpose-of-Lookers-Action-Hub)
+ [Can Looker handle data anomaly detection?](#Can-Looker-handle-data-anomaly-detection)
+ [How does Looker handle data lineage for transformations applied outside of Looker?](#How-does-Looker-handle-data-lineage-for-transformations-applied-outside-of-Looker)
+ [What is the purpose of Looker's PDT (Persistent Derived Tables) Performance Optimization?](#What-is-the-purpose-of-Lookers-PDT-Persistent-Derived-Tables-Performance-Optimization)
+ [Can Looker handle incremental data loads?](#Can-Looker-handle-incremental-data-loads)
+ [How does Looker handle data versioning and change tracking in LookML models?](#How-does-Looker-handle-data-versioning-and-change-tracking-in-LookML-models)
+ [Can Looker be deployed on-premises or is it only available as a cloud-based solution?](#Can-Looker-be-deployed-on-premises-or-is-it-only-available-as-a-cloud-based-solution)
+ [What is the purpose of Looker's Liquid syntax in LookML?](#What-is-the-purpose-of-Lookers-Liquid-syntax-in-LookML)
+ [How does Looker handle data storage and scalability?](#How-does-Looker-handle-data-storage-and-scalability)
+ [Can Looker integrate with data cataloging tools?](#Can-Looker-integrate-with-data-cataloging-tools)
+ [What is the purpose of Looker's "Always Use SQL Runner" option?](#What-is-the-purpose-of-Lookers-Always-Use-SQL-Runner-option)
+ [How does Looker handle data replication for disaster recovery purposes?](#How-does-Looker-handle-data-replication-for-disaster-recovery-purposes)
+ [Can Looker handle data exploration on semi-structured data formats like JSON or XML?](#Can-Looker-handle-data-exploration-on-semi-structured-data-formats-like-JSON-or-XML)
+ [What is the purpose of Looker's Advanced Scheduling options?](#What-is-the-purpose-of-Lookers-Advanced-Scheduling-options)
+ [How does Looker handle user access controls in a multi-tenant environment?](#How-does-Looker-handle-user-access-controls-in-a-multi-tenant-environment)
+ [Can Looker be integrated with data lake platforms like Hadoop or Amazon S3?](#Can-Looker-be-integrated-with-data-lake-platforms-like-Hadoop-or-Amazon-S3)
+ [What is the purpose of Looker's Development Mode?](#What-is-the-purpose-of-Lookers-Development-Mode)
+ [Real world use cases for Looker](#Real-world-use-cases-for-Looker)

## What is Looker?

Looker is a business intelligence (BI) and data visualization platform that allows users to explore, analyze, and share data insights.

Architecturally, Looker is a SQL generator plus a semantic model, not a data store: queries run in the connected warehouse, and LookML decides which SQL runs. That is why governance, metric consistency, and performance tuning all live in the modeling layer rather than in individual dashboards.

[Table of Contents](#Looker)

## What is LookML and why does it matter?

LookML is Looker's semantic modeling layer. It defines explores, views, joins, dimensions, measures, access rules, and reusable business logic. This helps teams centralize metric definitions instead of rebuilding them in each dashboard.

Example:

```text
measure: total_revenue {
  type: sum
  sql: ${amount} ;;
}
```

Strong LookML keeps BI consistent: "revenue" should mean the same thing across dashboards. A fuller example shows how dimensions, time frames, and measures compose in one view:

```text
view: orders {
  sql_table_name: analytics.fct_orders ;;

  dimension: order_id { primary_key: yes type: string sql: ${TABLE}.order_id ;; }

  dimension_group: created {
    type: time
    timeframes: [date, week, month, quarter, year]
    datatype: timestamp
    sql: ${TABLE}.created_at ;;
  }

  dimension: country { type: string sql: ${TABLE}.country ;; }

  measure: total_revenue {
    type: sum
    value_format_name: usd
    sql: ${TABLE}.amount ;;
  }

  measure: order_count { type: count_distinct sql: ${TABLE}.order_id ;; }

  measure: average_order_value {
    type: number
    value_format_name: usd
    sql: ${total_revenue} / NULLIF(${order_count}, 0) ;;
  }
}
```

Trade-off: LookML makes metrics reusable and testable (a Git diff shows a metric change), but it adds a modeling step and a deployment workflow, so it slows down purely exploratory one-off analysis compared with a tool that lets analysts write raw SQL freely.

[Table of Contents](#Looker)

## How do you avoid fanout problems in Looker?

Fanout happens when joins multiply rows and inflate measures. Prevent it by modeling correct join relationships, using aggregate-aware explores, pre-aggregating facts, or separating explores by grain.

Example:

```text
join: customers {
  type: left_outer
  relationship: many_to_one
  sql_on: ${orders.customer_id} = ${customers.customer_id} ;;
}
```

If the relationship is actually many-to-many, a bridge or aggregate table may be needed before exposing the data to users.

Two mechanisms protect you even when fanout is real. Symmetric aggregates make a `type: sum` correct across a join by aggregating the distinct primary keys first, and a `sql_distinct_key` makes a measure fanout-aware:

```text
measure: total_revenue {
  type: sum
  sql: ${TABLE}.amount ;;
  sql_distinct_key: ${order_id} ;;   # deduplicate at order grain before summing
}

measure: revenue_per_customer {
  type: number
  sql: ${total_revenue} / NULLIF(${customers.count}, 0) ;;
}
```

Fanout with `type: count_distinct` is a common trap: a count of distinct rows survives the join, but a `type: sum` doubles unless a distinct key is given. When NOT to rely on symmetric aggregates: the measure is over a pre-aggregated table where the primary key is no longer at the row grain; there, aggregate before joining or use separate explores.

[Table of Contents](#Looker)

## How does Looker handle data integration?

Looker connects to various data sources using database dialects and APIs, allowing it to integrate with different data platforms such as SQL databases, cloud storage, and data warehouses.

Looker talks SQL to a warehouse; it does not ingest data. Integration therefore means: a connection (with a service account or JDBC/ODBC credentials), a dialect (BigQuery, Snowflake, Redshift, Postgres, Databricks, etc.), and a LookML project whose `sql_table_name` points at warehouse objects. For files in a data lake, you expose them through the warehouse (external tables, Iceberg, BigLake, Delta sharing).

```text
connection: "acme_bigquery"

include: "/views/*.view.lkml"

explore: orders {
  view_name: orders
  sql_table_name: `acme-data-prod.curated.fct_orders` ;;
}
```

[Table of Contents](#Looker)

## Can you explain the concept of a LookML model in Looker?

LookML is Looker's modeling language that defines the relationship between data tables and creates reusable dimensions and measures. A LookML model is a collection of files that describe the structure and logic of your data.

A project has `.model.lkml` files (which define explores and the connection), `.view.lkml` files (which define dimensions and measures over one table or derived table), plus manifests, refinements, and data tests.

```text
# model file: acme.model.lkml
connection: "acme_bigquery"

include: "/views/**/*.view.lkml"

explore: orders {
  label: "Orders"
  always_filter: {
    filters: [orders.created_date: "last 90 days"]
  }
  join: customers {
    type: left_outer
    relationship: many_to_one
    sql_on: ${orders.customer_id} = ${customers.customer_id} ;;
  }
}

explore: customers {
  view_label: "Customers"
  fields: [customers.name, customers.segment, orders.total_revenue]
}
```

[Table of Contents](#Looker)

## What is a dimension in Looker?

A dimension in Looker represents a field or attribute in your data. It provides context and adds descriptive information to your analysis.

Dimension types include `string`, `number`, `yesno`, `tier`, `zipcode`, `distance`, and the common `time`. A time dimension is usually declared with `dimension_group` so Looker generates `orders.created_date`, `orders.created_month`, and so on automatically.

```text
dimension: segment {
  type: string
  sql: ${TABLE}.segment ;;
  suggest_explore: customers     # autocomplete values from a small explore
}

dimension: order_size_bucket {
  type: tier
  tiers: [0, 50, 100, 250, 1000]
  sql: ${TABLE}.amount ;;
}
```

[Table of Contents](#Looker)

## How can you create a calculated field in Looker?

In Looker, calculated fields can be created using LookML or Looker's Explore interface. LookML allows for more advanced calculations and reusable logic.

Looker distinguishes three layers of calculation, and interviews probe the difference:

+ LookML measure: runs in the warehouse SQL, reusable everywhere (`type: number`, `sql: ...`).
+ Table calculation: runs in Looker on the result set (percent of total, running total, offset).
+ Custom field in Explore: ad-hoc, user-scoped, not governed.

```text
measure: gross_margin_pct {
  type: number
  value_format_name: percent_2
  sql: (${total_revenue} - ${total_cost}) / NULLIF(${total_revenue}, 0) ;;
}
```

```text
# Table calculation (Looker expression, not SQL): running revenue within the view
running_total(${orders.total_revenue})

# Table calculation: month-over-month change
${orders.total_revenue} - offset(${orders.total_revenue}, -1)
```

Trade-off: a measure is governed and consistent but requires a Git deploy; a table calculation is instant but exists only in that tile and can silently disagree with the governed metric.

[Table of Contents](#Looker)

## What is a Looker Explore?

A Looker Explore is a tool within Looker that allows users to interactively explore and analyze data using a graphical user interface.

An Explore is the query surface: users pick fields from one or more joined views, apply filters, and Looker writes the SQL. What defines a good Explore is not the UI but the model behind it: correct `relationship`, `fields` curation, `always_filter`/`conditionally_filter` for cost control, and `access_filter` or `required_access_grants` for security.

```text
explore: orders {
  always_filter: { filters: [orders.created_date: "last 30 days"] }
  conditionally_filter: {
    filters: [orders.country: "US"]
    unless: [orders.created_date, orders.region]
  }
}
```

[Table of Contents](#Looker)

## What is the purpose of a Looker dashboard?

A Looker dashboard is a customizable collection of visualizations and reports that provide a consolidated view of key metrics and data insights.

Dashboards are layout + tiles + filters; each tile is a stored query. Dashboard-level filters (`listen` blocks) push values into tiles, and `dashboard:element` filters can drive cross-tile behavior.

```text
# Dashboard defined as LookML (dashboards can be code, not just UI artifacts)
- dashboard: revenue_overview
  title: Revenue Overview
  layout: newspaper
  filters:
    - name: date
      title: Date Range
      type: date_filter
      default_value: "90 days"
  elements:
    - name: revenue_by_country
      title: Revenue by Country
      model: acme
      explore: orders
      type: looker_bar
      fields: [orders.country, orders.total_revenue]
      listen: { date: orders.created_date }
```

[Table of Contents](#Looker)

## Can Looker handle real-time data?

Looker primarily works with batch data processing and is not designed for real-time data analysis. However, you can set up scheduled data refreshes to get near real-time insights.

The accurate answer: Looker can query any warehouse table at any freshness, so "real time" depends entirely on the warehouse. What Looker controls is the cache. Turning caching off (`max_cache_age: 0` or a short `datagroup`) gives live results at the cost of warehouse load.

```text
# Per-model cache policy
datagroup: orders_default {
  max_cache_age: "1 hour"
}

datagroup: orders_realtime {
  max_cache_age: "0 seconds"
}

explore: orders_live {
  persist_with: orders_realtime
}
```

Trade-off: disabling cache on a dashboard with 12 tiles and 50 concurrent users multiplies warehouse load 12x per user interaction. The right pattern is a fast-changing narrow explore for operational dashboards and a cached, modeled explore for analysis.

[Table of Contents](#Looker)

## How does Looker handle data security?

Looker offers various security features, such as user access controls, data encryption, and integration with identity providers for authentication and authorization.

Layers of security:

+ Authentication: SAML/OAuth/OIDC/Google SSO, LDAP, or email/password (discouraged).
+ Authorization: roles -> permission sets + model sets; `access_grant` and `required_access_grants` at field level.
+ Row-level security: `access_filter` or user attributes injected into SQL with Liquid.
+ Data: all queries run in the warehouse with the connection's service account; Looker stores no customer data beyond query cache.

```text
# Row-level security via a user attribute: each user sees only their region
explore: orders {
  access_filter: {
    field: orders.region
    user_attribute: region
  }
}

# Field-level: mask a cost field unless the user has the grant
dimension: unit_cost {
  sql: {% if _user_attributes['can_see_cost'] == 'yes' %} ${TABLE}.unit_cost
       {% else %} NULL {% endif %} ;;
  required_access_grants: [see_cost]
}
```

[Table of Contents](#Looker)

## What is the purpose of a Looker filter?

A Looker filter allows users to dynamically limit the data displayed in a report or visualization based on specific criteria.

Filters are translated into SQL `WHERE` clauses (or `HAVING` for measures). Looker adds filter suggestions, `always_filter` defaults, and `conditionally_filter` guards. A subtle point: filtering on a measure uses `HAVING`, which cannot use an index or partition pruning, so prefer dimension filters on partitioned columns.

```sql
-- What a typical Looker query compiles to (BigQuery dialect)
SELECT
  orders.country AS orders_country,
  SUM(orders.amount) AS orders_total_revenue
FROM `acme-data-prod.curated.fct_orders` AS orders
WHERE (orders.created_at >= TIMESTAMP('2026-07-06')
       AND orders.created_at < TIMESTAMP('2026-10-04'))
  AND orders.country IN ('DE', 'FR')
GROUP BY 1
ORDER BY 2 DESC
LIMIT 500;
```

[Table of Contents](#Looker)

## Can you explain the concept of Looker PDTs (Persistent Derived Tables)?

Looker PDTs are precomputed tables created in the database to improve query performance. They are especially useful for complex or resource-intensive calculations.

A PDT is a `derived_table` that Looker materializes with `CREATE TABLE AS SELECT` (or a materialized view), then rebuilds on `persist_for` or `datagroup` triggers. PDTs can be native (in the warehouse's scratch schema) or written to a schema your team owns.

```text
view: customer_lifetime_metrics {
  derived_table: {
    sql:
      SELECT
        o.customer_id,
        MIN(o.created_at) AS first_order_at,
        MAX(o.created_at) AS last_order_at,
        COUNT(DISTINCT o.order_id) AS orders,
        SUM(o.amount) AS lifetime_revenue
      FROM analytics.fct_orders o
      GROUP BY 1 ;;
    persist_for: "24 hours"
    datagroup_trigger: orders_default
    cluster_keys: ["customer_id"]
  }

  dimension: customer_id { primary_key: yes type: string sql: ${TABLE}.customer_id ;; }
  measure: lifetime_revenue { type: sum sql: ${TABLE}.lifetime_revenue ;; }
}
```

Trade-off: a PDT trades warehouse storage and build time for query speed and gives you a governed place for expensive logic, but each PDT is another table to monitor, and a `persist_for` that is too short causes rebuild storms while one that is too long silently serves stale data.

[Table of Contents](#Looker)

## How can you schedule data deliveries in Looker?

Looker provides scheduling options that allow you to automate the delivery of reports and dashboards via email, Slack, or other destinations.

Schedules can be created in the UI or via the API, with formats (PDF, PNG, CSV, XLSX), destinations (email, SFTP, S3/GCS, webhook, Slack), and run-as owner. API-driven schedules are how you keep delivery configuration in version control.

```python
# Create a scheduled plan with the Looker API 4.0
import looker_sdk

sdk = looker_sdk.init40()   # reads LOOKERSDK_* env vars

plan = sdk.create_scheduled_plan(
    body={
        "name": "Weekly revenue CSV to finance",
        "look_id": 1234,
        "crontab": "0 7 * * 1",
        "enabled": True,
        "run_as_recipient": False,
        "scheduled_plan_destination": [{
            "format": "csv",
            "type": "email",
            "address": "finance-ops@acme.com",
            "apply_formatting": False,
        }],
    }
)
print(plan.id)
```

[Table of Contents](#Looker)

## How does Looker handle data caching?

Looker intelligently caches query results to improve performance. The caching strategy can be customized based on the frequency and volatility of the underlying data.

Caching is per-query-result and controlled by `datagroup` policies (preferred), `persist_with`, or per-explore/connection overrides. `datagroup` is preferable because it ties cache invalidation to the warehouse load: when the ETL sets the datagroup's trigger table, Looker invalidates only the affected explores.

```text
# Datagroup whose SQL trigger is the date the ETL updated the table
datagroup: orders_default {
  sql_trigger: SELECT MAX(etl_run_at) FROM analytics.etl_audit WHERE table_name = 'fct_orders' ;;
  max_cache_age: "24 hours"
  description: "Invalidates when the orders load completes"
}
```

Trade-off: long cache reduces warehouse cost and speeds dashboards, but users who need to see a just-loaded row must either use a realtime explore or looker can be told to bypass cache; `cache` is also not shared across users with different row-level-security filters, so warehouse load scales with distinct security contexts.

[Table of Contents](#Looker)

## Can Looker be used for data transformation and ETL processes?

Looker is primarily focused on data visualization and exploration. While it provides some transformation capabilities, it is not a dedicated ETL tool.

Looker's transformation surface is PDTs and SQL Runner, plus Looker's integration with dbt (the recommended place for warehouse transformations). Use dbt/Dataflow/Spark for the heavy pipeline, and Looker for the last-mile aggregation that is too expensive to run per query.

```text
Transform where it belongs
  ingestion + cleaning + conformed models  -> dbt / Spark / Dataflow
  last-mile aggregates and wide tables     -> Looker PDT, materialized view
  ad-hoc exploration                       -> Explore with table calculations
```

[Table of Contents](#Looker)

## How does Looker handle data lineage and documentation?

Looker allows you to document the logic and definitions of your data models using LookML. It also provides options to track data lineage and maintain documentation within the platform.

LookML is self-documenting: `description`, `label`, `group_label`, `hidden`, and `tags` are surfaced in the UI; `/projects` shows LookML dependencies between views and explores; and the Admin panel exposes the SQL of any query. For end-to-end lineage across the warehouse, pair Looker with dbt docs or a catalog (DataHub, OpenMetadata, Dataplex) via the API.

```text
measure: total_revenue {
  label: "Total Revenue (net of returns)"
  description: "Sum of order amounts after refunds. Source: analytics.fct_orders.amount"
  tags: ["finance", "certified"]
  type: sum
  sql: ${TABLE}.amount ;;
}
```

[Table of Contents](#Looker)

## What are some ways to optimize Looker performance?

Performance optimization in Looker can be achieved through techniques such as optimizing SQL queries, utilizing caching, using PDTs strategically, and organizing your LookML models efficiently.

```text
Optimization order (cheapest first)
1. Fix the warehouse: partition/cluster the tables Looker scans, add the right sort keys
2. Reduce bytes: remove unneeded joins, avoid SELECT *, use aggregate awareness
3. Cache: datagroup tied to the ETL, longer max_cache_age for stable explores
4. PDT / materialized view for expensive repeated aggregations
5. Limit result sets: row limits, always_filter on a date partition
6. Only then add warehouse compute
```

```text
# Aggregate awareness: transparently use a pre-aggregated rollup when possible
explore: orders {
  aggregate_table: daily_rollup {
    query: {
      dimensions: [orders.created_date, orders.country]
      measures: [orders.total_revenue, orders.order_count]
    }
    materialization: {
      sql_trigger_value: SELECT MAX(etl_run_at) FROM analytics.etl_audit WHERE table_name='fct_orders' ;;
    }
  }
}
```

[Table of Contents](#Looker)

## Can Looker connect to non-SQL data sources?

Looker can connect to non-SQL data sources through the use of database dialects, APIs, and custom data connectors.

Looker requires a SQL-capable endpoint. Non-SQL sources such as MongoDB, Cassandra, or object storage are accessed through a query engine that speaks SQL (BigQuery external/BigLake tables, Athena/Trino, Databricks SQL, MongoDB Atlas SQL), or through an API connector modeled in LookML as a one-row derived table. There is no native "connect to an API and browse it" mode.

[Table of Contents](#Looker)

## What is the purpose of Looker's Data Actions?

Looker's Data Actions enable users to take actions directly from their data, such as updating records, creating tasks, or triggering external processes.

Actions are configured in the Action Hub (Slack, email, Google Sheets, Segment, Zapier, custom webhooks) and can be invoked from a dashboard tile or a data table row. They are a write path from the semantic layer, so treat them as production integrations: authenticate, validate, and audit.

```text
# Invoke a custom webhook action from a LookML-tagged dashboard tile
action: {
  name: "create_jira_ticket"
  label: "Escalate to Jira"
  url: "https://hooks.acme.internal/looker/jira"
  form: {
    ticket_title: { label: "Title" }
    priority: { label: "Priority", type: "select", options: ["P1", "P2", "P3"] }
  }
}
```

[Table of Contents](#Looker)

## Can Looker handle large-scale data processing?

Looker is designed to handle large-scale data processing by leveraging the computing power and scalability of modern data warehouses or databases.

Looker itself scales horizontally for the app tier, and query scale is the warehouse's problem. The practical limits are: result-set size delivered to the browser (row limits and pivot cell limits), query concurrency against the warehouse, and the cost of unpruned scans. Looker is not doing the heavy lifting; it must generate SQL that the warehouse can execute economically.

```sql
-- The shape Looker should generate for a large aggregate: partition-pruned and clustered
SELECT DATE(created_at) AS created_date, country, SUM(amount) AS total_revenue
FROM `acme-data-prod.curated.fct_orders`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY 1, 2;
```

[Table of Contents](#Looker)

## How does Looker support collaboration among team members?

Looker provides features for sharing, commenting, and collaborating on reports, dashboards, and data models. It also integrates with communication tools like Slack and email.

Collaboration features: boards (curated collections), favorites, dashboard comments and mentions, Slack/Teams delivery, and shared folders with role-based access. On the modeling side, Git branching + Development Mode is the real collaboration mechanism: every LookML change is a pull request with review.

[Table of Contents](#Looker)

## What are some limitations of Looker?

Some limitations of Looker include its focus on batch processing, limited real-time capabilities, and the need for underlying data infrastructure such as data warehouses.

The honest list: (1) it is expensive per user and pricing is negotiated, not list; (2) it requires a performant SQL warehouse, so cost is Looker + warehouse; (3) no native streaming/real-time push (it polls the warehouse); (4) LookML has a learning curve and the developer workflow (IDE, Git, deploy) is not beginner-friendly; (5) visual customization is weaker than Tableau/Power BI for pixel-perfect layouts; (6) row-level security adds warehouse load because cache is per security context. When NOT to use it: a single-team ad-hoc analysis shop with no warehouse, or a scenario needing sub-second push updates.

[Table of Contents](#Looker)

## Can Looker handle unstructured or semi-structured data?

Looker is primarily designed for structured data analysis. However, with appropriate data modeling and transformations, it can also handle certain types of unstructured or semi-structured data.

Semi-structured data (JSON, arrays, maps) is flattened or extracted in the warehouse, then modeled in LookML. BigQuery `JSON_VALUE`, Snowflake `LATERAL FLATTEN`, and Spark `explode` are the usual tools. Looker can also query a JSON column and extract with SQL, but doing so per query is expensive and hard to govern.

```sql
-- Flatten event properties before Looker sees them
SELECT
  event_id,
  event_name,
  JSON_VALUE(properties, '$.utm_source') AS utm_source,
  JSON_VALUE(properties, '$.plan')       AS plan,
  event_ts
FROM `acme-data-prod.raw.events`
WHERE DATE(event_ts) = DATE '2026-10-04';
```

[Table of Contents](#Looker)

## How does Looker handle data versioning and change management?

Looker allows you to version control your LookML models and manage changes using Git or other version control systems.

Each project is a Git repository; Development Mode creates a branch, the IDE validates and diffs changes, and deploying to Production is a commit/merge. Content (dashboards, Looks, schedules) is *not* in Git by default — export it with the API or use Looker's content validation and the `/content` endpoints if you need content-as-code.

```bash
# List projects and their Git state with the API
curl -s -H "Authorization: token $LOOKER_TOKEN" \
  "https://acme.looker.com/api/4.0/projects" \
  | python -c "import sys,json; [print(p['id'], p['git_remote_url'], p.get('uses_git')) for p in json.load(sys.stdin)]"
```

[Table of Contents](#Looker)

## What is Looker's scheduling and alerting capability?

Looker's scheduling and alerting feature allows you to schedule reports, dashboards, and data deliveries at specific intervals. You can also set up alerts based on predefined thresholds or conditions.

Looker alerts run a saved query on a schedule and notify when a condition holds (for example, `revenue < threshold`), sending to email or a webhook. Alerts are per-user in the UI (and API-manageable), and a common trap is alert fatigue: alert on the metric a human can act on, with a link to the dashboard and a runbook.

```text
# Alert condition example: page when daily revenue drops below the floor
# condition: orders.total_revenue < 250000
# comparison: less than
# schedule: every 6 hours during business hours
# destination: webhook -> PagerDuty
```

[Table of Contents](#Looker)

## Can Looker be integrated with other BI tools or data visualization platforms?

Looker provides APIs and integrations that allow it to be connected with other BI tools, data visualization platforms, or custom applications.

Looker's APIs (Looker API 4.0, Embed SDK, Explore API, Action API, and a JDBC driver) let other tools consume governed queries. The most common pattern is embedding into a product; the second is fetching data into another visualization tool via the API rather than duplicating the semantic layer.

```python
# Run an inline query through the Looker API and reuse governed metrics elsewhere
import looker_sdk

sdk = looker_sdk.init40()
result = sdk.run_inline_query(
    result_format="json",
    body={
        "model": "acme",
        "view": "orders",
        "fields": ["orders.country", "orders.total_revenue"],
        "filters": {"orders.created_date": "90 days"},
        "sorts": ["orders.total_revenue desc"],
        "limit": "100",
    },
)
print(result[:200])
```

[Table of Contents](#Looker)

## What are some advantages of using Looker compared to traditional BI tools?

Looker offers a more agile and self-service approach to data analysis, allowing users to explore data and create reports without heavy reliance on IT teams. It also provides powerful modeling capabilities with LookML.

```text
Advantages of a code-defined semantic layer
  one metric definition, reused across all dashboards
  Git review and CI for model changes
  row-level security and access grants expressed in code
  embedded analytics with per-customer theming and SSO
  the warehouse does the compute, so scale follows the warehouse
```

The trade-off against Tableau/Power BI is upfront modeling effort and less layout freedom; the payoff is consistency and embeddability, which is why product-embedded analytics is Looker's strongest use case.

[Table of Contents](#Looker)

## How can you create a custom visualization in Looker?

Looker supports custom visualizations through custom JavaScript or HTML. You can create custom visualizations using third-party libraries or build your own.

Looker custom visualizations are JavaScript files implementing a small lifecycle (`create`, `updateAsync`, `destroy`), loaded from the project or a marketplace, and referenced from a LookML `visualization` block or the UI.

```text
// custom_viz.js (abridged): a minimal Looker custom visualization contract
const vis = {
  create: function (element, config) {
    this.element = element;
  },
  updateAsync: function (data, element, config, queryResponse, details, done) {
    element.innerHTML = data.map((row) => row[0].value).join(", ");
    done();
  },
};
looker.plugins.visualizations.add(vis);
```

```text
visualization: {
  id: "acme_donut"
  label: "Acme Donut"
  file: "custom_viz.js"
  sri_hash: "sha256-..."
}
```

[Table of Contents](#Looker)

## What is Looker's Explore API used for?

Looker's Explore API allows developers to programmatically query and retrieve data from Looker Explore instances, enabling integration with external applications.

The Explore API (`run_inline_query`) returns governed query results as JSON/CSV/HTML and is used to power embedded analytics, reverse ETL, and data-app backends. It is preferable to querying the warehouse directly because filters, joins, and row-level security are applied by the model.

```bash
# Inline query via REST: same semantics as the Explore UI, no SQL duplication
curl -s -X POST -H "Authorization: token $LOOKER_TOKEN" -H "Content-Type: application/json" \
  -d '{"model":"acme","view":"orders","fields":["orders.country","orders.total_revenue"],
       "filters":{"orders.created_date":"30 days"},"limit":"50"}' \
  "https://acme.looker.com/api/4.0/queries/run/json" | head -c 300
```

[Table of Contents](#Looker)

## How does Looker handle data governance and compliance?

Looker offers features for data access controls, auditing, and compliance with regulations like GDPR and HIPAA. It allows administrators to manage user permissions and track data usage.

Governance controls: roles/permission sets, model sets, field-level access grants, user attributes for row-level security, content validation for broken/errored content, system activity explores and audit logs (`System Activity` model), and data retention controls for query cache and history. Compliance certifications come from the platform (SOC 2, ISO 27001, HIPAA-eligible under a BAA) and from the warehouse, so the data residency story is the warehouse's.

```text
access_grant: see_pii {
  user_attribute: pii_access
  allowed_values: ["yes"]
}

dimension: email {
  sql: ${TABLE}.email ;;
  required_access_grants: [see_pii]
}
```

[Table of Contents](#Looker)

## Can Looker handle geospatial data analysis?

Looker provides support for geospatial data analysis through various visualization options, including maps and geographic charts.

Looker has built-in map visualizations (points, heatmaps, regions) and supports geographic dimensions via `type: location` or lat/long fields. For rich geospatial work, model a GeoJSON/region join table in the warehouse and use an `area` map layer.

```text
dimension: location {
  type: location
  sql: ${TABLE}.city_name ;;
}

dimension: latitude { type: number sql: ${TABLE}.lat ;; }
dimension: longitude { type: number sql: ${TABLE}.lon ;; }
```

[Table of Contents](#Looker)

## What is Looker's Explore Permissions feature?

Looker's Explore Permissions feature allows administrators to control which users or groups can access specific data sources, tables, or fields within Looker.

Permissions work through model sets (which projects/models a role can see) and field-level `required_access_grants`. There is also `explore`-level control via `required_access_grants` on the explore itself, and `fields`/`hidden` to curate what appears in the UI.

```text
explore: orders {
  required_access_grants: [orders_access]
  fields: [orders.order_id, orders.created_date, orders.country, orders.total_revenue]
}
```

[Table of Contents](#Looker)

## Can Looker handle streaming data sources?

Looker is primarily designed for batch data processing, but it can leverage streaming data sources through appropriate integrations and data modeling techniques.

Looker never consumes a stream directly: the streaming layer writes into the warehouse (BigQuery, Snowflake, ClickHouse), and Looker queries the resulting table. Near-real-time therefore means short cache age plus a warehouse that accepts frequent small appends — which is usually expensive and rarely justified for BI.

[Table of Contents](#Looker)

## What are some best practices for optimizing Looker performance?

Best practices for optimizing Looker performance include reducing the number of queries, utilizing caching effectively, using PDTs strategically, and optimizing database performance.

```text
LookML hygiene that shows up as performance
  - one explore per grain; do not force users to filter out fanout themselves
  - always_filter a date partition on high-volume explores
  - use type: sum with sql_distinct_key or symmetric aggregates, not COUNT of joins
  - hide unused fields (hidden: yes) so users cannot build 40-join queries
  - aggregate_table for the three dashboards everyone runs every morning
  - datagroup rather than persist_for where the ETL can signal completion
```

[Table of Contents](#Looker)

## How does Looker handle data lineage and impact analysis?

Looker provides features for tracking data lineage and performing impact analysis by examining the relationships between different data models, tables, and fields.

Within Looker, the Content Validator checks every saved Look and dashboard for errors, and the "Used by" / dependency views plus the `/projects` endpoint show which explores and fields depend on a view. For impact analysis of a warehouse change, combine that with the warehouse catalog or dbt lineage; Looker cannot see upstream ETL lineage by itself.

```bash
# Find content broken by a field change before deploying it
curl -s -X POST -H "Authorization: token $LOOKER_TOKEN" \
  "https://acme.looker.com/api/4.0/content_validation" \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('total'), 'content items checked')"
```

[Table of Contents](#Looker)

## Can you explain Looker's dynamic time frame filters?

Looker's dynamic time frame filters allow users to select time-based periods, such as last month or last year, dynamically based on the current date.

Time frame filters use relative expressions (`7 days`, `last month`, `last 3 months`, `this year`) and are translated into warehouse `WHERE` clauses at query time. `dimension_group` defines which time frames exist, so a view that only declares `date` cannot filter by `month` without a model change.

```text
dimension_group: created {
  type: time
  timeframes: [raw, time, date, week, month, quarter, year]
  datatype: timestamp
  sql: ${TABLE}.created_at ;;
  convert_tz: no   # warehouse already stores UTC; avoid double conversion
}
```

[Table of Contents](#Looker)

## How does Looker handle data security in a cloud-based environment?

Looker implements various security measures in a cloud-based environment, including encryption of data in transit and at rest, compliance with industry standards, and access controls.

Looker Cloud encrypts traffic (TLS) and its metadata at rest, but the actual analytical data never lands in Looker — it stays in the warehouse. So the cloud security model is: SSO with your IdP, IP allowlisting, private connectivity (Private Service Connect / VPC SC) to the warehouse, customer-managed encryption at the warehouse, and row-level security in LookML. Looker itself holds query results in cache, which is an important caveat for very sensitive data.

[Table of Contents](#Looker)

## What are the advantages of using Looker's embedded analytics feature?

Looker's embedded analytics feature allows you to embed Looker dashboards and reports directly into external applications, providing seamless access to data insights within your own product or platform.

Embedding options: private embed (iframe with Looker login), SSO embed (signed URL, per-user identity), and the Embed SDK for full control. SSO embed is what makes per-tenant row-level security work, because the signed URL carries user attributes.

```python
# Generate an SSO embed URL signed with the embed secret
import base64
import hashlib
import hmac
import time
from urllib.parse import urlencode

def embed_url(secret: str, host: str, path: str, params: dict) -> str:
    nonce = base64.b64encode(f"{time.time()}:{path}".encode()).decode().rstrip("=")
    url = f"{host}{path}?{urlencode(params)}&nonce={nonce}"
    signature = base64.b64encode(
        hmac.new(secret.encode(), url.encode(), hashlib.sha1).digest()
    ).decode()
    return f"{url}&signature={signature}"

print(embed_url("s3cr3t", "https://acme.looker.com",
                "/embed/dashboards/42",
                {"tenant_id": "acme-retail", "embed_domain": "https://app.acme.com"}))
```

[Table of Contents](#Looker)

## Can Looker handle multi-tenant data environments?

Looker supports multi-tenant data environments, allowing different users or groups to access and analyze their specific datasets securely within the same instance.

Multi-tenancy is done with user attributes + `access_filter` (or hybrid: a separate warehouse per large tenant and a shared one for the long tail). The key design question is cache efficiency: because filters differ per tenant, cached results are per security context, so 500 tenants means 500 cache entries for the same dashboard unless you share a tenant-agnostic rollup.

```text
explore: usage {
  access_filter: {
    field: usage.tenant_id
    user_attribute: tenant_id
  }
}
```

[Table of Contents](#Looker)

## How does Looker handle data modeling for complex data structures?

Looker's LookML modeling language provides flexibility to handle complex data structures by defining relationships, joins, and transformations using LookML files.

Complex structures are handled by flattening in the warehouse (arrays, JSON), then modeling with `derived_table`, `extends`, and `refinements`. `extends` lets you build a base view (all dimensions) and specialized child views (e.g., a `orders_secure` view that hides PII), while `refinement` lets a downstream project add access grants without forking the base project.

```text
view: orders_base {
  dimension: order_id { primary_key: yes type: string sql: ${TABLE}.order_id ;; }
  measure: total_revenue { type: sum sql: ${TABLE}.amount ;; }
}

view: orders_secure {
  extends: [orders_base]
  dimension: email {
    sql: ${TABLE}.email ;;
    required_access_grants: [see_pii]
  }
}

view: orders_base {
  refinement: yes
  measure: total_revenue { required_access_grants: [finance] }
}
```

[Table of Contents](#Looker)

## Can Looker connect to cloud-based data warehouses like Amazon Redshift or Google BigQuery?

Yes, Looker can connect to cloud-based data warehouses like Amazon Redshift, Google BigQuery, and other popular cloud platforms.

```text
Supported dialects include BigQuery, Snowflake, Redshift, Synapse, Databricks,
Postgres, MySQL, Trino/Presto, Athena, ClickHouse, and more.
```

```text
connection: "acme_bigquery"
# BigQuery-specific: use qualification and let Looker use the project/dataset
# acme_bigquery is a connection created in Admin -> Connections with:
#   Project, Dataset, Service Account JSON / OAuth, PDT dataset, temp dataset
```

[Table of Contents](#Looker)

## How does Looker handle data governance in a self-service environment?

Looker allows administrators to implement data governance policies by managing user access controls, setting data permissions, and monitoring data usage through audit logs.

Self-service governance = guardrails in the model, not gates in front of users: a curated set of explores, hidden raw fields, `always_filter` on partitions to prevent full scans, certified content labels, and usage analytics from the System Activity model to see which fields are actually used (and which to deprecate).

[Table of Contents](#Looker)

## What are some advanced analytical capabilities offered by Looker?

Looker offers advanced analytical capabilities such as advanced calculations, data modeling, advanced filtering, derived tables, and custom visualizations.

```text
Advanced capabilities
  table calculations: running_total, offset, percent_of_total, rank, pivot_index
  derived tables and PDTs, including incremental PDTs
  parameters for user-driven dimensions and filters
  analytical blocks (cohorts, retention, funnels) built on LookML patterns
  custom visualizations and custom actions
  aggregate awareness and symmetric aggregates
```

[Table of Contents](#Looker)

## Can you explain Looker's data modeling best practices?

Looker's data modeling best practices include using views and explores effectively, creating reusable dimensions and measures, organizing files and folders in LookML, and implementing proper naming conventions.

```text
Best practices
  one view per table or derived table; one explore per business question/grain
  primary_key on every view; declare relationship on every join
  model the warehouse star schema, do not hide it behind 10 joins
  name measures for the business, not the column (total_revenue, not sum_amount)
  use dimension_group for time; use value_format_name for consistent formatting
  keep PII out of shared views; use access grants
  put descriptions on every exposed field; tag certified metrics
  test with data tests and content validation before deploy
```

[Table of Contents](#Looker)

## How can Looker integrate with data orchestration tools like Apache Airflow?

Looker can be integrated with data orchestration tools like Apache Airflow through custom scripts or using Looker's API to trigger data processes or update Looker models.

The usual integration points: Airflow triggers a PDT rebuild by hitting the Looker API (`start_pdt_build`/`check_pdt_build`), or the ETL writes a datagroup trigger table that invalidates Looker cache, or Airflow runs `looker-cli`/`gcloud` to deploy LookML after a dbt run.

```python
# Airflow task: rebuild a PDT after the warehouse load, then fail the DAG if it errors
import looker_sdk
import time

def rebuild_pdt(model: str, view: str) -> None:
    sdk = looker_sdk.init40()
    materialization = sdk.start_pdt_build(model_name=model, view_name=view)
    while True:
        state = sdk.check_pdt_build(materialization.materialization_id)
        if state.status in {"complete", "error", "killed"}:
            break
        time.sleep(10)
    if state.status != "complete":
        raise RuntimeError(f"PDT {view} build {state.status}: {state.message}")
```

[Table of Contents](#Looker)

## Can Looker handle multi-language support for international users?

Looker supports multi-language translations, allowing users to view the interface and content in their preferred language.

Looker localizes its UI (locale files) and supports localized labels/descriptions in LookML with `label` locale overrides via `localization` files. Data values (country names, product names) are not translated by Looker — that mapping belongs in a warehouse dimension.

```text
# strings file: en.strings.json / de.strings.json
# { "orders.total_revenue": { "label": "Umsatz gesamt" } }
```

[Table of Contents](#Looker)

## What is the purpose of Looker's SQL Runner?

Looker's SQL Runner provides a SQL interface within Looker for users to write and execute custom SQL queries against the connected data sources.

SQL Runner is an admin/developer tool: run SQL against any connection, inspect schemas, create and drop tables, and run Explain. It is powerful and dangerous — a developer with SQL Runner can write to the warehouse — so restrict the `sql_runner` permission to a small group and prefer LookML for anything reusable.

```sql
-- SQL Runner is useful to validate a derivation before modeling it
SELECT country, COUNT(*) AS orders, ROUND(AVG(amount), 2) AS aov
FROM analytics.fct_orders
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY country
ORDER BY orders DESC;
```

[Table of Contents](#Looker)

## How does Looker handle data replication and synchronization?

Looker does not handle data replication or synchronization directly. It relies on the underlying data infrastructure, such as data warehouses or databases, to manage replication and synchronization processes.

This is correct and worth expanding: the warehouse replica's lag becomes Looker's data freshness, and a read replica that lags behind the ETL watermark can make a dashboard appear stale even though Looker refreshed. Monitor replication lag as part of the BI SLA.

[Table of Contents](#Looker)

## Can Looker generate alerts or notifications based on predefined conditions?

Yes, Looker can generate alerts or notifications based on predefined conditions through Looker's scheduling and alerting features.

Alerts are available on Looks and dashboard tiles, with a condition (greater/less than, equal, changes by) evaluated on a schedule. They are best for threshold breaches tied to an owner; for anomaly detection use a warehouse model (z-score/IQR) and alert on the model's output rather than on raw values.

```sql
-- Warehouse-side anomaly flag that an alert can watch
WITH daily AS (
  SELECT DATE(created_at) AS ds, SUM(amount) AS revenue
  FROM analytics.fct_orders GROUP BY 1
), stats AS (
  SELECT ds, revenue,
         AVG(revenue) OVER (ORDER BY ds ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING) AS avg_28d,
         STDDEV(revenue) OVER (ORDER BY ds ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING) AS sd_28d
  FROM daily
)
SELECT ds, revenue, avg_28d, sd_28d,
       (revenue - avg_28d) / NULLIF(sd_28d, 0) AS z_score
FROM stats
WHERE ABS((revenue - avg_28d) / NULLIF(sd_28d, 0)) > 3;
```

[Table of Contents](#Looker)

## What is the difference between Looker's explore and join types?

Looker's explore defines a specific view of data, while join types determine how multiple tables are joined together to create a consolidated view of the data.

Join `type` (`left_outer`, `inner`, `full_outer`, `cross`) and `relationship` (`one_to_one`, `many_to_one`, `one_to_many`, `many_to_many`) are separate declarations in LookML; `relationship` is what lets Looker apply symmetric aggregates and choose the correct join direction, while `type` is the SQL join. Joining a `one_to_many` fanout into a measure-bearing explore without symmetric aggregates inflates every `type: sum`.

```text
join: order_items {
  type: left_outer
  relationship: one_to_many      # fanout! metrics on orders must be fanout-safe
  sql_on: ${orders.order_id} = ${order_items.order_id} ;;
}
```

[Table of Contents](#Looker)

## How does Looker handle data partitioning and sharding?

Looker relies on the data warehouse or database's partitioning and sharding capabilities. Looker models can leverage the partitioning and sharding configurations implemented at the database level.

Looker's job is to generate partition-prunable SQL, which means filtering on the partition column without wrapping it in a function. `always_filter` on the partition column and `conditionally_filter` are the LookML levers; `cluster_keys` on PDTs is the materialization lever.

```text
explore: events {
  always_filter: {
    filters: [events.event_date: "last 7 days"]
  }
}

view: events {
  dimension_group: event {
    type: time
    timeframes: [date, week, month]
    datatype: timestamp
    sql: ${TABLE}.event_ts ;;
  }
}
```

[Table of Contents](#Looker)

## Can you explain Looker's data permissions and access controls?

Looker's data permissions and access controls allow administrators to control which users or groups can access specific data sources, tables, or fields within Looker.

The object model: permission sets (what actions) + model sets (which models/explores) -> roles -> groups -> users (from SSO). Row-level access is `access_filter`/user attributes, column-level is `required_access_grants`, and content-level is folder permissions and board curation.

```text
role: analyst {
  permission_set: { name: "Analyst" }
  model_set: { name: "acme_finance" }
}

user_attribute: region {
  data_type: string
  user_access: [viewer]
  default_value: "US"
}
```

[Table of Contents](#Looker)

## How can Looker handle data lineage in a complex data ecosystem?

Looker tracks data lineage by mapping relationships between LookML models, explores, views, and the underlying data tables. This allows users to understand the flow of data and the transformations applied.

```text
End-to-end lineage needs three tools stitched together
  warehouse tables  -> catalog/dbt lineage (source of truth for ETL)
  LookML views      -> Looker /projects dependency graph + Git history
  explores/marts    -> Looker "Used by" + content validator
  BI artifacts      -> System Activity explores (who runs what)
```

[Table of Contents](#Looker)

## Can Looker handle near real-time data analysis?

Looker can provide near real-time data analysis by setting up frequent data refresh schedules or utilizing streaming data sources in combination with appropriate data modeling techniques.

```text
# Near-real-time = short cache + a fast-changing narrow explore
datagroup: ops_realtime {
  max_cache_age: "30 seconds"
}

explore: live_shipments {
  persist_with: ops_realtime
  always_filter: { filters: [live_shipments.updated_date: "today"] }
}
```

Trade-off: a 30-second cache on a dashboard with ten users and eight tiles is up to 160 warehouse queries a minute; size the warehouse for it or reduce the tile count.

[Table of Contents](#Looker)

## How does Looker handle data quality and cleansing?

Looker primarily focuses on data analysis and visualization rather than data quality and cleansing. However, data cleansing can be performed through SQL transformations or data preparation processes before connecting to Looker.

Looker can surface quality with data tests and a "data quality" explore (null rates, duplicate keys, freshness), but the fix belongs upstream in dbt/Dataflow. A useful pattern is a LookML data test that fails the model validation when a key constraint breaks.

```text
test: orders_unique_order_id {
  explore_source: orders {
    column: order_id {}
  }
  assert: {
    expression: "COUNT(${orders.order_id}) = COUNT(DISTINCT ${orders.order_id})"
  }
}
```

[Table of Contents](#Looker)

## What is the purpose of Looker's content validation feature?

Looker's content validation feature allows users to validate and ensure the accuracy of data displayed in dashboards, reports, and visualizations.

Content Validator runs every saved Look and dashboard against the current model and reports broken fields, removed dimensions/measures, and errored queries — the go-to tool before deploying a LookML change or migrating a database. It does not validate the numbers are *correct*, only that the queries still run.

```bash
# Content validation via the API is the CI gate before a LookML deploy
curl -s -X POST -H "Authorization: token $LOOKER_TOKEN" \
  "https://acme.looker.com/api/4.0/content_validation" \
  | python -c "import sys,json; d=json.load(sys.stdin); print('errors:', len(d.get('errors',[])), 'checked:', d.get('total'))"
```

[Table of Contents](#Looker)

## Can Looker integrate with external authentication providers?

Yes, Looker can integrate with external authentication providers such as LDAP, SAML, or OAuth to enable single sign-on (SSO) and centralized user management.

```text
Auth options
  Google OAuth / OIDC  simplest for Google Workspace + Cloud Identity shops
  SAML 2.0             Okta, Azure AD, Ping; passes user attributes and groups
  LDAP                 legacy directory; still supported
  Embed SSO            signed URL for embedded users (no Looker account UI)
```

Group membership from the IdP should map to Looker groups so role assignment is managed centrally, not per user in Looker.

[Table of Contents](#Looker)

## How does Looker handle data privacy and compliance requirements?

Looker provides features for data encryption, access controls, and compliance with regulations like GDPR and HIPAA, ensuring data privacy and meeting industry-specific compliance requirements.

Practical controls for GDPR/HIPAA/PCI in Looker: SSO + MFA, least-privilege roles, field-level access grants for PII, user attributes for regional row filtering, audit logs of every query, IP allowlisting, and a documented retention policy for query history and cache. The data itself must be governed in the warehouse (masking, residency, deletion workflows); Looker is the access layer.

[Table of Contents](#Looker)

## Can Looker perform predictive analytics or machine learning?

Looker itself does not provide built-in capabilities for predictive analytics or machine learning. However, it can integrate with external tools or platforms that offer these functionalities.

The pattern is "predict in the warehouse or Vertex AI, visualize in Looker": write model scores to a table, expose them as dimensions/measures, and monitor drift with a Looker dashboard. Looker also has BQML integration patterns where the model lives in BigQuery and Looker just queries `ML.PREDICT`.

```sql
-- BigQuery ML prediction surfaced through LookML
SELECT
  customer_id,
  predicted_churn,
  predicted_churn_probs[OFFSET(0)].prob AS churn_probability
FROM ML.PREDICT(
  MODEL `acme-data-prod.ml.churn_model`,
  (SELECT * FROM `acme-data-prod.ml.churn_features`)
);
```

[Table of Contents](#Looker)

## What is the purpose of Looker's PDT (Persistent Derived Tables) Events?

Looker's PDT Events feature allows you to schedule PDT builds at specific intervals or trigger them based on specific events or data changes.

PDT triggers are `persist_for` (time-based), `datagroup_trigger`/`sql_trigger` (data-based), and the API force-rebuild. "Events" in current Looker are the datagroup triggers; a build can also be kicked off by the ETL through the API. Watch for rebuild storms: if a datagroup's SQL trigger changes on every micro-batch, every dependent PDT rebuilds constantly.

[Table of Contents](#Looker)

## How does Looker handle data virtualization?

Looker does not provide native data virtualization capabilities. However, it can connect to virtualized data sources through appropriate connectors or APIs.

Looker connects to Trino/Deno/Presto, Starburst, Databricks, and BigQuery external/BigLake tables, which are common virtualization layers over S3/GCS/HDFS. So the virtualization is in the connection, and the LookML is written against the federated catalog; the trade-off is that federated queries are slower and less predictable than a materialized copy.

[Table of Contents](#Looker)

## Can you explain Looker's dynamic data masking feature?

Looker does not provide native dynamic data masking capabilities. Data masking should be implemented at the database or data source level before connecting to Looker.

Looker can approximate masking with Liquid + user attributes, but it is model-level obfuscation, not a database security control, and the raw value still appears in SQL Runner or a downloaded CSV for anyone with access. Real masking belongs in the warehouse (policy tags, Snowflake masking policies) or in an access-granted secured view.

```text
dimension: email_masked {
  sql: CASE
         WHEN '{{ _user_attributes["pii_access"] }}' = 'yes' THEN ${TABLE}.email
         ELSE CONCAT(LEFT(${TABLE}.email, 2), '***@***')
       END ;;
  required_access_grants: [view_pii_masked]
}
```

[Table of Contents](#Looker)

## How can Looker integrate with data governance tools?

Looker can integrate with data governance tools through custom scripts, APIs, or data connectors to enforce data governance policies and ensure compliance.

```text
Integration patterns
  Looker API -> catalog ingestion (DataHub/OpenMetadata/Atlas) for BI lineage
  dbt exposures -> Looker dashboards documented upstream
  System Activity model -> usage-based deprecation and cost attribution
  policy tags / masking policies -> enforced in the warehouse, referenced by Looker
```

[Table of Contents](#Looker)

## What is Looker's Explore Embed feature used for?

Looker's Explore Embed feature allows developers to embed Looker's Explore functionality directly into external applications, providing a seamless data exploration experience within the application.

Explore Embed gives end users of your product a full Explore (field picker, filters, viz) inside your app, with the model constrained by the embed user's permissions. It is the most capable embed mode and the one with the largest surface area to secure: enable only the explores that make sense for each tenant and restrict custom fields and SQL.

[Table of Contents](#Looker)

## How does Looker handle data lineage for derived or calculated fields?

Looker tracks data lineage for derived or calculated fields by tracing back to the underlying data tables and the transformations applied in LookML.

For a measure like `gross_margin_pct`, Looker can show the SQL it generates under the cover, which references `${total_revenue}` and `${total_cost}`, and each of those resolves to a `sql:` expression on a base table — that chain is the lineage. Table calculations, by contrast, run in the browser and have no warehouse lineage.

[Table of Contents](#Looker)

## Can Looker handle data visualization in real-time dashboards?

Looker is primarily designed for batch data processing and may not be suitable for real-time dashboards. However, with appropriate data modeling and frequent data refreshes, it can provide near real-time insights.

```text
Real-time dashboard checklist
  warehouse table refreshed by streaming with < 30s latency
  narrow explore with max_cache_age: "30 seconds"
  always_filter today's partition so each query scans little
  fewer, larger tiles (each tile is a query)
  warehouse sized for the concurrency, or accept queuing
```

[Table of Contents](#Looker)

## What is the purpose of Looker's Action Hub?

Looker's Action Hub provides a centralized platform for configuring and managing data actions, allowing users to take specific actions directly from their data.

Action Hub is a directory of integrations (Slack, email, Google Sheets, Zapier, Segment, custom webhook) that admins enable once; modelers then attach actions to dashboard tiles or data tables. Because actions write to external systems, they need the same scrutiny as any API integration: scoped credentials, idempotency, and audit logging.

[Table of Contents](#Looker)

## Can Looker handle data anomaly detection?

Looker is not specifically built for data anomaly detection. However, it can integrate with external tools or platforms that specialize in anomaly detection for analyzing data.

Looker has no built-in anomaly detection, but you can surface it: compute z-scores or use BigQuery ML `ML.DETECT_ANOMALIES` in the warehouse, expose the flag as a dimension/measure, and color the tile or alert on it.

```sql
-- BigQuery ML anomaly detection, consumed by Looker as a normal table
SELECT
  ds,
  revenue,
  is_anomaly,
  lower_bound,
  upper_bound
FROM ML.DETECT_ANOMALIES(
  MODEL `acme-data-prod.ml.revenue_anomaly_model`,
  STRUCT(0.95 AS anomaly_prob_threshold),
  (SELECT ds, revenue FROM `acme-data-prod.marts.revenue_daily`)
);
```

[Table of Contents](#Looker)

## How does Looker handle data lineage for transformations applied outside of Looker?

Looker can track data lineage for transformations applied outside of Looker by integrating with the appropriate tools or databases that capture and document the transformation steps.

Looker sees the warehouse table as a black box, so the link is documentation, not detection: dbt `exposures` referenced to Looker dashboards, table/field descriptions in the warehouse catalog, and `sql_table_name` pointing at a documented mart. A common interview answer is "Looker's lineage stops at the table; use dbt + a catalog for the upstream half."

[Table of Contents](#Looker)

## What is the purpose of Looker's PDT (Persistent Derived Tables) Performance Optimization?

Looker's PDT Performance Optimization feature allows users to optimize the performance of PDTs by managing their builds and refreshing schedules more efficiently.

Techniques: build PDTs incrementally (`incremental: yes` with `{% incrementcondition %}`), choose `datagroup` over a short `persist_for`, add `cluster_keys`/`sort` for the columns Looker filters on, separate `persist_for` per PDT to avoid a rebuild stampede, and use a designer/reader schema so a rebuild never breaks readers.

```text
view: events_daily_incremental {
  derived_table: {
    sql:
      SELECT event_date, event_name, COUNT(*) AS events
      FROM analytics.events
      {% incrementcondition %} WHERE event_date > (SELECT MAX(event_date) FROM analytics.events_daily) {% endincrementcondition %}
      GROUP BY 1, 2 ;;
    incremental: yes
    datagroup_trigger: events_default
    cluster_keys: ["event_date"]
  }
}
```

[Table of Contents](#Looker)

## Can Looker handle incremental data loads?

Looker relies on the underlying data infrastructure, such as data warehouses or databases, to handle incremental data loads. Proper configuration and modeling techniques are required to support incremental updates.

Two levels: the ETL does incremental loads into warehouse tables (dbt incremental models, MERGE), and Looker PDTs can be incremental. Looker's query cache is separate — it caches results, not data — so "incremental load" in a Looker conversation usually means either the dbt model or the PDT.

[Table of Contents](#Looker)

## How does Looker handle data versioning and change tracking in LookML models?

Looker provides version control capabilities, allowing users to track changes, compare versions, and revert to previous versions of LookML models using Git or other version control systems.

```text
LookML change flow
  dev branch -> IDE edit -> validate (LookML linter + data tests)
  -> content validation against the branch -> pull request review
  -> merge to main -> Deploy to Production -> datagroups invalidate cache
```

```bash
# Optional CI: validate LookML with lookmlint / looker-cli before merge
looker-cli project validate --project acme --branch feature/revenue-fix
```

[Table of Contents](#Looker)

## Can Looker be deployed on-premises or is it only available as a cloud-based solution?

Looker can be deployed both on-premises and as a cloud-based solution, providing flexibility based on the organization's infrastructure and requirements.

Current state: Looker is sold as a Google Cloud service (Looker, formerly Looker-hosted/GCP-managed). A self-hosted/on-prem deployment existed historically but is no longer the recommended or generally available path; most "on-prem" requirements are met with private networking from Looker Cloud to a private warehouse. Be careful in an interview: the historically correct answer is "both", the current answer is "Google-hosted with private connectivity options."

[Table of Contents](#Looker)

## What is the purpose of Looker's Liquid syntax in LookML?

Looker's Liquid syntax is used within LookML to dynamically generate SQL or control the behavior of dimensions, measures, or filters based on conditions or user inputs.

Liquid runs at query-generation time and can read parameters, user attributes, filters, and dates. It is the mechanism behind parameterized dimensions, date-range-aware PDT SQL, and conditional field masking.

```text
dimension: dynamic_metric {
  sql:
    {% if _parameter_value == 'revenue' %} ${total_revenue}
    {% elsif _parameter_value == 'orders' %} ${order_count}
    {% else %} NULL {% endif %} ;;
}

parameter: _parameter_value {
  type: unquoted
  allowed_value: { label: "Revenue" value: "revenue" }
  allowed_value: { label: "Orders" value: "orders" }
  default_value: "revenue"
}
```

```text
# Liquid can read the filter the user selected, e.g. for a date-bounded PDT
derived_table: {
  sql:
    SELECT * FROM analytics.events
    WHERE event_date BETWEEN {% date_start event_date %} AND {% date_end event_date %} ;;
}
```

[Table of Contents](#Looker)

## How does Looker handle data storage and scalability?

Looker does not handle data storage directly. It relies on the underlying data infrastructure, such as data warehouses or databases, which provide storage and scalability capabilities.

What Looker Cloud stores: metadata (projects, users, content), query history, and result cache. What it does not store: your analytical data. Scalability therefore follows the warehouse; a slow, unpartitioned warehouse cannot be fixed in LookML.

[Table of Contents](#Looker)

## Can Looker integrate with data cataloging tools?

Looker can integrate with data cataloging tools through APIs or connectors, enabling seamless data discovery and cataloging across the organization.

```text
Catalog integration patterns
  push: Looker API -> DataHub/OpenMetadata/Atlas ingestion (dashboards, explores, fields)
  pull: dbt exposures + warehouse catalog referenced from LookML descriptions
  classify: tags in LookML flow into catalog search
```

[Table of Contents](#Looker)

## What is the purpose of Looker's "Always Use SQL Runner" option?

Looker's "Always Use SQL Runner" option allows users to bypass LookML and directly write and execute custom SQL queries using Looker's SQL Runner interface.

In practice this is an admin/developer preference that routes query authoring to SQL Runner. Treat it as a break-glass path: it bypasses the semantic layer, so results cannot be compared with governed metrics and are not covered by row-level security expressed in LookML. Most teams disable it for general users and keep it for developers.

[Table of Contents](#Looker)

## How does Looker handle data replication for disaster recovery purposes?

Looker relies on the underlying data infrastructure for data replication and disaster recovery. Proper backup and replication strategies should be implemented at the database or data warehouse level.

For Looker itself, DR means metadata and content: Git remotes (or a mirror) hold the LookML, and content/dashboards can be exported via the API. Google Cloud provides the service-level DR for the Looker instance. The warehouse is the part you must design for RPO/RTO.

[Table of Contents](#Looker)

## Can Looker handle data exploration on semi-structured data formats like JSON or XML?

Looker supports data exploration on semi-structured data formats like JSON or XML through appropriate data modeling and transformations using LookML.

Model it as extraction, not exploration: parse JSON/XML in the warehouse into typed columns or a flattened view, then expose that view. Querying a JSON blob per Looker query prevents pruning and makes every tile full-scan.

```text
view: events_flat {
  sql_table_name: (
    SELECT
      event_id,
      event_ts,
      JSON_VALUE(properties, '$.utm_source') AS utm_source,
      JSON_VALUE(properties, '$.device')     AS device
    FROM `acme-data-prod.raw.events`
    WHERE event_date = CURRENT_DATE()
  ) ;;
}
```

[Table of Contents](#Looker)

## What is the purpose of Looker's Advanced Scheduling options?

Looker's Advanced Scheduling options allow users to define more complex and customizable schedules for report deliveries, including custom intervals and specific calendar dates.

Advanced scheduling adds cron expressions, time zones, filters at send time, conditional formatting/format variants, and multiple destinations per plan. For finance, the important ones are run-as owner vs run-as recipient (row-level security per recipient) and the failure notification so a broken delivery is noticed.

```python
# Advanced scheduled plan: cron, timezone, per-recipient security, format variants
from looker_sdk import models40 as md

plan = md.WriteScheduledPlan(
    name="Month-end finance pack",
    dashboard_id="42",
    crontab="0 6 1 * *",
    timezone="America/New_York",
    run_as_recipient=True,
    scheduled_plan_destination=[
        md.ScheduledPlanDestination(
            format="pdf", type="email", address="cfo@acme.com", apply_formatting=True
        )
    ],
)
print(plan.name)
```

[Table of Contents](#Looker)

## How does Looker handle user access controls in a multi-tenant environment?

Looker provides granular user access controls, allowing administrators to define permissions and restrictions for each user or group within a multi-tenant environment.

```text
Multi-tenant control stack (top to bottom)
  Embed SSO  -> issue a signed URL per user with tenant_id + role attributes
  Roles      -> model sets + permission sets per tenant tier
  LookML     -> access_filter on tenant_id for row-level isolation
  Warehouse  -> schema or database per large tenant, shared schema for the tail
  Cache      -> expect per-tenant cache entries; use tenant-agnostic rollups where possible
```

[Table of Contents](#Looker)

## Can Looker be integrated with data lake platforms like Hadoop or Amazon S3?

Looker can integrate with data lake platforms like Hadoop or Amazon S3 through appropriate connectors or APIs, allowing users to access and analyze data stored in those platforms.

Looker cannot read S3/HDFS directly; it queries a SQL engine over the lake — Athena/Trino, Databricks SQL, BigQuery BigLake/external tables, or Hive via a dialect. Performance depends on the lake table format (Iceberg/Delta/Hudi) and statistics; a raw Parquet directory queried through Trino will be slower than a managed warehouse table.

[Table of Contents](#Looker)

## What is the purpose of Looker's Development Mode?

Looker's Development Mode allows developers to make changes to LookML models without affecting the production environment. It provides a safe testing environment before deploying changes.

Development Mode creates a branch, keeps the IDE on dev until changes are committed, and can show a banner on content ("You are viewing in development mode"). Production is unaffected until Deploy. The important discipline: never validate against production data only — use a staging branch/environment and content validation before merging.

[Table of Contents](#Looker)

## Real world use cases for Looker

### 1. Marketing attribution for a multi-brand retailer

Business context: three brands share one data team; marketing wants CAC, ROAS, and channel mix by brand and campaign, refreshed daily, with each brand's team seeing only its own data. Volume: 12 ad platforms, 90M impressions/day, 14M sessions/day, 220K orders/day.

```text
ad APIs + clickstream + CRM -> dbt marts (finance.fct_marketing_daily)
   -> LookML: view marketing_daily + explore marketing
   -> access_filter by brand_id (user attribute from SSO groups)
   -> dashboard: CAC/ROAS tiles + campaign drill + alert on spend > plan
```

```text
explore: marketing_daily {
  access_filter: {
    field: marketing_daily.brand_id
    user_attribute: brand_id
  }
}

measure: cac {
  type: number
  value_format_name: usd
  sql: ${spend} / NULLIF(${new_customers}, 0) ;;
}

measure: roas {
  type: number
  value_format_name: usd
  sql: ${attributed_revenue} / NULLIF(${spend}, 0) ;;
}
```

Why this design: attribution logic lives once in LookML, so the three brand dashboards cannot drift; the brand row-level filter is a single user attribute fed from SSO groups, and the ratio measures are computed from summed components (never averaged), which is the difference between a defensible CAC and a misleading one.

### 2. Embedded analytics for a B2B SaaS platform

Business context: a vertical SaaS vendor sells usage analytics to 1,100 tenant companies inside its product; tenants only see their own data, and the vendor wants zero per-tenant modeling work. Volume: 2.5B events/month, 400 concurrent dashboard users, 60 tenants on premium isolated warehouses.

```text
product events -> warehouse (shared fct_usage + per-tenant schemas for premium)
   -> LookML model per tier
   -> SSO embed URLs from the product backend (signed with embed secret)
   -> tenant-scoped user attributes: tenant_id, plan, can_see_cost
```

```python
import base64
# Backend issues one signed embed URL per request; attributes carry the tenant
import hashlib
import hmac
import time
import urllib.parse

def signed_embed(secret: str, path: str, user: dict) -> str:
    params = {"embed_domain": "https://app.acme.com", **user}
    url = f"https://acme.looker.com{path}?{urllib.parse.urlencode(params)}"
    url += f"&nonce={time.time()}"
    url += "&signature=" + urllib.parse.quote(
        base64.b64encode(
            hmac.new(secret.encode(), url.encode(), hashlib.sha1).digest()
        ).decode()
    )
    return url

print(signed_embed("s3cr3t", "/embed/dashboards/usage",
                   {"tenant_id": "northwind", "plan": "premium"}))
```

Why this design: SSO embed plus a `tenant_id` user attribute means the model enforces isolation regardless of what the host application sends, one dashboard serves every tenant, and premium tenants can be routed to dedicated warehouses without changing the LookML or the product code beyond the attribute.

### 3. Regulatory reporting for a fintech

Business context: a lender must produce monthly capital and exposure reports with an auditable definition, regional row-level access, and a delivery to regulators and internal risk. Volume: 180M loan-month rows, 40 years of history, 12 report variants.

```text
core banking CDC -> warehouse (risk.fct_exposure, risk.dim_loan)
   -> LookML views with required_access_grants on PII and certified metrics
   -> dashboards + scheduled PDF/CSV deliveries to risk and regulators
   -> content validation in CI; every deliverable versioned
```

```text
measure: exposure_at_default {
  label: "Exposure at Default (EAD)"
  description: "Certified for regulatory reporting. Source: risk.fct_exposure.ead. Owner: risk-modeling."
  tags: ["certified", "regulatory"]
  type: sum
  sql: ${TABLE}.ead ;;
}

access_grant: view_borrower_pii {
  user_attribute: risk_pii_access
  allowed_values: ["true"]
}
```

Why this design: regulators require a single documented definition and an audit trail, so the metric, its description, and its tags live in Git where every change is reviewed; access grants keep borrower PII out of the reporting model except for the risk group, and scheduled Advanced deliveries with `run_as_recipient` ensure each region's report is filtered by that region's permissions.

### 4. Product analytics and retention for a consumer marketplace

Business context: the growth team wants weekly cohorts, retention curves, and feature adoption by acquisition channel, without asking the data team for every cut. Volume: 900M product events/month, 30M users, 24-month retention horizon.

```text
events -> warehouse (mart_user_activity_daily: user_id, ds, feature, channel)
   -> LookML: explore with cohort/retention derived table + parameters
   -> dashboard: cohort heatmap, retention curve, feature adoption
```

```text
view: cohort_activity {
  derived_table: {
    sql:
      WITH first_seen AS (
        SELECT user_id, MIN(event_date) AS cohort_date
        FROM marts.user_activity_daily GROUP BY 1
      )
      SELECT a.user_id, f.cohort_date,
             DATE_DIFF(a.event_date, f.cohort_date, DAY) AS day_number,
             a.feature, a.channel
      FROM marts.user_activity_daily a
      JOIN first_seen f USING (user_id) ;;
    datagroup_trigger: activity_default
    cluster_keys: ["cohort_date", "feature"]
  }

  dimension_group: cohort {
    type: time
    timeframes: [date, week, month]
    datatype: date
    sql: ${TABLE}.cohort_date ;;
  }

  dimension: day_number { type: number sql: ${TABLE}.day_number ;; }
  measure: users { type: count_distinct sql: ${TABLE}.user_id ;; }
}
```

Why this design: the cohort definition (first event date) is computed once in a persisted derived table, so every analyst gets the same retention number; clustering on cohort and feature keeps the weekly rebuild and the interactive heatmap affordable, and the parameterized explore lets growth self-serve cuts without new tiles.

### 5. Retail operations command center

Business context: a grocery chain monitors store operations in near real time during trading hours; a store manager sees only their store, a regional director only their region, and the exec team sees the chain. Volume: 1,200 stores, 40M transactions/day, 5-minute micro-batches.

```text
POS -> streaming/micro-batch -> warehouse (ops.store_trading_5m)
   -> LookML explores: store_ops (short cache) + chain_ops (aggregate)
   -> dashboard: sales vs plan, basket size, queue alerts
   -> access_filter: store_id for managers, region for directors
```

```text
explore: store_ops {
  persist_with: ops_5m          # max_cache_age: 5 minutes
  always_filter: { filters: [store_ops.business_date: "today"] }
  access_filter: [
    { field: store_ops.store_id, user_attribute: store_id },
    { field: store_ops.region,   user_attribute: region }
  ]
}

measure: sales_vs_plan_pct {
  type: number
  value_format_name: percent_1
  sql: ${net_sales} / NULLIF(${plan_sales}, 0) ;;
}
```

Why this design: a 5-minute cache with a today-only filter keeps the live dashboard cheap enough to serve 1,200 managers, while the region/chain views roll up from the same governed measures so a store manager and the COO cannot see different definitions of net sales; stacking two access filters lets one explore serve three levels of the org without three dashboards.

[Table of Contents](#Looker)
