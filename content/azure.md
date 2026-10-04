## [Main title](../README.md)
### [Interview questions](full.md)

# Azure

Azure's data platform centers on Azure Data Lake Storage Gen2 for storage, Azure Data Factory and Synapse Pipelines for orchestration, Azure Databricks and Synapse Spark for processing, Synapse SQL for serving, Microsoft Purview for governance, and Microsoft Entra ID for identity. Many of the classic "Windows Azure" questions below are legacy Cloud Services concepts; they are kept, with notes on what replaced them.

+ [What are the three Main Components of Windows Azure Platform?](#What-are-the-three-Main-Components-of-Windows-Azure-Platform)
+ [How would you design a data lake on Azure?](#How-would-you-design-a-data-lake-on-Azure)
+ [When would you use Azure Data Factory, Synapse, Databricks, or Functions?](#When-would-you-use-Azure-Data-Factory-Synapse-Databricks-or-Functions)
+ [What are the Service Model in Cloud Computing?](#What-are-the-Service-Model-in-Cloud-Computing)
+ [How many Types of Deployment Models are used in Cloud?](#How-many-Types-of-Deployment-Models-are-used-in-Cloud)
+ [What is Windows Azure Platform?](#What-is-Windows-Azure-Platform)
+ [What are the Roles Available in Windows Azure?](#What-are-the-Roles-Available-in-Windows-Azure)
+ [What is difference between Windows Azure Platform and Windows Azure?](#What-is-difference-between-Windows-Azure-Platform-and-Windows-Azure)
+ [What are the three Types of Roles in Compute Component in Windows Azure?](#What-are-the-three-Types-of-Roles-in-Compute-Component-in-Windows-Azure)
+ [What is Windows Azure Compute Emulator?](#What-is-Windows-Azure-Compute-Emulator)
+ [What is Fabric?](#What-is-Fabric)
+ [How many instances of a Role should be deployed to Satisfy Azure Sla?](#How-many-instances-of-a-Role-should-be-deployed-to-Satisfy-Azure-Sla)
+ [What are the options to manage Session State in Windows Azure?](#What-are-the-options-to-manage-Session-State-in-Windows-Azure)
+ [What is Cspack?](#What-is-Cspack)
+ [What is Csrun?](#What-is-Csrun)
+ [What is Guest Os?](#What-is-Guest-Os)
+ [How to programmatically Scale Out Azure Worker Role Instances?](#How-to-programmatically-Scale-Out-Azure-Worker-Role-Instances)
+ [What is Web Role in Windows Azure?](#What-is-Web-Role-in-Windows-Azure)
+ [What is the difference between Public Cloud and Private Cloud?](#What-is-the-difference-between-Public-Cloud-and-Private-Cloud)
+ [What is Windows Azure Diagnostics?](#What-is-Windows-Azure-Diagnostics)
+ [What is Blob?](#What-is-Blob)
+ [What is the difference between Block Blob Vs Page Blob?](#What-is-the-difference-between-Block-Blob-Vs-Page-Blob)
+ [What is the difference between Windows Azure Queues and Windows Azure Service Bus Queues?](#What-is-the-difference-between-Windows-Azure-Queues-and-Windows-Azure-Service-Bus-Queues)
+ [What is Deadletter Queue?](#What-is-Deadletter-Queue)
+ [What are Instance Sizes of Azure?](#What-are-Instance-Sizes-of-Azure)
+ [What is Table Storage in Windows Azure?](#What-is-Table-Storage-in-Windows-Azure)
+ [Difference between Web and Worker Roles in Windows Azure?](#Difference-between-Web-and-Worker-Roles-in-Windows-Azure)
+ [What is Azure Fabric Controller?](#What-is-Azure-Fabric-Controller)
+ [What is Autoscaling?](#What-is-Autoscaling)
+ [What is Vm Role in Windows Azure?](#What-is-Vm-Role-in-Windows-Azure)
+ [Apart from dotnet Framework please name other three language framework that can be used to Develop Windows Azure Applications?](#Apart-from-dotnet-Framework-please-name-other-three-language-framework-that-can-be-used-to-Develop-Windows-Azure-Applications)
+ [How would you categorize Windows Azure?](#How-would-you-categorize-Windows-Azure)
+ [What is Azure Cloud Service?](#What-is-Azure-Cloud-Service)
+ [What is Cloud Service Role?](#What-is-Cloud-Service-Role)
+ [What is Link Resource?](#What-is-Link-Resource)
+ [What is Scale Cloud Service?](#What-is-Scale-Cloud-Service)
+ [What is Web Role ?](#What-is-Web-Role)
+ [What is Worker Role ?](#What-is-Worker-Role)
+ [What is Role Instance ?](#What-is-Role-Instance)
+ [What is Guest Operating System ?](#What-is-Guest-Operating-System)
+ [What is Cloud Service Components?](#What-is-Cloud-Service-Components)
+ [What is Deployment Environments?](#What-is-Deployment-Environments)
+ [What is Swap Deployments?](#What-is-Swap-Deployments)
+ [What is Minimal Vs Verbose Monitoring?](#What-is-Minimal-Vs-Verbose-Monitoring)
+ [What is Service Definition File?](#What-is-Service-Definition-File)
+ [What is Service Configuration File?](#What-is-Service-Configuration-File)
+ [What is Service Package ?](#What-is-Service-Package)
+ [What is Cloud Service Deployment ?](#What-is-Cloud-Service-Deployment)
+ [What is Azure Diagnostics ?](#What-is-Azure-Diagnostics)
+ [What is Azure Service Level Agreement?](#What-is-Azure-Service-Level-Agreement)
+ [How do you use the Azure CLI for data platform tasks?](#How-do-you-use-the-Azure-CLI-for-data-platform-tasks)
+ [How do you write a Synapse SQL warehouse pipeline?](#How-do-you-write-a-Synapse-SQL-warehouse-pipeline)
+ [How do you build an Azure Data Factory pipeline?](#How-do-you-build-an-Azure-Data-Factory-pipeline)
+ [How do you work with ADLS Gen2 paths and access control?](#How-do-you-work-with-ADLS-Gen2-paths-and-access-control)
+ [How do you write a Databricks notebook and PySpark job?](#How-do-you-write-a-Databricks-notebook-and-PySpark-job)
+ [How do you implement Entra ID RBAC and managed identities?](#How-do-you-implement-Entra-ID-RBAC-and-managed-identities)
+ [How do you stream events with Azure Event Hubs?](#How-do-you-stream-events-with-Azure-Event-Hubs)
+ [How do you choose between Azure data services? Trade-offs and when not to use them](#How-do-you-choose-between-Azure-data-services-Trade-offs-and-when-not-to-use-them)
+ [Real world use cases for Azure](#Real-world-use-cases-for-Azure)

## What are the three Main Components of Windows Azure Platform?
+ Compute
+ Storage
+ AppFabric

In today's Azure terms these map to compute services (VMs, App Service, Functions, Container Apps, Databricks), storage services (Blob, ADLS Gen2, Files, Queues, Tables), and the integration/identity fabric (Service Bus, Event Grid, Event Hubs, Entra ID, API Management).

[Table of Contents](#Azure)

## How would you design a data lake on Azure?
Use ADLS Gen2 (hierarchical namespace enabled) for storage, Azure Data Factory or Synapse Pipelines for orchestration, Databricks or Synapse Spark for processing, Purview for catalog and governance, and Synapse SQL or Power BI for serving. Organize storage into raw, curated, and serving layers.

```text
abfss://lake@acme.dfs.core.windows.net/raw/orders/ds=2026-10-04/
abfss://lake@acme.dfs.core.windows.net/curated/orders/ds=2026-10-04/
abfss://lake@acme.dfs.core.windows.net/marts/fact_orders/
```

Good answers include identity and security: managed identities instead of keys, RBAC plus POSIX ACLs on ADLS paths, private endpoints, Key Vault for secrets, and diagnostic logs to Log Analytics.

[Table of Contents](#Azure)

## When would you use Azure Data Factory, Synapse, Databricks, or Functions?
Use Data Factory for orchestration, copy activities, and connecting many sources. Use Synapse when you want integrated SQL, Spark, pipelines, and warehouse-style analytics in one workspace. Use Azure Databricks for collaborative Spark, Delta Lake, ML, and advanced tuning. Use Azure Functions for small event-driven automation.

Example choices:

+ nightly copy from SQL Server to ADLS: Data Factory
+ large Spark transformation over Delta tables: Databricks or Synapse Spark
+ SQL serving layer for Power BI: Synapse SQL
+ validate a file when it lands in blob storage: Azure Functions

The decision depends on workload size, latency, team skills, governance, and how much runtime control you need. Databricks and Synapse Spark overlap heavily; choose Databricks when you want the richer Spark/ML ecosystem and Delta-first tooling, and Synapse when you want SQL and Spark unified in one workspace with tighter Synapse SQL integration.

[Table of Contents](#Azure)

## What are the Service Model in Cloud Computing?
Cloud providers offer three fundamental models: Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS). IaaS is the most basic, and each higher model abstracts more of the lower layers.

+ IaaS examples: Azure Virtual Machines, Amazon EC2, Google Compute Engine.
+ PaaS examples: Azure App Service, Azure SQL Database, Azure Databricks, Heroku, Google App Engine.
+ SaaS examples: Microsoft 365, Salesforce, Google Workspace.

Data engineering usually lands between IaaS and PaaS: managed Spark (PaaS) for compute, but you still own data models, pipelines, and governance.

[Table of Contents](#Azure)

## How many Types of Deployment Models are used in Cloud?
Four: public cloud, private cloud, community cloud, and hybrid cloud. Most enterprises run hybrid, keeping some systems on-premises while data lands in the cloud.

[Table of Contents](#Azure)

## What is Windows Azure Platform?
It is the collective name for Microsoft's Platform as a Service offering: a programming platform, a deployment vehicle, and a runtime environment hosted in Microsoft data centers. It is now branded Microsoft Azure and covers IaaS, PaaS, and SaaS.

[Table of Contents](#Azure)

## What are the Roles Available in Windows Azure?
The classic Cloud Services roles were web, worker, and VM, all running Windows Server. Web and Worker roles were nearly identical, with the OS and patches managed for you. These are legacy: Cloud Services (classic) is retired, and the modern equivalents are App Service and Container Apps (web), Functions and Container Apps Jobs (worker), and Virtual Machine Scale Sets (VM).

[Table of Contents](#Azure)

## What is difference between Windows Azure Platform and Windows Azure?
The Windows Azure Platform was Microsoft's PaaS offering including Windows Azure, SQL Azure, and AppFabric. Windows Azure was the cloud OS portion of that offering. Both names are now Microsoft Azure.

[Table of Contents](#Azure)

## What are the three Types of Roles in Compute Component in Windows Azure?
+ Web
+ Worker
+ VM

Modern mapping: Web -> App Service/Container Apps, Worker -> Functions/Container Apps Jobs, VM -> Virtual Machines/VM Scale Sets.

[Table of Contents](#Azure)

## What is Windows Azure Compute Emulator?
The compute emulator was a local emulator used to build and test a Cloud Services application before deploying it. It is legacy; modern development uses the Azurite storage emulator plus local Docker/Azure Functions Core Tools, or a personal dev environment.

[Table of Contents](#Azure)

## What is Fabric?
In the classic Windows Azure sense, the cloud fabric is the combination of many virtualized instances that run client applications. Do not confuse it with Microsoft Fabric, the modern SaaS analytics platform, or with Service Fabric, the microservices platform.

[Table of Contents](#Azure)

## How many instances of a Role should be deployed to Satisfy Azure Sla?
Two or more. With two or more instances per role, the classic Compute SLA guaranteed external connectivity at least 99.95% of the time. Modern services publish their own SLAs, and availability-zone or multi-region designs raise the achievable number.

[Table of Contents](#Azure)

## What are the options to manage Session State in Windows Azure?
+ Azure Cache for Redis (the modern default)
+ Azure SQL Database
+ Azure Table Storage (now part of Azure Storage / Cosmos DB Table API)

For distributed web apps, keep sessions out of the web tier and store them in Redis with a TTL.

[Table of Contents](#Azure)

## What is Cspack?
Cspack is a legacy command-line tool that generated a Cloud Services package file (`.cspkg`) for deployment to Windows Azure or the compute emulator. It belongs to the retired Cloud Services model.

[Table of Contents](#Azure)

## What is Csrun?
Csrun is a legacy command-line tool that deployed a packaged Cloud Services application to the compute emulator and managed the running service.

[Table of Contents](#Azure)

## What is Guest Os?
The guest OS is the operating system running on the virtual machine that hosts a role instance. In modern Azure this is the VM image you choose (Ubuntu, Windows Server, or a marketplace image), and you own its patching unless you use a managed service.

[Table of Contents](#Azure)

## How to programmatically Scale Out Azure Worker Role Instances?
In the classic model you used the Autoscaling Application Block or the Service Management API. Today you scale with VM Scale Sets autoscale rules, App Service autoscale, or AKS/Databricks autoscaling, driven by metrics such as CPU, queue length, or a custom metric.

```bash
az monitor autoscale create \
  --resource-group rg-data \
  --resource myVmss \
  --resource-type Microsoft.Compute/virtualMachineScaleSets \
  --min-count 2 --max-count 20 --count 2
az monitor autoscale rule create \
  --resource-group rg-data --autoscale-name myVmss \
  --condition "Percentage CPU > 70 avg 5m" --scale out 2
```

[Table of Contents](#Azure)

## What is Web Role in Windows Azure?
A web role was a Cloud Services role providing a dedicated IIS web server for hosting front-end web applications that could be scaled up or down. It is legacy; App Service, Container Apps, and Static Web Apps cover this today.

[Table of Contents](#Azure)

## What is the difference between Public Cloud and Private Cloud?
A public cloud is offered as a service over the internet to many customers on shared infrastructure. A private cloud is deployed within an organization's boundaries, often behind a firewall, and is managed and monitored by that organization. Hybrid cloud connects the two.

[Table of Contents](#Azure)

## What is Windows Azure Diagnostics?
Windows Azure Diagnostics collected diagnostic data from applications running in Azure for debugging, performance measurement, resource usage, traffic analysis, and auditing. Modern equivalents are Azure Monitor, Application Insights, Log Analytics workspaces, and diagnostic settings on each resource.

[Table of Contents](#Azure)

## What is Blob?
A BLOB (Binary Large Object) is a file of any type and size in Azure Blob Storage. Blob Storage offers block blobs, append blobs, and page blobs. The URL format is `https://<account>.blob.core.windows.net/<container>/<blob>`, or `https://<account>.dfs.core.windows.net/<container>/<path>` for the ADLS Gen2 (DFS) endpoint.

[Table of Contents](#Azure)

## What is the difference between Block Blob Vs Page Blob?
Block blobs are composed of blocks identified by block IDs; you upload blocks and commit them, and a small blob can be written in one `Put Blob`. They are optimized for sequential read/write and are the standard for data lakes, logs, and media. Page blobs are collections of 512-byte pages addressed by offset and are designed for random read/write, which is why they back Azure VM OS and data disks. Append blobs are optimized for append-only logs.

Limits to remember for interviews: a single block blob today supports up to about 190.7 TiB, and page blobs up to 8 TiB. If you need random writes to data, use a database or page blobs, not block blobs.

[Table of Contents](#Azure)

## What is the difference between Windows Azure Queues and Windows Azure Service Bus Queues?
Azure Queue Storage is a simple REST-based get/put/peek queue for reliable persistent messaging within and between services. Service Bus Queues are part of a richer messaging infrastructure that supports queuing plus publish/subscribe, sessions, transactions, dead-lettering, duplicate detection, and integration patterns. Use Queue Storage for cheap high-volume decoupling and Service Bus for ordered, transactional, or topic-based messaging.

[Table of Contents](#Azure)

## What is Deadletter Queue?
A dead-letter queue holds messages the system could not process. Messages are moved there when:

+ A message expires and dead-lettering for expired messages is enabled.
+ The max delivery count is exceeded on a queue or subscription.
+ A filter evaluation exception occurs on a subscription and dead-lettering on filter exceptions is enabled.

Always monitor dead-letter counts and build a replay path; a growing DLQ is a silent outage.

[Table of Contents](#Azure)

## What are Instance Sizes of Azure?
Azure VM sizes are grouped by family and purpose rather than the old extra-small-to-extra-large naming. Modern families include:

+ General purpose: B (burstable), D, and Dasv/Dsv-series.
+ Compute optimized: F-series.
+ Memory optimized: E, M-series.
+ Storage optimized: L-series.
+ GPU/accelerated: NC, ND, NV-series.

Data workloads typically pick D/E-series for Spark drivers, L-series or local NVMe for shuffle and caching, and burstable B-series only for lightweight orchestration.

[Table of Contents](#Azure)

## What is Table Storage in Windows Azure?
Azure Table Storage stores large amounts of structured, non-relational data and accepts authenticated calls from inside and outside Azure. A table is a collection of entities and does not enforce a schema; an account can have many tables. An entity is a set of properties like a row and can be up to 1 MB. A property is a name-value pair, up to 252 per entity, plus the system properties `PartitionKey`, `RowKey`, and `Timestamp`. Entities sharing a partition key are queried faster and support atomic batch operations; the row key is unique within a partition.

```python
from azure.data.tables import TableClient

table = TableClient.from_connection_string(conn_str, table_name="orders")
table.create_entity({"PartitionKey": "2026-10", "RowKey": "1001", "status": "created", "amount": 42.5})
```

Modern alternatives: Cosmos DB Table API for global scale and low latency, or Cosmos DB SQL API when you need richer queries and indexing.

[Table of Contents](#Azure)

## Difference between Web and Worker Roles in Windows Azure?
A web role instance ran IIS; a worker role instance did not. Both were managed the same way, and applications often used both, for example a web role receiving requests and handing work to a worker role. Modern equivalents: App Service or Container Apps for the web tier and Functions, Container Apps Jobs, or Worker Services for background processing.

[Table of Contents](#Azure)

## What is Azure Fabric Controller?
The Fabric Controller was the resource provisioning and management layer that managed the hardware and provided allocation, deployment, upgrade, and management for Cloud Services. Modern Azure abstracts this into the platform control plane; Service Fabric is a separate microservices platform and Microsoft Fabric is a separate analytics SaaS.

[Table of Contents](#Azure)

## What is Autoscaling?
Scaling out adds instances; scaling up uses larger instances. Azure supports both, and autoscaling adjusts instance count at runtime to balance performance against cost and reduce manual work. In data platforms, autoscaling is most valuable for Spark clusters (Databricks autoscaling or Synapse Spark pools), AKS node pools, and function consumption plans.

[Table of Contents](#Azure)

## What is Vm Role in Windows Azure?
The VM role let you deploy a custom Windows Server image to Windows Azure for applications needing heavy OS customization. It was a beta-era Cloud Services concept. Today you use Virtual Machines, VM Scale Sets, or custom images in a Shared Image Gallery, and configure them with cloud-init or Desired State Configuration.

[Table of Contents](#Azure)

## Apart from dotnet Framework please name other three language framework that can be used to Develop Windows Azure Applications?
PHP, Node.js, and Java. Today virtually any language is supported through App Service, Functions, containers, and SDKs for Python, Java, Go, JavaScript, .NET, and Rust.

[Table of Contents](#Azure)

## How would you categorize Windows Azure?
Originally positioned as PaaS. Microsoft Azure is now a full-spectrum cloud spanning IaaS, PaaS, and SaaS, plus specialized data and AI services.

[Table of Contents](#Azure)

## What is Azure Cloud Service?
A Cloud Service was a way to deploy a multi-tier web application with one or more web and worker roles, each with its own files and configuration, allowing flexible scaling. Its main advantage was supporting complex multi-tier architectures. Cloud Services (classic) is retired; modern equivalents are App Service, Container Apps, and AKS.

[Table of Contents](#Azure)

## What is Cloud Service Role?
A cloud service role was a set of application files plus configuration. A cloud service could have web roles, worker roles, or both. This concept is legacy.

[Table of Contents](#Azure)

## What is Link Resource?
Linking a resource showed a cloud service's dependencies on other resources, such as an Azure SQL Database, so you could view and scale them together in the portal. Linking did not connect the resource to the application; you still configured the connection in code. Legacy Cloud Services concept; modern deployments use ARM/Bicep/Terraform to express dependencies explicitly.

[Table of Contents](#Azure)

## What is Scale Cloud Service?
A cloud service scaled out by increasing role instances and scaled in by decreasing them, and linked resources such as SQL Database could be scaled in the same operation. Modern equivalent: autoscale rules on VM Scale Sets, App Service plans, or Databricks clusters.

[Table of Contents](#Azure)

## What is Web Role ?
A web role provided a dedicated IIS web server for hosting front-end web applications. Legacy; see App Service and Container Apps.

[Table of Contents](#Azure)

## What is Worker Role ?
A worker role hosted asynchronous, long-running, or perpetual tasks independent of user interaction. Legacy; see Azure Functions, Container Apps Jobs, and Worker Services.

[Table of Contents](#Azure)

## What is Role Instance ?
A role instance was a virtual machine running the application code and role configuration. A role could have multiple instances defined in the service configuration file. This is the direct ancestor of the modern replica/instance concept in App Service, Container Apps, and VM Scale Sets.

[Table of Contents](#Azure)

## What is Guest Operating System ?
The guest OS for a cloud service was the operating system installed on the role instances where application code ran. Today it is the VM image you select, and managed services hide it from you entirely.

[Table of Contents](#Azure)

## What is Cloud Service Components?
Three components were required to deploy a Cloud Services application: the service definition file (`.csdef`), the service configuration file (`.cscfg`), and the service package (`.cspkg`). Legacy.

[Table of Contents](#Azure)

## What is Deployment Environments?
Azure offered two Cloud Services deployment environments: staging, for testing before promotion, and production. They differed only by VIP, with staging reached via the GUID (`GUID.cloudapp.net`) and production via the friendly DNS name (`myservice.cloudapp.net`). Modern deployments use slots (App Service deployment slots) or separate environments and canary releases.

[Table of Contents](#Azure)

## What is Swap Deployments?
Swapping promoted a staging deployment to production by switching the VIPs, after which the DNS name pointed to what had been staging. App Service deployment slots provide the same zero-downtime swap semantics today.

[Table of Contents](#Azure)

## What is Minimal Vs Verbose Monitoring?
Minimal monitoring, the default, gathered performance counters from the host OS for role instances. Verbose monitoring gathered additional metrics from inside the role instances for closer analysis during processing. Modern equivalent: Azure Monitor metrics plus Application Insights or Log Analytics at whatever granularity you configure.

[Table of Contents](#Azure)

## What is Service Definition File?
The cloud service definition file (`.csdef`) defined the service model, including the roles. Legacy.

[Table of Contents](#Azure)

## What is Service Configuration File?
The cloud service configuration file (`.cscfg`) provided configuration settings for the service and individual roles, including the number of role instances. Legacy; modern equivalent is app settings, environment variables, and Key Vault references.

[Table of Contents](#Azure)

## What is Service Package ?
The service package (`.cspkg`) contained the application code and the service definition file. Legacy; modern packaging is a container image, a zip deploy, or a wheel/egg for Databricks jobs.

[Table of Contents](#Azure)

## What is Cloud Service Deployment ?
A cloud service deployment was an instance of a cloud service deployed to the staging or production environment, with both maintained at once. Legacy; modern releases use slots, blue/green environments, and infrastructure as code.

[Table of Contents](#Azure)

## What is Azure Diagnostics ?
Azure Diagnostics is the API for collecting diagnostic data from applications running in Azure; it had to be enabled for verbose monitoring. Modern equivalent: diagnostic settings that route platform logs and metrics to Log Analytics, Storage, or Event Hubs, plus Application Insights for app telemetry.

[Table of Contents](#Azure)

## What is Azure Service Level Agreement?
The classic Compute SLA guaranteed 99.95% access when two or more role instances were deployed for every role, and corrective action initiation 99.9% of the time when a role instance process was not running. Modern Azure SLAs are per-service; for example, availability-zone deployments of VMs and premium storage publish higher targets, and composite SLAs across services are lower than any single service.

[Table of Contents](#Azure)

## How do you use the Azure CLI for data platform tasks?
The Azure CLI (`az`) is the standard way to script resource creation, upload data, and inspect services in CI/CD. Authenticate with a service principal or workload identity federation in automation, and with `az login` interactively.

```bash
az login
az group create --name rg-data --location eastus2
az storage account create --name acmedata --resource-group rg-data \
  --location eastus2 --sku Standard_ZRS --kind StorageV2 --hns true
az storage container create --account-name acmedata --name lake --auth-mode login
az storage blob upload --account-name acmedata --container-name lake \
  --name raw/orders/ds=2026-10-04/orders.parquet --file orders.parquet --auth-mode login
az storage fs file list --account-name acmedata --file-system lake --path raw/orders --auth-mode login
```

```bash
az databricks workspace create --resource-group rg-data --name dbw-acme --location eastus2 --sku premium
az synapse workspace create --resource-group rg-data --name syn-acme --location eastus2 \
  --storage-account acmedata --file-system lake --sql-admin-login-user sqladmin
```

Interview point: prefer `--auth-mode login` (Entra ID) over account keys, and use `--hns true` to create a Gen2 account with a hierarchical namespace.

[Table of Contents](#Azure)

## How do you write a Synapse SQL warehouse pipeline?
Synapse SQL has a serverless pool for querying files in place and dedicated pools for provisioned warehouse performance. Dedicated pools use distributions (hash, round-robin, replicated) and a clustered columnstore index; loads use `COPY INTO` from ADLS rather than row inserts.

```sql
-- Serverless: query Parquet directly from ADLS Gen2
SELECT TOP 10 *
FROM OPENROWSET(
  BULK 'https://acmedata.dfs.core.windows.net/lake/curated/orders/**',
  FORMAT = 'PARQUET'
) AS orders;

-- Dedicated pool: modeled table with hash distribution and clustered columnstore
CREATE TABLE dbo.fact_orders (
  order_id    BIGINT NOT NULL,
  customer_id BIGINT NOT NULL,
  order_ts    DATETIME2 NOT NULL,
  amount      DECIMAL(12,2) NOT NULL
)
WITH (DISTRIBUTION = HASH(customer_id), CLUSTERED COLUMNSTORE INDEX);

COPY INTO dbo.fact_orders
FROM 'https://acmedata.dfs.core.windows.net/lake/curated/orders/'
WITH (FILE_TYPE = 'PARQUET', CREDENTIAL = (IDENTITY = 'Managed Identity'));
```

Choose the distribution around the largest fact-to-dimension join: hash-distribute on the join key to avoid data movement, and use replicated tables for small dimensions. `COPY INTO` uses managed identity and parallel file reads.

[Table of Contents](#Azure)

## How do you build an Azure Data Factory pipeline?
Data Factory pipelines are JSON activities driven by datasets and linked services. A copy activity reads a source dataset and writes a sink dataset, and triggers (schedule, tumbling window, or event) start the pipeline. Use parameterized datasets and a `ForEach` over a date range for backfills.

```json
{
  "name": "PL_Orders_Daily",
  "properties": {
    "parameters": {"windowStart": {"type": "String"}, "windowEnd": {"type": "String"}},
    "activities": [
      {
        "name": "CopyOrdersToCurated",
        "type": "Copy",
        "typeProperties": {
          "source": {
            "type": "ParquetSource",
            "storeSettings": {"type": "AzureBlobFSReadSettings", "recursive": true}
          },
          "sink": {
            "type": "ParquetSink",
            "storeSettings": {"type": "AzureBlobFSWriteSettings"}
          },
          "enableStaging": false
        },
        "inputs": [{"referenceName": "DS_RawOrders", "type": "DatasetReference",
          "parameters": {"folderPath": "@concat('raw/orders/ds=', pipeline().parameters.windowStart)"}}],
        "outputs": [{"referenceName": "DS_CuratedOrders", "type": "DatasetReference",
          "parameters": {"folderPath": "@concat('curated/orders/ds=', pipeline().parameters.windowStart)"}}]
      }
    ]
  }
}
```

Interview points: use managed identity for ADLS access, store secrets in Key Vault rather than linked-service credentials, prefer a tumbling-window trigger for exactly-once time slices, and use the data factory's mapping data flows only when a Spark-free visual transform is genuinely simpler than Databricks.

[Table of Contents](#Azure)

## How do you work with ADLS Gen2 paths and access control?
ADLS Gen2 is Blob Storage with a hierarchical namespace, so paths behave like a file system and support POSIX-like ACLs at directory and file level, plus Azure RBAC at the account/container level. Use `abfss://` in Spark and `https://<account>.dfs.core.windows.net` in SQL and the CLI.

```text
abfss://lake@acmedata.dfs.core.windows.net/raw/orders/ds=2026-10-04/
abfss://lake@acmedata.dfs.core.windows.net/curated/orders/ds=2026-10-04/
```

```bash
az storage fs access set --account-name acmedata --file-system lake --path raw \
  --acl "user:11111111-2222-3333-4444-555555555555:r-x" --auth-mode login
az storage fs access show --account-name acmedata --file-system lake --path raw
```

Key rules: RBAC and ACLs are both evaluated (the effective permission is the union of owner, RBAC, and ACL), the `dfs` endpoint supports directories while the `blob` endpoint does not, and a managed identity needs the `Storage Blob Data Contributor` role plus directory ACLs to write.

[Table of Contents](#Azure)

## How do you write a Databricks notebook and PySpark job?
In Databricks, notebooks are the interactive surface and `dbutils` provides workspace utilities. Jobs run the same code on a cluster; secrets come from secret scopes, and tables are usually Delta Lake managed by Unity Catalog. Prefer `MERGE` for idempotent upserts and `OPTIMIZE` for compaction.

```python
from pyspark.sql import functions as F

raw_path = "abfss://lake@acmedata.dfs.core.windows.net/raw/orders/"
orders = (
    spark.read.json(raw_path)
    .withColumn("order_ts", F.to_timestamp("order_ts"))
    .withColumn("amount", F.col("amount").cast("decimal(12,2)"))
    .dropDuplicates(["order_id"])
)

orders.write.format("delta").mode("overwrite").saveAsTable("curated.orders_bronze")

spark.sql("""
merge into curated.orders as target
using curated.orders_bronze as source
on target.order_id = source.order_id
when matched then update set target.amount = source.amount, target.order_ts = source.order_ts
when not matched then insert *
""")

spark.sql("optimize curated.orders zorder by (customer_id)")
```

Interview points: Unity Catalog gives three-level names (`catalog.schema.table`) and centralized governance; Delta gives ACID and time travel; `zorder` speeds filtered reads on the column you filter most; Delta Live Tables or Lakeflow pipelines add declarative expectations and lineage.

[Table of Contents](#Azure)

## How do you implement Entra ID RBAC and managed identities?
Microsoft Entra ID (formerly Azure AD) is the identity plane. Assign Azure roles at the right scope (management group, subscription, resource group, or resource) and use managed identities so services authenticate without stored secrets. For data access, the common roles are `Storage Blob Data Reader/Contributor`, `Synapse SQL Administrator`, and Databricks workspace/Unity Catalog grants.

```bash
# Grant a managed identity read access to the lake account at resource scope
az role assignment create --assignee-object-id <principal-id> --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/rg-data/providers/Microsoft.Storage/storageAccounts/acmedata

# Let a Synapse workspace use its managed identity to load data
az synapse workspace show --name syn-acme --resource-group rg-data --query identity.principalId
az storage fs access set --account-name acmedata --file-system lake --path curated \
  --acl "user:<principal-id>:rwx" --auth-mode login
```

Interview points: RBAC is inherited down the scope hierarchy; a deny assignment overrides allows; managed identity removes key rotation entirely; and for ADLS you often need both an RBAC role and a directory ACL. Federated credentials let CI/CD jobs use workload identity instead of a service-principal secret.

[Table of Contents](#Azure)

## How do you stream events with Azure Event Hubs?
Event Hubs is the Azure streaming ingestion service: a partitioned event log with consumer groups, retention (1-90 days depending on tier), and capture to ADLS or Blob Storage. Producers send events with a partition key; consumers read with an offset using the EventProcessorClient or Spark Structured Streaming.

```python
from azure.eventhub import EventHubProducerClient, EventData


def publish(connection_str: str, event_hub: str, orders: list[dict]) -> None:
    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_str, eventhub_name=event_hub
    )
    with producer:
        batch = producer.create_batch()
        for order in orders:
            batch.add(EventData(str(order)))
        producer.send_batch(batch)
```

```bash
az eventhubs namespace create --resource-group rg-data --name eh-acme --sku Standard
az eventhubs eventhub create --resource-group rg-data --namespace-name eh-acme \
  --name orders --partition-count 8 --message-retention 3
az eventhubs eventhub consumer-group create --resource-group rg-data \
  --namespace-name eh-acme --eventhub-name orders --name spark
```

Design points: the partition count is fixed at creation (or use auto-inflate) and sets the maximum consumer parallelism; the partition key preserves per-key ordering; Event Hubs Capture writes Avro micro-batches to storage; use the premium or dedicated tier for predictable latency, and use Kafka-compatible endpoints if you already have Kafka producers.

[Table of Contents](#Azure)

## How do you choose between Azure data services? Trade-offs and when not to use them
Match the service to data size, latency, team skills, and governance.

+ ADLS Gen2 - durable lake storage with file semantics; not a database, no transactions or row-level updates.
+ Azure Data Factory - orchestrator and connector-heavy copy tool; not a compute engine for heavy transforms (use Databricks or Synapse Spark).
+ Azure Databricks - best for large Spark/Delta workloads, ML, and advanced tuning; heavier cost model and cluster management.
+ Synapse - unified SQL plus Spark plus pipelines; convenient when you already standardize on Synapse, but the Spark experience is generally less rich than Databricks.
+ Synapse SQL serverless - pay-per-query over files; poor for high-concurrency repeated BI.
+ Synapse SQL dedicated - high-concurrency warehouse; not for tiny point lookups or OLTP.
+ Azure Functions - small event-driven automation; avoid long-running or memory-heavy transforms.
+ Event Hubs - high-throughput streaming ingestion; not a task queue (use Service Bus or Storage Queues) and not a long-term store beyond retention.
+ Cosmos DB - globally distributed low-latency NoSQL; not for analytical scans or ad-hoc joins.
+ Microsoft Fabric - SaaS analytics end to end; strong when you want one governed platform, weaker when you need fine-grained infrastructure control.

Cost drivers: cluster DBUs and VM hours (Databricks), DWU/vCore hours and pause behavior (Synapse SQL), activity runs and data movement units (Data Factory), throughput units and retention (Event Hubs), storage transactions and tiering (ADLS), and provisioned RU/s (Cosmos DB). Security drivers: Entra ID RBAC, managed identities, POSIX ACLs, private endpoints, Key Vault, and Purview classification. Performance drivers: file size and Parquet/Delta layout, partitioning, distribution keys, shuffle, and cluster sizing.

[Table of Contents](#Azure)

## Real world use cases for Azure
### Use case 1: Nightly retail ELT into a Synapse warehouse
Business context: a retailer consolidates point-of-sale, e-commerce, and inventory into one reporting layer for merchandising. Data volume: ~2 TB/night, ~40 source systems.

Architecture: Data Factory copies sources to `raw/` in ADLS Gen2, Databricks cleans and models to Delta in `curated/`, and Synapse SQL dedicated pools serve Power BI through `COPY INTO`.

```sql
COPY INTO dbo.fact_sales
FROM 'https://acmedata.dfs.core.windows.net/lake/curated/fact_sales/'
WITH (FILE_TYPE = 'PARQUET', CREDENTIAL = (IDENTITY = 'Managed Identity'));
```

Why: ADF handles breadth of connectors cheaply, Databricks absorbs the heavy transformation, and Synapse SQL gives sub-second dashboard queries with hash-distributed facts and replicated dimensions.

### Use case 2: IoT telemetry streaming with Event Hubs and Spark
Business context: a manufacturer monitors equipment health and predicts failures. Data volume: ~5 million events/minute, ~30 TB/month.

Architecture: devices -> IoT Hub/Event Hubs (8 or more partitions) -> Databricks Structured Streaming with a Delta sink; Event Hubs Capture archives raw Avro to ADLS for replay; Synapse or Power BI reads aggregates.

```python
events = (
    spark.readStream.format("eventhubs")
    .option("eventhubs.connectionString", connection_string)
    .load()
)
(events.writeStream.format("delta").option("checkpointLocation", "abfss://lake@acmedata.dfs.core.windows.net/checkpoints/telemetry")
 .trigger(availableNow=True).toTable("curated.telemetry"))
```

Why: Event Hubs absorbs bursty device traffic with ordering per partition key, Structured Streaming gives exactly-once Delta writes with checkpointing, and Capture keeps the raw stream available for reprocessing after a model change.

### Use case 3: Governed self-service analytics with Purview and Unity Catalog
Business context: a bank wants analysts to discover data without exposing PII, under regulatory audit. Data volume: ~50 TB across 300 tables.

Architecture: ADLS Gen2 registered in Unity Catalog, Purview scanning and classifying PII, Entra ID groups mapped to Unity Catalog grants, and Power BI consuming curated marts.

```bash
az role assignment create --assignee <analyst-group-id> --assignee-principal-type Group \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/<sub-id>/resourceGroups/rg-data/providers/Microsoft.Storage/storageAccounts/acmedata
```

Why: Unity Catalog centralizes table and column grants and lineage, Purview provides classification and data mapping for compliance, and Entra ID groups keep access management aligned with HR-driven identity.

### Use case 4: Cost-controlled log analytics with serverless SQL
Business context: an SRE team needs 12 months of application logs for incident response without a standing warehouse. Data volume: ~30 TB, bursty query patterns.

Architecture: diagnostic settings land logs in ADLS Gen2 as Parquet, Synapse SQL serverless queries them in place, and Workload Groups plus a per-query cost ceiling cap spend.

```sql
SELECT level, count(*) AS events
FROM OPENROWSET(BULK 'https://acmedata.dfs.core.windows.net/lake/logs/app/*/*.parquet', FORMAT = 'PARQUET') AS logs
WHERE status >= 500
GROUP BY level;
```

Why: serverless SQL avoids a provisioned warehouse for intermittent queries, Parquet plus directory partitioning keeps scans small, and lifecycle policies move older logs to cooler tiers.

[Table of Contents](#Azure)
