import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# DataFrames 1: pandas essentials and traps

A support team exports tickets as CSV every morning and wants a weekly summary per customer. The data is a few
hundred thousand rows: far too small for Spark, a little awkward for SQL alone, and exactly what pandas is used for
every day. pandas is also where many silent data bugs start: a column read with the wrong type, a join that
duplicated rows, an assignment that changed nothing.

This lesson covers what a data engineer needs from pandas 3: reading with explicit types, the new string and nullable
types, selecting and assigning safely under copy-on-write, missing values, joins that check their own cardinality,
group-by aggregation, dates and time zones, vectorized code instead of row loops, and memory.

*Last reviewed: November 2026, against pandas 3.0.*

**Prerequisites:** [Python 2: collections](../python/learning/python-02-collections.ipynb) and
[SQL 5: aggregations and CTEs](../sql/sql-05-aggregations-and-ctes.ipynb).
%% code
# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
!pip install -q pandas~=3.0.0 pyarrow numpy
%% md
## Setup and sample data

The cell writes the morning's export as CSV text: one row per ticket, with an id, a customer, a priority, an
opening timestamp in UTC, minutes to first response, and a satisfaction score that is often missing. A second small
table maps customers to their account manager.
%% code
import io

import numpy as np
import pandas as pd

tickets_csv = """ticket_id,customer,priority,opened_at,response_min,score
T001,acme,high,2026-03-02T08:15:00Z,12,5
T002,bright,low,2026-03-02T09:40:00Z,95,
T003,acme,medium,2026-03-03T23:50:00Z,30,4
T004,cyan,high,2026-03-04T14:05:00Z,,3
T005,bright,high,2026-03-05T10:00:00Z,8,5
T006,acme,low,2026-03-07T16:30:00Z,240,2
T007,delta,medium,2026-03-08T07:45:00Z,45,
"""
managers = pd.DataFrame({"customer": ["acme", "bright", "cyan", "cyan"], "manager": ["Ola", "Ines", "Raj", "Mei"]})
print(pd.__version__)
%% md
## Read with explicit types

`read_csv` guesses each column's type from the data. Guesses go wrong in predictable ways: an id with leading zeros
becomes a number, a column with one missing value becomes `float64`, timestamps stay text. For a pipeline, declare
the types (`dtype=`, `parse_dates=`) so the result does not depend on what today's file happens to contain.

pandas 3 reads text columns as the `str` dtype (backed by Arrow when PyArrow is installed) instead of the old
generic `object` dtype, and offers nullable types such as `Int64` (capital I) that hold integers and missing values
together.

**Where it matters**
- Every file you load more than once: today's file and tomorrow's must produce the same schema.

**Watch out for**
- An integer column with a single missing value silently becoming floats (`12` becomes `12.0`).
%% md
### Compare guessed and declared types

Read the same text twice: once letting pandas guess, once with declared types.
%% code
guessed = pd.read_csv(io.StringIO(tickets_csv))
declared = pd.read_csv(
    io.StringIO(tickets_csv),
    dtype={"ticket_id": "str", "customer": "str", "priority": "category", "response_min": "Int64", "score": "Int64"},
    parse_dates=["opened_at"],
)
print(pd.DataFrame({"guessed": guessed.dtypes.astype(str), "declared": declared.dtypes.astype(str)}))
print(guessed["response_min"].head(4).tolist(), "vs", declared["response_min"].head(4).tolist())
%% md
**What to notice:** Guessed, `response_min` and `score` became `float64` because they contain missing values, and
`opened_at` stayed a string. Declared, they are nullable `Int64` (whole numbers with `<NA>`), `priority` is a
`category`, and `opened_at` is a UTC timestamp, so date arithmetic works.
%% md
## Select and assign under copy-on-write

Since pandas 3, **copy-on-write** is always on: any DataFrame or Series you get from another one behaves as a copy.
Changing a filtered subset never changes the original, and the old *chained assignment* `df["col"][row] = value`
never works. To change values in place, use one `.loc[rows, columns] = value` call on the DataFrame itself.

