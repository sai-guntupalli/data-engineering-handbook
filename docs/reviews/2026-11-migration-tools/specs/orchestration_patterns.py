import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# Orchestration patterns

A nightly pipeline extracts orders, loads them, builds three marts and refreshes a dashboard. One night the
extract fails at 02:00 because the API times out; the marts must not run on half the data, the job should retry,
and on Monday someone asks to rebuild all of last month after a bug fix. None of that is the transformation code's
job. It is the **orchestrator's**: dependencies, schedules, retries, state, backfills and alerts.

This lesson builds the core of an orchestrator in plain Python, one pattern at a time, so the behaviour of
Airflow, Dagster or Prefect stops being magic: dependency graphs, data intervals, idempotent tasks, retries,
sensors versus events, dynamic fan-out, backfills, reruns and freshness checks. It ends with how the real tools
express the same ideas.

*Last reviewed: November 2026, against Apache Airflow 3.1, Dagster 1.12 and Prefect 3 documentation.*

**Prerequisites:** [Python 9: data engineering patterns](../python/learning/python-09-data-engineering.ipynb).
For the tool itself, read [Apache Airflow](../airflow/airflow.ipynb) after this lesson.
%% md
## Setup and sample data

This notebook uses only the Python standard library, so there is nothing to install. The cell below defines the
pipeline used throughout: six tasks and the tasks each one depends on, plus a `warehouse` dictionary that stands in
for the tables the tasks write, keyed by table and date.
%% code
import random
import time
from collections import defaultdict
from datetime import date, datetime, timedelta
from graphlib import CycleError, TopologicalSorter

PIPELINE = {
    "extract_orders": [],
    "extract_customers": [],
    "load_staging": ["extract_orders", "extract_customers"],
    "mart_revenue": ["load_staging"],
    "mart_customers": ["load_staging"],
    "refresh_dashboard": ["mart_revenue", "mart_customers"],
}
warehouse = defaultdict(dict)  # table -> {row key: row}
print(f"{len(PIPELINE)} tasks, {sum(len(d) for d in PIPELINE.values())} dependencies")
%% md
## The orchestrator's job

An orchestrator decides **when** something runs and **in what order**, records **what happened**, and reacts to
failure. The task decides **what** to compute and must be safe to run again. Keeping that split is the most important
design rule: a task that only works when run exactly once, in order, at the right time, cannot be retried or
backfilled by any orchestrator.

| Orchestrator owns | Task owns |
|---|---|
| Dependencies, schedule, concurrency limits | The computation and its inputs and outputs |
| Retries, timeouts, alerts | Idempotency: same interval in, same result out |
| Run history and state | Validating its own inputs and outputs |
| Backfills and reruns | Writing atomically (overwrite a partition, merge by key) |

**Where it matters**
- Designing any pipeline before choosing a tool.

**Watch out for**
- Business logic inside the orchestrator file (long Python in a DAG definition): it is hard to test and runs every
  time the scheduler parses the file.
%% md
## Dependencies form a graph

Tasks and their dependencies form a **directed acyclic graph** (DAG). A topological sort gives a valid order, and
tasks whose dependencies are all done can run in parallel. A cycle (A needs B, B needs A) has no valid order and must
be rejected when the pipeline is defined, not at 02:00.

**Where it matters**
- Running independent extracts in parallel to finish sooner.

**Watch out for**
- Hidden dependencies: a mart that reads a table nobody declared as upstream runs on stale data whenever the order
  happens to change.
%% md
### Find the waves that can run in parallel

`graphlib.TopologicalSorter` hands out tasks as soon as their dependencies are marked done.
%% code
def waves(pipeline):
    """Groups of tasks that can run at the same time, in order."""
    sorter = TopologicalSorter(pipeline)
    sorter.prepare()  # raises CycleError for a cycle
    result = []
    while sorter.is_active():
        ready = sorted(sorter.get_ready())
        result.append(ready)
        sorter.done(*ready)
    return result


for number, wave in enumerate(waves(PIPELINE), start=1):
    print(f"wave {number}: {wave}")

