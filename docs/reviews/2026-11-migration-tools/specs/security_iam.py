import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# Security and IAM for data pipelines

An orders pipeline runs in Airflow, reads from a Postgres replica, writes to S3, and loads Snowflake, where
analysts query it. Each hop is an **identity** using a **permission**: the scheduler's service account, a role it
assumes, the storage policy, the warehouse role. A breach, or an analyst seeing card numbers they should not, almost
always comes from one of those hops being broader than it needed to be.

This lesson follows identity through a pipeline: how cloud IAM policies are evaluated, how to cut a policy down to
least privilege from real usage, short-lived credentials and role assumption, secrets that stay out of code and
logs, pseudonymizing personal data, row- and column-level security in the warehouse, and reading an access log.
Policy evaluation and credentials are modeled in Python; the warehouse controls run in DuckDB.

*Last reviewed: November 2026, against the AWS IAM, Google Cloud IAM and Microsoft Entra documentation.*

**Prerequisites:** [Data governance](data-governance.ipynb) for ownership and classification.
%% code
# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
!pip install -q duckdb~=2.0
%% md
## Setup and sample data

The cell defines the pipeline's identities and the AWS-style policy attached to the loader role, and creates a
`customers` table with personal data in DuckDB for the warehouse sections.
%% code
import fnmatch
import hashlib
import hmac
import logging
import re
from datetime import datetime, timedelta

import duckdb

LOADER_POLICY = {
    "Statement": [
        {"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"], "Resource": ["arn:aws:s3:::lake/*", "arn:aws:s3:::lake"]},
        {"Effect": "Allow", "Action": ["s3:*"], "Resource": ["arn:aws:s3:::lake-tmp/*"]},
        {"Effect": "Deny", "Action": ["s3:*"], "Resource": ["arn:aws:s3:::lake/pii/*"],
         "Condition": {"StringNotEquals": {"aws:PrincipalTag/team": "privacy"}}},
    ]
}

con = duckdb.connect()
con.sql("""
create table customers as select * from (values
    (1, 'Ana Diaz',   'ana@example.com',   '4111111111111111', 'EU', 'smb'),
    (2, 'Ben Okafor', 'ben@example.com',   '5500000000000004', 'US', 'enterprise'),
    (3, 'Chen Wei',   'chen@example.com',  '340000000000009',  'EU', 'enterprise'),
    (4, 'Dana Levi',  'dana@example.com',  '6011000000000004', 'US', 'smb')
) t(customer_id, name, email, card_number, region, segment)
""")
print("roles: scheduler -> loader (S3), loader -> warehouse_loader (Snowflake), analysts_eu / analysts_us")
%% md
## Follow the identity through the pipeline

Every action in a pipeline is taken by some identity, and each identity should be able to do exactly its job:

| Hop | Identity | Should be able to |
|---|---|---|
| Scheduler | Airflow's service account / workload identity | Assume the loader role; nothing else |
| Extract | A read-only database user on the replica | `select` on the tables it extracts |
| Land | Loader role | Write `s3://lake/raw/orders/*` |
| Load | Warehouse loader role | `insert`, `merge` into staging and marts |
| Query | Analyst roles | `select` on marts, masked personal data |

Humans and services get **separate identities**, services never use a person's keys, and permissions are granted to
**roles or groups**, not to individuals.

**Where it matters**
- Designing a new pipeline, and every access review.

**Watch out for**
- One "etl" service account used by every job: a leak or a bug in one job reaches everything.
%% md
## How a cloud policy is evaluated

Cloud IAM policies are lists of statements: an **effect** (allow or deny), **actions**, **resources**, and optional
**conditions**. AWS evaluates a request like this: everything is **denied by default**; an **explicit deny**
anywhere wins; otherwise, an **allow** that matches action, resource and conditions permits it. Google Cloud and
Azure differ in syntax (roles bound to members on a resource hierarchy) but share the shape: default deny, allows
that add up, denies that override.

**Where it matters**
- Reading a policy someone wrote and knowing what it actually allows.

**Watch out for**
- Wildcards (`s3:*`, `Resource: "*"`) that grant far more than the job needs, including delete and permission changes.
%% md
### Evaluate requests against the loader's policy

