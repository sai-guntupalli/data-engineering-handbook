"""Shared setup for the dbt lessons: a fresh dbt project on DuckDB in a temporary directory."""

SETUP_PIP = """%% code
# Setup: install notebook dependencies in Colab.
!pip install -q dbt-core~=1.12 dbt-duckdb~=1.11 duckdb~=2.0"""

INTRO = """Every example runs real dbt (`dbt-core` with the `dbt-duckdb` adapter) through its Python entry point,
`dbtRunner`, against a DuckDB file in a temporary folder. The commands are the ones you would type in a terminal,
such as `dbt build --select fct_orders`; only the warehouse is local."""

HELPERS = '''%% code
from pathlib import Path
from tempfile import TemporaryDirectory

import duckdb
from dbt.cli.main import dbtRunner

workspace = TemporaryDirectory()
project = Path(workspace.name)
for folder in ["models", "tests", "snapshots"]:
    (project / folder).mkdir()
warehouse = project / "warehouse.duckdb"
(project / "dbt_project.yml").write_text("name: handbook\\nversion: '1.0'\\nprofile: handbook\\n")
(project / "profiles.yml").write_text(
    f"handbook:\\n  target: dev\\n  outputs:\\n    dev:\\n      type: duckdb\\n      path: '{warehouse}'\\n      threads: 1\\n"
)


last_result = None  # the most recent dbtRunner result, for inspecting details such as microbatch batches


def write(relative_path, text):
    """Create or replace a file in the dbt project."""
    (project / relative_path).write_text(text.strip() + "\\n")


def dbt(*args, expect_success=True):
    """Run a dbt command and print one line per node: its type, name, status and any failure message."""
    global last_result
    result = last_result = dbtRunner().invoke(
        ["--log-level", "none", *args, "--project-dir", str(project), "--profiles-dir", str(project)]
    )
    if result.exception is not None:
        raise result.exception
    if isinstance(result.result, list):  # dbt ls returns names
        print("\\n".join(result.result))
    else:
        for node in result.result:
            message = (node.message or "").split("\\n  > in macro")[0].rstrip()  # drop dbt's macro call stack
            detail = f" ({message})" if node.status in ("fail", "warn", "error") and message else ""
            print(f"{node.node.resource_type:>8} {node.node.name}: {node.status}{detail}")
    if result.success != expect_success:
        raise RuntimeError(f"dbt {' '.join(args)} returned success={result.success}")


def sql(statement):
    """Run SQL directly against the warehouse and return the rows."""
    with duckdb.connect(str(warehouse)) as connection:
        return connection.execute(statement).fetchall()'''
