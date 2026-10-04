## [Main title](../README.md)
### [Interview questions](full.md)

# AWS

AWS is the default cloud for a large share of data engineering work: S3 for durable storage, Glue and EMR for Spark, Athena and Redshift for SQL, Kinesis and MSK for streaming, and IAM, KMS, CloudTrail, and Lake Formation for security and governance. The questions below move from core services to concrete pipeline code and trade-offs.

+ [What is EC2?](#What-is-EC2)
+ [What is SnowBall?](#What-is-SnowBall)
+ [What is CloudWatch?](#What-is-CloudWatch)
+ [What is Elastic Transcoder?](#What-is-Elastic-Transcoder)
+ [What do you understand by VPC?](#What-do-you-understand-by-VPC)
+ [DNS and Load Balancer Services come under which type of Cloud Service?](#DNS-and-Load-Balancer-Services-come-under-which-type-of-Cloud-Service)
+ [What are the Storage Classes available in Amazon S3?](#What-are-the-Storage-Classes-available-in-Amazon-S3)
+ [Explain what T2 instances are?](#Explain-what-T2-instances-are)
+ [What are Key-Pairs in AWS?](#What-are-Key-Pairs-in-AWS)
+ [How many Subnets can you have per VPC?](#How-many-Subnets-can-you-have-per-VPC)
+ [List different types of Cloud Services.](#List-different-types-of-Cloud-Services)
+ [Explain what S3 is?](#Explain-what-S3-is)
+ [How does Amazon Route 53 provide high availability and low latency?](#How-does-Amazon-Route-53-provide-high-availability-and-low-latency)
+ [How can you send a request to Amazon S3?](#How-can-you-send-a-request-to-Amazon-S3)
+ [What does AMI include?](#What-does-AMI-include)
+ [What are the different types of Instances?](#What-are-the-different-types-of-Instances)
+ [What is the relation between the Availability Zone and Region?](#What-is-the-relation-between-the-Availability-Zone-and-Region)
+ [How do you monitor Amazon VPC?](#How-do-you-monitor-Amazon-VPC)
+ [What are the different types of EC2 instances based on their costs?](#What-are-the-different-types-of-EC2-instances-based-on-their-costs)
+ [What do you understand by stopping and terminating an EC2 Instance?](#What-do-you-understand-by-stopping-and-terminating-an-EC2-Instance)
+ [What are the consistency models for modern DBs offered by AWS?](#What-are-the-consistency-models-for-modern-DBs-offered-by-AWS)
+ [What is Geo-Targeting in CloudFront?](#What-is-Geo-Targeting-in-CloudFront)
+ [What are the advantages of AWS IAM?](#What-are-the-advantages-of-AWS-IAM)
+ [What do you understand by a Security Group?](#What-do-you-understand-by-a-Security-Group)
+ [What are Spot Instances and On-Demand Instances?](#What-are-Spot-Instances-and-On-Demand-Instances)
+ [Explain Connection Draining.](#Explain-Connection-Draining)
+ [What is a Stateful and a Stateless Firewall?](#What-is-a-Stateful-and-a-Stateless-Firewall)
+ [What is a Power User Access in AWS?](#What-is-a-Power-User-Access-in-AWS)
+ [What is an Instance Store Volume and an EBS Volume?](#What-is-an-Instance-Store-Volume-and-an-EBS-Volume)
+ [What are Recovery Time Objective and Recovery Point Objective in AWS?](#What-are-Recovery-Time-Objective-and-Recovery-Point-Objective-in-AWS)
+ [Is there a way to upload a file that is greater than 100 Megabytes in Amazon S3?](#Is-there-a-way-to-upload-a-file-that-is-greater-than-100-Megabytes-in-Amazon-S3)
+ [Can you change the Private IP Address of an EC2 instance while it is running or in a stopped state?](#Can-you-change-the-Private-IP-Address-of-an-EC2-instance-while-it-is-running-or-in-a-stopped-state)
+ [What is the use of lifecycle hooks is Autoscaling?](#What-is-the-use-of-lifecycle-hooks-is-Autoscaling)
+ [What are the policies that you can set for your user's passwords?](#What-are-the-policies-that-you-can-set-for-your-users-passwords)
+ [What do you know about the Amazon Database?](#What-do-you-know-about-the-Amazon-Database)
+ [Explain Amazon Relational Database?](#Explain-Amazon-Relational-Database)
+ [What are the Features of Amazon Database?](#What-are-the-Features-of-Amazon-Database)
+ [Which of the Aws Db Service is a Nosql Database and Serverless and Delivers Consistent singledigit Millisecond Latency at any scale?](#Which-of-the-Aws-Db-Service-is-a-Nosql-Database-and-Serverless-and-Delivers-Consistent-singledigit-Millisecond-Latency-at-any-scale)
+ [What is  Key Value Store?](#What-is-Key-Value-Store)
+ [What is Dynamodb?](#What-is-Dynamodb)
+ [List of the benefits of using Amazon Dynamodb?](#List-of-the-benefits-of-using-Amazon-Dynamodb)
+ [What is a Dynamodbmapper Class?](#What-is-a-Dynamodbmapper-Class)
+ [What are the Data Types supported by Dynamodb?](#What-are-the-Data-Types-supported-by-Dynamodb)
+ [What do you understand by Dynamodb Auto Scaling?](#What-do-you-understand-by-Dynamodb-Auto-Scaling)
+ [What is a Data Warehouse and how Aws Redshift can play a vital role in the Storage?](#What-is-a-Data-Warehouse-and-how-Aws-Redshift-can-play-a-vital-role-in-the-Storage)
+ [What is Amazon Redshift and why is it popular among other Cloud Data Warehouses?](#What-is-Amazon-Redshift-and-why-is-it-popular-among-other-Cloud-Data-Warehouses)
+ [What is Redshift Spectrum?](#What-is-Redshift-Spectrum)
+ [What is a Leader Node and Compute Node?](#What-is-a-Leader-Node-and-Compute-Node)
+ [How to load data iIn Amazon Redshift?](#How-to-load-data-iIn-Amazon-Redshift)
+ [Mention the database engines which are supported by Amazon Rds?](#Mention-the-database-engines-which-are-supported-by-Amazon-Rds)
+ [What is the work of Amazon Rds?](#What-is-the-work-of-Amazon-Rds)
+ [What is the purpose of standby Rds Instance?](#What-is-the-purpose-of-standby-Rds-Instance)
+ [Are Rds instances upgradable or down gradable according to the Need?](#Are-Rds-instances-upgradable-or-down-gradable-according-to-the-Need)
+ [What is Amazon Elastic Ache?](#What-is-Amazon-Elastic-Ache)
+ [What is the use of Amazon Elastic Ache?](#What-is-the-use-of-Amazon-Elastic-Ache)
+ [What are the Benefits of Amazon Elastic Ache?](#What-are-the-Benefits-of-Amazon-Elastic-Ache)
+ [Explain the Types of Engines in Elastic Ache?](#Explain-the-Types-of-Engines-in-Elastic-Ache)
+ [Is it possible to run Multiple Db Instances for free for Amazon Rds?](#Is-it-possible-to-run-Multiple-Db-Instances-for-free-for-Amazon-Rds)
+ [Which Aws Services will you choose for collecting and processing Ecommerce Data for Realtime Analysis?](#Which-Aws-Services-will-you-choose-for-collecting-and-processing-Ecommerce-Data-for-Realtime-Analysis)
+ [What will happen to the Db Snapshots and Backups if any user deletes Db Instance?](#What-will-happen-to-the-Db-Snapshots-and-Backups-if-any-user-deletes-Db-Instance)
+ [How would you design a basic AWS data lake?](#How-would-you-design-a-basic-AWS-data-lake)
+ [When would you use AWS Glue, EMR, Lambda, or ECS for data processing?](#When-would-you-use-AWS-Glue-EMR-Lambda-or-ECS-for-data-processing)
+ [How do Kinesis, MSK, SQS, and EventBridge differ for data pipelines?](#How-do-Kinesis-MSK-SQS-and-EventBridge-differ-for-data-pipelines)
+ [How do you load and optimize data in Amazon Redshift?](#How-do-you-load-and-optimize-data-in-Amazon-Redshift)
+ [How do you secure data engineering workloads on AWS?](#How-do-you-secure-data-engineering-workloads-on-AWS)
+ [How do you control cost in AWS data pipelines?](#How-do-you-control-cost-in-AWS-data-pipelines)
+ [How do you use the AWS CLI and boto3 with S3?](#How-do-you-use-the-AWS-CLI-and-boto3-with-S3)
+ [How do you write an AWS Glue PySpark job?](#How-do-you-write-an-AWS-Glue-PySpark-job)
+ [How do you query S3 with Athena and partition projection?](#How-do-you-query-S3-with-Athena-and-partition-projection)
+ [How do you load and unload data in Amazon Redshift with COPY and UNLOAD?](#How-do-you-load-and-unload-data-in-Amazon-Redshift-with-COPY-and-UNLOAD)
+ [How do you write least-privilege IAM policies for data pipelines?](#How-do-you-write-least-privilege-IAM-policies-for-data-pipelines)
+ [How do you orchestrate pipelines with Step Functions and EventBridge?](#How-do-you-orchestrate-pipelines-with-Step-Functions-and-EventBridge)
+ [How do you ingest streaming data with Amazon Kinesis?](#How-do-you-ingest-streaming-data-with-Amazon-Kinesis)
+ [How do you govern a data lake with AWS Lake Formation?](#How-do-you-govern-a-data-lake-with-AWS-Lake-Formation)
+ [How do you choose between AWS data services? Trade-offs and when not to use them](#How-do-you-choose-between-AWS-data-services-Trade-offs-and-when-not-to-use-them)
+ [Real world use cases for AWS](#Real-world-use-cases-for-AWS)

## What is EC2?
EC2 is a virtual machine in the cloud with OS-level control. You use it when you need your own servers, full control over hardware, and the ability to install arbitrary software. In data engineering, EC2 is mostly the substrate for self-managed engines (Spark, Kafka, Airflow) or the nodes behind EMR and ECS. Pick families by workload: `r` for Spark drivers and cached joins, `c` for Kafka brokers, `i`/`d` for shuffle and scratch storage.

[Table of Contents](#AWS)

## What is SnowBall?
Snowball is a physical device that transfers terabytes to petabytes into and out of AWS. You copy data on-premises, ship it, and AWS imports it to S3; Snowball Edge adds edge compute. Use it when a network transfer would take weeks. For ongoing transfers prefer AWS DataSync or S3 Transfer Acceleration.

[Table of Contents](#AWS)

## What is CloudWatch?
CloudWatch monitors AWS resources, stores logs and custom metrics, and triggers alarms on thresholds. For pipelines the useful pieces are one log group per job, metric filters for row counts or failures, and alarms routed to SNS or a paging tool.

```bash
aws cloudwatch put-metric-alarm --alarm-name glue-orders-failed \
  --metric-name glue.driver.aggregate.numFailedTasks --namespace Glue \
  --statistic Sum --period 300 --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:data-oncall \
  --dimensions Name=JobName,Value=orders_curated
```

[Table of Contents](#AWS)

## What is Elastic Transcoder?
Elastic Transcoder changes a video's format and resolution for different devices. It is largely superseded by AWS Elemental MediaConvert for new workloads; it appears in interviews to test whether you can distinguish a legacy service from its modern replacement.

[Table of Contents](#AWS)

## What do you understand by VPC?
A VPC (Virtual Private Cloud) is a logically isolated network where you control the IP range, subnets, route tables, gateways, and security groups. Data platforms use private subnets for EMR/Glue/RDS, VPC gateway endpoints for S3 and DynamoDB so traffic never leaves the AWS network, and interface endpoints for KMS and Secrets Manager.

[Table of Contents](#AWS)

## DNS and Load Balancer Services come under which type of Cloud Service?
Route 53 (DNS) and ELB/ALB/NLB (load balancing) are IaaS: infrastructure primitives you configure rather than a managed application platform.

[Table of Contents](#AWS)

## What are the Storage Classes available in Amazon S3?
Common classes: S3 Standard (hot data), Intelligent-Tiering (unknown access patterns), Standard-IA and One Zone-IA (infrequent access), Glacier Instant Retrieval, Glacier Flexible Retrieval, and Glacier Deep Archive (archives), plus S3 Express One Zone for latency-sensitive analytics. Use lifecycle rules to transition objects automatically, for example `STANDARD_IA` at 30 days and `GLACIER_IR` at 90 days for a `raw/` prefix.

Watch the IA/Glacier minimum billable duration and per-object overhead: these classes are a poor fit for millions of tiny files.

[Table of Contents](#AWS)

## Explain what T2 instances are?
T2 instances are burstable general-purpose instances with a moderate CPU baseline and the ability to burst using credits. T2 has largely been replaced by T3 and Graviton-based T4g, but the lesson still holds: a long-running Spark or Kafka workload that exhausts burst credits is silently throttled.

[Table of Contents](#AWS)

## What are Key-Pairs in AWS?
Key-Pairs are the public/private key pairs used to log into EC2 instances. Better practice on modern platforms is AWS Systems Manager Session Manager, which needs no inbound port and logs sessions for audit.

[Table of Contents](#AWS)

## How many Subnets can you have per VPC?
200 subnets per VPC by default, and it is a soft quota you can raise. A VPC defaults to a /16 CIDR and each subnet lives in exactly one Availability Zone.

[Table of Contents](#AWS)

## List different types of Cloud Services.
+ Software as a Service (SaaS)
+ Data as a Service (DaaS)
+ Platform as a Service (PaaS)
+ Infrastructure as a Service (IaaS)

[Table of Contents](#AWS)

## Explain what S3 is?
S3 (Simple Storage Service) stores and retrieves any amount of data via a REST API with pay-as-you-go pricing for storage, requests, and transfer. Since December 2020 S3 provides strong read-after-write consistency for all operations, which is what makes it safe as a lakehouse storage layer.

```python
import boto3

s3 = boto3.client("s3")
s3.put_object(Bucket="acme-raw", Key="orders/ds=2026-10-04/orders.json",
              Body=b'{"order_id": 1001, "amount": 42.50}\n',
              ServerSideEncryption="aws:kms")
print(s3.get_object(Bucket="acme-raw", Key="orders/ds=2026-10-04/orders.json")["Body"].read())
```

[Table of Contents](#AWS)

## How does Amazon Route 53 provide high availability and low latency?
Route 53 answers DNS queries from a globally distributed anycast network near the user. Routing policies - latency, geolocation, weighted, and failover - let you steer traffic to healthy endpoints, and health checks trigger automatic failover to a standby record.

[Table of Contents](#AWS)

## How can you send a request to Amazon S3?
S3 is a REST service; you can call the REST API directly, use the AWS CLI, or use an SDK wrapper. A common pattern for private objects is a presigned URL: `aws s3 presign s3://acme-raw/orders/ds=2026-10-04/orders.json --expires-in 3600`.

[Table of Contents](#AWS)

## What does AMI include?
An AMI includes a template for the root volume, launch permissions deciding which accounts can use it, and a block device mapping for attached volumes. Golden AMIs are useful for pinning an exact Spark/Python dependency set across a fleet of EC2 or EMR nodes.

[Table of Contents](#AWS)

## What are the different types of Instances?
General purpose (`t`, `m`), compute optimized (`c`), memory optimized (`r`, `x`, `z`), storage optimized (`i`, `d`, `h`), and accelerated computing (`p`, `g`, `inf`, `trn`). Choose by the dominant resource: cache and driver memory for Spark, local NVMe for shuffle, GPU for ML.

[Table of Contents](#AWS)

## What is the relation between the Availability Zone and Region?
An Availability Zone is one or more discrete data centers with independent power, cooling, and networking inside a Region. A Region is a geographic collection of AZs. Place stateful services such as RDS and MSK across multiple AZs, and keep S3, Glue, Athena, and Redshift in one Region to avoid cross-Region transfer cost.

[Table of Contents](#AWS)

## How do you monitor Amazon VPC?
+ CloudWatch - metrics and alarms for NAT gateways, VPN, and flow-log-derived metrics.
+ VPC Flow Logs - accepted/rejected traffic per ENI, delivered to CloudWatch Logs or S3.
+ CloudTrail - API-level audit of VPC and security group changes.
+ Reachability Analyzer - static path analysis for misconfigured routes or security groups.

[Table of Contents](#AWS)

## What are the different types of EC2 instances based on their costs?
On-Demand (pay by the second, flexible), Spot (spare capacity at a large discount but reclaimable with a two-minute warning), and Reserved Instances/Savings Plans (one- or three-year commitment for a discount). Run stateless Spark executors and EMR task nodes on Spot; keep drivers and stateful services on On-Demand or Reserved capacity.

[Table of Contents](#AWS)

## What do you understand by stopping and terminating an EC2 Instance?
Stopping shuts an instance down but keeps its EBS volumes and allows a restart. Terminating deletes the instance permanently; by default the root EBS volume is deleted too, and instance-store data is lost on both stop and terminate.

[Table of Contents](#AWS)

## What are the consistency models for modern DBs offered by AWS?
+ Eventual consistency - reads may briefly return stale data but the system converges; still relevant for DynamoDB eventually consistent reads and many GSIs.
+ Strong consistency - reads always reflect the latest committed write; DynamoDB offers strongly consistent reads on tables and local secondary indexes.

Important correction: the old "S3 is eventually consistent" answer is outdated. S3 has been strongly consistent for all operations since December 2020.

[Table of Contents](#AWS)

## What is Geo-Targeting in CloudFront?
Geo-targeting serves content based on the user's geographic location so it is more relevant. CloudFront implements it with geo restriction (allow/block by country) and by passing the `CloudFront-Viewer-Country` header to the origin or a Lambda@Edge function.

[Table of Contents](#AWS)

## What are the advantages of AWS IAM?
IAM grants granular access to users, groups, and roles, and supports federated access (SAML, OIDC, IAM Identity Center) without creating users. For data platforms, prefer roles over access keys, scope to specific buckets and prefixes, and add conditions such as `aws:SourceArn` and required encryption headers.

```json
{"Version":"2012-10-17","Statement":[{"Sid":"ReadRawOrders","Effect":"Allow",
 "Action":["s3:GetObject","s3:ListBucket"],
 "Resource":["arn:aws:s3:::acme-raw","arn:aws:s3:::acme-raw/orders/*"]}]}
```

[Table of Contents](#AWS)

## What do you understand by a Security Group?
Security groups are a stateful, allow-list virtual firewall attached to instances and ENIs. You define rules by port, protocol, and source/destination, and a source can be another security group, which keeps rules stable as IPs change. There are no deny rules in a security group.

[Table of Contents](#AWS)

## What are Spot Instances and On-Demand Instances?
Spot instances use AWS's spare EC2 capacity at a discount and can be interrupted, so they suit flexible, fault-tolerant work. On-Demand instances have a static price and stay available until you terminate them, so they suit steady-state or interruption-sensitive work.

[Table of Contents](#AWS)

## Explain Connection Draining.
Connection draining lets an instance being removed or updated finish in-flight requests while the load balancer stops sending it new ones. Modern ALBs and NLBs call this the deregistration delay (`deregistration_delay.timeout_seconds`).

[Table of Contents](#AWS)

## What is a Stateful and a Stateless Firewall?
A stateful firewall tracks connection state, so you define only inbound rules and return traffic is allowed automatically. A stateless firewall requires explicit inbound and outbound rules. In AWS, security groups are stateful and network ACLs are stateless.

[Table of Contents](#AWS)

## What is a Power User Access in AWS?
An administrator can create, modify, or delete resources and also manage users and permissions. Power User Access (`arn:aws:iam::aws:policy/PowerUserAccess`) grants everything except IAM user and permission management. Least privilege still beats both: give each pipeline its own scoped role.

[Table of Contents](#AWS)

## What is an Instance Store Volume and an EBS Volume?
Instance store is temporary, physically attached storage whose data is lost on stop, terminate, or host failure. EBS is persistent network-attached storage that survives stops and terminates. Spark on EMR typically uses instance store NVMe for shuffle scratch and EBS for anything that must persist.

[Table of Contents](#AWS)

## What are Recovery Time Objective and Recovery Point Objective in AWS?
+ RTO - the maximum acceptable downtime between interruption and restoration.
+ RPO - the maximum acceptable data loss measured from the last recovery point.

Mapped to services: Multi-AZ RDS gives low RTO with near-zero RPO; cross-Region S3 replication and AWS Backup survive a Region failure at a larger RPO; nightly snapshots accept up to 24 hours of loss.

[Table of Contents](#AWS)

## Is there a way to upload a file that is greater than 100 Megabytes in Amazon S3?
Yes, with multipart upload: the object is split into parts uploaded independently and in parallel, then merged. The CLI and SDKs do this automatically above a threshold. Limits: a single PUT is capped at 5 GiB, a part is 5 MiB to 5 GiB, and an object is up to 5 TiB.

```python
import boto3
from boto3.s3.transfer import TransferConfig

config = TransferConfig(multipart_threshold=64 * 1024 * 1024, max_concurrency=16)
boto3.client("s3").upload_file("bigfile.parquet", "acme-raw", "bigfile.parquet", Config=config)
```

[Table of Contents](#AWS)

## Can you change the Private IP Address of an EC2 instance while it is running or in a stopped state?
The primary private IPv4 is assigned to the primary ENI at launch and cannot be changed in place on a running instance. You can, however, add secondary private IPv4 addresses to a running instance, and you can move or replace the network interface to change the address.

[Table of Contents](#AWS)

## What is the use of lifecycle hooks is Autoscaling?
Lifecycle hooks pause a scale-out or scale-in event so custom actions run before the instance is fully in or out of service. On scale-out you bootstrap configuration; on scale-in you drain work, checkpoint, or upload logs before termination.

[Table of Contents](#AWS)

## What are the policies that you can set for your user's passwords?
The account password policy controls minimum length and complexity, password reuse, maximum age, whether users can self-change passwords, and the administrator contact for resets. Set it with `aws iam update-account-password-policy --minimum-password-length 14 --require-symbols --require-numbers --password-reuse-prevention 24`.

[Table of Contents](#AWS)

## What do you know about the Amazon Database?
AWS offers managed relational (RDS, Aurora), NoSQL key-value/document (DynamoDB), warehouse (Redshift), and in-memory (ElastiCache, MemoryDB) databases. Choose by access pattern, scale, consistency, and query flexibility - not by brand loyalty.

[Table of Contents](#AWS)

## Explain Amazon Relational Database?
Amazon RDS operates, scales, and manages relational databases and automates provisioning, patching, backups, and recovery. Supported engines are MySQL, Oracle, PostgreSQL, SQL Server, MariaDB, and Amazon Aurora. Use Multi-AZ for availability and read replicas for read scaling.

[Table of Contents](#AWS)

## What are the Features of Amazon Database?
Easy to administer, highly scalable, durable and reliable, fast, highly available with automated failover, secure with encryption and IAM integration, and cost-effective when matched to the workload.

[Table of Contents](#AWS)

## Which of the Aws Db Service is a Nosql Database and Serverless and Delivers Consistent singledigit Millisecond Latency at any scale?
Amazon DynamoDB - fully managed and serverless, with on-demand capacity and consistent single-digit millisecond latency.

[Table of Contents](#AWS)

## What is  Key Value Store?
A key-value store saves and retrieves objects identified by a key, storing the content as a value and looking items up by key rather than by joins. DynamoDB is a key-value/document store; Redis and Memcached are in-memory key-value stores.

[Table of Contents](#AWS)

## What is Dynamodb?
DynamoDB is a fully managed NoSQL database with fast, predictable performance at scale. It removes configuration, provisioning, replication, patching, and cluster scaling, so teams offload the operation of distributed databases to AWS.

[Table of Contents](#AWS)

## List of the benefits of using Amazon Dynamodb?
Fully managed with no servers to patch; consistent single-digit millisecond latency; highly scalable, available, and durable with global tables; very high throughput at low latency via on-demand or provisioned capacity; flexible schema; and streams for change data capture.

[Table of Contents](#AWS)

## What is a Dynamodbmapper Class?
The mapper is a client-side abstraction mapping objects to items. In Java it is `DynamoDBMapper`, which handles `put`, `get`, `query`, and `scan` without hand-writing attribute mappings; Python teams use the `boto3` resource API or PynamoDB instead.

[Table of Contents](#AWS)

## What are the Data Types supported by Dynamodb?
Scalar (string, number, binary, boolean, null), document (list, map), and sets (string, number, binary). Each item is limited to 400 KB, so large payloads belong in S3 with the key stored in DynamoDB.

[Table of Contents](#AWS)

##  What do you understand by Dynamodb Auto Scaling?
Auto scaling adjusts provisioned read and write capacity, and GSI capacity, up and down against a target utilization. On-demand mode removes capacity planning entirely and is the simpler default for spiky workloads.

[Table of Contents](#AWS)

## What is a Data Warehouse and how Aws Redshift can play a vital role in the Storage?
A data warehouse collects, models, and stores data from operational systems for analytics. The classic three tiers are data collection/cleansing, transformation and OLAP modeling, and front-end analysis and mining. On-premises warehouses are expensive because storage must be upgraded as data grows; Redshift provides managed warehouse compute and storage in the cloud instead.

[Table of Contents](#AWS)

## What is Amazon Redshift and why is it popular among other Cloud Data Warehouses?
Redshift is a fast, scalable, cost-effective cloud data warehouse for gigabytes to hundreds of petabytes. It is popular because it is easy to create and operate, scales by resizing or adding nodes, uses columnar storage and massively parallel processing for fast analytics, costs a fraction of traditional warehouses, and integrates with S3, the Glue Data Catalog, and Spectrum.

[Table of Contents](#AWS)

## What is Redshift Spectrum?
Spectrum runs SQL against exabytes in S3 without loading it, using external tables usually defined in the Glue Data Catalog and scaling across many nodes for parallel scan and filter.

```sql
CREATE EXTERNAL SCHEMA spectrum_raw FROM DATA CATALOG DATABASE 'raw'
IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-spectrum';
SELECT event_type, count(*) FROM spectrum_raw.events
WHERE event_ts >= '2026-10-01' GROUP BY 1 ORDER BY 2 DESC;
```

[Table of Contents](#AWS)

## What is a Leader Node and Compute Node?
The leader node receives client queries, parses them, builds the execution plan, coordinates steps, and returns results. Compute nodes execute the assigned steps and return data to the leader. On RA3 clusters, compute is separate from managed storage and concurrency scaling adds transient clusters for read bursts.

[Table of Contents](#AWS)

## How to load data iIn Amazon Redshift?
Use `COPY` from S3 for bulk loads (Parquet, ORC, CSV, JSON), Glue or EMR to prepare those files, Spectrum for query-in-place, the Data API or JDBC/ODBC for small writes, and Firehose or zero-ETL integrations for streaming. Avoid row-by-row `INSERT` for bulk data.

[Table of Contents](#AWS)

## Mention the database engines which are supported by Amazon Rds?
Amazon Aurora, MySQL, MariaDB, Oracle, SQL Server, and PostgreSQL.

[Table of Contents](#AWS)

## What is the work of Amazon Rds?
RDS provisions the requested infrastructure, installs the database engine, and automates patching, backups, and synchronous replication with automatic failover. You own schemas and queries; AWS owns the host, storage, and engine lifecycle.

[Table of Contents](#AWS)

## What is the purpose of standby Rds Instance?
The standby in a Multi-AZ deployment protects against infrastructure failure in a different Availability Zone and is promoted automatically if the primary fails. It does not serve reads; use read replicas for read scaling.

[Table of Contents](#AWS)

## Are Rds instances upgradable or down gradable according to the Need?
Yes. Change instance class, storage, or engine version with `aws rds modify-db-instance --db-instance-identifier orders-db --db-instance-class db.r6g.2xlarge --apply-immediately`. If unsure of CPU needs, start small and watch CloudWatch before committing.

[Table of Contents](#AWS)

## What is Amazon Elastic Ache?
Amazon ElastiCache is a fully managed in-memory key-value store supporting Valkey/Redis and Memcached. It is a zero-administration service used to build high-performance applications or accelerate existing ones in gaming, healthcare, and similar domains.

[Table of Contents](#AWS)

## What is the use of Amazon Elastic Ache?
Caching frequently reused data in memory serves it very fast without managing a separate caching server. ElastiCache provides a high-throughput, low-latency, open-source-compatible cache with replication and automatic failover.

[Table of Contents](#AWS)

## What are the Benefits of Amazon Elastic Ache?
Automatic detection and recovery of cache node failures, integration with other AWS services, offloaded setup and monitoring, very low response times, and easy scale up or down including serverless.

[Table of Contents](#AWS)

## Explain the Types of Engines in Elastic Ache?
+ Memcached - a simple multi-threaded in-memory object cache; sub-millisecond reads, key-value only, keys/values up to about 1 MB.
+ Redis/Valkey - rich data structures (strings, hashes, lists, sets, sorted sets, streams), persistence and backup/restore, replication, and pub/sub, with values up to 512 MB. Preferred for real-time applications needing sub-millisecond latency.

[Table of Contents](#AWS)

## Is it possible to run Multiple Db Instances for free for Amazon Rds?
Yes, but free-tier hours are pooled. If total usage across RDS Single-AZ micro instances exceeds 750 instance hours in a month, the excess is billed at standard pricing. Two instances at 400 hours each total 800 hours, so 50 hours are billed.

[Table of Contents](#AWS)

## Which Aws Services will you choose for collecting and processing Ecommerce Data for Realtime Analysis?
Use an architecture rather than one service: API Gateway or Kinesis ingests events, Lambda enriches them, Firehose lands them in S3, DynamoDB holds low-latency order state, and Redshift or Athena serves analytics. Kinesis gives ordered, replayable ingestion; Firehose gives cheap micro-batch delivery to S3; DynamoDB absorbs high-volume key lookups.

[Table of Contents](#AWS)

## What will happen to the Db Snapshots and Backups if any user deletes Db Instance?
On deletion RDS offers a final snapshot, which you can restore later, and keeps it alongside your manual snapshots. Automated backups are deleted with the instance; manually created snapshots are preserved.

[Table of Contents](#AWS)

## How would you design a basic AWS data lake?
A common lake uses S3 for durable storage, the Glue Data Catalog for metadata, Glue/EMR/Spark for processing, and Athena, Redshift Spectrum, or Redshift for analytics, with raw, curated, and analytics layers.

```text
s3://acme-lake/raw/orders/ds=2026-10-04/          # immutable, as landed
s3://acme-lake/curated/orders/ds=2026-10-04/      # typed, deduplicated Parquet
s3://acme-lake/analytics/fact_orders/ds=2026-10-04/
```

Governance matters as much as storage: bucket policies, IAM roles, KMS encryption, Lake Formation permissions, lifecycle rules, and CloudTrail. A lake needs metadata, access control, data quality, and cost management - not just files.

[Table of Contents](#AWS)

## When would you use AWS Glue, EMR, Lambda, or ECS for data processing?
Use Glue for managed, catalog-integrated Spark/Python ETL at moderate scale. Use EMR for large, shuffle-heavy, or custom Spark/Hadoop workloads and Spot-heavy batch. Use Lambda for small event-driven tasks under 15 minutes. Use ECS/Fargate for containerized jobs that need more runtime control than Lambda but no Spark. The choice is driven by data size, runtime, dependency complexity, and how much cluster operations you want to own.

[Table of Contents](#AWS)

## How do Kinesis, MSK, SQS, and EventBridge differ for data pipelines?
Kinesis Data Streams is ordered, shard-based streaming with replay within retention. MSK is managed Kafka for teams already on Kafka APIs and tooling. SQS is a decoupling queue for message-at-a-time work, not analytics streams. EventBridge routes events and schedules. Compare ordering, replay, retention, throughput, consumer model, and operational cost: MSK is more powerful but you own brokers; Kinesis is simpler but quotas shape the design.

[Table of Contents](#AWS)

## How do you load and optimize data in Amazon Redshift?
Stage files in S3 and use `COPY` rather than inserts, prefer Parquet, compressed and sized so slices work in parallel. Design distribution and sort keys around common joins and time filters, and use `EXPLAIN` and system tables to find skew and full scans.

```sql
COPY fact_orders FROM 's3://acme-curated/orders/'
IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-load-role'
FORMAT AS PARQUET STATUPDATE ON;
ALTER TABLE fact_orders ALTER DISTSTYLE KEY DISTKEY (customer_id);
ALTER TABLE fact_orders ALTER SORTKEY (order_ts);
```

RA3 managed storage, automatic table optimization, materialized views, and concurrency scaling help, but bad file layout and inefficient joins still dominate cost.

[Table of Contents](#AWS)

## How do you secure data engineering workloads on AWS?
Use least-privilege IAM roles instead of access keys, KMS encryption at rest and TLS in transit, private subnets, security groups, and VPC endpoints, plus CloudTrail and service logs for audit. Block public S3 access. Build security into the design with one role per job, separate raw and curated permissions, no shared admin roles, and ownership tags.

[Table of Contents](#AWS)

## How do you control cost in AWS data pipelines?
Reduce scanned data, choose the right compute, use lifecycle policies, right-size jobs, and shut down idle resources. Convert CSV/JSON to compressed Parquet, partition by common filters, expire staging data with S3 lifecycle rules, use Spot for fault-tolerant EMR, enable managed/auto scaling, and add cost allocation tags with Budgets alarms. Inefficient layout and unbounded scans usually cost more than an expensive instance.

[Table of Contents](#AWS)

## How do you use the AWS CLI and boto3 with S3?
The CLI suits operators and CI; boto3 is what runs inside Python jobs and Lambda. Always paginate listings and let the SDK handle multipart and retries.

```bash
aws s3 ls s3://acme-raw/orders/ --recursive --human-readable --summarize
aws s3 cp orders.parquet s3://acme-raw/orders/ds=2026-10-04/ --sse aws:kms
aws s3 sync ./staging/ s3://acme-curated/orders/ --exclude "*" --include "*.parquet"
```

```python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")


def list_parquet(bucket: str, prefix: str) -> list[str]:
    paginator = s3.get_paginator("list_objects_v2")
    keys: list[str] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    return keys


def upload(bucket: str, key: str, path: str) -> None:
    try:
        s3.upload_file(path, bucket, key, ExtraArgs={"ServerSideEncryption": "aws:kms"})
    except ClientError as exc:
        raise RuntimeError(f"upload failed for {key}") from exc
```

Interview points: never assume one page of `list_objects_v2`, use `upload_file`/`download_file` for automatic multipart, and rely on IAM roles or SSO profiles instead of hard-coded credentials.

[Table of Contents](#AWS)

## How do you write an AWS Glue PySpark job?
A Glue job is managed Spark. Read job parameters with `getResolvedOptions`, use `GlueContext` for catalog-aware IO, transform with Spark DataFrames, and write partitioned Parquet; call `job.commit()` to advance job bookmarks.

```python
import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME", "raw_path", "curated_path"])
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

curated = (
    spark.read.json(args["raw_path"])
    .withColumn("order_ts", F.to_timestamp("order_ts"))
    .withColumn("amount", F.col("amount").cast("decimal(12,2)"))
    .withColumn("ds", F.to_date("order_ts"))
    .filter(F.col("order_id").isNotNull())
    .dropDuplicates(["order_id"])
)
curated.write.mode("overwrite").partitionBy("ds").parquet(args["curated_path"])
job.commit()
```

Operational notes: enable job metrics and continuous logging, set worker type/size and a timeout, and consider `--enable-auto-scaling`. For very large shuffle-heavy jobs, EMR with Spot task nodes is often cheaper.

[Table of Contents](#AWS)

## How do you query S3 with Athena and partition projection?
Athena is serverless SQL over S3 and the Glue Data Catalog. Partition projection computes partition locations from the table definition, so you avoid `MSCK REPAIR TABLE` and crawler cost across tens of thousands of partitions.

```sql
CREATE EXTERNAL TABLE curated.orders (
  order_id bigint, customer_id bigint, order_ts timestamp, amount decimal(12,2)
)
PARTITIONED BY (ds string) STORED AS PARQUET
LOCATION 's3://acme-curated/orders/'
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.ds.type' = 'date',
  'projection.ds.range' = '2024-01-01,NOW',
  'projection.ds.format' = 'yyyy-MM-dd',
  'projection.ds.interval' = '1',
  'projection.ds.interval.unit' = 'DAYS',
  'storage.location.template' = 's3://acme-curated/orders/ds=${ds}/'
);

SELECT ds, count(*) AS orders, sum(amount) AS revenue
FROM curated.orders
WHERE ds BETWEEN '2026-09-01' AND '2026-10-04'
GROUP BY ds ORDER BY ds;
```

Athena bills by bytes scanned, so partition pruning, Parquet/ORC, compression, and selecting only needed columns matter more than engine size. Avoid `SELECT *` and wide raw-JSON scans, and set a per-query bytes-scanned cutoff in the workgroup.

[Table of Contents](#AWS)

## How do you load and unload data in Amazon Redshift with COPY and UNLOAD?
`COPY` is the parallel load path and `UNLOAD` the parallel export path; both use an IAM role and can write Parquet. Avoid single-file loads because they serialize on one slice.

```sql
COPY fact_orders FROM 's3://acme-curated/orders/'
IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-load-role'
FORMAT AS PARQUET STATUPDATE ON;

UNLOAD ('SELECT * FROM fact_orders WHERE order_ts >= ''2026-10-01''')
TO 's3://acme-analytics/exports/fact_orders/'
IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-unload-role'
FORMAT AS PARQUET PARTITION BY (ds) ALLOWOVERWRITE PARALLEL ON;
```

Use a manifest for a controlled file list, stage via S3 even from databases (UNLOAD or CDC), and tune `COMPUPDATE`/`STATUPDATE`.

[Table of Contents](#AWS)

## How do you write least-privilege IAM policies for data pipelines?
Build one role per pipeline, grant only the needed actions on specific ARNs, add encryption and network conditions, and use permissions boundaries. Prefer KMS key policies plus IAM to enforce encryption.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Sid": "ReadRaw", "Effect": "Allow", "Action": ["s3:GetObject"],
     "Resource": "arn:aws:s3:::acme-raw/orders/*"},
    {"Sid": "WriteCurated", "Effect": "Allow", "Action": ["s3:PutObject", "s3:AbortMultipartUpload"],
     "Resource": "arn:aws:s3:::acme-curated/orders/*",
     "Condition": {"StringEquals": {"s3:x-amz-server-side-encryption": "aws:kms"}}},
    {"Sid": "Catalog", "Effect": "Allow",
     "Action": ["glue:GetTable", "glue:GetDatabase", "glue:GetPartitions", "glue:UpdateTable"],
     "Resource": ["arn:aws:glue:us-east-1:123456789012:catalog",
                  "arn:aws:glue:us-east-1:123456789012:database/curated",
                  "arn:aws:glue:us-east-1:123456789012:table/curated/orders"]},
    {"Sid": "Kms", "Effect": "Allow", "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
     "Resource": "arn:aws:kms:us-east-1:123456789012:key/abcd-1234"}
  ]
}
```

Anti-patterns to call out: `"Resource": "*"` with `s3:*`, wildcard `iam:PassRole`, credentials in job configs, and one shared role across unrelated pipelines.

[Table of Contents](#AWS)

## How do you orchestrate pipelines with Step Functions and EventBridge?
Step Functions coordinate multi-step workflows with retries, catch blocks, and parallel branches; EventBridge triggers them on schedules or events such as an S3 `ObjectCreated`. Using `.sync` integration patterns makes the state machine wait for Glue and Athena.

```json
{
  "Comment": "Order file arrival to Glue to Athena validation",
  "StartAt": "RunGlue",
  "States": {
    "RunGlue": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {"JobName": "orders_curated"},
      "Retry": [{"ErrorEquals": ["States.TaskFailed"], "IntervalSeconds": 30, "MaxAttempts": 3, "BackoffRate": 2.0}],
      "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "NotifyFailure"}],
      "Next": "Validate"
    },
    "Validate": {
      "Type": "Task",
      "Resource": "arn:aws:states:::athena:startQueryExecution.sync",
      "Parameters": {"QueryString": "SELECT count(*) FROM curated.orders WHERE ds = current_date", "WorkGroup": "primary"},
      "Next": "Success"
    },
    "Success": {"Type": "Succeed"},
    "NotifyFailure": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {"TopicArn": "arn:aws:sns:us-east-1:123456789012:data-oncall", "Message": "orders pipeline failed"},
      "End": true
    }
  }
}
```

```json
{"Source": ["aws.s3"], "DetailType": ["Object Created"],
 "Detail": {"bucket": {"name": ["acme-raw"]}, "object": {"key": [{"prefix": "orders/"}]}}}
```

Interview points: Step Functions provide retry/backoff and idempotency hooks cron jobs lack, and EventBridge replaces polling with event-driven and scheduled triggers.

[Table of Contents](#AWS)

## How do you ingest streaming data with Amazon Kinesis?
Kinesis Data Streams is the replayable low-level stream and Firehose delivers to S3, Redshift, or OpenSearch with optional transformation. A producer partitions records by key; consumers read shards with an iterator.

```python
import json

import boto3

kinesis = boto3.client("kinesis")


def publish(stream_name: str, orders: list[dict]) -> None:
    records = [
        {"PartitionKey": str(order["customer_id"]), "Data": (json.dumps(order) + "\n").encode("utf-8")}
        for order in orders
    ]
    kinesis.put_records(StreamName=stream_name, Records=records)
```

Design points: the partition key controls ordering and hot-shard risk; one shard supports 1 MB/s or 1,000 records/s ingest and 2 MB/s egress; retention defaults to 24 hours and can extend to 365 days for replay; use enhanced fan-out for multiple fast consumers and on-demand mode to avoid shard math. Firehose buffers up to 900 seconds, so it is near-real-time.

[Table of Contents](#AWS)

## How do you govern a data lake with AWS Lake Formation?
Lake Formation centralizes fine-grained permissions on Glue Data Catalog tables and the S3 data behind them. You register S3 locations, grant table/column/row permissions to principals, and scale with LF-Tags instead of per-table grants.

```bash
aws lakeformation register-resource --resource-arn arn:aws:s3:::acme-curated --use-service-linked-role
aws lakeformation add-lf-tags --catalog-id 123456789012 --tag-key classification --tag-values public pii phi
aws lakeformation grant-permissions \
  --principal DataLakePrincipalIdentifier=arn:aws:iam::123456789012:role/analyst-role \
  --resource '{"TableWithColumns":{"DatabaseName":"curated","Name":"orders","ColumnNames":["order_id","order_ts","amount"],"ColumnWildcard":{}}}' \
  --permissions SELECT
```

It provides column-level and row-level security, tag-based access, and cross-account sharing, but it does not replace IAM and only governs engines that honor it (Athena, Glue, Redshift Spectrum, and EMR with the Lake Formation runtime).

[Table of Contents](#AWS)

## How do you choose between AWS data services? Trade-offs and when not to use them
Match the tool to data size, latency, team skills, and cost model.

+ S3 - durable lake storage, not a database; no transactions or row-level updates.
+ Glue - managed Spark/Python ETL; not for very large shuffle-heavy or long-running custom jobs.
+ EMR - large-scale Spark/Hadoop and Spot batch; more operations to own.
+ Lambda - small event-driven tasks; avoid beyond 15 minutes or for large shuffles.
+ Athena - ad-hoc and intermittent SQL over S3; poor for high-concurrency low-latency BI.
+ Redshift - high-concurrency modeled BI; not for tiny point lookups or OLTP.
+ Kinesis - AWS-native streaming; not a task queue and not Kafka-compatible.
+ MSK - best when already on Kafka; you pay for brokers and carry more operations.
+ DynamoDB - high-volume key access at single-digit milliseconds; not ad-hoc analytics.
+ Step Functions - multi-service orchestration; not high-throughput data movement.
+ Lake Formation - fine-grained lake governance; adds complexity for small teams that can start with IAM plus catalog policies.

Cost drivers: bytes scanned (Athena), DPU/worker-hours (Glue, EMR), cluster uptime and concurrency (Redshift), shard-hours and retention (Kinesis), broker-hours (MSK), and storage class plus requests (S3). Security drivers: least-privilege roles, KMS, VPC endpoints, Lake Formation column/row filters, and CloudTrail. Performance drivers: file sizes and formats, partitioning, distribution/sort keys, and shuffle management.

[Table of Contents](#AWS)

## Real world use cases for AWS
### Use case 1: E-commerce clickstream to real-time and batch analytics
Business context: up-to-the-minute conversion dashboards plus next-day cohort analysis. Data volume: ~1.5 TB/day, peaking at 40,000 events/second during promotions.

Architecture: API Gateway -> Kinesis Data Streams (on-demand) -> Lambda enrich -> Firehose -> S3 raw; Glue hourly -> S3 curated Parquet; Athena for ad-hoc, Redshift for BI.

```python
import base64
import json


def handler(event, context):
    records = []
    for record in event["Records"]:
        payload = json.loads(base64.b64decode(record["kinesis"]["data"]))
        payload["country"] = payload.get("country") or "unknown"
        records.append({"PartitionKey": record["kinesis"]["partitionKey"],
                        "Data": json.dumps(payload) + "\n"})
    return {"records": records}
```

Why: on-demand Kinesis absorbs promotion spikes without shard math, Firehose delivers cheap micro-batches to S3, Athena serves cheap exploration, and Redshift serves high-concurrency dashboards from the same raw truth.

### Use case 2: CDC from operational databases into a governed warehouse
Business context: near-real-time transaction reporting with strict PII controls. Data volume: ~5 TB/day, ~200 million change records/day from 12 databases.

Architecture: RDS/Aurora -> DMS CDC -> Kinesis/MSK -> Glue streaming -> S3 raw JSON; Glue dedupe/merge -> curated Parquet -> Redshift `COPY`; Lake Formation LF-Tags restrict PII columns.

```python
from pyspark.sql import Window
from pyspark.sql import functions as F

window = Window.partitionBy("transaction_id").orderBy(F.col("source_lsn").desc())
deduped = cdc.withColumn("rn", F.row_number().over(window)).where(F.col("rn") == 1).drop("rn")
```

Why: CDC avoids full extracts, Glue dedupes and absorbs schema drift, `COPY` loads files in parallel, and Lake Formation column filters keep raw PII out of analyst queries.

### Use case 3: Cost-controlled log analytics with Athena partition projection
Business context: 13 months of application and CDN logs searchable for incident response under tight cost control. Data volume: ~50 TB in S3, growing ~3 TB/month, queried in bursts.

Architecture: CloudFront/ALB logs -> S3 raw (gzip) -> Athena projection table on `ds`/`hour` -> dashboards, with a 10 GB per-query scan cutoff.

```json
{"Rules":[{"ID":"logs-tier","Status":"Enabled","Filter":{"Prefix":"logs/"},
 "Transitions":[{"Days":30,"StorageClass":"STANDARD_IA"},{"Days":90,"StorageClass":"GLACIER_IR"}]}]}
```

Why: projection removes crawler and `MSCK REPAIR` overhead across tens of thousands of partitions, Parquet conversion of hot prefixes cuts bytes scanned by an order of magnitude, and lifecycle tiers plus a scan cutoff keep the Athena bill predictable.

### Use case 4: A governed multi-team data lake with Lake Formation
Business context: healthcare analytics with data science, finance, and clinical teams sharing one lake under strict column and row restrictions. Data volume: ~20 TB curated across hundreds of tables.

Architecture: producers -> S3 raw (domain prefixes) -> Glue -> S3 curated registered with Lake Formation; consumers use Athena, Redshift Spectrum, or EMR, which honor LF permissions.

```bash
aws lakeformation grant-permissions \
  --principal DataLakePrincipalIdentifier=arn:aws:iam::123456789012:role/clinical-analyst \
  --resource '{"LFTagPolicy":{"ResourceType":"TABLE","Expression":[{"TagKey":"domain","TagValues":["clinical"]},{"TagKey":"classification","TagValues":["public","pii"]}]}}' \
  --permissions SELECT DESCRIBE
```

Why: LF-Tags scale permission management to hundreds of tables without an unmaintainable grant matrix, column exclusions on PHI satisfy compliance, and centrally registered S3 locations stop producers bypassing governance with ad-hoc bucket policies.

[Table of Contents](#AWS)