try:
    waves({**PIPELINE, "extract_orders": ["refresh_dashboard"]})
except CycleError as error:
    print("rejected:", " -> ".join(error.args[1]))
%% md
**What to notice:** The two extracts run together in wave 1, both marts together in wave 3, so six tasks finish in
four steps. Making `extract_orders` depend on the dashboard created a cycle, and the graph was rejected at definition
time with the loop spelled out.
%% md
## Schedules run over data intervals

A daily schedule does not mean "process whatever is there at midnight". Each run owns a **data interval**:
`[2026-03-01 00:00, 2026-03-02 00:00)` for the March 1 run, which starts after the interval ends. The task reads
exactly that interval, so a late or repeated run produces the same output. Airflow calls the start of the interval
the **logical date**; if the scheduler was down, **catchup** creates the missed runs.

**Where it matters**
- Every incremental pipeline: the interval, not the wall clock, decides which rows a run processes.

**Watch out for**
- `datetime.now()` inside a task: a rerun next week processes next week's data, not the interval it was meant for.
%% md
### List the runs a scheduler owes after downtime

The pipeline started on March 1. The scheduler was down until March 4 at 06:30. Which runs should it create?
%% code
def due_runs(start, now, every=timedelta(days=1)):
    """Data intervals whose end has passed: each one is a run the scheduler owes."""
    runs, interval_start = [], start
    while interval_start + every <= now:
        runs.append((interval_start, interval_start + every))
        interval_start += every
    return runs


for begin, end in due_runs(datetime(2026, 3, 1), datetime(2026, 3, 4, 6, 30)):
    print(f"logical date {begin:%Y-%m-%d}: reads [{begin:%m-%d %H:%M}, {end:%m-%d %H:%M})")
%% md
**What to notice:** Three runs are owed, for March 1, 2 and 3. There is no run for March 4 yet, because its interval
ends at midnight tonight. Each run reads its own day, whatever time it actually starts.
%% md
## Idempotent tasks

A task is **idempotent** when running it twice for the same interval leaves the same result as running it once.
Two ways to get there: **overwrite the partition** the interval owns, or **merge by key**. Appending is not
idempotent: a retry after a partial failure, or a backfill, duplicates rows.

**Where it matters**
- Retries, backfills and reruns, which every pipeline eventually needs.

**Watch out for**
- Side effects that cannot be undone (sending emails, calling a payment API): guard them with an idempotency key.
%% md
### Run an appending task and an overwriting task twice

Both tasks load March 1's orders into a table. Each runs twice, as a retry would.
%% code
orders_by_day = {date(2026, 3, 1): [("o1", 120.0), ("o2", 80.0)], date(2026, 3, 2): [("o3", 45.5)]}


def load_append(day, table):
    table.setdefault("rows", []).extend(orders_by_day[day])


def load_overwrite(day, table):
    table[day] = list(orders_by_day[day])  # the interval owns its partition: replace it


appended, partitioned = {}, {}
for _ in range(2):
    load_append(date(2026, 3, 1), appended)
    load_overwrite(date(2026, 3, 1), partitioned)
print("append:   ", len(appended["rows"]), "rows, total", sum(a for _, a in appended["rows"]))
print("overwrite:", sum(len(v) for v in partitioned.values()), "rows, total", sum(a for v in partitioned.values() for _, a in v))
%% md
**What to notice:** After two runs the appending task holds four rows and a total of 400.00, double the truth.
The overwriting task holds the two real rows and 200.00, no matter how many times it runs.
%% md
## Retries with backoff

Most failures in pipelines are **transient**: a timeout, a throttled API, a lost spot instance. Retrying after a
delay usually succeeds. The delay should grow (**exponential backoff**) so a struggling service gets room, and
include **jitter** so many tasks do not retry in lockstep. **Permanent** errors (bad credentials, a schema that
does not match) should fail fast instead of retrying for an hour.

**Where it matters**
- Every task that calls a network service.

