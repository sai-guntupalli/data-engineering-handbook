import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# Open table formats compared

A folder of Parquet files is not a table. Nothing stops a reader from seeing half of an overwrite, two writers from
clobbering each other, or a deleted row from coming back when someone re-runs yesterday's job. **Table formats**
(Delta Lake, Apache Iceberg, Apache Hudi, Apache Paimon) add a metadata layer on top of the files that turns
them into a table with atomic commits, snapshots, schema rules and row-level changes.

This lesson runs the same operations on a **Delta** table (with `deltalake`, the Rust implementation) and an
**Iceberg** table (with `pyiceberg` and a local SQLite catalog), and compares what each writes to disk: commits,
updates and deletes, time travel, schema evolution, partitioning and maintenance. Hudi and Paimon, which need
Spark or Flink, are compared in prose at the end.

*Last reviewed: November 2026, against deltalake 1.6, pyiceberg 0.12, the Delta protocol and the Iceberg v2/v3 specs.*

**Prerequisites:** [Parquet](../parquet/parquet.ipynb). For each format on its own, see [Delta Lake](../delta/delta.ipynb)
and [Apache Iceberg](../iceberg/iceberg.ipynb).
%% code
# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
!pip install -q deltalake~=1.6 pyiceberg[sql-sqlite,pyarrow]~=0.12 pyarrow
%% md
## Setup and sample data

The first cell creates a scratch folder, a Delta table location in it, and an Iceberg catalog stored in a SQLite
file (the catalog records where each table's current metadata lives). The second builds the first delivery of
orders as an Arrow table: one row per order, with an order timestamp.
%% code
import json
import tempfile
from datetime import datetime
from pathlib import Path

import pyarrow as pa
from deltalake import DeltaTable, write_deltalake
from pyiceberg.catalog.sql import SqlCatalog

work = Path(tempfile.mkdtemp(prefix="formats-"))
delta_path = str(work / "delta_orders")
catalog = SqlCatalog("local", uri=f"sqlite:///{work}/catalog.db", warehouse=f"file://{work}/iceberg")
catalog.create_namespace("shop")


def files_under(folder):
    """Files below a folder, relative to it, sorted: what the format wrote to disk."""
    root = Path(folder)
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and not p.name.endswith(".crc"))
%% code
schema = pa.schema([("order_id", pa.int64()), ("customer_id", pa.string()), ("status", pa.string()),
                    ("amount", pa.float64()), ("order_ts", pa.timestamp("us"))])
day1 = pa.table({
    "order_id": [1, 2, 3, 4],
    "customer_id": ["C1", "C2", "C1", "C3"],
    "status": ["paid", "placed", "paid", "paid"],
    "amount": [120.0, 80.0, 45.5, 300.0],
    "order_ts": [datetime(2026, 3, 1, 9), datetime(2026, 3, 1, 11), datetime(2026, 3, 2, 10), datetime(2026, 3, 2, 15)],
}, schema=schema)
print(day1.to_pandas())
%% md
## What a table format adds

A table format keeps a **log or tree of metadata** next to the data files. Each commit writes new data files and
then atomically publishes a new version of the metadata that lists exactly which files make up the table. Readers
read the metadata first and open only the files it lists, so they see the table before a commit or after it, never
in between. Files from a failed or uncommitted write exist on disk but are invisible.

| | Delta Lake | Apache Iceberg |
|---|---|---|
| Metadata | `_delta_log/` of numbered JSON commits, periodic Parquet checkpoints | metadata JSON → manifest list → manifests (Avro) → data files |
| Atomic commit | put-if-absent of the next log file (`00..01.json`) | catalog swaps the pointer to the new metadata file |
| Finding the table | a path | a catalog (REST, Glue, Hive, Unity, Polaris, JDBC/SQL) |
| Origin and home | Databricks; Linux Foundation | Netflix; Apache |

**Where it matters**
- Any lake table more than one job writes to, or that people read while it is being written.

**Watch out for**
- Writing plain Parquet files into a table's folder by hand: the format ignores files its metadata does not list.
%% md
### Create both tables from the same data

Write the first delivery to a new Delta table and a new Iceberg table, then list the files each format wrote.
%% code
write_deltalake(delta_path, day1)

iceberg_orders = catalog.create_table("shop.orders", schema=schema)
iceberg_orders.append(day1)

