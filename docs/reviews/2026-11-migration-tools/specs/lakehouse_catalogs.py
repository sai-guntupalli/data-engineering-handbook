import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# Lakehouse catalogs

Spark writes `s3://lake/silver/orders`. Trino, a notebook and a BI tool all need to read it, and only the pipeline
may change it. Who tells each engine that `silver.orders` lives at that path, which metadata file is current, and
who is allowed to write? That is the job of a **catalog**.

This lesson builds a small lakehouse with an Apache Iceberg catalog stored in SQLite and shows what a catalog does:
map names to tables, commit changes atomically, detect conflicting writers, rename and drop tables, publish audited
data with branches, and decide who may do what. It ends with the catalog products you will meet.

*Last reviewed: November 2026, against pyiceberg 0.12 and the Iceberg REST catalog specification.*

**Prerequisites:** [Open table formats compared](open-table-formats.ipynb).
%% code
# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
!pip install -q pyiceberg[sql-sqlite,pyarrow]~=0.12 pyarrow
%% md
## Setup and sample data

The first cell creates an Iceberg **SQL catalog** backed by a SQLite file, with table data under a local
`warehouse` folder. A production catalog would be a REST service, AWS Glue or a Hive metastore; the operations are
the same. The second cell creates `bronze` and `silver` namespaces and a `silver.orders` table with three orders.
%% code
import sqlite3
import tempfile
from datetime import date
from pathlib import Path

import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

work = Path(tempfile.mkdtemp(prefix="catalog-"))
catalog_db = work / "catalog.db"
catalog = SqlCatalog("lake", uri=f"sqlite:///{catalog_db}", warehouse=f"file://{work}/warehouse")


def catalog_rows():
    """What the catalog itself stores: one row per table, pointing at its current metadata file."""
    with sqlite3.connect(catalog_db) as con:
        rows = con.execute("select table_namespace, table_name, metadata_location from iceberg_tables order by 1, 2").fetchall()
    return [(ns, name, Path(loc).name) for ns, name, loc in rows]
%% code
for namespace in ("bronze", "silver"):
    catalog.create_namespace(namespace, properties={"owner": "data-platform"})

schema = pa.schema([("order_id", pa.int64()), ("customer_id", pa.string()), ("amount", pa.float64()), ("order_date", pa.date32())])
orders = catalog.create_table("silver.orders", schema=schema, properties={"owner": "orders-pipeline"})
orders.append(pa.table({"order_id": [1, 2, 3], "customer_id": ["C1", "C2", "C1"], "amount": [120.0, 80.0, 45.5],
                        "order_date": [date(2026, 3, 1)] * 3}, schema=schema))
print(catalog.list_namespaces(), catalog.list_tables("silver"))
%% md
## Names, not paths

Without a catalog, every engine is configured with paths, and every engine must agree on which metadata file is
current. A catalog gives tables **names** (`catalog.namespace.table`) and stores, for each name, one pointer: the
location of the table's current metadata. Engines ask the catalog, read that metadata, and from there find the data
files.

The layers of a lakehouse are then:

| Layer | Examples |
|---|---|
| Object storage | S3, ADLS, GCS |
| Table format | Iceberg, Delta Lake, Hudi |
| Catalog | Iceberg REST (Polaris, Unity Catalog, Lakekeeper, Nessie), AWS Glue, Hive metastore |
| Engines | Spark, Trino, Flink, DuckDB, Snowflake, BigQuery, Databricks SQL |

**Where it matters**
- Letting several engines share tables without copying data or hard-coding paths.

**Watch out for**
- Two catalogs that both think they own the same table: each moves its own pointer and the table forks.
%% md
### Look inside the catalog

The SQL catalog is just a table of pointers. Read it directly.
%% code
for row in catalog_rows():
    print(row)
loaded = catalog.load_table("silver.orders")
print("location:", loaded.location())
print("properties:", {k: v for k, v in loaded.properties.items() if k == "owner"})
%% md
**What to notice:** The catalog holds one row for `silver.orders`: its namespace, name and the file name of its
current metadata (`00001-...metadata.json`, the version written by the append). Everything else, schema, snapshots
and file lists, lives in the table's own metadata under its location. The catalog is small; the table is not.
%% md
## Commits are pointer swaps

