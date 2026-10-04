## [Main title](../README.md)
### [Interview questions](full.md)

# Docker for Data Engineers

**Notebook:** [`notebooks/topics/docker.ipynb`](../notebooks/topics/docker.ipynb) - runnable version of this topic with self-checking exercises.

Docker is the packaging layer of a modern data platform. It turns "it works on my laptop" into an immutable image with a pinned Python, Java, Spark, and driver stack, and that same image is what a scheduler, a CI runner, or Kubernetes executes. The practical skills are writing small reproducible images, wiring local stacks with Compose, and knowing how containers fail when they run out of memory or lose their entrypoint.

+ [What is Docker and why does it matter for data engineers?](#What-is-Docker-and-why-does-it-matter-for-data-engineers)
+ [What are images containers and layers?](#What-are-images-containers-and-layers)
+ [How does the Docker build cache work?](#How-does-the-Docker-build-cache-work)
+ [Which Dockerfile instructions should a data engineer know?](#Which-Dockerfile-instructions-should-a-data-engineer-know)
+ [How do you write a Dockerfile for a Python data job?](#How-do-you-write-a-Dockerfile-for-a-Python-data-job)
+ [How do multi-stage builds reduce image size?](#How-do-multi-stage-builds-reduce-image-size)
+ [What should go into a dockerignore file?](#What-should-go-into-a-dockerignore-file)
+ [What is the difference between CMD and ENTRYPOINT?](#What-is-the-difference-between-CMD-and-ENTRYPOINT)
+ [What is the difference between build args and environment variables?](#What-is-the-difference-between-build-args-and-environment-variables)
+ [What is the difference between volumes and bind mounts?](#What-is-the-difference-between-volumes-and-bind-mounts)
+ [How does Docker networking and service discovery work?](#How-does-Docker-networking-and-service-discovery-work)
+ [How do you use Docker Compose for a local data stack?](#How-do-you-use-Docker-Compose-for-a-local-data-stack)
+ [How do you run Airflow Postgres Spark and Trino locally with Compose?](#How-do-you-run-Airflow-Postgres-Spark-and-Trino-locally-with-Compose)
+ [How do you limit CPU and memory for a container?](#How-do-you-limit-CPU-and-memory-for-a-container)
+ [Why do resource limits matter for Spark and Airflow workers?](#Why-do-resource-limits-matter-for-Spark-and-Airflow-workers)
+ [How do healthchecks and depends_on work?](#How-do-healthchecks-and-depends_on-work)
+ [How do you run a container as a non-root user?](#How-do-you-run-a-container-as-a-non-root-user)
+ [How do you scan images for vulnerabilities?](#How-do-you-scan-images-for-vulnerabilities)
+ [How do you tag images and choose a registry?](#How-do-you-tag-images-and-choose-a-registry)
+ [How do you reduce image size?](#How-do-you-reduce-image-size)
+ [How do you build a custom Airflow image with extra Python dependencies?](#How-do-you-build-a-custom-Airflow-image-with-extra-Python-dependencies)
+ [How do you handle secrets in Docker?](#How-do-you-handle-secrets-in-Docker)
+ [How do you read container logs and debug a failing container?](#How-do-you-read-container-logs-and-debug-a-failing-container)
+ [How do you use Docker in a CI CD pipeline?](#How-do-you-use-Docker-in-a-CI-CD-pipeline)
+ [How does Docker relate to Kubernetes?](#How-does-Docker-relate-to-Kubernetes)
+ [What are common Docker pitfalls in data engineering?](#What-are-common-Docker-pitfalls-in-data-engineering)
+ [Real world use cases for Docker in data engineering](#Real-world-use-cases-for-Docker-in-data-engineering)

## What is Docker and why does it matter for data engineers?

Docker builds and runs OCI images. An image is a filesystem plus metadata; running it creates a container with isolated process, network, mount, and cgroup namespaces on the host kernel. It is not a virtual machine, so startup is milliseconds, but the isolation boundary is the kernel, not a hypervisor. The data engineering value is version pinning at the operating-system level, not just the package level: a virtualenv fixes `pyspark==3.5.3` but not the Java runtime, glibc, ODBC driver, or `tzdata` database, while an image fixes all of them together. That is why the same job behaves identically on a laptop, in CI, on an Airflow worker, and on a Kubernetes node.

```text
Dockerfile --docker build--> image --docker push--> registry
                                |
                                +--docker run--> laptop
                                +--compose-----> local stack
                                +--Kubernetes--> Pod
```

[Table of Contents](#Docker-for-Data-Engineers)

## What are images containers and layers?

An **image** is an immutable, ordered list of layers plus a JSON config (entrypoint, env, user, ports). A **layer** is the filesystem diff produced by one build step, addressed by content digest. A **container** is a running image plus a thin writable layer that is discarded with the container.

Layers are shared: ten images derived from `python:3.12-slim` store and pull that base once. The writable layer is also why writing a 50 GB shuffle file inside a container is a mistake: it fills the container filesystem rather than a mounted volume. A container whose main process exits is dead even if it "did nothing", so long-lived services must run in the foreground and must not daemonize.

```bash
docker image history registry.example.com/data/spark:3.5.3 --no-trunc
```

[Table of Contents](#Docker-for-Data-Engineers)

## How does the Docker build cache work?

Each instruction is hashed from its parent layer plus the instruction text and, for `COPY`, the checksum of copied files. `RUN` is skipped when the hash matches, so instruction order is the biggest build-speed lever: once one layer misses, every later layer rebuilds. The classic mistake is copying the whole source tree before installing dependencies, so editing one line of a job reinstalls everything.

```dockerfile
# good: dependencies cached independently of source changes
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY src/ /app/src/
```

BuildKit also provides build-time caches that are not layers, so pip or apt downloads persist across builds without bloating the image. Publish that cache to a registry in CI so every branch and runner reuses it:

```bash
docker buildx build --cache-from type=registry,ref=registry.example.com/data/etl:cache \
  --cache-to type=registry,ref=registry.example.com/data/etl:cache,mode=max -t registry.example.com/data/etl:1.4.0 .
```

[Table of Contents](#Docker-for-Data-Engineers)

## Which Dockerfile instructions should a data engineer know?

+ `FROM` sets the base; pin a version tag and ideally a digest. `WORKDIR` sets the working directory.
+ `RUN` executes a build step; chain with `&&` and clean up in the same layer.
+ `COPY` adds files from the build context; `ADD` also untars and fetches URLs, so prefer `COPY`.
+ `ENV` bakes runtime configuration into the image; `ARG` exists only at build time.
+ `USER` switches to a non-root account for the rest of the build and at runtime.
+ `EXPOSE` documents a port, `VOLUME` declares a mount point, `LABEL` carries metadata, and `ENTRYPOINT` with `CMD` defines what runs.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 TZ=UTC
RUN apt-get update && apt-get install -y --no-install-recommends tzdata libpq5 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
USER 1001
ENTRYPOINT ["python", "-m", "src.jobs.orders_daily"]
```

[Table of Contents](#Docker-for-Data-Engineers)

## How do you write a Dockerfile for a Python data job?

The shape is a minimal pinned base, the system libraries the Python packages link against, dependencies from a lockfile, application code last, a non-root user, and a foreground entrypoint.

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 TZ=UTC
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 tzdata \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt
COPY --chown=1001:1001 src/ ./src/
USER 1001
ENTRYPOINT ["python", "-m", "src.jobs.orders_daily"]
```

`PYTHONUNBUFFERED=1` makes prints and logging reach `docker logs` immediately instead of sitting in a buffer until exit. A modern JVM reads the cgroup limit, so heap defaults to a fraction of the container memory; the image must still ship its own JDK and driver jars rather than relying on the host.

[Table of Contents](#Docker-for-Data-Engineers)

## How do multi-stage builds reduce image size?

A multi-stage build uses several `FROM` statements; only the final stage becomes the image. The payoff is commonly 300 MB to 1 GB on Python data images, because compilers, headers, and pip caches never ship. The runtime stage copies just the built artifacts: a virtualenv, a wheel directory, or a compiled binary.

```dockerfile
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY src/ ./src/
ENTRYPOINT ["python", "-m", "src.jobs.orders_daily"]
```

For Spark images the same pattern matters more: download the distribution and Ivy jars in the builder stage, then copy only `/opt/spark` and the resolved jars into the runtime stage.

[Table of Contents](#Docker-for-Data-Engineers)

## What should go into a dockerignore file?

`.dockerignore` controls the build context, the files sent to the daemon. A missing or lazy one causes slow builds, cache invalidation from unrelated files, and secrets baked into layers by an over-broad `COPY .`.

```text
.git
.venv
__pycache__/
.env
.env.*
data/
dbt/target/
```

It is not a security boundary by itself: it only affects what `COPY` can see. The durable rule is to copy explicit paths (`COPY src/`) rather than `COPY .`, and to keep credentials out of images entirely.

[Table of Contents](#Docker-for-Data-Engineers)

## What is the difference between CMD and ENTRYPOINT?

`ENTRYPOINT` is the executable that always runs; `CMD` supplies default arguments, or the default command when there is no entrypoint. Arguments passed to `docker run` replace `CMD` but not `ENTRYPOINT`.

```dockerfile
ENTRYPOINT ["python", "-m", "src.jobs.orders_daily"]
CMD ["--ds", "2026-10-03"]
```

+ `docker run orders` runs the entrypoint with `--ds 2026-10-03`; `docker run orders --ds 2026-10-04` replaces the default argument; `docker run --entrypoint bash orders` replaces the entrypoint, the standard debugging move.

Use the exec form, not the shell form. Shell form wraps the process in `/bin/sh -c`, so the shell becomes PID 1, Python becomes a child, and `SIGTERM` from `docker stop` or a Kubernetes eviction is never forwarded. Airflow workers and Spark drivers then get killed hard, losing in-flight tasks and checkpoint writes.

[Table of Contents](#Docker-for-Data-Engineers)

## What is the difference between build args and environment variables?

`ARG` exists only while the image builds. `ENV` is written into the image config and persists into every container.

| Aspect | `ARG` | `ENV` |
| --- | --- | --- |
| Available during build | yes | yes, from the point it is declared |
| Persisted in image config | no | yes, visible via `docker inspect` |
| Overridable at runtime | no | yes, via `-e` or `environment:` |
| Good for | version pins and build flags | runtime config such as `TZ` |

Neither is a secret store. A password passed with `--build-arg` can be recorded in layer history, and one set with `ENV` shows up in `docker inspect` and in orchestrator manifests, readable by anyone who can pull the image. Redeclare an `ARG` after `FROM` if the stage needs it.

[Table of Contents](#Docker-for-Data-Engineers)

## What is the difference between volumes and bind mounts?

A **named volume** is storage managed by Docker under `/var/lib/docker/volumes`, portable across hosts and fast. A **bind mount** maps a host path into the container, which is ideal for live-editing code in development and wrong for production immutability.

```yaml
services:
  postgres:
    image: postgres:16
    volumes: ["pgdata:/var/lib/postgresql/data"]   # named volume: database files
  airflow-scheduler:
    image: acme/airflow:3.3.2
    volumes: ["./dags:/opt/airflow/dags:ro"]       # bind mount: author DAGs on the host
```

+ Named volumes survive `docker compose down` and are removed by `docker compose down -v`.
+ Bind mounts are read-through, so an edit is visible instantly; use `:ro` unless the container must write.
+ On SELinux hosts add `:z` or `:Z`; on macOS bind mounts cross a VM boundary and are slow for large data files.

For Postgres, always mount a named volume for the data directory; without it every `docker compose down` destroys the Airflow metadata database. In Kubernetes the same distinction appears as `PersistentVolumeClaim` versus `hostPath`.

[Table of Contents](#Docker-for-Data-Engineers)

## How does Docker networking and service discovery work?

Each Compose project gets a user-defined bridge network, and every container on it is reachable by its **service name**, resolved by Docker's embedded DNS at `127.0.0.11`. That is why `postgres:5432` works from the Airflow container while `localhost:5432` does not: inside a container, `localhost` means the container itself.

```yaml
services:
  postgres:
    image: postgres:16
    expose: ["5432"]            # reachable on the compose network only
```

+ Container-to-container traffic uses the service name and the container port, not the published port.
+ Published ports are for your laptop, not for sibling services, and two Compose projects do not see each other unless they share an external network.
+ From inside a container the host is `host.docker.internal` on Docker Desktop and the bridge gateway on Linux.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you use Docker Compose for a local data stack?

Compose is a declarative description of a multi-container application: services, networks, volumes, environment, health, and resource limits in one file, started with `docker compose up -d`. It replaces a wiki page of "install Postgres, create a role, run this SQL" with a reproducible command, and provides service-name DNS, dependency ordering, named volumes, and `docker compose logs -f` across every service. It does not provide high availability, autoscaling, or a scheduler, so keep it as a development and CI tool rather than a production runtime.

```bash
docker compose up -d --wait            # start everything and wait for health
docker compose down -v                 # stop and delete named volumes (fresh start)
```

[Table of Contents](#Docker-for-Data-Engineers)

## How do you run Airflow Postgres Spark and Trino locally with Compose?

This stack runs Airflow 3 with the Celery executor against Postgres, Redis as broker, a Spark master and worker for `SparkSubmitOperator`, and Trino for ad-hoc SQL. Named volumes keep Postgres data and Trino state across restarts.

```yaml
name: local-data-stack

x-airflow-common: &airflow-common
  image: acme/airflow:3.3.2
  user: "1001:0"
  environment:
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL: redis://redis:6379/0
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
    TZ: UTC
  volumes: ["./dags:/opt/airflow/dags:ro", "./logs:/opt/airflow/logs"]
  depends_on:
    postgres: {condition: service_healthy}

services:
  postgres:
    image: postgres:16
    environment: {POSTGRES_USER: airflow, POSTGRES_PASSWORD: airflow, POSTGRES_DB: airflow, TZ: UTC}
    command: ["postgres", "-c", "timezone=UTC", "-c", "max_connections=200"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    ports: ["5432:5432"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U airflow -d airflow"]
      interval: 10s
      retries: 10
  redis:
    image: redis:7-alpine
  airflow-api-server:
    <<: *airflow-common
    command: ["airflow", "api-server"]
    ports: ["8080:8080"]
  airflow-scheduler:
    <<: *airflow-common
    command: ["airflow", "scheduler"]
  airflow-dag-processor:
    <<: *airflow-common
    command: ["airflow", "dag-processor"]
  airflow-triggerer:
    <<: *airflow-common
    command: ["airflow", "triggerer"]
  airflow-worker:
    <<: *airflow-common
    command: ["airflow", "celery", "worker"]
    deploy: {resources: {limits: {cpus: "2.0", memory: 4G}}}
  spark-master:
    image: bitnamilegacy/spark:3.5.3
    environment: {SPARK_MODE: master, SPARK_MASTER_HOST: spark-master}
  spark-worker:
    image: bitnamilegacy/spark:3.5.3
    environment: {SPARK_MODE: worker, SPARK_MASTER_URL: "spark://spark-master:7077"}
    depends_on: [spark-master]
    deploy: {resources: {limits: {cpus: "2.0", memory: 3G}}}
  trino:
    image: trinodb/trino:463
    ports: ["8085:8080"]
    volumes: ["./trino/catalog:/etc/trino/catalog:ro"]

volumes: {pgdata: {}}
```

The Spark images come from `bitnamilegacy` because Bitnami retired its free image catalog and `bitnami/spark` no longer resolves. The `x-airflow-common` anchor is the point of the file: the API server, scheduler, DAG processor, worker, and triggerer cannot drift apart in image or environment. The API server waits on `postgres: service_healthy` rather than merely on the container existing, because migrations fail against a database that is still starting.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you limit CPU and memory for a container?

Containers share the host kernel, so limits are enforced with cgroups v2. Memory limits are hard: exceeding one triggers the OOM killer and the process dies with exit code 137. CPU limits throttle rather than kill, which shows up as slow jobs instead of failed jobs.

```bash
docker run --cpus=2 --memory=4g --memory-swap=4g \
  --pids-limit=512 --read-only --tmpfs /tmp \
  registry.example.com/data/spark-job:1.4.0
```

+ `--memory-swap` equal to `--memory` disables swap; leaving it unset lets a container swap and hide memory pressure as latency.
+ `-m 4g` limits the whole container, including every child process and the JVM heap plus off-heap.
+ `deploy.resources.limits` is the Compose and Kubernetes-shaped form and `mem_limit` is the plain Compose form; reservations affect scheduling, not enforcement, so limits are what kill you.

[Table of Contents](#Docker-for-Data-Engineers)

## Why do resource limits matter for Spark and Airflow workers?

For the JVM the container limit is the only memory signal that matters. A Spark executor sized for `spark.executor.memory=8g` in a container limited to 8 GB has no room for heap overhead, metaspace, thread stacks, or off-heap buffers, so the kernel kills it and the driver reports lost executors and retried stages.

```python
import math

# Size the container from the JVM side, not the other way around.
executor_heap_gb = 8
overhead_fraction = 0.15
container_gb = math.ceil(executor_heap_gb * (1 + overhead_fraction))  # 9.2 -> ask for 10g
print(f"limit={container_gb}g spark.executor.memory={executor_heap_gb}g")
```

Set `spark.executor.memoryOverhead` or `spark.executor.memoryOverheadFactor` explicitly, keep the container limit above heap plus overhead, and size the shuffle volume. On Kubernetes, `spark.kubernetes.executor.request.cores` must be at least `spark.executor.cores` or executors are throttled. An OOM-killed Airflow worker fails a task and retries it with no traceback, because the process never logged anything, and a CPU-starved scheduler shows up as DAG runs starting minutes late.

[Table of Contents](#Docker-for-Data-Engineers)

## How do healthchecks and depends_on work?

A `HEALTHCHECK` runs a command inside the container on an interval and marks it `starting`, `healthy`, or `unhealthy`. `depends_on` alone only waits for the container to start, which for Postgres means "the process exists", not "the database accepts connections".

```yaml
services:
  postgres:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U airflow -d airflow"]
      interval: 10s
  airflow-scheduler:
    image: acme/airflow:3.3.2
    depends_on: {postgres: {condition: service_healthy}}
```

+ `start_period` suppresses failures while a slow service boots, and `depends_on` is ordering, is not transitive, and says nothing about the dependency's own dependencies.
+ Kubernetes ignores `HEALTHCHECK` and uses `livenessProbe`, `readinessProbe`, and `startupProbe` instead.
+ Applications should still retry connections; a healthcheck narrows the race rather than removing it.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you run a container as a non-root user?

By default a container runs as root, and root in a container is one namespace escape away from root on the host. Running as an unprivileged UID is expected by platform security policy and by managed Kubernetes, where `runAsNonRoot: true` rejects images with a root `USER`.

```dockerfile
FROM python:3.12-slim
RUN groupadd --gid 1001 app && useradd --uid 1001 --gid 1001 --create-home app
WORKDIR /app
COPY --chown=1001:1001 requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=1001:1001 src/ ./src/
USER 1001:1001
ENTRYPOINT ["python", "-m", "src.jobs.orders_daily"]
```

+ Prefer a numeric UID in `USER`; Kubernetes cannot verify a named user against `runAsNonRoot`.
+ Install system packages as root, then switch back, and write only to locations the UID owns such as `/tmp` or a correctly chowned volume.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you scan images for vulnerabilities?

Every base image and every transitive Python or Java dependency is a potential CVE, and data images carry a lot of both. Scanning belongs in the build pipeline, not in a quarterly audit.

```bash
trivy image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed \
  registry.example.com/data/etl:1.4.0
```

+ Pin base images by digest so a tag move cannot silently change OS packages, and rebuild on a schedule because a scanned image is stale the moment a CVE is published.
+ Prefer minimal bases, but verify that PySpark and ODBC drivers still work, since they need a full glibc userland rather than musl; record accepted risk in an ignore file with a ticket rather than turning the scanner off.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you tag images and choose a registry?

A tag is a mutable pointer; a digest is immutable. Production deploys should record the digest even when a human-friendly tag triggers them.

```bash
IMAGE=registry.example.com/data/etl
SHA=$(git rev-parse --short HEAD)
docker build -t "${IMAGE}:1.4.0" -t "${IMAGE}:1.4.0-${SHA}" .
docker push "${IMAGE}:1.4.0" && docker push "${IMAGE}:1.4.0-${SHA}"
```

+ Tag with a semantic version plus the git SHA, and deploy the SHA tag so a running container maps to a commit.
+ Never rely on `:latest` in a cluster: with `imagePullPolicy: Always` deploys become unreproducible, and with `IfNotPresent` nodes silently run stale code.
+ Use a registry close to the cluster (ECR, Artifact Registry, ACR, Harbor, GHCR); cross-region pulls add seconds per pod, which matters when Spark starts 200 executors. Configure `imagePullSecrets`, prune old tags, and promote one immutable artifact through dev, staging, and prod.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you reduce image size?

Size drives pull time, cold-start latency, and vulnerability count. The biggest wins in order:

+ Start from `python:3.12-slim` or distroless rather than a full `ubuntu` base. `-alpine` is smaller but uses musl, which breaks many binary wheels and PySpark.
+ Use multi-stage builds and never ship compilers or headers.
+ Install with `--no-install-recommends`, clean `/var/lib/apt/lists` and pip caches in the same `RUN` layer, and enforce a size budget in CI so regressions fail the build.

```text
naive python:3.12 image with build tools ~ 2.6 GB vs multi-stage slim runtime ~ 620 MB
```

[Table of Contents](#Docker-for-Data-Engineers)

## How do you build a custom Airflow image with extra Python dependencies?

The stock Airflow image must not be modified at runtime. Installing packages in an entrypoint, or via `_PIP_ADDITIONAL_REQUIREMENTS`, makes every container start pay a pip resolve and lets the version you tested drift. Bake dependencies at build time, pinned against the official constraints file.

```dockerfile
# syntax=docker/dockerfile:1.7
ARG AIRFLOW_VERSION=3.3.2
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.12.txt"

FROM apache/airflow:${AIRFLOW_VERSION}-python3.12
ARG AIRFLOW_VERSION
ARG CONSTRAINT_URL

USER root
# system libraries needed by psycopg2, ODBC, and Kerberos-backed warehouses
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev libsasl2-dev unixodbc-dev tzdata \
    && rm -rf /var/lib/apt/lists/*
USER airflow
COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}" \
    && pip install --no-cache-dir -r /opt/airflow/requirements.txt --constraint "${CONSTRAINT_URL}" \
    && pip check
COPY --chown=airflow:root dags/ /opt/airflow/dags/
COPY --chown=airflow:root acme_pipelines/ /opt/airflow/dags/acme_pipelines/
ENV PYTHONPATH=/opt/airflow/dags
```

Build and publish it, then point every Compose service at `acme/airflow:3.3.2`, with your own `dbt-snowflake`, `apache-airflow-providers-*`, and `great-expectations` pins in `requirements.txt`. `pip check` makes an incompatible provider fail CI rather than the scheduler at 02:00.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you handle secrets in Docker?

Three rules: never bake a secret into an image, never pass one as a build argument, and never commit one in a Compose file. `docker inspect` exposes `ENV`, image history exposes `ARG`, and a layer that contained a secret still contains it after you delete the file in a later layer.

```yaml
services:
  etl:
    image: registry.example.com/data/etl:1.4.0
    environment: {SNOWFLAKE_USER: svc_etl, SNOWFLAKE_PASSWORD_FILE: /run/secrets/snowflake_password}
    secrets: [snowflake_password]
secrets:
  snowflake_password:
    file: ./secrets/snowflake_password.txt
```

```python
import os
from pathlib import Path

def read_secret(name: str, default: str | None = None) -> str | None:
    """Read a secret from a mounted file, falling back to an env var for local dev."""
    path = Path(f"/run/secrets/{name}")
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return os.environ.get(name.upper(), default)
```

In Kubernetes, use `Secret` objects with `secretKeyRef`, or a CSI driver mounting from Vault or a cloud secret manager, and authenticate with workload identity where possible so no static credential exists. File-mounted secrets only refresh if the driver supports it, so rotate by redeploying. An image that ever held a secret is compromised: rebuild it from a clean base.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you read container logs and debug a failing container?

Anything the process writes to stdout or stderr goes to the Docker log driver, so `print` and `logging` both work provided output is unbuffered. Set `PYTHONUNBUFFERED=1` in Python images; JVM jobs log to stdout unless log4j is reconfigured.

```bash
docker logs -f --tail 100 airflow-worker
docker logs --since 2h trino 2>&1 | grep -i "error\|exception"
docker inspect --format '{{.State.Status}} {{.State.ExitCode}} {{.State.OOMKilled}}' airflow-worker
```

Exit codes: **137** is SIGKILL, usually the OOM killer or a stop timeout; **143** is SIGTERM, a normal graceful stop; **1** is the application's own failure. If a container restarts in a loop, `docker compose logs --tail 50 <service>` plus `docker inspect` on the previous container is faster than guessing. For Airflow, task logs live in the `logs/` volume, scheduler logs are separate, and DAG import errors appear in the DAG processor's logs rather than the worker's.

[Table of Contents](#Docker-for-Data-Engineers)

## How do you use Docker in a CI CD pipeline?

CI builds the image once, scans it, pushes it under an immutable tag, and deploys that exact tag. The image is the artifact of record, so the pipeline never rebuilds per environment.

```yaml
jobs:
  image:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "${{ secrets.REGISTRY_TOKEN }}" | docker login registry.example.com -u "${{ secrets.REGISTRY_USER }}" --password-stdin
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: registry.example.com/data/etl:${{ github.sha }}
          cache-from: type=registry,ref=registry.example.com/data/etl:cache
          cache-to: type=registry,ref=registry.example.com/data/etl:cache,mode=max
      - run: trivy image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed registry.example.com/data/etl:${{ github.sha }}
      - run: kubectl -n data set image deploy/etl etl=registry.example.com/data/etl:${{ github.sha }}
```

Never build production images on a developer machine, use a registry cache so builds take seconds rather than minutes, run `pip check` and a DAG import check before publishing, and roll back by redeploying the previous digest rather than rebuilding an older commit.

[Table of Contents](#Docker-for-Data-Engineers)

## How does Docker relate to Kubernetes?

Docker builds images; Kubernetes runs them. The image is the unit of deployment that crosses the boundary, and most Docker-specific runtime behavior stops there.

+ Kubernetes no longer uses the Docker daemon; it uses containerd or CRI-O through the CRI, so `docker ps` shows nothing on a node. The image format is still OCI, so `docker build` and `docker push` produce exactly what the kubelet pulls.
+ `docker run` arguments become the Pod spec: `-e` becomes `env`, `-v` becomes `volumes` plus `volumeMounts`, and `--cpus` becomes `resources.requests` and `limits`.
+ `HEALTHCHECK` is ignored; Kubernetes uses `readinessProbe`, `livenessProbe`, and `startupProbe`.
+ A Pod is one or more containers sharing a network namespace, so containers inside a Pod reach each other on `localhost`, while across Pods they use a Service name instead of a Compose service name.
+ Compose is not a production runtime, and Pods are scheduled by resource requests, so accurate requests matter far more than in Compose. If an image works locally but behaves differently in the cluster, check probes, resource requests and limits, the service account, mounted secrets, then the timezone.

[Table of Contents](#Docker-for-Data-Engineers)

## What are common Docker pitfalls in data engineering?

+ **Installing dependencies at container start.** `pip install` in an entrypoint or `_PIP_ADDITIONAL_REQUIREMENTS` makes every restart slow and lets versions drift. Bake dependencies into the image.
+ **Baking credentials.** `ARG`, `ENV`, `COPY .env`, and a `.dockerignore` that misses `.env` all leak secrets into layers. Use mounted secrets or workload identity.
+ **Timezone and locale drift.** A slim image without `tzdata`, `TZ=UTC`, and `PYTHONUTF8=1` breaks timestamp parsing, `strftime`, and Spark jobs reading local timestamps.
+ **Huge images.** A 2 GB Airflow image takes minutes per worker restart and slows every Spark executor start. Build multi-stage, enforce a size budget, and never write shuffle files or caches into the container layer.
+ **OOM kills without a traceback.** Exit 137 from a cgroup limit looks mysterious. Size Spark executors with `memoryOverhead` above heap and give Airflow workers a limit covering the largest task.
+ **Shell-form entrypoints.** Signals are not forwarded, so `docker stop` or an eviction kills work in flight, and in a container `localhost` is the container itself, so sibling services must be reached by service name and container port.

[Table of Contents](#Docker-for-Data-Engineers)

## Real world use cases for Docker in data engineering

### 1. Local Airflow and Postgres development stack

Eight data engineers need everyone on the same Airflow version, metadata schema, and provider set without hours of setup. The Compose stack above is the onboarding doc: clone, `docker compose up -d --wait`, open `localhost:8080`, and run a task in isolation with `docker compose exec airflow-scheduler airflow tasks test daily_orders_pipeline extract 2026-10-03`.

Why this design: the Airflow image comes from the same Dockerfile CI publishes, so a DAG that imports locally imports in production; Postgres runs the same major version as production with `timezone=UTC`; named volumes keep history across restarts while `down -v` gives a clean slate. The trade-off is that Compose has no scheduler or autoscaling, so behavior depending on node pressure must be tested in a real cluster.

### 2. A reproducible Spark job image

A PySpark job depends on Python 3.12, Java 17, Spark 3.5.3, the PostgreSQL JDBC driver, and two private wheels. Shipping a zip to a shared cluster produced driver-version mismatches; one image carrying all of it removes that class of failure.

```dockerfile
FROM apache/spark:3.5.3-python3
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && curl -fsSL -o /opt/spark/jars/postgresql-42.7.4.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar
COPY src/ /opt/spark/jobs/
USER 185
ENTRYPOINT ["/opt/spark/bin/spark-submit", "--master", "k8s://https://kubernetes.default.svc", "--deploy-mode", "cluster", "/opt/spark/jobs/orders_daily.py"]
```

Why this design: the driver JAR is baked in rather than passed with `--jars`, so a network hiccup at submit time cannot change the runtime; the user is non-root; the exec-form entrypoint lets `SIGTERM` reach `spark-submit`. The trade-off is a large image and a rebuild per dependency change, which is cheap next to failures that only appear in production.

### 3. CI image build and publish

Every merge builds, scans, and publishes the pipeline image with a registry-backed layer cache, so a change that touches only DAG code is under a minute; nothing is built on a laptop for production.

Why this design: the deploy references a git SHA, so a rollback is a redeploy of the previous digest and the same artifact is promoted through staging and production.

```yaml
- uses: docker/build-push-action@v6
  with: {push: true, tags: "registry.example.com/data/pipelines:${{ github.sha }}", cache-to: "type=registry,ref=registry.example.com/data/pipelines:cache,mode=max"}
```

The trade-off is a registry dependency and the discipline of immutable tags; a team that keeps pushing `latest` gets none of the reproducibility.

### 4. Containerized dbt and Trino services

A dbt image pins `dbt-trino`, the profiles, and the packages, while Trino runs from the official image with its catalog directory mounted. Analysts get an isolated build with one command.

```yaml
services:
  dbt:
    image: ghcr.io/acme/dbt-trino:1.9.2
    volumes: ["./dbt:/usr/app:ro", "./profiles:/root/.dbt:ro"]
    environment: {DBT_PROFILES_DIR: /root/.dbt, DBT_TARGET: dev}
    depends_on:
      trino: {condition: service_healthy}
    entrypoint: ["dbt"]
    command: ["build", "--select", "tag:finance"]
```

Why this design: the dbt version, adapters, and profiles are identical for every analyst and in CI, and Trino stays a separate service so a bad model cannot restart the SQL engine. The trade-off is that bind-mounting models in development is not proof; CI must run the same models inside the published image.

### 5. Shipping a model or ETL job to Kubernetes

A nightly scoring job is packaged as an image, run as a Kubernetes `CronJob`, and given a service account that can read object storage, with no static credentials in the image.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata: {name: churn-scoring, namespace: ml}
spec:
  schedule: "0 3 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          serviceAccountName: churn-scoring
          containers:
            - name: score
              image: registry.example.com/ml/churn-scoring:2.1.0
              resources: {requests: {cpu: "1", memory: 2Gi}, limits: {cpu: "2", memory: 4Gi}}
              securityContext: {runAsNonRoot: true, runAsUser: 1001, readOnlyRootFilesystem: true}
```

Why this design: the image is the deployment unit, so the model version, Python runtime, and feature code move together and a rollback is a tag change; IAM is attached to the service account instead of baked into the container. The trade-off is an extra build and push per model change, which pays off as soon as more than one environment and more than one engineer are involved.

[Table of Contents](#Docker-for-Data-Engineers)