print("Delta:  ", files_under(delta_path))
print("Iceberg:", files_under(iceberg_orders.location().removeprefix("file://")))
%% md
**What to notice:** Each format wrote one Parquet data file. Delta added a single JSON commit in `_delta_log/`.
Iceberg wrote a metadata JSON file (one before the append and one after it) plus two Avro files: a **manifest list**
for the snapshot and a **manifest** listing the data file with its column statistics. The SQLite catalog points at
the newest metadata file.
%% md
### Read a Delta commit

A Delta commit is newline-delimited JSON: one action per line.
%% code
commit = (Path(delta_path) / "_delta_log" / "00000000000000000000.json").read_text().splitlines()
for line in commit:
    action = json.loads(line)
    kind = next(iter(action))
    detail = action[kind]
    summary = {k: detail[k] for k in ("path", "size", "numRecords") if k in detail} if kind == "add" else ""
    if kind == "add":
        summary["numRecords"] = json.loads(detail["stats"])["numRecords"]
    print(f"{kind:10} {summary}")
%% md
**What to notice:** The first commit holds `protocol` (the reader and writer features required), `metaData` (schema
and partition columns), `commitInfo` (what operation ran) and one `add` action per data file with its record count
and min/max statistics. The current table is the set of files added and not yet removed, replayed from these
commits.
%% md
## Commit and append

Every write is a new version (Delta) or snapshot (Iceberg). Appends add files; nothing existing is rewritten.
Both formats use **optimistic concurrency**: two writers prepare their files independently, and only one can publish
the next version; the other re-checks for conflicts and retries or fails.

**Where it matters**
- Several jobs appending to one table, such as a streaming job and a backfill.

**Watch out for**
- Many tiny appends: each one adds files and metadata, which later slows every read until compaction.
%% md
### Append the second day to both

Append two orders from March 3 and compare the version history.
%% code
day2 = pa.table({
    "order_id": [5, 6], "customer_id": ["C2", "C4"], "status": ["placed", "paid"],
    "amount": [60.0, 210.0], "order_ts": [datetime(2026, 3, 3, 9), datetime(2026, 3, 3, 18)],
}, schema=schema)
write_deltalake(delta_path, day2, mode="append")
iceberg_orders.append(day2)

delta = DeltaTable(delta_path)
print("Delta versions:")
for entry in reversed(delta.history()):
    print(f"  v{entry['version']}  {entry['operation']:6}  {entry.get('operationParameters', {}).get('mode', '')}")
print("Iceberg snapshots:")
for snap in iceberg_orders.inspect.snapshots().to_pylist():
    print(f"  {snap['snapshot_id']}  {snap['operation']:6}  added rows: {snap['summary'].get('added-records') if isinstance(snap['summary'], dict) else dict(snap['summary']).get('added-records')}")
%% md
**What to notice:** Delta numbers versions 0, 1, ...; Iceberg identifies snapshots by long random ids and links each
to its parent. Both recorded the append as a separate commit with its own statistics, and both tables now hold six
orders.
%% md
## Update and delete rows

Parquet files are immutable, so changing one row means writing new files. Two strategies exist:

- **Copy-on-write**: rewrite every data file that contains an affected row, and mark the old file removed. Reads stay
  fast; writes cost a full file per change.
- **Merge-on-read**: write a small **delete file** (Iceberg position or equality deletes, Delta **deletion vectors**)
  that masks rows, and let readers apply it. Writes are cheap; reads pay until compaction.

`deltalake` and `pyiceberg` below use copy-on-write. Spark, Trino and Flink can write merge-on-read for both formats.

**Where it matters**
- GDPR deletes, late corrections, and CDC upserts into a lake table.

**Watch out for**
- A delete with a broad predicate on a large table: copy-on-write rewrites every file that matches.
%% md
### Delete an order and upsert a correction

Delete order 2 from both tables, then upsert a batch that changes order 3 and adds order 7.
%% code
fix = pa.table({
    "order_id": [3, 7], "customer_id": ["C1", "C5"], "status": ["refunded", "paid"],
    "amount": [45.5, 75.0], "order_ts": [datetime(2026, 3, 2, 10), datetime(2026, 3, 3, 20)],
}, schema=schema)

