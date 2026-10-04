## [Main title](../README.md)
### [Interview questions](full.md)

# NiFi

**Notebook:** [`notebooks/topics/nifi.ipynb`](../notebooks/topics/nifi.ipynb) - runnable version of this topic with self-checking exercises.

Apache NiFi is a flow-based data distribution and processing system: you build a dataflow from processors that route, transform, enrich, and deliver FlowFiles, and NiFi handles the reliability, backpressure, provenance, and clustering around that flow.
+ [What is Apache NiFi?](#What-is-Apache-NiFi)
+ [What is NiFi FlowFile?](#What-is-NiFi-FlowFile)
+ [What is Relationship in NiFi DataFlow?](#What-is-Relationship-in-NiFi-DataFlow)
+ [What is Reporting Task?](#What-is-Reporting-Task)
+ [What is a NiFi Processor?](#What-is-a-NiFi-Processor)
+ [Is there a programming language that Apache NiFi supports?](#Is-there-a-programming-language-that-Apache-NiFi-supports)
+ [How do you define NiFi content Repository?](#How-do-you-define-NiFi-content-Repository)
+ [What is the Backpressure in NiFi system?](#What-is-the-Backpressure-in-NiFi-system)
+ [What is the template in NiFi?](#What-is-the-template-in-NiFi)
+ [What is the bulletin and how does it help in NiFi?](#What-is-the-bulletin-and-how-does-it-help-in-NiFi)
+ [Do the attributes get added to content (actual Data) when data is pulled by NiFi?](#Do-the-attributes-get-added-to-content-actual-Data-when-data-is-pulled-by-NiFi)
+ [What happens if you have stored a password in a dataflow and create a template out of it?](#What-happens-if-you-have-stored-a-password-in-a-dataflow-and-create-a-template-out-of-it)
+ [How does NiFi support huge volume of Payload in a Dataflow?](#How-does-NiFi-support-huge-volume-of-Payload-in-a-Dataflow)
+ [What is a NiFi custom properties registry?](#What-is-a-NiFi-custom-properties-registry)
+ [Does NiFi works as a Master Slave architecture?](#Does-NiFi-works-as-a-Master-Slave-architecture)
+ [How do you design a reliable NiFi flow?](#How-do-you-design-a-reliable-NiFi-flow)
+ [What are FlowFiles and provenance in NiFi?](#What-are-FlowFiles-and-provenance-in-NiFi)
+ [How do you version and promote NiFi flows as JSON?](#How-do-you-version-and-promote-NiFi-flows-as-JSON)
+ [How do you use Expression Language and record processing in NiFi?](#How-do-you-use-Expression-Language-and-record-processing-in-NiFi)
+ [How do you secure a NiFi deployment?](#How-do-you-secure-a-NiFi-deployment)
+ [How do you monitor NiFi and tune throughput?](#How-do-you-monitor-NiFi-and-tune-throughput)
+ [When should you NOT use NiFi?](#When-should-you-NOT-use-NiFi)
+ [Real world use cases for NiFi](#Real-world-use-cases-for-NiFi)

## What is Apache NiFi?
NiFi is helpful in creating DataFlow. It means you can transfer data from one system to another system as well as process the data in between. It was built at NSA to solve exactly the problem of moving data reliably between systems with different formats, protocols, and security models, and it became an Apache top-level project.

The design philosophy that interviewers care about:

+ **Flow-based programming**: processors are black boxes with typed relationships, and you compose behavior by wiring them together rather than writing a monolith.
+ **Guaranteed delivery**: FlowFiles sit in persisted repositories, so a restart or crash does not lose data that was already accepted.
+ **Backpressure and prioritization**: queues can tell upstream processors to stop, and you can prioritize which data moves first.
+ **Provenance**: every event on every FlowFile is recorded and queryable, down to the byte offset in a file.
+ **Zero-master clustering**: every node can do every job; coordinator and primary-node roles are elected, not statically assigned.

```text
ConsumeKafka -> ValidateRecord -> RouteOnAttribute -> PutS3Object  (valid, partitioned)
                                      |
                                      +-> PutFile (dead letter)

FlowFiles carry content + attributes; connections hold queues with backpressure.
```

Typical interview framing: NiFi is strongest as a *data ingress, routing, and last-mile delivery* layer, especially when you need protocol adapters (SFTP, JMS, MQTT, REST), per-record enrichment, or audit-ready lineage without writing a service. It is not a replacement for a general compute engine.

[Table of Contents](#NiFi)

## What is NiFi FlowFile?
A FlowFile is a message or event data or user data, which is pushed or created in the NiFi. A FlowFile has mainly two things attached with it. Its content (Actual payload: Stream of bytes) and attributes. Attributes are key value pairs attached to the content (You can say metadata for the content).

The critical design point is that a FlowFile is a **pointer**, not a blob. Content lives in the content repository; attributes live in memory and travel with the FlowFile reference.

Core attributes that NiFi sets automatically:

| Attribute | Meaning |
|---|---|
| `uuid` | Unique FlowFile identifier, used in provenance |
| `filename` | Logical file name |
| `path` / `absolute.path` | Source directory |
| `mime.type` | Content type |
| `size` | Content size in bytes |
| `entryDate` | When the FlowFile entered NiFi |
| `lineageStartDate` | Start of the current lineage chain |
| `fragment.identifier`, `fragment.index` | Split/merge bookkeeping |

```text
uuid=9c1f0f7e-1b2a-1c3d-4e5f-6a7b8c9d0e1f
filename=orders_20261004.json
path=/landing/orders/
absolute.path=/data/landing/orders/
mime.type=application/json
size=184320
entryDate=2026-10-04T12:31:00Z
```

Processors can read and write attributes without touching content, and expression language operates on attributes. That is why a `RouteOnAttribute` can branch on `filename` or `ingest_date` without reading a single byte of payload from disk.

[Table of Contents](#NiFi)

## What is Relationship in NiFi DataFlow?
When a processor finishes with processing of FlowFile. It can result in Failure or Success or any other relationship. And based on this relationship you can send data to the Downstream or next processor or mediated accordingly.

Relationships are the contract of a processor. Common ones are `success`, `failure`, `retry`, `original`, `unmatched`, `matched`, `invalid`, and `not.found`. Every relationship must either be connected or explicitly auto-terminated, and NiFi refuses to start a processor whose relationships are unhandled.

```text
ValidateRecord --valid----> ConvertRecord --success--> PutS3Object
               --invalid--> PutFile (/dead-letter/orders)
               --failure--> RetryFlowFile --> ValidateRecord
```

```json
{
  "component": {
    "name": "RouteOnAttribute",
    "type": "org.apache.nifi.processors.standard.RouteOnAttribute",
    "config": {
      "properties": {
        "Routing Strategy": "Route to Property name",
        "valid": "${amount:toNumber():ge(0)}",
        "high_value": "${amount:toNumber():ge(10000)}"
      },
      "autoTerminatedRelationships": ["unmatched"]
    }
  }
}
```

Interview notes:

+ Routing on a relationship is how you build dead-letter queues, retries, and priority lanes without extra infrastructure.
+ Auto-terminating `failure` on a sink is a common production mistake: it silently drops data. Route failures somewhere observable.
+ A processor penalizes a FlowFile when it routes to a relationship like `retry`, which delays re-processing and prevents hot loops.

[Table of Contents](#NiFi)

## What is Reporting Task?
A Reporting Task is a NiFi extension point that is capable of reporting and analyzing NiFi's internal metrics in order to provide the information to external resources or report status information as bulletins that appear directly in the NiFi User Interface.

Reporting tasks run on a schedule and read NiFi's own telemetry, not the dataflow payload. Common examples:

+ `ControllerStatusReportingTask`: queue sizes, processor statistics, and status.
+ `MonitorMemory`: emits a bulletin when JVM memory crosses a threshold.
+ `PrometheusReportingTask`: exposes NiFi metrics for Prometheus scraping.
+ `SiteToSiteStatusReportingTask`: pushes status to another NiFi or monitoring system.
+ `AmbariReportingTask`: integrates with Ambari-based operations stacks.

```json
{
  "revision": {"version": 1},
  "component": {
    "name": "prometheus-reporting",
    "type": "org.apache.nifi.reporting.prometheus.PrometheusReportingTask",
    "properties": {
      "Metrics Reporting Strategy": "All Components",
      "Send JVM Metrics": "true",
      "Send System Metrics": "true"
    },
    "schedulingPeriod": "60 sec",
    "schedulingStrategy": "TIMER_DRIVEN"
  }
}
```

Interview point: reporting tasks are the bridge between NiFi and your observability stack. A NiFi deployment without them is a black box, because queue growth and backpressure are the leading indicators of a dataflow problem.

[Table of Contents](#NiFi)

## What is a NiFi Processor?
Processor is a main component in the NiFi, which will really work on the FlowFile content and helps in creating, sending, receiving, transforming routing, splitting, merging, and processing FlowFile.

Processor categories and examples:

| Category | Examples |
|---|---|
| Ingest | `ConsumeKafka`, `GetFile`, `GetSFTP`, `ListenHTTP`, `ExecuteSQL`, `GetMongo` |
| Transform | `ConvertRecord`, `UpdateRecord`, `JoltTransformJSON`, `ReplaceText` |
| Enrich | `LookupRecord`, `InvokeHTTP`, `DistributedMapCacheClientService` |
| Route | `RouteOnAttribute`, `RouteOnContent`, `QueryRecord` |
| Split/merge | `SplitJson`, `SplitRecord`, `MergeContent`, `MergeRecord` |
| Deliver | `PutS3Object`, `PutHDFS`, `PublishKafka`, `PutDatabaseRecord`, `PutFile` |

Each processor is configured with properties, scheduling, and relationships. A REST-style processor configuration:

```json
{
  "revision": {"version": 3},
  "component": {
    "id": "b1d2f3a4-0001-1000-ffff-abcdef123456",
    "name": "UpdateAttribute",
    "type": "org.apache.nifi.processors.attributes.UpdateAttribute",
    "config": {
      "properties": {
        "ingest_date": "${now():format('yyyy-MM-dd')}",
        "source_system": "orders-api",
        "s3_prefix": "raw/orders/dt=${ingest_date}"
      },
      "schedulingStrategy": "TIMER_DRIVEN",
      "schedulingPeriod": "0 sec",
      "concurrentTasks": 4,
      "autoTerminatedRelationships": ["success"]
    }
  }
}
```

Tuning notes that matter in interviews: `concurrentTasks` controls parallelism per processor, `run duration` trades latency for throughput, and `@OnScheduled`-style controller services (record readers/writers, connection pools) are shared rather than per-processor.

[Table of Contents](#NiFi)

## Is there a programming language that Apache NiFi supports?
NiFi is implemented in the Java programming language and allows extensions (processors, controller services, and reporting tasks) to be implemented in Java. In addition, NiFi supports processors that execute scripts written in Groovy, Jython, and several other popular scripting languages.

Practical options for custom logic:

+ `ExecuteScript`: runs Groovy, Jython, JRuby, or JavaScript (JSR-223) against a FlowFile in-process.
+ `InvokeScriptedProcessor`: defines a custom processor interface in Groovy with `onTrigger`.
+ `ExecuteStreamCommand`: shells out to any CLI, including Python, R, or a compiled binary.
+ Custom NAR: a packaged Java extension for production-grade processors with dependencies.

```python
# Programmatic flow management with the nipyapi Python client (no Java required).
import nipyapi

nipyapi.config.default_host = "nifi.internal:8443"

flow = nipyapi.canvas.get_flow("orders_ingest")
for processor in nipyapi.canvas.list_all_processors(process_group_id=flow.id):
    print(processor.component.name, processor.component.type)
```

Interview nuance: scripting processors are convenient but slower than native processors and harder to test, and Jython is Python 2-era. For anything on the critical path, prefer native processors or a packaged Java extension; use scripts for glue and one-off transforms.

[Table of Contents](#NiFi)

## How do you define NiFi content Repository?
As we mentioned previously, contents are not stored in the FlowFile. They are stored in the content repository and referenced by the FlowFile. This allows the contents of FlowFiles to be stored independently and efficiently based on the underlying storage mechanism.

NiFi has three local repositories plus provenance:

+ **FlowFile repository**: the write-ahead log of FlowFile metadata and pointers, so state survives restart.
+ **Content repository**: the actual bytes, stored in per-partition directories and referenced by claim.
+ **Provenance repository**: the event history used for lineage and replay.
+ **Database repository**: internal state for newer NiFi versions (component state, versions).

```text
nifi.flowfile.repository.directory.default=./flowfile_repository
nifi.content.repository.directory.default=./content_repository
nifi.provenance.repository.directory.default=./provenance_repository
nifi.database.repository.directory=./database_repository

nifi.content.claim.max.appendable.size=1 MB
nifi.content.repository.archive.max.usage.percentage=50%
nifi.content.repository.archive.enabled=true
nifi.content.repository.archive.cleanup.frequency=1 min
```

How it works in practice: small FlowFiles are written into a shared **claim** file to avoid a file per FlowFile, and a content claim is reference-counted. When a FlowFile is deleted, its claim bytes eventually become garbage and the archive cleanup reclaims them. `nifi.content.claim.max.appendable.size` is therefore a throughput lever, and repository disk usage is a capacity-planning requirement, not an afterthought.

[Table of Contents](#NiFi)

## What is the Backpressure in NiFi system?
Sometime what happens that Producer system is faster than consumer system. Hence, the messages which are consumed is slower. Hence, all the messages (FlowFiles) which are not being processed will remain in the connection buffer. However, you can limit the connection backpressure size either based on number of FlowFiles or number of data size. If it reaches to defined limit, connection will give back pressure to producer processor not run. Hence, no more FlowFiles generated, until backpressure is reduced.

Each connection has two thresholds, and the queue is "full" when either is exceeded:

+ **Back Pressure Object Threshold**: maximum number of FlowFiles in the queue (default 10,000).
+ **Back Pressure Data Size Threshold**: maximum bytes in the queue (default 1 GB).

```json
{
  "component": {
    "id": "c2e3f4a5-0002-2000-ffff-abcdef123456",
    "config": {
      "backPressureObjectThreshold": 50000,
      "backPressureDataSizeThreshold": "2 GB",
      "flowFileExpiration": "0 sec",
      "prioritizers": ["org.apache.nifi.prioritizer.NewestFlowFileFirstPrioritizer"]
    }
  }
}
```

Interview notes:

+ Backpressure protects memory and downstream systems; without it, a fast producer fills the queue, exhausts heap, and takes down the node.
+ It is per-connection, so a slow branch stops only its own upstream processor, not the whole flow.
+ Prioritizers decide *which* FlowFile moves when a queue is drained; they do not increase throughput. Use them for SLAs, for example newest-first for real-time dashboards and oldest-first for regulatory files.
+ `flowFileExpiration` is the safety valve; setting it to `0 sec` disables expiry, which is fine only when you have real backpressure and alerting.

[Table of Contents](#NiFi)

## What is the template in NiFi?
Template is a re-usable workflow. Which you can import and export in the same or different NiFi instances. It can save lot of time rather than creating Flow again and again each time. Template is created as an xml file.

Templates were the original reuse mechanism: export a process group as XML, upload it to another instance, and instantiate it. They are still present but effectively legacy for two reasons: passwords are stripped on export (see below), and templates have no version history or promotion workflow.

The modern mechanism is **versioned flows** backed by NiFi Registry or a Git-backed flow registry. You commit the entire process group as JSON, and each change becomes a numbered version with an author and comment.

```json
{
  "name": "orders_ingest",
  "bucketIdentifier": "7c2f0f3e-1111-2222-3333-444455556666",
  "versionCount": 12,
  "snapshotMetadata": {
    "version": 12,
    "author": "data-platform",
    "comments": "Add dead-letter routing for schema failures"
  }
}
```

```bash
# Promote version 12 of a versioned flow into another environment.
curl -k -X POST "https://nifi-uat.internal:8443/nifi-api/versions/process-groups/${PG_ID}" \
  -H "Authorization: Bearer ${NIFI_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"processGroupRevision":{"version":1},"versionControlInformation":{"groupId":"7c2f0f3e-1111-2222-3333-444455556666","registryId":"reg-1","version":12}}'
```

Interview answer: use templates only for throwaway demos and legacy migrations; use Registry/Git-backed versioned flows with parameter contexts for real promotion across dev, UAT, and prod.

[Table of Contents](#NiFi)

## What is the bulletin and how does it help in NiFi?
If you want to know if any problems occur in a dataflow. You can check in the logs for anything interesting, it is much more convenient to have notifications pop up on the screen. If a Processor logs anything as a WARNING or ERROR, we will see a "Bulletin Indicator" show up in the top-right-hand corner of the Processor.

This indicator looks like a sticky note and will be shown for five minutes after the event occurs. Hovering over the bulletin provides information about what happened so that the user does not have to sift through log messages to find it. If in a cluster, the bulletin will also indicate which node in the cluster emitted the bulletin. We can also change the log level at which bulletins will occur in the Settings tab of the Configure dialog for a Processor.

Operational details:

+ Bulletins are visible on the global bulletin board as well as on the component that emitted them.
+ The five-minute indicator is a UI convenience; the underlying bulletin stays in the component's in-memory ring buffer until newer bulletins displace it, and can be queried through the API.
+ The bulletin repository is volatile: it is held in memory (`VolatileBulletinRepository`) and does not survive a node restart. If you need retention or a history across restarts, forward bulletins to your logging/metrics stack with a reporting task such as `SiteToSiteBulletinReportingTask`.
+ Bulletins complement, but do not replace, centralized logging and metrics. Send `nifi-app.log` to your log platform and scrape metrics with a reporting task.

A flow that treats every warning as noise will hide the one bulletin that matters. Set processor log levels deliberately and alert on repeated severe bulletins.

[Table of Contents](#NiFi)

## Do the attributes get added to content (actual Data) when data is pulled by NiFi?
You can certainly add attributes to your FlowFiles at anytime, that's the whole point of separating metadata from the actual data. Essentially, one FlowFile represents an object or a message moving through NiFi. Each FlowFile contains a piece of content, which is the actual bytes. You can then extract attributes from the content, and store them in memory. You can then operate against those attributes in memory, without touching your content. By doing so you can save a lot of IO overhead, making the whole flow management process extremely efficient.

Attributes are not written into the payload. They are metadata on the FlowFile, so the content bytes are unchanged unless a processor explicitly transforms them. This is why a flow can filter, route, and correlate billions of FlowFiles while touching content only at the edges.

```json
{
  "component": {
    "name": "ExtractText",
    "type": "org.apache.nifi.processors.standard.ExtractText",
    "config": {
      "properties": {
        "order_id_regex": "\\\"order_id\\\":\\s*\\\"([^\\\"]+)\\\"",
        "order_id": "$1"
      }
    }
  }
}
```

Practical guidance:

+ Prefer record-aware `UpdateRecord`/`QueryRecord` over regex `ExtractText`; regex against large payloads is a common throughput sink.
+ Attributes are held in the JVM heap, so do not explode millions of distinct attributes or very large attribute values.
+ A `MergeContent` of many small FlowFiles plus attributes is usually cheaper than writing each one to object storage.
+ Remember that attributes are visible in provenance, so never put secrets in them.

[Table of Contents](#NiFi)

## What happens if you have stored a password in a dataflow and create a template out of it?
Password is a sensitive property. Hence, while exporting the DataFlow as a template password will be dropped. As soon as you import the template in the same or different NiFi system.

Sensitive properties are encrypted at rest with `nifi.sensitive.props.key` and are deliberately excluded from template XML exports. After import, the property is empty and the processor is invalid until an operator re-enters the secret.

```text
nifi.sensitive.props.key=<32+ character passphrase>
nifi.sensitive.props.algorithm=PBEWITHMD5AND256BITAES-CBC-OPENSSL
nifi.sensitive.props.additional.keys=
```

The modern, better answer for interviews:

+ Use **Parameter Contexts** with sensitive parameters. The flow references `#{db.password}` and the secret lives outside the versioned flow.
+ Store the flow in NiFi Registry or Git and let each environment supply its own parameter values, so promotion never carries credentials.
+ Restrict who can read parameter contexts; knowing a FlowFile's attributes or a processor's config should not reveal a secret.
+ Rotate `nifi.sensitive.props.key` carefully; changing it requires re-entering every sensitive property.
+ Never bake credentials into `ExecuteScript` literals or `InvokeHTTP` properties; they are harder to audit than a parameter.

[Table of Contents](#NiFi)

## How does NiFi support huge volume of Payload in a Dataflow?
Huge volume of data can transit from DataFlow. As data moves through NiFi, a pointer to the data is being passed around, referred to as a FlowFile. The content of the FlowFile is only accessed as needed.

Mechanisms that make large payloads and high throughput work:

+ **Content addressing**: processors receive a claim reference, so passing a 50 GB file between processors does not copy 50 GB through the JVM.
+ **Streaming processing**: `PutS3Object`, `PutHDFS`, and `MergeContent` stream from the content repository to the destination instead of buffering.
+ **Claim appending**: small FlowFiles are packed into claims, and `nifi.content.claim.max.appendable.size` controls the packing ceiling.
+ **Site-to-Site**: transfers between NiFi instances are chunked and compressed rather than sent as one blob.
+ **Split then process**: `SplitRecord` with a record count turns a huge file into bounded units that parallelize across `concurrentTasks`.

```text
nifi.content.claim.max.appendable.size=1 MB
nifi.content.repository.archive.max.usage.percentage=70%
nifi.queue.backpressure.count=100000
nifi.queue.backpressure.size=2 GB
```

```bash
# Give NiFi enough file handles and page cache on Linux for high-throughput ingestion.
sysctl -w fs.file-max=100000
ulimit -n 65536
```

Interview warning: NiFi streams well, but a processor that calls `readAllBytes()` or executes a non-streaming script breaks the model and can OOM the node. For genuinely huge analytical payloads, land them in object storage and process them with Spark rather than inside a NiFi flow.

[Table of Contents](#NiFi)

## What is a NiFi custom properties registry?
You can use to load custom key, value pair you can use custom properties registry, which can be configure as (in nifi.properties file)
nifi.variable.registry.properties=/conf/nifi_registry
And you can put key value pairs in that file and you can use that properties in you NiFi processor using expression language e.g. ${OS} , if you have configured that property in registry file.

```text
# /conf/nifi_registry
OS=linux
ENV=prod
S3_BUCKET=acme-raw-prod
```

```text
# nifi.properties
nifi.variable.registry.properties=/conf/nifi_registry
```

```text
${OS}                     -> linux
${S3_BUCKET}/orders/      -> acme-raw-prod/orders/
```

Modern replacement: **Parameter Contexts**. Instead of a global variables file, you bind a parameter context to a process group and reference parameters as `#{S3_BUCKET}`. Parameter contexts are versioned objects, can hold sensitive values, support validation, and can be inherited by child process groups.

```text
processor property: s3.bucket = #{S3_BUCKET}
parameter context "prod-orders": S3_BUCKET = acme-raw-prod (sensitive=false)
parameter context "prod-db":     DB_PASSWORD = ***** (sensitive=true)
```

Interview answer: the variable registry is the legacy global mechanism and still works for non-sensitive values; for multi-environment promotion, use parameter contexts and reference `#{param}` in processor properties.

[Table of Contents](#NiFi)

## Does NiFi works as a Master Slave architecture?
No, from NiFi 1.0 there is 0-master philosophy is considered. And each node in the NiFi cluster is the same. NiFi cluster is managed by the Zookeeper. Apache ZooKeeper elects a single node as the Cluster Coordinator, and failover is handled automatically by ZooKeeper. All cluster nodes report heartbeat and status information to the Cluster Coordinator. The Cluster Coordinator is responsible for disconnecting and connecting nodes. Additionally, every cluster has one Primary Node, also elected by ZooKeeper.

Clarify the two roles, because interviews probe them:

+ **Cluster Coordinator**: monitors node health, joins and disconnects nodes, and replicates flow configuration. It is an operational role.
+ **Primary Node**: the single node allowed to run "primary node only" processors such as `GetSFTP`, `ListS3`, or `ExecuteSQL` where exactly-once listing is required. It is a data-processing role.

```text
Cluster Coordinator (elected)      Primary Node (elected)
  - heartbeats, node lifecycle       - runs @PrimaryNodeOnly processors
  - flow config replication          - fails over to another node
  - not a data-processing supernode  - all nodes still run normal processors
```

Version nuance: NiFi 1.x uses an external ZooKeeper ensemble for coordination. Newer NiFi releases removed the requirement for an external ZooKeeper while keeping the coordinator and primary-node concepts; check the exact version in your environment before designing around ZooKeeper. In all versions, there is no master that processes all data, which is why horizontal scaling works and why any node can serve as coordinator or primary after failover.

[Table of Contents](#NiFi)

## How do you design a reliable NiFi flow?
A reliable NiFi flow uses back pressure, prioritizers, retry paths, failure relationships, and provenance tracking. Each processor should have clear success and failure routing. For external systems, use idempotent writes or deduplication because retries can happen.

Example flow:

```text
GetSFTP -> ValidateRecord -> PutS3
                    |
                    +-> PutFile dead-letter
```

This keeps invalid records visible instead of silently dropping them.

A production-grade design adds:

+ **Backpressure on every connection**, sized to the downstream system's true capacity.
+ **Retry with penalization** for transient failures: route to `RetryFlowFile` with a retry count and backoff instead of hammering the target.
+ **Dead-letter storage** keyed by reason, so operators can reprocess a known-bad batch.
+ **Idempotent sinks**: object keys derived from `filename` plus a content hash, and database upserts on a business key.
+ **Provenance enabled and retained** long enough for audit and replay.
+ **Parameter contexts** for environment-specific configuration, and versioned flows for promotion.
+ **Monitoring on queue depth and bulletin rate**, not only on processor errors.

```json
{
  "component": {
    "name": "RetryFlowFile",
    "type": "org.apache.nifi.processors.standard.RetryFlowFile",
    "config": {
      "properties": {
        "Maximum Retries": "5",
        "Retry Attribute": "retry_count",
        "Penalize Retry": "true",
        "Penalty Duration": "30 sec"
      },
      "autoTerminatedRelationships": ["retries_exceeded"]
    }
  }
}
```

Failure modes to name in an interview: a queue that grows without bound, a dead-letter directory nobody watches, credentials that expire and turn into a wall of bulletins, and non-idempotent sinks that duplicate rows after a retry.

[Table of Contents](#NiFi)

## What are FlowFiles and provenance in NiFi?
A FlowFile represents data moving through NiFi plus attributes that describe it. Provenance records show where FlowFiles came from, what processors touched them, and where they went. This is valuable for debugging, audits, and replay.

Example attributes:

```text
filename=orders_20261004.json
path=/landing/orders/
mime.type=application/json
```

Processors can route, transform, or enrich FlowFiles based on these attributes.

Provenance answers concrete questions: which processor modified this record, what the content looked like at that point, how long each hop took, and where a given input file ended up. It also enables replay: you can re-inject a FlowFile from a provenance event.

```json
{
  "provenance": {
    "totalCount": 2,
    "results": [
      {
        "eventType": "SEND",
        "componentName": "PutS3Object",
        "flowFileUuid": "9c1f0f7e-1b2a-1c3d-4e5f-6a7b8c9d0e1f",
        "attributes": {"filename": "orders_20261004.json", "path": "/landing/orders/"}
      }
    ]
  }
}
```

```python
import nipyapi

events = nipyapi.provenance.query(
    provenance_endpoint="nifi.internal:8443",
    query=nipyapi.provenance.ProvenanceQueryBuilder()
    .with_component("PutS3Object")
    .with_max_results(100)
    .build(),
)
print(events)
```

Cost note: provenance is powerful and heavy. Indexing every event at very high throughput grows the provenance repository quickly, so choose the retention and indexing strategy deliberately (`nifi.provenance.repository.indexed.fields`, `nifi.provenance.repository.max.storage.time`).

[Table of Contents](#NiFi)

## How do you version and promote NiFi flows as JSON?
NiFi stores a process group as a JSON document (`flow.json`), and version control wraps that document in a registry with numbered versions. Promotion means applying a known version to another environment and supplying environment parameters, not hand-copying templates.

```text
Developer -> NiFi dev -> commit version -> NiFi Registry / Git
                                              |
                     UAT NiFi <- apply version + UAT parameter context
                                              |
                    Prod NiFi <- apply version + prod parameter context
```

Export and import through the API:

```bash
# Export a process group as flow JSON
curl -k "https://nifi-dev.internal:8443/nifi-api/process-groups/${PG_ID}/download" \
  -H "Authorization: Bearer ${NIFI_TOKEN}" -o orders_ingest.json

# Import it into another environment
curl -k -X POST "https://nifi-uat.internal:8443/nifi-api/process-groups/root/process-groups" \
  -H "Authorization: Bearer ${NIFI_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @orders_ingest.json
```

```python
import nipyapi

nipyapi.config.default_host = "nifi-dev.internal:8443"

registry = nipyapi.versioning.get_registry_client("nifi-registry")
versions = nipyapi.versioning.list_flows_in_bucket(registry.id)
for flow in versions:
    print(flow.name, flow.version_count)
```

Promotion rules worth stating: never promote by exporting a template, because sensitive values and parameter bindings are lost; keep the flow version and the parameter context as separate artifacts; test in UAT with production-like volumes; and record the applied version in your change log so a rollback is a version downgrade rather than a rebuild.

[Table of Contents](#NiFi)

## How do you use Expression Language and record processing in NiFi?
Expression Language manipulates FlowFile attributes and is evaluated in processor properties with `${...}`. Record processing reads and writes structured data through RecordReader and RecordWriter controller services, so a single processor handles JSON, Avro, CSV, or Parquet without per-format code.

```text
${filename}                                  -> orders_20261004.json
${filename:substringBefore('.')}             -> orders_20261004
${now():format('yyyy-MM-dd')}                -> 2026-10-04
${amount:toNumber():ge(10000)}               -> true / false
${status:equals('cancelled')}                -> true / false
${attr:replaceNull('unknown')}               -> default that avoids nulls
${path:append('/archive')}                   -> /landing/orders/archive
```

```json
{
  "controllerServices": [
    {
      "name": "JsonTreeReader",
      "type": "org.apache.nifi.json.JsonTreeReader",
      "properties": {"schema-access-strategy": "infer-schema"}
    },
    {
      "name": "AvroRecordSetWriter",
      "type": "org.apache.nifi.avro.AvroRecordSetWriter",
      "properties": {"schema-access-strategy": "inherit-record-schema"}
    }
  ]
}
```

A record-oriented flow replaces brittle text processing:

```text
ConsumeKafka (JSON) -> ConvertRecord (JsonTreeReader -> AvroRecordSetWriter)
                    -> QueryRecord (filter amount > 0)
                    -> PartitionRecord (by order_date)
                    -> PutS3Object (partitioned Parquet)
```

Interview notes: record processing is schema-aware, so schema-registry integration keeps producers and consumers aligned; `UpdateRecord`/`QueryRecord` are usually far faster and safer than `ReplaceText`/`ExtractText`; and expression language is evaluated per FlowFile, so avoid expensive functions in tight loops.

[Table of Contents](#NiFi)

## How do you secure a NiFi deployment?
NiFi security has four layers: transport encryption, user authentication, authorization, and site-to-site trust. All four are configured, not optional, in a production deployment.

```text
nifi.security.keystore=/opt/nifi/conf/keystore.jks
nifi.security.keystoreType=JKS
nifi.security.keystorePasswd=<encrypted>
nifi.security.keyPasswd=<encrypted>
nifi.security.truststore=/opt/nifi/conf/truststore.jks
nifi.security.truststoreType=JKS
nifi.security.truststorePasswd=<encrypted>
nifi.security.user.authorizer=managed-authorizer
nifi.security.user.login.identity.provider=ldap-provider
nifi.web.https.port=8443
nifi.remote.input.secure=true
nifi.cluster.protocol.is.secure=true
```

What each layer covers:

+ **TLS**: encrypts the UI, REST API, cluster protocol, and site-to-site transport. NiFi can generate a self-signed keystore for internal clusters.
+ **Authentication**: who the user is, via LDAP, Kerberos, OpenID Connect, or client certificates.
+ **Authorization**: what the user can do, via `StandardManagedAuthorizer` with file-based or policy-based user groups and fine-grained policies (`read`, `write`, `execute` on components and parameter contexts).
+ **Site-to-site**: mutual TLS between NiFi instances, so data transfer is authenticated in both directions.
+ **Sensitive properties**: encrypted with `nifi.sensitive.props.key`; prefer parameter contexts for secrets.

Interview notes: enabling TLS after the fact is disruptive, so plan it from day one; a common production failure is broad `write` policy for convenience, which lets any operator change a live flow; and audit through provenance plus the access log rather than trusting component configuration alone.

[Table of Contents](#NiFi)

## How do you monitor NiFi and tune throughput?
Monitoring and tuning answer two questions: is the flow keeping up, and where is the bottleneck. Queue depth and backpressure are the leading indicators; CPU, heap, and disk throughput explain why.

What to monitor:

+ **Queue depth and backpressure** per connection; a queue at its threshold is a stalled pipeline, not a busy one.
+ **Processor throughput and time per FlowFile**, which localizes the slow processor.
+ **JVM heap, GC pause, and thread counts**; NiFi is heap-sensitive because attributes and queues live in memory.
+ **Repository disk usage and IOPS** for content, flowfile, and provenance repositories.
+ **Bulletin rate by severity and node**, and cluster node health.
+ **End-to-end latency** derived from provenance timestamps.

```json
{
  "component": {
    "name": "prometheus-reporting",
    "type": "org.apache.nifi.reporting.prometheus.PrometheusReportingTask",
    "properties": {
      "Metrics Reporting Strategy": "All Components",
      "Send JVM Metrics": "true",
      "Send System Metrics": "true"
    },
    "schedulingPeriod": "30 sec"
  }
}
```

```bash
bin/nifi.sh status
bin/nifi.sh diagnostics /tmp/nifi-diag.zip
tail -f logs/nifi-app.log | grep -i 'backpressure\|OutOfMemory\|bulletin'
```

Tuning levers, roughly in order of impact:

1. Increase `concurrentTasks` on I/O-bound processors, then confirm the downstream system can absorb the added parallelism.
2. Use run duration batching (for example 1-2 seconds) on high-volume processors to amortize per-invocation cost.
3. Move expensive routing into record processors rather than regex on raw content.
4. Split very large FlowFiles with `SplitRecord` and process the parts in parallel.
5. Tune JVM heap and repository directories, placing content and provenance on fast, separate disks where possible.
6. Scale horizontally by adding nodes once a single node saturates, since there is no master bottleneck.

[Table of Contents](#NiFi)

## When should you NOT use NiFi?
NiFi is a dataflow and integration tool, not a general-purpose compute engine. Be explicit about where it does not fit.

+ **Complex stateful analytics**: joins across large datasets, windowed aggregations, and graph or ML workloads belong in Spark, Flink, or a warehouse. NiFi can trigger and route them.
+ **Sub-second, very high-volume streaming**: at millions of messages per second, Kafka plus a stream processor is cheaper per event; NiFi is better for ingress, enrichment, and delivery.
+ **Heavy business logic in code**: a flow with hundreds of `ExecuteScript` processors is an unmaintainable service written in the wrong language.
+ **Scheduled batch orchestration**: dependency-aware scheduling, backfills, and SLAs are Airflow's job; NiFi's scheduler is per-processor, not a DAG scheduler for external jobs.
+ **Simple, single-step pipelines**: a cron job or a managed connector is less operational overhead than a NiFi cluster.
+ **Teams without operational capacity**: a production NiFi cluster means TLS, ZooKeeper or equivalent coordination, disk sizing, heap tuning, and upgrade management.
+ **Exactly-once semantics everywhere**: NiFi provides reliable delivery with retries, not exactly-once end to end; you still need idempotent sinks.

Interview answer: choose NiFi for protocol-diverse ingress, per-record routing and enrichment, and audit-ready delivery; hand off aggregation and heavy transformation to a compute engine downstream.

[Table of Contents](#NiFi)

## Real world use cases for NiFi

### 1. E-commerce order events into a lakehouse
Business context: an e-commerce platform must land order events into object storage within minutes and reject malformed events visibly. Volume: ~40M events/day, peak 8k events/s, ~3 KB per event.

```text
ConsumeKafka (orders.events) -> ValidateRecord (schema from Schema Registry)
      --valid--> UpdateRecord (add ingest_date, source) -> PutS3Object (Parquet, dt=)
      --invalid--> PutFile (/dead-letter/orders/{reason}/)
```

```json
{
  "component": {
    "name": "PutS3Object",
    "type": "org.apache.nifi.processors.aws.s3.PutS3Object",
    "config": {
      "properties": {
        "Bucket": "acme-raw-prod",
        "Object Key": "orders/dt=${ingest_date}/${filename}",
        "Content Type": "application/octet-stream",
        "Server Side Encryption": "AES256"
      }
    }
  }
}
```

Why this design: NiFi absorbs protocol and schema churn at the edge, routes invalid records to an inspectable dead-letter tree instead of dropping them, and writes date-partitioned Parquet that Spark and the warehouse can read directly. Backpressure protects S3 from request storms.

### 2. Fintech regulatory file ingestion
Business context: a payments firm ingests daily settlement and AML files from banks over SFTP and must prove chain of custody. Volume: ~2,000 files/day, 50 MB-5 GB each, strict audit.

```text
ListSFTP -> FetchSFTP -> ValidateRecord -> RouteOnAttribute --valid--> PutHDFS/PutS3
                                                          --invalid--> PutFile (quarantine)
Provenance retained 90 days; every file tied to a bank, batch id, and checksum
```

```text
nifi.provenance.repository.max.storage.time=90 days
nifi.provenance.repository.indexed.fields=filename,path,sourceSystem,batchId
nifi.content.repository.archive.max.usage.percentage=70%
```

Why this design: NiFi's provenance gives the audit trail regulators ask for, primary-node-only listing avoids duplicate pickup across the cluster, validation happens before data reaches the warehouse, and quarantine keeps failures reviewable rather than silently retried into the lake.

### 3. IoT telemetry normalization into Kafka
Business context: 200k devices publish MQTT with vendor-specific payloads; a platform must normalize them to one schema before consumers use them. Volume: ~600M messages/day, ~400 bytes each.

```text
ListenMQTT -> EvaluateJsonPath/UpdateRecord (vendor -> canonical schema)
           -> PublishKafka (key = device_id, partition by device)
Edge sites use MiNiFi -> Site-to-Site -> central NiFi cluster
```

```json
{
  "component": {
    "name": "PublishKafkaRecord_2_6",
    "type": "org.apache.nifi.kafka.processors.PublishKafkaRecord_2_6",
    "config": {
      "properties": {
        "bootstrap.servers": "broker-1:9092,broker-2:9092",
        "topic": "telemetry.normalized",
        "message-key-field": "device_id",
        "Delivery Guarantee": "Guarantee Replicated Delivery"
      }
    }
  }
}
```

Why this design: NiFi handles many device protocols and normalization rules centrally, MiNiFi extends the same flow model to constrained edge sites, and keying by `device_id` preserves per-device ordering for downstream stream processing. Kafka, not NiFi, carries the long-term event backbone.

### 4. Partner file drops into a multi-tenant SaaS lake
Business context: a B2B SaaS platform onboards 300 partners who upload CSV and JSON files to per-tenant SFTP directories; data must be isolated, validated, and attributed. Volume: ~15 TB/month, highly uneven per tenant.

```text
ListSFTP (primary node) -> FetchSFTP -> ExtractText (tenant from path)
                        -> ValidateRecord (tenant schema)
                        --valid--> PutS3Object (s3://acme-lake/tenant=${tenant}/...)
                        --invalid--> PutFile (/quarantine/${tenant}/)
```

```text
${path:substringAfter('/upload/'):substringBefore('/')}   -> tenant id
${filename:toLower():endsWith('.csv')}                    -> format routing
```

Why this design: tenant is extracted from the path with expression language, so no per-tenant flow is needed; isolated S3 prefixes and quarantine directories make data residency and blast radius explicit; and backpressure per connection stops one enormous tenant upload from starving the others.

### 5. Legacy database change capture to Kafka (CDC fan-out)
Business context: a retailer has five legacy databases with no usable CDC connector and needs changes streamed to the warehouse team. Volume: ~2M changed rows/day across sources.

```text
ExecuteSQL/QueryDatabaseTableRecord (incremental, primary node only)
  -> ConvertRecord (JSON -> Avro)
  -> RouteOnAttribute (insert/update/delete)
  -> PublishKafka (topic per source table)
  -> provenance + monitoring on lag and row counts
```

```json
{
  "component": {
    "name": "QueryDatabaseTableRecord",
    "type": "org.apache.nifi.processors.standard.QueryDatabaseTableRecord",
    "config": {
      "properties": {
        "Database Connection Pooling Service": "orders-dbcp",
        "Table Name": "ORDERS",
        "Maximum-value Columns": "LAST_UPDATED_AT",
        "Records Per Fetch": "10000",
        "Use Avro Logical Types": "true"
      }
    }
  }
}
```

Why this design: NiFi's incremental fetch by a maximum-value column gives a usable change feed without database-native CDC, and it can run primary-node-only for exactly-once listing semantics. Routing to per-table Kafka topics keeps downstream contracts stable, while provenance ties each row back to a fetch execution when reconciliation is needed.

[Table of Contents](#NiFi)