**Where it matters**
- Data cleaning code that fixes values for some rows.

**Watch out for**
- Code written for pandas 1 or 2 that relied on chained assignment: under pandas 3 it silently changes nothing (with a
  warning).
%% md
### Fix a value three ways

Try to set ticket T004's missing response time to 60 minutes through a filtered subset, through chained assignment,
and with `.loc`.
%% code
import warnings

df = declared.copy()
subset = df[df["ticket_id"] == "T004"]
subset.loc[:, "response_min"] = 60
print("after changing a subset:", df.loc[df["ticket_id"] == "T004", "response_min"].item())

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    df["response_min"][df["ticket_id"] == "T004"] = 60
print("after chained assignment:", df.loc[df["ticket_id"] == "T004", "response_min"].item(), "| warning:", caught[0].category.__name__)

df.loc[df["ticket_id"] == "T004", "response_min"] = 60
print("after .loc:", df.loc[df["ticket_id"] == "T004", "response_min"].item())
%% md
**What to notice:** Changing the subset left `df` untouched, and chained assignment also changed nothing, with a
`ChainedAssignmentError` warning. Only the single `.loc` call on `df` set the value to 60. Under copy-on-write that is
the one way to update in place.
%% md
## Handle missing values deliberately

pandas marks missing values as `NaN` (floats), `NaT` (timestamps) or `pd.NA` (nullable types). Aggregations skip
them, like SQL: `mean` averages only known values and `count` counts non-missing ones. `fillna`, `dropna` and
`isna` make the decision explicit.

**Where it matters**
- Averages and rates, where skipping and filling give different answers.

**Watch out for**
- `fillna(0)` on a satisfaction score: a missing answer is not a zero rating.
%% md
### Count, average and fill missing scores

Summarise the score column, then compare the average with missing scores skipped and filled with 0.
%% code
scores = declared["score"]
print("rows:", len(scores), "| known:", scores.count(), "| missing:", scores.isna().sum())
print("mean skipping missing:", scores.mean())
print("mean with missing as 0:", round(scores.fillna(0).mean(), 2))
print("tickets without a score:", declared.loc[scores.isna(), "ticket_id"].tolist())
%% md
**What to notice:** 2 of 7 tickets have no score. The mean of the 5 known scores is 3.8; filling the gaps with 0
drags it to 2.71. Same data, different metric; which one is right depends on what "average satisfaction" means.
%% md
## Join with a cardinality check

`merge` is pandas' join. Its most useful argument is `validate`: `"many_to_one"` raises an error if the right side
has duplicate keys, catching the fan-out that silently multiplies rows. `indicator=True` adds a column saying
whether each row matched, which is how you find orphans.

**Where it matters**
- Every enrichment join from a fact-like table to a lookup.

**Watch out for**
- A lookup that "should" be unique but is not: customer `cyan` has two managers here.
%% md
### Join tickets to managers, then check it

Join without a check, then with `validate="many_to_one"`, then deduplicate and use `indicator` to find unmatched tickets.
%% code
naive = declared.merge(managers, on="customer", how="left")
print("tickets:", len(declared), "| rows after naive join:", len(naive))

try:
    declared.merge(managers, on="customer", how="left", validate="many_to_one")
except pd.errors.MergeError as error:
    print("validate refused:", str(error)[:70])

one_manager = managers.drop_duplicates("customer", keep="first")
checked = declared.merge(one_manager, on="customer", how="left", validate="many_to_one", indicator=True)
print(checked["_merge"].value_counts().to_dict())
print("no manager:", checked.loc[checked["_merge"] == "left_only", ["ticket_id", "customer"]].values.tolist())
%% md
**What to notice:** The naive join turned 7 tickets into 8 rows, because `cyan` has two managers. `validate` refused
the join outright. After keeping one manager per customer the join keeps 7 rows; `indicator` shows that ticket T007
(customer `delta`) has no manager.
%% md
## Group and aggregate

