## [Main title](../README.md)
### [Interview questions](full.md)

# Apache Airflow

**Notebook:** [`notebooks/topics/airflow.ipynb`](../notebooks/topics/airflow.ipynb) - runnable version of this topic with self-checking exercises.

Apache Airflow is a batch workflow orchestrator: you describe pipelines as Python DAGs and Airflow schedules, retries, backfills, and monitors them.

Examples below are shown for both versions: **Airflow 3** first, then the **Airflow 2** equivalent wherever the code differs. Airflow 2's final line (2.11.x) reached end of life on April 22, 2026, so Airflow 3 is the target for new work, but Airflow 2 code is still common in production and interviews.
+ [What is Airflow?](#What-is-Airflow)
+ [What problems does Airflow solve compared to cron?](#What-problems-does-Airflow-solve-compared-to-cron)
+ [When should you not use Airflow?](#When-should-you-not-use-Airflow)
+ [Explain how a workflow is designed in Airflow?](#Explain-how-a-workflow-is-designed-in-Airflow)
+ [Explain Airflow architecture and its components?](#Explain-Airflow-architecture-and-its-components)
+ [What are the types of executors in Airflow?](#What-are-the-types-of-executors-in-Airflow)
+ [How do you choose an executor for a production workload?](#How-do-you-choose-an-executor-for-a-production-workload)
+ [What are the logical date and data interval of a DAG run?](#What-are-the-logical-date-and-data-interval-of-a-DAG-run)
+ [How do you define a workflow in Airflow?](#How-do-you-define-a-workflow-in-Airflow)
+ [How do you schedule a DAG in Airflow?](#How-do-you-schedule-a-DAG-in-Airflow)
+ [Understanding cron expressions in Airflow](#Understanding-cron-expressions-in-Airflow)
+ [How do you pass data between tasks with XComs?](#How-do-you-pass-data-between-tasks-with-XComs)
+ [What is xcom_pull in Airflow?](#What-is-xcom_pull-in-Airflow)
+ [What are Jinja templates?](#What-are-Jinja-templates)
+ [How do you use Airflow XComs in Jinja templates?](#How-do-you-use-Airflow-XComs-in-Jinja-templates)
+ [How do you build dynamic pipelines with dynamic task mapping?](#How-do-you-build-dynamic-pipelines-with-dynamic-task-mapping)
+ [How do you make a DAG data-aware with Assets?](#How-do-you-make-a-DAG-data-aware-with-Assets)
+ [How do you wait for external data with sensors and deferrable operators?](#How-do-you-wait-for-external-data-with-sensors-and-deferrable-operators)
+ [How do Airflow backfills differ from normal scheduled runs?](#How-do-Airflow-backfills-differ-from-normal-scheduled-runs)
+ [How do you make tasks idempotent and safe to retry?](#How-do-you-make-tasks-idempotent-and-safe-to-retry)
+ [How do you handle retries, timeouts, and alerts?](#How-do-you-handle-retries-timeouts-and-alerts)
+ [How do you control concurrency with pools and DAG limits?](#How-do-you-control-concurrency-with-pools-and-DAG-limits)
+ [How do you design an Airflow DAG for a production data pipeline?](#How-do-you-design-an-Airflow-DAG-for-a-production-data-pipeline)
+ [How do you test Airflow DAGs before deploying them?](#How-do-you-test-Airflow-DAGs-before-deploying-them)
+ [How do you make a custom module available to Airflow if you are using Docker Compose?](#How-do-you-make-a-custom-module-available-to-Airflow-if-you-are-using-Docker-Compose)
+ [How do the same pipelines look in Airflow 2 and Airflow 3?](#How-do-the-same-pipelines-look-in-Airflow-2-and-Airflow-3)
+ [What changed between Airflow 2 and Airflow 3?](#What-changed-between-Airflow-2-and-Airflow-3)
+ [Real world use cases for Airflow](#Real-world-use-cases-for-Airflow)
+ [How does Airflow compare with cron, dbt, and Spark?](#How-does-Airflow-compare-with-cron-dbt-and-Spark)

## What is Airflow?

Apache Airflow is an open-source workflow orchestration platform. It started at Airbnb in October 2014 and is now an Apache top-level project. You author pipelines as Python code: a DAG (Directed Acyclic Graph) is a set of tasks plus the dependencies between them. The scheduler creates DAG runs on a timetable, dispatches task instances, records state, retries failures, and exposes everything through the UI, REST API, and CLI.

Airflow does not move or transform data itself. It orchestrates work that runs somewhere else: SQL in Snowflake, BigQuery, Redshift, or Postgres, dbt models, Spark jobs, Kubernetes pods, Python functions, shell scripts, or an HTTP call. Think of it as the *when and in what order* layer, not the *how* layer.

The current line is Airflow 3.x (3.3.x at the time of writing). The most important change for DAG authors is that authoring uses the public `airflow.sdk` namespace, and task code can no longer touch the metadata database directly. `from airflow import DAG` still resolves to the SDK class, and legacy paths such as `airflow.models.dag.DAG` still import but emit deprecation warnings; new code should use `airflow.sdk`.

A minimal Airflow 3 DAG:

```python
import pendulum
from airflow.sdk import DAG, task

with DAG(
    dag_id="hello_airflow",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
):

    @task
    def greet() -> str:
        return "hello"

    @task
    def shout(message: str) -> None:
        print(f"{message.upper()} from Airflow")

    shout(greet())
```
The same DAG in Airflow 2 uses the classic imports and `schedule_interval`:

```python
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago   # removed in Airflow 3

with DAG(
    dag_id="hello_airflow",
    start_date=days_ago(1),
    schedule_interval="@daily",                 # renamed to schedule= in Airflow 3
    catchup=False,
) as dag:

    @task
    def greet() -> str:
        return "hello"

    @task
    def shout(message: str) -> None:
        print(f"{message.upper()} from Airflow")

    shout(greet())
```

For an interview, the short version is: Airflow is an orchestrator (control plane), it models a pipeline as a DAG of idempotent tasks, and it separates scheduling from execution through executors and workers.

[Table of Contents](#Apache-Airflow)

## What problems does Airflow solve compared to cron?

Cron is a timer, not a workflow manager. It runs one command on a clock and forgets about it. Production pipelines need state, ordering, retries, and history.

| Problem | cron | Airflow |
|---|---|---|
| Dependencies between steps | shell scripts, lock files, `sleep 10m` | first-class `>>` dependencies and upstream/downstream task states |
| Failure handling | none, unless you write wrappers | per-task retries, exponential backoff, timeouts, callbacks |
| Backfills | hand-written loops | scheduler-managed backfills for a date range, one run per interval |
| Observability | grep logs across many hosts | UI and REST API with per-run and per-task state, logs, durations, Gantt |
| Reruns | ad hoc, usually unsafe | logical dates and partitioned outputs make reruns repeatable |
| Dynamic pipelines | crontab templating hacks | Python, dynamic task mapping, branching, sensors, assets |
| Access and audit | ssh and crontab files | roles, connections, variables, metadata-DB audit trail |

Concrete example: a nightly job must wait for a partner file, load it, run dbt, publish a report, and retry only the failed step when the warehouse times out. With cron you chain shell scripts and parse log files. In Airflow it is one DAG with a sensor, five tasks, retries, and an alert.

[Table of Contents](#Apache-Airflow)

## When should you not use Airflow?

Airflow is a batch orchestrator, so be honest about where it does not fit:

+ **Streaming**: Kafka, Flink, and Spark Structured Streaming process continuous events. Airflow can start and stop those jobs, but it should not be in the event path.
+ **Heavy data processing**: transformations belong in Spark, dbt, SQL, or a warehouse. Airflow tasks should trigger them, not reimplement them in a Python process.
+ **Long-running services**: an always-on API or a worker that runs for days is not a task. Deploy it as a service and orchestrate its lifecycle if needed.
+ **Sub-minute loops**: the scheduler is not designed for second-level scheduling. Use a stream processor or a real-time system.
+ **A single trivial cron job**: if one `curl` once a day is all you need, Airflow is operational overhead.
+ **Data movement at scale**: use Kafka, NiFi, or a managed transfer service; Airflow can trigger it.
+ **Notebook-style interactive work**: Airflow is for reproducible, scheduled pipelines, not exploratory analysis.

[Table of Contents](#Apache-Airflow)

## Explain how a workflow is designed in Airflow?

A workflow is a DAG: tasks are nodes, dependencies are edges, and cycles are not allowed. Designing one is really four decisions:

1. **Break the pipeline into units of work** that can fail and retry independently: extract one partition, validate one dataset, load one table, run one dbt selector.
2. **Wire the data flow** with `>>`, `<<`, `chain()`, or TaskFlow function arguments. Never model ordering with `sleep`.
3. **Make every task idempotent**, because Airflow will retry it, clear it, and backfill it. The same logical date may run many times.
4. **Choose the right granularity.** One task per row is an anti-pattern (thousands of scheduler rows); one task for the whole pipeline loses retry value. Batch with dynamic task mapping instead.

```python
from airflow.sdk import chain, task

# extract, validate, load, build_marts, and publish are task objects defined in this DAG
extract >> validate >> load
chain(load, build_marts, publish)      # equivalent to load >> build_marts >> publish

# branch at runtime
@task.branch
def choose_path(ds: str) -> str:
    return "full_refresh" if is_first_run(ds) else "incremental_load"
```

DAG structure is resolved when the DAG file is parsed, so anything dynamic must be expressed with dynamic task mapping or `@task.branch`, not with Python `if` around task definitions that change between runs.

[Table of Contents](#Apache-Airflow)

## Explain Airflow architecture and its components?

Airflow 3 has a small set of components, each a Python service you can scale or isolate:

+ **Scheduler** - reads serialized DAGs from the metadata database, creates DAG runs from the timetable, queues task instances, and reacts to completion events. The executor runs *inside* the scheduler process; it is a configuration choice, not a separate service.
+ **DAG processor** - parses DAG files from a DAG bundle and serializes them into the metadata database. In Airflow 3 it is a required standalone process, which also means it can be isolated from the scheduler for security.
+ **DAG bundle** - where DAG files come from: a local folder by default, or a git repository or object storage.
+ **API server** - serves the React UI and the REST API, and is the only component that talks to the metadata database on behalf of tasks and workers. It replaced the Flask webserver (`airflow api-server`, and the `[webserver]` config section became `[api]`).
+ **Metadata database** - Postgres or MySQL holding DAG, run, task, variable, connection, pool, and XCom state.
+ **Worker** (optional) - executes task instances. With `LocalExecutor` there is no separate worker process.
+ **Triggerer** (optional) - an asyncio event loop that runs deferred tasks (deferrable operators and sensors) without holding a worker slot.
+ **Plugins folder** (optional) - custom operators, hooks, timetables, and listeners loaded by the other components.

```text
  dags/*.py  --parse-->  DAG processor  --serialize-->  Metadata DB (Postgres/MySQL)
                                                             ^
                                                             |  API server is the only
                                                             |  DB access point for tasks
  Browser / CI / CLI  <--REST/UI-->  API server  <--Task Execution API--  Scheduler (+ executor)
                                                                              |
                                                                     queues task instances
                                                                              v
                                                       Workers (Celery / Kubernetes / Edge)
                                                       Triggerer (deferrable tasks)
```
Airflow 2 differences: the Flask webserver served the UI instead of the API server, task code ran with direct access to the metadata database, and the DAG processor was optional because the scheduler parsed DAG files by default.

The Airflow 3 security and scaling story is the key interview point: task code runs in a worker with the Task SDK and talks to the **Task Execution API** on the API server. It cannot import a database session or write to the metadata database, which removes a whole class of accidental (and malicious) access, cuts the number of direct database connections, and makes remote or edge execution possible.

[Table of Contents](#Apache-Airflow)

## What are the types of executors in Airflow?

An executor decides *where and how* queued task instances actually run. The executor is chosen with one config value:

```text
[core]
executor = LocalExecutor
# multiple executors at once (Airflow 2.10+); the first is the default
# executor = LocalExecutor,CeleryExecutor
```

```bash
airflow config get-value core executor
```

Airflow 3 executor landscape:

+ **LocalExecutor** - the default and the only executor shipped in `airflow-core`. Runs tasks as subprocesses inside the scheduler process on one machine. Simple, low latency, no extra infrastructure. It shares CPU and memory with the scheduler, so it is best for small to medium single-node deployments.
+ **CeleryExecutor** - a queued executor. Workers are long-lived and pull tasks from a broker such as Redis or RabbitMQ. Steady throughput and low queue latency, but you manage worker pools and the broker. Provider: `apache-airflow-providers-celery`.
+ **KubernetesExecutor** - a containerized executor. Every task starts in its own pod, created on demand. Best isolation, per-task images and resources (CPU, memory, GPU), at the cost of pod startup latency and cluster operations. Provider: `apache-airflow-providers-cncf-kubernetes`.
+ **EdgeExecutor** - runs tasks on remote or edge machines that cannot be reached by the scheduler. Provider: `apache-airflow-providers-edge3`.
+ **Provider executors** - cloud and ecosystem specific options such as `BatchExecutor` and `EcsExecutor` in the Amazon provider, and `DaskExecutor` in `apache-airflow-providers-daskexecutor`.
+ **SequentialExecutor** - existed in Airflow 2 for SQLite-based local development (one task at a time). It was **removed in Airflow 3**, along with the hybrid `LocalKubernetesExecutor` and `CeleryKubernetesExecutor`; use the comma-separated multi-executor config instead.

Do not confuse "executor" with "worker": the executor lives in the scheduler and decides how to run tasks; workers are the processes or pods that execute them, and only remote executors have them.

[Table of Contents](#Apache-Airflow)

## How do you choose an executor for a production workload?

Trade-offs are latency, isolation, and cost. Pick the simplest executor that meets your isolation and scale needs.

| Executor | Isolation | Startup latency | Best for | Watch out for |
|---|---|---|---|---|
| LocalExecutor | low (shared with scheduler) | none | single-node, moderate task volume, dev and staging | one machine to size and to lose; noisy neighbors |
| CeleryExecutor | medium (shared pool of workers) | low (workers are warm) | steady high volume, many similar small tasks | idle worker cost, noisy neighbors, broker to operate |
| KubernetesExecutor | high (one pod per task) | seconds to tens of seconds | heterogeneous dependencies, GPUs, bursty or untrusted workloads | pod startup adds latency for tiny tasks; cluster skills required |
| EdgeExecutor | high (runs on the edge host) | depends on the network | on-prem, factory, or remote sites behind NAT | connectivity and upgrade management |

Rules of thumb that work in real deployments:

+ Start with **LocalExecutor** on one VM. Move on when tasks compete with the scheduler or you need more than one machine.
+ Use **CeleryExecutor** when task volume is high and steady, dependencies are similar across tasks, and you want warm workers with the lowest queue latency.
+ Use **KubernetesExecutor** when tasks need different images, system libraries, GPU nodes, or hard resource isolation, and when workloads are bursty enough that always-on workers waste money.
+ Use **multiple executors** when a single answer is wrong: for example Celery for routine load tasks and Kubernetes for the occasional heavyweight Spark or ML task, selected per task with `executor="KubernetesExecutor"`.
+ Protect downstream systems with **pools** regardless of executor; the executor controls placement, not load on your warehouse.

[Table of Contents](#Apache-Airflow)

## What are the logical date and data interval of a DAG run?

`logical_date` (called `execution_date` before Airflow 2.2) identifies a run and is the anchor for `ds`, `ds_nodash`, the `run_id` timestamp, and templated values. The **data interval** (`data_interval_start`, `data_interval_end`) is the window of data the run covers, and it is defined by the timetable. Airflow 3 has two families of timetables, and the difference is a common interview trap:

+ **Trigger timetables** - `CronTriggerTimetable` and `DeltaTriggerTimetable`. There is no meaningful data interval: `data_interval_start` and `data_interval_end` are both the trigger time, and `logical_date` is that trigger time. **This is the Airflow 3 default** for a bare cron string or `timedelta` (`[scheduler] create_cron_data_intervals = False`).
+ **Data interval timetables** - `CronDataIntervalTimetable` and `DeltaDataIntervalTimetable`. This is the classic Airflow 2 behavior: for `@daily`, the interval runs midnight to midnight and the run is created when the interval ends. `logical_date` is the start of the interval, so it is one period behind the trigger time.

Airflow 2 defaulted to data intervals; Airflow 3 defaults to trigger timetables. The two anchor `logical_date` differently, so if your pipeline logic depends on interval semantics, **pin the timetable explicitly** instead of relying on the default:

```python
import pendulum
from airflow.sdk import CronDataIntervalTimetable, DAG

# Classic interval semantics: the run for the [Oct 3 02:00, Oct 4 02:00) window
# is created at Oct 4 02:00 and has logical_date = ds = 2026-10-03.
DAG(
    dag_id="daily_orders_pipeline",
    schedule=CronDataIntervalTimetable("0 2 * * *", timezone="UTC"),
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
)
```

Other facts that matter in practice:

+ `catchup` defaults to `False` in Airflow 3 (`[scheduler] catchup_by_default`). With `catchup=True`, the scheduler creates one run per missed interval between `start_date` and now.
+ For a manual trigger, the run's data interval may differ from the `logical_date` you supplied, so read `logical_date` explicitly when that is the value your logic needs.
+ Asset-triggered runs have no `logical_date`, so `ds` and `data_interval_start` are not available in them.
+ Pick a partition-key convention and encode it in code: `data_interval_start`/`data_interval_end` with a data interval timetable, or `logical_date` with a trigger timetable. Never `datetime.now()`.

[Table of Contents](#Apache-Airflow)

## How do you define a workflow in Airflow?

A DAG file should be a thin graph definition. Business logic lives in importable, unit-tested modules so the scheduler spends little time parsing and you can test the logic without Airflow.

```python
from datetime import timedelta

import pendulum
from airflow.sdk import DAG, task

# business logic in a versioned package, not in the DAG file
from acme.orders import land_partition, count_rows, merge_partition
from acme.dbt import run_dbt
from acme.alerts import notify_slack

with DAG(
    dag_id="daily_orders_pipeline",
    description="Land raw orders, validate, load, and publish marts",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="0 2 * * *",
    catchup=False,
    max_active_runs=1,
    default_args={
        "owner": "data-platform",
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "retry_exponential_backoff": True,
        "execution_timeout": timedelta(minutes=45),
    },
    tags=["orders", "tier-1"],
) as dag:

    @task
    def extract_orders(ds: str) -> str:
        return land_partition(f"s3://acme-raw/orders/ds={ds}/", table="stg_orders")

    @task
    def validate_orders(staging_path: str, ds: str) -> int:
        row_count = count_rows(staging_path)
        if row_count == 0:
            raise ValueError(f"orders partition for {ds} is empty")
        return row_count

    @task
    def load_orders(staging_path: str, ds: str) -> None:
        merge_partition(staging_path, target="analytics.orders", partition=ds)

    @task
    def build_marts(ds: str) -> None:
        run_dbt(select="tag:orders", vars={"ds": ds})

    @task
    def publish(ds: str) -> None:
        notify_slack(f"orders marts are ready for {ds}")

    staging = extract_orders()
    rows = validate_orders(staging)
    loaded = load_orders(staging)
    rows >> loaded >> build_marts() >> publish()
```

TaskFlow passes values between tasks for you: `validate_orders(staging)` receives the return value of `extract_orders`. Parameters named after context variables (`ds`, `ti`, `run_id`, ...) are injected by Airflow instead of being treated as inputs. With a plain cron schedule in Airflow 3, `ds` is the run's logical date, which for a trigger timetable is the time the run fires; use `CronDataIntervalTimetable` if the task must own a specific data window.

The same pipeline in Airflow 2 changes only the imports, the scheduling argument, and where the operators come from:

```python
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago

from acme.orders import land_partition, count_rows, merge_partition

with DAG(
    dag_id="daily_orders_pipeline",
    start_date=days_ago(1),
    schedule_interval="0 2 * * *",        # Airflow 2 spelling of schedule=
    catchup=False,
    max_active_runs=1,
    default_args={"owner": "data-platform", "retries": 3},
) as dag:

    @task
    def extract_orders(ds: str) -> str:
        return land_partition(f"s3://acme-raw/orders/ds={ds}/", table="stg_orders")

    @task
    def validate_orders(staging_path: str, ds: str) -> int:
        return count_rows(staging_path)

    @task
    def load_orders(staging_path: str, ds: str) -> None:
        merge_partition(staging_path, target="analytics.orders", partition=ds)

    staging = extract_orders()
    rows = validate_orders(staging)
    rows >> load_orders(staging)
```

[Table of Contents](#Apache-Airflow)

## How do you schedule a DAG in Airflow?

In Airflow 3 the single `schedule` argument accepts a cron expression, a `timedelta`, a preset, a timetable, a list of Assets, or `None` (the default). The old `schedule_interval` and `timetable` arguments from Airflow 2 are gone.

```python
from datetime import timedelta

import pendulum
from airflow.sdk import DAG
from airflow.timetables.trigger import CronTriggerTimetable

# A bare cron string or timedelta becomes a trigger timetable in Airflow 3.
with DAG(
    dag_id="daily_orders",
    schedule="0 2 * * *",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
):
    ...

# Other values accepted by schedule=
schedule_values = [
    timedelta(hours=6),                                              # every 6 hours
    "@daily",                                                        # preset
    CronTriggerTimetable("0 2 * * *", timezone="America/New_York"),  # explicit timezone
    None,                                                            # only triggered externally
]
```
The same schedules in Airflow 2:

```python
from datetime import timedelta

from airflow import DAG
from airflow.timetables.interval import CronDataIntervalTimetable

DAG(dag_id="cron_example", schedule_interval="0 2 * * *")            # daily at 02:00
DAG(dag_id="interval_example", schedule_interval=timedelta(hours=6))
DAG(dag_id="preset_example", schedule_interval="@daily")
DAG(dag_id="timetable_example", timetable=CronDataIntervalTimetable("0 2 * * *", timezone="UTC"))
DAG(dag_id="manual_example", schedule_interval=None)                 # only triggered externally
```

In Airflow 2, `schedule_interval=` and `timetable=` were separate arguments (mutually exclusive), and `catchup` defaulted to `True`.

Cron presets:

| Preset | Meaning | Cron |
|---|---|---|
| `None` | only external triggers | |
| `@once` | run once | |
| `@continuous` | run again as soon as the previous run finishes | |
| `@hourly` | once an hour at the end of the hour | `0 * * * *` |
| `@daily` | once a day at midnight | `0 0 * * *` |
| `@weekly` | once a week at midnight on Sunday | `0 0 * * 0` |
| `@monthly` | once a month on the first day | `0 0 1 * *` |
| `@quarterly` | once a quarter on the first day | `0 0 1 */3 *` |
| `@yearly` | once a year on January 1 | `0 0 1 1 *` |

The DAG's timezone comes from `start_date`; pass an explicit `timezone` to a timetable when the schedule must be pinned to a business timezone rather than the authoring machine. Remember that a bare cron string becomes a **trigger timetable** in Airflow 3, so `data_interval_start` and `data_interval_end` are equal unless you use a data interval timetable or set `[scheduler] create_cron_data_intervals = True`. Schedule changes only affect future intervals: Airflow 3 has DAG versioning, so already-created runs keep interpreting the DAG version they started with.

Operations you will use in practice:

```bash
airflow scheduler                     # run the scheduler process
airflow dags trigger daily_orders_pipeline
airflow dags pause daily_orders_pipeline
airflow dags next-execution daily_orders_pipeline
```

Airflow 3.3 introduces the `airflowctl` CLI for DAG operations and marks several `airflow dags ...` commands as deprecated in its favor (AIP-94); the classic commands still work.

[Table of Contents](#Apache-Airflow)

## Understanding cron expressions in Airflow

A cron expression has five fields separated by spaces:

| Field | Position | Allowed values | Description |
|---|---|---|---|
| Minute | 1 | `0-59` | minute of the hour |
| Hour | 2 | `0-23` | hour of the day |
| Day of month | 3 | `1-31` | day of the month |
| Month | 4 | `1-12` or `JAN-DEC` | month |
| Day of week | 5 | `0-6` or `SUN-SAT` | day of the week, `0` = Sunday |

Airflow parses cron with the **croniter** library, which supports an extended syntax. For example `0 0 * * MON#1` runs at midnight on the first Monday of the month.

Worked example, `30 8 * * 1-5`:

1. `30` - at minute 30.
2. `8` - during hour 8, so **08:30**.
3. `*` - every day of the month.
4. `*` - every month.
5. `1-5` - Monday through Friday, so weekends are skipped.

The schedule means "08:30 on weekdays" in the DAG's timezone. A real use case is an operational report that must reach the business before the workday starts: a DAG with `schedule="30 8 * * 1-5"` aggregates the previous day's data, renders a report, and posts it to Slack; the same DAG can be paused on public holidays or guarded with a holiday check.

Because the default cron timetable is a trigger timetable, the run created at Tuesday 08:30 has `logical_date = 2026-10-06 08:30` and `ds = 2026-10-06`, even though the report content is about October 5. Be explicit about which date the pipeline uses: `ds` identifies the run, not necessarily the data window. Use `CronDataIntervalTimetable` if you want the run to own an interval that ends at the trigger time.

[Table of Contents](#Apache-Airflow)

## How do you pass data between tasks with XComs?

XCom (**cross-communication**) is a small key/value record written to the metadata database and scoped to a DAG run. In Airflow 3 a TaskFlow task pushes its return value automatically under the key `return_value`, and downstream tasks can receive it as a function argument:

```python
from airflow.sdk import task

@task
def extract_orders(ds: str) -> dict:
    uri = f"s3://acme-staging/orders/ds={ds}/orders.parquet"
    upload_partition("s3://acme-raw/orders", uri)
    return {"uri": uri, "row_count": 120345}      # pushed to XCom automatically

@task
def load_orders(payload: dict) -> None:
    merge_from(uri=payload["uri"], target="analytics.orders")   # pulled automatically
```

You can also push and pull explicitly with the task instance:

```python
from airflow.sdk import task

@task
def load_orders(ds: str, **context) -> None:
    ti = context["ti"]
    staging_path = ti.xcom_pull(task_ids="extract_orders", key="return_value")
    ti.xcom_push(key="loaded_partition", value=ds)
    merge_from(uri=staging_path, target="analytics.orders")
```
The same explicit pull in Airflow 2 could omit `task_ids`, which searched every task in the run:

```python
from airflow.decorators import task

@task
def load_orders(ds: str, **context) -> None:
    ti = context["ti"]
    staging_path = ti.xcom_pull(key="return_value")   # task_ids was optional in Airflow 2
    merge_from(uri=staging_path, target="analytics.orders")
```

Use `@task(multiple_outputs=True)` when a task returns a dict and you want each key pushed as its own XCom instead of one `return_value`.

Rules that matter in production:

+ XComs are for **metadata**, not data. A path, a row count, a status, or a small config object is fine; a million-row DataFrame is not.
+ Large payloads belong in object storage. Write the file to S3/GCS/ADLS and pass the URI; the task that reads it fetches only what it needs. `airflow.sdk.ObjectStoragePath` helps keep those paths typed, and an object-storage XCom backend is an option if metadata volume grows.
+ XComs live in the metadata database and are removed when the task instance is cleared for a retry, so they are not durable state. Persist anything you cannot recompute.
+ XComs are per DAG run by default. Pulling from another run requires `include_prior_dates` or an explicit `dag_id`/`run_id`.
+ Since Airflow 3, `xcom_pull` requires `task_ids` when you pull by key; the old behavior of searching every task is gone.

[Table of Contents](#Apache-Airflow)

## What is xcom_pull in Airflow?

`xcom_pull` reads a value that another task instance pushed, and `xcom_push` writes one. If you do not pass a `key`, `xcom_pull` defaults to `return_value`, which is the key every operator and `@task` function uses when it auto-pushes its result.

```python
@task
def merge_table(**context) -> None:
    ti = context["ti"]

    # return value of a task in the same DAG run (key defaults to "return_value")
    table_name = ti.xcom_pull(task_ids="pick_table")

    # a named value pushed with xcom_push
    row_count = ti.xcom_pull(task_ids="extract_orders", key="row_count")

    # look at earlier DAG runs as well
    previous_watermark = ti.xcom_pull(task_ids="extract_orders", include_prior_dates=True)

    # one instance of a dynamically mapped task
    first_partition = ti.xcom_pull(task_ids="process_partition", map_indexes=0)
```

Key points:

+ The pull is resolved at runtime, so the upstream task must already have run in that DAG run unless you opt into prior dates.
+ `task_ids` is required when pulling by key. Pulling a default `return_value` without `task_ids` is ambiguous and no longer searches every task.
+ Dynamic task mapping produces several XComs under one `task_id`; index them with `map_indexes`.
+ Prefer passing XComArg values between TaskFlow functions over hand-written `xcom_pull` when both tasks are in the same DAG, because the dependency is then explicit in the graph.

[Table of Contents](#Apache-Airflow)

## What are Jinja templates?

Jinja is the templating engine Airflow uses to render task arguments at runtime. Operators declare which arguments are templated through `template_fields` - for example `BashOperator` templates `bash_command`, `env`, and `cwd`, while `SQLExecuteQueryOperator` templates `sql`, `parameters`, `conn_id`, `database`, and `hook_params`.

Frequently used context variables:

| Variable | Meaning |
|---|---|
| `ds`, `ds_nodash` | logical date as `YYYY-MM-DD` / `YYYYMMDD` |
| `data_interval_start`, `data_interval_end` | interval boundaries (timezone-aware) |
| `run_id` | unique run identifier, including manual and scheduled runs |
| `dag_run.conf` | JSON config passed to a manual or triggered run |
| `params` | DAG-level or task-level parameters |
| `ti` | task instance, for `xcom_pull` inside a template |
| `var.value`, `conn` | Variables and Connections |

A templated bash command:

```python
from airflow.providers.standard.operators.bash import BashOperator

export_partition = BashOperator(
    task_id="export_partition",
    bash_command="python /opt/airflow/scripts/export.py --date {{ ds }} --run-id {{ run_id }}",
)
```
In Airflow 2 the same operator is imported from core instead of a provider:

```python
from airflow.operators.bash import BashOperator
```

A templated SQL statement:

```python
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

insert_partition = SQLExecuteQueryOperator(
    task_id="insert_orders_partition",
    conn_id="warehouse",
    sql="""
        DELETE FROM analytics.orders WHERE ds = '{{ ds }}';
        INSERT INTO analytics.orders
        SELECT * FROM staging.orders
        WHERE ds = '{{ ds }}';
    """,
)
```

Two caveats:

+ Asset-triggered runs have no `logical_date`, so `ds` and `data_interval_start` are not available and a template that uses them fails. Pass the needed value through `dag_run.conf` or task params instead.
+ Never interpolate user-supplied values such as `dag_run.conf` straight into a shell command. Jinja does not sanitize the output, so a manual trigger can become shell injection. Pass values through the `env` argument instead:

```python
from airflow.providers.standard.operators.bash import BashOperator

BashOperator(
    task_id="say_hello",
    bash_command='echo "hello $name"',
    env={"name": '{{ dag_run.conf["name"] }}'},
)
```

[Table of Contents](#Apache-Airflow)

## How do you use Airflow XComs in Jinja templates?

Templates can call `ti.xcom_pull` while rendering, which is useful when a value decides the SQL or command to run. The example below reads a table name that an upstream task discovered and uses it to build the query:

```python
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

count_rows = SQLExecuteQueryOperator(
    task_id="count_rows",
    conn_id="warehouse",
    sql="SELECT COUNT(*) FROM {{ ti.xcom_pull(task_ids='pick_table', key='table_name') }};",
)
```

Two cautions: the upstream task must have run before rendering, so the dependency has to exist in the graph (`pick_table >> count_rows`), and templating a pull adds a metadata-database round trip at render time. When the value is only needed by Python code, plain `xcom_pull` in the task body is simpler and easier to test.

[Table of Contents](#Apache-Airflow)

## How do you build dynamic pipelines with dynamic task mapping?

Dynamic task mapping creates one task instance per item **at runtime**, so DAGs can react to how many files or partitions actually exist. Combine `.partial()` for fixed arguments with `.expand()` for the list, and Airflow derives the dependencies.

```python
from airflow.sdk import task

@task
def list_new_files(ds: str) -> list[str]:
    return discover(f"s3://acme-landing/partners/ds={ds}/")

@task
def validate_file(path: str) -> str:
    assert_file_is_readable(path)
    return path

@task
def load_file(path: str, target_table: str) -> None:
    load(path, target_table)

files = list_new_files()
validate_file.partial().expand(path=files)
load_file.partial(target_table="raw.partner_feed").expand(path=files)
```

Notes from real pipelines:

+ A zero-length expansion is skipped automatically, which is how "no files today" becomes a successful no-op instead of a failure.
+ Use `expand_kwargs([{"path": "a.csv", "table": "orders"}, {"path": "b.csv", "table": "returns"}])` when each mapped instance needs a different combination of arguments.
+ Every mapped instance is a task instance in the database, and `[core] max_map_length` defaults to 1024, so keep batches reasonable. Map over files, partitions, or tables, not over individual rows.
+ Cap parallel copies with `max_active_tis_per_dag` and a pool when mapped tasks all hit the same system.
+ Mapping does not replace partitioning: the mapped tasks should still write to partition-scoped paths so a retry of one item is safe.

Dynamic task mapping exists since Airflow 2.3 and the API is identical. Only the TaskFlow import changes: Airflow 2 uses `from airflow.decorators import task`, while Airflow 3 uses `from airflow.sdk import task`.

[Table of Contents](#Apache-Airflow)

## How do you make a DAG data-aware with Assets?

Airflow 3 renamed **Datasets** to **Assets**. An Asset is a logical piece of data (a table, an S3 prefix, a Kafka topic). A task declares that it produces one with `outlets`, and another DAG can be scheduled on it instead of on the clock.

```python
import pendulum
from airflow.sdk import Asset, DAG, task

orders_asset = Asset("s3://acme-curated/orders")

with DAG(
    dag_id="orders_transform",
    schedule="0 3 * * *",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
) as transform_dag:

    @task(outlets=[orders_asset])
    def build_orders_asset(ds: str) -> None:
        run_dbt(select="fct_orders", vars={"ds": ds})


with DAG(
    dag_id="orders_dashboard_refresh",
    schedule=[orders_asset],        # run when the asset is updated
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
) as dashboard_dag:

    @task
    def refresh_dashboard() -> None:
        refresh_bi_extract()
```
Airflow 2.4 to 2.11 used `Dataset` for the same job, with the same `outlets` and `schedule=[...]` API:

```python
import pendulum
from airflow import DAG, Dataset
from airflow.decorators import task

orders_asset = Dataset("s3://acme-curated/orders")

with DAG(
    dag_id="orders_transform",
    schedule="0 3 * * *",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
) as dag:

    @task(outlets=[orders_asset])
    def build_orders_asset(ds: str) -> None:
        run_dbt(select="fct_orders", vars={"ds": ds})
```

There is also a single-task shorthand, `@asset(schedule="@daily")` on a decorated function, which creates the Asset, the task, and its DAG in one go. Assets can be used as task `inlets` to declare what a task consumes.

Why this matters: the downstream pipeline no longer guesses. It runs because the upstream data actually landed, which removes brittle `ExternalTaskSensor` wiring and long polling. Airflow 3.2 added asset **partitioning**, so only the partition that changed triggers downstream work, and asset aliases let several producers satisfy one logical input.

Good candidates for asset triggers: a dbt model finishing, a partition landing in the lake, a partner feed arriving. Keep time-based schedules for "run every day at 02:00" and use assets for "run when this data exists". Remember that asset-triggered runs have no logical date, so they cannot use `ds`.

[Table of Contents](#Apache-Airflow)

## How do you wait for external data with sensors and deferrable operators?

Sensors wait for a condition to become true. They differ mainly in how they use resources:

+ `mode="poke"` (default) keeps a worker slot while it waits.
+ `mode="reschedule"` releases the slot between checks and reschedules the task, which is what you want for anything that may wait more than a few minutes.
+ **Deferrable** sensors and operators (`deferrable=True`, `...Async` variants, or `@task.sensor`) hand the wait to the **triggerer**, which can hold thousands of waits in one asyncio loop. They require a triggerer component.

Real-world pattern: wait for a partner file marker, then process whatever arrived.

```python
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

wait_for_partner_file = S3KeySensor(
    task_id="wait_for_partner_file",
    bucket_name="acme-landing",
    bucket_key="partners/ds={{ ds }}/_SUCCESS",
    poke_interval=60,
    timeout=60 * 60 * 6,          # always bound the wait
    mode="reschedule",
)
```

The same wait as a deferrable TaskFlow sensor:

```python
from airflow.sdk import task

@task.sensor(poke_interval=60, timeout=3600, mode="reschedule")
def wait_for_partner_file(ds: str) -> bool:
    return object_exists(f"s3://acme-landing/partners/ds={ds}/_SUCCESS")
```
The Airflow 2 version of the deferrable wait uses the TaskFlow sensor decorator from `airflow.decorators`; provider sensors such as `S3KeySensor` also accept `deferrable=True` (deferrable operators arrived in Airflow 2.2 and need a triggerer):

```python
from airflow.decorators import task

@task.sensor(poke_interval=60, timeout=3600, mode="reschedule")
def wait_for_partner_file(ds: str) -> bool:
    return object_exists(f"s3://acme-landing/partners/ds={ds}/_SUCCESS")
```

Pick the right mechanism:

+ Waiting for a **file or object**: object-store sensors (S3/GCS/ADLS), with `deferrable=True` when the provider supports it.
+ Waiting for **another DAG**: asset-triggered scheduling first; `ExternalTaskSensor` only when you need the other DAG's run to complete.
+ Waiting for a **time**: `DateTimeSensor` / `DateTimeSensorAsync` instead of `sleep`.
+ Waiting for a **queue or API**: a custom deferrable trigger.

Always set a `timeout`, decide whether a timeout is a failure or a skip, and prefer an event-driven asset trigger when the upstream system can emit one. Airflow 3.3 also adds **resumable tasks**: the task state store can checkpoint progress or an external job id so a retry resumes instead of re-submitting work, which is valuable for long Spark or ML runs.

[Table of Contents](#Apache-Airflow)

## How do Airflow backfills differ from normal scheduled runs?

A scheduled run processes the current interval. A **backfill** creates runs for historical intervals and can do many of them at once. Use it after a bug fix, a late source system, or a schema change that needs reprocessing.

Airflow 3 backfills are scheduler-managed and available from the CLI, the REST API, and the UI. The Airflow 2 command `airflow dags backfill` is gone:

```bash
airflow backfill create \
  --dag-id daily_orders_pipeline \
  --from-date 2026-09-01 \
  --to-date 2026-09-30 \
  --reprocess-behavior failed \
  --max-active-runs 3 \
  --run-backwards \
  --dry-run
```

+ `--reprocess-behavior` chooses what to do when a run already exists: `none` (the default, never recreate), `failed` (recreate failed runs), or `completed` (recreate failed and successful runs). A run that is still queued or running is never duplicated.
+ `--max-active-runs` caps how many backfill runs execute at once, independently of the DAG's own `max_active_runs`. Use it to protect the warehouse.
+ `--run-backwards` processes the most recent interval first.
+ `--dry-run` prints the intervals that would be created before you create them.
+ Partitioned DAGs are detected automatically; `--from-date`/`--to-date` are interpreted as partition dates.
+ In the UI, open the DAG and choose Trigger -> Backfill, where the same options appear as Missing Runs, Missing and Errored Runs, or All Runs.
The Airflow 2 equivalent of the same backfill:

```bash
airflow dags backfill \
  --start-date 2026-09-01 \
  --end-date 2026-09-30 \
  daily_orders_pipeline
```

Backfills are only safe when tasks are idempotent and partition-aware. A task that appends to a shared table without a partition key will double-count data, and 30 parallel runs will reproduce that mistake 30 times. Concurrency controls, pools, and a lower `--max-active-runs` are the practical guardrails.

[Table of Contents](#Apache-Airflow)

## How do you make tasks idempotent and safe to retry?

Airflow retries tasks, clears them, and backfills them; assume every task can run more than once for the same logical date. Idempotency is the property that makes those reruns safe.

Rules that work in production:

+ **One task, one partition.** Read `s3://raw/orders/ds={{ ds }}/` and write `s3://curated/orders/ds={{ ds }}/`, so the run owns its slice of data.
+ **Prefer merge or partition replace over blind append.** `MERGE` on a stable business key, or delete the partition and insert it again.
+ **Never use `datetime.now()` for business logic.** Use `ds`, `data_interval_start`, or `data_interval_end`.
+ **Make external side effects idempotent** with an idempotency key, or check "already done" before calling a non-idempotent API.
+ **Stage then swap** when atomicity matters: write to a temporary table or path, validate, then replace the target in one statement.
+ **Set `catchup=False`** for pipelines that genuinely cannot be replayed, and use backfills deliberately instead.

```sql
-- idempotent partition load: rerunning this for the same ds is safe
DELETE FROM analytics.orders WHERE ds = '{{ ds }}';

INSERT INTO analytics.orders
SELECT *
FROM staging.orders
WHERE ds = '{{ ds }}';
```

A useful interview answer: "I make the logical date part of the data contract. If the same `ds` is processed twice, the second run overwrites exactly what the first one wrote, so a retry, a clear, and a backfill all converge to the same state."

[Table of Contents](#Apache-Airflow)

## How do you handle retries, timeouts, and alerts?

Set reliability policy in `default_args` and override it per task when the task differs. Retry transient failures, fail fast on data errors, and bound every task in time.

```python
from datetime import timedelta

import pendulum
from airflow.sdk import AsyncCallback, DAG, DeadlineAlert, DeadlineReference

def alert_on_failure(context) -> None:
    notify_pagerduty(f"task {context['task_instance'].task_id} failed")

with DAG(
    dag_id="daily_orders_pipeline",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="0 2 * * *",
    default_args={
        "retries": 4,
        "retry_delay": timedelta(minutes=2),
        "retry_exponential_backoff": True,
        "max_retry_delay": timedelta(minutes=30),
        "execution_timeout": timedelta(hours=1),
        "on_failure_callback": alert_on_failure,
    },
    # Airflow 3.1+ replaced SLA with Deadline Alerts (experimental):
    # alert when the run has not finished 6 hours after it was queued
    deadline=DeadlineAlert(
        reference=DeadlineReference.DAGRUN_QUEUED_AT,
        interval=timedelta(hours=6),
        callback=AsyncCallback(alert_on_failure),
    ),
) as dag:
    ...
```
The Airflow 2 equivalent was an SLA with a miss callback:

```python
import pendulum
from datetime import timedelta

from airflow import DAG

# def alert_on_missed_sla(dag, task_list, blocking_task_list, slas, blocking_tis): ...

DAG(
    dag_id="daily_orders_pipeline",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    default_args={
        "sla": timedelta(hours=6),
        "sla_miss_callback": alert_on_missed_sla,
    },
)
```

Guidance:

+ Retry what is transient: network errors, warehouse contention, rate limits, a lock timeout. Do not retry a schema mismatch or a business-rule validation failure; retries just delay the alert. Airflow 3.3 also supports a per-exception `retry_policy` when different errors need different treatment.
+ Use `retry_exponential_backoff` and `max_retry_delay` to avoid hammering a struggling system.
+ Set `execution_timeout` on tasks and `timeout` on sensors so a stuck task cannot hold a worker slot forever.
+ Put alerting in callbacks (`on_failure_callback`, `on_retry_callback`, `on_execute_callback`, `on_success_callback`) or in a Notifier so every DAG reports consistently. Note that `on_success_callback` does not fire for skipped tasks.
+ In Airflow 2, alerting used `sla=` and `sla_miss_callback`; **SLA was removed in Airflow 3** and replaced in 3.1 by **Deadline Alerts**, which watch a reference point (for example `DAGRUN_QUEUED_AT`) plus an interval and fire a callback. They are the operational answer to "the 06:00 report must exist by 07:00".
+ Monitor the pipeline itself, not only tasks: task duration trends, queue time, scheduler heartbeat, and pool usage catch slow degradation before it becomes an incident.

[Table of Contents](#Apache-Airflow)

## How do you control concurrency with pools and DAG limits?

Airflow has several independent limits; know which one you are reaching for.

| Control | Scope | Typical use |
|---|---|---|
| `parallelism` | whole Airflow instance | cap total running task instances to fit the workers or the database |
| `max_active_tasks` | per DAG | cap tasks running at once in one DAG (was `concurrency`) |
| `max_active_runs` | per DAG | keep runs ordered or avoid two runs writing the same target |
| `max_active_tis_per_dag` | per task | stop one task from flooding a system (was `task_concurrency`) |
| `pool` + `pool_slots` | named, cross-DAG | protect a warehouse, an API, or a shared cluster |
| `queue` | Celery workers | route tasks to specific worker pools |
| `priority_weight` | task | bias the scheduler when many tasks are ready |

Pools are the most useful tool for data engineers because they express a business constraint: at most N queries against Snowflake, at most M calls to a vendor API. The built-in `default_pool` has 128 slots; create named pools for anything that can be overloaded.

```python
@task(pool="snowflake_etl", pool_slots=2)
def run_heavy_query() -> None:
    execute_query(...)
```
The pool mechanics are the same in Airflow 2; only the two task-level names changed (`concurrency` became `max_active_tasks`, and `task_concurrency` became `max_active_tis_per_dag`).

Two habits that prevent incidents: set `max_active_runs=1` on DAGs whose tasks write to a shared target unless you have proven parallel runs are safe, and size pools from the downstream system's limits rather than from Airflow's capacity. During a backfill, pool slots and `--max-active-runs` are what keep 30 concurrent runs from becoming an outage.

[Table of Contents](#Apache-Airflow)

## How do you design an Airflow DAG for a production data pipeline?

A production DAG is deterministic, idempotent, observable, and cheap to retry. The checklist below is what senior engineers actually review:

+ **Idempotent and partition-scoped tasks.** Same logical date in, same output out, no matter how many times it runs.
+ **Thin DAG files.** No heavy imports or API calls at module scope; logic lives in versioned, unit-tested modules. Parse time is a shared resource.
+ **Clear task boundaries.** One unit of work per task, with dynamic task mapping for fan-out instead of thousands of static tasks.
+ **Explicit dependencies.** Data flow in the graph, not in `sleep` or in filesystem polling.
+ **Reliability policy.** `retries`, backoff, `execution_timeout`, callbacks, and a Deadline Alert for tier-1 pipelines.
+ **Deliberate concurrency.** `max_active_runs`, pools, and `pool_slots` chosen from downstream limits.
+ **Configuration outside code.** Connections, Variables, and `params` for environment-specific values; secrets from a secrets backend rather than DAG source.
+ **Operability metadata.** `owner`, `description`, `tags`, `docs`, a `doc_md`, and a runbook link so an on-call engineer can act without reading the code.
+ **Safe change management.** Airflow 3 keeps DAG versions, so in-flight runs keep the version they started with; test the new version in staging and use `ruff` AIR301/AIR302 rules to catch Airflow 2 patterns before they reach production.
+ **Tests and monitoring.** Structure tests in CI, `dag.test()` locally, and dashboards for duration, queue time, and failures.

Tier the work explicitly. A tier-1 pipeline that feeds finance gets `max_active_runs=1`, retries, a deadline, and a paging alert; a tier-3 experimental DAG can run with defaults and a Slack message. Not every DAG deserves the same ceremony.

[Table of Contents](#Apache-Airflow)

## How do you test Airflow DAGs before deploying them?

Test at three levels: DAG structure, business logic, and the real path against a dev environment.

```python
# tests/test_dag_structure.py
from airflow.models.dagbag import DagBag

def test_dags_import_without_errors():
    bag = DagBag(dag_folder="dags", include_examples=False)
    assert bag.import_errors == {}
    assert "daily_orders_pipeline" in bag.dag_ids

def test_orders_pipeline_shape():
    dag = DagBag(dag_folder="dags", include_examples=False).get_dag("daily_orders_pipeline")
    assert dag.max_active_runs == 1
    assert dag.get_task("load_orders").upstream_task_ids == {"validate_orders"}

def test_task_logic():
    # business logic is imported from your package, so it can be tested without Airflow
    assert count_rows("tests/data/orders.parquet") == 3
```
`DagBag`, `airflow tasks test`, and `airflow dags list-import-errors` work the same way in Airflow 2; `dag.test()` was added in Airflow 2.5.

Other tools in the toolbox:

+ `dag.test()` runs a DAG in a single process with a database connection, which is the fastest way to debug a DAG end to end (`python dags/daily_orders_pipeline.py` with `if __name__ == "__main__": dag.test()`).
+ `airflow tasks test <dag_id> <task_id> <logical_date>` runs one task without recording state.
+ `airflow dags list-import-errors` fails fast in CI when a DAG file cannot be parsed.
+ Run a DAG twice for the same `ds` in staging and assert row counts are unchanged; that is the idempotency test that catches the expensive bugs.
+ Use `ruff check --select AIR30 --preview` to detect removed Airflow 2 imports and arguments during migration.

[Table of Contents](#Apache-Airflow)

## How do you make a custom module available to Airflow if you are using Docker Compose?

There are two separate concerns: DAG files must be visible to the scheduler and workers, and Python dependencies must be importable by every component that executes or parses a DAG.

**1. Mount DAGs and plugins (development).**

```yaml
# docker-compose.override.yml
services:
  airflow-scheduler:
    volumes:
      - ./dags:/opt/airflow/dags
      - ./plugins:/opt/airflow/plugins
      - ./config:/opt/airflow/config
```

The Airflow 3 Compose stack runs the API server, scheduler, DAG processor, worker, and triggerer as separate services, so mount the same volumes into each one. Append `:z` to the bind mounts on SELinux hosts. Add your package on `PYTHONPATH` or install it, otherwise `from acme.orders import ...` works on your laptop and fails in the container.

**2. Build a custom image for dependencies (the correct production answer).**

```text
FROM apache/airflow:3.3.2

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -r /requirements.txt

# optional: bake DAGs and the internal package into an immutable image
COPY --chown=airflow:root dags/ /opt/airflow/dags/
COPY --chown=airflow:root acme_pipelines/ /opt/airflow/dags/acme_pipelines/
```

Pin the Airflow version in the same `pip install` as your requirements so pip does not resolve a different Airflow, and use the official constraints file. Then point every service at `image: acme/airflow:3.3.2` instead of the stock image.
The Airflow 2 base image is the same pattern with the final 2.x tag:

```text
FROM apache/airflow:2.11.2
```

**What not to do:** `_PIP_ADDITIONAL_REQUIREMENTS` installs packages when each container starts. It is convenient for a demo and unacceptable for production, because every restart reinstalls dependencies, startup time grows, and the version you tested can drift. The Compose quick-start also makes no security guarantees and is not a production deployment; the official production path is Kubernetes with the community Helm chart.

References: [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) and [Building the image](https://airflow.apache.org/docs/docker-stack/build.html).

[Table of Contents](#Apache-Airflow)

## How do the same pipelines look in Airflow 2 and Airflow 3?

Airflow 2 (final line 2.11.2) reached **end of life on April 22, 2026**, so new pipelines should target Airflow 3. In practice you still meet Airflow 2 code: legacy production DAGs, migration projects, and interviewers who learned Airflow before 3.0. The pairs below show the same idea in both versions so you can read either one.

### A minimal DAG

Airflow 3:

```python
import pendulum
from airflow.sdk import DAG, task

with DAG(
    dag_id="hello_airflow",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="@daily",                # unified scheduling field
    catchup=False,
) as dag:

    @task
    def greet() -> str:
        return "hello"

    greet()
```

Airflow 2:

```python
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago   # removed in Airflow 3

with DAG(
    dag_id="hello_airflow",
    start_date=days_ago(1),
    schedule_interval="@daily",        # renamed to schedule= in Airflow 3
    catchup=False,
) as dag:

    @task
    def greet() -> str:
        return "hello"

    greet()
```

### Scheduling and data intervals

Airflow 3:

```python
import pendulum
from airflow.sdk import CronDataIntervalTimetable, DAG

DAG(
    dag_id="daily_orders",
    schedule=CronDataIntervalTimetable("0 2 * * *", timezone="UTC"),
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
)
```

Airflow 2:

```python
import pendulum
from airflow import DAG
from airflow.timetables.interval import CronDataIntervalTimetable

DAG(
    dag_id="daily_orders",
    # schedule_interval= and timetable= were mutually exclusive
    timetable=CronDataIntervalTimetable("0 2 * * *", timezone="UTC"),
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
)
```

In Airflow 2 a bare cron string already meant a data interval timetable; in Airflow 3 it means a trigger timetable, so `data_interval_start == data_interval_end` unless you use `CronDataIntervalTimetable` or set `[scheduler] create_cron_data_intervals = True`.

### Operators

Airflow 3 moves the standard operators and sensors into a provider:

```python
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

run_export = BashOperator(task_id="run_export", bash_command="python export.py --date {{ ds }}")
```

Airflow 2 imports them from core:

```python
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

run_export = BashOperator(task_id="run_export", bash_command="python export.py --date {{ ds }}")
```

Airflow 3 moved these operators into the `apache-airflow-providers-standard` provider, and the old `airflow.operators.*` imports are deprecated; use the provider path in new code.

### XComs

Airflow 3 requires `task_ids` when you pull by key:

```python
@task
def load(**context) -> None:
    rows = context["ti"].xcom_pull(task_ids="extract_orders", key="row_count")
```

Airflow 2 could search every task in the run when `task_ids` was omitted:

```python
@task
def load(**context) -> None:
    # task_ids was optional in Airflow 2; it searched all tasks for the key
    rows = context["ti"].xcom_pull(key="row_count")
```

### Data-aware scheduling

Airflow 3 uses `Asset`:

```python
import pendulum
from airflow.sdk import Asset, DAG, task

orders = Asset("s3://acme-curated/orders")

@task(outlets=[orders])
def build_orders() -> None:
    ...

DAG(
    dag_id="publish_orders",
    schedule=[orders],
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
)
```

Airflow 2.4+ uses `Dataset`:

```python
import pendulum
from airflow import DAG, Dataset
from airflow.decorators import task

orders = Dataset("s3://acme-curated/orders")

@task(outlets=[orders])
def build_orders() -> None:
    ...

DAG(
    dag_id="publish_orders",
    schedule=[orders],
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
)
```

### Alerting when a run is late

Airflow 3 uses experimental Deadline Alerts:

```python
import pendulum
from datetime import timedelta

from airflow.sdk import AsyncCallback, DAG, DeadlineAlert, DeadlineReference

def alert_on_failure(context) -> None:
    notify_pagerduty("pipeline missed its deadline")

DAG(
    dag_id="daily_orders",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    deadline=DeadlineAlert(
        reference=DeadlineReference.DAGRUN_QUEUED_AT,
        interval=timedelta(hours=6),
        callback=AsyncCallback(alert_on_failure),
    ),
)
```

Airflow 2 used SLAs (removed in Airflow 3):

```python
import pendulum
from datetime import timedelta

from airflow import DAG

# def alert_on_missed_sla(dag, task_list, blocking_task_list, slas, blocking_tis): ...

DAG(
    dag_id="daily_orders",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    default_args={
        "sla": timedelta(hours=6),
        "sla_miss_callback": alert_on_missed_sla,
    },
)
```

### Backfill

Airflow 3:

```bash
airflow backfill create \
  --dag-id daily_orders \
  --from-date 2026-09-01 \
  --to-date 2026-09-30 \
  --reprocess-behavior failed
```

Airflow 2:

```bash
airflow dags backfill \
  --start-date 2026-09-01 \
  --end-date 2026-09-30 \
  daily_orders
```

### Services and deployment

Airflow 3 runs the API server, a required standalone DAG processor, and the scheduler as separate components:

```bash
airflow api-server                 # replaced: airflow webserver
airflow scheduler
airflow dag-processor              # required in Airflow 3
airflow db migrate                 # replaced: airflow db init / airflow db upgrade
```

Airflow 2 typically ran the webserver and scheduler, with DAG parsing inside the scheduler:

```bash
airflow webserver
airflow scheduler
airflow db init
# optional since 2.7: airflow dag-processor
```

The container base image changes the same way:

```text
# Airflow 3
FROM apache/airflow:3.3.2
```

```text
# Airflow 2 (final line, EOL)
FROM apache/airflow:2.11.2
```

### At a glance

| Concern | Airflow 2 | Airflow 3 |
|---|---|---|
| DAG import | `from airflow import DAG` | `from airflow.sdk import DAG` (legacy import still works) |
| Task decorator | `from airflow.decorators import task` | `from airflow.sdk import task` |
| Scheduling | `schedule_interval=` or `timetable=` | unified `schedule=` |
| Start date | `days_ago(n)` common | removed; use timezone-aware datetimes |
| Default schedule / catchup | daily / catchup on | `None` / catchup off |
| Cron data interval | data interval by default | trigger timetable by default |
| Standard operators | `airflow.operators.*` | `airflow.providers.standard.operators.*` |
| Data-aware scheduling | `Dataset` (2.4+) | `Asset` |
| Lateness alerting | `sla=` / `sla_miss_callback` | `deadline=DeadlineAlert(...)` |
| Local executor | `SequentialExecutor` with SQLite | `LocalExecutor` |
| UI and API | Flask webserver, REST API v1 | API server + React UI, REST API v2 |
| Backfill CLI | `airflow dags backfill` | `airflow backfill create` |
| Database setup | `airflow db init` / `airflow db upgrade` | `airflow db migrate` |
| Status | 2.11.2, EOL April 22, 2026 | 3.3.x, current |

[Table of Contents](#Apache-Airflow)

## What changed between Airflow 2 and Airflow 3?

The section above shows the code; this is the checklist version. Interviewers ask it to check whether you are current:

+ **Author from `airflow.sdk`.** `airflow.models.dag.DAG` still imports but warns, and core operators and sensors moved to `apache-airflow-providers-standard` (`BashOperator`, `PythonOperator`, `FileSensor`, ...), so `airflow.operators.*` imports are legacy.
+ **One scheduling field.** `schedule_interval` and the `timetable` argument are removed in favor of `schedule=`, and `days_ago()` is gone. `schedule` now defaults to `None`, and `catchup` defaults to `False`.
+ **Cron and timedelta default to trigger timetables**, so `data_interval_start == data_interval_end` unless you choose a data interval timetable or enable `create_cron_data_intervals`.
+ **Executor cleanup.** `SequentialExecutor` and `DebugExecutor` are removed; `airflow-core` ships only `LocalExecutor`, while Celery, Kubernetes, Edge, and Dask executors live in providers. Hybrid executors are replaced by the multi-executor config.
+ **API server replaces the Flask webserver** (`airflow api-server`, `[webserver]` becomes `[api]`), with a React UI and REST API v2.
+ **No metadata database access from task code.** Tasks use the Task SDK and the Task Execution API, which isolates them and enables remote, edge, and non-Python execution.
+ **Datasets are now Assets** (`airflow.datasets.*` becomes `airflow.sdk.*`), with partition-aware scheduling since 3.2.
+ **SLA was removed**; Deadline Alerts arrived in 3.1 as the replacement and are still experimental.
+ **DAG versioning and a standalone DAG processor** are standard, which also means in-flight runs keep the DAG version they started with.
+ **CLI and API renames** such as `airflow dags backfill` to `airflow backfill create`, `airflow db init`/`upgrade` to `airflow db migrate`, and `airflow webserver` to `airflow api-server`.
+ **DAG code that no longer works**: SubDAGs, pickling, `fail_stop` (renamed `fail_fast`), the `execution_date` and `conf` context variables, `xcom_pull` without `task_ids`, and future logical dates.
+ **Migration tooling**: `ruff check --select AIR30 --preview` flags Airflow 2 patterns, and `airflow config lint` plus `airflow config update` help move configuration.

[Table of Contents](#Apache-Airflow)

## Real world use cases for Airflow

### 1. Nightly e-commerce ELT (batch, tier-1)

Raw order events land in object storage; a DAG validates the partition, merges it into the warehouse, runs dbt marts, publishes a report, and alerts if the marts are not ready by 06:00.

```text
extract_orders (ds partition) -> validate_orders (row count, schema)
    -> load_orders (MERGE on order_id) -> build_marts (dbt) -> publish (Slack + BI)
```

Why Airflow: partitioned, idempotent steps; retries only the failed step; `catchup=True` plus scheduler-managed backfills to reprocess September after a pricing bug; `max_active_runs=1` so two runs never write the same target; a Deadline Alert at 06:00.

### 2. Hourly CDC ingestion into a lakehouse

Debezium writes change events to Kafka, a sink lands micro-batches in the lake, and an Airflow DAG per source table compacts and merges them into Iceberg or Delta. The table list is dynamic, so the DAG maps over it.

```python
tables = list_changed_tables()
merge_table.partial(target_format="iceberg").expand(table=tables)
```

Why Airflow: Airflow does not consume the stream; it owns the micro-batch merge, deduplication, and compaction cadence. A pool caps how many merges hit the catalog at once, and each mapped task is independently retryable.

### 3. Partner file drop pipeline (event-driven)

A partner uploads a daily CSV and a `_SUCCESS` marker. A reschedule-mode or deferrable sensor waits without holding a worker slot, then the DAG validates the schema and maps over every file in the delivery.

```python
files = list_delivered_files(ds)
validate_file.expand(path=files)
load_file.partial(target_table="raw.partner_feed").expand(path=files)
```

Why Airflow: late files are normal, so the sensor has a timeout and an alert; zero files is a successful no-op; a failed file can be retried without reloading the whole delivery.

### 4. Feature refresh and model retraining

Feature tables are materialized as Assets. A training DAG is scheduled on `[feature_asset]` rather than on the clock, runs on KubernetesExecutor with a GPU node selector and a per-task image, and registers the model artifact. A Deadline Alert fires if training misses the morning release window.

Why Airflow: data-aware scheduling means training runs on fresh features, not on a hopeful fixed time; Kubernetes isolation gives the training task its own image and GPU; resumable tasks in 3.3 let a retried training job resume instead of starting over.

### 5. Business-hours operational report

A DAG on `30 8 * * 1-5` aggregates the prior day's revenue, renders a workbook, and emails it to the operations team in the DAG's timezone.

Why Airflow: cron could run the script, but it could not rerun just the failed step, skip holidays, retry the warehouse query, page the on-call engineer when the report is late, or show the business exactly which run produced the numbers.

[Table of Contents](#Apache-Airflow)

## How does Airflow compare with cron, dbt, and Spark?

They solve different problems, and mature platforms use all of them.

| Tool | Role | What it does | What it does not do |
|---|---|---|---|
| cron | timer | runs a command on a clock | dependencies, retries, state, backfills, visibility |
| Airflow | orchestrator (control plane) | schedules, sequences, retries, backfills, and monitors work across systems | process data at scale or consume streams |
| dbt | transformer | builds a SQL model DAG with tests, docs, and lineage inside the warehouse | schedule across systems, wait for files, or orchestrate non-SQL work |
| Spark | compute engine | distributed batch or streaming data processing | scheduling, dependencies across systems, alerting |
| Kafka / Flink | streaming data plane | continuous ingestion and processing of events | batch orchestration and historical backfills |

The practical arrangement: Airflow triggers, dbt transforms, Spark computes, and Kafka streams. dbt also has its own DAG, which is exactly why Airflow usually runs `dbt build` as one or a few steps of a bigger pipeline. In an interview, frame it as "Airflow is the control plane; dbt, Spark, and Kafka are the data plane", and mention alternatives (Dagster, Prefect, Argo Workflows, managed services such as MWAA, Cloud Composer, or Astronomer) only to show you know the landscape.

[Table of Contents](#Apache-Airflow)
