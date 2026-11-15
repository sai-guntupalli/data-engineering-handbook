import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from dbt_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/dbt/dbt-05-microbatch.ipynb"
SPEC = f"""%% md
# dbt 5: Microbatch incremental models

The incremental models in dbt 3 process "everything after the high-water mark" in one query. The **microbatch**
strategy instead splits time into fixed batches (an hour, a day) and builds each batch as an independent query that
replaces that slice of the table. This lesson configures a daily microbatch model, watches a scheduled run process
the latest batches, backfills a corrected day, and retries only the batch that failed.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell creates an empty dbt project with the `write`, `dbt` and `sql` helpers from dbt 1, and loads raw click
events for three days. The source is declared with `event_time`, the column that says when each event happened.

{HELPERS}


sql(\"\"\"
create table raw_events as select * from (values
    (1, timestamp '2026-02-01 10:00', 1200), (2, timestamp '2026-02-01 18:30', 300),
    (3, timestamp '2026-02-02 11:00', 800),
    (4, timestamp '2026-02-03 09:00', 900), (5, timestamp '2026-02-03 23:59', 100)
) t(id, event_time, cents)
\"\"\")
write("models/sources.yml", \"\"\"
version: 2
sources:
  - name: raw
    schema: main
    tables:
      - name: raw_events
        config:
          event_time: event_time
\"\"\")


def batches():
    \"\"\"The batch windows the last dbt run processed, per model.\"\"\"
    for node in last_result.result:
        done = node.batch_results.successful if node.batch_results else []
        failed = node.batch_results.failed if node.batch_results else []
        print(node.node.name, "built:", [start.strftime("%m-%d") for start, _ in done], "failed:", [start.strftime("%m-%d") for start, _ in failed])


def daily():
    return sql("select cast(event_time as date) as day, count(*), sum(cents) from daily_clicks group by 1 order by 1")
%% md
## Batches instead of a high-water mark

A microbatch model needs four settings: `incremental_strategy='microbatch'`, its own `event_time` column,
`batch_size` (`hour`, `day`, `month` or `year`) and `begin`, the first batch to build. The model's SQL selects
**everything**: dbt adds the time filter itself, to the model and to every input that declares an `event_time`, so each
batch reads only its own slice.

`--event-time-start` and `--event-time-end` choose which batches a run builds. Without them, dbt builds from `begin`
on the first run, and later the current batch plus `lookback` earlier ones.

**Where it matters**

Event and log tables with billions of rows suit microbatch: each batch is small, batches can run and fail
independently, and a backfill is just a range of batches.

**Watch out for**

Microbatch replaces each batch's rows (delete, then insert); it does not upsert by key, and dbt rejects a
`unique_key`. A row whose `event_time` changes can therefore leave a copy in its old batch, so use it for immutable
events, not for mutable records such as orders.
%% code
write("models/daily_clicks.sql", \"\"\"
{{{{ config(
    materialized='incremental',
    incremental_strategy='microbatch',
    event_time='event_time',
    batch_size='day',
    begin='2026-02-01',
    lookback=1
) }}}}
select id, event_time, cents from {{{{ source('raw', 'raw_events') }}}}
\"\"\")
dbt("run", "--event-time-start", "2026-02-01", "--event-time-end", "2026-02-04")
batches()
print(daily())
%% md
**What to notice:** dbt ran one query per day, three in total, and reported each batch separately. The two events on
February 3, including the one at 23:59, landed in that day's batch, because batches are half-open days.
%% md
## A scheduled run processes the latest batches

In production the model runs on a schedule with no time arguments. dbt then builds the batch containing "now" and
`lookback` batches before it, so a run at 00:15 also rebuilds yesterday and catches events that arrived after
yesterday's run.

**Where it matters**

`lookback` is how a microbatch model absorbs late data: set it to cover how late events typically arrive, as with the
lookback window in dbt 3, but in whole batches.

**Watch out for**

The batches are computed from the run time in UTC. A job that runs late, or a warehouse in another time zone,
shifts which days are rebuilt, so pass explicit `--event-time-start` and `--event-time-end` for anything you need to
reproduce.
%% code
dbt("run")
print("batches in a scheduled run:", len(last_result.result[0].batch_results.successful), "(today plus lookback=1)")
%% md
**What to notice:** The scheduled run built two batches: the current day and one day of lookback. Which two depends on
the date you run this cell, which is exactly why reproducible backfills pass explicit dates.
%% md
## Backfilling a corrected day

When a source fixes historical data, rebuild just the affected batches with `--event-time-start` and
`--event-time-end`. Each selected batch is deleted and rebuilt from the source; every other day is untouched.

**Where it matters**

Corrections, late partner files and bug fixes in model logic are all handled the same way: pick the range, run it,
and check the totals for those days.

**Watch out for**

Rebuilding a batch reads only that batch's slice of the inputs. If the fix is in an upstream model, rebuild that
model's batches first, or the downstream batch rebuilds from the old upstream rows.
%% code
sql("update raw_events set cents = 850 where id = 3")
sql("insert into raw_events values (6, timestamp '2026-02-02 21:00', 400)")  # a late event for February 2
dbt("run", "--event-time-start", "2026-02-02", "--event-time-end", "2026-02-03")
batches()
print(daily())
%% md
**What to notice:** Only the February 2 batch was rebuilt. It now holds two events totalling 1,250 cents (the
corrected 850 plus the late 400), while February 1 and 3 kept their rows without being touched.
%% md
## Retrying only the failed batch

Batches succeed or fail independently. If one day fails (a malformed file, a timeout), the other batches are still
committed, the run reports a **partial success**, and `dbt retry` re-runs only what failed, with the same arguments
as the failed run.

Below, the model rejects negative amounts, and a malformed event with a negative amount lands on February 2.

**Where it matters**

On a large backfill, a single bad hour no longer forces you to rerun the whole range, and the failure points at
exactly which slice of data to investigate.

**Watch out for**

`dbt retry` repeats the failed command exactly, so retrying before fixing the cause fails the same way. And a partial
success leaves a gap in the table until the retry succeeds. Downstream models and dashboards should treat
missing batches as missing data, not as zero.
%% code
write("models/daily_clicks.sql", (project / "models/daily_clicks.sql").read_text().replace(
    "select id, event_time, cents",
    "select id, event_time, case when cents < 0 then error('negative amount for event ' || id) else cents end as cents",
))
sql("insert into raw_events values (7, timestamp '2026-02-02 12:00', -50)")  # a malformed event
dbt("run", "--event-time-start", "2026-02-01", "--event-time-end", "2026-02-04", expect_success=False)
batches()
sql("delete from raw_events where id = 7")  # fix the cause first: retry repeats the same command
dbt("retry")
batches()
print(daily())
%% md
**What to notice:** The run built February 1 and 3 and failed only February 2. After the bad event was removed, `dbt
retry` re-ran that batch, listed first, and carried over the two batches that had already succeeded; all three days
are back with their earlier totals.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Hourly batches

**Difficulty:** Easy · about 10 min

Copy the model as `hourly_clicks` with `batch_size='hour'`, build February 1, and count how many batches dbt built.
%% code
# Try your solution here.
%% solution
write("models/hourly_clicks.sql", (project / "models/daily_clicks.sql").read_text().replace("batch_size='day'", "batch_size='hour'"))
dbt("run", "--select", "hourly_clicks", "--event-time-start", "2026-02-01", "--event-time-end", "2026-02-02")
print(len(last_result.result[0].batch_results.successful), "hourly batches for one day")
%% md
### Exercise 2: Check a backfill

**Difficulty:** Medium · about 10 min

Delete event 5 from the source, rebuild only February 3, and show that the day's total dropped by 100 cents while the
other days are unchanged.
%% code
# Try your solution here.
%% solution
before = {{day: cents for day, _, cents in daily()}}
sql("delete from raw_events where id = 5")
dbt("run", "--select", "daily_clicks", "--event-time-start", "2026-02-03", "--event-time-end", "2026-02-04")
after = {{day: cents for day, _, cents in daily()}}
print({{str(day): after[day] - before[day] for day in before}})
%% md
### Exercise 3: Why not microbatch for orders?

**Difficulty:** Medium · about 15 min

Move event 1's `event_time` from February 1 to February 2 in the source, rebuild only February 2, and show that
event 1 now exists twice in `daily_clicks`.
%% code
# Try your solution here.
%% solution
sql("update raw_events set event_time = timestamp '2026-02-02 08:00' where id = 1")
dbt("run", "--select", "daily_clicks", "--event-time-start", "2026-02-02", "--event-time-end", "2026-02-03")
print(sql("select id, cast(event_time as date) from daily_clicks where id = 1 order by 2"))
print("February 1 still holds the old copy until its batch is rebuilt too.")
%% md
## Key takeaways

- A microbatch model selects everything; dbt filters the model and every input with an `event_time` into fixed
  batches and builds each one as a separate query.
- Scheduled runs build the current batch plus `lookback` earlier ones; explicit `--event-time-start` and
  `--event-time-end` make any range reproducible.
- Each batch is replaced with delete-then-insert, so microbatch suits immutable events, not rows that change key or
  time.
- Batches fail independently: a run can partly succeed, and `dbt retry` rebuilds only the failed batches.
%% md
**Next:** [Semantic layer](../concepts/semantic-layer.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