**Watch out for**
- Retries on a non-idempotent task: each retry repeats the side effect.
%% md
### Retry a flaky extract

`flaky_extract` times out on its first two attempts. `run_with_retries` retries transient errors with backoff and
jitter, and stops at once on a permanent one.
%% code
class TransientError(Exception):
    pass


class PermanentError(Exception):
    pass


def run_with_retries(task, retries=4, base_delay=1.0, sleep=lambda seconds: None, rng=random.Random(7)):
    """Run task(); on TransientError wait base * 2**attempt, plus up to 50% jitter, and try again."""
    for attempt in range(retries + 1):
        try:
            return task(), attempt
        except TransientError as error:
            if attempt == retries:
                raise
            delay = base_delay * 2**attempt * (1 + rng.random() * 0.5)
            print(f"  attempt {attempt + 1} failed ({error}); retrying in {delay:.1f}s")
            sleep(delay)  # a real orchestrator sleeps or reschedules; here we only print the delay


attempts = iter([TransientError("timeout"), TransientError("timeout"), None])


def flaky_extract():
    outcome = next(attempts)
    if outcome:
        raise outcome
    return 1250


rows, failures = run_with_retries(flaky_extract)
print(f"extracted {rows} rows after {failures} failed attempts")


def bad_credentials():
    raise PermanentError("403 forbidden")


try:
    run_with_retries(bad_credentials)
except PermanentError as error:
    print("failed fast:", error)
%% md
**What to notice:** The extract failed twice, waited about 1 and then about 2 seconds (doubling, with some jitter),
and succeeded on the third attempt. The `403` was not a `TransientError`, so it failed on the first attempt instead
of burning four retries.
%% md
## Sensors and events

A downstream pipeline often waits for something outside the orchestrator: a file from a partner, a table another
team publishes. Two ways to wait:

- A **sensor** polls ("does the file exist yet?") every few minutes. Simple, but each check costs a worker slot or a
  scheduler cycle, and a short poll interval multiplies the cost. Airflow's **deferrable** sensors free the worker
  while waiting.
- **Event- or data-aware scheduling** runs the consumer when the producer reports an update: Airflow **assets**,
  Dagster **asset sensors and declarative automation**, a message on a queue, or a cloud storage notification.

**Where it matters**
- Cross-team dependencies, where you do not control when the upstream finishes.

**Watch out for**
- Sensors without a timeout: a partner who never sends the file holds a slot forever and nobody is alerted.
%% md
### Compare polling with an event

The partner's file lands at 05:47. A sensor checks every 5 minutes from 01:00; an event subscription is notified
when the file lands.
%% code
arrives = datetime(2026, 3, 2, 5, 47)
check, checks = datetime(2026, 3, 2, 1, 0), 0
while True:
    checks += 1
    if check >= arrives:
        break
    check += timedelta(minutes=5)

print(f"sensor: {checks} checks, starts at {check:%H:%M} ({(check - arrives).seconds // 60} min after arrival)")
print(f"event:  1 notification, starts at {arrives:%H:%M}")
%% md
**What to notice:** The sensor ran 59 checks over almost five hours and still started 3 minutes late, because the
file arrived between checks. The event started the consumer when the file landed with one notification. Polling
is fine for a handful of waits; for many it wastes capacity.
%% md
## Dynamic fan-out and fan-in

Some work is only known at run time: process each file that landed today, each tenant, each partition. The
orchestrator **maps** one task over the list (fan-out), runs the copies with a concurrency limit, and a downstream
task collects the results (fan-in). Decide up front what a partial failure means: retry only the failed copies,
fail the run, or continue with what succeeded and alert.

**Where it matters**
- File-based ingestion and per-tenant processing.

**Watch out for**
- Mapping over thousands of tiny items: the scheduling overhead dominates; batch items into chunks.
%% md
### Process each landed file with at most two at a time

Five files landed; one is corrupt. Map a task over them in groups of two and collect the results.
%% code
landed = ["orders_01.csv", "orders_02.csv", "orders_03.csv", "orders_04_corrupt.csv", "orders_05.csv"]


