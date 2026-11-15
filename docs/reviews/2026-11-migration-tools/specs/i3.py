import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from nbtools import build, run

PATH = "notebooks/topics/ingestion/ingestion-03-object-storage.ipynb"
SPEC = """%% md
# Ingestion 3: Object storage and manifests

Files are the most common hand-off between systems: an exporter writes CSV or Parquet to an S3 bucket, and a loader
picks them up. Object storage has no transactions and no "file is finished" flag, so the conventions around the files
decide whether the hand-off is reliable. This lesson covers a landing layout, listing at scale, publishing a manifest
last, naming objects so reruns overwrite, and a ledger that makes the loader idempotent.

Every example uses the real `boto3` S3 client against `moto`, which serves the S3 API in memory. The same calls work
against AWS S3, and most of them against S3-compatible stores such as MinIO or Cloudflare R2.
%% code
# Setup: install notebook dependencies in Colab.
!pip install -q boto3 moto[s3]
%% md
## Setup and sample data

The next cell starts moto's in-memory S3, creates a landing bucket, and defines `write_batch`, which an exporter would
call: it uploads a batch of CSV parts for one day and, unless told it crashed, a manifest listing each part with its
row count and SHA-256 checksum.
%% code
import hashlib
import json

import boto3
from moto import mock_aws

aws = mock_aws()
aws.start()  # every boto3 call below goes to the in-memory S3
s3 = boto3.client("s3", region_name="us-east-1")
BUCKET = "landing"
s3.create_bucket(Bucket=BUCKET)


def write_batch(day, batch, parts, crash_before_manifest=False):
    prefix = f"orders/dt={day}/batch={batch}/"
    entries = []
    for i, rows in enumerate(parts):
        body = ("id,cents\\n" + "".join(f"{r},{r * 100}\\n" for r in rows)).encode()
        key = f"{prefix}part-{i:04d}.csv"
        s3.put_object(Bucket=BUCKET, Key=key, Body=body)
        entries.append({"key": key, "rows": len(rows), "sha256": hashlib.sha256(body).hexdigest()})
    if not crash_before_manifest:
        s3.put_object(Bucket=BUCKET, Key=prefix + "_manifest.json", Body=json.dumps({"parts": entries}).encode())
    return prefix


write_batch("2026-02-01", "001", [[1, 2], [3]])
write_batch("2026-02-02", "002", [[4, 5, 6]])
write_batch("2026-02-03", "003", [[7], [8]], crash_before_manifest=True)
print("objects:", s3.list_objects_v2(Bucket=BUCKET)["KeyCount"])
%% md
## A landing layout and listing at scale

Object stores have no folders, only keys, but a layout like `orders/dt=2026-02-01/batch=001/part-0000.csv` makes keys
behave like a hierarchy. Engines such as Spark, DuckDB and Athena read `dt=...` as a partition column, and a `Prefix`
narrows a listing to one dataset or day. A listing returns at most 1,000 keys per call; a **paginator** follows the
continuation tokens for you.

**Where it matters**

A consistent layout lets every reader find "all of February" or "one batch" with a prefix, without scanning the bucket,
and keeps partition pruning working downstream.

**Watch out for**

Code that calls `list_objects_v2` once silently reads only the first 1,000 keys. Always paginate, and list the
narrowest prefix you can; listing a whole bucket with millions of keys is slow and billed per request.
%% code
first = s3.list_objects_v2(Bucket=BUCKET, Prefix="orders/", MaxKeys=3)
print("one call with MaxKeys=3:", first["KeyCount"], "keys, truncated:", first["IsTruncated"])

keys = []
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="orders/", PaginationConfig={"PageSize": 3}):
    keys += [obj["Key"] for obj in page.get("Contents", [])]
print("paginated:", len(keys), "keys")
days = s3.list_objects_v2(Bucket=BUCKET, Prefix="orders/", Delimiter="/")["CommonPrefixes"]
print("days:", [p["Prefix"] for p in days])
%% md
**What to notice:** A single call capped at three keys reported `IsTruncated: True`, so code that stopped there would
have missed more than half of the seven objects. The paginator returned all seven, and listing with `Delimiter="/"` returned
each day once, as a folder-like prefix.
%% md
## Publish a manifest last

An exporter writes several files, and a reader that lists the prefix mid-write sees a partial batch. The convention
that fixes this is a **manifest** (or `_SUCCESS` marker) written **after** every data file. Readers only process
batches that have one, and the manifest's row counts and checksums let them verify that they read exactly what was
written.

**Where it matters**

Any multi-file hand-off: daily partner drops, Spark job outputs, database exports. Without a completion signal, the
loader races the writer.

**Watch out for**

A manifest only helps if every reader respects it. And because S3 has no rename, never write data files and then
"move" them into place: copy and delete are separate, non-atomic operations.
%% code
def complete_batches():
    found = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="orders/"):
        found += [obj["Key"].removesuffix("_manifest.json") for obj in page.get("Contents", []) if obj["Key"].endswith("_manifest.json")]
    return sorted(found)


def verify(prefix):
    manifest = json.loads(s3.get_object(Bucket=BUCKET, Key=prefix + "_manifest.json")["Body"].read())
    total = 0
    for part in manifest["parts"]:
        body = s3.get_object(Bucket=BUCKET, Key=part["key"])["Body"].read()
        matches = hashlib.sha256(body).hexdigest() == part["sha256"] and body.count(b"\\n") - 1 == part["rows"]
        if not matches:
            return f"{part['key']} does not match the manifest"
        total += part["rows"]
    return f"ok, {total} rows"


for prefix in complete_batches():
    print(prefix, "->", verify(prefix))
print("batches without a manifest:", sorted({k.rsplit("/", 1)[0] + "/" for k in keys} - set(complete_batches())))
%% md
**What to notice:** Only the first two batches are complete: their parts match the manifests' checksums and row
counts (3 rows each). The February 3 batch has data files but no manifest, because its writer crashed, so a reader
skips it instead of loading half of it.
%% md
## Name objects so reruns overwrite

When an exporter reruns a batch, the result depends on how it names objects. Names with a timestamp or random UUID
create **new** objects on every run, so the prefix ends up holding both attempts. Names derived from the batch (its
ID and part number) make a rerun **overwrite** the same keys, which is idempotent.

**Where it matters**

Reruns happen after every failure. Deterministic names turn "did the retry create duplicates?" into a question that
never comes up.

**Watch out for**

Overwriting replaces objects one by one; a reader in the middle of a rerun can still see a mix. Rewrite the manifest
last on the rerun too, and have readers verify against it.
%% code
import uuid

for attempt in range(2):
    s3.put_object(Bucket=BUCKET, Key=f"uuid-demo/dt=2026-02-04/{uuid.uuid4()}.csv", Body=b"id\\n9\\n")
    s3.put_object(Bucket=BUCKET, Key="batch-demo/dt=2026-02-04/batch=004/part-0000.csv", Body=b"id\\n9\\n")
for prefix in ["uuid-demo/", "batch-demo/"]:
    print(prefix, s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)["KeyCount"], "object(s) after two runs")
%% md
**What to notice:** After two runs, the random names left two copies of the same data, while the deterministic name
left one object: the second run replaced the first.
%% md
## A ledger makes the loader idempotent

The loader needs to remember which batches it has already loaded, or every run reloads everything. A small **load
ledger** table, written in the same transaction as the loaded rows, records each batch's prefix and manifest
checksum. A batch is loaded only if it is complete and not in the ledger, or if its manifest changed (a rerun).

**Where it matters**

Scheduled loaders, event-driven ones (an S3 notification per object) and manual backfills can all process the same
batch; the ledger makes the outcome the same however many times it runs.

**Watch out for**

S3 event notifications can be delivered more than once and out of order. Trigger on the manifest object, not on data
files, and still check the ledger.
%% code
import sqlite3

warehouse = sqlite3.connect(":memory:")
warehouse.execute("create table orders (id integer primary key, cents integer)")
warehouse.execute("create table load_ledger (batch text primary key, manifest_sha256 text)")


def load_new_batches():
    loaded = []
    for prefix in complete_batches():
        manifest = s3.get_object(Bucket=BUCKET, Key=prefix + "_manifest.json")["Body"].read()
        digest = hashlib.sha256(manifest).hexdigest()
        if warehouse.execute("select 1 from load_ledger where batch = ? and manifest_sha256 = ?", (prefix, digest)).fetchone():
            continue
        with warehouse:  # rows and ledger entry commit together
            for part in json.loads(manifest)["parts"]:
                lines = s3.get_object(Bucket=BUCKET, Key=part["key"])["Body"].read().decode().splitlines()[1:]
                warehouse.executemany("insert or replace into orders values (?, ?)", [line.split(",") for line in lines])
            warehouse.execute("insert or replace into load_ledger values (?, ?)", (prefix, digest))
        loaded.append(prefix)
    return loaded


print("first run loaded:", load_new_batches())
print("second run loaded:", load_new_batches())
write_batch("2026-02-03", "003", [[7], [8]])  # the exporter reruns the crashed batch
print("after the rerun:", load_new_batches(), "| rows:", warehouse.execute("select count(*) from orders").fetchone()[0])
%% md
**What to notice:** The first run loaded the two complete batches and the second loaded nothing. Once the exporter
re-ran February 3 and wrote its manifest, the next run loaded just that batch, bringing the table to eight orders.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: List the batches of one day

**Difficulty:** Easy · about 5 min

Use a prefix and `Delimiter="/"` to list the batch prefixes under `orders/dt=2026-02-01/`.
%% code
# Try your solution here.
%% solution
listing = s3.list_objects_v2(Bucket=BUCKET, Prefix="orders/dt=2026-02-01/", Delimiter="/")
print([p["Prefix"] for p in listing["CommonPrefixes"]])
%% md
### Exercise 2: Catch a corrupted part

**Difficulty:** Medium · about 10 min

Overwrite `part-0000.csv` of the February 2 batch with different content (keep the manifest), and run `verify` on that
batch.
%% code
# Try your solution here.
%% solution
s3.put_object(Bucket=BUCKET, Key="orders/dt=2026-02-02/batch=002/part-0000.csv", Body=b"id,cents\\n4,1\\n5,1\\n6,1\\n")
print(verify("orders/dt=2026-02-02/batch=002/"))
%% md
### Exercise 3: A changed manifest triggers a reload

**Difficulty:** Medium · about 10 min

Rerun the February 1 batch with an extra order 10 in its second part, then call `load_new_batches`. Which batch loads,
and how many orders does the table hold?
%% code
# Try your solution here.
%% solution
write_batch("2026-02-01", "001", [[1, 2], [3, 10]])
print(load_new_batches(), warehouse.execute("select count(*) from orders").fetchone()[0])
%% md
## Key takeaways

- Lay out keys as `dataset/dt=YYYY-MM-DD/batch=ID/part-NNNN`, list with the narrowest prefix, and always paginate.
- Write a manifest with row counts and checksums after the data files; readers load only complete, verified batches.
- Derive object names from the batch so a rerun overwrites instead of duplicating.
- Record loaded batches and their manifest checksums in a ledger, in the same transaction as the rows, so the loader is
  idempotent and reloads only changed batches.
%% md
**Next:** [Ingestion 4: Load into DuckDB with dlt](ingestion-04-dlt.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
