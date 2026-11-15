import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from af_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/airflow/airflow-02-assets.ipynb"
SPEC = """%% md
# Airflow 2: Assets and data-aware scheduling

A time schedule runs a DAG at 06:00 whether or not its input is ready. **Assets** let a DAG run when the data it reads
has actually been updated. This lab publishes asset events with metadata, shows that a failed task publishes
nothing, declares consumers that wait for one or several assets, and reads the producer's metadata from a consumer.

@@INTRO@@

@@SETUP_PIP@@
%% md
## Setup and sample data

The next cell creates an Airflow home and its metadata database and defines `run_dag_file` and the `report` module
from Airflow 1. The DAGs below describe two curated tables, `orders` and `customers`, as assets.

@@HELPERS@@
%% md
## Assets, outlets and asset events

An `Asset` names a piece of data by URI, such as `s3://lake/orders`. Airflow does not read or check the data; the URI
is an identifier. A task lists the assets it writes in `outlets`, and every time that task **succeeds**, Airflow
records an **asset event**. Through `outlet_events` the task can attach `extra` metadata to the event, such as the
row count or the partition it wrote.

**Where it matters**

Asset events replace guesswork such as "the upstream job usually finishes by 05:30". They also leave an audit trail
of when each table was last updated and by which run.

**Watch out for**

An event means "the task succeeded", not "the data is good". Validate inside the producing task, or in a task before
it, so that a bad load fails instead of announcing itself.
%% code
run_dag_file("publish_orders.py", '''
from datetime import datetime, timezone

from airflow.models.asset import AssetEvent
from airflow.sdk import Asset, dag, task
from airflow.utils.session import create_session
from lab_report import report

orders = Asset("s3://lake/orders")


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc))
def publish_orders():
    @task(outlets=[orders])
    def publish(*, outlet_events):
        rows = 3  # in a real task: the count from the write you just did
        outlet_events[orders].extra = {"rows": rows, "day": "2026-02-03"}

    publish()


pipeline = publish_orders()

if __name__ == "__main__":
    report(pipeline.test())
    with create_session() as session:
        for event in session.query(AssetEvent):
            print("LAB asset event:", event.asset.uri, event.extra)
''')
%% md
**What to notice:** The successful `publish` task produced one asset event for `s3://lake/orders`, carrying the
`extra` metadata the task attached: three rows for 2026-02-03.
%% md
## A failed task publishes nothing

Because events are recorded only on success, a producer that fails leaves the asset untouched, and no consumer is
triggered. This is what makes asset scheduling safe: downstream DAGs never start on a half-written table.

**Where it matters**

Put the asset on the task that **finishes** publishing, such as the swap of a staging table into place, not on an
earlier step, so that the event means the data is complete.

**Watch out for**

If the data is written by something outside Airflow (a vendor drop, another scheduler), Airflow cannot know when it
changes. Record the event yourself through the REST API, or use a sensor, rather than pretending a schedule is enough.
%% code
run_dag_file("publish_bad_orders.py", '''
from datetime import datetime, timezone

from airflow.models.asset import AssetEvent
from airflow.sdk import Asset, dag, task
from airflow.utils.session import create_session
from lab_report import report

orders = Asset("s3://lake/orders")


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc), default_args={"retries": 0})
def publish_bad_orders():
    @task(outlets=[orders])
    def publish():
        raise ValueError("3 rows have a negative amount")

    publish()


pipeline = publish_bad_orders()

if __name__ == "__main__":
    report(pipeline.test())
    with create_session() as session:
        print("LAB asset events for orders:", session.query(AssetEvent).count())
''')
%% md
**What to notice:** The failing `publish` task left the asset with the single event from the earlier successful run.
No new event, so nothing downstream would start.
%% md
## Consumers: waiting for one asset or several

A consumer DAG puts assets in its `schedule` instead of a time. `schedule=[orders]` runs after every update to
`orders`. Assets combine with `&` (wait until **both** have been updated since the last run) and `|` (run when
**either** is). The scheduler records each DAG's dependencies when it parses the files, which `airflow dags
reserialize` does on demand.

**Where it matters**

A report that joins orders and customers should wait for both to be fresh. With `&`, it runs once after both
producers finish, in whichever order they finish.

**Watch out for**

Several updates to an asset before the consumer runs produce one consumer run, not one per event. A consumer that must
process each update separately has to read all of its triggering events, not just the latest.
%% code
(dags / "consumers.py").write_text('''
from datetime import datetime, timezone

from airflow.sdk import Asset, dag, task

orders = Asset("s3://lake/orders")
customers = Asset("s3://lake/customers")
start = datetime(2026, 1, 1, tzinfo=timezone.utc)


@dag(schedule=[orders], start_date=start)
def orders_report():
    @task
    def build():
        pass

    build()


@dag(schedule=(orders & customers), start_date=start)
def customer_revenue():
    @task
    def build():
        pass

    build()


orders_dag, revenue_dag = orders_report(), customer_revenue()
''')
airflow("dags", "reserialize")
run_python(home / "dependencies.py", '''
from airflow.models.asset import DagScheduleAssetReference
from airflow.utils.session import create_session

with create_session() as session:
    for ref in session.query(DagScheduleAssetReference).order_by(DagScheduleAssetReference.dag_id):
        print("LAB", ref.dag_id, "waits for", ref.asset.uri)
''')
%% md
**What to notice:** The scheduler now knows that `orders_report` waits for `orders` alone, while `customer_revenue`
depends on both `orders` and `customers`. Because of the `&`, it would start only after both had new events.
%% md
## Reading what changed

A consumer often needs to know **what** was updated, not just that something was: which day to process, how many rows
arrived. A task that declares an asset in `inlets` can read that asset's events through `inlet_events`, including the
`extra` the producer attached.

**Where it matters**

Passing the partition date in `extra` lets the consumer process exactly the slice that changed, instead of
recomputing "yesterday" from the clock.

**Watch out for**

`extra` is for small metadata. Treat it like XCom: a date or a count, never the data itself.
%% code
run_dag_file("read_events.py", '''
from datetime import datetime, timezone

from airflow.sdk import Asset, dag, task
from lab_report import report

orders = Asset("s3://lake/orders")


@dag(schedule=[orders], start_date=datetime(2026, 1, 1, tzinfo=timezone.utc))
def daily_summary():
    @task(inlets=[orders])
    def summarize(*, inlet_events):
        events = inlet_events[orders]
        latest = events[-1].extra
        print(f"LAB {len(events)} event(s) so far; latest: {latest['rows']} rows for {latest['day']}")

    summarize()


pipeline = daily_summary()

if __name__ == "__main__":
    report(pipeline.test())
''')
%% md
**What to notice:** The consumer read the producer's metadata, three rows for 2026-02-03, from the most recent event.
It saw one event in total, because the failed run earlier recorded none.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Publish two partitions

**Difficulty:** Easy · about 10 min

Write a producer DAG that publishes `s3://lake/customers` with `extra={"day": ...}`, run it twice for 2026-02-04 and
2026-02-05 (pass the day through `dag.test(run_conf=...)` and read it from `params` or `dag_run.conf`), and print
every event's `extra`.
%% code
# Try your solution here.
%% solution
run_dag_file("publish_customers.py", '''
from datetime import datetime, timezone

from airflow.models.asset import AssetEvent
from airflow.sdk import Asset, dag, get_current_context, task
from airflow.utils.session import create_session

customers = Asset("s3://lake/customers")


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc))
def publish_customers():
    @task(outlets=[customers])
    def publish(*, outlet_events):
        outlet_events[customers].extra = {"day": get_current_context()["dag_run"].conf["day"]}

    publish()


pipeline = publish_customers()

if __name__ == "__main__":
    for day in ["2026-02-04", "2026-02-05"]:
        pipeline.test(run_conf={"day": day})
    with create_session() as session:
        for event in session.query(AssetEvent).filter(AssetEvent.asset.has(uri="s3://lake/customers")):
            print("LAB", event.extra)
''')
%% md
### Exercise 2: Either input

**Difficulty:** Medium · about 10 min

Add a DAG `any_update_audit` scheduled on `orders | customers`, reserialize, and list the assets it waits for.
%% code
# Try your solution here.
%% solution
source = (dags / "consumers.py").read_text()
(dags / "consumers.py").write_text(source + \'\'\'

@dag(schedule=(orders | customers), start_date=start)
def any_update_audit():
    @task
    def audit():
        pass

    audit()


audit_dag = any_update_audit()
\'\'\')
airflow("dags", "reserialize")
run_python(home / "dependencies.py", (home / "dependencies.py").read_text())
%% md
### Exercise 3: Validate before announcing

**Difficulty:** Medium · about 15 min

Write a producer with a `validate` task followed by a `publish` task that has the outlet. Make `validate` fail and
show that no new event appears for `s3://lake/orders`.
%% code
# Try your solution here.
%% solution
run_dag_file("validated_publish.py", '''
from datetime import datetime, timezone

from airflow.models.asset import AssetEvent
from airflow.sdk import Asset, dag, task
from airflow.utils.session import create_session
from lab_report import report

orders = Asset("s3://lake/orders")


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc), default_args={"retries": 0})
def validated_publish():
    @task
    def validate():
        raise ValueError("duplicate order ids")

    @task(outlets=[orders])
    def publish():
        pass

    validate() >> publish()


pipeline = validated_publish()

if __name__ == "__main__":
    report(pipeline.test())
    with create_session() as session:
        print("LAB orders events:", session.query(AssetEvent).filter(AssetEvent.asset.has(uri="s3://lake/orders")).count())
''')
%% md
## Key takeaways

- An asset names data by URI; a task that lists it in `outlets` records an asset event each time it succeeds, with
  optional `extra` metadata.
- Failed tasks record nothing, so put the outlet on the step that completes publishing and validate before it.
- Consumers schedule on assets instead of times, with `&` to wait for all inputs and `|` for any of them.
- Several updates can trigger one consumer run; read `inlet_events` to see what changed, and keep `extra` small.
%% md
**Next:** [Airflow 3: Data intervals and backfills](airflow-03-backfill.ipynb)
"""
SPEC = SPEC.replace("@@INTRO@@", INTRO).replace("@@SETUP_PIP@@", SETUP_PIP).replace("@@HELPERS@@", HELPERS)

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
