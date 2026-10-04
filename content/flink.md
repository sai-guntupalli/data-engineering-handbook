## [Main title](../README.md)
### [Interview questions](full.md)

# Apache Flink

Apache Flink is a distributed, stateful stream processor with true event-time semantics, watermarks, keyed state, checkpointing, and exactly-once connectors. It runs the same operators over unbounded streams and bounded (batch) inputs. These questions cover the DataStream and Table APIs, event time, windowing, checkpointing and savepoints, state backends, exactly-once Kafka pipelines, and production trade-offs.

+ [When would you choose Flink over Spark Structured Streaming?](#When-would-you-choose-Flink-over-Spark-Structured-Streaming)
+ [What are event time, processing time, and watermarks in Flink?](#What-are-event-time-processing-time-and-watermarks-in-Flink)
+ [See you using Flink, briefly introduce Flink?](#See-you-using-Flink-briefly-introduce-Flink)
+ [What are the differences between Flink and Spark Streaming?](#What-are-the-differences-between-Flink-and-Spark-Streaming)
+ [What are the Flink component stacks](#What-are-the-Flink-component-stacks)
+ [Does Flink need to depend on Hadoop?](#Does-Flink-need-to-depend-on-Hadoop)
+ [How big is your FLink cluster?](#How-big-is-your-FLink-cluster)
+ [What is the Flink programming model?](#What-is-the-Flink-programming-model)
+ [What are the roles of Flink cluster? What are the functions?](#What-are-the-roles-of-Flink-cluster-What-are-the-functions)
+ [What is TaskSolt?](#What-is-TaskSolt)
+ [What are the commonly used operators in Flink?](#What-are-the-commonly-used-operators-in-Flink)
+ [What is the parallelism of Flink and What is the parallelism setting of Flink?](#What-is-the-parallelism-of-Flink-and-What-is-the-parallelism-setting-of-Flink)
+ [What is the relationship between Flink's Solt and parallelism?](#What-is-the-relationship-between-Flinks-Solt-and-parallelism)
+ [What if Flink encounters an abnormal restart of the program?](#What-if-Flink-encounters-an-abnormal-restart-of-the-program)
+ [Flink's distributed cache](#Flinks-distributed-cache)
+ [Broadcast variables in Flink](#Broadcast-variables-in-Flink)
+ [Do you know what windows in Flink are?](#Do-you-know-what-windows-in-Flink-are)
+ [Flink's state storage?](#Flinks-state-storage)
+ [What kind of time are there in Flink?](#What-kind-of-time-are-there-in-Flink)
+ [What is Watermark in Flink?](#What-is-Watermark-in-Flink)
+ [What is Unbounded streams in Apache Flink?](#What-is-Unbounded-streams-in-Apache-Flink)
+ [Apache Flink Job Execution Architecture](#Apache-Flink-Job-Execution-Architecture)
+ [What is Bounded streams in Apache Flink?](#What-is-Bounded-streams-in-Apache-Flink)
+ [What is Dataset API in Apache Flink?](#What-is-Dataset-API-in-Apache-Flink)
+ [What is DataStream API in Apache Flink?](#What-is-DataStream-API-in-Apache-Flink)
+ [What is Apache Flink Table API?](#What-is-Apache-Flink-Table-API)
+ [What is Apache Flink FlinkML?](#What-is-Apache-Flink-FlinkML)
+ [What is Apache Flink?](#What-is-Apache-Flink)
+ [Explain Apache Flink Architecture?](#Explain-Apache-Flink-Architecture)
+ [Explain the Apache Flink Job Execution Architecture?](#Explain-the-Apache-Flink-Job-Execution-Architecture)
+ [What are the features of Apache Flink?](#What-are-the-features-of-Apache-Flink)
+ [What is Storage and Streaming in Apache Flink?](#What-is-Storage-and-Streaming-in-Apache-Flink)
+ [What is DataSet API?](#What-is-DataSet-API)
+ [What are the DSL Tool's in Flink?](#What-are-the-DSL-Tools-in-Flink)
+ [What are the Apache Flink domain-specific libraries?](#What-are-the-Apache-Flink-domain-specific-libraries)
+ [What is the programing model of Apache Flink?](#What-is-the-programing-model-of-Apache-Flink)
+ [What are the different types of tools supported by Apache Flink?](#What-are-the-different-types-of-tools-supported-by-Apache-Flink)
+ [Can we consider Apache Flink as an alternative to Hadoop? if so then explain why?](#Can-we-consider-Apache-Flink-as-an-alternative-to-Hadoop-if-so-then-explain-why)
+ [What are the use cases of Apache Flink?](#What-are-the-use-cases-of-Apache-Flink)
+ [What are the different ways to use Apache Flink?](#What-are-the-different-ways-to-use-Apache-Flink)
+ [What is the different component stack of Apache Flink?](#What-is-the-different-component-stack-of-Apache-Flink)
+ [What is the command to start Apache Flink Cluster?](#What-is-the-command-to-start-Apache-Flink-Cluster)
+ [What is the Apache Flink SQL client and how to start it?](#What-is-the-Apache-Flink-SQL-client-and-how-to-start-it)
+ [What are the SQL statements supported in Apache Flink?](#What-are-the-SQL-statements-supported-in-Apache-Flink)
+ [What is bounded and unbounded data in Apache Flink?](#What-is-bounded-and-unbounded-data-in-Apache-Flink)
+ [What is the building block of Apache Flink streaming applications?](#What-is-the-building-block-of-Apache-Flink-streaming-applications)
+ [What are the most common types of applications that use the Apache Flink?](#What-are-the-most-common-types-of-applications-that-use-the-Apache-Flink)
+ [What are the features of the Apache Flink execution Engine?](#What-are-the-features-of-the-Apache-Flink-execution-Engine)
+ [What is Apache FlinkML?](#What-is-Apache-FlinkML)
+ [How can I check the progress of an Apache Flink Program?](#How-can-I-check-the-progress-of-an-Apache-Flink-Program)
+ [How Apache Flink handles the fault-tolerance?](#How-Apache-Flink-handles-the-fault-tolerance)
+ [How to run an Apache Flink program using CLI mode?](#How-to-run-an-Apache-Flink-program-using-CLI-mode)
+ [What is the responsibility of JobManager in Apache Flink Cluster?](#What-is-the-responsibility-of-JobManager-in-Apache-Flink-Cluster)
+ [What is the responsibility of TaskManager in Apache Flink Cluster?](#What-is-the-responsibility-of-TaskManager-in-Apache-Flink-Cluster)
+ [What is the filesystem supported by Apache Flink?](#What-is-the-filesystem-supported-by-Apache-Flink)
+ [What is the difference between stream processing and batch processing?](#What-is-the-difference-between-stream-processing-and-batch-processing)
+ [What can I do with my state?](#What-can-I-do-with-my-state)
+ [Flink watermark Transmission mechanism.](#Flink-watermark-Transmission-mechanism)
+ [Flink The time semantics of?](#Flink-The-time-semantics-of)
+ [Flink window join:](#Flink-window-join)
+ [Flink What are the window functions:](#Flink-What-are-the-window-functions)
+ [keyedProcessFunction How it works](#keyedProcessFunction-How-it-works)
+ [How to deal with offline data such as the association with offline data?](#How-to-deal-with-offline-data-such-as-the-association-with-offline-data)
+ [What if there is a data skew?](#What-if-there-is-a-data-skew)
+ [How to do dimension table Association?](#How-to-do-dimension-table-Association)
+ [Flink checkpoint The overtime problem of How to solve?](#Flink-checkpoint-The-overtime-problem-of-How-to-solve)
+ [FlinkTopN And offline TopN The difference between?](#FlinkTopN-And-offline-TopN-The-difference-between)
+ [Sparkstreaming and flink in checkpoint?](#Sparkstreaming-and-flink-in-checkpoint)
+ [A brief introduction cep State programming:](#A-brief-introduction-cep-State-programming)
+ [How to deal with abnormal data in Flink.](#How-to-deal-with-abnormal-data-in-Flink)
+ [Is there any possibility of data loss in Flink?](#Is-there-any-possibility-of-data-loss-in-Flink)
+ [At the time of submission How to make parallelism and how to allocate resources?](#At-the-time-of-submission-How-to-make-parallelism-and-how-to-allocate-resources)
+ [What's the common stream of API?](#Whats-the-common-stream-of-API)
+ [How to maintain Checkpoint?](#How-to-maintain-Checkpoint)
+ [What's the difference at Spark and Flink Serialization?](#Whats-the-difference-at-Spark-and-Flink-Serialization)
+ [How to deal with late data?](#How-to-deal-with-late-data)
+ [When to use aggregate perhaps process:](#When-to-use-aggregate-perhaps-process)
+ [How does checkpointing work in Flink?](#How-does-checkpointing-work-in-Flink)
+ [What are savepoints and how do you use them?](#What-are-savepoints-and-how-do-you-use-them)
+ [How do you configure the state backend?](#How-do-you-configure-the-state-backend)
+ [How do you build an exactly-once Kafka to Kafka pipeline?](#How-do-you-build-an-exactly-once-Kafka-to-Kafka-pipeline)
+ [How do you do windowing in Flink SQL?](#How-do-you-do-windowing-in-Flink-SQL)
+ [How do you handle event time and watermarks in PyFlink?](#How-do-you-handle-event-time-and-watermarks-in-PyFlink)
+ [What are Flink's trade-offs and when should you not use it?](#What-are-Flinks-trade-offs-and-when-should-you-not-use-it)
+ [Real world use cases for Apache Flink](#Real-world-use-cases-for-Apache-Flink)

## When would you choose Flink over Spark Structured Streaming?
Choose Flink when you need true event-by-event stream processing, low latency, complex event-time handling, large stateful operations, or exactly-once streaming semantics with long-running jobs. Spark Structured Streaming is often simpler for micro-batch workloads and teams already standardized on Spark.

Example:

+ fraud detection with millisecond-level decisions: Flink
+ hourly incremental aggregation into a lakehouse: Spark Structured Streaming

The strongest answer compares latency, state management, operational complexity, connectors, and team skill set.

[Table of Contents](#Apache-Flink)

## What are event time, processing time, and watermarks in Flink?
Event time is when the event actually happened. Processing time is when Flink processes the event. Watermarks tell Flink how far event time has advanced and how long to wait for late data before closing windows.

Example:

```text
event happened: 10:00:05
event processed: 10:02:10
watermark: events up to 10:01:00 are mostly complete
```

Watermarks are essential for correct windowed aggregations when events arrive late or out of order.

[Table of Contents](#Apache-Flink)

## See you using Flink, briefly introduce Flink?
Flink is a distributed, stateful stream-processing framework that treats batch as a bounded stream. A job is a dataflow of `source -> transformation -> sink`, and the same runtime handles unbounded (streaming) and bounded (batch) input.

The main APIs are the DataStream API (Java, Scala, Python), the Table API and SQL, plus domain libraries such as CEP and FlinkML. Flink provides event-time processing, watermarks, keyed state, checkpointing, and exactly-once semantics.

```python
from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
env.from_collection(["hello", "flink"]).print()
env.execute("flink-intro")
```

[Table of Contents](#Apache-Flink)

## What are the differences between Flink and Spark Streaming?
1. The design ideas are different. Flink considers batch to be a kind of streaming, and spark considers a streaming batch.
2. The architecture model is different. Spark has Driver, Master, Worker, and Executor. Flink has the concepts of TaskManager, JobManager, Task, SubTask, and Slot
3. Flink's streaming data processing is much stronger than spark, for example, time supports three kinds of time
There are more windows than spark
4. In the case of out-of-order data, Flink is stronger than spark, because flink has watermark. In fact, the calculation method when running is the time of the last data-if watermaker is greater than the end of the window, execute
5. For fault tolerance, flink is also better than spark. For example, flink supports two-stage transactions to ensure that data after program crashes will not be re-consumed. Spark also has checkpoints, but it only ensures that data is not lost, and it cannot be repeated. consumption.

| Aspect | Spark Structured Streaming | Flink |
|---|---|---|
| Model | micro-batch | true record-at-a-time streaming |
| Latency | sub-second to seconds | milliseconds |
| Time semantics | event time with watermarks | event time, watermarks, three time notions |
| State | limited, epoch-based | large keyed state, RocksDB |
| Exactly-once | checkpoint + idempotent sink | checkpoint + two-phase-commit sinks |
| Batch | Spark SQL engine | bounded streams on the same runtime |

[Table of Contents](#Apache-Flink)

## What are the Flink component stacks
1. The deployment mode can be Local, Cluster, Cloud
2. Then perform all basic services based on Runtime components
3. The upper layer provides DataStream API and DataSet API
4. At the high-level, there are Table API, CEP complex family care, ML machine learning, graph computing

[Table of Contents](#Apache-Flink)

## Does Flink need to depend on Hadoop?
Flink can be completely independent of Hadoop and run without relying on Hadoop components, but as the basis of big data, it is conceivable that most big data frameworks cannot bypass it. Flink can support many components, such as Yarn's resource scheduling, Hbase's real-time data storage and dimensional table access, HDFS state storage and offline computing, and so on.

[Table of Contents](#Apache-Flink)

## How big is your FLink cluster?
This can be done according to the situation of your own company. Most companies use the yarn mode of deployment. Of course, yarn also has multiple modes of deployment, such as a single job or directly apply for a large amount of resources in yarn to be responsible. Job submission, most companies choose, should be single job mode.

[Table of Contents](#Apache-Flink)

## What is the Flink programming model?
In fact, in one sentence,Source->Transformation->Sink*

[Table of Contents](#Apache-Flink)

## What are the roles of Flink cluster? What are the functions?
Flink programs mainly have three roles: TaskManager, JobManager, and Client when they are running.
JobManager In the role of a manager in the cluster, it is the coordinator of the entire cluster. It is responsible for receiving the execution of Flink Job, coordinating checkpoints, recovering from failures, and managing Task Manager.
TaskManager It is responsible for the resource information on the node where the manager is located, such as memory, disk, and network. It will report the resource to the JobManager when it is started.
Client It is the client submitted by the Flink program. When a user submits a Flink program, a Client is first created. Then the program submitted by the user will be preprocessed and submitted to the cluster for processing.

[Table of Contents](#Apache-Flink)

## What is TaskSolt?
In Flink's architecture, TaskManager is the working node that is actually used to execute our program. TaskManager is a JVM process. In fact, in order to achieve the concept of resource isolation and parallel execution, the concept of TaskSlot was proposed at this time, which is actually In order to control how many Tasks the TaskManager can receive, the TaskManager is controlled by tasksolt, that is, if we have a source that specifies three parallelism, then he will use three solts, and the other one needs to be mainly parallel as an operator When the degree is the same, and there is no change in the degree of parallelism, or there is no shuffle, they will be together at this time. This is an optimized concept.

[Table of Contents](#Apache-Flink)

## What are the commonly used operators in Flink?
Map operator
Filter operator
KeyBy operator
Window window

```python
stream = env.from_source(source, watermark_strategy, "orders")

mapped = stream.map(lambda o: enrich(o))
flat = stream.flat_map(lambda o: o["items"])
filtered = stream.filter(lambda o: o["amount"] > 0)
keyed = filtered.key_by(lambda o: o["customer_id"])
counts = keyed.map(CountByKey())
joined = keyed.connect(other).key_by(lambda a: a["k"], lambda b: b["k"]).process(JoinFn())
```

Common shape: `source -> map/flatMap/filter -> keyBy -> window/process -> sink`. `keyBy` is what turns an operator into a stateful, parallel one, because state is scoped per key.

[Table of Contents](#Apache-Flink)

## What is the parallelism of Flink and What is the parallelism setting of Flink?
In fact, the parallelism of Flink is well understood. For example, kafkaSource, its parallelism is the number of partitions by default. The degree of parallelism is this operator, and how many tasksolt are needed, we should know that is the advantage of parallel computing. Generally, the degree of parallelism is set according to the amount of data. It is best to keep the source and map operators without shuffle, because the pressure on the source and map operators is not very large, but when our data table is widened, It is better to set it larger.

Parallelism is per operator and can be set globally, per job, or per operator. A Kafka source defaults to the topic's partition count.

```python
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(8)                      # job-wide default
stream.key_by(lambda o: o["cust"]).map(Enrich()).set_parallelism(16)

# flink-conf.yaml
# parallelism.default: 8
```
```bash
# CLI override at submit time
flink run -p 16 -c com.acme.OrdersJob orders.jar
```

[Table of Contents](#Apache-Flink)

## What is the relationship between Flink's Solt and parallelism?
Solt is a concept in TaskManager. Parallelism is a concept in the program, that is, the concept of execution level. In fact, Solt specifies how many slots this TaskManager has and how much parallelism can be supported, but the parallelism developed by the program uses slots That is Solt, that is, TaskManager is the provider and the program is the user

[Table of Contents](#Apache-Flink)

## What if Flink encounters an abnormal restart of the program?
Flink has some restart strategies, and as long as the checkpoint is done, it can be done at least once. Of course, it may not be accurate once, but some components can be done. The restart strategy generally set is a fixed delay restart strategy. The restart does not delete the checkpoint. Generally, the number of restarts set by our company is 4 times. If it stops, we will send a nail warning and start from the checkpoint when it starts.

Flink restarts failed tasks from the last completed checkpoint using a restart strategy. Set it per job:

```python
from pyflink.common import RestartStrategies

env.set_restart_strategy(
    RestartStrategies.fixed_delay_restart(4, 10_000)   # 4 attempts, 10 s delay (ms)
)
# or: RestartStrategies.failure_rate_restart(failure_rate, failure_interval, delay_interval)
# or: RestartStrategies.no_restart()
```

After the configured attempts are exhausted the job fails, which is when your alerting should fire and an operator restarts it from the latest savepoint.

[Table of Contents](#Apache-Flink)

## Flink's distributed cache
The distributed cache implemented by Flink is similar to Hadoop. The purpose is to read the file locally and put it in the taskmanager node to prevent the task from repeatedly pulling data and reduce performance.

[Table of Contents](#Apache-Flink)

## Broadcast variables in Flink
We know that Flink is parallel, and the calculation process may not be performed in a Slot. Then there is a situation: when we need to access the same data. Then the broadcast variable in Flink is to solve this situation. We can understand the broadcast variable as a public shared variable. We can broadcast a dataset, and then different tasks can be obtained on the node. There will only be one copy of this data on each node.

[Table of Contents](#Apache-Flink)

## Do you know what windows in Flink are?
Flink supports two ways to divide windows, according to time and count. session is also a kind of time
Tumbing Count Window： Perform calculation when reaching a certain number, no folding
Sliding Time Window： When a certain period of time is reached, roll over, there can be overlap, generally used to calculate the recent demand, such as nearly 5 minutes.
Tumbing time Window： When a certain period of time is reached, the slide is carried out, which can be thought of as the Nokia slide phone used before. This is actually a micro batch
Sliding Count Window： Slide when it reaches a certain number
Session Window: The window data has no fixed size, it is divided according to the parameters passed in by the user, and the window data does not overlap. It is similar to calculating the user's previous actions when the user logs out.

```python
from pyflink.common import Time
from pyflink.datastream import window

keyed = stream.key_by(lambda e: e["user_id"])
keyed.window(window.TumblingEventTimeWindows.of(Time.minutes(5))).aggregate(SumAmount())
keyed.window(window.SlidingEventTimeWindows.of(Time.minutes(15), Time.minutes(5))).process(TopN())
keyed.window(window.EventTimeSessionWindows.with_gap(Time.minutes(10))).process(Sessionize())
keyed.count_window(100).aggregate(SumAmount())   # count window
```

Time windows use event time with watermarks; count windows trigger on record count per key. Session windows close after a gap of inactivity and have no fixed size.

[Table of Contents](#Apache-Flink)

## Flink's state storage?
Flink often needs to store intermediate states during calculations to avoid data loss and recover from abnormal states. Choosing a different state storage strategy will affect the state interaction between JobManager and Subtask, that is, JobManager will interact with State to store state.
Flink provides three state storage:
MemoryStateBackend
FsSateBackend
RocksDBStateBackend

State backends decide where keyed state lives and how checkpoints are written. `HashMapStateBackend` keeps state on the JVM heap (fast, memory-bound), while `EmbeddedRocksDBStateBackend` spills to local disk and supports incremental checkpoints (large state). See the dedicated state backend question for configuration.

[Table of Contents](#Apache-Flink)

## What kind of time are there in Flink?
Event time: the time when the event actually occurred
Intake time: time to enter flink
Processing time: the time to enter the flink operator

```text
event time:      when the event actually happened (embedded in the record)
ingestion time:  when the event entered Flink
processing time: when a specific operator processes the event (wall clock)
```

Event time is the only notion that gives deterministic results, because it does not depend on when data arrives or how fast the job runs. Processing time is cheapest but non-reproducible.

[Table of Contents](#Apache-Flink)

## What is Watermark in Flink?
Watermark is an operation used by Flink to deal with out-of-order time. In fact, in Flink, if we use event time and take kafka's source, then the window execution time at this time is the smallest among the partitions Partitions are used for triggering, and each partition must be triggered to perform calculations. Why is this? In fact, it is because the partitions of Kafka are disordered. Orderly in the zone. The execution time is the maximum time minus the watermark>window end time, and the calculation will be executed at this time.

A watermark is a monotonically increasing timestamp that says "no event older than this should arrive". It drives window firing in event time.

```python
from pyflink.common import Duration, WatermarkStrategy
from pyflink.common.watermark_strategy import TimestampAssigner

class EventTimestamps(TimestampAssigner):
    def extract_timestamp(self, event, record_timestamp):
        return event["event_ts"]

wm = (
    WatermarkStrategy
    .for_bounded_out_of_orderness(Duration.of_seconds(5))
    .with_timestamp_assigner(EventTimestamps())
)
stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "kafka-orders")
stream = stream.assign_timestamps_and_watermarks(wm)
```

With multiple input partitions, the operator's watermark is the minimum across inputs, so one idle partition can hold every window open; idle-source detection (`with_idleness`) fixes that.

[Table of Contents](#Apache-Flink)

## What is Unbounded streams in Apache Flink?
Any type of data is produced as a stream of events. Data can be processed as unbounded or bounded streams.
Unbounded streams have a beginning but no end. They do not end and continue to provide data as it is produced. Unbounded streams should be processed continuously, i.e., events should be handled as soon as they are consumed. Since the input is unbounded and will not be complete at any point in time, it is not possible to wait for all of the data to arrive.

[Table of Contents](#Apache-Flink)

## Apache Flink Job Execution Architecture
Processing unbounded data sometimes requires that events are consuming in a specific order, such as the order in which events arrives, to be able to reason about result completeness.

[Table of Contents](#Apache-Flink)

## What is Bounded streams in Apache Flink?
Bounded streams have a beginning and an end point. Bounded streams could be processed by consuming all data before doing any computations. Ordered ingestion is not needed to process bounded streams since a bounded data set could always be sorted. Processing of bounded streams is also called as batch processing.

[Table of Contents](#Apache-Flink)

## What is Dataset API in Apache Flink?
The Apache Flink Dataset API was used to do batch operations on data over time. It was available in Java, Scala, and Python, and performed transformations such as filtering, mapping, aggregating, joining, and grouping. Note: the DataSet API is formally deprecated and was removed in Flink 2.0 — new jobs should use the DataStream API, Table API, or SQL instead.
```java
DataSet<Tuple2<String, Integer>> wordCounts = text
.flatMap(new LineSplitter())
.groupBy(0)
.sum(1);
```

[Table of Contents](#Apache-Flink)

## What is DataStream API in Apache Flink?
The Apache Flink DataStream API is used to handle data in a continuous stream. On the stream data, you can perform operations such as filtering, routing, windowing, and aggregation. On this data stream, there are different sources such as message queues, files, and socket streams, and the resulting data can be written to different sinks such as command line terminals. This API is supported by the Java and Scala programming languages.

```java
DataStream<Tuple2<String, Integer>> dataStream = env
.socketTextStream("localhost", 9091)
.flatMap(new Splitter())
.keyBy(0)
.timeWindow(Time.seconds(7))
.sum(1);
```

```python
from pyflink.common import Types, WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "orders")

result = (
    stream.map(lambda o: (o["region"], o["amount"]), output_type=Types.TUPLE([Types.STRING(), Types.DOUBLE()]))
    .key_by(lambda t: t[0])
    .reduce(lambda a, b: (a[0], a[1] + b[1]))
)
result.print()
env.execute("regional-revenue")
```

The DataStream API gives explicit control over state, timers, watermarks, and connectors, which is why it is used for complex stateful pipelines where SQL is not expressive enough.

[Table of Contents](#Apache-Flink)

## What is Apache Flink Table API?
Table API is a relational API with an expression language similar to SQL. This API is capable of batch and stream processing. It is compatible with the Java and Scala Dataset and Datastream APIs. Tables can be generated from internal Datasets and Datastreams as well as from external data sources. You can use this relational API to perform operations such as join, select, aggregate, and filter. The semantics of the query are the same if the input is batch or stream.
```scala
val tableEnvironment = TableEnvironment.getTableEnvironment(env)
// register a Table
tableEnvironment.registerTable("TestTable1", ...);
// create a new Table from a Table API query
val newTable2 = tableEnvironment.scan(TestTable1).select(...);
```

[Table of Contents](#Apache-Flink)

## What is Apache Flink FlinkML?
FlinkML is the Flink Machine Learning (ML) library. It is a new initiative in the Flink community, with an expanding list of algorithms and contributors. FlinkML aims to include scalable ML algorithms, an easy-to-use API, and tools to help reduce glue code in end-to-end ML systems. Note: Flink Community has planned to delete/deprecate the legacy flink-libraries/flink-ml package in Flink1.9, and replace it with the new flink-ml interface proposed in FLIP39 and FLINK-12470.

[Table of Contents](#Apache-Flink)

## What is Apache Flink?
The Apache Software Foundation created Apache Flink, an open-source, unified stream-processing and batch-processing framework. Apache Flink is built around a distributed streaming data-flow engine written in Java and Scala. Flink runs every dataflow programm in a data-parallel and pipelined fashion.

[Table of Contents](#Apache-Flink)

## Explain Apache Flink Architecture?
Apache Flink is based on the Kappa architecture. The Kappa architecture uses a single processor - stream, who accepts all information as a stream, and the streaming engine processes data in real-time. Batch data in kappa architecture is a form of streaming data.
Apache Flink Architecture
The majority of big data frameworks are built on the Lambda architecture, which uses different processors for batch and streaming data. In Lambda architecture, batch and stream views have different codebases. The codebases must be combined in order to query and retrieve the results. Maintaining different codebases/views and combining them is a hassle, but the Kappa architecture fixes this problem by having only one real-time view, which eliminates the need for codebase merging.
The core principle of the Kappa architecture is to manage batch and real-time data via a single stream processing engine.
That is not to say that Kappa architecture is preferred to Lambda architecture; it is entirely dependent on the use-case and application to determine which architecture is optimal.

[Table of Contents](#Apache-Flink)

## Explain the Apache Flink Job Execution Architecture?
The Apache Flink job execution architecture is shown in the diagram below.Apache Flink Job Execution Architecture
Program
It is a piece of code that is executed on the Flink Cluster.
Client
It is in charge of taking code from the given programm and creating a job dataflow graph, which is then passed to JobManager. It also retrieves the Job data.
JobManager
It is responsible for generating the execution graph after obtaining the Job Dataflow Graph from the Client. It assigns the job to TaskManagers in the cluster and monitors its execution.
TaskManager
It is in charge of executing all of the tasks assigned to it by JobManager. Both TaskManagers execute the tasks in their respective slots in the specified parallelism. It is in charge of informing JobManager about the status of the tasks.

[Table of Contents](#Apache-Flink)

## What are the features of Apache Flink?
Flink uses common runtime for data streaming applications and batch processing applications.
It can run both Batch and Stream programs.
Provides APIs.
It has lightning fast speed.
Can process data in low latency.
It can easily integrate with big data tools like Apache Hadoop, Apache MapReduce, etc.
It is highly scalable.
It acts as a Fault tolerent.

[Table of Contents](#Apache-Flink)

## What is Storage and Streaming in Apache Flink?
Flink compose various capacity framework and can devour information from gushing frameworks.The following gushing framework, flink can persue compose information like:
FLume - Acts as an Aggregation Tool
HBase - Acts like NoSQL Databse in a Hadoop ecosystem
HDFS - Helps as Hadoop Distributed File System
Kafka - Helps in distributing messaging queue
RabbitMQ - Acts as a Messaging queue
S3 - It is Simple Storage Service from Amazon

[Table of Contents](#Apache-Flink)

## What is DataSet API?
DataSet API helps us in enabling the client to actualize activities like a guide, channel, gathering and so on.It is utilized for appropriated preparing, it is an uncommon instance of stream preparing where we have a limited information source.They are regular programs that implement transformation on data sets like filtering, mapping, etc. The DataSet API is deprecated (removed in Flink 2.0); batch work now runs on the DataStream API, Table API, or SQL.
Data sets are created from sources like reading files, local collections, etc.All the results are returned through sinks, the execution can happen in a local JVM or on clusters of many machines.

[Table of Contents](#Apache-Flink)

## What are the DSL Tool's in Flink?
There are 3 types of DSL tools:
Table - Its is implanted in DataSet and DataStream API.As it helps in performing impromptu investigation utilizing SQL like articulation languague for preparing bunch and social strem.
Gelly - It enables clients to run a set of tasks and change the procedure of the diagram.
FlinkML - It is composed in Scala.It gives instinctive APIs and proficient calculation to deal with applications.

[Table of Contents](#Apache-Flink)

## What are the Apache Flink domain-specific libraries?
The following is the list of Apache Flink domain-specific libraries.
FlinkML: It is used for machine learning.
Table: It is used to perform the relational operation.
Gelly: It is used to perform the Graph operation.
CEP: It is used for complex event processing.

[Table of Contents](#Apache-Flink)

## What is the programing model of Apache Flink?
The Apache Flink Datastream and the Dataset work as a programming model of flink and its other layers of architecture. The Datastream programming model is useful in real-time stream processing whereas the Dataset programming model is useful in batch processing.

```text
source (Kafka, files, collections)
   -> transformations (map, filter, keyBy, window, connect, process)
   -> sink (Kafka, filesystem, JDBC, Iceberg)
```

Each transformation becomes a chained operator where possible, and keyed operations carry state with them. Fault tolerance comes from checkpointing the state of the whole dataflow, not from replaying the source alone.

[Table of Contents](#Apache-Flink)

## What are the different types of tools supported by Apache Flink?
Apache Flink supports the below list of tools.
CLI(Command Line Interface
Apache Flink Dashboard
Apache Flink SQL Client
Scala Shell

[Table of Contents](#Apache-Flink)

## Can we consider Apache Flink as an alternative to Hadoop? if so then explain why?
Apache Flink provides more features and flexibility comparing to Hadoop because it uses the cycle dataflow programming model despite Mapreduce which is a two-stage disk storage model, Flink programs can work in memory and can be used with other filesystems apart from Hadoop. Flink provides the unified framework using that we can create a single data flow that will use batch, streaming, machine learning, and SQL queries.

[Table of Contents](#Apache-Flink)

## What are the use cases of Apache Flink?
Many real-world industries are using Apache Flink and their use cases are as mentioned below.

Financial Services
Financial industries are using Flink to perform fraud detection in real-time and send mobile notifications.

Healthcare
The hospitals are using Apache Flink to collect data from devices such as MRI, IVs for real-time issue detection and analysis.

Ad Tech
Ads companies are using Flink to find out the real-time customer preference.

Oil Gas
The Oil and Gas industries are using Flink for real-time monitoring of pumping and issue detection.

Telecommunications
The telecom companies are using Apache Flink to provide the best services to the users such as real-time view of billing and payment, the optimization of antenna per-user location, mobile offers, and so on.

[Table of Contents](#Apache-Flink)

## What are the different ways to use Apache Flink?
Apache Flink can be deployed and configured in the below ways.
Flink can be setup Locally (Single Machine)
It can be deployed on a VM machine.
We can use Flink as a Docker image.
We can configure and deploy Flink as a standalone cluster.
Flink can be deployed and configured on Hadoop YARN and another resource managing framework.
Flink can be deployed and configured on a Cloud system.

[Table of Contents](#Apache-Flink)

## What is the different component stack of Apache Flink?
Apache Flink has a stack of components such as at storage level it supports different types of file such as HDFS, local file system, it also supports the database like HBase, MongoDB. Flink can be deployed in the standalone mode, cluster mode, and on the cloud system. It provides the dataset API for batch processing and the datastream API for stream processing also supports SQL, machine learning, and graph processing.

[Table of Contents](#Apache-Flink)

## What is the command to start Apache Flink Cluster?
We can use the following command to start the Apache Flink Cluster.
```bash
cloudduggu@ubuntu:~/flink$ ./bin/start-cluster.sh
```

[Table of Contents](#Apache-Flink)

## What is the Apache Flink SQL client and how to start it?
Apache Flink SQL client provides a command-line interface to run SQL operations such as create a table, drop table, create a view, drop the view, and other SQL commands as well.
We can start the SQL client using the below command.
```bash
cloudduggu@ubuntu:~/flink/bin$ ./start-cluster.sh
cloudduggu@ubuntu:~/flink$ ./bin/sql-client.sh embedded
```

The SQL client runs DDL and queries against tables registered with a catalog, and it supports streaming queries with windowing.

```sql
CREATE TABLE orders (
  order_id     STRING,
  customer_id  STRING,
  amount       DECIMAL(12, 2),
  order_ts     TIMESTAMP(3),
  WATERMARK FOR order_ts AS order_ts - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'orders',
  'properties.bootstrap.servers' = 'broker1:9092',
  'format' = 'json'
);

SELECT customer_id, SUM(amount) AS revenue
FROM orders
GROUP BY customer_id;
```

[Table of Contents](#Apache-Flink)

## What are the SQL statements supported in Apache Flink?
Apache Flink SQL supports the below list of statements.
SELECT query
CREATE TABLE, CREATE DATABASE, CREATE VIEW, CREATE FUNCTION
DROP TABLE, DROP DATABASE, DROP VIEW, DROP FUNCTION
ALTER TABLE, ALTER DATABASE, ALTER FUNCTION
INSERT TABLE
SQL HINTS
DESCRIBE
EXPLAIN
USE
SHOW

```sql
CREATE TABLE orders (...) WITH (...);
CREATE VIEW paid_orders AS SELECT * FROM orders WHERE amount > 0;
INSERT INTO revenue_sink SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id;
EXPLAIN SELECT * FROM orders;
SHOW TABLES;
```

[Table of Contents](#Apache-Flink)

## What is bounded and unbounded data in Apache Flink?
Apache Flink processes data in the form of bounded and unbounded streams. The bounded data will have a start point and an endpoint and the computation starts once all data has arrived. It is also called batch processing. The unbounded data will have a start point but no endpoint because it is streaming of data. The processing of unbounded data is continous and doesn't wait for complete data. As soon the data is generated the processing will start.

[Table of Contents](#Apache-Flink)

## What is the building block of Apache Flink streaming applications?
The applications which are executed on the Apache Flink cluster are defined by the following three building blocks for stream processing.
Streams
State
Time

[Table of Contents](#Apache-Flink)

## What are the most common types of applications that use the Apache Flink?
+ **Event-driven applications** such as fraud detection, anomaly detection, and rule-based alerting, where each event can trigger stateful logic.
+ **Data analytics applications** such as quality checks for telecom networks and product analysis for mobile apps.
+ **Data pipeline applications** such as continuously indexing an e-commerce catalog or feeding a lakehouse table.

[Table of Contents](#Apache-Flink)

## What are the features of the Apache Flink execution Engine?
The core of the Apache Flink architecture is the robust, distributed, dataflow engine that performs execution as a stream using cycle dataflow execution. It provides the cost-based optimization for batch and stream programs for optimum processing and able to work in distributed memory.

[Table of Contents](#Apache-Flink)

## What is Apache FlinkML?
Apache FlinkML is the machine learning library that provides APIs and scalable algorithms to perform the machine learning operations. FlinkML helps developers to reduce the Glue codes and test the code locally. The same code can be used by the developer to run on a cluster of the machine. Some of the algorithms of FlinkML are Supervised Learning, Unsupervised Learning, Data Preprocessing, and so on.

[Table of Contents](#Apache-Flink)

## How can I check the progress of an Apache Flink Program?
The best way to track the progress of the Flink program is the Apache Flink Dashboard web interface. It shows the jobs which are in running such as its state the resources allocated for that job and so on. We can start the Apache Flink Dashboard using "http://localhost:8081/".

Use the Web UI at `http://jobmanager:8081` for job state, per-operator records, backpressure, checkpoints, and the watermark per subtask. In production, scrape the REST API and metrics into Prometheus/Grafana.

```bash
curl -s http://jobmanager:8081/jobs/overview
curl -s http://jobmanager:8081/jobs/<jobId>/checkpoints | head
curl -s http://jobmanager:8081/jobs/<jobId>/metrics?get=numRecordsOut,currentInputWatermark
```

[Table of Contents](#Apache-Flink)

## How Apache Flink handles the fault-tolerance?
Apache Flink manages the fault-tolerance of stream applications by capturing the snapshot of the streaming dataflow state so in case of failure those snapshots will be used for recovery. For batch processing, Flink uses the program’s sequence of transformations for recovery.

Flink injects checkpoint barriers into the stream. When a barrier reaches an operator, that operator snapshots its state; the JobManager collects all snapshots and marks the checkpoint complete. On failure, every task restarts from the last completed checkpoint.

```python
env.enable_checkpointing(60_000)   # checkpoint every 60s
```
```yaml
# flink-conf.yaml
execution.checkpointing.mode: EXACTLY_ONCE
execution.checkpointing.interval: 60s
execution.checkpointing.timeout: 10min
execution.checkpointing.min-pause: 30s
state.backend: rocksdb
state.checkpoints.dir: s3://acme-flink/checkpoints/
```

[Table of Contents](#Apache-Flink)

## How to run an Apache Flink program using CLI mode?
We can use Apache Flink CLI(command-line interface) tool to run the programs which are built as JAR files.
For example, we can run a "WordCounts.jar" JAR file using the below command.
```bash
cloudduggu@ubuntu:~/flink$ ./bin/flink run ./examples/batch/WordCounts.jar
```

[Table of Contents](#Apache-Flink)

## What is the responsibility of JobManager in Apache Flink Cluster?
The Job Manager is responsible for managing and coordinating with distributed processing of a program. It assigns the task to node managers, handles the failures for recovery, and performs the checkpointing. It has three components namely ResourceManager, Dispatcher, and JobMaster.

[Table of Contents](#Apache-Flink)

## What is the responsibility of TaskManager in Apache Flink Cluster?
The Task Manager is responsible for executing the dataflow task and return the result to JobManager. It executes the task in the form of a slot hence the number of slots shows the number of process execution.

[Table of Contents](#Apache-Flink)

## What is the filesystem supported by Apache Flink?
Apache Flink supports the following list of the filesystem.
local filesystem
Hadoop HDFS
Amazon S3
MapR FS
OpenStack Swift FS
Aliyun OSS
Azure Blob Storage

[Table of Contents](#Apache-Flink)

## What is the difference between stream processing and batch processing?
Batch processing consumes a bounded data set: all input is available before computation starts, so the engine can sort, optimize globally, and finish. Stream processing consumes an unbounded data set: results must be produced continuously as records arrive, with bounded state and event-time handling for out-of-order data.

Flink unifies both. A bounded job is simply a stream that ends, and the same operators run in both modes. The practical differences are latency, state size, and how the engine decides that a window is complete.

```text
batch:   read all input -> optimize -> compute -> write result
stream:  source -> operator -> operator -> sink   (runs forever, stateful)
```

[Table of Contents](#Apache-Flink)

## What can I do with my state?
Flink There are two main ways to use state ：
checkpoint Data recovery
Logical computing

[Table of Contents](#Apache-Flink)

## Flink watermark Transmission mechanism.
Flink Medium watermark Mechanism is used to deal with disorder ,flink It has to be event time , A simple example is , If the window is 5 second ,watermark yes 2 second , that All in all 7 second , When will calculation be triggered at this time , Suppose the initial time of the data is 1000, Then wait until 6999 It will trigger 5999 The calculation of windows , So the next one is 13999 Is triggered when 10999 The window of
In fact, this is watermark The mechanism of , In multi parallelism , For example, in kafka The window will not be triggered until all partitions are reached

[Table of Contents](#Apache-Flink)

## Flink The time semantics of?
Event Time Time of occurrence
Ingestion time Events enter Flink Time for
processing time The time that the event enters the operator

[Table of Contents](#Apache-Flink)

## Flink window join:
1、window join, That is, according to the specified fields and scrolling sliding window and session window inner join
2、 yes coGoup In fact, that is left join and right join,
3、interval join That is to say In the window join There are some problems , Because some of the data really came after the meeting , It's still a long time , Then there will be interval join But it has to be the time of the event , And also specify watermark And water level and getting event timestamps . And set it up Offset interval , because join I can't wait all the time .

```java
// Tumbling window inner join: join on key and time window
left.join(right)
    .where(a -> a.key)
    .equalTo(b -> b.key)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .apply(new JoinFunction<Event, Event, Joined>() {
        @Override
        public Joined join(Event a, Event b) { return new Joined(a, b); }
    });

// Interval join: right timestamp -5min <= left timestamp <= right timestamp +5min
keyedLeft.intervalJoin(keyedRight)
    .between(Time.minutes(-5), Time.minutes(5))
    .process(new ProcessJoinFunction<Event, Event, Joined>() {
        @Override
        public void processElement(Event a, Event b, Context ctx, Collector<Joined> out) {
            out.collect(new Joined(a, b));
        }
    });

// CoGroup (outer-join semantics) over a window
left.coGroup(right)
    .where(a -> a.key)
    .equalTo(b -> b.key)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .apply(new CoGroupFunction<Event, Event, Joined>() {
        @Override
        public void coGroup(Iterable<Event> l, Iterable<Event> r, Collector<Joined> out) {
            // emit combinations; a missing side gives outer-join semantics
        }
    });
```

These joins are part of the Java/Scala DataStream API; PyFlink does not expose `join`, `coGroup`, or `intervalJoin`.

Window joins require both sides to be keyed on the same expression and to share the window, which bounds the join state. Interval joins avoid buffering an entire window.

[Table of Contents](#Apache-Flink)

## Flink What are the window functions:
Tumbing window
Silding window
Session window
Count winodw

[Table of Contents](#Apache-Flink)

## keyedProcessFunction How it works
keyedProcessFunction There is one ontime Operation of the , If so event In time that The time to call is to look at ,event Of watermark Is it greater than trigger time Time for , If it is greater than, calculate it , No, just wait , If it is kafka Words , Then the default is to trigger the partition key in the shortest time .

[Table of Contents](#Apache-Flink)

## How to deal with offline data such as the association with offline data?
1、async io
2、broadcast
3、async io + cache
4、open Method , Then the thread is refreshed at a fixed time , Cache updates are deleted first , Then write another one, and then write to the cache

Dimension enrichment from a database or object store is usually done one of four ways, in increasing order of freshness and cost:

+ **Async I/O**: query an external system per record without blocking the operator thread.
+ **Broadcast state**: broadcast a small dimension to every task.
+ **Async I/O plus cache**: add a TTL cache in front of the lookup.
+ **Scheduled refresh**: load the dimension in `open()` and refresh on a timer.

```java
public class DimLookup extends RichAsyncFunction<Order, Enriched> {
    private transient DatabaseClient client;

    @Override
    public void open(Configuration parameters) {
        client = makeClient();
    }

    @Override
    public void asyncInvoke(Order key, ResultFuture<Enriched> resultFuture) {
        client.query(key, record -> resultFuture.complete(Collections.singleton(record)));
    }
}

// Async I/O must be wrapped by AsyncDataStream (ordered/unordered wait)
AsyncDataStream.unorderedWait(stream, new DimLookup(), 1000, TimeUnit.MILLISECONDS)
    .sinkTo(kafkaSink);
```

PyFlink does not expose `RichAsyncFunction`/`AsyncDataStream`; use the Java DataStream API above or a Table API lookup join.

[Table of Contents](#Apache-Flink)

## What if there is a data skew?
Flink How to view data skew ：
stay flink Of web ui You can see the data skew in , It's every one subtask The amount of data processed varies greatly , For example, some have only one M yes , we have 100M This is a serious data skew .
KafkaSource Data skew at the end
For example, upstream kafka It was specified when it was sent key There are data hotspots , So just after the access , Do a load balancing （ The premise is not keyby）.
Aggregation class operator data skew
Pre aggregation plus global aggregation

Look at the Flink Web UI: if one subtask processes far more records than its peers, that key group is hot. Two fixes:

+ **Pre-aggregate** locally before the global aggregation (a combiner), so the hot key sends fewer rows.
+ **Salt the key** for the hot keys, aggregate per salt, then aggregate again over the salts.

```python
# local pre-aggregation then global aggregation
partial = stream.key_by(lambda e: e["key"]).process(LocalAgg())
final = partial.key_by(lambda e: e["key"]).process(GlobalAgg())

# salted key for a small number of hot keys
import random
salted = stream.map(lambda e: (f"{e['key']}-{random.randint(0, 9)}", e))
agg = salted.key_by(lambda t: t[0]).reduce(sum_amount)
result = agg.map(lambda t: (t[0].rsplit("-", 1)[0], t[1])).key_by(lambda t: t[0]).reduce(sum_amount)
```

[Table of Contents](#Apache-Flink)

## How to do dimension table Association?
1、async io
2、broadcast
3、async io + cache
4、open Method , Then the thread is refreshed at a fixed time , Cache updates are deleted first , Then write another one, and then write to the cache

For a slowly changing dimension, the two production patterns are a **lookup join** (Flink SQL, backed by an async lookup) and a **broadcast dimension** (Temporal Table Join).

```sql
-- Lookup join against a JDBC dimension with a cache
SELECT o.order_id, o.amount, c.region
FROM orders AS o
JOIN dim_customer FOR SYSTEM_TIME AS OF o.proc_time AS c
  ON o.customer_id = c.customer_id;
```
```sql
CREATE TABLE dim_customer (
  customer_id STRING, region STRING, updated_at TIMESTAMP(3),
  PRIMARY KEY (customer_id) NOT ENFORCED
) WITH (
  'connector' = 'jdbc',
  'url' = 'jdbc:postgresql://pg:5432/app',
  'table-name' = 'customer',
  'lookup.cache.max-rows' = '10000',
  'lookup.cache.ttl' = '10min'
);
```

[Table of Contents](#Apache-Flink)

## Flink checkpoint The overtime problem of How to solve?
1、 Is there a network problem
2、 Whether it is barrir problem
3、 see webui, Whether there is data skew
4、 If there's a data skew , So after solving the data skew , There will be improvements ,

Checkpoint timeouts almost always have one of four causes: backpressure, a slow external system inside the checkpoint, a barrier stuck behind a large in-flight batch, or RocksDB state that has grown too large.

```yaml
execution.checkpointing.timeout: 10min
execution.checkpointing.min-pause: 30s
execution.checkpointing.max-concurrent-checkpoints: 1
state.backend.incremental: true
state.backend.rocksdb.memory.managed: true
```

Diagnose with the Web UI: check the alignment time, the sync/async checkpoint durations, and whether one subtask is slow (data skew). Enabling unaligned checkpoints removes the barrier-alignment wait when backpressure is the cause.

[Table of Contents](#Apache-Flink)

## FlinkTopN And offline TopN The difference between?
topn It is a common function in both offline and real-time computing , It's different from... In offline computing topn, Real time data is continuous , This will give topn It's very difficult to calculate , Because it's going to keep a... In memory topn Data structure of , When new data comes , Update this data structure

[Table of Contents](#Apache-Flink)

## Sparkstreaming and flink in checkpoint?
sparkstreaming Of checkpoint It will lead to repeated consumption of data
however flink Of checkpoint Sure Make sure it's accurate one time , At the same time, it can be incremental , fast checkpoint Of , There are three states ,memery、rocksdb、hdfs

[Table of Contents](#Apache-Flink)

## A brief introduction cep State programming:
Complex Event Processing（CEP）：
FLink Cep Is in FLink Complex time processing library implemented in ,CEP Allows event patterns to be detected in an endless stream of time , Give us a chance to grasp the important parts of the data , One or more time streams composed of simple events are matched by certain rules , Then output the data the user wants , That is, complex events that satisfy the rules .
Flink Data aggregation in , How to aggregate without windows
valueState Used to save a single value
ListState Used to hold list Elements
MapState Used to save a set of key value pairs
ReducingState Provided with ListState Same method , Return to one ReducingFunction The aggregated value .
AggregatingState and ReducingState similar , Return to one AggregatingState The value after internal aggregation

Flink CEP matches event patterns over a stream, and the underlying state is ordinary keyed state.

```java
Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
    .where(evt -> evt.getAmount() > 10_000)
    .next("confirm")
    .where(evt -> evt.getAmount() > 10_000)
    .within(Time.minutes(5));

PatternStream<Event> alerts = CEP.pattern(stream.keyBy(Event::getAccountId), pattern);
```

CEP lives in the Java/Scala `flink-cep` library; PyFlink has no `cep` module.

Flink exposes several state primitives: `ValueState` (one value), `ListState` (a list), `MapState` (a key-value map), `ReducingState` and `AggregatingState` (incrementally aggregated values).

[Table of Contents](#Apache-Flink)

## How to deal with abnormal data in Flink.
Abnormal data in our scenario , It is generally divided into missing fields and outlier data .
outliers ： For example, data on the age of the baby , For example, for the maternal and infant industry , The age of a baby is a crucial data , It's the most important , Because the baby is bigger than 3 At the age of 20, you hardly buy things from mothers and babies . There are days like ours 、 Unknown 、 And for a long time . This is an exception field , We will show the data to store managers and regional managers , Let them know how many ages are not allowed . If we have to deal with it , It can be corrected in real time according to the time of purchase , For example, maternity clothing 、 The rank of milk powder 、 The size of a diaper , As well as pacifiers, some can distinguish the age group to carry on the processing . We don't process the data in real time , We're going to have a low-level strategy task, night dimension, to run , Run once a week .
Missing field ： For example, some fields are really missing , If you can fix it, you can fix it . Give up if you can't fix it , It's like the news recommendation filter in the last company .

[Table of Contents](#Apache-Flink)

## Is there any possibility of data loss in Flink?
Flink There are three kinds of data consumption semantics ：
At Most Once One consumption at most In case of failure, it may be lost
At Least Once At least once If there is a fault, it may be repeated
Exactly-Once Exactly once If something goes wrong , It can also ensure that the data will not be lost or repeated .
flink The new version is no longer available At-Most-Once semantics .

Flink interval join Can you write it simply
```java
KeyedStream<Event, String> keyed1 = ds1.keyBy(o -> o.getString("key"));
KeyedStream<Event, String> keyed2 = ds2.keyBy(o -> o.getString("key"));
// right.ts - 5s <= left.ts <= right.ts + 5s
keyed1.intervalJoin(keyed2)
    .between(Time.seconds(-5), Time.seconds(5))
    .process(new ProcessJoinFunction<Event, Event, Joined>() {
        @Override
        public void processElement(Event a, Event b, Context ctx, Collector<Joined> out) {
            out.collect(new Joined(a, b));
        }
    });
```

[Table of Contents](#Apache-Flink)

## At the time of submission How to make parallelism and how to allocate resources?
Parallelism based on kafka topic Parallelism of , A degree of parallelism 3 individual G

```bash
# per-job parallelism and TaskManager resources
flink run -p 16 \
  -D taskmanager.numberOfTaskSlots=4 \
  -D taskmanager.memory.process.size=4096m \
  -D jobmanager.memory.process.size=2048m \
  -c com.acme.OrdersJob orders.jar

# YARN: size the application cluster explicitly
flink run -m yarn-cluster -ynm orders-job -p 16 -ys 4 -yjm 2048m -ytm 4096m orders.jar
```

A Kafka source with `N` partitions gets at most `N` useful source parallelism, so align `-p` with the topic's partition count before scaling TaskManagers.

[Table of Contents](#Apache-Flink)

## What's the common stream of API?
window join ah cogroup ah map flatmap,async io etc.

```python
env.from_source(...)                 # source connector
stream.map / flat_map / filter       # stateless transformations
stream.key_by(...)                   # keyed stream
stream.window(...) / process(...)    # windowed or stateful processing
stream.connect(other)                # two-stream operators, co-process
stream.union(other)                  # merge same-typed streams
# async I/O: Java AsyncDataStream; PyFlink has no async_io operator
stream.sink_to(...)                  # sink connector
```

[Table of Contents](#Apache-Flink)

## How to maintain Checkpoint?
By default , If set Checkpoint Options ,Flink Only the most recently generated 1 individual Checkpoint. When Flink When the program fails , From the nearest one Checkpoint To recover . however , If we want to keep more than one Checkpoint, And can choose one of them to recover according to the actual needs , It's more flexible .Flink Support to keep multiple Checkpoint, Need to be in Flink Configuration file for conf/flink-conf.yaml in , Add the following configuration to specify that at most Checkpoint The number of .
For small files, please refer to The death of Daedalus - Solutions to the problem of small files in the field of big data .

Flink keeps only the latest completed checkpoint by default. Retain more if you want to choose a recovery point:

```yaml
# flink-conf.yaml
state.checkpoints.num-retained: 5
```
```bash
flink savepoint <jobId> s3://acme-flink/savepoints/
flink list
flink cancel -s s3://acme-flink/savepoints/ <jobId>
```

[Table of Contents](#Apache-Flink)

## What's the difference at Spark and Flink Serialization?
Spark The default is Java Serialization mechanism , At the same time, there is an optimization mechanism , That is to say kryo
Flink It's a self implemented serialization mechanism , That is to say TypeInformation

Spark defaults to Java serialization (with Kryo as an option) and pays that cost per shuffled object. Flink uses `TypeInformation` and its own serializers, so it can serialize a record once, understand its schema, and compare keys without deserializing whole objects.

```java
// Flink needs type information to build serializers
DataStream<Tuple2<String, Integer>> s = env.fromElements(new Tuple2<>("a", 1));
```

[Table of Contents](#Apache-Flink)

## How to deal with late data?
Flink Of watermark It's a delayed trigger mechanism .
commonly watermark Is and window To process out of order data ,Watermark The most fundamental is a time mechanism , For example, I set the maximum out of order time to 2s, The window time is 5 second , So when the event time is greater than 7s The window will be triggered when the window is opened . Of course, if there are data partitions , for example kafka Medium access watermake Words , that watermake It will flow , Take the smallest of all partitions watermake To flow , Because only the smallest can guarantee , All the previous data has come to , You can trigger the calculation .
use flink Can replace spark Batch processing function of
Flink The future goal is to integrate batch and stream processing , Because the batch data set you can understand is a limited data stream .Flink In terms of approval management , Especially this year Flink 1.9 Release after , Join in a large number of Hive Function of aspect , You can use Flink SQL To read Hive Metadata and datasets in , And use Flink SQL It is logically processed , But so far Flink Performance in batch processing , I can't do it Spark Of .
So far ,Flink There is still a lot to do in batch processing , Of course , If it's the introduction of real-time computing engine ,Flink Of course, it's the first choice .

Watermarks plus allowed lateness define the window's closing and grace period.

```python
stream.key_by(lambda e: e["user"]).window(
    TumblingEventTimeWindows.of(Time.minutes(5))
).allowed_lateness(120_000).side_output_late_data(late_tag).process(MyWindowFn())   # 2 minutes in ms
```

Records older than watermark minus allowed lateness go to the side output, which you can write to a quarantine sink and reconcile in a later batch job. Setting `allowed_lateness` to 0 gives the fastest results with the most late drops.

[Table of Contents](#Apache-Flink)

## When to use aggregate perhaps process:
aggregate： Incremental aggregation
process： Total polymerization
When calculating the accumulation operation, you can use aggregate operation .
When calculating the full amount of data in the window, use process, For example, sorting and other operations.

`aggregate` (or `reduce`) is an incremental aggregation: Flink keeps a small accumulator and updates it per record, so state stays constant. `process` with a window function buffers the window contents and lets you sort, iterate, and access timers, at the cost of state proportional to the window.

```python
# incremental: cheap in memory, no access to individual records
keyed.window(TumblingEventTimeWindows.of(Time.minutes(5))).aggregate(SumAmount())

# full window: needed for Top-N, sorting, or custom timers
keyed.window(TumblingEventTimeWindows.of(Time.minutes(5))).process(TopNPerRegion())
```

[Table of Contents](#Apache-Flink)

## How does checkpointing work in Flink?
Flink injects checkpoint barriers into the stream. When a barrier reaches an operator, that operator snapshots its state; once every sink acknowledges its barrier, the JobManager marks the checkpoint complete. On failure, every task restarts from the last completed checkpoint.

```python
from pyflink.datastream import CheckpointingMode, ExternalizedCheckpointCleanup

env.enable_checkpointing(10_000, CheckpointingMode.EXACTLY_ONCE)
cfg = env.get_checkpoint_config()
cfg.set_min_pause_between_checkpoints(5_000)
cfg.set_checkpoint_timeout(60_000)
cfg.set_max_concurrent_checkpoints(1)
cfg.enable_externalized_checkpoints(ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION)
```

Key knobs: interval (latency vs overhead), timeout (how long before a checkpoint is abandoned), min-pause (breathing room between checkpoints), and unaligned checkpoints (skip barrier alignment under backpressure).

[Table of Contents](#Apache-Flink)

## What are savepoints and how do you use them?
A savepoint is a manually triggered, externally owned snapshot used for upgrades, rescaling, and planned migration. Unlike a checkpoint, it is not deleted when the job stops, and it is the supported way to change job parallelism or topology.

```bash
# trigger a savepoint for a running job
flink savepoint <jobId> s3://acme-flink/savepoints/

# stop the job and take a savepoint first
flink stop --savepointPath s3://acme-flink/savepoints/ <jobId>

# resume from it, possibly with a different parallelism
flink run -s s3://acme-flink/savepoints/savepoint-xxxx -p 32 orders.jar
```

A savepoint only restores cleanly if the operator state is compatible; use `--allowNonRestoredState` only when you intentionally removed operators.

[Table of Contents](#Apache-Flink)

## How do you configure the state backend?
State backends decide where keyed state lives and how snapshots are written.

```yaml
# flink-conf.yaml
state.backend: rocksdb
state.backend.incremental: true
state.checkpoints.dir: s3://acme-flink/checkpoints/
state.savepoints.dir: s3://acme-flink/savepoints/
state.backend.rocksdb.memory.managed: true
```
```python
from pyflink.datastream import StreamExecutionEnvironment, EmbeddedRocksDBStateBackend

env = StreamExecutionEnvironment.get_execution_environment()
env.set_state_backend(EmbeddedRocksDBStateBackend(enable_incremental_checkpointing=True))
```

`HashMapStateBackend` is fastest but bounded by heap; `EmbeddedRocksDBStateBackend` supports state larger than memory with incremental checkpoints, at the cost of local disk I/O. State TTL (`StateTtlConfig`) is what keeps long-running keyed state from growing forever.

[Table of Contents](#Apache-Flink)

## How do you build an exactly-once Kafka to Kafka pipeline?
End-to-end exactly-once needs three things: checkpointing enabled, a replayable source that stores offsets in Flink state, and a transactional sink that only commits when a checkpoint completes.

```python
from pyflink.common import WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment, CheckpointingMode
from pyflink.datastream.connectors.kafka import (
    KafkaSource, KafkaSink, KafkaOffsetsInitializer,
    KafkaRecordSerializationSchema, DeliveryGuarantee,
)

env = StreamExecutionEnvironment.get_execution_environment()
env.enable_checkpointing(10_000, CheckpointingMode.EXACTLY_ONCE)

source = (
    KafkaSource.builder()
    .set_bootstrap_servers("broker1:9092")
    .set_topics("orders")
    .set_group_id("orders-flink")
    .set_starting_offsets(KafkaOffsetsInitializer.committed_offsets())
    .set_value_only_deserializer(SimpleStringSchema())
    .build()
)

sink = (
    KafkaSink.builder()
    .set_bootstrap_servers("broker2:9092")
    .set_record_serializer(
        KafkaRecordSerializationSchema.builder()
        .set_topic("orders-enriched")
        .set_value_serialization_schema(SimpleStringSchema())
        .build()
    )
    .set_delivery_guarantee(DeliveryGuarantee.EXACTLY_ONCE)
    .set_transactional_id_prefix("orders-flink-")
    .build()
)

stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "kafka-orders")
stream.map(lambda v: v.upper()).sink_to(sink)
env.execute("orders-exactly-once")
```

Offsets are committed into the checkpoint (two-phase commit), and the Kafka transactions are committed only after the checkpoint succeeds, so a failure replays from the last checkpoint without duplicates downstream.

[Table of Contents](#Apache-Flink)

## How do you do windowing in Flink SQL?
Flink SQL uses table-valued window functions, which are composable with normal `GROUP BY` and joins.

```sql
-- Tumbling window: one row per minute per region
SELECT window_start, window_end, region, SUM(amount) AS revenue
FROM TABLE(TUMBLE(TABLE orders, DESCRIPTOR(order_ts), INTERVAL '1' MINUTE))
GROUP BY window_start, window_end, region;

-- Sliding (HOP) window: emitted every minute over a 10-minute span
SELECT window_start, window_end, region, COUNT(*) AS orders
FROM TABLE(HOP(TABLE orders, DESCRIPTOR(order_ts), INTERVAL '1' MINUTE, INTERVAL '10' MINUTE))
GROUP BY window_start, window_end, region;

-- Cumulative window: running totals for the day
SELECT window_start, window_end, region, SUM(amount) AS revenue
FROM TABLE(CUMULATE(TABLE orders, DESCRIPTOR(order_ts), INTERVAL '1' HOUR, INTERVAL '1' DAY))
GROUP BY window_start, window_end, region;
```

Window results are emitted to the sink as the watermark advances past the window end; a record that arrives after its window has fired is dropped by default, and whether an already-emitted row can be corrected depends on the sink supporting retract/upsert updates.

[Table of Contents](#Apache-Flink)

## How do you handle event time and watermarks in PyFlink?
Assign timestamps and a watermark strategy at the source, so every downstream operator has a consistent notion of event time.

```python
from pyflink.common import Duration, WatermarkStrategy
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()

class EventTimestamps(TimestampAssigner):
    def extract_timestamp(self, event, record_timestamp):
        return event["event_ts"]

watermarks = (
    WatermarkStrategy
    .for_bounded_out_of_orderness(Duration.of_seconds(5))
    .with_idleness(Duration.of_minutes(1))
)

stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "kafka-orders")
stream = stream.assign_timestamps_and_watermarks(
    watermarks.with_timestamp_assigner(EventTimestamps())
)
keyed = stream.key_by(lambda e: e["user_id"])
```

`for_bounded_out_of_orderness(5s)` holds windows for five seconds past the newest event timestamp, and `with_idleness` prevents a silent partition from freezing all watermarks. Watermarks are per partition and the operator takes the minimum.

[Table of Contents](#Apache-Flink)

## What are Flink's trade-offs and when should you not use it?
+ **Performance:** millisecond latency and true event-time semantics, but throughput per core is lower than Spark's micro-batch and JVM/GC tuning matters.
+ **Resource contention:** state size, checkpoint duration, and TaskManager memory are tightly coupled; RocksDB state spills to local disk and a slow disk becomes a checkpoint bottleneck.
+ **Exactly-once:** guaranteed only when the source is replayable and the sink supports transactions or idempotent upserts. An external JDBC write is not transactional unless you make it idempotent.
+ **Operations:** savepoints, state schema evolution, and watermark/backpressure diagnosis require real operational maturity.

When NOT to use Flink: simple scheduled batch jobs (Spark/dbt are cheaper), pure ETL with no state or latency requirement, tiny data volumes, or teams without the operational capacity to run a stateful cluster.

[Table of Contents](#Apache-Flink)

## Real world use cases for Apache Flink
### 1. Real-time fraud detection

A payments company scores every card transaction within milliseconds and blocks suspicious ones. ~8,000 transactions/second (~700 million/day), 30-day rolling per-account state. Kafka carries transactions keyed by `account_id`; Flink keeps per-account velocity and amount state in RocksDB and writes alerts to Kafka and a case-management API.

```python
keyed = transactions.key_by(lambda t: t["account_id"])
alerts = keyed.process(VelocityDetector())   # timers + ValueState per account
alerts.sink_to(kafka_sink("fraud.alerts"))
```

Why: event time plus keyed state gives deterministic, replayable scoring, and exactly-once avoids double-blocking a customer after a failure.

### 2. Continuous lakehouse ingestion from CDC

A retailer streams Debezium change events into an Iceberg table with upserts. ~120,000 events/second, ~40 TB of current-state data, 5-minute checkpoints. Kafka source with committed offsets, Flink SQL `MERGE` (or the Iceberg sink), and hourly Iceberg compaction.

```sql
INSERT INTO lakehouse.customers
SELECT customer_id, name, email, updated_at
FROM cdc_customers;
```
```python
env.enable_checkpointing(300_000, CheckpointingMode.EXACTLY_ONCE)
```

Why: checkpointed Kafka offsets plus a transactional Iceberg sink make ingestion exactly-once, and Flink absorbs bursty CDC without a nightly rebuild.

### 3. Sessionization and product analytics

A media platform groups viewer events into sessions and computes engagement metrics. ~25,000 events/second, 10-minute session gaps, late-arriving mobile events up to 2 minutes old. Session windows with allowed lateness and a side output for late records.

```python
sessions = (
    events.key_by(lambda e: e["user_id"])
    .window(EventTimeSessionWindows.with_gap(Time.minutes(10)))
    .allowed_lateness(120_000)   # 2 minutes in ms
    .side_output_late_data(late_tag)
    .process(SessionMetrics())
)
```

Why: session windows match the business concept directly, and allowed lateness plus a side output turns "late" into a handled case instead of a silent drop.

### 4. Real-time alerting on infrastructure metrics

A SaaS provider detects anomalies in host and application metrics. ~500,000 samples/second, 1-second resolution, 15-minute sliding windows. Flink aggregates metrics, compares against a broadcast model, and emits alerts.

```python
windowed = (
    metrics.key_by(lambda m: m["host_id"])
    .window(SlidingEventTimeWindows.of(Time.minutes(15), Time.minutes(1)))
    .aggregate(MetricStats())
)
alerts = windowed.connect(model_stream.broadcast(state_descriptor)).process(AnomalyFn())
```

Why: a broadcast state stream lets the detection model update without redeploying the job, and sliding windows give continuous coverage instead of fixed buckets.

### 5. Exactly-once enrichment pipeline to Kafka

A logistics company enriches shipment events with customer and route data and republishes them. ~15,000 events/second, JDBC dimensions with a 10-minute cache, exactly-once output. Async lookup join for the dimension, Kafka source and transactional Kafka sink.

```python
env.enable_checkpointing(10_000, CheckpointingMode.EXACTLY_ONCE)
enriched = orders.key_by(lambda o: o["customer_id"]).map(AsyncDimLookup())
enriched.sink_to(exactly_once_kafka_sink("shipments-enriched"))
```

Why: async I/O keeps the external lookup off the operator thread, and transactional Kafka writes plus checkpointed offsets give true end-to-end exactly-once.

[Table of Contents](#Apache-Flink)