An Iceberg commit writes new data and metadata files, then asks the catalog to change the pointer **from** the
metadata the writer started with **to** the new one. The catalog does this atomically: a compare-and-swap. If the
pointer has moved in the meantime, the swap is refused.

**Where it matters**
- Every write from every engine; it is what makes multi-engine writes safe.

**Watch out for**
- Catalogs that cannot compare-and-swap (plain file systems without atomic rename): concurrent writers can lose
  commits. Object stores need a catalog or a locking service for this.
%% md
### Watch the pointer move

Append a fourth order and compare the catalog row before and after.
%% code
before = catalog_rows()[0][2]
orders.append(pa.table({"order_id": [4], "customer_id": ["C3"], "amount": [300.0], "order_date": [date(2026, 3, 2)]}, schema=schema))
after = catalog_rows()[0][2]
print("before:", before)
print("after: ", after)
print("snapshots:", len(orders.snapshots()))
%% md
**What to notice:** The append wrote a new metadata file (`00002-...`), and the catalog row now points at it. The old
metadata file still exists on disk; readers that loaded the table earlier keep reading the version they started
with until they refresh.
%% md
## Conflicting writers

Two writers load the same table version. The first commits. The second tries to swap the pointer from a version that
is no longer current, and the catalog refuses. What happens next depends on the operation: an engine retries an
append on top of the new version automatically, but for an overwrite or delete it must check whether the other
commit changed the same data.

**Where it matters**
- A backfill and the daily job writing to the same table; two streaming jobs.

**Watch out for**
- Retry loops that blindly reapply an overwrite: they can undo the other writer's commit.
%% md
### Two engines commit from the same version

`engine_a` and `engine_b` each load `silver.orders`. A appends; B then tries to replace the table's contents with
a stale view of it.
%% code
from pyiceberg.exceptions import CommitFailedException, ValidationException

engine_a = catalog.load_table("silver.orders")
engine_b = catalog.load_table("silver.orders")

engine_a.append(pa.table({"order_id": [5], "customer_id": ["C4"], "amount": [60.0], "order_date": [date(2026, 3, 3)]}, schema=schema))
stale = engine_b.scan().to_arrow()  # B's snapshot does not include order 5
try:
    engine_b.overwrite(stale)
    print("B committed")
except (CommitFailedException, ValidationException) as error:
    print("B refused:", type(error).__name__, "-", str(error).splitlines()[0][:100])
print("orders now:", sorted(catalog.load_table("silver.orders").scan().to_arrow()["order_id"].to_pylist()))
%% md
**What to notice:** Two things happened. The catalog refused B's first attempt to swap the pointer (the log line
"Commit failed due to a concurrent update, retrying"). On the retry, pyiceberg checked whether files had been added
since B's snapshot that its overwrite would remove, found order 5's file, and gave up with a `ValidationException`.
Had the overwrite gone through, it would have replaced the table with B's stale four orders and silently deleted
order 5. The table still has all five orders; B must reload, recompute and try again.
%% md
## Rename and drop

Renaming a table changes only the catalog entry: the files stay where they are. Dropping a table removes the entry;
whether the files are deleted depends on the catalog and the `purge` option. Because files are not moved, a rename
is instant even for a petabyte table.

**Where it matters**
- Promoting a rebuilt table: build `silver.orders_v2`, validate it, then swap names.

**Watch out for**
- Engines or jobs that cached a path instead of a name: after a rename they still read the old location.
%% md
### Rename a table and check its files