def process(file):
    if "corrupt" in file:
        raise ValueError(f"cannot parse {file}")
    return int(file[7:9]) * 100  # pretend row count


results, failed = {}, {}
for group_start in range(0, len(landed), 2):  # concurrency limit: two copies at once
    group = landed[group_start:group_start + 2]
    for file in group:
        try:
            results[file] = process(file)
        except ValueError as error:
            failed[file] = str(error)
    print("ran together:", group)

print(f"fan-in: {len(results)} files, {sum(results.values())} rows; failed: {list(failed)}")
%% md
**What to notice:** Five mapped copies ran in three groups of at most two. The corrupt file failed on its own
without stopping the others, and the fan-in step saw four successes and one named failure, so a rerun can target
just `orders_04_corrupt.csv`.
%% md
## Backfills and reruns

A **backfill** runs the pipeline for a range of past intervals, after a bug fix or for a new table. Because each run
owns its interval and its tasks are idempotent, a backfill is just many ordinary runs, limited by a maximum number
of active runs so it does not starve the daily schedule.

A **rerun** after a failure should start from the failed task, not from the beginning, and must also rerun
everything downstream of it (in Airflow: "clear" the task with downstream).

**Where it matters**
- Recovering from a bad deploy without redoing expensive extracts that succeeded.

**Watch out for**
- Backfilling tasks with `depends_on_past` or cumulative state in date order only; others can run in parallel.
%% md
### Rerun from a failed task

Run the pipeline for March 2 with `mart_revenue` failing, then rerun only what is needed.
%% code
def run(pipeline, day, state, fail=frozenset(), only=None):
    """Run tasks in dependency order; skip tasks whose upstream did not succeed."""
    for task in [t for wave in waves(pipeline) for t in wave]:
        if only is not None and task not in only:
            continue
        if any(state.get(up) != "success" for up in pipeline[task]):
            state[task] = "upstream_failed"
        elif task in fail:
            state[task] = "failed"
        else:
            state[task] = "success"
    return state


def downstream_of(pipeline, task):
    children = {t for t, deps in pipeline.items() if task in deps}
    return children | {d for c in children for d in downstream_of(pipeline, c)}


state = run(PIPELINE, date(2026, 3, 2), {}, fail={"mart_revenue"})
print("first run:", state)
to_clear = {"mart_revenue"} | downstream_of(PIPELINE, "mart_revenue")
state = run(PIPELINE, date(2026, 3, 2), state, only=to_clear)
print("cleared:  ", sorted(to_clear))
print("rerun:    ", state)
%% md
**What to notice:** The first run failed `mart_revenue`, so `refresh_dashboard` was marked `upstream_failed`
rather than running on stale numbers, while `mart_customers` succeeded. Clearing `mart_revenue` with its
downstream reran just those two tasks; the extracts and staging load were not repeated.
%% md
## Freshness and alerts

A pipeline can be green and still wrong: it ran, but on no new data, or it finished after the business needed it.
Alert on what consumers care about: **freshness** (the newest data is at most N hours old), **completeness** (row
counts in an expected range), and **deadlines** (the mart is ready by 07:00). Alert on symptoms, route alerts to an
owner, and include the run, the interval and a link to logs.

**Where it matters**
- Every table someone depends on for a decision.

**Watch out for**
- Alerting on every retry: people learn to ignore the channel.
%% md
### Check freshness against a deadline

Three tables, the time their newest data was loaded, and a 6-hour freshness target, checked at 07:00.
%% code
now = datetime(2026, 3, 2, 7, 0)
last_loaded = {"mart_revenue": datetime(2026, 3, 2, 3, 10), "mart_customers": datetime(2026, 3, 1, 23, 50),
               "refresh_dashboard": datetime(2026, 3, 1, 3, 5)}
target = timedelta(hours=6)
for table, loaded in last_loaded.items():
    age = now - loaded
    status = "ok" if age <= target else "STALE"
    print(f"{table:18} {age.total_seconds() / 3600:5.1f} h old  {status}")