delta.delete("order_id = 2")
(delta.merge(source=fix, predicate="t.order_id = s.order_id", source_alias="s", target_alias="t")
      .when_matched_update_all().when_not_matched_insert_all().execute())

iceberg_orders.delete("order_id == 2")
result = iceberg_orders.upsert(fix, join_cols=["order_id"])
print(f"Iceberg upsert: {result.rows_updated} updated, {result.rows_inserted} inserted")

delta_rows = DeltaTable(delta_path).to_pyarrow_table().sort_by("order_id").select(["order_id", "status"]).to_pylist()
iceberg_rows = iceberg_orders.scan().to_arrow().sort_by("order_id").select(["order_id", "status"]).to_pylist()
print("same result:", delta_rows == iceberg_rows)
print([(r["order_id"], r["status"]) for r in delta_rows])
%% md
**What to notice:** Both tables now hold orders 1, 3 to 7: order 2 is gone, order 3 is `refunded` and order 7 was
inserted, and the two formats agree row for row. Each operation was one more commit; the next section reads the
older versions.
%% md
## Time travel

Because old files are only marked removed, every earlier version stays readable until maintenance deletes the
files. Delta reads a version number or timestamp; Iceberg reads a snapshot id, a timestamp, or a named **tag** or
**branch**.

**Where it matters**
- Reproducing yesterday's report, auditing what a bad load changed, and rolling back (`restore` in Delta,
  `rollback_to_snapshot` in Iceberg).

**Watch out for**
- Time travel only reaches back as far as retention allows: Delta's `vacuum` and Iceberg's snapshot expiry delete
  the files older versions need.
%% md
### Read both tables as they were after the first day

Delta version 0 and Iceberg's first snapshot hold the original four orders.
%% code
first_snapshot = iceberg_orders.snapshots()[0].snapshot_id
old_delta = DeltaTable(delta_path, version=0).to_pyarrow_table()
old_iceberg = iceberg_orders.scan(snapshot_id=first_snapshot).to_arrow()
for name, table in [("Delta v0", old_delta), ("Iceberg first snapshot", old_iceberg)]:
    rows = table.sort_by("order_id").select(["order_id", "status"]).to_pylist()
    print(f"{name:24} {[(r['order_id'], r['status']) for r in rows]}")
print("Delta now at version", DeltaTable(delta_path).version(), "| Iceberg snapshots:", len(iceberg_orders.snapshots()))
%% md
**What to notice:** Both old reads return orders 1 to 4 with order 2 still present and order 3 still `paid`: the
delete and the correction never touched the old files. The current Delta table is several versions on, and Iceberg
has kept a snapshot for every commit, including the intermediate steps of the delete and the upsert.
%% md
## Evolve the schema

Adding a column is a metadata change in both formats: old files simply lack the column and read as null.
Iceberg tracks columns by **field id**, so renaming or reordering a column never confuses it with another, and old
files are matched by id rather than by name. Delta matches by name unless **column mapping** is enabled.

**Where it matters**
- A source adds a field; a team renames a badly named column.

**Watch out for**
- Changing a column's type to an incompatible one: only safe widenings (int to long, float to double, and in Delta
  with type widening, more) are allowed without rewriting.
%% md
### Add a `channel` column to both tables

Append an order that has a new `channel` field, letting each format add the column.
%% code
from pyiceberg.types import StringType

day3 = pa.table({
    "order_id": [8], "customer_id": ["C1"], "status": ["paid"], "amount": [150.0],
    "order_ts": [datetime(2026, 3, 4, 9)], "channel": ["mobile"],
})
write_deltalake(delta_path, day3.cast(schema.append(pa.field("channel", pa.string()))), mode="append", schema_mode="merge")

with iceberg_orders.update_schema() as update:
    update.add_column("channel", StringType())
iceberg_orders.append(day3.cast(iceberg_orders.schema().as_arrow()))

print("Delta columns:  ", DeltaTable(delta_path).schema().to_arrow().names)
print("Iceberg columns:", [f"{f.name}(id {f.field_id})" for f in iceberg_orders.schema().fields])
print(DeltaTable(delta_path).to_pyarrow_table().sort_by("order_id").select(["order_id", "channel"]).to_pandas().tail(3))
%% md
**What to notice:** Both tables gained `channel`. Iceberg shows each column's field id (`channel` got the next free
id, 6), which is what lets it rename columns safely. Orders written before the change read `channel` as null
(pandas shows `NaN`); only order 8 has a value.
%% md
## Partition the data