Rename `silver.orders` to `silver.orders_v1` and compare the location.
%% code
old_location = catalog.load_table("silver.orders").location()
catalog.rename_table("silver.orders", "silver.orders_v1")
renamed = catalog.load_table("silver.orders_v1")
print(catalog.list_tables("silver"))
print("same location:", renamed.location() == old_location, "|", Path(renamed.location()).name)
print("rows:", renamed.scan().to_arrow().num_rows)
_ = catalog.rename_table("silver.orders_v1", "silver.orders")  # put it back for the next sections
%% md
**What to notice:** After the rename the catalog lists `orders_v1`, but its location is still the `orders` folder
and all five rows read as before. Only the catalog row changed. Renaming it back is just as cheap.
%% md
## Write, audit, publish with branches

Iceberg tables can have **branches** and **tags**, like Git. A pipeline can write a new batch to an `audit` branch,
run data-quality checks on that branch while readers of `main` see nothing new, and then publish by moving `main`
to the audited snapshot. A **tag** names a snapshot to keep, such as the data behind a quarterly report.

**Where it matters**
- Publishing only validated data to consumers (the write-audit-publish pattern).

**Watch out for**
- Readers that query the branch by mistake: name branches clearly and give consumers `main`.
%% md
### Stage a bad batch on a branch, then publish a good one

Create an `audit` branch from the current snapshot and write a batch with a negative amount to it. Check it, reject
it, then write a corrected batch to a fresh branch and publish it to `main`.
%% code
orders = catalog.load_table("silver.orders")
orders.manage_snapshots().create_branch(orders.current_snapshot().snapshot_id, "audit").commit()

bad_batch = pa.table({"order_id": [6, 7], "customer_id": ["C1", "C5"], "amount": [75.0, -10.0],
                      "order_date": [date(2026, 3, 4)] * 2}, schema=schema)
orders.append(bad_batch, branch="audit")


def audit(table, branch):
    snapshot = table.snapshot_by_name(branch).snapshot_id
    rows = table.scan(snapshot_id=snapshot).to_arrow()
    negatives = [r for r in rows.to_pylist() if r["amount"] < 0]
    return rows.num_rows, negatives


print("main rows:", orders.scan().to_arrow().num_rows, "| audit branch:", audit(orders, "audit"))

orders.manage_snapshots().remove_branch("audit").commit()  # reject: drop the branch, main never saw it
orders.manage_snapshots().create_branch(orders.current_snapshot().snapshot_id, "audit").commit()
orders.append(bad_batch.set_column(2, "amount", pa.array([75.0, 10.0])), branch="audit")
rows, negatives = audit(orders, "audit")
if negatives:
    raise ValueError(f"audit failed: {negatives}")
orders.manage_snapshots().set_current_snapshot(ref_name="audit").commit()  # publish: main jumps to the audited snapshot
print("published; main rows:", orders.scan().to_arrow().num_rows)
%% md
**What to notice:** While the bad batch sat on `audit`, `main` still returned five rows and the audit found order 7's
-10.00. Dropping the branch discarded it without `main` ever changing. The corrected batch passed, and setting
`main` to the audit snapshot published both rows in one step: seven rows.
%% md
## Who may do what

A catalog is also where access is decided, because every engine goes through it. Modern catalogs grant privileges
on catalog objects, and grants **inherit** downwards: a grant on a namespace applies to its tables. With
**credential vending**, the catalog hands an engine short-lived storage credentials scoped to one table's files, so
engines never hold broad bucket keys.

```sql
-- Unity Catalog / Polaris style grants (syntax varies by product)
grant usage on namespace silver to role analysts;
grant select on table silver.orders to role analysts;
grant modify on table silver.orders to role orders_pipeline;
```

**Where it matters**
- One permission model for Spark, Trino and SQL warehouses instead of separate bucket policies per engine.

**Watch out for**
- Engines that bypass the catalog and read storage paths directly: they bypass its permissions too. Lock bucket
  access down to the catalog's vended credentials.
%% md
### Evaluate grants with inheritance

A small model of catalog privileges: grants on the catalog, a namespace or a table, checked from the most specific
object up.
%% code
grants = {
    ("lake", "analysts"): {"usage"},
    ("lake.silver", "analysts"): {"usage", "select"},
    ("lake.silver.orders", "orders_pipeline"): {"select", "modify"},
    ("lake.bronze", "orders_pipeline"): {"usage", "select"},
}