`evaluate` implements default deny, wildcard matching, conditions on principal tags and explicit-deny-wins.
%% code
def matches(patterns, value):
    return any(fnmatch.fnmatchcase(value, p) for p in patterns)


def condition_holds(condition, context):
    for operator, pairs in (condition or {}).items():
        for key, expected in pairs.items():
            actual = context.get(key)
            if operator == "StringEquals" and actual != expected:
                return False
            if operator == "StringNotEquals" and actual == expected:
                return False
    return True


def evaluate(policy, action, resource, context=None):
    """'Deny' if any matching Deny, else 'Allow' if any matching Allow, else 'ImplicitDeny'."""
    context = context or {}
    decision = "ImplicitDeny"
    for statement in policy["Statement"]:
        if matches(statement["Action"], action) and matches(statement["Resource"], resource) and condition_holds(statement.get("Condition"), context):
            if statement["Effect"] == "Deny":
                return "Deny"
            decision = "Allow"
    return decision


requests = [
    ("s3:PutObject", "arn:aws:s3:::lake/raw/orders/2026-03-02.parquet", {"aws:PrincipalTag/team": "orders"}),
    ("s3:DeleteObject", "arn:aws:s3:::lake/raw/orders/2026-03-02.parquet", {"aws:PrincipalTag/team": "orders"}),
    ("s3:DeleteObject", "arn:aws:s3:::lake-tmp/scratch/x.csv", {"aws:PrincipalTag/team": "orders"}),
    ("s3:GetObject", "arn:aws:s3:::lake/pii/customers.parquet", {"aws:PrincipalTag/team": "orders"}),
    ("s3:GetObject", "arn:aws:s3:::lake/pii/customers.parquet", {"aws:PrincipalTag/team": "privacy"}),
]
for action, resource, context in requests:
    print(f"{evaluate(LOADER_POLICY, action, resource, context):12} {action:16} {resource.split(':::')[1]:38} team={context['aws:PrincipalTag/team']}")
%% md
**What to notice:** Writing raw orders is allowed, deleting them is an implicit deny (no statement allows it), and
anything in `lake-tmp` is allowed because of `s3:*`. Reading `lake/pii/` is allowed by the first statement but
explicitly denied unless the caller is tagged `team=privacy`: the deny wins for the orders team, and the condition
lets the privacy team through.
%% md
## Least privilege from real usage

Policies grow by accretion: someone adds `s3:*` to get a job working and nobody removes it. The fix is evidence:
compare what a role is **granted** with what it **used** over a few weeks of access logs (CloudTrail, Cloud Audit
Logs, Azure activity logs), then replace wildcards with the actions and resources actually used. Cloud tools do
this for you (IAM Access Analyzer policy generation, GCP role recommendations).

**Where it matters**
- Access reviews and incident follow-ups.

**Watch out for**
- Narrowing from too short a window: a monthly job's permissions look unused after two weeks.
%% md
### Narrow a policy from an access log

Thirty days of the loader's log entries, summarized. Which granted actions were never used?
%% code
access_log = [
    ("s3:PutObject", "arn:aws:s3:::lake/raw/orders/2026-02-01.parquet"),
    ("s3:PutObject", "arn:aws:s3:::lake/raw/orders/2026-03-01.parquet"),
    ("s3:ListBucket", "arn:aws:s3:::lake"),
    ("s3:PutObject", "arn:aws:s3:::lake-tmp/stage/batch.csv"),
    ("s3:DeleteObject", "arn:aws:s3:::lake-tmp/stage/batch.csv"),
]
granted = {(a, r) for s in LOADER_POLICY["Statement"] if s["Effect"] == "Allow" for a in s["Action"] for r in s["Resource"]}
used_actions = sorted({a for a, _ in access_log})
print("granted action patterns:", sorted({a for a, _ in granted}))
print("actions used:           ", used_actions)
unused = sorted({a for a, _ in granted if not any(fnmatch.fnmatchcase(u, a) for u in used_actions)})
print("granted but never used: ", unused)

prefixes = sorted({re.sub(r"[^/]+$", "*", r) if "/" in r.split(":::")[1] else r for _, r in access_log})
print("narrowed resources:     ", prefixes)
%% md
**What to notice:** `s3:GetObject` was granted on the whole lake and never used, and `s3:*` on `lake-tmp` was used
only for put and delete. The resources actually touched were two prefixes and the bucket listing, so a narrowed
policy grants `PutObject` on `lake/raw/orders/*`, `PutObject` and `DeleteObject` on `lake-tmp/stage/*` and
`ListBucket` on `lake`, instead of the whole lake.
%% md
## Short-lived credentials and role assumption