`groupby(...).agg(...)` is SQL's `GROUP BY`. Named aggregations (`new_column=("source", "function")`) keep the output
readable. `observed=True` limits categorical groupings to categories that occur, and `as_index=False` returns
the keys as ordinary columns.

**Where it matters**
- Daily and weekly summaries, the most common pandas job in data engineering.

**Watch out for**
- `groupby` drops rows whose key is missing unless you pass `dropna=False`.
%% md
### Summarise tickets per customer

Count tickets, take the median response time and the average score per customer.
%% code
summary = (
    declared.groupby("customer", as_index=False)
    .agg(tickets=("ticket_id", "count"), median_response=("response_min", "median"), avg_score=("score", "mean"))
    .sort_values("tickets", ascending=False)
)
print(summary.to_string(index=False))
print(declared.groupby("priority", observed=True)["ticket_id"].count().to_dict())
%% md
**What to notice:** Acme has 3 tickets with a median first response of 30 minutes. Delta's average score is `<NA>`
because its only ticket has no score, and Cyan's median response is `<NA>` for the same reason: aggregates skip
missing values, and an all-missing group gives no value at all.
%% md
## Work with dates and time zones

Parsed timestamps support vectorized arithmetic and the `.dt` accessor. Keep them time-zone aware in UTC, convert
to a local zone only to answer local questions such as "which business day", and bucket with `dt.floor` or
`resample`.

**Where it matters**
- Daily reports for a business that is not in UTC.

**Watch out for**
- Bucketing UTC timestamps by date when the business day is local: late-evening events move to the next day.
%% md
### Count tickets by UTC day and by Oslo day

Ticket T003 was opened at 23:50 UTC on March 3. Count tickets per day in both zones.
%% code
opened = declared.set_index("opened_at")["ticket_id"]
utc_days = opened.groupby(opened.index.date).count()
oslo = opened.tz_convert("Europe/Oslo")
oslo_days = oslo.groupby(oslo.index.date).count()
print(pd.DataFrame({"utc": utc_days, "oslo": oslo_days}).fillna(0).astype(int))
print("T003 in Oslo:", oslo[oslo == "T003"].index[0])
%% md
**What to notice:** In UTC, March 3 has one ticket; in Oslo time (UTC+1 in March) T003 was opened at 00:50 on March 4,
so March 3 has none and March 4 has two. The same data gives different daily counts depending on the time zone
you bucket in.
%% md
## Vectorize instead of looping

pandas is fast when an operation runs on whole columns in compiled code. `apply` with a Python function and `iterrows`
run Python once per row and are often hundreds of times slower. Most row logic has a vectorized form: arithmetic on
columns, `np.where` or `np.select` for conditions, `.str` and `.dt` methods for text and dates.

**Where it matters**
- Any transformation on more than a few thousand rows.

**Watch out for**
- `apply(axis=1)` hiding in a pipeline: it is the usual cause of a "pandas is slow" complaint.
%% md
### Classify 200,000 tickets two ways

Label each ticket `urgent` when it is high priority and took more than 15 minutes, `late` when any ticket took more
than 60 minutes, and `ok` otherwise: once with a row-wise `apply(axis=1)`, once with `np.select`. Time both.
%% code
import time

rng = np.random.default_rng(7)
n = 200_000
big = pd.DataFrame({"priority": rng.choice(["low", "medium", "high"], size=n), "response_min": rng.integers(1, 300, size=n)})


def label(row):
    if row["priority"] == "high" and row["response_min"] > 15:
        return "urgent"
    return "late" if row["response_min"] > 60 else "ok"


start = time.perf_counter()
by_apply = big.apply(label, axis=1)
apply_s = time.perf_counter() - start

start = time.perf_counter()
conditions = [(big["priority"] == "high") & (big["response_min"] > 15), big["response_min"] > 60]
by_select = pd.Series(np.select(conditions, ["urgent", "late"], default="ok"), index=big.index)
select_s = time.perf_counter() - start

