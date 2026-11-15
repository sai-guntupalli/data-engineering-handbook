import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# CI/CD and infrastructure as code for data

A pull request changes how `fct_orders` treats refunds. The unit tests pass. It is merged, deployed at 17:00, and the
next morning the revenue dashboard is 4% lower and a downstream team's job fails because a column was renamed.
Application CI asks "does the code work?"; data CI must also ask "what does this change do to the **data** and to
the **people who read it**?", and data deployment must never leave consumers looking at a half-built table.

This lesson builds the checks a data pipeline's CI should run, in DuckDB: unit tests for transformations, schema
contract checks, a data diff between production and the pull request's build, and a write-audit-publish deployment
that swaps tables atomically. It then reads an infrastructure-as-code plan to block destructive changes, and shows a
complete CI workflow.

*Last reviewed: November 2026, against the dbt, Terraform and GitHub Actions documentation.*

**Prerequisites:** [Python 7: errors, logging and testing](../python/learning/python-07-errors-logging-and-testing.ipynb)
and [Data modeling 9: testing, metrics and change](../data-modeling/data-modeling-09-testing-metrics-and-change.ipynb).
%% code
# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
!pip install -q duckdb~=2.0
%% md
## Setup and sample data

The cell creates a `raw_orders` source table, and a `prod` schema holding the current production build of the
`fct_orders` model. The pull request's version of the model is defined later.
%% code
import json
import re

import duckdb

con = duckdb.connect()
con.sql("""
create table raw_orders as select * from (values
    (1, 'C1', 'complete',  120.00,  0.00), (2, 'C2', 'complete',  300.00, 40.00),
    (3, 'C1', 'cancelled', 110.00,  0.00), (4, 'C3', 'complete',  250.00,  0.00),
    (5, 'C4', 'complete',  485.50, 30.00), (6, 'C2', 'complete',  200.00,  0.00)
) t(order_id, customer_id, status, amount, refund);

create schema prod;
create table prod.fct_orders as
select order_id, customer_id, amount as revenue
from raw_orders where status = 'complete';
""")
con.sql("select * from prod.fct_orders order by order_id").show()
%% md
## What CI/CD means for data

| Stage | Application CI | Data CI adds |
|---|---|---|
| Lint and compile | Code style, types | SQL lint (sqlfluff), model compiles against the warehouse |
| Unit tests | Functions on fixtures | Transformations on small fixture tables |
| Integration | Services together | Build changed models (and their children) in an isolated schema |
| Impact | — | Schema contract checks, data diff against production |
| Deploy | Roll out new code | Build, audit, then swap tables atomically; backfill if needed |
| Infrastructure | Terraform plan | Same, plus guarding buckets, databases and grants from deletion |

Environments matter more for data than for code: a dev build must read production-like inputs but never write to
production tables. Tools such as dbt do this with a target schema per developer and per pull request, and
**deferral** (`--defer --state prod-manifest`), which builds only changed models and reads unchanged parents from
production.

**Where it matters**
- Every repository of SQL models or pipeline code with more than one contributor.

**Watch out for**
- CI that only compiles: a model can compile and still double revenue.
%% md
## Unit test transformations

Write the transformation as a function of its inputs (here, a SQL query over named tables), feed it small fixture
tables covering the edge cases, and compare the output with the expected rows. Each test states one rule: cancelled
orders are excluded, refunds reduce revenue, a customer with no orders does not appear.

**Where it matters**
- Logic changes such as the refund rule in this pull request.

**Watch out for**
- Fixtures copied from production: they are large, hide the case being tested, and may contain personal data.
%% md
### Test the pull request's model on fixtures

The pull request's model subtracts refunds. The tests run it on a fixture and report each rule. The second version
contains a bug: it subtracts the refund twice.
%% code
PR_MODEL = """
select order_id, customer_id, amount - refund as revenue
from {source} where status = 'complete'
"""
BUGGY_MODEL = """
select order_id, customer_id, amount - 2 * refund as revenue
from {source} where status = 'complete'
"""


def build_model(sql, source_rows):
    con.sql("create or replace temp table fixture as select * from (values " + ", ".join(source_rows) + ") t(order_id, customer_id, status, amount, refund)")
    return {row[0]: row[2] for row in con.sql(sql.format(source="fixture")).fetchall()}


def test_cancelled_orders_are_excluded(model):
    out = build_model(model, ["(1, 'A', 'complete', 10.0, 0.0)", "(2, 'A', 'cancelled', 99.0, 0.0)"])
    assert set(out) == {1}, out


def test_refunds_reduce_revenue(model):
    out = build_model(model, ["(1, 'A', 'complete', 100.0, 30.0)"])
    assert out[1] == 70.0, out