Long-lived access keys leak: in a notebook, a log, a Docker image. Modern pipelines use **short-lived credentials**
obtained by **assuming a role**: the scheduler proves who it is (a workload identity, an OIDC token from GitHub
Actions or Kubernetes) and receives credentials that expire in an hour. The role's **trust policy** says who may
assume it; its permission policy says what it may do.

**Where it matters**
- CI/CD deploying to the cloud, and jobs on Kubernetes or serverless platforms.

**Watch out for**
- Trust policies that let any identity in an account (or any GitHub repository) assume a role: always pin the subject.
%% md
### Assume a role, then use expired credentials

`assume_role` checks the trust policy and issues credentials valid for one hour. The job then uses them, and again
after they expire.
%% code
TRUST = {"loader": {"repo:shop/pipelines:ref:refs/heads/main", "system:serviceaccount:airflow:scheduler"}}


def assume_role(role, subject, now):
    if subject not in TRUST[role]:
        raise PermissionError(f"{subject} may not assume {role}")
    return {"role": role, "expires": now + timedelta(hours=1)}


def call(credentials, now):
    return "ok" if now < credentials["expires"] else "ExpiredToken: refresh by assuming the role again"


start = datetime(2026, 3, 2, 2, 0)
creds = assume_role("loader", "system:serviceaccount:airflow:scheduler", start)
print("02:30", call(creds, start + timedelta(minutes=30)))
print("03:05", call(creds, start + timedelta(minutes=65)))
for subject in ["repo:shop/pipelines:ref:refs/heads/feature-x", "repo:someone/fork:ref:refs/heads/main"]:
    try:
        assume_role("loader", subject, start)
    except PermissionError as error:
        print("denied:", error)
%% md
**What to notice:** The credentials worked at 02:30 and failed at 03:05, so a leaked copy is useless an hour later
and a long job must refresh them. The trust policy accepted only the Airflow scheduler and the `main` branch of one
repository; a feature branch and a fork with a `main` branch were both refused.
%% md
## Secrets stay out of code and logs

Database passwords and API tokens belong in a **secret manager** (AWS Secrets Manager, Google Secret Manager, Azure
Key Vault, Vault) or the orchestrator's connections, injected at run time as environment variables or fetched by
the job. They never go in code, notebooks, Docker images or configuration in Git. Logs are the other leak: a
connection string or a request dump prints the password.

**Where it matters**
- Every job with a credential, and every log line that includes a URL or a config object.

**Watch out for**
- Secrets committed once and "removed" later: they stay in Git history; rotate them.
%% md
### Redact secrets from log output

A logging filter masks passwords in URLs and token-like values before a record is written.
%% code
class RedactSecrets(logging.Filter):
    patterns = [(re.compile(r"(://[^:/]+:)[^@]+(@)"), r"\1****\2"), (re.compile(r"(token|api_key|password)=\S+", re.I), r"\1=****")]

    def filter(self, record):
        message = record.getMessage()
        for pattern, replacement in self.patterns:
            message = pattern.sub(replacement, message)
        record.msg, record.args = message, ()
        return True


log = logging.getLogger("loader")
log.handlers.clear()
handler = logging.StreamHandler(__import__("sys").stdout)
handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
handler.addFilter(RedactSecrets())
log.addHandler(handler)
log.setLevel(logging.INFO)

log.info("connecting to %s", "postgresql://loader:S3cr3t!@replica.internal:5432/shop")
log.info("calling https://api.partner.example/orders?since=2026-03-01&api_key=abc123xyz")
%% md
**What to notice:** The password in the connection string and the API key in the URL were replaced with `****`
before the records were written, while the rest of each line stayed readable for debugging. Redaction is a safety
net; the first defence is not logging secrets at all.
%% md
## Pseudonymize personal data

Analytics rarely needs the actual email or card number; it needs to count, join and deduplicate people. A **keyed
hash** (HMAC with a secret key) turns an identifier into a stable pseudonym: the same email always gives the same
token, so joins still work, but without the key nobody can recompute it from a list of known emails, which a plain
SHA-256 allows. **Tokenization** with a lookup vault is the reversible alternative, for the few processes that must
recover the real value.