print("same labels:", (by_apply == by_select).all())
print(f"apply(axis=1): {apply_s:.2f}s | np.select: {select_s:.3f}s | {apply_s / select_s:.0f}x faster")
print(by_select.value_counts().to_dict())
%% md
**What to notice:** Both give the same labels, but the row-wise `apply` builds a Series for every row and calls Python
200,000 times, while `np.select` evaluates two column comparisons once. The vectorized version is many times faster
(the exact ratio depends on the machine). `np.select` checks conditions in order, like a SQL `CASE`.
%% md
## Know the memory cost

A DataFrame lives entirely in memory, and pandas often needs several times the data's size while it works (each
step can create new columns). `memory_usage(deep=True)` shows the real footprint. Categories for repeated strings,
smaller integer types and reading only the needed columns (`usecols=`) shrink it; beyond that, use an engine that
streams or spills: Polars, DuckDB or Spark.

**Where it matters**
- Deciding whether a job fits on its machine before it is killed at 3 a.m.

**Watch out for**
- `object` columns of Python strings: each value is a separate Python object, often the largest part of a DataFrame.
%% md
### Measure a column three ways

Store one million priority labels as Python objects, as the `str` dtype and as a `category`, and compare memory.
%% code
priorities = pd.Series(rng.choice(["low", "medium", "high"], size=1_000_000))
as_object = priorities.astype(object)
as_str = priorities.astype("str")
as_category = priorities.astype("category")
for name, series in [("object", as_object), ("str", as_str), ("category", as_category)]:
    print(f"{name:9} {series.memory_usage(deep=True) / 1e6:6.1f} MB")
%% md
**What to notice:** The same million labels take tens of megabytes as Python objects, less as pandas 3's Arrow-backed
`str` dtype, and about one megabyte as a `category`, which stores each distinct label once and a small integer code per
row.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** Yesterday's file loaded `customer_id` as integers; today's as floats. What happened and how do you prevent it?

**A.** Today's file has a missing value in that column, so pandas guessed `float64`. Declare the type (`dtype={"customer_id": "Int64"}` or `"str"`) so every file gives the same schema.

**Q2.** `df[df.status == "late"]["fee"] = 10` ran without error but no fee changed. Why, and what is the fix?

**A.** It is chained assignment: under copy-on-write the filtered DataFrame is a copy, so the original is unchanged. Use `df.loc[df.status == "late", "fee"] = 10`.

**Q3.** How do you make a pandas join fail when the lookup has duplicate keys?

**A.** Pass `validate="many_to_one"` (or the cardinality you expect) to `merge`; it raises `MergeError` instead of silently multiplying rows.

**Q4.** A report counts orders per day from UTC timestamps, but the business is in New York. What goes wrong?

**A.** Evening orders in New York fall on the next UTC day, so daily counts shift. Convert to `America/New_York` with `tz_convert` before bucketing by date.

**Q5.** When is pandas the wrong tool?

**A.** When the data does not fit comfortably in memory several times over, when the job must stream, or when many processes need the same data. Polars, DuckDB or Spark handle larger-than-memory work.
%% md
## Key takeaways

- Declare column types when reading; pandas 3 uses a `str` dtype for text and nullable types such as `Int64`.
- Copy-on-write is always on: update in place only with one `.loc[rows, columns] = value` call.
- Decide what missing values mean before aggregating; `mean` and `count` skip them.
- Use `validate=` on every `merge` and `indicator=True` to find orphans.
- Prefer vectorized column operations and `np.select` to `apply` and row loops.
- Measure memory with `memory_usage(deep=True)`; use categories and smaller types, or a bigger engine.
%% md
**Next:** Continue with [DuckDB](../duckdb/duckdb.ipynb), which runs the same kind of work as SQL on files, with
less memory.
'''

build("notebooks/topics/dataframes/dataframes-01-pandas.ipynb", SPEC)