%% md
**What to notice:** `mart_revenue` (3.8 hours) is fresh, `mart_customers` at 7.2 hours just missed the target, and
the dashboard has not refreshed in over a day. Only the stale tables should alert, each to its owner.
%% md
## How the tools express these patterns

| Pattern | Apache Airflow 3 | Dagster | Prefect 3 |
|---|---|---|---|
| Unit of work | Task in a DAG | Asset (or op) | Task in a flow |
| Dependencies | `a >> b`, or TaskFlow function calls | Asset inputs (`deps=`) | Function calls |
| Data intervals | `data_interval_start/end`, logical date | Partitions (daily, static, dynamic) | Parameters you pass |
| Retries | `retries`, `retry_exponential_backoff` | `RetryPolicy(backoff=...)` | `retries`, `retry_delay_seconds` |
| Waiting on others | Sensors, deferrable operators, assets | Sensors, declarative automation | Events and automations |
| Fan-out | Dynamic task mapping `.expand()` | Dynamic outputs, partitions | `.map()` |
| Backfill | `airflow backfill create` | Partition backfills in the UI | Re-run deployments with parameters |

```python
# Airflow 3 (TaskFlow): the same idempotent, retried, interval-based task
from airflow.sdk import dag, task
from datetime import datetime, timedelta

@dag(schedule="@daily", start_date=datetime(2026, 3, 1), catchup=True, max_active_runs=3)
def orders():
    @task(retries=3, retry_delay=timedelta(minutes=2), retry_exponential_backoff=True)
    def load(data_interval_start=None, data_interval_end=None):
        overwrite_partition("orders", data_interval_start, data_interval_end)
    load()

orders()
```

Cloud services (AWS Step Functions, Google Cloud Workflows, Azure Data Factory) and dbt's own scheduler cover
narrower cases with less to operate. Choose by where the pipeline runs, whether you think in tasks or in data
assets, and who will operate the scheduler.

**Where it matters**
- Picking or migrating an orchestrator.

**Watch out for**
- Choosing by features alone: the patterns above exist in all of them; operations cost and team familiarity decide.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** A task loads "yesterday's" orders using `date.today() - 1`. What goes wrong in a backfill?

**A.** Every backfill run loads the same day (yesterday relative to when it runs), not the interval it was created for. The task should use the run's data interval.

**Q2.** Why must `refresh_dashboard` be `upstream_failed` rather than run when `mart_revenue` fails?

**A.** Running it would publish yesterday's revenue next to today's customers as if both were current. Not running it keeps the dashboard consistent and makes the failure visible.

**Q3.** Which errors should not be retried, and why?

**A.** Permanent ones: bad credentials, missing permissions, invalid configuration, a schema mismatch. Retrying wastes time and delays the alert; the fix needs a human.

**Q4.** A partner's file arrives at an unpredictable time between midnight and 09:00. Sensor or event?

**A.** An event (storage notification, asset update, message) starts the consumer when the file lands with no polling. If you must use a sensor, make it deferrable and give it a timeout and an alert.

**Q5.** What makes a backfill of 90 days safe to run in parallel?

**A.** Each run reads only its own interval and writes idempotently (partition overwrite or merge by key), with no task depending on the previous day's output. A cap on active runs protects the daily schedule.
%% md
## Key takeaways

- The orchestrator owns order, timing, retries, state and backfills; the task owns idempotent computation.
- Dependencies are a DAG: independent tasks run in parallel, cycles are rejected at definition time.
- Each run processes its data interval, never the wall clock.
- Retry transient errors with exponential backoff and jitter; fail permanent errors fast.
- Prefer events over polling for cross-team waits; map over runtime lists with a concurrency limit.
- Rerun from the failed task with its downstream; alert on freshness and deadlines.
%% md
**Next:** Continue with [Apache Airflow](../airflow/airflow.ipynb) to see these patterns in the most widely used
orchestrator.
'''

build("notebooks/topics/concepts/orchestration-patterns.ipynb", SPEC)