**Where it matters**
- Lake and warehouse tables that analysts and data scientists use.

**Watch out for**
- Unkeyed hashes of low-entropy values (emails, phone numbers): a dictionary attack reverses them in seconds.
%% md
### Compare a plain hash with a keyed one

An attacker has a list of likely emails. Can they find which customer a pseudonym belongs to?
%% code
secret_key = b"from-the-secret-manager"  # in production: fetched at run time, rotated, never in code


def plain_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()[:16]


def keyed_hash(value):
    return hmac.new(secret_key, value.encode(), hashlib.sha256).hexdigest()[:16]


emails = [r[0] for r in con.sql("select email from customers order by customer_id").fetchall()]
plain = {plain_hash(e): e for e in emails}
keyed = {keyed_hash(e): e for e in emails}
attacker_guesses = ["ben@example.com", "zoe@example.com"]
print("plain hash reversed:", [plain.get(plain_hash(g)) for g in attacker_guesses])
print("keyed hash reversed:", [keyed.get(plain_hash(g)) for g in attacker_guesses])
print("stable for joins:   ", keyed_hash("ben@example.com") == keyed_hash("ben@example.com"))
%% md
**What to notice:** With plain SHA-256 the attacker hashed their guesses and matched `ben@example.com`. With the
keyed hash their guesses match nothing, because they cannot compute the HMAC without the key. The pseudonym is
still identical every time, so tables can be joined on it.
%% md
## Row- and column-level security in the warehouse

Inside the warehouse, access is decided per role on schemas, tables, rows and columns. **Row access policies** keep
only the rows a role may see (EU analysts see EU customers); **masking policies** replace a column's value for roles
that should not see it (the last four digits of a card). Snowflake, BigQuery, Databricks and Redshift all offer
both as policies attached to the table, so every query and tool gets the same rules.

**Where it matters**
- Regional data-residency rules, PII, and multi-tenant data products.

**Watch out for**
- Implementing security in each dashboard's filter: anyone with SQL access bypasses it.
%% md
### Build a secure view keyed on the current role

DuckDB has no roles, so a session variable stands in for the current role. The view filters rows by region and masks
the email and card for everyone except the privacy role.
%% code
con.sql("""
create table role_regions as select * from (values ('analysts_eu', 'EU'), ('analysts_us', 'US'),
    ('privacy', 'EU'), ('privacy', 'US')) t(role, region);

create view customers_secure as
select customer_id,
       name,
       case when getvariable('current_role') = 'privacy' then email
            else regexp_replace(email, '^[^@]+', '***') end as email,
       case when getvariable('current_role') = 'privacy' then card_number
            else '**** ' || right(card_number, 4) end as card_number,
       region, segment
from customers
where region in (select region from role_regions where role = getvariable('current_role'))
""")
for role in ["analysts_eu", "analysts_us", "privacy"]:
    con.sql(f"set variable current_role = '{role}'")
    print(role)
    con.sql("select * from customers_secure order by customer_id").show()
%% md
**What to notice:** The EU analyst saw only customers 1 and 3, with emails reduced to `***@example.com` and cards to
their last four digits. The US analyst saw customers 2 and 4 with the same masking. The privacy role saw all four
customers unmasked. The rules live in one view; in a real warehouse they would be row access and masking policies
on the table itself, and analysts would have no grant on the base table.
%% md
## Read the access log

Every cloud and warehouse records who accessed what (CloudTrail, Cloud Audit Logs, Snowflake's `access_history`,
Unity Catalog audit logs). Use it to answer "who read this table" during an incident, and alert on patterns that
should not happen: a service account used from a laptop, a human reading a PII table at 03:00, a role suddenly
reading a hundred times more rows.

**Where it matters**
- Incident response, compliance audits, and detecting compromised credentials.

**Watch out for**
- Logs nobody reads: decide the few alerts that matter and route them to an owner.
%% md
### Flag unusual access

