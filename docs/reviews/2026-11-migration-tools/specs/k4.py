import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from kafka_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/kafka/kafka-04-delivery-and-transactions.ipynb"
SPEC = f"""%% md
# Kafka 4: Delivery guarantees and transactions

"Exactly once" is the most misunderstood phrase in streaming. This lesson shows where loss and duplication come
from (the order of processing and committing), how an idempotent sink makes replays harmless, and what Kafka
transactions actually guarantee: atomic writes across topics and partitions, visible only to readers that ask for
committed data.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell starts the mock cluster and defines the helpers from Kafka 1. The sample data is five payments for one
merchant, in one partition, so every replay is easy to follow.

{HELPERS}
import json

payments = [("merchant-7", json.dumps({{"payment_id": f"p-{{i}}", "cents": 1000 * i}})) for i in range(1, 6)]
partition = produce("payments", payments)[0][0]
print("payments total:", sum(json.loads(value)["cents"] for _, value in payments), "cents")
%% md
## Commit order decides loss or duplication

A consumer does two things per record: it **processes** it (writes to a database, calls an API) and it **commits**
its offset. A crash can fall between the two, and which comes first decides the outcome:

```text
commit, then process   crash in between -> record marked done but never processed   -> at-most-once (loss)
process, then commit   crash in between -> record processed but not marked done     -> at-least-once (duplicate)
```

The `run` function below processes payments into a running total and crashes after the third one, committing either
before or after processing.

**Where it matters**

Almost every pipeline should be at-least-once: losing a payment is worse than seeing it twice, and duplicates can be
removed downstream. At-most-once suits only data you can afford to drop, such as some metrics.

**Watch out for**

Auto-commit (`enable.auto.commit=true`) commits on a timer from the background, independently of your processing,
so it can produce either failure. Turn it off for any consumer whose output matters.
%% code
def run(group, commit_first, crash_after=None):
    consumer = Consumer(
        {{
            "bootstrap.servers": BOOTSTRAP,
            "group.id": group,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "session.timeout.ms": 6000,
            "heartbeat.interval.ms": 500,
        }}
    )
    consumer.subscribe(["payments"])
    _, end = consumer.get_watermark_offsets(TopicPartition("payments", partition), timeout=10)
    processed, deadline = [], time.time() + 30
    while time.time() < deadline:
        msg = consumer.poll(0.2)
        if msg is None or msg.error():
            continue
        payment = json.loads(msg.value())["payment_id"]
        crash = msg.offset() == crash_after  # the process dies between the two steps
        if commit_first:
            consumer.commit(message=msg, asynchronous=False)
            if crash:
                break
            processed.append(payment)
        else:
            processed.append(payment)
            if crash:
                break
            consumer.commit(message=msg, asynchronous=False)
        if msg.offset() + 1 == end:
            break
    consumer.close()
    return processed


for name, commit_first in [("at-most-once", True), ("at-least-once", False)]:
    before = run(name, commit_first, crash_after=2)
    after = run(name, commit_first)
    print(f"{{name:>13}}: before crash {{before}}, after restart {{after}}")
%% md
**What to notice:** Both runs crashed while handling `p-3`. Committing first had already marked it done, so the
restart began at `p-4` and `p-3` was never processed: it was lost. Processing first had already applied `p-3` but not
committed it, so the restart applied it again: nothing was lost, and `p-3` was processed twice.
%% md
## Idempotent sinks make replays harmless

At-least-once delivery becomes **effectively exactly-once** when applying a record twice has the same effect as
applying it once. The usual way is a sink keyed by a stable event ID: an upsert or an insert that ignores a key it
already has. The sink below is a real SQLite table with `payment_id` as its primary key, fed the same topic twice, as
a full replay after a bad deployment would.

**Where it matters**

This is how most production pipelines get exactly-once results into databases and warehouses: `MERGE` or
`INSERT ... ON CONFLICT` on the event key, or a Delta or Iceberg merge. It works for any sink that supports keyed
writes, which Kafka transactions do not cover.

**Watch out for**

The key must identify the **event**, not the record: an offset changes if the event is produced twice, and a
timestamp can collide. Use the source's event ID or a hash of the fields that define the event.
%% code
import sqlite3

sink = sqlite3.connect(":memory:")
sink.execute("create table payments (payment_id text primary key, cents integer)")


def load(group):
    for _, _, _, value in consume("payments", group=group, expected=len(payments)):
        event = json.loads(value)
        sink.execute("insert into payments values (?, ?) on conflict (payment_id) do nothing", (event["payment_id"], event["cents"]))
    return sink.execute("select count(*), sum(cents) from payments").fetchone()


print("after the first load:", load("loader-1"))
print("after a full replay: ", load("loader-2"))
%% md
**What to notice:** The replay read all five payments again, but the table still holds five rows totalling 15,000
cents. The primary key turned the duplicate inserts into no-ops.
%% md
## Transactions: atomic writes across topics

A **transactional producer** (one with a `transactional.id`) can write to several topics and partitions and then
commit or abort them as a unit. Aborted records are still appended to the log, followed by a marker, so what a
consumer sees depends on its **isolation level**:

```text
read_uncommitted   sees every record, including those of aborted transactions (the Java client's default)
read_committed     sees only committed transactions, and waits at an open transaction (librdkafka's default)
```

A transactional producer also **fences zombies**: when a restarted instance calls `init_transactions()` with the same
`transactional.id`, the broker bumps the producer epoch and rejects any further writes from the old instance, so a
paused process that wakes up cannot commit stale results.

**Where it matters**

Use transactions when one input must produce several outputs that are only valid together, such as an order event
and its matching ledger entries, or when a stream processor writes results and must never expose half a batch.

**Watch out for**

Transactions guarantee nothing to a consumer reading with `read_uncommitted`. Every downstream consumer of a
transactional topic must set `isolation.level=read_committed`, and a long-running transaction stalls those readers.

The mock cluster runs the transaction protocol, so the calls below are the real API, but it does **not** hide open or
aborted transactions from `read_committed` readers and does not fence old producers. Check those two behaviors
against a real broker (for example a local Kafka container) before relying on them.
%% code
tx = Producer({{"bootstrap.servers": BOOTSTRAP, "transactional.id": "ledger-writer"}})
tx.init_transactions(10)

tx.begin_transaction()
tx.produce("orders-tx", key="order-2", value="order-2 placed")
tx.produce("ledger-tx", key="order-2", value="debit 800")
tx.commit_transaction(10)  # both records become visible together, or neither does

tx.begin_transaction()
tx.produce("orders-tx", key="order-3", value="order-3 placed")
tx.abort_transaction(10)  # validation failed before the record was sent: the client discards it
print("buffered after abort:", len(tx))

for topic in ["orders-tx", "ledger-tx"]:
    seen = consume(topic, group=f"audit-{{topic}}", expected=1, timeout=8, **{{"isolation.level": "read_committed"}})
    print(f"{{topic}}:", [value for *_, value in seen])
%% md
**What to notice:** The committed transaction delivered one record to each topic as a unit. The aborted record was
still in the producer's buffer when the transaction aborted, so the client dropped it (`len(tx)` is 0) and it never
reached the log; on a real broker, a record that had already been sent would stay in the log, behind an abort
marker, and be skipped by `read_committed` readers.
%% md
## Consume, transform, produce exactly once

The full **exactly-once** pattern in Kafka combines a transactional producer with the consumer's offsets: the
outputs and the input offsets are committed in the **same** transaction with `send_offsets_to_transaction`. If the
process crashes, the transaction aborts, the outputs disappear for `read_committed` readers, and the offsets roll back
with them, so the batch is reprocessed cleanly. Kafka Streams and Flink's Kafka sink use this under the hood.

```python
consumer = Consumer({{..., "group.id": "enricher", "enable.auto.commit": False, "isolation.level": "read_committed"}})
producer = Producer({{..., "transactional.id": "enricher-1"}})
producer.init_transactions()
while True:
    batch = consumer.consume(500, timeout=1.0)
    producer.begin_transaction()
    for msg in batch:
        producer.produce("orders-enriched", key=msg.key(), value=enrich(msg.value()))
    producer.send_offsets_to_transaction(consumer.position(consumer.assignment()), consumer.consumer_group_metadata())
    producer.commit_transaction()  # outputs and input offsets become visible together
```

The cell below runs the output half of that loop against the mock cluster. The mock cluster accepts
`send_offsets_to_transaction` but does not store transactional offsets, so this lesson does not print them; verify that
step against a real broker.

**Where it matters**

Topic-to-topic processing (enrichment, filtering, aggregation into another topic) can be exactly-once end to end
without an idempotent sink, as long as every reader uses `read_committed`.

**Watch out for**

The guarantee stops at Kafka's edge. A transaction cannot include a database write, an HTTP call or an email, so
side effects outside Kafka still need idempotency or their own coordination.
%% code
reader = Consumer(
    {{"bootstrap.servers": BOOTSTRAP, "group.id": "enricher", "auto.offset.reset": "earliest", "enable.auto.commit": False}}
)
reader.subscribe(["payments"])
batch, deadline = [], time.time() + 20
while len(batch) < len(payments) and time.time() < deadline:
    msg = reader.poll(0.2)
    if msg is not None and not msg.error():
        batch.append(msg)

enricher = Producer({{"bootstrap.servers": BOOTSTRAP, "transactional.id": "enricher-1"}})
enricher.init_transactions(10)
enricher.begin_transaction()
for msg in batch:
    event = json.loads(msg.value())
    enricher.produce("payments-enriched", key=msg.key(), value=json.dumps({{**event, "dollars": event["cents"] / 100}}))
enricher.commit_transaction(10)
reader.close()

enriched = consume("payments-enriched", group="audit", expected=len(batch), **{{"isolation.level": "read_committed"}})
print(len(enriched), "enriched records, first:", enriched[0][3])
%% md
**What to notice:** The five enriched payments were committed as one transaction and read back by a
`read_committed` consumer. On a real broker no such reader could ever see only two or three of them, and the same
commit would also move the `enricher` group's offset past these five inputs.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Count what was lost

**Difficulty:** Easy · about 10 min

Using `run`, crash a new commit-first consumer after offset 0, restart it, and compute how many cents never reached
processing.
%% code
# Try your solution here.
%% solution
done = run("lossy", commit_first=True, crash_after=0) + run("lossy", commit_first=True)
cents = {{json.loads(v)["payment_id"]: json.loads(v)["cents"] for _, v in payments}}
lost = set(cents) - set(done)
print("lost:", sorted(lost), sum(cents[p] for p in lost), "cents")
%% md
### Exercise 2: A sink that is not idempotent

**Difficulty:** Medium · about 15 min

Create a second SQLite table without a primary key, load the topic into it twice with plain `insert`, and compare its
total with the idempotent table's.
%% code
# Try your solution here.
%% solution
sink.execute("create table payments_append (payment_id text, cents integer)")
for group in ["append-1", "append-2"]:
    for _, _, _, value in consume("payments", group=group, expected=len(payments)):
        event = json.loads(value)
        sink.execute("insert into payments_append values (?, ?)", (event["payment_id"], event["cents"]))
print("append-only total:", sink.execute("select sum(cents) from payments_append").fetchone()[0])
print("idempotent total: ", sink.execute("select sum(cents) from payments").fetchone()[0])
%% md
### Exercise 3: All or nothing

**Difficulty:** Medium · about 15 min

Write three refunds to `refunds-tx` in one transaction, but abort it if any refund is over 5,000 cents. Use refunds of
1,000, 7,000 and 2,000 cents, and show what a `read_committed` reader sees.
%% code
# Try your solution here.
%% solution
refunds = [1000, 7000, 2000]
tx.begin_transaction()
for i, cents in enumerate(refunds):
    tx.produce("refunds-tx", key=f"refund-{{i}}", value=str(cents))
if any(cents > 5000 for cents in refunds):
    tx.abort_transaction(10)
else:
    tx.commit_transaction(10)
print("committed refunds:", consume("refunds-tx", group="refund-audit", expected=1, timeout=6, **{{"isolation.level": "read_committed"}}))
%% md
## Key takeaways

- Loss or duplication comes from where a crash lands between processing and committing: commit first is
  at-most-once, process first is at-least-once.
- Default to at-least-once with auto-commit off, and make the sink idempotent by keying writes on a stable event ID.
- Kafka transactions make writes to several topics and partitions atomic, but only for consumers that read with
  `isolation.level=read_committed`.
- Committing input offsets inside the producer's transaction gives exactly-once from topic to topic; anything outside
  Kafka still needs its own idempotency.
%% md
**Next:** [Kafka 5: Connect, schemas and change events](kafka-05-connect-and-schemas.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