Both formats split data into partitions so a filter can skip files, but they expose it differently:

- **Delta** uses Hive-style **partition columns**: the value is a column the writer must fill and the folder name
  (`order_date=2026-03-01/`). Queries must filter on that column to prune.
- **Iceberg** uses **hidden partitioning**: the spec says "partition by `day(order_ts)`", the writer derives the
  value, and a filter on `order_ts` itself prunes files. The spec can change later (**partition evolution**)
  without rewriting old data.

Both also prune inside partitions with the min/max statistics kept per file. Delta's **liquid clustering** and
Iceberg's sort orders replace fixed partitions for many tables.

**Where it matters**
- Large tables filtered by date or tenant.

**Watch out for**
- Delta queries that filter on `order_ts` when the partition column is `order_date`: no partition pruning.
%% md
### Partition by day in each format

Create a Delta table partitioned by an explicit `order_date` column and an Iceberg table partitioned by `day(order_ts)`.
%% code
import pyarrow.compute as pc
from pyiceberg.transforms import DayTransform

all_orders = DeltaTable(delta_path).to_pyarrow_table().select(schema.names)

by_date_path = str(work / "delta_orders_by_date")
write_deltalake(by_date_path, all_orders.append_column("order_date", pc.cast(all_orders["order_ts"], pa.date32())),
                partition_by=["order_date"])

by_day = catalog.create_table("shop.orders_by_day", schema=schema)
with by_day.update_spec() as spec:  # the partition spec is metadata: day(order_ts), named order_day
    spec.add_field("order_ts", DayTransform(), "order_day")
by_day.append(all_orders)

print("Delta folders:  ", sorted({f.split("/")[0] for f in files_under(by_date_path) if f.startswith("order_date")}))
print("Iceberg folders:", sorted({f.split("/")[1] for f in files_under(by_day.location().removeprefix("file://")) if f.startswith("data/")}))
plan = by_day.scan(row_filter="order_ts >= '2026-03-03T00:00:00'").plan_files()
print("Iceberg files for order_ts >= March 3:", len(plan), "of", len(by_day.inspect.files()))
%% md
**What to notice:** Delta wrote one folder per `order_date` value because the writer supplied that column. Iceberg
also wrote one folder per day, named from the transform (`order_day=...`), although the data has no such column; a
filter on `order_ts` alone planned only the files for March 3 and later.
%% md
## Maintain the table

Every commit leaves files behind: small files from appends, rewritten files from updates, and old versions kept for
time travel. Both formats need regular maintenance:

| Job | Delta Lake | Apache Iceberg |
|---|---|---|
| Merge small files | `optimize` (compact, Z-order or liquid clustering) | `rewrite_data_files` |
| Drop old versions | `vacuum` (deletes unreferenced files older than the retention) | `expire_snapshots`, then `remove_orphan_files` |
| Keep metadata small | checkpoints, log cleanup | `rewrite_manifests` |

**Where it matters**
- Any table with frequent small writes; storage cost of old versions.

**Watch out for**
- Running `vacuum` with zero retention while a long query or a streaming reader still uses an old version: its
  files disappear.
%% md
### Compact and vacuum the Delta table

Count the data files, compact them, then vacuum with zero retention (only for a demo).
%% code
dt = DeltaTable(delta_path)
before = len(dt.file_uris())
metrics = dt.optimize.compact()
dt = DeltaTable(delta_path)
removed = dt.vacuum(retention_hours=0, enforce_retention_duration=False, dry_run=False)
print(f"live files: {before} -> {len(dt.file_uris())}; files compacted: {metrics['numFilesRemoved']}; files deleted by vacuum: {len(removed)}")
try:
    DeltaTable(delta_path, version=0).to_pyarrow_table()
    print("version 0 still readable")
except Exception as error:
    print("version 0 is gone:", type(error).__name__)
%% md
**What to notice:** Compaction rewrote the live data files into one, and vacuum then deleted every file no longer
referenced by the current version, including the files version 0 needed. Time travel to version 0 now fails: the
log still remembers the version, but its data is gone. That is why retention defaults to seven days.
%% md
### Expire old Iceberg snapshots