def test_full_refund_gives_zero(model):
    out = build_model(model, ["(1, 'A', 'complete', 50.0, 50.0)"])
    assert out[1] == 0.0, out


def run_tests(model, label):
    results = []
    for test in [test_cancelled_orders_are_excluded, test_refunds_reduce_revenue, test_full_refund_gives_zero]:
        try:
            test(model)
            results.append(f"PASS {test.__name__}")
        except AssertionError as error:
            results.append(f"FAIL {test.__name__}: got {error}")
    print(label)
    print("\n".join("  " + r for r in results))


run_tests(PR_MODEL, "pull request model")
run_tests(BUGGY_MODEL, "buggy model")
%% md
**What to notice:** The pull request's model passes all three rules. The buggy version still excludes cancelled
orders, but returns 40.0 instead of 70.0 for a 30.00 refund and -50.0 for a full refund, so CI fails with the actual
values in the message. In a repository these functions live in `tests/` and pytest runs them; the `assert` inside a
test is the test itself.
%% md
## Check schema contracts

Downstream jobs and dashboards depend on a model's **columns and types**: its contract. Some changes are safe for
consumers (adding a column, widening `int` to `bigint`); others break them (removing or renaming a column, narrowing
a type, changing what a column means). CI should compare the new schema with the published contract and block
breaking changes unless the model is versioned (`fct_orders_v2`) with a deprecation period for the old version.
dbt enforces declared contracts with `contract: {enforced: true}`.

**Where it matters**
- Shared models that other teams build on.

**Watch out for**
- Semantic changes with the same schema: a column that changes from gross to net revenue passes the schema check.
  Rename it or version the model.
%% md
### Compare the pull request's schema with the contract

The contract is the production schema. A second candidate renames `revenue` to `net_revenue` and adds `refund`.
%% code
def schema_of(sql):
    return {row[0]: row[1] for row in con.sql(f"describe {sql}").fetchall()}


def widens(old, new):
    """True for safe widenings: INTEGER -> BIGINT, or DECIMAL(p,s) -> DECIMAL(p2,s) with p2 > p."""
    if (old, new) in {("INTEGER", "BIGINT"), ("FLOAT", "DOUBLE")}:
        return True
    a, b = re.fullmatch(r"DECIMAL\((\d+),(\d+)\)", old), re.fullmatch(r"DECIMAL\((\d+),(\d+)\)", new)
    return bool(a and b and a[2] == b[2] and int(b[1]) >= int(a[1]))


def contract_changes(contract, candidate):
    breaking = [f"removed {c}" for c in contract if c not in candidate]
    changed = [c for c in contract if c in candidate and candidate[c] != contract[c]]
    breaking += [f"type of {c}: {contract[c]} -> {candidate[c]}" for c in changed if not widens(contract[c], candidate[c])]
    additive = [f"added {c}" for c in candidate if c not in contract]
    additive += [f"widened {c}: {contract[c]} -> {candidate[c]}" for c in changed if widens(contract[c], candidate[c])]
    return breaking, additive


contract = schema_of("select * from prod.fct_orders")
candidates = {
    "subtract refunds": PR_MODEL.format(source="raw_orders"),
    "rename and add": "select order_id, customer_id, amount - refund as net_revenue, refund from raw_orders where status = 'complete'",
}
print("contract:", contract)
for name, sql in candidates.items():
    breaking, additive = contract_changes(contract, schema_of(sql))
    print(f"{name:17} breaking={breaking} additive={additive} -> {'BLOCK' if breaking else 'ok'}")
%% md
**What to notice:** Subtracting refunds kept the same columns, but `revenue` changed type from `DECIMAL(5,2)` to
`DECIMAL(6,2)`: DuckDB gives the result of a subtraction one more digit. Nobody intended that, and the check found
it; it classifies a wider precision with the same scale as a safe widening, so the change passes. The check cannot see
that the *meaning* of `revenue` changed, which is why the data diff below matters. Renaming `revenue` to
`net_revenue` removes a column consumers depend on and is blocked.
%% md
## Diff the data

A **data diff** builds the changed model from production inputs and compares it with the production table by
primary key: rows added, removed and changed, and how much each important measure moves. Posted on the pull request,
it shows reviewers the impact in numbers ("revenue changes on 2 of 5 rows, total -70.00") before anything is
deployed. Tools: `datafold`/`data-diff`, `dbt-audit-helper`, SQLMesh's table diff, or a query like the one below.

**Where it matters**
- Reviewing any logic change to an important model.

**Watch out for**
- Diffing on a sample: rare cases are exactly what a diff should catch; diff by key on the full table, or at least on
  a full recent partition.
%% md
### Diff production with the pull request's build

