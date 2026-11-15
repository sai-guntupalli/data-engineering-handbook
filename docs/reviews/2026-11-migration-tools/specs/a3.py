import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from af_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/airflow/airflow-03-backfill.ipynb"
SPEC = """%% md
# Airflow 3: Data intervals and backfills

A scheduled DAG run is not "the job that ran at midnight"; it is "the job responsible for one slice of time". This lab
shows how Airflow 3 assigns that slice (and how `@daily` changed from Airflow 2), how tasks select input by it and
publish idempotently, how templates hand it to operators, and how to plan a backfill with Airflow's CLI before running
it.

@@INTRO@@

@@SETUP_PIP@@
%% md
## Setup and sample data

The next cell creates an Airflow home and its metadata database and defines the helpers from Airflow 1, plus
`airflow`, which runs an Airflow CLI command. The sample data is a daily orders export written to a `published`
folder, one file per day.

@@HELPERS@@
%% md
## Logical dates and data intervals

Every DAG run has a **logical date** and a **data interval** (`data_interval_start` to `data_interval_end`), chosen by
the DAG's **timetable**. The timetable decides what those mean:

```text
CronDataIntervalTimetable("0 0 * * *")   interval = the previous day; the run starts after the day ends
CronTriggerTimetable("0 0 * * *")         interval = an instant (start == end); "@daily" means this in Airflow 3
```

In Airflow 2, a cron string or `@daily` meant a data interval covering the previous day. In Airflow 3 it means a
trigger at that time with an empty interval, unless you choose `CronDataIntervalTimetable` explicitly.

**Where it matters**

Daily batch pipelines that load "yesterday" should use an interval timetable, so that every run, rerun and backfill
carries the exact slice it owns.

**Watch out for**

Upgrading from Airflow 2 silently changes DAGs that relied on the default: `data_interval_start` and
`data_interval_end` become equal, and a filter such as `start <= t < end` selects nothing.
%% code
run_dag_file("timetables.py", '''
from datetime import datetime, timezone

from airflow.sdk import dag, get_current_context, task
from airflow.timetables.interval import CronDataIntervalTimetable

start = datetime(2026, 1, 1, tzinfo=timezone.utc)


def show_interval():
    context = get_current_context()
    print(f"LAB {context['dag'].dag_id:>14}: {context['data_interval_start']:%m-%d %H:%M} -> {context['data_interval_end']:%m-%d %H:%M}")


@dag(schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC"), start_date=start)
def interval_daily():
    task(show_interval)()


@dag(schedule="@daily", start_date=start)
def trigger_daily():
    task(show_interval)()


interval_dag, trigger_dag = interval_daily(), trigger_daily()

if __name__ == "__main__":
    when = datetime(2026, 2, 3, tzinfo=timezone.utc)
    interval_dag.test(logical_date=when)
    trigger_dag.test(logical_date=when)
''')
%% md
**What to notice:** For the same logical date, the interval timetable's run owns February 2 from 00:00 to February 3
00:00, the day that has just ended. The `@daily` run's interval starts and ends at the same instant: there is no
"yesterday" in it unless the code computes one.
%% md
## Select by interval, publish by partition

A task should select its input with the run's interval and write its output to a location named after that
interval, replacing whatever is there. Then running the same interval twice gives the same result, which is what
makes retries, reruns and backfills safe.

**Where it matters**

Reprocessing a bad day becomes "rerun that interval": the task overwrites the day's partition, and no other day is
touched.

**Watch out for**

`datetime.now()` or `date.today()` inside a task breaks this: a backfill of February 2 run in March would process
March. Use the interval from the context or a template, never the clock.
%% code
run_dag_file("daily_export.py", '''
from datetime import datetime, timezone
from pathlib import Path

from airflow.sdk import dag, get_current_context, task
from airflow.timetables.interval import CronDataIntervalTimetable

published = Path(__file__).resolve().parent.parent / "published"


@dag(schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC"), start_date=datetime(2026, 2, 1, tzinfo=timezone.utc))
def daily_export():
    @task
    def export():
        context = get_current_context()
        day = context["data_interval_start"].date()
        published.mkdir(exist_ok=True)
        (published / f"orders_{day}.csv").write_text(f"day,cents\\\\n{day},1200\\\\n")  # overwrite the day
        print(f"LAB exported {day}")

    export()


pipeline = daily_export()

if __name__ == "__main__":
    for day in (2, 3, 4, 3):  # the last run repeats February 3's run
        pipeline.test(logical_date=datetime(2026, 2, day, tzinfo=timezone.utc))
    print("LAB files:", sorted(path.name for path in published.glob("*.csv")))
''')
%% md
**What to notice:** Four runs produced three files. Each run exported the day before its logical date, and the
repeated February 3 run rewrote `orders_2026-02-02.csv` instead of adding a fourth file.
%% md
## Templates hand the interval to operators

Operators that are not Python functions, such as `BashOperator` or SQL operators, receive the interval through
**Jinja templates** in their arguments: `{{ ds }}` (the logical date as `YYYY-MM-DD`), `{{ data_interval_start }}` and
`{{ data_interval_end }}`. Airflow renders them for each run just before the task executes.

**Where it matters**

A SQL task with `where event_time >= '{{ data_interval_start }}' and event_time < '{{ data_interval_end }}'` is
idempotent and backfillable without any Python.

**Watch out for**

Only an operator's templated fields are rendered; a template in an ordinary argument stays literal text. Check the
operator's `template_fields`, and look at the "Rendered template" view when a value looks wrong.
%% code
run_dag_file("templated.py", '''
from datetime import datetime, timezone

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag
from airflow.timetables.interval import CronDataIntervalTimetable


@dag(schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC"), start_date=datetime(2026, 2, 1, tzinfo=timezone.utc))
def templated_export():
    BashOperator(
        task_id="export",
        bash_command="echo LAB exporting rows from {{ data_interval_start | ds }} to {{ data_interval_end | ds }}",
    )


pipeline = templated_export()

if __name__ == "__main__":
    pipeline.test(logical_date=datetime(2026, 2, 3, tzinfo=timezone.utc))
''')
%% md
**What to notice:** The shell command received concrete dates, February 2 to February 3, rendered from the run's
interval. The same DAG run for another logical date would render that date instead, with no code change.
%% md
## Plan a backfill before running it

A **backfill** creates runs for a range of past intervals. In Airflow 3 the scheduler runs it, and the CLI (or the UI)
creates it: `airflow backfill create --dag-id ... --from-date ... --to-date ...`. `--dry-run` lists the runs it would
create without creating them, and `--reprocess-behavior` decides what happens to intervals that already have runs:
`none` skips them, `failed` re-runs failed ones, `completed` re-runs all.

**Where it matters**

A dry run shows exactly which intervals a backfill will touch before it costs warehouse time, and
`--max-active-runs` keeps a long backfill from crowding out the daily schedule.

**Watch out for**

The default skips intervals that already have runs, so a backfill meant to reprocess a buggy week does nothing unless
you choose `completed`. Read the dry run before trusting the result.
%% code
airflow("dags", "reserialize")
window = ["--dag-id", "daily_export", "--from-date", "2026-02-01", "--to-date", "2026-02-05", "--dry-run"]
print("default (skip existing runs):")
airflow("backfill", "create", *window, show="|")
print("--reprocess-behavior completed:")
airflow("backfill", "create", *window, "--reprocess-behavior", "completed", show="|")
%% md
**What to notice:** The default dry run lists only February 1 and 5: the earlier `dag.test()` runs already cover
February 2, 3 and 4, so a default backfill would skip them. With `--reprocess-behavior completed`, the same window
lists all five dates.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Hourly intervals

**Difficulty:** Easy · about 10 min

Write a DAG with an hourly `CronDataIntervalTimetable` and print the interval of the run for logical date
2026-02-03 09:00.
%% code
# Try your solution here.
%% solution
run_dag_file("hourly.py", '''
from datetime import datetime, timezone

from airflow.sdk import dag, get_current_context, task
from airflow.timetables.interval import CronDataIntervalTimetable


@dag(schedule=CronDataIntervalTimetable("0 * * * *", timezone="UTC"), start_date=datetime(2026, 2, 1, tzinfo=timezone.utc))
def hourly():
    @task
    def show():
        context = get_current_context()
        print(f"LAB {context['data_interval_start']:%m-%d %H:%M} -> {context['data_interval_end']:%m-%d %H:%M}")

    show()


pipeline = hourly()

if __name__ == "__main__":
    pipeline.test(logical_date=datetime(2026, 2, 3, 9, tzinfo=timezone.utc))
''')
%% md
### Exercise 2: Find the clock bug

**Difficulty:** Medium · about 10 min

The task below names its file after `date.today()`. Run it for logical date 2026-02-03 and compare the file it
writes with the file the interval says it should write.
%% code
# Try your solution here.
%% solution
run_dag_file("clock_bug.py", '''
from datetime import date, datetime, timezone

from airflow.sdk import dag, get_current_context, task
from airflow.timetables.interval import CronDataIntervalTimetable


@dag(schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC"), start_date=datetime(2026, 2, 1, tzinfo=timezone.utc))
def clock_bug():
    @task
    def export():
        should = get_current_context()["data_interval_start"].date()
        print(f"LAB wrote orders_{date.today()}.csv; the interval owns orders_{should}.csv")
        print("LAB same file:", date.today() == should)

    export()


pipeline = clock_bug()

if __name__ == "__main__":
    pipeline.test(logical_date=datetime(2026, 2, 3, tzinfo=timezone.utc))
''')
%% md
### Exercise 3: Re-run only failures

**Difficulty:** Easy · about 5 min

Dry-run a backfill of `daily_export` for February 1 to 5 that would re-run only failed intervals. Which dates does it
list, and why?
%% code
# Try your solution here.
%% solution
airflow("backfill", "create", *window, "--reprocess-behavior", "failed", show="|")
print("No existing run failed, so only the dates without any run are listed.")
%% md
## Key takeaways

- Each run owns a data interval chosen by the timetable. Use `CronDataIntervalTimetable` for "process yesterday";
  in Airflow 3, `@daily` and cron strings give an empty interval.
- Select input by `data_interval_start` and `data_interval_end` and overwrite the output partition, so any run can be
  repeated safely. Never use the clock inside a task.
- Templates such as `{{ data_interval_start | ds }}` pass the interval to operators' templated fields.
- Plan backfills with `airflow backfill create --dry-run`, and set `--reprocess-behavior` deliberately: the default
  skips intervals that already ran.
%% md
**Next:** [Capstone: an end-to-end batch pipeline](../concepts/end-to-end-pipeline-capstone.ipynb), which puts
ingestion, quality checks, dbt and Airflow together.
"""
SPEC = SPEC.replace("@@INTRO@@", INTRO).replace("@@SETUP_PIP@@", SETUP_PIP).replace("@@HELPERS@@", HELPERS)

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
