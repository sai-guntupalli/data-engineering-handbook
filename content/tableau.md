## [Main title](../README.md)
### [Interview questions](full.md)

# Tableau

**Notebook:** [`notebooks/topics/tableau.ipynb`](../notebooks/topics/tableau.ipynb) - runnable version of this topic with self-checking exercises.

Tableau is a visual analytics platform: you model a data source, build worksheets by dragging fields onto shelves, and publish governed dashboards with extracts, schedules, and permissions.

+ [How should data be modeled for Tableau dashboards?](#How-should-data-be-modeled-for-Tableau-dashboards)
+ [What is the difference between live connections and extracts in Tableau?](#What-is-the-difference-between-live-connections-and-extracts-in-Tableau)
+ [What is data visualization in Tableau?](#What-is-data-visualization-in-Tableau)
+ [What is the difference between various BI tools and Tableau?](#What-is-the-difference-between-various-BI-tools-and-Tableau)
+ [What are different Tableau products?](#What-are-different-Tableau-products)
+ [What is a parameter in Tableau?](#What-is-a-parameter-in-Tableau)
+ [Tell me something about measures and dimensions?](#Tell-me-something-about-measures-and-dimensions)
+ [What are continuous and discrete field types?](#What-are-continuous-and-discrete-field-types)
+ [What is aggregation and disaggregation of data?](#What-is-aggregation-and-disaggregation-of-data)
+ [What are the different types of joins in Tableau?](#What-are-the-different-types-of-joins-in-Tableau)
+ [Tell me the different connections to make with a dataset?](#Tell-me-the-different-connections-to-make-with-a-dataset)
+ [What are the supported file extensions in Tableau?](#What-are-the-supported-file-extensions-in-Tableau)
+ [What are the supported data types in Tableau?](#What-are-the-supported-data-types-in-Tableau)
+ [What are sets?](#What-are-sets)
+ [What are groups in Tableau?](#What-are-groups-in-Tableau)
+ [What are shelves?](#What-are-shelves)
+ [Tell me something about Data blending in Tableau?](#Tell-me-something-about-Data-blending-in-Tableau)
+ [How do you generally perform load testing in Tableau?](#How-do-you-generally-perform-load-testing-in-Tableau)
+ [Why would someone not use Tableau?](#Why-would-someone-not-use-Tableau)
+ [What is Tableau data engine?](#What-is-Tableau-data-engine)
+ [What are the various types of filters in Tableau?](#What-are-the-various-types-of-filters-in-Tableau)
+ [What are dual axes?](#What-are-dual-axes)
+ [What is the difference between a tree and heat map?](#What-is-the-difference-between-a-tree-and-heat-map)
+ [What are extracts and schedules in Tableau server?](#What-are-extracts-and-schedules-in-Tableau-server)
+ [What are the components in a dashboard?](#What-are-the-components-in-a-dashboard)
+ [What is a TDE file?](#What-is-a-TDE-file)
+ [What is the story in Tableau?](#What-is-the-story-in-Tableau)
+ [What are different Tableau files?](#What-are-different-Tableau-files)
+ [How do you embed views into webpages?](#How-do-you-embed-views-into-webpages)
+ [What is the maximum num of rows Tableau can utilize at one time?](#What-is-the-maximum-num-of-rows-Tableau-can-utilize-at-one-time)
+ [Mention what is the difference between published data sources and embedded data sources in Tableau?](#Mention-what-is-the-difference-between-published-data-sources-and-embedded-data-sources-in-Tableau)
+ [What is the DRIVE Program Methodology?](#What-is-the-DRIVE-Program-Methodology)
+ [How to use groups in a calculated field?](#How-to-use-groups-in-a-calculated-field)
+ [Explain when would you use Joins vs Blending in Tableau?](#Explain-when-would-you-use-Joins-vs-Blending-in-Tableau)
+ [What is Assume referential integrity?](#What-is-Assume-referential-integrity)
+ [What is a Calculated Field and How Will You Create One?](#What-is-a-Calculated-Field-and-How-Will-You-Create-One)
+ [How Can You Display the Top Five and Bottom Five Sales in the Same View?](#How-Can-You-Display-the-Top-Five-and-Bottom-Five-Sales-in-the-Same-View)
+ [What is the Rank Function in Tableau?](#What-is-the-Rank-Function-in-Tableau)
+ [What is the difference between Tableau and other similar tools like QlikView or IBM Cognos?](#What-is-the-difference-between-Tableau-and-other-similar-tools-like-QlikView-or-IBM-Cognos)
+ [Real world use cases for Tableau](#Real-world-use-cases-for-Tableau)

## How should data be modeled for Tableau dashboards?

Tableau performs best when connected to clean, business-ready datasets at the right grain. Use warehouse marts, extracts, or semantic views that already define measures and dimensions clearly. Avoid pushing complex, inconsistent business logic into many separate workbooks.

Example:

```text
fact_sales_daily + dim_product + dim_region -> certified Tableau data source
```

Modeling rules that survive an audit:

+ Publish one certified data source per domain instead of dozens of workbook-level connections.
+ Define the grain explicitly. If `fact_sales` is one row per order line, every measure must be valid at that grain.
+ Keep joins in the warehouse where possible. Relationship-level modeling is easier to govern than ad-hoc joins inside workbooks.
+ Expose conformed dimensions (`dim_date`, `dim_customer`) so date logic and customer logic are identical everywhere.

```sql
-- The kind of mart Tableau should connect to: already conformed at a known grain
CREATE OR REPLACE VIEW analytics.mart_sales_daily AS
SELECT
  d.date_key,
  d.date_day,
  p.category,
  p.subcategory,
  r.region,
  r.country,
  SUM(f.net_revenue)  AS net_revenue,
  SUM(f.quantity)     AS units,
  COUNT(DISTINCT f.order_id) AS orders
FROM analytics.fact_sales f
JOIN analytics.dim_date d     ON d.date_key = f.date_key
JOIN analytics.dim_product p  ON p.product_key = f.product_key
JOIN analytics.dim_region r   ON r.region_key = f.region_key
GROUP BY 1, 2, 3, 4, 5, 6;
```

This improves performance and makes metrics easier to govern. Trade-off: a pre-aggregated mart is fast and consistent but limits drill-through to detail; keep the line-level fact available as a second (`Detail`) data source for analysts who need it, rather than hiding detail behind a slow live join.

[Table of Contents](#Tableau)

## What is the difference between live connections and extracts in Tableau?

A live connection queries the source system at view time, which keeps data fresh but depends on source performance. An extract stores a snapshot optimized for Tableau, improving performance and reducing source load but requiring refresh management.

Example choice:

+ live: operational dashboard needing current data
+ extract: executive dashboard over stable daily aggregates

```text
Decision rule
  freshness need < extract refresh interval?  -> live (or shorten the schedule)
  source cannot tolerate dashboard concurrency? -> extract
  dashboard scans billions of rows? -> extract or pre-aggregate, never live
  row-level security implemented in the warehouse? -> live (so policies apply)
```

The choice depends on freshness needs, source capacity, dashboard speed, and governance.

```bash
# tabcmd: refresh an extract on demand after the nightly warehouse load
tabcmd login -s https://tableau.example.com -t mysite -u svc_tableau -p "$TABLEAU_PASSWORD"
tabcmd refreshextracts --project "Finance" --workbook "Revenue_v3" --datasource "Certified Sales"
tabcmd logout
```

Trade-off: extracts duplicate storage and add a scheduling dependency; live connections push load onto the warehouse and can be throttled by connection limits. A common compromise is a "hot" extract for executive aggregates refreshed hourly and live access for drill-through.

[Table of Contents](#Tableau)

## What is data visualization in Tableau?

Data visualization is a way to represent data that is visually appealing and interactive. With advancements in technology, the number of business intelligence tools has increased which helps users understand data, data sets, data points, charts, graphs, and focus on its impact rather than understanding the tool itself.

Tableau's value is the speed of the visual loop: encode a question as a view, change a field's role or aggregation, and see the answer. A good visualization encodes one measure with position (bar/line), supports comparison with a shared axis, and avoids dual encoding that misleads (for example, encoding the same metric with both color and length).

[Table of Contents](#Tableau)

## What is the difference between various BI tools and Tableau?

The basic difference between the traditional BI tools and Tableau lies in the efficiency and speed.
The architecture of Traditional BI tools has hardware limitations. While Tableau does not have any sort of dependencies
The traditional BI tools work on complex technologies while Tableau uses simple associative search to make it dynamic.
Traditional BI tools do not support multi-thread, in-memory, or multi-core computing while Tableau supports all these features after integrating complex technologies.
Traditional BI tools have a pre-defined data view while Tableau does a predictive analysis for business operations.

A fairer comparison in an interview: legacy tools (Cognos, MicroStrategy) were designed around server-side cubes and governed report bursting, while Tableau was designed around a client-side visual query model. Modern Tableau Server/Cloud has caught up on governance (permissions, extract schedules, data sources), and competitors like Power BI and Looker compete on price, semantic modeling, or embedded analytics rather than on drag-and-drop speed alone.

[Table of Contents](#Tableau)

## What are different Tableau products?

Tableau like other BI tools has a range of products:
Tableau Desktop: Desktop product is used to create optimized queries out from pictures of data. Once the queries are ready, you can perform those queries without the need to code. Tableau desktop encompasses data from various sources into its data engine and creates an interactive dashboard.
Tableau Server: When you have published dashboards using Tableau Desktop, Tableau servers help in sharing them throughout the organization. It is an enterprise-level feature that is installed on a Windows or Linux server.
Tableau Reader: Tableau Reader is a free feature available on Desktop that lets you open and views data visualizations. You can filter or drill down the data but restricts editing any formulas or performing any kind of actions on it. It is also used to extract connection files.
Tableau Online: Tableau online is also a paid feature but doesn't need exclusive installation. It comes with the software and is used to share the published dashboards anywhere and everywhere.
Tableau Public: Tableau public is yet another free feature to view your data visualizations by saving them as worksheets or workbooks on Tableau Server.

Add Tableau Prep (visual data preparation), Tableau Cloud (the SaaS successor to Tableau Online), and the Tableau REST API/Metadata API for automation. In interviews, note the licensing split: Creator (author + publish), Explorer (edit on published sources), and Viewer (consume), because license mix is usually the largest Tableau cost line.

[Table of Contents](#Tableau)

## What is a parameter in Tableau?

The parameter is a variable (numbers, strings, or date) created to replace a constant value in calculations, filters, or reference lines. For example, you create a field that returns true if the sales are greater than 30,000 and false if otherwise. Parameters are used to replace these numbers (30000 in this case) to dynamically set this during calculations. Parameters allow you to dynamically modify values in a calculation. The parameters can accept values in the following options:
All: Simple text field
List: List of possible values to select from
Range: Select values from a specified range

```text
// Parameter: [Revenue Threshold] (integer, default 30000)
// Calculated field: Above Threshold
[Net Revenue] >= [Revenue Threshold]

// Parameters also drive what-if analysis and reference lines.
// A parameter is global to the workbook; a filter is per-worksheet.
```

```text
// Dynamic top-N using a parameter instead of hard-coded 10
// Parameter: [Top N] (integer, default 10)
RANK(SUM([Net Revenue])) <= [Top N]
```

Trade-off: parameters are workbook-scoped and computed client-side, so a parameter-driven filter cannot be pushed down to the warehouse as efficiently as a normal filter. For large extracts, prefer a filter over a parameter where both would work.

[Table of Contents](#Tableau)

## Tell me something about measures and dimensions?

In Tableau, when we connect to a new data source, each field in the data source is either mapped as measures or dimensions. These fields are the columns defined in the data source. Each field is assigned a dataType (integer, string, etc.) and a role (discrete dimension or continuous measure).
Measures contain numeric values that are analyzed by a dimension table. Measures are stored in a table that allows storage of multiple records and contains foreign keys referring uniquely to the associated dimension tables.
While Dimensions contain qualitative values (name, dates, geographical data) to define comprehensive attributes to categorize, segment, and reveal the data details.

In practice: dimensions set the level of detail (the GROUP BY), and measures are aggregated within that level. Numeric fields can be used as dimensions (`Customer ID` should be a dimension, not a summed measure), and text/date fields can drive measures (`COUNTD`). Every measure needs a default aggregation (SUM, AVG, COUNTD, MIN/MAX, or `None` for row-level).

```sql
-- What Tableau sends for SUM(Net Revenue) by Category and Month
SELECT p.category, DATE_TRUNC('month', d.date_day) AS month, SUM(f.net_revenue) AS net_revenue
FROM fact_sales f
JOIN dim_product p ON p.product_key = f.product_key
JOIN dim_date d    ON d.date_key = f.date_key
GROUP BY 1, 2;
```

[Table of Contents](#Tableau)

## What are continuous and discrete field types?

Tableau's specialty lies in displaying data differently either in continuous format or discrete. Both of them are mathematical terms used to define data where continuous means without interruptions and discrete means are individually separate and distinct.
While the blue color indicates discrete behavior, the green color indicates continuous behavior. On one hand, the discrete view defines the headers and can be easily sorted, while continuous defines the axis in a graph view and cannot be sorted.
Discrete View Tableau

Rules of thumb: discrete (blue) fields create headers and partition the view; continuous (green) fields create an axis and interpolate. A date can be either — discrete `MONTH(date)` gives 12 headers, continuous `MONTH(date)` gives a timeline. Switching date from discrete to continuous (or vice versa) is one of the most common "why does my line chart look wrong" questions.

[Table of Contents](#Tableau)

## What is aggregation and disaggregation of data?

Aggregation of data means displaying the measures and dimensions in an aggregated form. The aggregate functions available in the Tableau tool are:
SUM (expression): Adds up all the values used in the expression. Used only for numeric values.
AVG (expression): Calculates the average of all the values used in the expression. Used only for numeric values.
Median (expression): Calculates the median of all the values across all the records used in the expression. Used only for numeric values.
Count (expression): Returns the number of values in the set of expressions. Excludes null values.
Count (distinct): Returns the number of unique values in the set of expressions.
Tableau, in fact, lets you alter the aggregation type for a view.

Disaggregation of data means displaying each and every data field separately.

Disaggregation matters because it changes the query and the number of marks: a disaggregated view returns one row per record (potentially millions of marks) while an aggregated view returns one row per dimension combination. Use `Analysis > Aggregate Measures` to toggle it, and prefer `ATTR()` only when you have proven the values are identical within the group.

```text
// Guard against fan-out double counting in a blended/joined model
// Measure: Net Revenue (correct regardless of join)
SUM([Net Revenue])

// If the grain is multiplied, a naive SUM doubles; use a LOD to fix the grain:
{ FIXED [Order ID] : MIN([Net Revenue]) }
```

[Table of Contents](#Tableau)

## What are the different types of joins in Tableau?

Tableau is pretty similar to SQL. Therefore, the types of joins in Tableau are similar:
Left Outer Join: Extracts all the records from the left table and the matching rows from the right table.
Right Outer Join: Extracts all the records from the right table and the matching rows from the left table.
Full Outer Join: Extracts the records from both the left and right tables. All unmatched rows go with the NULL value.
Inner Join: Extracts the records from both tables.

Tableau also adds a Left Join with "Assume Referential Integrity" optimization (see below), and Relationship-level "logical" joins that are not physical joins at all — Tableau decides at query time whether to join or blend based on the fields used. Distinguish physical joins (Data Source page, one SQL query) from relationships (logical model, per-view join resolution), because the performance and row-count consequences differ sharply.

```text
Physical join in Tableau
  orders (order_id, customer_id, amount)
  JOIN customers ON orders.customer_id = customers.customer_id

Relationship in Tableau
  orders  --- (many_to_one) ---> customers
  // Tableau adds the join to the SQL only if a customer field is used,
  // which avoids fan-out on dashboards that never need customer detail.
```

[Table of Contents](#Tableau)

## Tell me the different connections to make with a dataset?

There are two types of data connections in Tableau:
LIVE: Live connection is a dynamic way to extract real-time data by directly connecting to the data source. Tableau directly creates queries against the database entries and retrieves the query results in a workbook.
EXTRACT: A snapshot of the data, extract the file (.tde or .hyper file) contains data from a relational database. The data is extracted from a static source of data like an Excel Spreadsheet. You can schedule to refresh the snapshots which are done using the Tableau server. This doesn't need any connection with the database.

Modern extracts use the `.hyper` format (TDE is deprecated). Extracts can be full or incremental: an incremental refresh appends new rows using a "refresh if" condition, which is much cheaper than a full rebuild.

```text
Extract refresh options
  Full refresh          -> rebuild the whole snapshot (predictable, expensive)
  Incremental refresh   -> append rows where [Increment Key] > last refresh value
  Refresh from source   -> re-run the source query; then re-apply extract filters

Extract filters
  // Keep only the last 24 months to shrink a 400 GB source to ~40 GB
  [Order Date] >= DATEADD('month', -24, TODAY())
```

[Table of Contents](#Tableau)

## What are the supported file extensions in Tableau?

The supported file extensions used in Tableau Desktop are:
Tableau Workbook (TWB): contains all worksheets, story points, dashboards, etc.
Tableau Data Source (TDS): contains connection information and metadata about your data source
Tableau Data Extract (TDE): contains data that has been extracted from other data sources.
Tableau Packaged Workbook (TWBX): contains a combination of the workbook, connection data, and metadata, and the data itself in the form of TDE.  It can be zipped and shared.
Tableau Packaged Data Source (TDSX): contains a combination of different files.
Tableau Bookmark (TBM): to earmark a specific worksheet.

Also `.hyper` (the current extract format, replacing `.tde`) and `.twbl` (Tableau workbook locale file). `.twb` does not contain extracts, so a `.twb` opened on another machine needs access to the same published data source; `.twbx` and `.tdsx` are self-contained packages and are what you attach to a support ticket.

[Table of Contents](#Tableau)

## What are the supported data types in Tableau?

The following data types are supported in Tableau:

| Data type | Example values |
|---|---|
| Boolean | True / False |
| Date | December 28, 2016 |
| Date & Time | December 28, 2016 06:00:00 PM |
| Geographical | Beijing, Mumbai (role = geographic) |
| String | "EMEA", "Germany" |
| Number (decimal) | 8.00 |
| Number (whole) | 5 |

Tableau also has a NULL type that appears when all values are unknown, and date/time values carry a time zone from the source. Aggregations on strings (`COUNTD`, `MIN`, `MAX`) are valid; arithmetic on strings is not, which is why a numeric-looking string column is a common extract-time fix.

[Table of Contents](#Tableau)

## What are sets?

Sets are custom fields created as a subset of the data in your Tableau desktop. Sets can be computed based on conditions or created manually based on the dimensions of the data source.
For example, A set of customers that earned revenue more than some value. Now, set data may update dynamically based on the conditions applied. Learn More

Sets are powerful because they can be combined with `IN`/`OUT`, used as a filter, and compared in a calculated field. A set with a cross-tab condition creates an in/out split that updates on refresh; a constant set does not. In/out sets also power set actions (click a mark to add it to the set), which is the cleanest way to build "highlight selected customers" dashboards.

```text
// Set: [Top 100 Customers]
// Condition: SUM([Net Revenue]) >= 100000, Top 100 by SUM([Net Revenue])
// Calculated field: [Is Top 100 Customer]
IF [Top 100 Customers] THEN 'Top 100' ELSE 'Long tail' END
```

[Table of Contents](#Tableau)

## What are groups in Tableau?

Groups are created to visualize larger memberships using dimensions. Groups can create their own fields to categorize values in that specific dimension.

Groups are best for ad-hoc bucketing of a dimension (for example, mapping 60 country values into 6 regions). Groups are static metadata: they are not pushed into the warehouse query as a CASE expression, so both the members and the "Other" bucket are visible and reusable across worksheets.

```text
// Group: [Country (Group)] maps
//   Germany, France, Spain -> Europe
//   USA, Canada, Mexico    -> Americas
//   (everything else)      -> Other

// Calculated field on top of the group to sort regions deliberately
IF [Country (Group)] = 'Europe'   THEN 1
ELSEIF [Country (Group)] = 'Americas' THEN 2
ELSE 3 END
```

[Table of Contents](#Tableau)

## What are shelves?

Tableau worksheets contain various named elements like columns, rows, marks, filters, pages, etc. which are called shelves. You can place fields on shelves to create visualizations, increase the level of detail, or add context to it.

+ Rows / Columns: the axes or headers; putting a dimension here changes the grain of the view.
+ Marks: color, size, label, detail, tooltip, path, shape — detail adds a level to the grain without visual encoding.
+ Filters: restrict rows returned by the query (dimension/measure/date/context filters live here).
+ Pages: split the view into a sequence of pages by a discrete field.

Performance note: every field on a shelf (especially on Marks > Detail and Color) adds to the GROUP BY, which increases the number of marks and can turn a fast aggregate into a slow high-cardinality view.

[Table of Contents](#Tableau)

## Tell me something about Data blending in Tableau?

Data blending is viewing and analyzing data from multiple sources in one place. Primary and secondary are two types of data sources that are involved in data blending.

Blending is a client-side left join: the primary source's marks are the anchor, and the secondary source is queried and matched on common linking fields. Because it happens after the primary query, the secondary source must be aggregated to the link level or it will not join.

```text
Primary:   CRM opportunities (opportunity_id, account_id, owner)
Secondary: Marketing spend (account_id, campaign, spend)
Link:      account_id

// Secondary must be aggregated to account_id before it can be blended:
// e.g. SUM([Spend]) by [Account ID], not row-level spend.
```

Rules: blend only when sources cannot be joined in the warehouse; the link field must have the same data type and can involve only one common dimension reliably; and a blended measure is available only at the link grain. If in doubt, land both sources in the warehouse and use a real join — blending is a fallback, not a modeling strategy.

[Table of Contents](#Tableau)

## How do you generally perform load testing in Tableau?

Load testing in Tableau is done to understand the server's capacity with respect to its environment, data, workload, and use. It is preferable to conduct load testing at least 3-4 times in a year because with every new user, upgrade, or content authoring, the usage, data, and workload change.
Tabjolt was created by Tableau to conduct point-and-run load and performance testing specifically for Tableau servers. Tabjolt:
Automates the process of user-specified loads
Eliminates dependency on script development or script maintenance
Scales linearly with an increase in the load by adding more nodes to the cluster

Modern load testing is usually a mix of Tabjolt and the REST API. The table below maps the signal to the action:

| Symptom | Likely cause | Fix |
|---|---|---|
| Slow first render, fast refresh | heavy source query | extract or pre-aggregate |
| All views slow under load | server CPU/memory contention | more nodes, extract-heavy workload |
| Vizql timeouts at peak | too many concurrent live queries | caching, extract schedules, query throttling |
| Extract refresh misses window | source load or too-large extract | incremental refresh, split schedules |

```bash
# Simple concurrency probe against the REST API
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{http_code} %{time_total}\n" \
    -H "X-Tableau-Auth: $TOKEN" \
    "https://tableau.example.com/api/3.19/sites/$SITE/views/$VIEW/image" &
done
wait
```

[Table of Contents](#Tableau)

## Why would someone not use Tableau?

The limitations of using Tableau are:
Not cost-effective: Tableau is not that cost-effective when we compare it well with the other available data visualization tools. In addition to this, it has software upgrades, proper deployment, maintenance, and also training people for using the tool.
Not so secure: When it comes to data, everyone is extra cautious. Tableau focussed on security issues but fails to provide centralized data-level security. It pushes for row-level security and creates an account for every user which makes it more prone to security glitches.
BI capabilities are not enough: Tableau lacks basic BI capabilities like large-scale reporting, building data tables, or creating static layouts. It has limited result-sharing capabilities, email notification configuration is limited to admins, and the vendor doesn't support trigger-based notifications.

The fair version of this answer: Tableau is expensive per seat, its data-level security is implemented through user filters or row-level security in the source (both of which must be maintained), and it is not a scheduling/reporting engine for pixel-perfect operational documents. It is also weak as a semantic layer for programmatic consumers — Looker/dbt-style metrics and an API-first model are better when other applications need the same definitions. When NOT to use it: very high-volume operational reporting with strict formatting, or when the metric definitions must be consumed by services rather than humans.

[Table of Contents](#Tableau)

## What is Tableau data engine?

An analytical database that computes instant query responses, predictive analysis of the server, and integrated data. The data engine is useful when you need to create, refresh, or query extracts. It can be used for cross-database joins as well.

The data engine (Hyper) is a columnar in-memory/on-disk engine that executes against extracts. It is the reason `.hyper` extracts are fast: filters, aggregations, and cross-database joins run inside Hyper rather than round-tripping to the source.

```text
Source A (Oracle)  --\
                      >-- Hyper extract --(in-process query)--> view
Source B (Excel)   --/

When to extract: joins across heterogeneous sources, repeated expensive scans,
                  or a source that cannot serve concurrent interactive queries.
When NOT to:      data must be live, or the extract is larger than the value it adds.
```

[Table of Contents](#Tableau)

## What are the various types of filters in Tableau?

Tableau has 6 different types of filters:
Extract Filter: This filter retrieves a subset of data from the data source.
Dimension Filter: This filter is for non-aggregated data (discrete).
Data Source Filter: This filter refrains users from viewing sensitive information and thus reduces data feeds.
Context Filter: This filter creates datasets by applying presets in Tableau.
Measure Filter: This filter applies various operations like sum, median, avg, etc.
Table Calculation Filter: This filter is applied after the view has been created.

The order of operations is the interview point, because it explains why a filter does not remove a percentage:

```text
Extract filter -> Data source filter -> Context filter -> Dimension filter
   -> Measure filter -> Table calculation filter -> Percent-of-total table calc

// Percent of total computed after a dimension filter reflects the filtered set.
// If you filter out a region, the remaining regions still total 100% only if
// the percent-of-total calc is set to "Table (across)" and computed after the filter.
```

FIXED LOD expressions are computed before dimension filters but after context filters — that ordering is why `{ FIXED ... }` totals can look "wrong" when a dimension filter is applied, and why context filters are used to constrain LODs.

[Table of Contents](#Tableau)

## What are dual axes?

Dual axes are used to analyze two different measures at two different scales in the same graph. This lets you compare multiple attributes on one graph with two independent axes layered one above the other.
To add a measure as a dual-axis, drag the field to the right side of the view and drop it when you see a black dashed line appear. You can also right-click (control-click on Mac) the measure on the Columns or Rows shelf and select Dual Axis.

Distinguish dual axis (two independent scales, can mislead) from combined axis (one shared scale, honest comparison). For revenue and margin, a blended axis (`Measure Values`) on one scale is usually the correct choice; dual axis is for measures whose units genuinely differ (revenue in dollars and conversion rate in percent), and the axes should be labeled.

```text
// Dual axis best practice
Rows: SUM(Revenue)   -- synchronize axis OFF, label "USD"
Rows: SUM(Margin %)  -- synchronize axis OFF, label "%"
Format: label both axes; add a reference line at the target margin.
```

[Table of Contents](#Tableau)

## What is the difference between a tree and heat map?

Both the maps help in analyzing data. While a heat map visualizes and compares different categories of data, a treemap displays a hierarchical structure of data in rectangles. Heat map visualizes measures against dimensions by depicting them in different colors. Similar to a text table with values defined in different colors.
Heatmap In Tableau
Treemap visualizes the hierarchy of data in nested rectangles. Hierarchy levels are displayed from larger rectangles to smaller ones.
Example - Below treemap shows aggregated sales totals across a range of product categories:
TreeMap in Tableau

Practical differences: a heat map needs two dimensions (row/column) and a measure mapped to color, and is read by scanning intersections; a treemap needs a hierarchy and a size measure, and is read by rectangle area. Both degrade quickly above ~20 categories or with a non-sequential color palette, so use a diverging palette only for deviations (variance to target) and a sequential palette for magnitudes.

[Table of Contents](#Tableau)

## What are extracts and schedules in Tableau server?

Data extracts are the subsets of data created from data sources. Schedules are scheduled refreshes made on extracts after publishing the workbook. This keeps the data up-to-date. Schedules are strictly managed by the server administrators.

```text
Schedule design pattern
  06:00  warehouse daily load completes
  06:15  full refresh: small dimension extracts (< 5 min)
  06:30  incremental refresh: large fact extracts (append today's rows)
  07:00  subscription emails + dashboard cache warm
```

Schedules run as the extract owner, so if that user is deactivated the refresh silently fails — always assign refreshes to a service account and monitor refresh failures through the REST API rather than trusting the UI status.

```bash
# Query extract refresh status (REST API), then alert on failures
curl -s -H "X-Tableau-Auth: $TOKEN" \
  "https://tableau.example.com/api/3.19/sites/$SITE/tasks/extractRefreshes" \
  | python -c "import sys,json; [print(t['id'], t.get('schedule',{}).get('frequency'), t.get('lastRunAt')) for t in json.load(sys.stdin)['extractRefreshes']['extractRefresh']]"
```

[Table of Contents](#Tableau)

## What are the components in a dashboard?

The components displayed in a dashboard are:
Horizontal: Horizontal view allows the users to combine the worksheets and dashboard elements from left to right and edit the height of the elements.
Vertical: Vertical view allows the users to combine the worksheets and dashboard elements from top to bottom and edit the width of the elements.
Text: All the textual fields.
Image Extract: To extract an image Tableau applies some code, extracts the image, and saves it in a workbook in the XML format.
Web URL: Hyperlink that points to a web page, file, or other web resources outside of Tableau

Modern dashboards add layout containers (horizontal/vertical nesting), floating objects, device layouts (desktop/tablet/phone), dashboard actions (filter, highlight, URL, parameter, set, go-to-sheet), and dynamic zone visibility driven by a parameter. Layout containers are the difference between a dashboard that resizes gracefully and one that breaks on a laptop.

[Table of Contents](#Tableau)

## What is a TDE file?

TDE stands for Tableau Data Extract and uses the `.tde` extension. A TDE file points to a file that contains data from external sources like MS Excel, MS Access, or CSV files. TDE makes it easier to analyze and discover data.

TDE was replaced by the `.hyper` format; Tableau still opens `.tde` but converts it. For automation, use the Hyper API to write extracts directly without Tableau Desktop:

```python
# Write a Hyper extract with the Hyper API (runs in a pipeline, no Desktop needed)
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, TableDefinition

table = TableDefinition("Extract", [
    TableDefinition.Column("order_id", "text"),
    TableDefinition.Column("order_date", "date"),
    TableDefinition.Column("revenue", "double precision"),
])

with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(hyper.endpoint, "orders.hyper", CreateMode.CREATE_AND_REPLACE) as conn:
        conn.catalog.create_schema("Extract")
        conn.catalog.create_table(table)
        conn.execute_command(
            "COPY \"Extract\".\"Extract\" FROM 'orders.csv' WITH (format csv, header true)"
        )
```

[Table of Contents](#Tableau)

## What is the story in Tableau?

Creating a story is effective in Tableau which is created by combining various charts to portray a plot of viewers. A story is a sheet that contains all the methods used to create those worksheets. To create a story:
Click the New Story on the dashboard.
Choose the right size of the story from the bottom-left corner or choose a custom size.
Start building the story by double-clicking the sheet and add it to the story point.
Add a caption to the story by clicking Add a caption.
You can update the highlights by clicking Update in the toolbar. You can also add layout options, format a story, or fit the story to your dashboard.

A story is a sequence of captured worksheet states with captions — useful for a narrative walkthrough (monthly business review), but every story point freezes the filters and selections of that moment, so it must be re-captured when the underlying data or a view changes. For recurring reviews, a parameter-driven dashboard is usually more maintainable than a hand-maintained story.

[Table of Contents](#Tableau)

## What are different Tableau files?

Workbooks: Workbooks contain one or more worksheets and dashboard elements.
Bookmarks: Contains a single worksheet that is easier to share.
Packaged Workbooks: Contains a workbook along with supporting local file data and background images.
Data Extraction Files: Extract files that contain a subset of data.
Data Connection Files: Small XML file with various connection information.

| File | Contains | Portable? | Typical use |
|---|---|---|---|
| `.twb` | worksheets, dashboards, XML | no data | version control in Git |
| `.twbx` | workbook + extracts + assets | yes | sharing a self-contained analysis |
| `.tds` | data source connection + metadata | no data | publish a shared data source |
| `.tdsx` | data source + extract | yes | share a source with an extract |
| `.hyper` | extract data | yes | scheduled extract, Hyper API |
| `.tbm` | single worksheet bookmark | no data | quickly reopen one view |

For version control, store `.twb`/`.tds` as XML in Git (never `.twbx`) so diffs are reviewable, and publish through a CI job rather than by hand.

[Table of Contents](#Tableau)

## How do you embed views into webpages?

You can easily integrate interactive views from your Tableau Server or Tableau online onto webpages, blogs, web applications, or internet portals. But to have a look at the views, the permissions demand the viewer to create an account on the Tableau Server. To embed views, click the Share button on the top of the view and copy the embed code to paste it on the web page.
You can also customize the embedded code or Tableau Javascript APIs to embed views.

For a public/anonymous embed, enable "Let people access this view without signing in" (and ensure the data is not sensitive). For a logged-in embed, use connected apps or trusted authentication so the user does not see a Tableau login page.

```text
Embed URL shape
https://tableau.example.com/views/Finance/Revenue?:showVizHome=no&:embed=y&:toolbar=no
&:tabs=no&:refresh=yes
```

```python
# Trusted authentication: the web app asks Tableau Server for a one-time ticket
import requests

resp = requests.post(
    "https://tableau.example.com/trusted",
    data={"username": "viewer@acme.com", "client_ip": "10.0.0.5", "target_site": "finance"},
    timeout=10,
)
ticket = resp.text
url = f"https://tableau.example.com/trusted/{ticket}/views/Finance/Revenue?:embed=y"
```

Security note: embedding with a hard-coded user or a shared service account defeats row-level security. Always pass the real user identity through trusted auth/connected apps and let the warehouse or user filter enforce access.

[Table of Contents](#Tableau)

## What is the maximum num of rows Tableau can utilize at one time?

The maximum number of rows or columns is indefinite because even though Tableau contains petabytes of data, it intelligently uses only those rows and columns which you need to extract for your purpose.

The real limits are practical: Hyper extract size is bounded by disk and by memory for query execution, marks are slower above ~100k, and cross-database joins run in the data engine. Tableau pushes aggregation to the source when possible, so the honest answer is "the limit is the number of marks and the source query, not a row count."

| Layer | Practical ceiling | Mitigation |
|---|---|---|
| Marks rendered | ~100k before interactivity suffers | aggregate, use density/heatmap |
| Extract size | tens to hundreds of GB | extract filters, partition, incremental refresh |
| Live query rows | source-dependent | pre-aggregate mart, materialized view |
| Columns in a view | dozens | hide unused fields, use folders |

[Table of Contents](#Tableau)

## Mention what is the difference between published data sources and embedded data sources in Tableau?

Connection information is the details of data that you want to bring into Tableau. Before publishing it, you can create an extract of the same.
Published Data Source: It contains connection information that is independent of any workbook.
Embedded Data Source: It contains connection information which is connected to a workbook

Published sources are the governance mechanism: credentials are stored once, extract schedules run centrally, and a change to the source propagates to every dependent workbook. Embedded sources are convenient for ad-hoc work but mean every workbook owns its own connection and credentials rotation.

```bash
# Publish a data source over the REST API (initiate -> upload -> commit)
curl -s -X POST -H "X-Tableau-Auth: $TOKEN" -H "Content-Type: application/json" \
  -d '{"datasource":{"name":"Certified Sales","project":{"id":"'"$PROJECT_ID"'"}}}' \
  "https://tableau.example.com/api/3.19/sites/$SITE/datasources"
```

[Table of Contents](#Tableau)

## What is the DRIVE Program Methodology?

DRIVE program methodology creates a structure around data analytics derived from enterprise deployments. The drive methodology is iterative in nature and includes agile methods that are faster and effective.

DRIVE is Tableau's deployment methodology (Define, Refine, Implement, Validate, Expand). In interviews, connect it to a real rollout: define the success metric and audience first, refine the data model and pilot with a small group, implement governance (certified sources, permissions, extracts), validate adoption with usage telemetry, then expand domain by domain. The failure mode it prevents is a large launch with no adoption measurement.

[Table of Contents](#Tableau)

## How to use groups in a calculated field?

Add the GroupBy clause to SQL queries or create a calculated field in the data window to group fields.
Using groups in a calculation. You cannot reference ad-hoc groups in a calculation.
Blend data using groups created in the secondary data source: Only calculated groups can be used in data blending if the group was created in the secondary data source.
Use a group in another workbook. You can easily replicate a group in another workbook by copy and pasting a calculation.

A group created in the Data pane can be referenced by name in a calculation; an ad-hoc group created by selecting marks cannot. If you need the grouping logic in SQL, replicate it as a CASE expression so the warehouse and Tableau agree.

```sql
-- Warehouse-side equivalent of a Tableau group
SELECT
  CASE
    WHEN country IN ('Germany', 'France', 'Spain') THEN 'Europe'
    WHEN country IN ('USA', 'Canada', 'Mexico')   THEN 'Americas'
    ELSE 'Other'
  END AS region_group,
  SUM(net_revenue) AS net_revenue
FROM analytics.mart_sales_daily
GROUP BY 1;
```

[Table of Contents](#Tableau)

## Explain when would you use Joins vs Blending in Tableau?

While the two terms may sound similar, there is a difference in their meaning and use in Tableau:
While Join is used to combine two or more tables within the same data source.
Blending is used to combine data from multiple data sources such as Oracle, Excel, SQL server, etc.

```text
Use a JOIN when:
  - both tables are in the same database
  - you need row-level detail from both sides
  - you want the work pushed down to the warehouse

Use BLENDING when:
  - the sources are genuinely different systems you cannot land together
  - the secondary source can be aggregated to the link grain
  - you accept a client-side left join and its performance cost

Use NEITHER when:
  - the join would multiply rows (fan-out). Land a bridge/aggregate table instead.
```

Fan-out example: joining `orders` to `order_items` and then summing `orders.amount` double-counts the order for every item. The fix is to aggregate one side first or to use a FIXED LOD, not to blend.

[Table of Contents](#Tableau)

## What is Assume referential integrity?

In some cases, you can improve query performance by selecting the option to Assume Referential Integrity from the Data menu. When you use this option, Tableau will include the joined table in the query only if it is specifically referenced by fields in the view.

Conditions: the join must be a left/right (not full outer) join, the join key on the "one" side must be unique or a primary key, and the join must be defined at the data source level. If the assumption is wrong — for example a fact row references a missing dimension row — rows silently disappear from the result, which is a correctness bug disguised as a performance win.

```sql
-- With Assume Referential Integrity, Tableau may generate this instead of a join:
SELECT SUM(amount) FROM fact_sales;                -- dimension not referenced
-- Without it, the engine must join to dim_product to prove the join is safe.
```

Use it deliberately for proven foreign keys, and add a warehouse-level not-null/foreign-key test to keep the assumption true.

[Table of Contents](#Tableau)

## What is a Calculated Field and How Will You Create One?

Calculated fields are created using formulas based on other fields. These fields do not exist but are created by you.
You can create these fields to:
Segment data
Convert the data type of a field, such as converting a string to a date.
Aggregate data
Filter results
Calculate ratios

There are three main types of calculations that you can create:
Basic Calculations: Transform values of the data fields at the source level
Level of Detail (LOD) Expressions: Transform values of the data fields at the source level like basic calculations but with more granular access
Table Calculations: Transform values of the data fields only at the visualization level
To create calculate fields:
In Tableau, navigate to Analysis>Create a calculated field. Input details in the calculation editor.
And, done!

Worked examples of each type:

```text
// Basic calculation (row-level, then aggregated by the view)
[Net Revenue] - [Cost]

// Ratio that must not be summed across rows
SUM([Net Revenue]) / SUM([Cost])

// FIXED LOD: revenue per customer, independent of the view's dimensions
{ FIXED [Customer ID] : SUM([Net Revenue]) }

// INCLUDE LOD: average order value at the customer level while keeping region
AVG({ INCLUDE [Customer ID] : SUM([Net Revenue]) })

// EXCLUDE LOD: percent of region total regardless of the product in the view
SUM([Net Revenue]) / SUM({ EXCLUDE [Product] : SUM([Net Revenue]) })

// Table calculation: running total across the view
RUNNING_SUM(SUM([Net Revenue]))

// Table calculation: percent difference from previous month
(SUM([Net Revenue]) - LOOKUP(SUM([Net Revenue]), -1)) / LOOKUP(SUM([Net Revenue]), -1)
```

Order of operations in one line: basic calculations at the data-source grain, LODs at the declared grain (after context filters), table calculations last, at the partition and addressing you choose. Trade-off: LODs run in the query and are expensive on large extracts; table calculations are cheap but only valid in the view they were built for and cannot be used as a dimension filter before computation.

[Table of Contents](#Tableau)

## How Can You Display the Top Five and Bottom Five Sales in the Same View?

You can see top five and bottom five sales with the help of these functions:
Drag customer name to row and sales to the column.
Sort Sum(sales) in descending order.
Create a calculated field Rank of Sales.

```text
// Rank of Sales (table calculation, compute using Customer Name)
RANK_DENSE(SUM([Net Revenue]))

// Top 5 and Bottom 5 in one view:
// 1. Create [Rank of Sales] with RANK_DENSE(SUM([Net Revenue]))
// 2. Create a set or filter: [Rank of Sales] <= 5 OR [Rank of Sales] > TOTAL_COUNT - 5
// 3. Better: two parameters for N, and a set based on rank
[Rank of Sales] <= [Top N] OR [Rank of Sales] > SIZE() - [Bottom N]
```

```text
// Cleaner: sort-independent top/bottom using RANK on both directions
Top:    RANK(SUM([Net Revenue]))
Bottom: RANK(SUM(-[Net Revenue]))
```

Trade-off: a rank table calculation depends on the view's addressing (here, Customer Name), so adding another dimension changes the ranking. If the ranking is a business definition (top 5 customers by revenue this quarter), compute it in SQL at the correct grain so every workbook agrees.

```sql
-- Warehouse-side top/bottom, deterministic and reusable
WITH ranked AS (
  SELECT customer_id, SUM(net_revenue) AS revenue,
         RANK() OVER (ORDER BY SUM(net_revenue) DESC) AS rnk_desc,
         RANK() OVER (ORDER BY SUM(net_revenue) ASC)  AS rnk_asc
  FROM analytics.mart_sales_daily
  WHERE date_day >= DATE '2026-07-01'
  GROUP BY customer_id
)
SELECT 'top' AS bucket, * FROM ranked WHERE rnk_desc <= 5
UNION ALL
SELECT 'bottom', * FROM ranked WHERE rnk_asc <= 5;
```

[Table of Contents](#Tableau)

## What is the Rank Function in Tableau?

Rank function is used to give positions (rank) to any measure in the data set. Tableau can rank measure in the following ways:
Rank: The rank function in Tableau accepts two arguments: aggregated measure and ranking order (optional) with a default value of desc.
Rank_dense: The rank_dense also accepts the two arguments: aggregated measure and ranking order. This assigns the same rank to the same values but doesn't stop there and keeps incrementing with the other values. For instance, if you have values 10, 20, 20, 30, then ranks will be 1, 2, 2, 3.
Rank_modified: The rank_modified assigns the same rank to similar values.
Rank_unique: The rank_unique assigns a unique rank to each and every value. For example, If the values are 10, 20, 20, 30 then the assigned ranks will be 1,2,3,4 respectively.

| Values | RANK | RANK_DENSE | RANK_MODIFIED | RANK_UNIQUE |
|---|---|---|---|---|
| 30 | 1 | 1 | 1 | 1 |
| 20 | 2 | 2 | 2 | 2 |
| 20 | 2 | 2 | 2 | 3 |
| 10 | 4 | 3 | 4 | 4 |

Rank functions are table calculations, not aggregations: they compute in the view and honor the addressing/partitioning you set. `RANK_DENSE` is the one to use for "top N categories" because ties do not consume a position, and `RANK` is the SQL-standard behavior with gaps after ties.

[Table of Contents](#Tableau)

## What is the difference between Tableau and other similar tools like QlikView or IBM Cognos?

Tableau is different than QlikView or IBM Cognos for various reasons:
Tableau is an intuitive data visualization tool simplifying the story creation by simple drag and drop techniques. On the other hand, BI tools like QlikView or Cognos convert data into metadata to let the users explore data relations. If your presentation runs around presenting data in aesthetic visualizations then opt for Tableau. If not, and might need a full BI platform then go for Cognos/QlikView
The ease of use or extracting data details is easier in Tableau than compared to extensive BI tools like Cognos. With Tableau, your team members, be it a guy from sales can easily read the data and give insights. But with Cognos, only members with extensive tool knowledge are appreciated and welcomed.

A more current framing: Qlik uses an in-memory associative engine with a different governance model, Power BI competes on price and Microsoft integration, and Looker competes on a code-defined semantic layer (LookML) with embedded analytics. The decision criteria are semantic-layer reuse, embedding, cost per user, and whether metric definitions must be consumed by applications — not just chart aesthetics.

[Table of Contents](#Tableau)

## Real world use cases for Tableau

### 1. Retail category management on a certified extract

Business context: a grocery retailer's category managers review sales, margin, and stock cover every Monday across 1,200 stores and 90,000 SKUs; the warehouse holds 4 years of line-item history (~2.1B rows, 380 GB). Managers need sub-5-second filtering.

```text
warehouse star schema (fact_sales + dims)
   -> nightly dbt mart mart_sales_daily (~250M rows)
   -> Tableau published data source "Certified Sales" (Hyper extract, 22 GB)
   -> parameter-driven dashboard: category, region, week, top-N
```

```text
// Dashboard parameter: [Week Offset] (integer, default 0)
// Calculated date: TODAY() - [Week Offset] * 7

// LOD for store-level stock cover, independent of the SKU in the view
{ FIXED [Store ID] : SUM([Stock On Hand]) } / NULLIF(SUM([Avg Daily Units]), 0)

// Extract filter: keep the extract to a manageable size
[Date] >= DATEADD('year', -2, TODAY())
```

Why this design: the extract is refreshed nightly after a 19:00 warehouse load, which matches the Monday review cadence while avoiding a live query against a busy warehouse; the certified published source means every manager sees the same margin definition, and the extract filter caps growth at two years so dashboard latency stays stable.

### 2. Fintech regulatory reporting with row-level security

Business context: a payments company must give regional compliance teams scoped access to transaction reporting (EU, UK, US) while auditors see everything. Data is 180M transactions/month with strict access requirements.

```text
regulated warehouse tables (transaction_fact, dim_region)
   -> live connection (no extract, so warehouse RLS applies at query time)
   -> Tableau user filters on [Region] = USERNAME()/USERATTRIBUTE('region')
   -> subscriptions to compliance teams with PDF snapshots archived
```

```sql
-- Warehouse-side row-level security is the source of truth
CREATE OR REPLACE ROW ACCESS POLICY rap_region
ON analytics.transaction_fact
GRANT TO ('role:compliance_reader')
FILTER USING (region = CURRENT_ROLE());
```

```text
// Tableau user filter (defense in depth, for extract-based sources)
[Region] = USERATTRIBUTE('region')
// USERATTRIBUTE requires the site to be configured with the attribute;
// auditors get 'ALL' and the calculation short-circuits:
USERATTRIBUTE('region') = 'ALL' OR [Region] = USERATTRIBUTE('region')
```

Why this design: compliance data should not be copied into a movable extract, so the connection stays live and the warehouse enforces access; the Tableau user filter is a second layer for any extract and prevents an accidental cross-region leak if a source is republished.

### 3. Marketing spend efficiency across channels

Business context: a D2C brand spends $1.8M/month across six ad platforms and wants CAC and ROAS by channel and campaign, updated daily by 08:00. Volume: 90M impressions/day, 14M sessions/day, 220K orders/day, six API feeds landed in the warehouse.

```text
ad platform APIs -> warehouse staging -> mart_channel_daily (spend, clicks, orders, revenue)
   -> Tableau dashboard: CAC = spend / new_customers, ROAS = revenue / spend
   -> parameter [Date Range] + filter action from channel to campaign detail
```

```text
// CAC with an LOD so it is correct at every level of the view
SUM([Spend]) / NULLIF(COUNTD([New Customer ID]), 0)

// ROAS
SUM([Attributed Revenue]) / NULLIF(SUM([Spend]), 0)

// Blended vs paid: a fixed ratio that must not be recomputed per campaign
SUM({ FIXED : [Spend] }) / NULLIF(SUM({ FIXED : [Attributed Revenue] }), 0)
```

Why this design: spend and revenue live in one warehouse mart with a shared date and channel key, so CAC is a true ratio rather than a ratio of averages; the parameterized date range lets media buyers compare 7/28/90-day windows without six separate workbooks.

### 4. SaaS product adoption for customer success

Business context: a B2B SaaS company's CSMs need account-level usage, seat utilization, and risk flags, with each CSM seeing only their book of business. Volume: 340 enterprise accounts, 900M product events/month, refreshed hourly.

```text
product events -> warehouse -> mart_account_usage_hourly
   -> live connection with Tableau user filter on [CSM Email] = USERNAME()
   -> account scorecard + risk heatmap + drill-through to feature usage
```

```text
// Seat utilization LOD: independent of the feature rows in the view
{ FIXED [Account ID] : SUM([Active Seats]) } / NULLIF({ FIXED [Account ID] : MAX([Licensed Seats]) }, 0)

// Risk flag combining three signals in one calculated field
IF { FIXED [Account ID] : SUM([Active Seats]) } / NULLIF(MAX([Licensed Seats]), 0) < 0.6
   AND { FIXED [Account ID] : MAX([Days Since Login]) } > 21
   AND { FIXED [Account ID] : SUM([Usage Trend 30d]) } < 0
THEN 'At risk' ELSE 'Healthy' END
```

Why this design: the CSM user filter keeps each rep scoped without duplicating dashboards per region, and FIXED LODs compute account-level ratios that stay correct whether the CSM is looking at accounts, features, or weeks.

### 5. Operations monitoring for a logistics network

Business context: a 3PL monitors on-time delivery across 60 hubs; dispatch needs a live view during peak, and planning needs a trend view. Volume: 1.4M shipments/day, 40M scan events/day.

```text
scanner events -> Kafka -> warehouse micro-batch (5 min) -> mart_shipment_status
   -> live connection dashboard (on-time %, delays, hub backlog)
   -> hyper extract for the 12-month trend workbook (refreshed daily 03:00)
```

```text
// On-time % as a ratio of sums, not an average of averages
SUM([On Time Shipments]) / NULLIF(SUM([Total Shipments]), 0)

// Hub backlog alert: colour the heat map when active shipments exceed capacity
IF SUM([Active Shipments]) > MAX([Hub Daily Capacity]) THEN 'Over capacity' ELSE 'Normal' END
```

Why this design: the operational dashboard uses a live connection so a 5-minute-old micro-batch is visible immediately, while the heavy 12-month trend uses an extract so it does not compete with dispatch queries; splitting the two workloads by connection type keeps both fast without extra server capacity.

[Table of Contents](#Tableau)
