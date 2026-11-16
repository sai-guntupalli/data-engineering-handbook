"""Shared header and setup for the Kafka lessons (all run against librdkafka's built-in mock cluster)."""

SETUP_PIP = """%% code
# Setup: install notebook dependencies in Colab.
!pip install -q confluent-kafka~=2.16"""

INTRO = """Every example uses the real `confluent-kafka` client against **librdkafka's mock cluster**: three brokers that run
inside the client library on localhost. There is nothing to download and no server to start, and the producer,
consumer and transaction APIs are the ones you would use against a production cluster. The mock cluster does not
model disk, replication timing or broker failures, so latency and durability numbers here mean nothing; behavior
does."""

HELPERS = '''%% code
import time

from confluent_kafka import Consumer, KafkaException, Producer, TopicPartition

# The mock cluster lives as long as this client; other clients reach it through its bootstrap address.
cluster = Producer({"test.mock.num.brokers": 3})
BOOTSTRAP = ",".join(f"{b.host}:{b.port}" for b in cluster.list_topics(timeout=10).brokers.values())


def text(raw):
    return raw.decode() if raw is not None else None


def produce(topic, records, **config):
    """Send (key, value) pairs; return (partition, offset, key, value) from each delivery report, in log order."""
    producer = Producer({"bootstrap.servers": BOOTSTRAP, **config})
    delivered = []

    def report(err, msg):
        if err is not None:
            raise KafkaException(err)
        delivered.append((msg.partition(), msg.offset(), text(msg.key()), text(msg.value())))

    for key, value in records:
        producer.produce(topic, key=key, value=value, on_delivery=report)
    producer.flush(10)
    return sorted(delivered)


def consume(topic, group, expected, timeout=20, **config):
    """Read `expected` records with a consumer in `group`; return (partition, offset, key, value) in arrival order."""
    consumer = Consumer(
        {"bootstrap.servers": BOOTSTRAP, "group.id": group, "auto.offset.reset": "earliest", **config}
    )
    consumer.subscribe([topic])
    records, deadline = [], time.time() + timeout
    while len(records) < expected and time.time() < deadline:
        msg = consumer.poll(0.2)
        if msg is not None and not msg.error():
            records.append((msg.partition(), msg.offset(), text(msg.key()), text(msg.value())))
    consumer.close()
    return records


print("mock brokers:", len(BOOTSTRAP.split(",")))'''