Build the pull request's model into a `ci` schema and compare it with `prod.fct_orders` by `order_id`.
%% code
con.sql("create schema ci")
con.sql(f"create table ci.fct_orders as {PR_MODEL.format(source='raw_orders')}")
diff = con.sql("""
select coalesce(p.order_id, c.order_id) as order_id,
       case when p.order_id is null then 'added' when c.order_id is null then 'removed'
            when p.revenue <> c.revenue then 'changed' else 'same' end as change,
       p.revenue as prod_revenue, c.revenue as ci_revenue
from prod.fct_orders p full join ci.fct_orders c using (order_id)
""")
diff.filter("change <> 'same'").order("order_id").show()
summary = con.sql("""
select count(*) filter (where change = 'changed') as changed_rows, count(*) as rows,
       sum(ci_revenue) - sum(prod_revenue) as revenue_delta
from diff
""").fetchall()[0]
print(f"PR comment: revenue changes on {summary[0]} of {summary[1]} orders; total {summary[2]:+.2f}")
%% md
**What to notice:** Only orders 2 and 5 change, by their refunds of 40.00 and 30.00; no rows are added or removed,
and total revenue falls by 70.00. That one line on the pull request is what tells the finance team their dashboard
will move, before it moves.
%% md
## Deploy with write, audit, publish

Never build a model in place where consumers read it: they would see an empty or half-built table, and a failed
build would leave it broken. Instead **write** the new version beside the old one, **audit** it (row counts,
uniqueness, not-null, reconciliation with the source), and **publish** with one atomic step: a rename, a view swap,
`create or replace` in a transaction, Snowflake's `swap with`, or moving a table-format branch. If the audit fails,
production is untouched.

**Where it matters**
- Every scheduled build of a table people read, not only deployments.

**Watch out for**
- Publishing with `drop` followed by `create`: between the two statements the table does not exist.
%% md
### Publish only an audited build

`deploy` builds into a staging table, audits it, and swaps it into production in one transaction. The second call
deploys a broken model that duplicates rows.
%% code
def audit(table):
    problems = []
    rows, keys, nulls = con.sql(f"select count(*), count(distinct order_id), count(*) filter (where revenue is null) from {table}").fetchall()[0]
    if rows != keys:
        problems.append(f"{rows - keys} duplicate order_id")
    if nulls:
        problems.append(f"{nulls} null revenue")
    if rows == 0:
        problems.append("no rows")
    return problems


def deploy(model_sql):
    con.sql(f"create or replace table prod.fct_orders__staging as {model_sql}")
    problems = audit("prod.fct_orders__staging")
    if problems:
        con.sql("drop table prod.fct_orders__staging")
        return f"not published: {problems}"
    con.begin()
    con.sql("drop table prod.fct_orders")
    con.sql("alter table prod.fct_orders__staging rename to fct_orders")
    con.commit()
    return "published"


broken = PR_MODEL.format(source="raw_orders") + " union all select 2, 'C2', 260.00"
print("broken model:", deploy(broken))
print("prod revenue:", con.sql("select sum(revenue) from prod.fct_orders").fetchall()[0][0])
print("PR model:    ", deploy(PR_MODEL.format(source="raw_orders")))
print("prod revenue:", con.sql("select sum(revenue) from prod.fct_orders").fetchall()[0][0])
%% md
**What to notice:** The broken build duplicated order 2; the audit caught it, the staging table was dropped, and
production kept its revenue of 1,355.50. The pull request's build passed the audit and was swapped in inside one
transaction, so readers saw either the old table or the new one with 1,285.50, never neither.
%% md
## Infrastructure as code

Buckets, warehouses, databases, roles, grants and the orchestrator itself should be declared in code (Terraform or
OpenTofu, Pulumi, CloudFormation, Bicep) and changed through pull requests, like models. CI runs `terraform plan`
and shows reviewers exactly what will be created, changed or **destroyed**. For data, the dangerous changes are the
ones that delete or replace stateful resources: a renamed bucket is a new, empty bucket and a deleted old one.

```hcl
resource "aws_s3_bucket" "lake" {
  bucket = "shop-lake-prod"
  lifecycle { prevent_destroy = true }   # refuse any plan that would delete it
}

resource "snowflake_grant_privileges_to_account_role" "analysts_read" {
  account_role_name = "ANALYSTS"
  privileges        = ["SELECT"]
  on_schema_object { all { object_type_plural = "TABLES", in_schema = "\"SHOP\".\"MARTS\"" } }
}
```

**Where it matters**
- Reproducible environments, reviewable permission changes, and disaster recovery.

**Watch out for**
- Changes made by hand in the console: the next `apply` reverts them, or the drift hides a security hole.
%% md
### Block a plan that destroys stateful resources