A day of access records. Flag PII reads outside working hours and service identities used from outside the platform.
%% code
con.sql("""
create table access_history as select * from (values
    (timestamp '2026-03-02 02:05', 'svc_loader',  'service', 'k8s',    'raw.orders',        12000),
    (timestamp '2026-03-02 09:30', 'ana',         'human',   'laptop', 'marts.revenue',       400),
    (timestamp '2026-03-02 03:12', 'ben',         'human',   'laptop', 'pii.customers',     50000),
    (timestamp '2026-03-02 14:00', 'svc_loader',  'service', 'laptop', 'raw.orders',          10),
    (timestamp '2026-03-02 11:00', 'privacy_bot', 'service', 'k8s',    'pii.customers',       200)
) t(ts, identity, kind, origin, object, rows_read)
""")
con.sql("""
select ts, identity, object, rows_read,
       case when kind = 'human' and object like 'pii.%' and hour(ts) not between 7 and 19 then 'PII read outside hours'
            when kind = 'service' and origin <> 'k8s' then 'service identity used outside the platform' end as alert
from access_history
where alert is not null
order by ts
""").show()
%% md
**What to notice:** Two records stand out: a person reading 50,000 rows of `pii.customers` at 03:12, and the loader's
service identity used from a laptop, which suggests its credentials were copied. The service reading PII at 11:00
from the platform is expected and not flagged.
%% md
## The same ideas in each cloud

| Concept | AWS | Google Cloud | Azure |
|---|---|---|---|
| Identity for services | IAM roles (assumed) | Service accounts | Managed identities (Entra ID) |
| Federation from CI / Kubernetes | OIDC identity providers, IRSA / Pod Identity | Workload Identity Federation | Workload identity federation |
| Policy model | Identity and resource policies, SCPs | Role bindings on the resource hierarchy, deny policies | Role assignments (RBAC) on scopes |
| Fine-grained data access | Lake Formation, Redshift RLS/masking | BigQuery row access and policy tags | Purview, Fabric/Synapse RLS |
| Keys and secrets | KMS, Secrets Manager | Cloud KMS, Secret Manager | Key Vault |
| Audit | CloudTrail | Cloud Audit Logs | Activity and resource logs |

Encryption at rest with provider-managed keys is the default everywhere; customer-managed keys add control over
rotation and revocation at an operational cost. Encryption in transit (TLS) should be required on every connection,
including inside a VPC.

**Where it matters**
- Translating a design between clouds, and reading a security review.

**Watch out for**
- Assuming network isolation replaces identity checks: inside a VPC every request still needs least-privilege identity.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** A policy allows `s3:*` on `lake/*` and another statement denies `s3:GetObject` on `lake/pii/*`. Can the role read `lake/pii/x`?

**A.** No. An explicit deny overrides any allow. It can still do everything else `s3:*` grants on `lake/pii/*`, which is a reason to avoid wildcards.

**Q2.** Why are short-lived credentials from role assumption safer than access keys?

**A.** They expire within an hour, so a leaked copy is soon useless, and the trust policy controls exactly which workloads can obtain them. Access keys work until someone notices and revokes them.

**Q3.** Why is `sha256(email)` not a safe pseudonym?

**A.** Emails are guessable, so an attacker hashes a list of candidates and matches them. A keyed hash (HMAC) with a secret key prevents this while staying stable for joins.

**Q4.** Where should row-level security be enforced, and why not in the dashboard?

**A.** In the warehouse, as a policy on the table or a secure view, so every tool and every SQL query gets the same rules. A dashboard filter is bypassed by anyone who can query the table.

**Q5.** How do you find which permissions a role can safely lose?

**A.** Compare granted actions and resources with those used in access logs over a window long enough to include periodic jobs, then replace wildcards with what was used.
%% md
## Key takeaways

- Every hop of a pipeline is an identity; give each its own, granted through roles, with only the permissions its job needs.
- Cloud policies deny by default, allows add up, and an explicit deny always wins.
- Narrow permissions from access logs; replace wildcards with the actions and resources actually used.
- Prefer short-lived credentials from role assumption with tightly pinned trust policies.
- Keep secrets in a secret manager and out of logs; pseudonymize personal data with keyed hashes.
- Enforce row and column rules in the warehouse, and watch the access log for patterns that should not happen.
%% md
**Next:** Continue with [Data governance](data-governance.ipynb) for ownership, classification and access reviews,
or [CI/CD and infrastructure as code](cicd-and-iac.ipynb) for deploying these policies as code.
'''

build("notebooks/topics/concepts/security-and-iam.ipynb", SPEC)
