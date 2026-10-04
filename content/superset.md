## [Main title](../README.md)
### [Interview questions](full.md)

# Superset

Apache Superset is a SQL-first BI layer. It does not store data and it does not have its own calculation engine: every chart becomes a SQL query against a database you connect to, and the metadata database only stores users, datasets, chart definitions, and schedules. That single architectural fact explains most of the answers below - performance, caching, security, and cross-database limits all follow from it.

+ [What is Apache Superset?](#What-is-Apache-Superset)
+ [How do you model datasets for Superset dashboards?](#How-do-you-model-datasets-for-Superset-dashboards)
+ [How do you improve Superset dashboard performance?](#How-do-you-improve-Superset-dashboard-performance)
+ [How does Superset differ from other BI tools?](#How-does-Superset-differ-from-other-BI-tools)
+ [Which programming language is Superset primarily built with?](#Which-programming-language-is-Superset-primarily-built-with)
+ [What are the key components of Superset?](#What-are-the-key-components-of-Superset)
+ [What databases does Superset support?](#What-databases-does-Superset-support)
+ [How can you install Superset?](#How-can-you-install-Superset)
+ [Can you explain the process of connecting a database to Superset?](#Can-you-explain-the-process-of-connecting-a-database-to-Superset)
+ [What is a slice in Superset?](#What-is-a-slice-in-Superset)
+ [How can you create a new slice in Superset?](#How-can-you-create-a-new-slice-in-Superset)
+ [What is a dashboard in Superset?](#What-is-a-dashboard-in-Superset)
+ [How can you create a new dashboard in Superset?](#How-can-you-create-a-new-dashboard-in-Superset)
+ [What are the different visualization types available in Superset?](#What-are-the-different-visualization-types-available-in-Superset)
+ [Can you create custom visualizations in Superset?](#Can-you-create-custom-visualizations-in-Superset)
+ [What is SQL Lab in Superset?](#What-is-SQL-Lab-in-Superset)
+ [What are the advantages of using SQL Lab in Superset?](#What-are-the-advantages-of-using-SQL-Lab-in-Superset)
+ [Can you schedule and automate reports in Superset?](#Can-you-schedule-and-automate-reports-in-Superset)
+ [How can you secure Superset?](#How-can-you-secure-Superset)
+ [What is Druid in the context of Superset?](#What-is-Druid-in-the-context-of-Superset)
+ [Can you integrate Superset with other BI tools or data platforms?](#Can-you-integrate-Superset-with-other-BI-tools-or-data-platforms)
+ [How can you extend Superset's functionality?](#How-can-you-extend-Supersets-functionality)
+ [What are some ways to optimize query performance in Superset?](#What-are-some-ways-to-optimize-query-performance-in-Superset)
+ [What is the role of metadata databases in Superset?](#What-is-the-role-of-metadata-databases-in-Superset)
+ [Can you integrate Superset with version control systems?](#Can-you-integrate-Superset-with-version-control-systems)
+ [How does Superset handle data security and access control?](#How-does-Superset-handle-data-security-and-access-control)
+ [What is Superset's "Explore" feature?](#What-is-Supersets-Explore-feature)
+ [Can you define metrics and dimensions in Superset?](#Can-you-define-metrics-and-dimensions-in-Superset)
+ [How does Superset handle large datasets?](#How-does-Superset-handle-large-datasets)
+ [What is the purpose of the Superset configuration file?](#What-is-the-purpose-of-the-Superset-configuration-file)
+ [Can you deploy Superset in a distributed environment?](#Can-you-deploy-Superset-in-a-distributed-environment)
+ [How does Superset handle data lineage and data governance?](#How-does-Superset-handle-data-lineage-and-data-governance)
+ [What is Superset's SQL Lab Ad-Hoc Editor?](#What-is-Supersets-SQL-Lab-Ad-Hoc-Editor)
+ [Does Superset support geospatial data visualization?](#Does-Superset-support-geospatial-data-visualization)
+ [What are Superset's alerting capabilities?](#What-are-Supersets-alerting-capabilities)
+ [How can you monitor the performance of Superset?](#How-can-you-monitor-the-performance-of-Superset)
+ [Can Superset connect to streaming data sources?](#Can-Superset-connect-to-streaming-data-sources)
+ [What is Superset's data caching mechanism?](#What-is-Supersets-data-caching-mechanism)
+ [Does Superset support embedding dashboards in other applications?](#Does-Superset-support-embedding-dashboards-in-other-applications)
+ [What is the Superset SQL Lab Query History feature?](#What-is-the-Superset-SQL-Lab-Query-History-feature)
+ [Can you share dashboards with other users in Superset?](#Can-you-share-dashboards-with-other-users-in-Superset)
+ [Does Superset support data exploration using natural language queries (NLQ)?](#Does-Superset-support-data-exploration-using-natural-language-queries-NLQ)
+ [What are some common security best practices for deploying Superset?](#What-are-some-common-security-best-practices-for-deploying-Superset)
+ [Can Superset handle real-time data processing and visualization?](#Can-Superset-handle-real-time-data-processing-and-visualization)
+ [How can you create interactive filters in Superset?](#How-can-you-create-interactive-filters-in-Superset)
+ [What is Superset's support for user-defined functions (UDFs)?](#What-is-Supersets-support-for-user-defined-functions-UDFs)
+ [Can Superset connect to data lakes or distributed file systems?](#Can-Superset-connect-to-data-lakes-or-distributed-file-systems)
+ [What is Superset's approach to data caching and cache invalidation?](#What-is-Supersets-approach-to-data-caching-and-cache-invalidation)
+ [Can Superset handle data from multiple databases or data sources within the same dashboard?](#Can-Superset-handle-data-from-multiple-databases-or-data-sources-within-the-same-dashboard)
+ [How can you customize the look and feel of Superset's visualizations and dashboards?](#How-can-you-customize-the-look-and-feel-of-Supersets-visualizations-and-dashboards)
+ [What is Superset's support for row-level security (RLS)?](#What-is-Supersets-support-for-row-level-security-RLS)
+ [Does Superset support multi-tenancy?](#Does-Superset-support-multi-tenancy)
+ [What is Superset's support for time-series data analysis?](#What-is-Supersets-support-for-time-series-data-analysis)
+ [Can Superset connect to NoSQL databases?](#Can-Superset-connect-to-NoSQL-databases)
+ [What is Superset's integration with Apache Airflow?](#What-is-Supersets-integration-with-Apache-Airflow)
+ [Can you integrate Superset with external authentication systems?](#Can-you-integrate-Superset-with-external-authentication-systems)
+ [What is Superset's support for data storytelling and annotations?](#What-is-Supersets-support-for-data-storytelling-and-annotations)
+ [Does Superset provide data lineage tracking?](#Does-Superset-provide-data-lineage-tracking)
+ [How does Superset handle data caching for queries with dynamic parameters?](#How-does-Superset-handle-data-caching-for-queries-with-dynamic-parameters)
+ [What is Superset's support for anomaly detection?](#What-is-Supersets-support-for-anomaly-detection)
+ [Can you create drill-down or drill-through reports in Superset?](#Can-you-create-drill-down-or-drill-through-reports-in-Superset)
+ [What is Superset's support for data permissions and data masking?](#What-is-Supersets-support-for-data-permissions-and-data-masking)
+ [Can Superset be used for real-time data streaming analytics?](#Can-Superset-be-used-for-real-time-data-streaming-analytics)
+ [What is the Superset Database Metadata Model?](#What-is-the-Superset-Database-Metadata-Model)
+ [How does Superset handle data lineage in complex data pipelines?](#How-does-Superset-handle-data-lineage-in-complex-data-pipelines)
+ [What are some security considerations when using Superset in a production environment?](#What-are-some-security-considerations-when-using-Superset-in-a-production-environment)
+ [Can Superset integrate with external data catalog systems?](#Can-Superset-integrate-with-external-data-catalog-systems)
+ [What is Superset's support for data access logging and auditing?](#What-is-Supersets-support-for-data-access-logging-and-auditing)
+ [Can you create custom SQL functions or macros in Superset?](#Can-you-create-custom-SQL-functions-or-macros-in-Superset)
+ [What is Superset's support for dashboard interactivity and filtering?](#What-is-Supersets-support-for-dashboard-interactivity-and-filtering)
+ [Does Superset support data lineage across multiple dashboards and slices?](#Does-Superset-support-data-lineage-across-multiple-dashboards-and-slices)
+ [What is Superset's support for time-zone conversions in visualizations?](#What-is-Supersets-support-for-time-zone-conversions-in-visualizations)
+ [Can Superset connect to cloud-based data warehouses like Amazon Redshift or Google BigQuery?](#Can-Superset-connect-to-cloud-based-data-warehouses-like-Amazon-Redshift-or-Google-BigQuery)
+ [What is Superset's support for data exploration on streaming data sources?](#What-is-Supersets-support-for-data-exploration-on-streaming-data-sources)
+ [Does Superset support cross-database joins in SQL queries?](#Does-Superset-support-cross-database-joins-in-SQL-queries)
+ [How do you define a dataset in Superset (physical vs virtual)?](#How-do-you-define-a-dataset-in-Superset-physical-vs-virtual)
+ [How do you use Jinja templating and CTEs in SQL Lab?](#How-do-you-use-Jinja-templating-and-CTEs-in-SQL-Lab)
+ [How do you manage Superset as code with the API and CLI?](#How-do-you-manage-Superset-as-code-with-the-API-and-CLI)
+ [Real world use cases for Superset](#Real-world-use-cases-for-Superset)

## What is Apache Superset?

Apache Superset is an open-source business intelligence (BI) and data visualization tool that enables users to explore and analyze large datasets using interactive visualizations, dashboards, and SQL-based queries.

It is a **semantic-free** BI tool: there is no proprietary in-memory engine or extract format. A chart is generated as SQL, sent to the connected database, and the result set is rendered in the browser. The metadata database (Postgres/MySQL) stores dashboards, charts, datasets, users, and schedules - never the analytical data.

```text
browser -> Superset web/API server -> SQLAlchemy -> warehouse (Snowflake/BigQuery/Trino/...)
                    |
              metadata DB (dashboards, datasets, users, RLS, alerts)
```

[Table of Contents](#Superset)

## How do you model datasets for Superset dashboards?

Superset works best when datasets are already clean, documented, and modeled at the right grain. Create curated tables or views for dashboards instead of asking every chart to perform complex joins. Define certified datasets for trusted reporting.

Example:

```text
gold.fact_orders_daily -> Superset dataset -> revenue dashboard
```

This keeps dashboards fast and reduces metric inconsistencies across teams.

A dataset in Superset is a named table or view, or a saved SQL query (a "virtual dataset"). Keep joins and business rules in the warehouse (dbt models, views) so they are tested once and reused; reserve virtual datasets for a handful of shared queries that many charts need.

[Table of Contents](#Superset)

## How do you improve Superset dashboard performance?

Use efficient SQL, pre-aggregated tables, caching, database indexes/partitions, and appropriate chart limits. Avoid dashboards that run many expensive queries at once. Push heavy logic into warehouse models rather than custom SQL inside each chart.

Example:

+ bad: chart scans raw events for every page load
+ better: chart reads daily aggregate table refreshed hourly

Performance is usually solved in the data model and warehouse before it is solved in the BI tool.

The concrete levers, in order: pre-aggregate to the chart grain; partition and cluster the source table; enable result caching (`DATA_CACHE_CONFIG`); set a sane `ROW_LIMIT` and time range; reduce the number of charts per dashboard; and use asynchronous queries (`GLOBAL_ASYNC_QUERIES`) so one slow chart does not block the page.

[Table of Contents](#Superset)

## How does Superset differ from other BI tools?

Superset stands out due to its intuitive user interface, extensive customization options, and ability to handle large datasets. It supports multiple databases, provides a wide range of visualization options, and offers an interactive environment for data exploration.

| Aspect | Superset | Tableau / Power BI | Looker |
|---|---|---|---|
| Query model | SQL to the source DB | extract or live connection | LookML-generated SQL |
| Semantic layer | datasets + metrics | data source + calculations | LookML (strongest) |
| Cost | open source (infra + people) | per-seat license | per-seat + warehouse cost |
| Governance | roles, RLS, certified datasets | strong | strong |
| Extensibility | Python + React plugins, API | limited | LookML + API |
| Best fit | SQL-literate org, open stack | business-user org | governed metrics at scale |

The honest trade-off: Superset is cheaper and SQL-transparent, but it has a weaker semantic layer than Looker and a weaker self-service experience than Power BI. It wins when the organization already trusts dbt/warehouse models and wants dashboards without per-seat licensing.

[Table of Contents](#Superset)

## Which programming language is Superset primarily built with?

Superset is primarily built using Python.

The backend (Flask, SQLAlchemy, Celery, Pandas) is Python; the frontend is TypeScript/React with Apache ECharts and deck.gl for visualizations. Visualization plugins therefore have a Python registration class and a TypeScript implementation, which is why "custom viz" is not a Python-only task.

[Table of Contents](#Superset)

## What are the key components of Superset?

The key components of Superset include the web server, database backend, metadata database, and the visualization engine.

More precisely:

+ **Web/API server** (Flask + Gunicorn) - serves the UI, the REST API, and the SQL Lab query endpoint.
+ **Metadata database** - Postgres/MySQL holding users, datasets, charts, dashboards, RLS rules, alert/report schedules, and query history.
+ **Celery workers + broker** - run asynchronous queries, alerts, reports, and cache warmup.
+ **Cache backend** - Redis (or Memcached) for query results and dashboard metadata.
+ **Analytical databases** - the warehouses and engines Superset queries; they do all the heavy computation.

[Table of Contents](#Superset)

## What databases does Superset support?

Superset supports various databases, including MySQL, PostgreSQL, SQLite, Oracle, Microsoft SQL Server, and many others.

It supports anything with a SQLAlchemy dialect or a DB-API driver: Snowflake, BigQuery, Redshift, Trino/Presto, Athena, Databricks, ClickHouse, Druid, Pinot, DuckDB, Elasticsearch (SQL), and more. The practical checklist for a new engine is a maintained SQLAlchemy dialect, a driver compatible with the Python version, correct time-grain and `LIMIT` support, and a reasonably fast query path.

[Table of Contents](#Superset)

## How can you install Superset?

To install Superset, you can use pip, the Python package manager, by running the command `pip install apache-superset` (the package is `apache-superset`, not `superset`).

```bash
python -m venv .venv && source .venv/bin/activate
pip install apache-superset
export SUPERSET_SECRET_KEY="$(openssl rand -base64 42)"
superset db upgrade
superset fab create-admin --username admin --firstname Admin --lastname User \
  --email admin@example.com --password 'change-me'
superset init
superset run -p 8088 --with-threads
```

```yaml
# production: docker compose or the official Helm chart
# docker run -p 8088:8088 \
#   -e SUPERSET_SECRET_KEY=... \
#   -e DATABASE_DB=superset apache/superset:4.1.1
```

Production installs use the official container image or the Helm chart, with Postgres for metadata and Redis for the cache. `pip install` is fine for local evaluation.

[Table of Contents](#Superset)

## Can you explain the process of connecting a database to Superset?

To connect a database to Superset, you need to configure a database connection string in the Superset configuration file. This involves specifying the necessary details such as the host, port, database name, username, and password.

In practice you do it in the UI (**Settings -> Database Connections -> + Database**) or through the API, using a SQLAlchemy URI:

```text
snowflake://user:password@account/ANALYTICS/PUBLIC?warehouse=WH_XS&role=REPORTER
postgresql+psycopg2://user:password@host:5432/analytics
trino://user@trino.internal:8080/hive/gold
```

```bash
curl -X POST http://superset.internal/api/v1/database/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "database_name": "warehouse",
    "sqlalchemy_uri": "trino://svc_superset@trino.internal:8080/hive/gold",
    "expose_in_sqllab": true,
    "allow_run_async": true,
    "allow_ctas": false,
    "allow_dml": false
  }'
```

Then **Test Connection**, and optionally "Sync columns from source" so the columns appear in Explore. Prefer a read-only service account with a statement timeout; Superset should never be able to write to the warehouse.

[Table of Contents](#Superset)

## What is a slice in Superset?

In Superset, a slice represents a visual representation of a dataset, such as a chart or a table. The term comes from the classic Superset UI ("Slice" / "Slice Add"); in current versions and the API it is called a **chart** (`/api/v1/chart/`). The underlying object is the same: a named visualization plus its form data and dataset reference.

[Table of Contents](#Superset)

## How can you create a new slice in Superset?

To create a new slice in Superset, you can use the Slice Add form, which allows you to select the visualization type, choose the dataset, and configure various chart-specific settings.

The current flow is **Charts -> + Chart**, or open SQL Lab, run a query, and choose **Create Chart**. The chart form is the same Explore view, pre-filled with the query you just ran.

[Table of Contents](#Superset)

## What is a dashboard in Superset?

A dashboard in Superset is a collection of slices, visualizations, and filters that provide a comprehensive view of the data. It also carries native filters, a layout, and metadata such as owners, tags, and a published state.

[Table of Contents](#Superset)

## How can you create a new dashboard in Superset?

To create a new dashboard in Superset, you can use the Dashboard Add form, which enables you to select and arrange slices, define filters, and set other dashboard-specific properties.

Charts can be added from a chart's **Save -> Add to dashboard** action, then arranged in a grid. Native filters are configured once at the dashboard level and applied to the charts that declare the matching column.

[Table of Contents](#Superset)

## What are the different visualization types available in Superset?

Superset offers a wide range of visualization types, including bar charts, line charts, scatter plots, pie charts, maps, tables, and many more.

Grouped for interviews:

+ **Time series**: line, area, bar, scatter, time-series table, forecast.
+ **Comparison**: bar, funnel, gauge, big number with trendline.
+ **Part-to-whole**: pie, treemap, sunburst, sankey.
+ **Distribution / correlation**: histogram, box plot, heatmap, scatter, bubble.
+ **Tabular**: table, pivot table, time-series table, hand's-on table.
+ **Geospatial**: deck.gl scatter, heatmap, polygon, GeoJSON, mapbox lines.
+ **Flow / hierarchy**: Sankey, chord, graph, treemap.

[Table of Contents](#Superset)

## Can you create custom visualizations in Superset?

Yes, Superset allows you to create custom visualizations using the rich set of visualization libraries available in Python.

Be precise in an interview: a visualization plugin has a **Python class** (metadata: name, control panel, query requirements) and a **TypeScript/React component** that renders the chart, usually with ECharts or deck.gl. You scaffold it with the Superset CLI (`superset viz plugin` generators), build the frontend, and register the plugin. Python alone is not enough unless you reuse an existing plugin type.

[Table of Contents](#Superset)

## What is SQL Lab in Superset?

SQL Lab is a feature in Superset that allows users to write and execute SQL queries directly against the connected databases. It includes a schema browser, autocomplete, a results grid with export, query history, and one-click conversion of a query into a virtual dataset or chart.

[Table of Contents](#Superset)

## What are the advantages of using SQL Lab in Superset?

SQL Lab provides an interactive and collaborative environment for data exploration, ad-hoc querying, and iterative development of SQL queries.

```sql
-- SQL Lab: check the grain and freshness of a candidate dataset
select order_date,
       count(*)          as orders,
       sum(net_amount)   as net_revenue,
       max(updated_at)   as last_load
from gold.fact_orders_daily
where order_date >= current_date - interval '30' day
group by order_date
order by order_date desc;
```

It is also the fastest path from exploration to production: save the query as a virtual dataset, define metrics, and build a chart on top - without asking a data engineer to publish a table.

[Table of Contents](#Superset)

## Can you schedule and automate reports in Superset?

Yes, Superset supports report scheduling and automation using the Celery distributed task queue. You can define periodic jobs to run queries and send reports via email or other communication channels.

This is the **Reports** feature under **Settings -> Alerts & Reports**. A report takes a dashboard or chart, a schedule (cron), a time range, and a delivery target (email, Slack, or a webhook), and can attach a screenshot or a CSV/PDF export.

```bash
# create a scheduled report through the API
curl -X POST http://superset.internal/api/v1/report/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name": "Weekly revenue PDF",
    "type": "Report",
    "dashboard_id": 12,
    "crontab": "0 7 * * 1",
    "timezone": "America/New_York",
    "active": true,
    "recipients": [{"type": "email", "recipient": "finance@example.com"}]
  }'
```

Reports need the Celery worker, beat scheduler, and `screenshot`/`thumbnails` support (a headless Chrome) for image and PDF output. Email settings come from `SMTP_*` config or `ALERT_REPORTS_NOTIFICATION_DRY_RUN` in dev.

[Table of Contents](#Superset)

## How can you secure Superset?

Superset can be secured by enabling authentication and authorization mechanisms such as LDAP, OAuth, or database-backed authentication. Additionally, you can configure role-based access control (RBAC) to control user permissions.

The layers that matter: network (put Superset behind TLS and a private load balancer), authentication (SSO/OAuth/LDAP plus MFA at the identity provider), authorization (roles and per-dataset permissions), data access (RLS rules and, if needed, database-enforced controls), and secrets (`SUPERSET_SECRET_KEY` stored in a secret manager, database credentials stored encrypted with `FERNET_KEY`).

[Table of Contents](#Superset)

## What is Druid in the context of Superset?

Druid is an open-source distributed data store designed for real-time analytics. In Superset, Druid can be used as a backend database to provide high-performance querying and visualization capabilities.

Druid was Superset's original backend and remains a first-class engine: sub-second aggregation on high-cardinality event data, pre-aggregated rollups, and native time-series support. The trade-off is another distributed system to operate; many teams now use ClickHouse, StarRocks, or a warehouse instead, and Superset treats them all the same way - send SQL, render the result.

[Table of Contents](#Superset)

## Can you integrate Superset with other BI tools or data platforms?

Yes, Superset provides integration capabilities with other BI tools and data platforms. It supports data ingestion from various sources and can also export visualizations and dashboards to different formats.

Realistic integrations: embed Superset charts in another application (guest tokens or the embedded SDK), export charts and dashboards as JSON for migration, pull/push metadata through the REST API, deliver scheduled reports by email/Slack, and connect to the same warehouse that Tableau/Looker use during a migration. Superset is not an ingestion tool - data arrives through the warehouse.

[Table of Contents](#Superset)

## How can you extend Superset's functionality?

Superset allows you to extend its functionality by creating custom visualization plugins, integrating with external systems using its API, or developing new features using its extensible architecture.

Other extension points: custom **database engines/specs**, custom **security managers** (for SSO), custom **Celery tasks**, `FLASK_APP_MUTATOR` for extra routes and middleware, and the `superset_config.py` hooks for caching and feature flags.

[Table of Contents](#Superset)

## What are some ways to optimize query performance in Superset?

Some ways to optimize query performance in Superset include using appropriate indexes on database tables, aggregating data at the database level, caching query results, and tuning Superset's configuration settings.

A concrete checklist:

```text
1. pre-aggregate: chart reads gold.fact_orders_daily, not raw events
2. partition/cluster the source on the filter columns (date, tenant)
3. limit the dashboard time range and set ROW_LIMIT (default 10000)
4. enable caching: DATA_CACHE_CONFIG + per-dataset "cache timeout"
5. use async queries so slow charts do not block the page
6. reduce charts per dashboard; a dashboard is N queries, not one
7. avoid SELECT * in virtual datasets; project only needed columns
```

[Table of Contents](#Superset)

## What is the role of metadata databases in Superset?

Metadata databases store information about Superset's data models, users, dashboards, and other system-related metadata. They help manage and organize Superset's internal data structures.

Concretely the metadata DB holds: users/roles/permissions, database connections (with encrypted credentials), datasets and their columns/metrics, charts, dashboards, RLS rules, alert/report schedules, SQL Lab query history, and audit logs. It should be a managed Postgres (not SQLite) with backups, because losing it means losing every dashboard definition.

[Table of Contents](#Superset)

## Can you integrate Superset with version control systems?

Yes, you can integrate Superset with version control systems like Git by storing Superset's configuration files, dashboards, and visualization definitions in a Git repository. This enables versioning, collaboration, and easy deployment.

Two practical patterns: export dashboards/charts/datasets as YAML/JSON with `superset export-dashboards` and commit those artifacts; or run a GitOps pipeline that imports them into each environment after review. Keep `superset_config.py` in git as well, but never commit secrets - reference environment variables instead.

[Table of Contents](#Superset)

## How does Superset handle data security and access control?

Superset provides access control through role-based permissions. You can define roles and assign them specific permissions to control who can access and modify datasets, slices, dashboards, and other resources.

+ **Roles**: `Admin`, `Alpha`, `Gamma`, `Public`, plus custom roles. `Gamma` users need explicit access to databases and datasets.
+ **Dataset access**: grant a role access to specific datasets rather than to the whole database.
+ **RLS**: filter rows automatically per user/role.
+ **Column-level**: the `masked`/`%` handling and certified-dataset metadata help, but true masking belongs in a secure view or the database.

[Table of Contents](#Superset)

## What is Superset's "Explore" feature?

The "Explore" feature in Superset allows users to interactively explore datasets, execute SQL queries, apply filters, and visualize the results using different chart types.

Explore is the chart builder: it runs a query built from the dataset's columns, metrics, filters, time range, and chart-specific controls, then re-runs it on every change. It is where a saved chart is defined, and it is the same UI that SQL Lab hands off to with **Create Chart**.

[Table of Contents](#Superset)

## Can you define metrics and dimensions in Superset?

Yes, in Superset, you can define metrics (aggregations) and dimensions (groupings) to create complex analytical queries and visualizations.

```yaml
# dataset definition (exported YAML, simplified)
table_name: fact_orders_daily
metrics:
  - metric_name: net_revenue
    expression: SUM(net_amount)
  - metric_name: avg_order_value
    expression: SUM(net_amount) / NULLIF(COUNT(DISTINCT order_id), 0)
    metric_type: derived
columns:
  - column_name: order_date
    is_dttm: true          # time column
  - column_name: country_code
    groupby: true
  - column_name: channel
    groupby: true
```

Metrics are saved expressions - put the business definition here so every chart uses the same formula. Dimensions are the columns (or column expressions) available for `GROUP BY` and filters. Derived metrics can reference other metrics, which keeps formulas readable.

[Table of Contents](#Superset)

## How does Superset handle large datasets?

Superset can handle large datasets by leveraging the power of the underlying database systems. It uses efficient SQL queries and implements pagination and caching mechanisms to optimize performance.

It never loads the full dataset: SQL Lab paginates, Explore aggregates in the database, and the browser receives only the result set (bounded by `ROW_LIMIT`). "Handling large datasets" is really "generate good SQL and let the warehouse do the work". If a chart is slow, the fix is upstream - a smaller aggregate, a partition filter, or a faster engine.

[Table of Contents](#Superset)

## What is the purpose of the Superset configuration file?

The Superset configuration file contains various settings and parameters that define the behavior and customization options for the Superset instance.

`superset_config.py` is imported at startup and can override any setting, for example:

```python
# superset_config.py
import os

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]
SQLALCHEMY_DATABASE_URI = os.environ["SUPERSET_METADATA_URI"]
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")

DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}
FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    "GLOBAL_ASYNC_QUERIES": True,
    "ALERT_REPORTS": True,
}
SQLLAB_TIMEOUT = 300
SUPERSET_WEBSERVER_TIMEOUT = 120
ROW_LIMIT = 10000
```

The file is usually mounted from a ConfigMap/secret, with all secrets coming from environment variables.

[Table of Contents](#Superset)

## Can you deploy Superset in a distributed environment?

Yes, Superset can be deployed in a distributed environment using tools like Kubernetes or Docker Swarm to manage containerized instances of Superset across multiple nodes or machines.

The reference topology is: N stateless web/API pods behind a load balancer, M Celery worker pods, one Celery beat pod, one metadata Postgres, one Redis, and a shared `superset_config.py`. The official Helm chart packages exactly this.

```yaml
# values.yaml (abridged)
replicaCount: 4
celery:
  worker:
    replicaCount: 6
  beat: true
postgresql:
  enabled: true
redis:
  enabled: true
configOverrides:
  secret: |
    SECRET_KEY = "..."
```

Two operational rules: never run more than one `superset db upgrade` at a time (use a pre-install Job with a lock), and always set a shared `SECRET_KEY` across all pods or sessions and encrypted credentials break.

[Table of Contents](#Superset)

## How does Superset handle data lineage and data governance?

Superset provides features to capture and display data lineage, allowing users to track the source and transformations of data used in dashboards and visualizations. It also supports data governance by enforcing access controls and data security measures.

Be precise: Superset captures the **object graph** (chart -> dataset -> database, and which dashboards use a chart), and recent versions add dataset/column lineage derived from SQL parsing. It is not a full column-level lineage system across the whole warehouse - for that you pair it with OpenLineage/Marquez, DataHub, or your dbt docs, and use the Superset API to publish dashboard usage into the catalog.

[Table of Contents](#Superset)

## What is Superset's SQL Lab Ad-Hoc Editor?

The SQL Lab Ad-Hoc Editor in Superset provides a web-based interface where users can write and execute SQL queries, visualize query results, and save queries for future reference.

The editor supports multiple tabs/query history, a schema browser, Jinja templating for parameterized queries, CTAS/insert when the database allows it, and export to CSV/Excel. Saved queries become virtual datasets that charts can build on.

[Table of Contents](#Superset)

## Does Superset support geospatial data visualization?

Yes, Superset supports geospatial data visualization by providing map charts and integrating with map libraries like Leaflet and Mapbox.

The current deck.gl-based charts are the recommended path: scatter, heatmap, hexagon, GeoJSON polygons, arcs, and paths. They need a latitude/longitude pair plus optional metrics, and Mapbox charts need `MAPBOX_API_KEY`; the non-Mapbox variants render on a base map without a key.

[Table of Contents](#Superset)

## What are Superset's alerting capabilities?

Superset has limited built-in alerting capabilities. However, you can leverage external tools or integrate Superset with alerting systems to set up notifications based on predefined metrics or thresholds.

This used to be true, but modern Superset ships **Alerts & Reports** natively. An alert is a saved chart plus a SQL condition (for example `value > 1000`) checked on a schedule; when it fires, Celery sends email/Slack notifications and optionally a screenshot.

```text
Alert: "Daily net revenue below plan"
  chart:   Net revenue (last 7 days)
  condition:  sum(net_revenue) < 250000
  schedule:   0 9 * * *
  action:     email finance-ops
```

For anything richer (multi-metric anomaly detection, incident routing, SLO burn rate), Superset is a notifier - the real monitoring lives in Prometheus/Grafana or a data-quality tool, and Superset can be triggered by the API.

[Table of Contents](#Superset)

## How can you monitor the performance of Superset?

Superset can be monitored using various tools like monitoring agents, log analyzers, and performance tracking systems. You can analyze server logs, monitor resource usage, and track query performance to identify and resolve bottlenecks.

Superset exposes Prometheus metrics at `/metrics` (web, Celery, cache, and `sqllab_*` timings) and stores query execution records in the metadata DB.

```text
# slow queries and error rate
histogram_quantile(0.95, sum(rate(superset_sqllab_query_duration_seconds_bucket[5m])) by (le))
sum(rate(superset_sqllab_query_errors_total[5m]))
```

Watch web pod memory (large result sets), Celery queue depth and task duration, Redis evictions, metadata-DB connection saturation, and error rates per database. Enable `statsd`/`otel` exporters if you already standardize on them.

[Table of Contents](#Superset)

## Can Superset connect to streaming data sources?

Yes, Superset can connect to streaming data sources by leveraging technologies like Apache Kafka or Apache Pulsar. It can consume data from topics or streams and visualize it in real-time.

This is misleading as stated. Superset has **no Kafka connector**: it issues SQL and cannot consume a topic. What you actually do is land the stream in a queryable store - Druid, Pinot, ClickHouse, Rockset, a Flink/Kafka sink, or a warehouse micro-batch - and connect Superset to that. Freshness is then bounded by the sink, not by Superset.

[Table of Contents](#Superset)

## What is Superset's data caching mechanism?

Superset provides data caching to improve query performance and reduce the load on the underlying databases. It stores query results in a cache and serves subsequent requests from the cache instead of executing the queries again.

```python
# cache chart query results for 5 minutes (a per-deployment choice)
DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}
# dashboards also cache their metadata/permissions layout briefly
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}
```

Each dataset can override the timeout in its settings ("Cache timeout"), and chart-level "force refresh" bypasses the cache. The cache key is derived from the query context; if you rely on row-level security, confirm that per-user caching is enabled (`CACHE_QUERY_BY_USER` or per-database caching) so users with different rules cannot share a cached result.

[Table of Contents](#Superset)

## Does Superset support embedding dashboards in other applications?

Yes, Superset supports embedding dashboards in other applications by providing embed codes or URLs that can be integrated into web pages or portals.

Two mechanisms:

+ **Embedded dashboard (guest token)** - the host app authenticates the user, calls `POST /api/v1/security/guest_token/`, and renders `<superset-embedded-sdk>` with the token. RLS can be applied per guest with a `rls` clause in the token.
+ **Public link** - a read-only URL for anyone with the link. Fine for marketing dashboards, not for internal data.

```text
import { embedDashboard } from "@superset-ui/embedded-sdk";

embedDashboard({
  id: "2f1b8f4e-...",
  supersetDomain: "https://superset.example.com",
  mountPoint: document.getElementById("dashboard"),
  fetchGuestToken: () => fetch("/api/guest-token").then((r) => r.json()),
});
```

[Table of Contents](#Superset)

## What is the Superset SQL Lab Query History feature?

The SQL Lab Query History feature in Superset allows users to view their previously executed queries, review query results, and rerun or modify queries as needed.

History is stored in the metadata database and is filterable by user, database, status, and time (admins can see all users' queries). It is the first place to look when a dashboard is slow or wrong: the exact SQL that ran, its duration, and its error are all there.

[Table of Contents](#Superset)

## Can you share dashboards with other users in Superset?

Yes, in Superset, you can share dashboards with other users by providing them with the dashboard's URL or embedding the dashboard in other applications. You can also control access permissions to restrict or allow specific users to view and edit the dashboards.

Sharing options: add owners/editors, grant a role access to the underlying dataset (needed or the charts are empty), share a permalink with the current filter state, publish the dashboard, or embed it. A user who can see the dashboard but not the dataset sees an access error per chart - a common support ticket.

[Table of Contents](#Superset)

## Does Superset support data exploration using natural language queries (NLQ)?

Superset does not natively support NLQ. However, you can integrate Superset with NLQ platforms or use external libraries to enable natural language query capabilities.

There is active work in the ecosystem (including AI assistants/SDK experiments), but the reliable pattern is an external NL-to-SQL service that writes SQL Lab queries or hits the API; the user still reviews the generated SQL before it becomes a certified chart.

[Table of Contents](#Superset)

## What are some common security best practices for deploying Superset?

Some common security best practices for deploying Superset include using HTTPS for secure communication, enforcing strong passwords and authentication methods, restricting database access privileges, and keeping the software up to date with security patches.

Add: set a strong `SUPERSET_SECRET_KEY` and `FERNET_KEY` from a secret manager; use SSO with MFA; run database connections with read-only accounts and statement timeouts; disable `allow_dml`/`allow_ctas` unless required; put the metadata DB and Redis on private networks; restrict `PUBLIC_ROLE_LIKE` so anonymous access has no datasets; enable `TALISMAN_ENABLED` security headers; and audit role grants regularly.

[Table of Contents](#Superset)

## Can Superset handle real-time data processing and visualization?

Superset can handle real-time data processing and visualization when used with appropriate data stores like Apache Druid or by integrating with streaming data platforms.

Superset does no processing. Real-time means the connected store is real-time (Druid, Pinot, ClickHouse) and the dashboard has a short cache timeout or cache disabled plus an auto-refresh interval. On a warehouse, dashboards are as fresh as the last load - typically minutes to hours - and the auto-refresh setting only re-runs the same query.

[Table of Contents](#Superset)

## How can you create interactive filters in Superset?

In Superset, you can create interactive filters by defining filter controls based on the dataset's columns. Users can then interact with these filters to dynamically update the displayed data.

Native filters are added at the dashboard level and scoped to specific charts; filter types include value, range, time range, time column, and numerical. Cross-filtering lets a click on one chart filter the rest. URL parameters (`?native_filters=...`) make a filtered view shareable.

[Table of Contents](#Superset)

## What is Superset's support for user-defined functions (UDFs)?

Superset supports user-defined functions (UDFs) by allowing you to define custom SQL functions in the database backend and use them in queries and visualizations.

Superset does not execute UDFs itself. You create the function in the database (or Trino/Spark), then reference it in a metric expression or a virtual dataset, and Superset sends it as plain SQL. Anything requiring a Python UDF must run in the database or upstream in the pipeline.

[Table of Contents](#Superset)

## Can Superset connect to data lakes or distributed file systems?

Yes, Superset can connect to data lakes or distributed file systems like Hadoop Distributed File System (HDFS) or Amazon S3 by using appropriate database connectors or file system interfaces.

In practice you put a SQL engine in front of the lake - Trino/Presto, Hive, Spark Thrift Server, Athena, Databricks SQL, or DuckDB - and connect Superset to that. Connecting Superset to "S3" directly is only possible through an engine that can query S3 (for example Athena over Glue or Trino with the Hive/Iceberg connector).

[Table of Contents](#Superset)

## What is Superset's approach to data caching and cache invalidation?

Superset employs a caching mechanism where query results are cached based on the underlying database and query parameters. Cache invalidation is handled by the cache timeout settings or by manually clearing the cache.

Invalidation options, from most to least common:

+ Wait for the per-dataset or global TTL to expire.
+ A data engineer calls `POST /api/v1/cachekey/invalidate` with the dataset or dashboard id after a load, which bumps the cache key so all users see fresh data.
+ Users click **Force refresh** on a chart or dashboard.
+ Alerts/reports always run with a fresh key so a scheduled report is not served stale data.

Because the cache key includes the query and the user, "invalidate a dataset" is the operation that matters after a nightly load; a global Redis flush is the blunt fallback.

[Table of Contents](#Superset)

## Can Superset handle data from multiple databases or data sources within the same dashboard?

Yes, Superset can handle data from multiple databases or data sources within the same dashboard by defining database connections and datasets for each source and then using appropriate joins or unions in the queries.

Be precise about the limitation: a dashboard may show charts from several databases, but **one chart queries exactly one database**. "Joins across sources" are not pushed down; you either replicate/conform the data into one store (the usual answer) or pre-join upstream. Cross-database joins in a single SQL statement are not possible - see the dedicated question below.

[Table of Contents](#Superset)

## How can you customize the look and feel of Superset's visualizations and dashboards?

Superset allows customization of visualizations and dashboards by providing options to modify chart properties, apply themes or styles, and use custom CSS or JavaScript code.

Options: per-chart controls, dashboard CSS via the dashboard settings (`css` field / `DASHBOARD_CSS`), a custom theme (`THEME_DEFAULT` / `THEME_DARK`, or the theme editor), custom logos and `APP_NAME`, and markdown/text components. Custom CSS is scoped to one dashboard and is a good place for branding, not for layout hacks that break on upgrade.

[Table of Contents](#Superset)

## What is Superset's support for row-level security (RLS)?

Superset supports row-level security (RLS) by allowing you to define filters or query conditions based on user-specific roles or attributes. This enables restricting data access based on user permissions.

```yaml
# RLS rule: a Gamma role sees only its region
name: emea_analyst_region
filter_type: Regular
tables:
  - dataset_id: 17          # gold.fact_orders_daily
roles:
  - emea_analyst
group_key: region_id
clause: "country_code IN ('DE','FR','NL','ES','IT')"
```

```python
# RLS derived from the logged-in user's JWT attribute
class CustomSecurityManager(SupersetSecurityManager):
    def get_rls_filters(self, table, user):
        if getattr(user, "region", None):
            return [f"country_code = '{user.region}'"]
        return []
```

RLS is enforced by **rewriting the SQL** before it is sent, so it applies to SQL Lab, Explore, and dashboards alike. It is not a database permission: a user who can bypass Superset and reach the warehouse directly is not protected by RLS.

[Table of Contents](#Superset)

## Does Superset support multi-tenancy?

Not natively. Superset has no tenant or workspace object to switch between, so multi-tenancy is built from its access-control features rather than enabled with a setting.

The accurate version: Superset has **no native tenant/workspace object**. Multi-tenancy is built from roles, dataset permissions, and RLS - one shared deployment with per-tenant roles, or one deployment per tenant for hard isolation. For an embedded, customer-facing use case, guest tokens plus per-guest RLS are the standard pattern; for strict regulatory separation, separate deployments are safer.

[Table of Contents](#Superset)

## What is Superset's support for time-series data analysis?

Superset provides robust support for time-series data analysis by offering specialized chart types like line charts, area charts, and time-series forecasting models.

It supports time grains (second through year), time comparison (previous period, same period last year), rolling windows, cumulative sums, and the seasonality/forecast options on the time-series charts. For anything beyond that, model the series upstream - Superset is a visualizer, not a forecasting engine.

[Table of Contents](#Superset)

## Can Superset connect to NoSQL databases?

Superset primarily focuses on SQL-based databases. However, you can use Superset's SQLAlchemy integration to connect to some NoSQL databases that have SQL-like interfaces, such as Apache Cassandra or MongoDB.

The practical rule: if the store speaks SQL (or a SQL-ish dialect) and has a SQLAlchemy driver, Superset can query it - MongoDB Atlas SQL, Cassandra via a Presto/Trino connector, Elasticsearch SQL, Druid's native connector, ClickHouse. A pure key-value store or a document store with no SQL endpoint is out of reach; query it through a pipeline that lands data in SQL.

[Table of Contents](#Superset)

## What is Superset's integration with Apache Airflow?

Superset integrates seamlessly with Apache Airflow, an open-source platform for workflow management. This integration allows you to schedule and orchestrate data pipelines, trigger dashboards based on pipeline execution, and use Airflow operators to interact with Superset.

Concrete patterns that hold up:

+ Airflow loads the warehouse, then invalidates the Superset cache (HTTP call or the `superset` provider's operator) so dashboards are fresh immediately.
+ An Airflow DAG calls the Superset API to export dashboards as code, or to trigger a report.
+ Superset alerts/reports have their own Celery scheduler and do **not** need Airflow; use Airflow only when report delivery must be part of a pipeline SLA.

[Table of Contents](#Superset)

## Can you integrate Superset with external authentication systems?

Yes, Superset provides integration options with external authentication systems like Lightweight Directory Access Protocol (LDAP), OAuth, or single sign-on (SSO) solutions. This allows users to log in to Superset using their existing credentials.

Supported paths: `AUTH_LDAP`, `AUTH_OAUTH` (Google, Okta, Azure AD, Keycloak, Auth0), `AUTH_REMOTE_USER` behind a proxy, SAML through `Authlib`, and `AUTH_DB` for local accounts. Role mapping from IdP groups to Superset roles (including `AUTH_ROLES_MAPPING` and `AUTH_ROLES_SYNC_AT_LOGIN`) is what avoids hand-managing permissions.

[Table of Contents](#Superset)

## What is Superset's support for data storytelling and annotations?

Superset supports data storytelling and annotations by providing features like markdown components, text boxes, and annotations on charts and dashboards. This enables users to add narrative context and insights to their visualizations.

There is a **Annotations** layer (time-based events such as a campaign launch or a deploy) that can be overlaid on time-series charts, plus dashboard header/divider/markdown components and per-chart descriptions. Use annotations for events that explain a spike; a dashboard without them tends to generate "why did this change?" tickets.

[Table of Contents](#Superset)

## Does Superset provide data lineage tracking?

Yes, Superset has built-in features to track data lineage by capturing and displaying information about the source tables, columns, and transformations used in the dashboards and visualizations.

Correct the overstatement: Superset tracks **usage lineage** - which dashboards use which charts, and which datasets and columns a chart references, plus dataset-level lineage from SQL parse when enabled. It does not track lineage from raw source tables through every transformation; that is the job of a catalog (DataHub, OpenMetadata, Unity Catalog) or OpenLineage, which can ingest Superset metadata through its API or exporter.

[Table of Contents](#Superset)

## How does Superset handle data caching for queries with dynamic parameters?

For queries with dynamic parameters, Superset intelligently handles data caching by including the parameter values as part of the cache key. This ensures that different query instances with different parameter values are not mixed up in the cache.

The cache key is derived from the database, the rendered query (after Jinja/parameters), and the user context, so `{{ filter_values('country') }}` with a different value produces a different key. The consequence is cache cardinality: highly dynamic filters with thousands of combinations can fill Redis with near-unique keys, so keep the TTL short for those charts and pre-aggregate where possible.

[Table of Contents](#Superset)

## What is Superset's support for anomaly detection?

Superset does not provide native support for anomaly detection. However, you can leverage Python libraries or integrate Superset with anomaly detection systems to incorporate anomaly detection capabilities.

Nuance: time-series charts include a seasonality/confidence-band option that can visually flag anomalies, and alerts can fire on a threshold. Serious anomaly detection (Prophet, isolation forest, SLO models) runs in a scheduled job that writes a flag/anomaly table, and Superset displays it - that keeps the model testable and reproducible.

[Table of Contents](#Superset)

## Can you create drill-down or drill-through reports in Superset?

Yes, Superset supports drill-down or drill-through reports by allowing users to interactively explore data hierarchies or navigate from summary-level visualizations to detailed information.

Drill-down is configured on a chart's dimensions (a hierarchy such as country -> region -> city) or via the chart's "Drill to detail" page, which runs a row-level query for the clicked point. Cross-filtering narrows the rest of the dashboard, and a dashboard URL with the filter state is the drill-through link to a second dashboard.

[Table of Contents](#Superset)

## What is Superset's support for data permissions and data masking?

Superset supports data permissions by enforcing role-based access control (RBAC), allowing you to grant or restrict access to specific datasets or columns. However, data masking functionality needs to be implemented at the database layer rather than within Superset.

That is broadly right. Superset can hide columns from a dataset (mark them not groupable/filterable) and RLS can restrict rows, but true masking - showing `***` or a hash - should be done with a secure view, a database policy, or a separate dataset for the restricted role. Never rely on hiding a column in the UI as a security control.

[Table of Contents](#Superset)

## Can Superset be used for real-time data streaming analytics?

Superset is primarily designed for interactive querying and visualization of stored data. While it can integrate with real-time data sources like Apache Kafka, it is not optimized for real-time data streaming analytics. For such use cases, a specialized streaming analytics platform would be more suitable.

The corrected statement: Superset queries a store, so "real-time" is a property of the store. With Druid/Pinot/ClickHouse and a short or disabled cache plus auto-refresh, dashboards refresh in seconds and are used for operational monitoring; with a warehouse they are minutes-to-hours. It has no windowing, no per-event alerts, and no streaming SQL, so true per-event monitoring belongs in Flink/Grafana.

[Table of Contents](#Superset)

## What is the Superset Database Metadata Model?

The Superset Database Metadata Model represents the structure and attributes of databases and tables within Superset. It stores information about the database connections, schemas, tables, columns, and other metadata.

In object terms: `Database` -> `Dataset` (table/view/virtual SQL) -> `TableColumn` and `SqlMetric`, and charts/dashboards reference the dataset. Column metadata is synced from the source ("Sync columns from source") or declared manually in a virtual dataset, and it is what drives Explore validation, autocomplete, and the CSV export types.

[Table of Contents](#Superset)

## How does Superset handle data lineage in complex data pipelines?

In complex data pipelines, Superset relies on the metadata captured from the underlying database systems to track data lineage. By ensuring that the database connections are properly configured, Superset can accurately capture and display data lineage across different data sources.

For a robust answer, separate the layers: the warehouse/dbt/catalog owns transformation lineage; Superset owns **consumption lineage** (which dashboard reads which dataset). Publishing Superset usage into the catalog - via the API, a metadata exporter, or OpenLineage - connects the two halves so an impact analysis ("what breaks if I drop this column?") covers both dashboards and models.

[Table of Contents](#Superset)

## What are some security considerations when using Superset in a production environment?

Some security considerations for using Superset in a production environment include enforcing secure communication over HTTPS, setting up strong authentication and authorization mechanisms, regularly updating Superset and its dependencies, and conducting regular security audits.

Superset-specific risks worth naming: the database connection credentials are stored encrypted with `FERNET_KEY`, so losing or rotating that key breaks every connection; a leaked guest token grants dashboard access until expiry; `allow_dml`/`allow_ctas` let a user write through Superset; and a `Gamma` user with access to a database can read anything the service account can read unless RLS or dataset permissions stop it. Treat Superset's service accounts as production credentials and review them.

[Table of Contents](#Superset)

## Can Superset integrate with external data catalog systems?

Yes, Superset can integrate with external data catalog systems by leveraging metadata connectors or APIs. This allows users to discover and explore datasets from the data catalog within the Superset interface.

Realistic integrations: push Superset charts/dashboards/dataset usage into the catalog via its API; pull dataset descriptions, owners, and tags back into Superset metadata; and link a dataset to its catalog page. There is no turnkey bidirectional sync in core Superset, so most teams write a small scheduled exporter.

[Table of Contents](#Superset)

## What is Superset's support for data access logging and auditing?

Superset provides logging capabilities that can be configured to record user activities, query executions, and system events. These logs can be used for auditing purposes and to track data access and usage.

Sources of truth: the metadata DB `query` table (SQL text, user, database, duration, status), the `logs`/audit tables when an audit backend is configured, application logs, and the database's own audit trail. Export query logs to your SIEM if data access must be audited, and remember that a query in SQL Lab can read any table the connection can read unless RLS or row/column restrictions apply.

[Table of Contents](#Superset)

## Can you create custom SQL functions or macros in Superset?

Yes, Superset allows you to define custom SQL functions or macros using the underlying database's capabilities or by using the SQLAlchemy expression language.

Split the two ideas:

+ **Macros** are Jinja in SQL Lab, metrics, and virtual datasets: `{{ current_username() }}`, `{{ filter_values('country') }}`, `{{ url_param('tenant') }}`, and custom Jinja context added in `superset_config.py` via `JINJA_CONTEXT_ADDONS`.
+ **Custom SQL functions** live in the database. Create them once (in the warehouse or Trino/Spark), then call them from a metric expression.

```python
# superset_config.py: expose a helper to every SQL Lab query
def jinja_context_addons():
    return {"tenant_id": lambda: current_tenant_id()}

JINJA_CONTEXT_ADDONS = jinja_context_addons()
```

[Table of Contents](#Superset)

## What is Superset's support for dashboard interactivity and filtering?

Superset provides robust support for dashboard interactivity and filtering. Users can interact with filters, drill down into specific data points, and dynamically update visualizations based on their selections.

Features: native filters (value, range, time, numerical), cross-filtering, drill-to-detail, drill-by-dimension, URL-shareable filter state, cascading filters that depend on another filter, and dashboard-level auto-refresh. A large dashboard with many native filters can issue many queries per change, so scope each filter to only the charts that need it.

[Table of Contents](#Superset)

## Does Superset support data lineage across multiple dashboards and slices?

Yes, Superset supports data lineage across multiple dashboards and slices. By capturing and displaying the metadata information, users can trace the origin and transformations of the data used in various dashboards and slices.

Within Superset you can see that a dataset is used by N charts and those charts appear on M dashboards, and you can filter the dashboard list by dataset. Cross-source/transformation lineage needs the catalog integration described above.

[Table of Contents](#Superset)

## What is Superset's support for time-zone conversions in visualizations?

Superset provides time-zone conversion capabilities for visualizations by allowing users to specify the desired time zone for date and time fields. This ensures that the data is displayed in the appropriate time zone based on the user's preference.

There are three time zones to keep straight: the **database** time zone (where the stored timestamp's meaning comes from), the **dataset/column** setting for a naive datetime, and the **user/profile** time zone used for display (`Timezone` in the user profile plus the dashboard time-range setting). Store UTC, set the user time zone, and test a DST boundary - most "the chart is off by an hour" bugs are a naive timestamp interpreted as local time.

[Table of Contents](#Superset)

## Can Superset connect to cloud-based data warehouses like Amazon Redshift or Google BigQuery?

Yes, Superset can connect to cloud-based data warehouses like Amazon Redshift, Google BigQuery, or Snowflake. It provides specific database connectors or dialects to establish connections and query data from these platforms.

Connection notes: Redshift uses the `redshift+redshift_connector` driver; BigQuery uses `bigquery://project/dataset` with a service-account JSON (`GOOGLE_APPLICATION_CREDENTIALS` or `BigQuery` extra); Snowflake uses key-pair or SSO auth and a dedicated warehouse (`warehouse=WH_BI&role=REPORTER`) so BI load cannot starve ETL. In all three, give Superset a read-only role and a warehouse/consumer group sized for concurrency.

[Table of Contents](#Superset)

## What is Superset's support for data exploration on streaming data sources?

Superset provides limited support for data exploration on streaming data sources. While it can connect to streaming platforms like Apache Kafka, the exploration capabilities are typically focused on visualizing historical data snapshots rather than real-time analysis.

Treat Kafka as an ingestion transport, not a Superset source. Land the stream in a queryable store (Druid, Pinot, ClickHouse, Iceberg/Trino, or a warehouse micro-batch) and explore that; freshness and retention are properties of the sink, and Superset gives you SQL, filters, and charts on top.

[Table of Contents](#Superset)

## Does Superset support cross-database joins in SQL queries?

Yes, Superset supports cross-database joins in SQL queries by utilizing the appropriate database connectors and schemas. It allows you to combine data from different databases using join statements.

This answer is wrong and is a good trap. **Superset does not support cross-database joins.** A SQL query runs against exactly one database connection, so `JOIN` across two connections fails; a dashboard can mix charts from different databases, but each chart is a single-database query. To join across sources you must conform the data into one store (the standard fix), use a federated engine (Trino, Databricks, BigQuery Omni, Starburst) as the single connection, or pre-join upstream in the pipeline.

[Table of Contents](#Superset)

## How do you define a dataset in Superset (physical vs virtual)?

A **physical dataset** points at an existing table or view; a **virtual dataset** is a saved SQL query that Superset treats as a table. Both appear in Explore with columns and metrics.

```sql
-- virtual dataset: the shared query behind several charts
select o.order_date,
       c.country_code,
       c.segment,
       count(distinct o.order_id) as orders,
       sum(o.net_amount)       as net_revenue
from gold.fact_orders_daily o
join gold.dim_customer c on c.customer_sk = o.customer_sk
where o.order_date >= '2024-01-01'
group by 1, 2, 3
```

```python
# create it through the API
dataset = {
    "database": 3,
    "schema": "gold",
    "table_name": "orders_by_country_day",
    "sql": "select ... from gold.fact_orders_daily ...",
    "is_virtual": True,
    "columns": [
        {"column_name": "order_date", "is_dttm": True},
        {"column_name": "country_code", "groupby": True},
        {"column_name": "net_revenue", "type": "DOUBLE"},
    ],
    "metrics": [
        {"metric_name": "net_revenue", "expression": "SUM(net_revenue)"},
    ],
}
```

Guidance: prefer physical datasets over warehouse models, because they are testable and reusable. Use a virtual dataset when a query is genuinely shared by many charts and the warehouse does not allow creating a view (for example a read-only replica or an external table). Keep virtual SQL small - it is re-parsed and re-executed on every chart load, and only dataset-level caching protects it.

[Table of Contents](#Superset)

## How do you use Jinja templating and CTEs in SQL Lab?

SQL Lab, virtual datasets, and SQL-based metrics are rendered with Jinja before execution. The built-in context gives you user and filter information, and you can add your own helpers.

```sql
{% set country = filter_values('country') %}
{% set start = from_dttm or '2024-01-01' %}

with base as (
  select order_date, country_code, sum(net_amount) as net_revenue
  from gold.fact_orders_daily
  where order_date >= '{{ start }}'
    {% if country %}
    and country_code in ({{ "'" + country|join("','") + "'" }})
    {% endif %}
  group by 1, 2
)
select order_date, country_code, net_revenue
from base
order by order_date desc;
```

Useful built-ins:

+ `{{ filter_values('column_name') }}` - current dashboard filter values.
+ `{{ from_dttm }}` / `{{ to_dttm }}` - the selected time range.
+ `{{ current_username() }}`, `{{ current_user_id() }}` - for audit or per-user logic (never as the only security control; use RLS).
+ `{{ url_param('tenant') }}` - read a URL parameter for embedding.
+ `{{ cache_key_wrapper(...) }}` - control cache keys for expensive queries.

Rules: Jinja is rendered server-side, so treat inputs as untrusted - prefer parameterized helpers over string concatenation, and never build the whole query from a raw user parameter. CTEs are fine, but a heavy CTE repeated across charts is better materialized as a view or table.

[Table of Contents](#Superset)

## How do you manage Superset as code with the API and CLI?

Dashboards are metadata objects in a database, so treat them like code: export, review, and import. The CLI and REST API both support this.

```bash
# export a dashboard (plus its charts/datasets) as YAML
superset export-dashboards -f ./export --dashboard_ids 12

# import it into another environment
superset import-dashboards -p ./export/dashboard_export_20261004T120000.zip -u admin

# list and create through the API
curl -H "Authorization: Bearer $TOKEN" \
  "http://superset.internal/api/v1/chart/?q=(filters:!((col:dashboard_title,opr:eq,value:'Exec%20Overview')))"

curl -X POST http://superset.internal/api/v1/dataset/import/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "formData=@dataset_export.zip"

# security/login for a token when you are not using SSO
curl -X POST http://superset.internal/api/v1/security/login \
  -H "Content-Type: application/json" \
  -d '{"username":"ci","password":"'"$SUPERSET_CI_PASSWORD"'","provider":"db","refresh":false}'
```

A workable GitOps loop:

1. Author in dev, add to a `dashboards/` export directory.
2. Commit the YAML/zip; review the diff (dataset ids and SQL changes are visible).
3. CI calls the import API against staging, runs a smoke test (dashboard returns 200, every chart's `/api/v1/chart/{id}/data/` returns rows).
4. Promote the same artifact to prod.

Caveats: exports reference database ids by name, so import maps by name; owners and some permissions are not fully captured; and imports can overwrite by UUID, so always back up the metadata database before a bulk import.

[Table of Contents](#Superset)

## Real world use cases for Superset

### 1. Retail: self-service revenue dashboard over a warehouse star schema

A retailer with 40 stores and an e-commerce site loads `gold.fact_orders_daily`, `gold.dim_product`, and `gold.dim_store` every two hours. 150 business users need revenue, margin, and promotion lift by store, category, and week.

```sql
-- physical dataset: gold.fact_orders_daily
-- metrics defined on the dataset
net_revenue     = SUM(net_amount)
gross_margin    = SUM(net_amount - cost_amount)
promo_orders    = COUNT(DISTINCT CASE WHEN promotion_sk IS NOT NULL THEN order_id END)
```

```python
DATA_CACHE_CONFIG = {"CACHE_TYPE": "RedisCache", "CACHE_DEFAULT_TIMEOUT": 1800}
# cache 30 min; the load is every 2 hours, so most page loads hit cache
```

Why this design: pre-aggregated daily facts keep every chart to a `GROUP BY` on a small table, native filters replace a chart per region, and certified metrics stop finance and merchandising from disagreeing. The trade-off is that "today" is only as fresh as the last load; intraday questions use a separate real-time dataset on ClickHouse.

### 2. Fintech: multi-tenant embedded analytics with row-level security

A payments platform embeds dashboards in its merchant portal. 8,000 merchants each see only their own transactions; one Superset deployment serves all of them through guest tokens.

```python
# guest token request carries the tenant RLS clause
{
  "user": {"username": "merchant_4821", "first_name": "Merchant", "last_name": "4821"},
  "resources": [{"type": "dashboard", "id": "b1a2..."}],
  "rls": [{"clause": "merchant_id = '4821'"}],
  "iat": 1791098400,
  "exp": 1791102000,
}
```

```sql
-- dataset behind the dashboard
select txn_date, merchant_id, sum(amount) as volume, count(*) as txns
from gold.fact_transactions_daily
group by 1, 2
```

Why this design: one codebase and one dashboard template for all merchants, with isolation enforced by the token's RLS clause so a merchant cannot read another's rows. Cache keys include the user context, so cached results are never shared across tenants. The trade-off is token/session management in the host app and the need to test RLS exhaustively, because a bug there is a data breach.

### 3. SaaS: product analytics over ClickHouse for large event volume

A B2B SaaS company stores 5 billion product events in ClickHouse and wants funnels, retention, and feature adoption without waiting on the warehouse.

```sql
-- virtual dataset in Superset (ClickHouse)
select
  toDate(event_time)                          as event_date,
  tenant_id,
  feature_name,
  uniqExact(user_id)                          as active_users,
  countIf(event_name = 'feature_used')        as feature_uses
from analytics.events
where event_time >= now() - interval 90 day
group by 1, 2, 3
```

```python
DATA_CACHE_CONFIG = {"CACHE_TYPE": "RedisCache", "CACHE_DEFAULT_TIMEOUT": 300}
```

Why this design: ClickHouse answers large aggregations in sub-second time, so Superset can query event-level tables without a pre-aggregation layer; a 5-minute cache absorbs dashboard refreshes. The trade-off is a second analytical engine to operate and a virtual dataset that must stay simple - heavy SQL on every chart load is what makes this pattern slow.

### 4. Marketing: scheduled executive report and threshold alerts

A marketing team sends a Monday-morning PDF to leadership and wants a Slack warning when daily spend exceeds plan.

```bash
curl -X POST http://superset.internal/api/v1/report/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name": "Marketing weekly", "type": "Report", "dashboard_id": 7,
    "crontab": "0 6 * * 1", "timezone": "America/New_York",
    "recipients": [{"type": "email", "recipient": "leads@example.com"}]
  }'

curl -X POST http://superset.internal/api/v1/report/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name": "Spend over plan", "type": "Alert", "chart_id": 41,
    "crontab": "0 9 * * *", "sql": "SELECT sum(spend) FROM ({{ sql }}) WHERE sum(spend) > 25000",
    "recipients": [{"type": "slack", "recipient": "#marketing-ops"}]
  }'
```

Why this design: reports and alerts run on Celery with their own schedules, so they do not depend on anyone opening a dashboard, and the alert condition is a SQL predicate over the same certified chart. The trade-off is that screenshot/PDF rendering needs a working headless-browser worker and alerting is threshold-based, not anomaly-based.

### 5. Platform: dashboards-as-code promotion across environments

A central BI team maintains 120 dashboards across dev, staging, and prod, reviewed in Git like application code.

```bash
superset export-dashboards -f ./export --dashboard_ids 7,12,19
git add export/ && git commit -m "adjust revenue filters"
# CI
superset import-dashboards -p ./export/dashboard_export_*.zip -u "$SUPERSET_USER"
curl -sf -H "Authorization: Bearer $TOKEN" \
  http://staging-superset/api/v1/dashboard/12 | jq '.result.dashboard_title'
```

Why this design: exports make chart and dataset changes reviewable, catch accidental metric edits, and let the same artifact move through environments. The trade-off is partial fidelity - owners, permissions, and some features are not fully represented in the export - so promotion is always followed by a smoke test and a metadata-DB backup.

[Table of Contents](#Superset)
