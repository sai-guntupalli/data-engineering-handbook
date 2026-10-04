## [Main title](../README.md)
### [Interview questions](full.md)

# Apache Flume

**Notebook:** [`notebooks/topics/flume.ipynb`](../notebooks/topics/flume.ipynb) - runnable version of this topic with self-checking exercises.

Apache Flume is a distributed, reliable, and available service for efficiently collecting, aggregating, and moving large amounts of log and event data into HDFS, HBase, Kafka, Solr, or another agent. An agent is a JVM process that wires a source to one or more channels and a sink, and the channel is what makes every handoff transactional.

```text
source -> interceptors -> channel selector -> channel (buffer) -> sink -> storage / next agent
```

Key ideas:

+ A source writes events into a channel; it never writes directly to HDFS.
+ A channel is the durability boundary: memory for speed, file or JDBC for survival across restarts.
+ A sink removes an event from the channel only after the destination acknowledges the batch.
+ The unit of transfer is a transaction; reliability comes from commit/rollback across source, channel, and sink.

+ [What is Flume?](#What-is-Flume)
+ [Where does Apache Flume fit in modern data platforms?](#Where-does-Apache-Flume-fit-in-modern-data-platforms)
+ [How do Flume memory channels and file channels differ?](#How-do-Flume-memory-channels-and-file-channels-differ)
+ [What is Apache Flume?](#What-is-Apache-Flume)
+ [Which is the reliable channel in Flume to ensure that there is no Data Loss?](#Which-is-the-reliable-channel-in-Flume-to-ensure-that-there-is-no-Data-Loss)
+ [How can Flume be used with Hbase?](#How-can-Flume-be-used-with-Hbase)
+ [What is an Agent?](#What-is-an-Agent)
+ [Is it possible to Leverage Real Time Analysis on the Big Data collected by Flume directly?](#Is-it-possible-to-Leverage-Real-Time-Analysis-on-the-Big-Data-collected-by-Flume-directly)
+ [What is a Channel?](#What-is-a-Channel)
+ [Explain about the different channel types in Flume and which channel type is faster?](#Explain-about-the-different-channel-types-in-Flume-and-which-channel-type-is-faster)
+ [Explain about the replication and multiplexing selectors in Flume?](#Explain-about-the-replication-and-multiplexing-selectors-in-Flume)
+ [Does Apache Flume provide support for third party Plugins?](#Does-Apache-Flume-provide-support-for-third-party-Plugins)
+ [Differentiate between FileSink and FileRollSink?](#Differentiate-between-FileSink-and-FileRollSink)
+ [Why we are using Flume?](#Why-we-are-using-Flume)
+ [What is Flumeng?](#What-is-Flumeng)
+ [What are the complicated steps in Flume configurations?](#What-are-the-complicated-steps-in-Flume-configurations)
+ [What are Flume core components?](#What-are-Flume-core-components)
+ [What are the Data Extraction Tools in Hadoop?](#What-are-the-Data-Extraction-Tools-in-Hadoop)
+ [Does Flume provide 100 percents reliability to the Data Flow?](#Does-Flume-provide-100-percents-reliability-to-the-Data-Flow)
+ [Tell any two Features of Flume?](#Tell-any-two-Features-of-Flume)
+ [What are Interceptors?](#What-are-Interceptors)
+ [Why Flume?](#Why-Flume)
+ [What is Flume Event?](#What-is-Flume-Event)
+ [How Multi hop agent can be setup in Flume?](#How-Multi-hop-agent-can-be-setup-in-Flume)
+ [Can Flume can distribute data to multiple destinations?](#Can-Flume-can-distribute-data-to-multiple-destinations)
+ [Can you explain about configuration files?](#Can-you-explain-about-configuration-files)
+ [How do you write a complete Flume agent configuration?](#How-do-you-write-a-complete-Flume-agent-configuration)
+ [How do you configure a Flume agent to write to Kafka?](#How-do-you-configure-a-Flume-agent-to-write-to-Kafka)
+ [How do you use interceptors in a Flume configuration?](#How-do-you-use-interceptors-in-a-Flume-configuration)
+ [How do you configure reliability and failover in Flume?](#How-do-you-configure-reliability-and-failover-in-Flume)
+ [How do you monitor and tune a Flume agent?](#How-do-you-monitor-and-tune-a-Flume-agent)
+ [How does Flume compare with Kafka Connect, Fluentd, and Filebeat?](#How-does-Flume-compare-with-Kafka-Connect-Fluentd-and-Filebeat)
+ [When should you not use Flume?](#When-should-you-not-use-Flume)
+ [What are the similarities and differences between Apache Flume and Apache Kafka?](#What-are-the-similarities-and-differences-between-Apache-Flume-and-Apache-Kafka)
+ [Explain Reliability and Failure Handling in Apache Flume?](#Explain-Reliability-and-Failure-Handling-in-Apache-Flume)
+ [Real world use cases for Flume](#Real-world-use-cases-for-Flume)

## What is Flume?
Flume is a distributed, reliable, and available service for efficiently collecting, aggregating, and moving large amounts of log data. It has a simple and flexible architecture based on streaming data flows. It is robust and fault tolerant with tunable reliability mechanisms and many failover and recovery mechanisms, and it uses an extensible data model that allows for online analytic applications.

```text
web/app servers --taildir--> agent --file channel--> HDFS sink --> partitioned log archive
```

The reliability story in one sentence: the source and the sink each run a transaction against the channel, so an event is either committed end to end or replayed from the channel.

[Table of Contents](#Apache-Flume)

## Where does Apache Flume fit in modern data platforms?
Flume is used for reliably collecting, aggregating, and moving log and event data into storage systems such as HDFS or HBase. In modern stacks Kafka, cloud-native streaming services, and lightweight collectors are more common, but Flume remains a useful model for source-channel-sink pipeline design and is still found in Hadoop-era clusters and edge aggregation layers.

Example flow:

```text
web server logs -> Flume source -> memory/file channel -> HDFS sink
```

The important concept is the durable handoff between components. Channels buffer events so that a short downstream failure does not immediately lose data.

[Table of Contents](#Apache-Flume)

## How do Flume memory channels and file channels differ?
A memory channel is fast but loses buffered events if the agent JVM dies. A file channel is slower but durable because events and checkpoints are written to disk before delivery. Choose based on whether throughput or durability matters more.

+ memory channel: high-volume ephemeral logs where a small loss is acceptable
+ file channel: audit, security, or billing logs where loss is unacceptable
+ JDBC channel: durable and transactional via an embedded Derby database, but rarely the fastest or the most commonly deployed today

For critical pipelines, file channels plus careful disk sizing and monitoring of channel fill percentage are safer.

```properties
# File channel: durable, survives agent restart
a1.channels.c1.type = file
a1.channels.c1.checkpointDir = /data/flume/checkpoint
a1.channels.c1.dataDirs = /data/flume/data
a1.channels.c1.capacity = 1000000
a1.channels.c1.transactionCapacity = 10000
a1.channels.c1.checkpointInterval = 30000
a1.channels.c1.keep-alive = 3
```

[Table of Contents](#Apache-Flume)

## What is Apache Flume?
Apache Flume is a distributed, reliable, and available system for efficiently collecting, aggregating, and moving large amounts of log data from many different sources to a centralized store such as HDFS or HBase. Flume is a framework for populating Hadoop with data: agents are deployed across the IT infrastructure - inside web servers, application servers, and network devices - to collect data and integrate it into Hadoop.

A common historical example is Mozilla collecting browser telemetry with Flume into Hive for analysis. The same design still appears as an edge aggregation tier that forwards into Kafka.

[Table of Contents](#Apache-Flume)

## Which is the reliable channel in Flume to ensure that there is no Data Loss?
The FILE channel is the most reliable of the built-in channels (JDBC, FILE, MEMORY). The file channel writes each event to disk and keeps a checkpoint, so a restart replays anything that was not acknowledged by the sink.

```properties
a1.channels.c1.type = file
a1.channels.c1.dataDirs = /data/flume/data
a1.channels.c1.checkpointDir = /data/flume/checkpoint
```

Reliability also depends on the source and sink semantics: a durable channel cannot make an unreliable source or a non-transactional sink exactly once, it can only guarantee that committed events are not lost.

[Table of Contents](#Apache-Flume)

## How can Flume be used with Hbase?
Apache Flume can write to HBase through one of two sinks:

+ HBaseSink (`org.apache.flume.sink.hbase.HBaseSink`) supports secure HBase clusters and the newer HBase IPC introduced in HBase 0.96.
+ AsyncHBaseSink (`org.apache.flume.sink.hbase.AsyncHBaseSink`) has better performance because it makes non-blocking calls to HBase.

How HBaseSink works:

+ A Flume event is converted into HBase increments or puts by an `HBaseEventSerializer` that is instantiated when the sink starts.
+ For every event the sink calls the serializer, which translates the event into increments and puts sent to the HBase cluster.

How AsyncHBaseSink works:

+ AsyncHBaseSink implements `AsyncHBaseEventSerializer`; `initialize` is called once when the sink starts.
+ The sink calls `setEvent`, then `getIncrements` and `getActions`, and calls `cleanUp` when it stops.

```properties
# HBase sink with a regex serializer that extracts the row key from the body
a1.sinks.k1.type = hbase
a1.sinks.k1.table = metrics
a1.sinks.k1.columnFamily = d
a1.sinks.k1.serializer = org.apache.flume.sink.hbase.RegexHbaseEventSerializer
a1.sinks.k1.serializer.regex = ^([^|]+)\|([^|]+)\|(.*)$
a1.sinks.k1.serializer.colNames = host,metric,value
a1.sinks.k1.batchSize = 100
a1.sinks.k1.channel = c1
```

[Table of Contents](#Apache-Flume)

## What is an Agent?
An agent is a process that hosts Flume components such as sources, channels, and sinks, and therefore has the ability to receive, store, and forward events to their destination. Every agent has its own name and its own configuration block (for example `a1.sources`, `a1.channels`, `a1.sinks`).

```bash
# Start one agent named a1 with a properties config file
flume-ng agent --conf /etc/flume/conf --conf-file /etc/flume/conf/weblogs.conf -n a1 \
  -Dflume.root.logger=INFO,console
```

[Table of Contents](#Apache-Flume)

## Is it possible to Leverage Real Time Analysis on the Big Data collected by Flume directly?
Yes. Data from Flume can be extracted, transformed, and loaded in real time into Apache Solr using `MorphlineSolrSink`, or written into a low-latency store such as HBase for key lookups. For true streaming analytics, the more common pattern is to land events in Kafka and let a stream processor such as Flink or Spark Structured Streaming consume them.

```text
Flume -> MorphlineSolrSink -> Solr index -> search and faceted queries
```

[Table of Contents](#Apache-Flume)

## What is a Channel?
A channel stores events. Events are delivered to the channel by sources running inside the agent, and an event stays in the channel until a sink removes it for further transport. It decouples producers from consumers and absorbs downstream outages.

[Table of Contents](#Apache-Flume)

## Explain about the different channel types in Flume and which channel type is faster?
The built-in channel types are:

+ MEMORY channel - events are held in an in-memory queue and passed to the sink; fastest, with the risk of data loss on agent failure.
+ JDBC channel - events are stored in an embedded Derby database; durable but slow for very high throughput.
+ FILE channel - events are written to files on the local filesystem after the source reads them, and are deleted only after successful delivery to the sink.
+ KAFKA channel - events are stored in a Kafka topic, giving durability plus the ability to serve multiple consumers; a good bridge between Flume collection and a Kafka-centric platform.
+ SPILLABLE MEMORY channel - memory first, spilling to disk when a threshold is reached; a middle ground between memory and file.

MEMORY is the fastest channel, but it has the risk of data loss. The right choice depends on the value of each event and the acceptable recovery path.

| Channel | Speed | Durability | Typical use |
|---|---|---|---|
| memory | highest | none across restart | high-volume, loss-tolerant logs |
| file | medium | high | audit, billing, security logs |
| jdbc | low | high | small legacy pipelines |
| kafka | medium-high | high | decoupled multi-consumer ingestion |
| spillable memory | high until spill | medium | bursty traffic with a disk safety net |

[Table of Contents](#Apache-Flume)

## Explain about the replication and multiplexing selectors in Flume?
Channel selectors decide which channels a source writes to. With no selector configured, the default is the replicating selector, which writes the same event to every channel in the source's `channels` list. The multiplexing selector routes each event to one or more channels based on a header value.

```properties
# Replication: every event goes to both channels
a1.sources.r1.channels = c1 c2
a1.sources.r1.selector.type = replicating

# Multiplexing: route by the "type" header
a1.sources.r1.channels = errors info
a1.sources.r1.selector.type = multiplexing
a1.sources.r1.selector.header = type
a1.sources.r1.selector.mapping.errors = errors
a1.sources.r1.selector.mapping.info = info
a1.sources.r1.selector.default = info
```

Replication is used for fan-out to multiple destinations; multiplexing is used to split different event classes cheaply at the source.

[Table of Contents](#Apache-Flume)

## Does Apache Flume provide support for third party Plugins?
Yes. Flume has a plug-in based architecture: sources, channels, sinks, serializers, and interceptors are all configurable class names, so custom implementations can load data from external sources and transfer it to external destinations. A custom sink is written by implementing the Sink interface and packaging the class on the agent classpath.

[Table of Contents](#Apache-Flume)

## Differentiate between FileSink and FileRollSink?
HDFS File Sink (`hdfs`) writes events into the Hadoop Distributed File System, while File Roll Sink (`file_roll`) stores events in the local filesystem of the agent host, rolling files by size or count.

```properties
# Roll local files every 10 MB, keeping 24 files
a1.sinks.k1.type = file_roll
a1.sinks.k1.sink.directory = /var/flume/roll
a1.sinks.k1.sink.rollInterval = 0
a1.sinks.k1.sink.batchSize = 100
a1.sinks.k1.sink.serializer = text
```

[Table of Contents](#Apache-Flume)

## Why we are using Flume?
Hadoop developers use Flume to pull data from sources such as social media, web servers, and application logs. It was developed at Cloudera for aggregating and moving very large amounts of data. The primary use is to gather log files from many sources and asynchronously persist them into the Hadoop cluster, with buffering that tolerates downstream outages.

[Table of Contents](#Apache-Flume)

## What is Flumeng?
Flume NG is the second-generation Flume agent architecture: a single JVM agent with pluggable sources, channels, sinks, and interceptors. It stores data in HDFS or HBase and replaced the original multi-process "Flume OG" design. Modern Apache Flume documentation describes Flume NG.

[Table of Contents](#Apache-Flume)

## What are the complicated steps in Flume configurations?
Flume processes streaming data, so once started there is no natural stop or end to the process; it flows data from source to sink through an agent continuously. The agent must be told how its components connect, and external sources add their own credentials. For example, downloading from Twitter requires `consumerKey`, `consumerSecret`, `accessToken`, and `accessTokenSecret`.

The steps that cause the most incidents in practice:

+ Matching source, channel, and sink names consistently across the three lists.
+ Sizing a file channel (capacity, transactionCapacity, disk) so it cannot fill up.
+ Choosing the right HDFS sink parameters (`rollSize`, `rollCount`, `round`, `hdfs.fileType`).
+ Handling HDFS `append` vs `create` and small-file accumulation.
+ Restarting an agent without losing the file channel checkpoint.

```bash
# Validate a config without starting the agent
flume-ng agent --conf /etc/flume/conf --conf-file /etc/flume/conf/weblogs.conf -n a1 \
  -Dflume.root.logger=DEBUG,console --dry-run
```

[Table of Contents](#Apache-Flume)

## What are Flume core components?
Source, channel, and sink are the core components.

+ A Flume source receives an event from an external source and stores it in one or more channels.
+ A Flume channel temporarily stores the event until it is consumed by a sink; it acts as the repository that decouples the two sides.
+ A Flume sink removes the event from the channel and puts it into an external repository such as HDFS or HBase, or forwards it to the next Flume agent.

Additional components are interceptors (mutate/filter events in flight), channel selectors (route events to channels), and sink processors (load balancing and failover across sinks).

[Table of Contents](#Apache-Flume)

## What are the Data Extraction Tools in Hadoop?
Sqoop transfers data between relational databases and HDFS, while Flume extracts streaming data from sources such as social media and web logs and stores it in HDFS. In a modern stack these are joined by Kafka Connect (database and service connectors), Debezium (CDC), and cloud-native transfer services.

[Table of Contents](#Apache-Flume)

## Does Flume provide 100 percents reliability to the Data Flow?
Flume provides end-to-end reliability when it is configured with durable components, because of its transactional approach: the source and sink each commit against the channel. "100%" is a design property, not a default - a memory channel or a non-transactional sink breaks it. There is also no end-to-end exactly-once guarantee to arbitrary destinations; the guarantee is at-least-once plus idempotency at the sink.

[Table of Contents](#Apache-Flume)

## Tell any two Features of Flume?
+ Flume collects, aggregates, and moves large amounts of log data from many different sources to a centralized data store.
+ Flume is not restricted to log data: it can transport network traffic data, social-media data, email messages, and pretty much any event data.
+ It has tunable reliability (memory vs file channel) and supports failover and load balancing across sinks.

[Table of Contents](#Apache-Flume)

## What are Interceptors?
Interceptors sit between a source and a channel and can inspect or modify events in flight. They are configured as a chain, and each interceptor returns the same event or a modified one; dropping an event is done with a channel selector or a filter interceptor.

Common built-in interceptors:

+ `timestamp` - inserts the collector time into a header.
+ `host` - inserts the agent hostname.
+ `static` - inserts fixed key/value headers.
+ `regex_filter` - drops events matching (or not matching) a regex.
+ `regex_extractor` - extracts fields from the body into headers.
+ `uuid` - adds a random UUID header.

```properties
a1.sources.r1.interceptors = i1 i2 i3
a1.sources.r1.interceptors.i1.type = timestamp
a1.sources.r1.interceptors.i2.type = host
a1.sources.r1.interceptors.i2.preserveExisting = false
a1.sources.r1.interceptors.i3.type = regex_filter
a1.sources.r1.interceptors.i3.regex = ^.*ERROR.*$
a1.sources.r1.interceptors.i3.excludeEvents = false
```

[Table of Contents](#Apache-Flume)

## Why Flume?
Flume is not limited to collecting logs from distributed systems; it is also capable of other use cases such as:

+ Collecting readings from an array of sensors.
+ Collecting impressions from custom apps for an ad network.
+ Collecting readings from network devices to monitor their performance.

Flume targets reliability, scalability, manageability, and extensibility while serving many clients with high QoS.

[Table of Contents](#Apache-Flume)

## What is Flume Event?
An event is the unit of data that Flume transports: a byte payload plus a set of string headers. The external source sends events to the source, and internally Flume understands the source format. Each event has a header section (metadata) and a body (the value).

```text
Event {
  headers: { host: web-07, timestamp: 1759600000000 },
  body:    "2026-10-04T13:20:34Z INFO checkout order=88217 amount=42.10"
}
```

Headers are the hook for routing: channel selectors and HDFS sinks read them to decide where an event goes.

[Table of Contents](#Apache-Flume)

## How Multi hop agent can be setup in Flume?
An Avro RPC bridge is used to set up a multi-hop agent: the first agent ends with an Avro sink, the next agent starts with an Avro source on a port, and the event flows across the network with transaction guarantees at both ends.

```properties
# Agent on the edge: tail local logs, forward over Avro
edge.sources.r1.type = taildir
edge.sources.r1.filegroups = f1
edge.sources.r1.filegroups.f1 = /var/log/app/.*\.log
edge.sources.r1.channels = c1
edge.channels.c1.type = file
edge.channels.c1.checkpointDir = /data/flume/edge/checkpoint
edge.channels.c1.dataDirs = /data/flume/edge/data
edge.sinks.k1.type = avro
edge.sinks.k1.hostname = collector.example.com
edge.sinks.k1.port = 4141
edge.sinks.k1.channel = c1
```

```properties
# Collector agent: receive Avro, write to HDFS
col.sources.r1.type = avro
col.sources.r1.bind = 0.0.0.0
col.sources.r1.port = 4141
col.sources.r1.channels = c1
col.channels.c1.type = file
col.channels.c1.checkpointDir = /data/flume/col/checkpoint
col.channels.c1.dataDirs = /data/flume/col/data
col.sinks.k1.type = hdfs
col.sinks.k1.hdfs.path = hdfs://nn/logs/app/%Y/%m/%d/%H
col.sinks.k1.hdfs.filePrefix = events-
col.sinks.k1.hdfs.fileType = DataStream
col.sinks.k1.hdfs.rollSize = 134217728
col.sinks.k1.hdfs.rollCount = 0
col.sinks.k1.channel = c1
```

[Table of Contents](#Apache-Flume)

## Can Flume can distribute data to multiple destinations?
Yes. Flume supports multiplexing and replication. An event can flow from one source to multiple channels and thus multiple destinations; replication is the default selector behavior when multiple channels are listed.

```properties
a1.sources.r1.channels = c1 c2
a1.sources.r1.selector.type = replicating
a1.sinks.k1.channel = c1
a1.sinks.k2.channel = c2
```

To fan out at the sink layer, a sink group with a load-balancing or failover processor sends each batch to one of several sinks.

```properties
a1.sinkgroups = g1
a1.sinkgroups.g1.sinks = k1 k2
a1.sinkgroups.g1.processor.type = load_balance
a1.sinkgroups.g1.processor.selector = round_robin
a1.sinkgroups.g1.processor.backoff = true
```

[Table of Contents](#Apache-Flume)

## Can you explain about configuration files?
The agent configuration is stored in a local properties file that describes each agent's source, channel, and sink wiring plus their type-specific parameters. The `--conf-file` argument points to it and `-n` names the agent.

A minimal complete agent: spool a directory into a memory channel and log the events.

```properties
# /etc/flume/conf/spool-to-logger.conf
a1.sources = r1
a1.channels = c1
a1.sinks = k1

a1.sources.r1.type = spooldir
a1.sources.r1.spoolDir = /var/spool/incoming
a1.sources.r1.fileSuffix = .DONE
a1.sources.r1.deletePolicy = never

a1.channels.c1.type = memory
a1.channels.c1.capacity = 100000
a1.channels.c1.transactionCapacity = 1000

a1.sinks.k1.type = logger
a1.sinks.k1.maxBytesToLog = 256

a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```

The same file can define several agents; each agent is a separate JVM started with its own `-n` argument.

[Table of Contents](#Apache-Flume)

## How do you write a complete Flume agent configuration?
A production log pipeline needs a directory source, a durable channel, and an HDFS sink whose path is time partitioned. The example below tails application logs, stamps each event, and writes it to HDFS one file per 128 MB or 10 minutes.

```properties
# /etc/flume/conf/weblogs.conf
a1.sources = r1
a1.channels = c1
a1.sinks = k1

# --- source: follow an active log file ---
a1.sources.r1.type = taildir
a1.sources.r1.filegroups = logs
a1.sources.r1.filegroups.logs = /var/log/web/access-.*\.log
a1.sources.r1.positionFile = /data/flume/taildir_position.json
a1.sources.r1.batchSize = 1000
a1.sources.r1.channels = c1

# --- channel: durable, disk backed ---
a1.channels.c1.type = file
a1.channels.c1.checkpointDir = /data/flume/checkpoint
a1.channels.c1.dataDirs = /data/flume/data
a1.channels.c1.capacity = 2000000
a1.channels.c1.transactionCapacity = 10000
a1.channels.c1.checkpointInterval = 30000
a1.channels.c1.keep-alive = 3

# --- sink: partitioned HDFS files ---
a1.sinks.k1.type = hdfs
a1.sinks.k1.hdfs.path = hdfs://nn.example.com/logs/web/year=%Y/month=%m/day=%d/hour=%H
a1.sinks.k1.hdfs.filePrefix = access-
a1.sinks.k1.hdfs.fileSuffix = .log
a1.sinks.k1.hdfs.fileType = DataStream
a1.sinks.k1.hdfs.writeFormat = Text
a1.sinks.k1.hdfs.round = true
a1.sinks.k1.hdfs.roundValue = 10
a1.sinks.k1.hdfs.roundUnit = minute
a1.sinks.k1.hdfs.rollInterval = 600
a1.sinks.k1.hdfs.rollSize = 134217728
a1.sinks.k1.hdfs.rollCount = 0
a1.sinks.k1.hdfs.batchSize = 1000
a1.sinks.k1.hdfs.callTimeout = 60000
a1.sinks.k1.channel = c1
```

Design notes:

+ `rollCount = 0` disables count-based rolling so files are governed by size and time, which keeps file sizes predictable.
+ The `year=.../month=...` layout is Hive-friendly partition naming, so the downstream table can use `PARTITIONED BY (year, month, day, hour)`.
+ `rollInterval` must be shorter than the sink `callTimeout` tuning window; otherwise a stalled file accumulates events.
+ The file channel checkpoint directory and data directories should be on separate fast disks with enough free space for at least a few hours of events.

[Table of Contents](#Apache-Flume)

## How do you configure a Flume agent to write to Kafka?
A Kafka sink lets Flume hand events to a Kafka topic instead of HDFS, so multiple consumers can read the same stream. A Kafka channel is also available and is durable by itself.

```properties
# Tail logs and publish to Kafka
a1.sources = r1
a1.channels = c1
a1.sinks = k1

a1.sources.r1.type = taildir
a1.sources.r1.filegroups = logs
a1.sources.r1.filegroups.logs = /var/log/payments/.*\.log
a1.sources.r1.channels = c1

a1.channels.c1.type = file
a1.channels.c1.checkpointDir = /data/flume/kafka/checkpoint
a1.channels.c1.dataDirs = /data/flume/kafka/data

a1.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.k1.kafka.bootstrap.servers = kafka-1:9092,kafka-2:9092,kafka-3:9092
a1.sinks.k1.kafka.topic = payments.raw
a1.sinks.k1.kafka.producer.acks = all
a1.sinks.k1.kafka.producer.linger.ms = 20
a1.sinks.k1.kafka.producer.compression.type = lz4
a1.sinks.k1.batchSize = 500
a1.sinks.k1.channel = c1
```

Reliability notes:

+ `acks=all` means the broker leader waits for in-sync replicas, so a broker failure does not silently drop the event.
+ Keep at least three brokers and a replication factor of three for a topic that a file channel feeds.
+ The Kafka sink is transactional with the channel, so a Kafka outage backs events up in the file channel rather than losing them - size the channel for the expected outage window.

[Table of Contents](#Apache-Flume)

## How do you use interceptors in a Flume configuration?
Interceptors are the cheapest place to enrich, filter, and route events. The chain runs in order, and each interceptor sees the output of the previous one.

```properties
a1.sources.r1.interceptors = ts host static extract drop_debug
a1.sources.r1.interceptors.ts.type = timestamp

a1.sources.r1.interceptors.host.type = host
a1.sources.r1.interceptors.host.hostHeader = agent_host

a1.sources.r1.interceptors.static.type = static
a1.sources.r1.interceptors.static.key = env
a1.sources.r1.interceptors.static.value = prod

# Extract level= and service= from a line like "ERROR service=checkout ..."
a1.sources.r1.interceptors.extract.type = regex_extractor
a1.sources.r1.interceptors.extract.regex = ^(\\w+) service=(\\w+).*
a1.sources.r1.interceptors.extract.serializers = s1 s2
a1.sources.r1.interceptors.extract.serializers.s1.name = level
a1.sources.r1.interceptors.extract.serializers.s2.name = service

# Drop known-noisy debug lines before they hit the channel
a1.sources.r1.interceptors.drop_debug.type = regex_filter
a1.sources.r1.interceptors.drop_debug.regex = ^.*DEBUG.*$
a1.sources.r1.interceptors.drop_debug.excludeEvents = true
```

With `level` in a header, a multiplexing selector can send ERROR events to an alerting channel and INFO events to the archive channel without a second parse downstream.

[Table of Contents](#Apache-Flume)

## How do you configure reliability and failover in Flume?
Reliability is a combination of source, channel, and sink settings. Use a durable channel, transactional sinks, and either a failover or load-balancing sink processor when more than one destination exists.

```properties
# Durable channel sized for a downstream outage
a1.channels.c1.type = file
a1.channels.c1.dataDirs = /data/flume/data
a1.channels.c1.checkpointDir = /data/flume/checkpoint
a1.channels.c1.capacity = 5000000
a1.channels.c1.transactionCapacity = 20000
a1.channels.c1.keep-alive = 5

# Two HDFS sinks: fail over to k2 if k1 goes down
a1.sinkgroups = g1
a1.sinkgroups.g1.sinks = k1 k2
a1.sinkgroups.g1.processor.type = failover
a1.sinkgroups.g1.processor.priority.k1 = 10
a1.sinkgroups.g1.processor.priority.k2 = 5
a1.sinkgroups.g1.processor.maxpenalty = 60000
```

Practical rules:

+ Set `transactionCapacity` well below `capacity` (for example 1% to 5%) so a large batch cannot starve checkpointing.
+ Monitor `ChannelFillPercentage`; a filling channel is the leading indicator of a slow sink.
+ Prefer at-least-once delivery plus idempotent downstream writes over chasing exactly-once in Flume.
+ For multi-hop agents, use Avro links and keep a durable channel on both the edge and the collector so a collector restart does not lose edge events.

[Table of Contents](#Apache-Flume)

## How do you monitor and tune a Flume agent?
Flume exposes a JSON metrics endpoint that can be scraped by any monitoring system, plus optional Ganglia reporting.

```bash
# Start the agent with the HTTP reporting endpoint
flume-ng agent --conf /etc/flume/conf --conf-file /etc/flume/conf/weblogs.conf -n a1 \
  -Dflume.monitoring.type=http \
  -Dflume.monitoring.port=34545 \
  -Dflume.root.logger=INFO,console
```

```bash
# Inspect channel fill and sink throughput
curl -s http://localhost:34545/metrics | python -m json.tool
```

Metrics worth alerting on:

+ `CHANNEL.c1.ChannelFillPercentage` - approaching 100% means the sink cannot keep up.
+ `CHANNEL.c1.EventPutSuccessCount` vs `EventTakeSuccessCount` - a widening gap is the same signal.
+ `SINK.k1.BatchCompleteCount` and `EventDrainSuccessCount` - throughput and stalls.
+ JVM heap and GC - a memory channel lives on heap, so a large channel needs a large heap.

[Table of Contents](#Apache-Flume)

## How does Flume compare with Kafka Connect, Fluentd, and Filebeat?
| Tool | Model | Strength | Weakness |
|---|---|---|---|
| Flume | agent: source-channel-sink | durable HDFS/HBase sinks, mature Hadoop integration | JVM per agent, operational overhead, smaller ecosystem |
| Kafka Connect | workers plus connectors | declarative connectors, offsets managed by Kafka, huge connector library | needs Kafka as the backbone |
| Fluentd / Fluent Bit | plugin-driven collector | lightweight, cloud-native, strong filtering and parsers | HDFS/HBase sinks less common |
| Filebeat | shipper plus Logstash | tiny footprint on hosts, great for rotation-aware tailing | delivery and routing handled by a downstream tier |

Choose Flume when the destination is HDFS or HBase and the environment is already Hadoop-centric. Choose Kafka Connect or Fluent Bit for a Kafka-centric or Kubernetes platform.

[Table of Contents](#Apache-Flume)

## When should you not use Flume?
+ You need an event backbone with replay, many consumers, and long retention - use Kafka and consume with your own application or Kafka Connect.
+ You need per-event stream processing with state, windows, and joins - use Flink or Spark Structured Streaming.
+ You need simple, host-local log shipping with low resource use - use Fluent Bit or Filebeat.
+ You need database change capture from an operational system - use Debezium or a managed CDC service rather than a Flume SQL source.
+ You need exactly-once semantics into a lakehouse - land in Kafka and use a transactional sink (Iceberg or Delta).

Flume still fits a narrow, valuable role: durable, back-pressured collection of file and syslog-style events into HDFS or HBase on an existing Hadoop cluster.

[Table of Contents](#Apache-Flume)

## What are the similarities and differences between Apache Flume and Apache Kafka?
Both move large event streams reliably and both support multiple consumers of the same data through a publish/subscribe style design.

Differences:

+ Flume pushes events to the destination through its sinks; Kafka is a durable log that consumers pull from at their own pace.
+ Flume's channel is internal to an agent and bounded by the agent's disk or heap; Kafka retains events on brokers for a configured retention period and supports replay.
+ Flume is typically an edge collection and delivery tier; Kafka is a shared backbone with many producers and consumers.
+ Flume has first-class HDFS and HBase sinks; Kafka needs a consumer, Kafka Connect, or a stream processor to reach those sinks.

They are often combined: Flume for collection and back-pressure close to the source, Kafka as the central, replayable buffer, and Connect or Flink for delivery into storage.

[Table of Contents](#Apache-Flume)

## Explain Reliability and Failure Handling in Apache Flume?
Flume NG uses channel-based transactions to guarantee reliable message delivery. When a message moves from one agent to another, two transactions are started: one on the agent that delivers the event and one on the agent that receives it. For the sending agent to commit its transaction, it must receive a success indication from the receiving agent. The receiving agent returns success only after its own transaction commits. This gives guaranteed at-least-once delivery between hops.

```text
Producer agent                         Consumer agent
  source -> channel                      channel -> sink
     |  begin txn                            |  begin txn
     |  write events                         |  write events
     |  commit  ----------------------------->|  commit
     |  (waits for ack)          ack          |  (returns success)
```

Failure handling:

+ If the sink fails, events stay in the channel and are retried; a file channel survives an agent restart.
+ If a downstream agent is unreachable, the upstream sink rolls back and retries, applying back-pressure to the source.
+ Duplicates are possible when an ack is lost, so sinks should be idempotent (for example, writing with a deterministic file name or an upsert).
+ A full channel blocks the source; monitoring channel fill percentage is the primary operational guardrail.

[Table of Contents](#Apache-Flume)

## Real world use cases for Flume

### 1. Web and application log aggregation into HDFS
A media company runs 400 application servers producing 3 TB of access and application logs per day. Each host runs a lightweight Flume agent that tails the active log files and forwards over Avro to a tier of six collector agents, which write partitioned files to HDFS for Hive and Spark.

Business context: the analytics team needs daily and hourly log partitions without installing a heavy agent on every host. Data volume: 3 TB/day, roughly 35k events/second at peak.

Agent design: `taildir` source on the edge, file channel at the edge sized for 30 minutes of backlog, Avro sink to the collectors; collectors use a file channel and an HDFS sink with hour partitioning.

```properties
# Collector: partition by hour, roll at 128 MB or 10 minutes
col.sinks.k1.type = hdfs
col.sinks.k1.hdfs.path = hdfs://nn/logs/app/year=%Y/month=%m/day=%d/hour=%H
col.sinks.k1.hdfs.filePrefix = app-
col.sinks.k1.hdfs.fileType = DataStream
col.sinks.k1.hdfs.rollSize = 134217728
col.sinks.k1.hdfs.rollCount = 0
col.sinks.k1.hdfs.rollInterval = 600
col.sinks.k1.hdfs.round = true
col.sinks.k1.hdfs.roundValue = 10
col.sinks.k1.hdfs.roundUnit = minute
```

Why this design: two hops keep per-host memory small, the file channel at the edge absorbs collector restarts, and hour-level HDFS partitioning matches the Hive table's partition columns.

### 2. Clickstream into HBase for real-time lookup
An ad-tech company streams 2 billion ad impressions per day and needs millisecond lookups of recent impressions by user. Flume collects the impressions from edge servers and writes them into HBase with the user id as part of the row key.

Business context: the bidding service reads the last few impressions for a user during auction time. Data volume: ~25k events/second, 2 billion rows/day.

Agent design: a `taildir` or `http` source, a memory channel for throughput (the raw stream is also archived to S3), and an HBase sink with a regex serializer extracting `user_id`, `campaign_id`, and `ts`.

```properties
a1.sinks.k1.type = hbase
a1.sinks.k1.table = impressions
a1.sinks.k1.columnFamily = i
a1.sinks.k1.serializer = org.apache.flume.sink.hbase.RegexHbaseEventSerializer
a1.sinks.k1.serializer.regex = ^([^|]+)\\|([^|]+)\\|([^|]+)\\|(.*)$
a1.sinks.k1.serializer.colNames = user_id,campaign_id,ts,payload
a1.sinks.k1.batchSize = 500
a1.sinks.k1.channel = c2
```

Why this design: HBase gives key-based random reads at high write throughput; the row key (see the HBase topic) reverses the timestamp so the newest impressions for a user sort first. The memory channel is acceptable because a duplicate or a small loss in the ad stream is cheaper than the latency of a file channel.

### 3. Multi-datacenter log fan-in with failover
A payments platform collects audit logs from three regions into a central HDFS archive. Each region has a primary and a secondary collector; edge agents must not lose events when a collector is down.

Business context: audit logs are regulatory evidence and must be durable. Data volume: 400 GB/day, bursty at settlement time.

Agent design: an Avro sink group with a `failover` processor, priorities set so the in-region collector is preferred, and a file channel with a multi-hour capacity on every edge agent.

```properties
edge.sinkgroups = g1
edge.sinkgroups.g1.sinks = k_primary k_secondary
edge.sinkgroups.g1.processor.type = failover
edge.sinkgroups.g1.processor.priority.k_primary = 10
edge.sinkgroups.g1.processor.priority.k_secondary = 5
edge.sinkgroups.g1.processor.maxpenalty = 120000
```

Why this design: failover preserves ordering per agent better than load balancing, the file channel survives an agent restart, and the two collectors can be in different racks or regions.

### 4. IoT sensor telemetry from the edge
A utility monitors 60,000 smart meters, each emitting a reading every 15 seconds. A gateway host per substation runs Flume to buffer and forward telemetry to a central platform.

Business context: readings drive outage detection and billing reconciliation. Data volume: ~4,000 events/second, small JSON bodies.

Agent design: a `syslog` or `netcat` source on the gateway, a spillable memory channel to survive short collector outages without a large disk footprint, and a Kafka sink so multiple downstream consumers (billing, monitoring, ML) can read the stream.

```properties
gw.channels.c1.type = spillablememorychannel
gw.channels.c1.capacity = 500000
gw.channels.c1.overflowCapacity = 2000000
gw.channels.c1.checkpointDir = /data/flume/spill/checkpoint
gw.channels.c1.dataDirs = /data/flume/spill/data

gw.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
gw.sinks.k1.kafka.topic = meter.readings
gw.sinks.k1.kafka.producer.acks = all
gw.sinks.k1.kafka.producer.compression.type = zstd
```

Why this design: the spillable channel handles bursty meter traffic with a disk safety net, and publishing to Kafka lets independent teams consume the same telemetry without coupling to the collection agent.

### 5. Security and audit log archival with zero loss
A bank must retain authentication and privilege-escalation logs for seven years. Agents run on domain controllers and application servers, and evidence of loss must be avoidable.

Business context: compliance requires an immutable, complete archive. Data volume: 80 GB/day but with a strict zero-loss requirement.

Agent design: a `taildir` source with `positionFile` for restart-safe tailing, a file channel with checkpointing, and an HDFS sink writing to a WORM-style directory with zstd or gzip compression and file names that include the collector host.

```properties
a1.sources.r1.type = taildir
a1.sources.r1.positionFile = /var/lib/flume/audit_position.json
a1.sources.r1.filegroups = audit
a1.sources.r1.filegroups.audit = /var/log/audit/.*\.log

a1.channels.c1.type = file
a1.channels.c1.capacity = 3000000
a1.channels.c1.transactionCapacity = 10000
a1.channels.c1.checkpointDir = /data/audit/checkpoint
a1.channels.c1.dataDirs = /data/audit/data

a1.sinks.k1.type = hdfs
a1.sinks.k1.hdfs.path = hdfs://nn/audit/%Y/%m/%d
a1.sinks.k1.hdfs.fileType = CompressedStream
a1.sinks.k1.hdfs.codeC = gzip
a1.sinks.k1.hdfs.filePrefix = audit-%{agent_host}-
a1.sinks.k1.hdfs.rollSize = 268435456
a1.sinks.k1.hdfs.rollCount = 0
```

Why this design: `taildir` with a position file never skips a line across restarts, the file channel turns a downstream outage into back-pressure instead of loss, and per-host file prefixes make it obvious when a host is missing from the archive.

[Table of Contents](#Apache-Flume)
