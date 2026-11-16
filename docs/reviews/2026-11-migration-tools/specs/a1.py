import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from af_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/airflow/airflow-01-test-a-dag.ipynb"
SPEC = """%% md
# Airflow 1: Write and test a DAG

An Airflow DAG is Python that declares tasks and the order they run in. This lab writes DAGs with the TaskFlow API
and runs them for real: passing data between tasks, fanning out over a list with dynamic task mapping, recovering
from a transient failure with retries, choosing what runs after a failure with trigger rules, and catching broken DAG
files before they reach a scheduler.

@@INTRO@@

@@SETUP_PIP@@
%% md
## Setup and sample data

The next cell creates an Airflow home in a temporary folder and initializes its metadata database. It defines
`run_dag_file`, which writes a DAG file and runs it, printing only the lines the DAG marks with `LAB`, and a small
`report` module the DAGs import to print every task instance's final state. Each DAG builds its own sample data.

@@HELPERS@@
%% md
## Tasks, dependencies and XCom

With the TaskFlow API, a task is a Python function decorated with `@task`, and the DAG is a function decorated with
`@dag`. Calling one task with another's result does two things: it makes the second task depend on the first, and it
passes the return value between them through **XCom**, Airflow's store for small task results.

`dag.test()` runs every task in dependency order inside the current process, which is how you check a DAG on a
laptop or in CI.

**Where it matters**

Most pipelines are a chain of extract, transform and load steps. Writing them as separate tasks lets Airflow retry,
time and alert on each step on its own.

**Watch out for**

XCom lives in the metadata database, so it is for small values: row counts, file paths, IDs. Passing a whole dataset
through XCom slows the scheduler and can exceed size limits; write data to storage and pass its location.
%% code
run_dag_file("orders_pipeline.py", '''
from datetime import datetime, timezone

from airflow.sdk import dag, task
from lab_report import report


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc))
def orders_pipeline():
    @task
    def extract():
        return [{"id": 1, "cents": 1200}, {"id": 2, "cents": 800}, {"id": 3, "cents": -50}]

    @task
    def clean(orders):
        valid = [order for order in orders if order["cents"] >= 0]
        print(f"LAB clean kept {len(valid)} of {len(orders)} orders")
        return valid

    @task
    def load(orders):
        print("LAB load wrote revenue:", sum(order["cents"] for order in orders))

    load(clean(extract()))


pipeline = orders_pipeline()

if __name__ == "__main__":
    report(pipeline.test())
''')
%% md
**What to notice:** The three tasks ran in the order their calls implied, and each received the previous task's
return value through XCom: `clean` dropped the negative order and `load` summed the remaining 2,000 cents. Every task
succeeded on its first try.
%% md
## Dynamic task mapping

Often the number of things to process is known only at run time: the files that landed today, the tables in a
schema. `.expand()` creates one **mapped task instance** per item of a list, each with its own state, retries and
logs, and a downstream task that takes the mapped results receives them all as a list.

**Where it matters**

Processing each landed file, partition or customer as its own task instance means one bad file fails one instance,
and a retry re-runs only that instance.

**Watch out for**

Thousands of mapped instances put real load on the scheduler and database. Batch small items together, and cap
parallelism with `max_active_tis_per_dag` or a pool so a big day does not swamp the warehouse.
%% code
run_dag_file("daily_files.py", '''
from datetime import datetime, timezone

from airflow.sdk import dag, task
from lab_report import report


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc))
def daily_files():
    @task
    def list_files():
        return ["orders_eu.csv", "orders_us.csv", "orders_apac.csv"]

    @task
    def load_file(name):
        rows = {"orders_eu.csv": 120, "orders_us.csv": 340, "orders_apac.csv": 75}[name]
        print(f"LAB loaded {name}: {rows} rows")
        return rows

    @task
    def summarize(counts):
        print("LAB total rows:", sum(counts))

    summarize(load_file.expand(name=list_files()))


pipeline = daily_files()

if __name__ == "__main__":
    report(pipeline.test())
''')
%% md
**What to notice:** `load_file` ran three times, as instances `[0]`, `[1]` and `[2]`, one per file returned by
`list_files`, and `summarize` received all three counts and added them to 535 rows.
%% md
## Retries and trigger rules

A task that raises an exception fails; with `retries` set it is re-run after `retry_delay`, and `try_number` counts
attempts. When a task fails for good, its downstream tasks are marked `upstream_failed` and do not run, because the
default **trigger rule** is `all_success`. Other rules change that: `all_done` runs once every upstream task has
finished, whatever the outcome, which suits cleanup; `one_failed` runs only if something failed, which suits alerts.

**Where it matters**

Set retries for failures that are usually transient (network timeouts, a busy warehouse) and make sure temporary
resources are cleaned up even when the pipeline fails.

**Watch out for**

Retries are only safe when the task is idempotent: a retried load that appends rows doubles them. And retrying a
task that fails on bad data wastes time; fail fast on errors that a retry cannot fix.
%% code
run_dag_file("retries.py", '''
from datetime import datetime, timedelta, timezone

from airflow.sdk import dag, get_current_context, task
from airflow.task.trigger_rule import TriggerRule
from lab_report import report


@dag(
    schedule=None,
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    default_args={"retries": 2, "retry_delay": timedelta(seconds=1)},
)
def retries_and_rules():
    @task
    def call_api():
        attempt = get_current_context()["ti"].try_number
        print(f"LAB call_api attempt {attempt}")
        if attempt < 2:
            raise ConnectionError("timeout")  # transient: succeeds on the retry
        return 42

    @task(retries=0)
    def validate():
        raise ValueError("schema mismatch")  # not transient: fail at once

    @task
    def publish():
        print("LAB publish ran")

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def cleanup():
        print("LAB cleanup ran")

    api, checked = call_api(), validate()
    checked >> publish()
    [api, checked] >> cleanup()


pipeline = retries_and_rules()

if __name__ == "__main__":
    report(pipeline.test())
''')
%% md
**What to notice:** `call_api` failed on its first attempt and succeeded on try 2. `validate` failed with no retries,
so `publish` was marked `upstream_failed` and never ran, while `cleanup` ran anyway because its rule is `all_done`.
The DAG run as a whole is `failed`.
%% md
## Testing DAG files before deployment

A DAG file with a syntax error or a missing import never appears in the scheduler; it shows up as an **import
error**. Loading the folder into a `DagBag` parses every file the way the scheduler does, so a CI job can fail on
import errors and enforce rules such as "every DAG sets retries" before anything is deployed.

**Where it matters**

Import errors in production are silent: the DAG simply stops being scheduled. A short pytest suite over the `DagBag`
catches them, and policy checks keep every team's DAGs consistent.

**Watch out for**

Code at the top level of a DAG file runs every time the scheduler parses it, every 30 seconds by default. Keep
database calls, API requests and heavy imports inside tasks, or parsing becomes slow and fragile.
%% code
(dags / "broken_dag.py").write_text("from airflow.sdk import dag\\nimport pandas_typo\\n")

checks = '''
import os
import sys

from airflow.dag_processing.dagbag import DagBag

folder = os.environ["AIRFLOW__CORE__DAGS_FOLDER"]
sys.path.insert(0, folder)  # the scheduler does this too, so DAG files can import shared modules
bag = DagBag(folder)


def test_no_import_errors():
    errors = {path.rsplit("/", 1)[-1]: error.strip().splitlines()[-1] for path, error in bag.import_errors.items()}
    print("LAB import errors:", errors)
    assert not errors


def test_every_dag_retries():
    missing = sorted(dag_id for dag_id, dag in bag.dags.items() if "retries" not in dag.default_args)
    print("LAB DAGs without retries:", missing)
    assert not missing


for check in [test_no_import_errors, test_every_dag_retries]:
    try:
        check()
        print(f"LAB {check.__name__}: passed")
    except AssertionError:
        print(f"LAB {check.__name__}: FAILED")
'''
run_python(home / "test_dags.py", checks)
%% md
**What to notice:** Parsing the folder found exactly one import error, `broken_dag.py`, with the
`ModuleNotFoundError` that a scheduler would only have logged. The policy check also failed: `daily_files` and
`orders_pipeline` set no retries, while `retries_and_rules` does.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Map over partitions

**Difficulty:** Easy · about 10 min

Write a DAG that maps a `count_rows` task over the dates `2026-02-01` to `2026-02-03` and prints the number of mapped
instances that succeeded.
%% code
# Try your solution here.
%% solution
run_dag_file("partitions.py", '''
from datetime import datetime, timezone

from airflow.sdk import dag, task
from lab_report import report


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc), default_args={"retries": 1})
def partitions():
    @task
    def count_rows(day):
        return len(day)

    count_rows.expand(day=["2026-02-01", "2026-02-02", "2026-02-03"])


pipeline = partitions()

if __name__ == "__main__":
    report(pipeline.test())
''')
%% md
### Exercise 2: Alert only on failure

**Difficulty:** Medium · about 15 min

Add an `alert` task to a DAG with one failing task, so that `alert` runs only when an upstream task failed. Run it
and check `alert`'s state.
%% code
# Try your solution here.
%% solution
run_dag_file("alerting.py", '''
from datetime import datetime, timezone

from airflow.sdk import dag, task
from airflow.task.trigger_rule import TriggerRule
from lab_report import report


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc), default_args={"retries": 0})
def alerting():
    @task
    def load():
        raise RuntimeError("disk full")

    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def alert():
        print("LAB alert sent")

    load() >> alert()


pipeline = alerting()

if __name__ == "__main__":
    report(pipeline.test())
''')
%% md
### Exercise 3: Fix the policy failures

**Difficulty:** Medium · about 10 min

Delete the broken file, add `default_args={"retries": 2}` to the two DAGs without retries, and rerun the checks
until both pass.
%% code
# Try your solution here.
%% solution
(dags / "broken_dag.py").unlink()
for name in ["orders_pipeline.py", "daily_files.py"]:
    path = dags / name
    path.write_text(path.read_text().replace(
        "@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc))",
        '@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc), default_args={"retries": 2})',
    ))
run_python(home / "test_dags.py", checks)
%% md
## Key takeaways

- A TaskFlow DAG is Python: `@task` functions, with dependencies and XCom created by passing one task's result to
  another. Keep XCom for small values.
- `.expand()` maps a task over a list known only at run time, giving each item its own state and retries.
- Retry transient failures, fail fast on bad data, and use trigger rules such as `all_done` and `one_failed` for
  cleanup and alerts.
- `dag.test()` runs a DAG in one process, and a `DagBag` test catches import errors and policy violations before
  deployment.
%% md
**Next:** [Airflow 2: Assets and data-aware scheduling](airflow-02-assets.ipynb)
"""
SPEC = SPEC.replace("@@INTRO@@", INTRO).replace("@@SETUP_PIP@@", SETUP_PIP).replace("@@HELPERS@@", HELPERS)

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
