import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from kafka_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/kafka/kafka-02-producers.ipynb"
SPEC = f"""%% md
# Kafka 2: Producers, batching and retries

A producer call returns before the record is stored. This lesson follows a record from `produce()` to the broker's
acknowledgement: how delivery reports tell you what actually happened, how batching and compression trade a few
milliseconds for far fewer requests and bytes, and what idempotence does and does not protect you from.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell starts the mock cluster and defines the `produce` and `consume` helpers from Kafka 1. The sample data is
a stream of JSON order events built in the examples.

{HELPERS}
%% md
## Delivery reports and acknowledgements

`produce()` only places the record in the client's in-memory buffer and returns at once. A background thread
batches and sends it, and the broker's answer arrives later as a **delivery report**: a callback with either the
record's partition and offset or an error. `flush()` waits until every buffered record has a report.

How long the broker waits before answering is the `acks` setting:

```text
acks=0    the producer does not wait: fastest, and a lost record is never reported
acks=1    the partition leader has written it: lost if the leader dies before followers copy it
acks=all  every in-sync replica has it: the default with idempotence, and the only safe choice for pipelines
```

Some errors are known before anything is sent. A record larger than `message.max.bytes` is rejected by
`produce()` itself.

**Where it matters**

A pipeline that never checks delivery reports cannot tell a stored record from a dropped one. Count failures in the
callback and fail the job, or retry, before you advance any checkpoint.

**Watch out for**

Exiting without `flush()` silently discards buffered records. And a `BufferError` from `produce()` means the local
queue is full: call `poll()` or `flush()` to drain it rather than dropping the record.
%% code
producer = Producer({{"bootstrap.servers": BOOTSTRAP, "acks": "all", "message.max.bytes": 1000}})
outcomes = []


def report(err, msg):
    outcomes.append(("failed: " + err.str()) if err else f"stored at partition {{msg.partition()}} offset {{msg.offset()}}")


producer.produce("payments", key="payment-1", value='{{"amount_cents": 1200}}', on_delivery=report)
print("right after produce():", outcomes)
producer.flush(10)
print("after flush():", outcomes)

try:
    producer.produce("payments", key="payment-2", value="x" * 5000, on_delivery=report)
except KafkaException as error:
    print("rejected before sending:", error.args[0].name())
%% md
**What to notice:** Immediately after `produce()` there is no outcome yet; the report only arrives during `flush()`.
The 5,000-byte record never reached the broker: the client rejected it with `MSG_SIZE_TOO_LARGE` because it exceeds
`message.max.bytes`.
%% md
## Batching with linger.ms

Every request to a broker has a fixed cost, so the producer groups records for the same partition into **batches**.
`linger.ms` is how long it waits for more records before sending a partly filled batch, and `batch.size` caps a
batch's bytes. With `linger.ms=0` it sends as soon as it can, which under steady load means many tiny requests.

The cell below sends the same 2,000 events twice and reads the client's own statistics to count requests sent to
the brokers.

**Where it matters**

High-volume producers (clickstreams, CDC, log shipping) are usually limited by request count, not bytes. A few
milliseconds of linger is often the cheapest throughput gain available.

**Watch out for**

Linger adds up to that many milliseconds of latency to every record. For a latency-sensitive path, keep it small and
measure end-to-end time rather than raising it blindly.
%% code
import json


def send_with_stats(topic, count=2000, **config):
    stats = []
    producer = Producer(
        {{"bootstrap.servers": BOOTSTRAP, "statistics.interval.ms": 100, "stats_cb": stats.append, **config}}
    )
    for i in range(count):
        event = {{"order_id": i, "status": "placed", "amount_cents": 1200 + i % 7}}
        producer.produce(topic, key=f"order-{{i % 50}}", value=json.dumps(event))
        producer.poll(0)
    producer.flush(10)
    time.sleep(0.3)
    producer.poll(0.1)
    last = json.loads(stats[-1])
    brokers = [b for b in last["brokers"].values() if b["nodeid"] >= 0]
    return {{"records": last["txmsgs"], "requests": sum(b["tx"] for b in brokers), "bytes_sent": sum(b["txbytes"] for b in brokers)}}


eager = send_with_stats("clicks-eager", **{{"linger.ms": 0}})
lingering = send_with_stats("clicks-linger", **{{"linger.ms": 50}})
print("linger.ms=0: ", eager)
print("linger.ms=50:", lingering)
print("requests saved:", f"{{1 - lingering['requests'] / eager['requests']:.0%}}")
%% md
**What to notice:** Both runs delivered all 2,000 records. With `linger.ms=0` the producer needed hundreds of
requests (the exact number changes from run to run with timing); with 50 ms of linger it needed about ten, and sent
fewer bytes because each request carries its own overhead.
%% md
## Compression

Compression is applied **per batch**, so it works better as batches grow: repeated field names and values in JSON
compress very well. The broker stores the compressed batch as is, and consumers decompress it, so compression also
shrinks disk usage and the traffic to every consumer group.

**Where it matters**

Cross-zone and cross-region traffic is billed per byte in the cloud, and JSON or Avro event streams typically
compress several times over. `zstd` or `lz4` is a sensible default for new topics.

**Watch out for**

Compression costs producer CPU, and tiny batches (`linger.ms=0` with low traffic) barely compress. Set it together
with linger, and check the topic's own `compression.type` so the broker does not recompress.
%% code
plain = send_with_stats("orders-plain", **{{"linger.ms": 50, "compression.type": "none"}})
packed = send_with_stats("orders-zstd", **{{"linger.ms": 50, "compression.type": "zstd"}})
print("none:", plain["bytes_sent"], "bytes sent")
print("zstd:", packed["bytes_sent"], "bytes sent", f"({{plain['bytes_sent'] / packed['bytes_sent']:.0f}}x smaller)")
%% md
**What to notice:** The same 2,000 events took about 150 KB uncompressed and about 11 KB with zstd, more than ten
times smaller. Repetitive JSON is close to the best case; varied binary data compresses far less.
%% md
## Idempotence covers retries, not resends

Networks lose acknowledgements. If the broker stores a batch but its answer is lost, the producer retries, and
without protection the batch is written twice. With `enable.idempotence=true` (the default in recent clients) the
producer has an ID and numbers its batches per partition, and the broker discards a batch whose sequence number it
has already stored. Retries inside one producer session therefore never duplicate records.

Idempotence knows nothing about your business events. If your **application** times out and calls `produce()` again
with the same event, or a restarted job resends a file, those are new records with new sequence numbers.

**Where it matters**

Keep idempotence on, and give every event a stable ID (an order event ID, a CDC log position) so consumers can
recognize an application-level resend.

**Watch out for**

Idempotence protects one producer instance per partition. A new process gets a new producer ID, so a job that crashes
and resends its last batch produces duplicates that only a stable event ID can catch.
%% code
resend = [
    ("order-20", '{{"event_id": "e-1", "status": "placed"}}'),
    ("order-20", '{{"event_id": "e-1", "status": "placed"}}'),  # the application retried after a timeout
    ("order-20", '{{"event_id": "e-2", "status": "paid"}}'),
]
stored = produce("orders-idempotent", resend, **{{"enable.idempotence": True}})
print("records in the log:", [(offset, json.loads(value)["event_id"]) for _, offset, _, value in stored])

seen, applied = set(), []
for _, _, _, value in consume("orders-idempotent", group="sink", expected=len(stored)):
    event = json.loads(value)
    if event["event_id"] not in seen:
        seen.add(event["event_id"])
        applied.append(event["status"])
print("applied once per event_id:", applied)
%% md
**What to notice:** The idempotent producer stored all three records, at offsets 0, 1 and 2, because the resend was a
new `produce()` call. Only the consumer's check on `event_id` collapsed them to one `placed` and one `paid`.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Count failed deliveries

**Difficulty:** Easy · about 10 min

Send ten records to `audit-log` with a producer whose `message.max.bytes` is 1,000 (the smallest allowed); make every third record 2,000
bytes. Count how many were stored and how many were rejected, without letting the job crash.
%% code
# Try your solution here.
%% solution
small = Producer({{"bootstrap.servers": BOOTSTRAP, "message.max.bytes": 1000}})
stored, rejected = [], []
for i in range(10):
    value = "x" * (2000 if i % 3 == 0 else 50)
    try:
        small.produce("audit-log", key=str(i), value=value, on_delivery=lambda err, msg: (rejected if err else stored).append(msg))
    except KafkaException:
        rejected.append(i)
small.flush(10)
print("stored:", len(stored), "rejected:", len(rejected))
%% md
### Exercise 2: Find a linger setting

**Difficulty:** Medium · about 10 min

Use `send_with_stats` to compare `linger.ms` of 5, 20 and 100. Which is the smallest value that keeps requests
within about twice the 100 ms result?
%% code
# Try your solution here.
%% solution
results = {{linger: send_with_stats(f"clicks-{{linger}}", **{{"linger.ms": linger}})["requests"] for linger in (5, 20, 100)}}
print(results)
print("smallest good-enough linger:", min(linger for linger, requests in results.items() if requests <= 2 * results[100]))
%% md
### Exercise 3: Make a resend harmless

**Difficulty:** Medium · about 15 min

A job resends a whole file of payments after a crash. Produce payments `p-1` to `p-4`, then `p-3` and `p-4` again,
and compute a total that counts each payment once. Each value is a JSON object with `payment_id` and `cents`.
%% code
# Try your solution here.
%% solution
payments = [{{"payment_id": f"p-{{i}}", "cents": 100 * i}} for i in range(1, 5)]
produce("payments-file", [(p["payment_id"], json.dumps(p)) for p in payments + payments[2:]])
latest = {{}}
for _, _, key, value in consume("payments-file", group="ex3", expected=6):
    latest[key] = json.loads(value)["cents"]
print("naive total would be", sum(p["cents"] for p in payments + payments[2:]), "- deduplicated total:", sum(latest.values()))
%% md
## Key takeaways

- `produce()` only buffers a record. The delivery report is the outcome, and `flush()` before exit is mandatory.
- Use `acks=all` for pipeline data; with fewer acknowledgements, a broker failure can lose records the producer
  believes were sent.
- A few milliseconds of `linger.ms` turns hundreds of tiny requests into a handful of batches, and compression is
  applied per batch, so the two work together.
- Idempotence stops duplicates from the client's own retries. Application resends still need a stable event ID that
  consumers deduplicate on.
%% md
**Next:** [Kafka 3: Consumers and groups](kafka-03-consumers-and-groups.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