Expire every snapshot except the current one and compare the snapshot counts.
%% code
current = iceberg_orders.current_snapshot().snapshot_id
older = [s.snapshot_id for s in iceberg_orders.snapshots() if s.snapshot_id != current]
iceberg_orders.maintenance.expire_snapshots().by_ids(older).commit()
print(f"snapshots: {len(older) + 1} -> {len(iceberg_orders.snapshots())}")
print("current rows:", iceberg_orders.scan().to_arrow().num_rows)
%% md
**What to notice:** Only the current snapshot remains and the table still reads its seven orders. Expiring a snapshot
removes it from metadata; deleting the data files that no snapshot references any more is a separate step
(`remove_orphan_files` or the engine's cleanup procedure).
%% md
## Hudi, Paimon and choosing a format

**Apache Hudi** was built at Uber for upserts and incremental pulls. Its tables are copy-on-write or merge-on-read,
keep a **timeline** of instants, and index records by key so an upsert finds the file holding a key quickly.
Incremental queries ("everything changed since instant X") are a first-class feature. **Apache Paimon** grew out
of Flink: an LSM-tree table format for streaming upserts with a changelog that downstream jobs can read.

| Choose | When |
|---|---|
| Iceberg | Many engines (Spark, Trino, Flink, Snowflake, BigQuery, DuckDB) must read and write the same tables through a shared catalog |
| Delta Lake | The platform is Databricks or mostly Spark; you want deletion vectors, liquid clustering and the change data feed with little setup |
| Hudi | Upsert-heavy CDC ingestion with record-level indexes and incremental pulls, usually on Spark or Flink |
| Paimon | Flink-first streaming tables that need fast primary-key upserts and a readable changelog |

Interoperability is narrowing the gap: Delta **UniForm** writes Iceberg metadata for Delta tables, Apache XTable
translates metadata between all three, and catalogs such as Unity Catalog and Apache Polaris serve Iceberg's REST
catalog API. Choose by which engines and catalog must work with the tables, not by a feature checklist; most
features exist in all of them.

**Where it matters**
- Platform decisions that are hard to undo once hundreds of tables exist.

**Watch out for**
- Protocol upgrades: enabling a new feature (deletion vectors, Iceberg v3 types) can make a table unreadable to an
  older reader. Test every reader before enabling it.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** A job overwrites a plain Parquet folder while a dashboard reads it. What can the dashboard see, and how does a table format prevent it?

**A.** A mix of old and new files, or none, mid-write. A table format publishes the new file list in one atomic commit, and readers open only files listed in the version they started with.

**Q2.** Why does deleting one row from a 1 GB file cost more under copy-on-write than under merge-on-read?

**A.** Copy-on-write rewrites the whole file without the row. Merge-on-read writes a small delete file or deletion vector that readers apply, deferring the rewrite to compaction.

**Q3.** After a `vacuum` with one-hour retention, an analyst's time-travel query to last week fails. Why?

**A.** Vacuum deleted data files that only old versions referenced. The log still lists the version, but its files are gone.

**Q4.** What does Iceberg's hidden partitioning change for people writing queries?

**A.** They filter on the real column (`order_ts`) and Iceberg prunes partitions derived from it; they do not need to know or fill a separate partition column.

**Q5.** Your company has Spark, Trino and Snowflake reading the same lake tables. Which format do you lean towards and what decides it?

**A.** Usually Iceberg, because all three read and write it through a shared catalog. The deciding factor is the catalog and writer support each engine has, which you should verify for the exact versions in use.
%% md
## Key takeaways

- A table format adds metadata that lists the files of each version, giving atomic commits, snapshots and safe concurrent writes.
- Delta keeps a JSON log found by path; Iceberg keeps a metadata tree found through a catalog.
- Row changes rewrite files (copy-on-write) or add delete files (merge-on-read); both leave old files for time travel.
- Iceberg partitions by transforms of real columns and tracks columns by id; Delta partitions by explicit columns.
- Compaction and version cleanup are routine jobs, and cleanup limits how far back time travel reaches.
- Choose the format by the engines and catalog that must use it.
%% md
**Next:** Continue with [Lakehouse catalogs](lakehouse-catalogs.ipynb), which explains how engines find these tables
and who may change them.
'''

build("notebooks/topics/concepts/open-table-formats.ipynb", SPEC)