def allowed(role, privilege, table):
    """A privilege on a table holds if it is granted on the table or any parent object."""
    parts = table.split(".")
    objects = [".".join(parts[:i]) for i in range(len(parts), 0, -1)]  # table, namespace, catalog
    return any(privilege in grants.get((obj, role), set()) for obj in objects)


checks = [("analysts", "select", "lake.silver.orders"), ("analysts", "modify", "lake.silver.orders"),
          ("analysts", "select", "lake.bronze.events"), ("orders_pipeline", "modify", "lake.silver.orders"),
          ("orders_pipeline", "modify", "lake.silver.customers")]
for role, privilege, table in checks:
    print(f"{role:16} {privilege:7} {table:24} {'allowed' if allowed(role, privilege, table) else 'denied'}")
%% md
**What to notice:** Analysts can `select` any silver table through the namespace grant, but cannot modify
`silver.orders` or read `bronze`. The pipeline can modify `silver.orders` because of a table-level grant, yet not
`silver.customers`: least privilege, granted at the narrowest object that does the job.
%% md
## The catalogs you will meet

| Catalog | What it is | Notes |
|---|---|---|
| Hive metastore | The original catalog of the Hadoop world | Tables are paths plus partitions; Iceberg uses it with a lock; still common |
| AWS Glue Data Catalog | Managed metastore on AWS | Used by Athena, EMR, Glue; Iceberg REST endpoint available |
| Iceberg REST catalogs | A standard HTTP API for Iceberg catalogs | Apache Polaris, Lakekeeper, Nessie (with Git-like branches), Gravitino |
| Unity Catalog | Databricks' governance catalog, open-sourced in 2024 | Delta and Iceberg tables, grants, lineage, credential vending |
| Snowflake Horizon / Open Catalog | Snowflake's catalog; Open Catalog is managed Polaris | Exposes Iceberg tables to other engines |
| BigLake metastore | Google Cloud's shared catalog | BigQuery, Spark and Iceberg REST access |

Choose the catalog the engines you run support for both reading and writing, and decide early which one is the
single owner of each table.

**Where it matters**
- Platform design: the catalog decision outlives individual engines.

**Watch out for**
- Registering the same table in two catalogs that both accept writes.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** What exactly does an Iceberg catalog store for each table?

**A.** The table's identifier (namespace and name) and a pointer to its current metadata file, plus optional properties. Schema, snapshots and file lists live in the table's metadata.

**Q2.** Why can a catalog refuse a commit even though the writer's files were written successfully?

**A.** The writer asks to swap the pointer from the metadata version it started with. If another commit moved the pointer first, the compare-and-swap fails, and the writer must reload and retry or recompute.

**Q3.** Why is renaming a huge table instant?

**A.** A rename changes the catalog entry only; the data and metadata files stay at the same location.

**Q4.** How do branches implement write-audit-publish?

**A.** The batch is written to a branch that consumers do not read, checks run against that branch, and publishing moves `main` to the audited snapshot in one metadata change. A failed audit drops the branch.

**Q5.** An analyst reads table files directly with storage keys. What governance problem does that create?

**A.** It bypasses the catalog's grants, masking and audit log. Access should go through the catalog, which vends scoped, short-lived credentials.
%% md
## Key takeaways

- A catalog maps table names to the current metadata file and makes that pointer swap atomic.
- Conflicting writers are caught by compare-and-swap; appends retry, overwrites must recompute.
- Renames and drops are catalog operations; files stay where they are unless purged.
- Branches and tags let a pipeline audit data before publishing it to `main`.
- The catalog is the natural place for grants and credential vending across all engines.
%% md
**Next:** Continue with [Data modeling 6: warehouse architectures](../data-modeling/data-modeling-06-warehouse-architectures.ipynb)
for how layers such as bronze, silver and gold are modeled, or [Security and IAM](security-and-iam.ipynb) for the
identities behind those grants.
'''

build("notebooks/topics/concepts/lakehouse-catalogs.ipynb", SPEC)