`terraform show -json plan.out` lists each resource change with its actions. The cell checks a plan of that shape
(an example written for this lesson) and blocks deletes and replacements of stateful resource types.
%% code
plan = json.loads("""
{"resource_changes": [
  {"address": "aws_s3_bucket.lake", "type": "aws_s3_bucket", "change": {"actions": ["delete", "create"]}},
  {"address": "aws_iam_role_policy.loader", "type": "aws_iam_role_policy", "change": {"actions": ["update"]}},
  {"address": "snowflake_warehouse.transform", "type": "snowflake_warehouse", "change": {"actions": ["update"]}},
  {"address": "snowflake_database.analytics", "type": "snowflake_database", "change": {"actions": ["delete"]}},
  {"address": "aws_glue_job.compact", "type": "aws_glue_job", "change": {"actions": ["create"]}}
]}
""")
STATEFUL = {"aws_s3_bucket", "snowflake_database", "snowflake_schema", "snowflake_table", "aws_db_instance", "google_bigquery_dataset"}

blocked = []
for change in plan["resource_changes"]:
    actions = change["change"]["actions"]
    kind = "replace" if actions == ["delete", "create"] else "/".join(actions)
    flag = change["type"] in STATEFUL and "delete" in actions
    blocked += [change["address"]] if flag else []
    print(f"{kind:8} {change['address']:34} {'BLOCK: stateful resource would be deleted' if flag else ''}")
print("plan", "blocked:" if blocked else "allowed", blocked)
%% md
**What to notice:** The plan would replace the lake bucket (delete then create, which empties it) and delete the
analytics database, so CI blocks it and names both. The policy update, warehouse resize and new Glue job are routine.
A human can still approve a deliberate deletion, but never by accident.
%% md
## A complete workflow

A pull request workflow for a dbt project with Terraform, as GitHub Actions. It authenticates to the cloud with
OIDC (no stored keys), builds only changed models into a per-PR schema, runs the checks above, and deploys on merge.

```yaml
name: data-ci
on:
  pull_request:
  push: {branches: [main]}
permissions: {id-token: write, contents: read, pull-requests: write}
jobs:
  ci:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: sqlfluff lint models/
      - run: pytest tests/unit                      # transformation unit tests on fixtures
      - run: dbt build --select state:modified+ --defer --state prod-artifacts --target ci_pr_${{ github.event.number }}
      - run: python ci/contract_check.py            # block breaking schema changes
      - run: python ci/data_diff.py --post-comment  # impact on the PR
      - run: terraform -chdir=infra plan -out plan.out && terraform -chdir=infra show -json plan.out > plan.json
      - run: python ci/block_destructive.py plan.json
  deploy:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production                         # requires approval, holds prod credentials
    steps:
      - uses: actions/checkout@v4
      - run: terraform -chdir=infra apply -auto-approve
      - run: dbt build --select state:modified+ --target prod   # models publish via write-audit-publish
```

**Where it matters**
- Making every change to data, models and infrastructure go through the same reviewed path.

**Watch out for**
- CI that writes to production schemas: every CI target must be isolated and cleaned up when the PR closes.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** All unit tests pass and the schema is unchanged. What can still go wrong, and which check catches it?

**A.** The meaning or values of a column can change (gross to net revenue). A data diff against production shows how many rows and how much of each measure change.

**Q2.** Which schema changes are breaking for consumers?

**A.** Removing or renaming a column, narrowing a type, or changing a column's meaning. Adding a column and widening a type are usually safe.

**Q3.** Why build into a staging table and swap, instead of rebuilding the production table in place?

**A.** Readers would see an empty or partial table during the build, and a failure would leave it broken. Write-audit-publish keeps production untouched until an audited build is swapped in atomically.

**Q4.** Why is a Terraform rename of a bucket dangerous?

**A.** The provider plans it as delete plus create: a new empty bucket and the old one (with its data) deleted. Use `prevent_destroy`, `moved` blocks, and CI that blocks deletes of stateful resources.

**Q5.** What does dbt's `--defer --state` do in CI?

**A.** It builds only the modified models (and their children) and resolves references to unchanged models against production, so CI is fast and uses production-like inputs without rebuilding everything.
%% md
## Key takeaways

- Data CI tests code, schemas and data: unit tests on fixtures, contract checks, and a data diff against production.
- Build pull requests into isolated schemas; build only what changed and defer to production for the rest.
- Deploy and schedule with write-audit-publish: build beside, audit, swap atomically.
- Declare infrastructure, roles and grants as code, and block plans that delete stateful resources.
- Authenticate CI with OIDC and short-lived credentials; keep production credentials behind an approved environment.
%% md
**Next:** Continue with [Orchestration patterns](orchestration-patterns.ipynb) for running these builds on a
schedule, or [dbt](../dbt/dbt.ipynb) for the tool most data CI is built around.
'''

build("notebooks/topics/concepts/cicd-and-iac.ipynb", SPEC)
