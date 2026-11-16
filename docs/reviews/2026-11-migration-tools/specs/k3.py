import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from kafka_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/kafka/kafka-03-consumers-and-groups.ipynb"
SPEC = f"""%% md
# Kafka 3: Consumers and groups

A consumer's job is not only to read records but to remember how far it got. This lesson covers the poll loop, where
a consumer group stores its position, what is replayed after a crash, how a group shares partitions between
workers when one joins or leaves, and how to measure lag.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell starts the mock cluster and defines the `produce` and `consume` helpers from Kafka 1. The sample data
is six shipment events for one warehouse. They share a key, so they sit in one partition in a known order, which
keeps the replay examples easy to follow.

{HELPERS}
shipments = [("warehouse-1", f"shipment-{{i}}") for i in range(1, 7)]
partition = produce("shipments", shipments)[0][0]
print("all six shipments are in partition", partition)
%% md
## The poll loop and committed offsets

A consumer calls `poll()` in a loop; each call returns the next record (or nothing within the timeout). Its
**position** is the offset of the next record it will read, held in memory. Its **committed offset** is the position
saved in the cluster for its **group**, and it is what a restarted consumer in that group resumes from.

With `enable.auto.commit=false` you decide when to commit. `commit(message=msg)` stores the offset *after* `msg`,
meaning "everything up to and including this record is done".

**Where it matters**

The committed offset is the consumer's checkpoint. Every recovery, deployment and scaling event starts from it, so
when it is written decides what is lost or repeated.

**Watch out for**

`auto.offset.reset` (`earliest` or `latest`) applies only when a group has no committed offset yet. A new group with
`latest` silently skips everything already in the topic. A restarted consumer also waits for its old session to
expire if the previous instance did not leave cleanly, so `session.timeout.ms` bounds how long a crash pauses its
partitions.
%% code
def worker(group, stop_after, commit_every=1):
    \"\"\"Process `stop_after` records, committing after every `commit_every`; then stop without a final commit.\"\"\"
    consumer = Consumer(
        {{
            "bootstrap.servers": BOOTSTRAP,
            "group.id": group,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "session.timeout.ms": 6000,  # short, so the restarted worker is not kept waiting for its old session
            "heartbeat.interval.ms": 500,
        }}
    )
    consumer.subscribe(["shipments"])
    processed = []
    while len(processed) < stop_after:
        msg = consumer.poll(0.2)
        if msg is None or msg.error():
            continue
        processed.append(text(msg.value()))
        if len(processed) % commit_every == 0:
            consumer.commit(message=msg, asynchronous=False)
    committed = consumer.committed([TopicPartition("shipments", partition)], timeout=10)[0].offset
    consumer.close()  # leaves the group; nothing more is committed
    return processed, committed


done, committed = worker("billing", stop_after=4)
print("first run processed:", done, "| committed offset:", committed)
done, committed = worker("billing", stop_after=2)
print("second run resumed with:", done, "| committed offset:", committed)
%% md
**What to notice:** The first run committed after each record, so its committed offset is 4: the next record to read.
The second run, a new consumer in the same `billing` group, resumed at `shipment-5` instead of starting over, and
finished at committed offset 6.
%% md
## What a crash replays

Committing after every record is safe but costs a round trip per record, so real consumers commit every few hundred
records or every few seconds. Everything processed since the last commit is processed **again** after a crash,
because the group resumes from the committed offset. That is **at-least-once** delivery: nothing is lost, and the
tail since the last commit is repeated.

The worker below commits every two records and stops after five, as if the process were killed.

**Where it matters**

Size the commit interval by how much replay the downstream can absorb, and make the processing idempotent (an upsert
by key, a deduplicating sink) so a replayed record changes nothing.

**Watch out for**

Committing **before** processing turns the replay into loss: the crashed records are marked done but never
processed. Kafka 4 shows both orderings.
%% code
done, committed = worker("shipping-labels", stop_after=5, commit_every=2)
print("before the crash:", done, "| committed offset:", committed)
replayed, committed = worker("shipping-labels", stop_after=2)
print("after restart:   ", replayed, "| committed offset:", committed)
%% md
**What to notice:** The crash happened after `shipment-5` was processed but before its batch was committed, so the
committed offset was 4. The restarted worker processed `shipment-5` a second time before moving on to `shipment-6`.
%% md
## Consumer groups and rebalancing

Consumers that share a `group.id` split a topic's partitions between them: each partition has exactly one owner in
the group, so the group reads in parallel without reading anything twice. When a consumer joins, leaves or stops
sending heartbeats, the group **rebalances**: partitions are revoked and reassigned. The `on_assign` and
`on_revoke` callbacks let a consumer react, for example by committing its progress before a partition moves away.

The cell below starts consumer A, waits until it owns every partition, then starts consumer B in the same group and
records the callbacks.

**Where it matters**

A group can have at most as many active consumers as the topic has partitions, so the partition count caps a
consumer group's parallelism. Every deployment of a consumer service causes rebalances.

**Watch out for**

This example uses the `range` assignor, an **eager** protocol: every consumer gives up all its partitions before any
are reassigned, so the whole group pauses. Production clients should use `cooperative-sticky`, which moves only the
partitions that change owner. Commit in `on_revoke`, or the new owner replays work since your last commit.
%% code
events = []
config = {{
    "bootstrap.servers": BOOTSTRAP,
    "group.id": "packers",
    "auto.offset.reset": "earliest",
    "partition.assignment.strategy": "range",
    "session.timeout.ms": 6000,
    "heartbeat.interval.ms": 500,
}}


def subscribe(name):
    consumer = Consumer(config)
    consumer.subscribe(
        ["shipments"],
        on_assign=lambda c, parts: events.append(f"{{name}} assigned {{[p.partition for p in parts]}}"),
        on_revoke=lambda c, parts: events.append(f"{{name}} revoked  {{[p.partition for p in parts]}}"),
    )
    return consumer


def poll_until(consumers, done, timeout=20):
    deadline = time.time() + timeout
    while not done() and time.time() < deadline:
        for consumer in consumers:
            consumer.poll(0.1)


a = subscribe("A")
poll_until([a], lambda: len(a.assignment()) == 4)
b = subscribe("B")
poll_until([a, b], lambda: b.assignment())
print("\\n".join(events))
print("A owns", sorted(p.partition for p in a.assignment()), "| B owns", sorted(p.partition for p in b.assignment()))
%% md
**What to notice:** A first owned all four partitions. When B joined, A had to revoke **all** of them, including the
two it would get back, before the group gave two partitions to each consumer. Which two each gets depends on member
IDs and changes from run to run; the full stop does not, and it is the cost of an eager rebalance.
%% md
## Measuring lag

**Consumer lag** is how far a group is behind the end of a partition: the partition's **high watermark** (the offset
the next record will get) minus the group's committed offset. Lag that keeps growing means the consumers cannot keep
up; lag that spikes and recovers usually means a rebalance or a slow downstream.

**Where it matters**

Lag in records, and the age of the oldest unprocessed record, are the main health signals of a streaming pipeline.
Alert on sustained growth, not on a single high reading.

**Watch out for**

Lag counts records, not time or work. One partition with a hot key can lag far behind the others while the group's
total looks fine, so watch per-partition lag.
%% code
a.close()
b.close()
produce("shipments", [("warehouse-1", f"shipment-{{i}}") for i in range(7, 11)])


def lag(group):
    probe = Consumer({{"bootstrap.servers": BOOTSTRAP, "group.id": group}})
    tp = TopicPartition("shipments", partition)
    committed = probe.committed([tp], timeout=10)[0].offset
    _, high = probe.get_watermark_offsets(tp, timeout=10)
    probe.close()
    return {{"committed": committed, "high_watermark": high, "lag": high - committed}}


for group in ["billing", "shipping-labels"]:
    print(group, lag(group))
%% md
**What to notice:** Four new shipments raised the high watermark to 10. Both groups had committed offset 6, so each
now lags by four records, until its consumers run again.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Catch up and check lag

**Difficulty:** Easy · about 10 min

Run the `billing` group until it has processed the four new shipments, then show that its lag is zero.
%% code
# Try your solution here.
%% solution
caught_up, _ = worker("billing", stop_after=4)
print(caught_up)
print(lag("billing"))
%% md
### Exercise 2: Choose a commit interval

**Difficulty:** Medium · about 15 min

A new group `reports` processes the ten shipments, committing every three records, and crashes after the eighth.
Predict which shipments are processed twice, then check your prediction.
%% code
# Try your solution here.
%% solution
first, committed = worker("reports", stop_after=8, commit_every=3)
print("committed offset after the crash:", committed)  # the last commit came after the sixth record
again, _ = worker("reports", stop_after=4)
print("processed twice:", sorted(set(first) & set(again)))
%% md
### Exercise 3: Three workers, four partitions

**Difficulty:** Medium · about 15 min

Start three consumers in a new group with the `range` assignor. How many partitions does each one own, and why can a
fourth consumer not make this group any faster on a four-partition topic?
%% code
# Try your solution here.
%% solution
events.clear()
config["group.id"] = "three-workers"
workers = [subscribe(name) for name in "XYZ"]
poll_until(workers, lambda: sum(len(w.assignment()) for w in workers) == 4 and all(w.assignment() for w in workers))
for name, w in zip("XYZ", workers):
    print(name, sorted(p.partition for p in w.assignment()))
for w in workers:
    w.close()
print("A fourth consumer would own one partition and leave a fifth idle: parallelism is capped at 4.")
%% md
## Key takeaways

- A group's committed offset is its checkpoint: a restarted consumer resumes there, and `auto.offset.reset` applies
  only when there is none.
- Committing after processing gives at-least-once delivery. Everything since the last commit is replayed after a
  crash, so make processing idempotent and choose the commit interval deliberately.
- A group spreads partitions over its consumers, one owner each, so the partition count caps parallelism. Joins,
  leaves and deployments trigger rebalances.
- Prefer the `cooperative-sticky` assignor and commit in `on_revoke`; eager assignors pause the whole group.
- Lag is high watermark minus committed offset, per partition. Watch its trend, not one reading.
%% md
**Next:** [Kafka 4: Delivery guarantees and transactions](kafka-04-delivery-and-transactions.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
