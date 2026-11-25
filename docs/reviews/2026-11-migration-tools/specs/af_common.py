"""Shared setup for the Airflow labs: a throwaway Airflow 3 home with a SQLite metadata database."""

SETUP_PIP = """%% code
# Setup: install notebook dependencies in Colab.
!pip install -q apache-airflow~=3.4"""

INTRO = """Every example runs real Airflow 3 against a throwaway SQLite metadata database. Each DAG file is executed as a
script that calls `dag.test()`, which runs the DAG's tasks in one process without a scheduler or workers: task
states, retries, XCom and asset events are real, while scheduling across time is shown with Airflow's own CLI."""

HELPERS = '''%% code
import os
import re
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

workspace = TemporaryDirectory()
home = Path(workspace.name)
dags = home / "dags"
dags.mkdir()
env = {
    **os.environ,
    "AIRFLOW_HOME": str(home),
    "AIRFLOW__CORE__DAGS_FOLDER": str(dags),
    "AIRFLOW__CORE__LOAD_EXAMPLES": "False",
}

# A helper module the DAG files import to print each task instance's final state.
(dags / "lab_report.py").write_text("""
from airflow.models.taskinstance import TaskInstance
from airflow.utils.session import create_session


def report(run):
    print(f"LAB run {run.dag_id}: {run.state}")
    with create_session() as session:
        rows = (
            session.query(TaskInstance)
            .filter(TaskInstance.dag_id == run.dag_id, TaskInstance.run_id == run.run_id)
            .order_by(TaskInstance.task_id, TaskInstance.map_index)
        )
        for ti in rows:
            index = f"[{ti.map_index}]" if ti.map_index >= 0 else ""
            print(f"LAB   {ti.task_id}{index}: {ti.state} (try {ti.try_number})")
""")


def airflow(*args, show=None):
    """Run an Airflow CLI command; print its output lines that contain `show`."""
    done = subprocess.run([sys.executable, "-m", "airflow", *args], env=env, capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(done.stderr[-2000:])
    if show:
        print("\\n".join(line for line in (done.stdout + done.stderr).splitlines() if show in line))


def run_dag_file(name, source):
    """Write a DAG file into the DAGs folder and execute it."""
    run_python(dags / name, source)


def run_python(path, source):
    """Write a script and execute it; print the lines it marks with LAB (Airflow's own logging is hidden)."""
    path.write_text(source)
    done = subprocess.run([sys.executable, str(path)], env=env, capture_output=True, text=True)
    output = re.sub(r"\\x1b\\[[0-9;]*m", "", done.stdout + done.stderr).splitlines()  # drop log colors
    lines = [line.split("LAB ", 1)[1].split(" [airflow.")[0] for line in output if "LAB " in line and "Running command" not in line]
    print("\\n".join(lines))
    if done.returncode:
        raise RuntimeError(done.stderr[-2000:])


airflow("db", "migrate")
print("metadata database created:", (home / "airflow.db").exists())'''
