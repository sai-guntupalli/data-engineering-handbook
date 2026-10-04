## [Main title](../README.md)
### [Interview questions](full.md)

# Data Governance

+ [What is data governance and why does it matter?](#What-is-data-governance-and-why-does-it-matter)
+ [What is a data contract?](#What-is-a-data-contract)
+ [How do lineage and cataloging help governance?](#How-do-lineage-and-cataloging-help-governance)
+ [What is the difference between governance and security?](#What-is-the-difference-between-governance-and-security)
+ [What are common roles in data governance (owner/steward/custodian)?](#What-are-common-roles-in-data-governance-ownerstewardcustodian)
+ [What is a data catalog and what should it contain?](#What-is-a-data-catalog-and-what-should-it-contain)
+ [What is business glossary vs technical metadata?](#What-is-business-glossary-vs-technical-metadata)
+ [RBAC vs ABAC: what is the difference?](#RBAC-vs-ABAC-what-is-the-difference)
+ [What is row-level and column-level security?](#What-is-row-level-and-column-level-security)
+ [How do you implement row-level and column-level security in practice?](#How-do-you-implement-row-level-and-column-level-security-in-practice)
+ [How do you handle PII/PHI data in analytics platforms?](#How-do-you-handle-PIIPHI-data-in-analytics-platforms)
+ [What is data masking and tokenization?](#What-is-data-masking-and-tokenization)
+ [How do you tag and classify data in a catalog?](#How-do-you-tag-and-classify-data-in-a-catalog)
+ [How do you implement tag-based access control in Unity Catalog?](#How-do-you-implement-tag-based-access-control-in-Unity-Catalog)
+ [How do you implement Lake Formation tag-based access control?](#How-do-you-implement-Lake-Formation-tag-based-access-control)
+ [What is policy as code for data governance?](#What-is-policy-as-code-for-data-governance)
+ [How do you implement auditability for data access?](#How-do-you-implement-auditability-for-data-access)
+ [How do you handle GDPR right to be forgotten in a lakehouse or warehouse?](#How-do-you-handle-GDPR-right-to-be-forgotten-in-a-lakehouse-or-warehouse)
+ [What are data retention policies and how do you enforce them?](#What-are-data-retention-policies-and-how-do-you-enforce-them)
+ [How do you measure data governance maturity?](#How-do-you-measure-data-governance-maturity)
+ [Real world use cases for Data Governance](#Real-world-use-cases-for-Data-Governance)

## What is data governance and why does it matter?
Data governance is the set of processes, policies, and responsibilities that ensure data is discoverable, trusted, secure, and used correctly. It matters because data platforms scale to many teams; without governance, definitions diverge, access becomes risky, and compliance issues appear. Good governance enables faster, safer self-service analytics.

The four pillars interviewers expect:

```text
1. Ownership      - every dataset has an accountable owner and a steward.
2. Discovery      - catalog, glossary, lineage, and clear access request paths.
3. Protection     - classification, least privilege, masking, encryption, audit.
4. Lifecycle      - quality SLAs, retention, archival, and safe deprecation.
```

A governance program is only real when it is enforced in the platform, not just documented. Example enforcement points: catalog tags drive access policies, data contracts are checked in CI, retention is a scheduled job, and access reviews are tracked tickets.

[Table of Contents](#Data-Governance)

## What is a data contract?
A data contract is an agreement between data producers and consumers about schema, semantics, quality expectations, ownership, and change process. It prevents upstream teams from changing fields silently and breaking downstream pipelines.

Example contract items:

+ `order_id` is required and unique per order
+ `amount` is decimal and must be non-negative
+ `order_status` allowed values are `created`, `paid`, `cancelled`, `refunded`
+ breaking changes require versioning and consumer notice

In interviews, connect contracts to CI checks, schema registries, catalog ownership, and incident reduction.

A contract as code, validated before deployment:

```yaml
# contracts/orders_v1.yaml
dataset: gold.fact_orders
owner: orders-platform@example.com
stewards: [data-platform@example.com]
sla:
  freshness_minutes: 30
  availability: "99.9%"
schema:
  - name: order_id
    type: string
    required: true
    unique: true
  - name: amount
    type: decimal(12,2)
    required: true
    constraints: ["amount >= 0"]
  - name: order_status
    type: string
    enum: [created, paid, cancelled, refunded]
    required: true
quality_checks:
  - name: no_null_order_id
    sql: "select count(*) from {table} where order_id is null"
    expect: 0
change_policy:
  breaking: requires_new_version_and_consumer_signoff
  additive: allowed_with_notice
consumers:
  - name: finance_marts
    contact: finance-data@example.com
```

```python
# CI check: fail the build if the produced table violates the contract.
from pyspark.sql import functions as F

contract_violations = (
    spark.table("gold.fact_orders")
    .select(
        F.sum(F.col("order_id").isNull().cast("int")).alias("null_ids"),
        F.sum((F.col("amount") < 0).cast("int")).alias("negative_amounts"),
        F.sum((~F.col("order_status").isin("created", "paid", "cancelled", "refunded")).cast("int")).alias("bad_status"),
    )
    .first()
)

assert contract_violations.null_ids == 0, "order_id contract violated"
```

[Table of Contents](#Data-Governance)

## How do lineage and cataloging help governance?
Cataloging tells users what datasets exist, who owns them, what fields mean, and how to request access. Lineage shows where data came from and what downstream assets depend on it. Together they help with impact analysis, audits, and trust.

Example: before dropping `customer_email`, lineage can show dashboards, dbt models, and ML features that still use the column. The owner can then coordinate a safe deprecation instead of causing a production incident.

Lineage has two useful granularities:

+ Table-level lineage: fast impact analysis for schema changes and outages.
+ Column-level lineage: needed for PII propagation, because it answers "which derived columns contain data from `customer_email`?"

```sql
-- Query Unity Catalog table lineage (Delta sharing style metadata).
select
  source_table_full_name,
  target_table_full_name,
  event_time
from system.access.table_lineage
where target_table_full_name = 'main.gold.fact_orders'
  and event_time > current_timestamp() - interval 30 days
order by event_time desc;
```

Governance use cases for lineage: PII propagation analysis, cost attribution, deprecation impact, incident blast radius, and proving in an audit which systems processed regulated data.

[Table of Contents](#Data-Governance)

## What is the difference between governance and security?
Security focuses on preventing unauthorized access and ensuring confidentiality/integrity (access controls, encryption). Governance includes security but also covers ownership, definitions, quality, lifecycle, and change management. Governance answers "who owns this data and what does it mean", not just "who can access it".

| Concern | Security | Governance |
|---|---|---|
| Primary question | who can access it? | who owns it, what does it mean, how does it change? |
| Controls | IAM, encryption, network | catalog, glossary, contracts, retention |
| Failure mode | breach | wrong numbers, untraceable data, compliance gaps |
| Owner | security/CISO | data owner plus platform team |
| Evidence | access logs, pen tests | lineage, contracts, access reviews |

They overlap at classification: you cannot secure sensitive data if nobody has classified it, which is why governance usually drives the tag that security then enforces.

[Table of Contents](#Data-Governance)

## What are common roles in data governance (owner/steward/custodian)?
Common roles are:
+ data owner: accountable for the dataset and its business definition
+ data steward: maintains quality, metadata, and processes
+ data custodian: operates the technical platform (storage, access, backups)

Clear roles prevent "nobody owns it" incidents.

```text
Data owner      - business accountability (VP of Sales owns customer master).
Data steward    - day-to-day definitions, quality rules, dispute resolution.
Data custodian  - platform engineering: storage, pipelines, backups, access plumbing.
Data consumer   - analysts and data scientists who must follow the contract.
Privacy officer - legal/compliance for PII/PHI and erasure requests.
```

Interview note: the most common governance failure is an ownership gap at the boundary between teams, for example a table produced by a pipeline team but consumed as a business metric by finance. Name the accountable owner explicitly in the catalog.

[Table of Contents](#Data-Governance)

## What is a data catalog and what should it contain?
A data catalog is an inventory of datasets with searchable metadata. It typically contains dataset descriptions, owners, lineage, classifications, freshness/SLA, schema, and links to dashboards. A good catalog reduces time to discovery and improves trust and reuse.

Minimum useful catalog fields:

```yaml
asset: main.gold.fact_orders
kind: table
description: "One row per completed order, conformed for finance reporting."
owner: orders-platform@example.com
steward: finance-data@example.com
domain: sales
classification: [confidential, pii-adjacent]
tags: [tier-1, finance-certified]
freshness_sla_minutes: 30
retention_days: 2555
schema:
  - {name: order_id, type: string, pii: false}
  - {name: customer_token, type: string, pii: true, policy: tokenized}
links:
  runbook: https://wiki.example.com/runbooks/fact-orders
  dashboard: https://bi.example.com/dashboards/revenue
  source_of_truth: orders-db.public.orders
```

Certification is what turns a catalog into a trust signal: mark tier-1/finance datasets as certified only after contract tests, ownership, and freshness SLAs are in place.

[Table of Contents](#Data-Governance)

## What is business glossary vs technical metadata?
A business glossary defines business terms (for example "active user", "net revenue") and their approved definitions. Technical metadata describes datasets and fields (schemas, types, partitions, lineage). Both are needed: glossary aligns meaning, technical metadata enables implementation and discovery.

```text
Business glossary item:
  term: net_revenue
  definition: gross_revenue - refunds - chargebacks, excluding tax
  owner: finance-data@example.com
  synonyms: [net sales, net bookings]
  related_assets: [gold.fact_orders, gold.revenue_daily]

Technical metadata for the same concept:
  asset: gold.revenue_daily
  column: net_revenue
  type: decimal(18,2)
  upstream: [silver.orders_current, silver.refunds_current]
  freshness: hourly
```

Interview point: glossary without technical metadata is documentation that drifts; technical metadata without a glossary is a schema nobody agrees on. Link each glossary term to the certified asset and column that implements it.

[Table of Contents](#Data-Governance)

## RBAC vs ABAC: what is the difference?
RBAC (Role-Based Access Control) grants permissions to roles (analyst, engineer) and assigns users to roles. ABAC (Attribute-Based Access Control) uses attributes (department, region, sensitivity) to evaluate policies dynamically. ABAC is more flexible but can be harder to manage without good tooling.

```text
RBAC:
  grant role analyst to user alice;
  grant select on table gold.fact_orders to role analyst;

ABAC (policy evaluated per request):
  allow if
    subject.department == resource.domain
    and subject.region == row.region
    and subject.clearance >= resource.classification
```

| Dimension | RBAC | ABAC |
|---|---|---|
| Granularity | table/schema | row, column, attribute |
| Scale | many roles, role explosion | policy count stays small |
| Audit | simple to explain | needs policy evaluation logs |
| Best for | coarse access, small orgs | multi-tenant, regional, regulated data |

Most modern lakehouses combine them: RBAC grants the base privilege, ABAC (row filters, column masks, tag policies) refines it.

[Table of Contents](#Data-Governance)

## What is row-level and column-level security?
Row-level security restricts which rows a user can see (for example only their region). Column-level security restricts which columns are visible (for example hide salary or PII). These controls are important for multi-tenant analytics and compliance.

```text
Row-level: a regional manager in APAC sees only APAC orders, even though the table
           contains global orders.
Column-level: an analyst can see customer_id but sees a masked email.
Cell-level: the combination, enforced by a row filter plus a column mask.
```

Both controls should be enforced in the query engine so that BI tools, notebooks, and ad-hoc SQL all inherit the same policy. Enforcing only in a BI tool's semantic layer leaves a hole for anyone with direct SQL access.

[Table of Contents](#Data-Governance)

## How do you implement row-level and column-level security in practice?
Unity Catalog (Databricks) example: a row filter function plus a column mask function, attached to a table.

```sql
-- Row filter: only rows for the caller's region.
create or replace function main.security.region_filter(region string)
returns boolean
return region = current_user_region();

alter table main.gold.fact_orders
set row filter main.security.region_filter on (region);

-- Column mask: show the last four digits unless the caller is in the PII group.
create or replace function main.security.mask_email(email string)
returns string
return case
  when is_account_group_member('pii_readers') then email
  else concat('***', right(email, 4))
end;

alter table main.silver.customers
alter column email set mask main.security.mask_email;
```

Snowflake example:

```sql
create or replace masking policy mask_email as (val string) returns string ->
  case
    when current_role() in ('PII_READERS') then val
    else regexp_replace(val, '(^[^@]+)@', '****@')
  end;

alter table silver.customers modify column email set masking policy mask_email;

create or replace row access policy rap_region as (region string) returns boolean ->
  region = current_role();

alter table gold.fact_orders add row access policy rap_region on (region);
```

BigQuery uses policy tags for column-level security:

```bash
bq query --use_legacy_sql=false \
  'CREATE OR REPLACE TABLE gold.fact_orders (
     order_id STRING,
     customer_email STRING OPTIONS(policy_tags=["projects/p/locations/us/taxonomies/1/policyTags/2"]),
     amount NUMERIC
   )'
```

Interview guidance: state how you test these controls (a CI test that assumes the role and asserts the filtered count) and how you audit changes (who altered a policy and when).

[Table of Contents](#Data-Governance)

## How do you handle PII/PHI data in analytics platforms?
You classify sensitive fields, minimize exposure, and enforce least privilege. Common controls include encryption, masking/tokenization, column-level access, and auditing. You also ensure downstream marts only include necessary fields and implement secure sharing patterns.

A practical layered approach:

```text
1. Discover and classify: scan for emails, national IDs, card numbers, health codes.
2. Minimize: do not land raw PII in the lake at all; tokenize at the app boundary.
3. Isolate: keep a short-retention vault table with raw PII, exempt from broad grants.
4. Protect: encryption at rest/in transit, column masks, row filters, tag-based policies.
5. Govern: retention, erasure, access reviews, and audit logs on all of the above.
6. Propagate: column-level lineage flags derived columns that still carry PII.
```

PHI adds HIPAA-style requirements on top: minimum necessary access, business associate agreements, breach notification, and stricter audit retention. In an interview, mention that PHI often requires its own catalog classification and a separate access-approval workflow rather than a self-service request.

[Table of Contents](#Data-Governance)

## What is data masking and tokenization?
Masking hides sensitive values (for example showing only last 4 digits) while keeping the dataset usable. Tokenization replaces sensitive values with tokens that can be detokenized only with access to a secure mapping. Tokenization is useful when analytics needs stable identifiers without exposing raw PII.

Comparison:

| Technique | Reversible | Stable across rows | Use case |
|---|---|---|---|
| Static masking | no | n/a | non-production copies |
| Dynamic masking | no | n/a | role-based display in production |
| Hashing (unsalted) | no | yes | joins on a pseudonymous key |
| Salted hashing / HMAC | no | yes (with same salt) | pseudonymization for analytics |
| Tokenization | yes, with vault | yes | stable key plus controlled re-identification |
| Format-preserving encryption | yes, with key | yes | payment data where format must remain valid |

Deterministic tokenization in PySpark, using HMAC so the same input always maps to the same token:

```python
import hmac
import hashlib
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

SALT = b"rotate-me-in-a-secret-manager"

def tokenize(value: str) -> str:
    if value is None:
        return None
    digest = hmac.new(SALT, value.encode("utf-8"), hashlib.sha256).hexdigest()
    return digest[:32]

tokenize_udf = F.udf(tokenize, StringType())

customers = spark.table("silver.customers").withColumn(
    "customer_token", tokenize_udf(F.col("email"))
)
```

Interview caution: unsalted `sha256(email)` is trivially reversible for a small email space via rainbow tables; always salt or HMAC. Also decide whether the token must survive a key rotation, because rotating the salt breaks historical joins.

[Table of Contents](#Data-Governance)

## How do you tag and classify data in a catalog?
Tags are the bridge between governance intent and enforcement. Classify columns with a small, controlled taxonomy rather than free-form strings.

```yaml
# classification taxonomy
classification:
  public:        {rank: 0}
  internal:      {rank: 1}
  confidential:  {rank: 2}
  restricted:    {rank: 3}   # PII, PHI, PCI, secrets

pii_categories: [email, phone, national_id, payment_card, health_record, address]

tagging_rules:
  - match: {column_name_matches: "(?i)(email|e_mail)"}
    apply: {pii_type: email, classification: restricted}
  - match: {column_name_matches: "(?i)(iban|card_number|pan|cvv)"}
    apply: {pii_type: payment_card, classification: restricted}
  - match: {column_name_matches: "(?i)(diagnosis|icd10|medication)"}
    apply: {pii_type: health_record, classification: restricted}
```

Unity Catalog tagging:

```sql
create catalog if not exists main;
create schema if not exists main.security;

alter table main.silver.customers
alter column email set tags ('pii_type' = 'email', 'classification' = 'restricted');

alter table main.gold.fact_orders set tags ('domain' = 'sales', 'tier' = '1');
```

Automate tagging from an information schema scan so new columns are classified within a day, and make unclassified `restricted`-looking columns fail a CI check.

[Table of Contents](#Data-Governance)

## How do you implement tag-based access control in Unity Catalog?
Unity Catalog ABAC policies attach governed tags to data and let a policy grant or deny access based on those tags.

```sql
-- 1. Define governed tags at the account level (done once by an account admin).
--    Example tags: classification, pii_type, domain.

-- 2. Tag data.
alter table main.silver.customers
alter column email set tags ('pii_type' = 'email');

-- 3. Create a policy: only the pii_readers group may see restricted PII columns.
create policy main.security.pii_column_policy
on catalog main
comment 'Mask PII columns for everyone except pii_readers'
as
  for select
  to all
  except (pii_readers)
  match columns with tag pii_type
  using column mask main.security.mask_email;
```

```sql
-- Row-level ABAC by governed region tag.
create policy main.security.region_rows
on schema main.gold
as
  for select
  to all
  match tables with tag domain = 'sales'
  using row filter main.security.region_filter;
```

Interview points:

+ Tags must be governed (account-level) to be trustworthy; a schema-local tag anyone can set is not a security boundary.
+ Policy evaluation happens at query time, so ad-hoc SQL, notebooks, and BI all inherit it.
+ Audit `system.access.audit` to prove who saw or changed what.

[Table of Contents](#Data-Governance)

## How do you implement Lake Formation tag-based access control?
AWS Lake Formation uses LF-Tags to express ABAC: you tag data assets and grant permissions to principals by tag expression instead of per-table grants.

```yaml
# Terraform-style sketch of LF-Tag based access control.
resource "aws_lakeformation_lf_tag" "classification" {
  key    = "classification"
  values = ["public", "internal", "confidential", "restricted"]
}

resource "aws_lakeformation_lf_tag" "pii_type" {
  key    = "pii_type"
  values = ["none", "email", "phone", "payment_card", "health_record"]
}

# Tag a table and its email column.
resource "aws_lakeformation_resource_lf_tags" "customers" {
  database { name = "silver" }
  table    { name = "customers" }
  lf_tag {
    key   = "classification"
    value = "restricted"
  }
  lf_tag {
    key   = "pii_type"
    value = "email"
  }
}

# Grant analysts access only to non-restricted, non-PII data.
resource "aws_lakeformation_permissions" "analyst_tag_grant" {
  principal   = "arn:aws:iam::111122223333:role/AnalystRole"
  permissions = ["SELECT", "DESCRIBE"]
  lf_tag_policy {
    resource_type = "TABLE"
    expression {
      key    = "classification"
      values = ["public", "internal", "confidential"]
    }
  }
}
```

Lake Formation also supports row-level and cell-level security by attaching a data filter expression and column lists to a grant. Inspect effective permissions with `aws lakeformation list-permissions` and monitor access through CloudTrail.

[Table of Contents](#Data-Governance)

## What is policy as code for data governance?
Policy as code means governance rules live in version control, are reviewed like software, and are applied by automation instead of a wiki and good intentions.

```yaml
# policies/pii_access.yaml
apiVersion: governance.example.com/v1
kind: DataPolicy
metadata:
  name: pii-read-access
spec:
  match:
    tags: {pii_type: "*"}
  rules:
    - effect: deny
      principals: {not_in_group: pii_readers}
      actions: [select, export, download]
    - effect: allow
      principals: {in_group: pii_readers}
      actions: [select]
      conditions:
        - mfa_required: true
        - purpose: [fraud_investigation, compliance]
  exceptions:
    process: access-request-ticket
    max_duration_days: 30
```

Benefits: reviewable diffs, testable policy (unit tests assert allow/deny decisions), consistent enforcement across engines, and an audit trail linking a policy version to a change window.

```python
# Unit test a policy decision before deploying it.
def evaluate(subject, action, resource_tags, policy):
    if "pii_type" in resource_tags and "pii_readers" not in subject["groups"]:
        return "deny"
    return "allow"

assert evaluate({"groups": []}, "select", {"pii_type": "email"}, {}) == "deny"
assert evaluate({"groups": ["pii_readers"]}, "select", {"pii_type": "email"}, {}) == "allow"
```

[Table of Contents](#Data-Governance)

## How do you implement auditability for data access?
You log access events (who queried what, when, from where) and retain logs per policy. You also track permission changes and administrative actions. Audit logs should be queryable for investigations and compliance reporting.

```sql
-- Unity Catalog audit events: reads, writes, and permission changes.
select
  event_time,
  user_identity.email as actor,
  action_name,
  request_params.full_name_arg as table_name,
  source_ip_address,
  response.status_code
from system.access.audit
where action_name in ('getTable', 'commandSubmit', 'updatePermissions', 'createTable')
  and event_time > current_timestamp() - interval 7 days
order by event_time desc;
```

```sql
-- Snowflake access history for a sensitive table, flattened to object names.
select
  h.query_start_time,
  h.user_name,
  o.value:objectName::string as object_name
from snowflake.account_usage.access_history as h,
     lateral flatten(input => h.direct_objects_accessed) as o
where o.value:objectName::string = 'SILVER.CUSTOMERS'
order by h.query_start_time desc
limit 100;
```

What a good audit story covers: access events, export/download events, permission changes, policy changes, retention/erasure actions, and admin actions on the account. Protect the audit log itself with restricted access and immutable storage.

[Table of Contents](#Data-Governance)

## How do you handle GDPR right to be forgotten in a lakehouse or warehouse?
You need a process to delete or anonymize personal data across raw, derived, and serving layers. This can involve targeted deletes (where supported), reprocessing from raw logs without the user, or storing personal data separately to allow deletion without rewriting large datasets. You also document what is feasible given retention and legal constraints.

```text
Erasure runbook:
1. Resolve the subject to every identifier (customer_id, email token, device id).
2. Vault: delete the raw PII mapping.
3. Raw/bronze: delete or expire affected partitions and compact so the data is gone.
4. Silver/gold: hard-delete keyed rows and rebuild aggregates that included them.
5. Downstream: purge search indexes, caches, exports, and ML feature stores.
6. Evidence: write an immutable erasure record (request id, scope, operator, timestamp).
7. Backups: rely on documented backup expiry; do not promise instant backup erasure.
```

```sql
-- Iceberg makes targeted deletes and snapshot expiry practical.
delete from main.bronze.events_raw where customer_token = :token;
delete from main.silver.customers_current where customer_token = :token;
delete from main.silver.customer_history where customer_token = :token;

-- Expire the snapshots that still reference the deleted rows.
call main.system.expire_snapshots(
  table => 'bronze.events_raw',
  older_than => timestamp '2026-10-04 00:00:00',
  retain_last => 1
);
```

Interview point: deleting a row from a table with time travel or an immutable raw log is not erasure until old snapshots and files are expired. State the retention guarantee explicitly: "new queries cannot see it immediately; physical removal completes at the next compaction/expiry, within N days."

[Table of Contents](#Data-Governance)

## What are data retention policies and how do you enforce them?
Retention policies define how long data is kept and when it must be deleted or archived. Enforcement can be implemented with partition expiry jobs, lifecycle rules on object storage, snapshot expiration, and access reviews. Retention must align with legal requirements and business needs.

```yaml
# retention matrix
retention:
  raw_events:        {days: 90, action: delete, storage_class: standard}
  pii_vault:         {days: 365, action: delete, owner: privacy@example.com}
  silver_current:    {days: 1825, action: keep, review: annual}
  gold_aggregates:   {days: 2555, action: keep, review: annual}
  audit_logs:        {days: 3650, action: archive_immutable}
  backups:           {days: 35, action: expire}
```

```sql
-- Partition expiry for a date-partitioned raw table.
alter table main.bronze.events_raw drop partition (event_date < '2026-07-01');

-- Or delete with Iceberg and then expire snapshots + orphans.
delete from main.bronze.events_raw where event_date < date '2026-07-01';
```

```bash
# S3 lifecycle rule for the raw landing zone.
aws s3api put-bucket-lifecycle-configuration \
  --bucket company-raw \
  --lifecycle-configuration file://lifecycle.json
```

Interview note: retention and erasure interact. A shorter raw retention reduces erasure surface but also shortens replay ability; state the trade-off and who owns it (usually the privacy officer plus the platform owner).

[Table of Contents](#Data-Governance)

## How do you measure data governance maturity?
Governance needs metrics, or it becomes an unenforceable policy document. Useful measures:

+ Coverage: percentage of tier-1 datasets with an owner, definition, and freshness SLA.
+ Classification: percentage of columns auto-classified, and mean time to classify a new column.
+ Access hygiene: orphan permissions, over-privileged service accounts, access reviews completed on time.
+ Contract health: CI contract checks passing, breaking-change incidents per quarter.
+ Lifecycle: datasets past retention without an exemption, erasure requests closed within SLA.
+ Trust: certified-asset count and incident count caused by unannounced schema changes.

```text
Level 1 - ad hoc: no catalog, access by ticket, definitions in chat.
Level 2 - documented: catalog and glossary exist, ownership assigned, reviews manual.
Level 3 - enforced: tags drive policies, contracts in CI, retention automated.
Level 4 - trusted: certified assets, column-level lineage, measured freshness/compliance SLAs.
Level 5 - self-improving: policy decisions measured, exceptions expire automatically, cost and risk optimized.
```

[Table of Contents](#Data-Governance)

## Real world use cases for Data Governance

### 1. E-commerce PII protection and GDPR

Business context: an online retailer with 30 million customers must let 200 analysts query orders while keeping email, phone, and address out of reach, and must honor ~500 erasure requests per month. Volume: 4 TB of order data, 40 million events/day, 8 source systems.

Architecture: raw PII lives in a short-retention vault; the lakehouse stores `customer_token`; columns are tagged `pii_type`; a Unity Catalog policy masks email for everyone except the `pii_readers` group; an erasure orchestrator deletes tokens from bronze/silver and writes an immutable audit record.

```sql
alter table main.silver.customers
alter column email set tags ('pii_type' = 'email', 'classification' = 'restricted');

create policy main.security.pii_email
on catalog main
as
  for select
  to all
  except (pii_readers)
  match columns with tag pii_type
  using column mask main.security.mask_email;
```

Why this design: tokenization at the application boundary removes raw PII from the lake entirely, so erasure is a keyed delete plus a vault operation rather than a rewrite of immutable files, and tag-driven policy means new columns inherit protection without a per-table ticket.

### 2. Fintech multi-tenant analytics with regional isolation

Business context: a payments provider serves merchants in the EU, US, and APAC from one lakehouse and must guarantee that a merchant analyst never sees another region's data and that card data is never exposed. Volume: 50 million transactions/day, 1.2 PB total, 400 tenants.

Architecture: every table carries `region` and `tenant_id`; row access policies enforce region, row filters enforce tenant, and PCI columns are masked with tokenized values; governed tags drive the policies so a new table in the schema is covered automatically.

```sql
create or replace function main.security.region_filter(region string)
returns boolean
return region = current_user_region();

alter table main.gold.transactions
set row filter main.security.region_filter on (region);

create or replace function main.security.tenant_filter(tenant_id string)
returns boolean
return tenant_id = current_user_tenant();

alter table main.gold.transactions
set row filter main.security.tenant_filter on (tenant_id);
```

Why this design: cell-level access is enforced in the engine, so notebooks, BI, and ad-hoc SQL all behave identically; tag-driven policies scale to thousands of tables without thousands of grants; and the two filters compose so tenant isolation holds even inside a shared region.

### 3. Multi-tenant SaaS data contracts in CI

Business context: a SaaS platform feeds customer-facing analytics from 2,000 tenant schemas; an unannounced upstream rename previously broke dashboards for three days. Volume: 300 million events/day, 2,000 active contracts.

Architecture: contracts live in git, are validated against the produced tables in CI, and publish to the catalog on merge; a schema registry enforces `BACKWARD` compatibility on streaming topics; contract violations block the deploy and page the producing team.

```yaml
dataset: gold.tenant_events
owner: platform-analytics@example.com
schema:
  - {name: tenant_id, type: string, required: true}
  - {name: event_name, type: string, required: true}
  - {name: occurred_at, type: timestamp, required: true}
sla: {freshness_minutes: 15}
change_policy: {breaking: requires_new_version_and_consumer_signoff}
```

Why this design: moving the agreement from a wiki into CI turns "please tell us before renaming" into a build failure, and the catalog entry means every consumer can find the owner and the contract version without asking around.

### 4. Healthcare PHI lakehouse with audit and retention

Business context: a hospital network must let researchers query de-identified records while keeping PHI access limited, auditable, and retention-bound under HIPAA. Volume: 900 million clinical rows, 15 TB, 7-year audit retention.

Architecture: PHI is separated into a restricted schema with its own access workflow; researchers query a de-identified view with date shifting and removed identifiers; every access is logged; retention jobs expire partitions and snapshots on schedule.

```python
# De-identification view logic: shift dates and drop direct identifiers.
from pyspark.sql import functions as F

deidentified = (
    spark.table("restricted.encounters")
    .select(
        F.sha2(F.col("patient_mrn"), 256).alias("patient_token"),
        F.date_sub(F.col("admit_date"), 365).alias("admit_date_shifted"),
        F.col("diagnosis_code"),
        F.col("facility_id"),
    )
)
```

Why this design: researchers never touch the restricted schema, date shifting prevents re-identification by cross-referencing public records, and the immutable audit log plus retention automation is what satisfies the compliance review rather than a policy PDF.

### 5. Marketplace catalog and lineage-driven deprecation

Business context: an acquired company's data must be merged into the parent catalog, and 300 legacy tables must be deprecated without breaking reports. Volume: 12,000 tables, 400,000 columns, 5,000 dashboards.

Architecture: automated profiling classifies and describes every table; column-level lineage maps dashboard fields to source columns; each legacy table gets an owner, a deprecation date, and a redirect to its replacement; a weekly report shows remaining consumers.

```sql
select
  t.table_name,
  count(distinct l.target_table_full_name) as downstream_assets,
  max(l.event_time) as last_used
from system.information_schema.tables t
left join system.access.column_lineage l
  on l.source_table_full_name = concat_ws('.', t.table_catalog, t.table_schema, t.table_name)
where t.table_schema = 'legacy'
group by t.table_name
order by downstream_assets desc;
```

Why this design: lineage turns deprecation from guesswork into evidence, ownership makes someone accountable for each retirement, and the weekly consumer report gives holdouts a deadline instead of an accidental outage.

[Table of Contents](#Data-Governance)
