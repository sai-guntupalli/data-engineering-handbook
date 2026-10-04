## [Main title](../README.md)
### [Interview questions](full.md)

# Kubernetes

**Notebook:** [`notebooks/topics/kubernetes.ipynb`](../notebooks/topics/kubernetes.ipynb) - runnable version of this topic with self-checking exercises.

Kubernetes is the default runtime for data platforms that need reproducible packaging, per-job isolation, and elastic compute. A data engineer rarely administers the whole cluster, but you are expected to read and write the manifests that run Spark drivers and executors, Airflow workers and triggerers, dbt jobs, Kafka/Flink operators, and the APIs around data products.

+ [Why is Kubernetes useful for data engineering workloads?](#Why-is-Kubernetes-useful-for-data-engineering-workloads)
+ [What is the difference between a Kubernetes Job, CronJob, Deployment, and StatefulSet?](#What-is-the-difference-between-a-Kubernetes-Job-CronJob-Deployment-and-StatefulSet)
+ [How to do maintenance activity on the K8 node?](#How-to-do-maintenance-activity-on-the-K8-node)
+ [How do we control the resource usage of POD?](#How-do-we-control-the-resource-usage-of-POD)
+ [What are the various K8's services running on nodes and describe the role of each service?](#What-are-the-various-K8s-services-running-on-nodes-and-describe-the-role-of-each-service)
+ [What is PDB (Pod Disruption Budget)?](#What-is-PDB-Pod-Disruption-Budget)
+ [What's the init container and when it can be used?](#Whats-the-init-container-and-when-it-can-be-used)
+ [What is the role of Load Balance in Kubernetes?](#What-is-the-role-of-Load-Balance-in-Kubernetes)
+ [What are the various things that can be done to increase Kubernetes security?](#What-are-the-various-things-that-can-be-done-to-increase-Kubernetes-security)
+ [How to monitor the Kubernetes cluster?](#How-to-monitor-the-Kubernetes-cluster)
+ [How to get the central logs from POD?](#How-to-get-the-central-logs-from-POD)
+ [How to turn the service defined below in the spec into an external one?](#How-to-turn-the-service-defined-below-in-the-spec-into-an-external-one)
+ [How to configure TLS with Ingress?](#How-to-configure-TLS-with-Ingress)
+ [Why use namespaces? What is the problem with using the default namespace?](#Why-use-namespaces-What-is-the-problem-with-using-the-default-namespace)
+ [In the following file which service and in which namespace is referred?](#In-the-following-file-which-service-and-in-which-namespace-is-referred)
+ [What is an Operator?](#What-is-an-Operator)
+ [Why do we need Operators?](#Why-do-we-need-Operators)
+ [What is GKE?](#What-is-GKE)
+ [What is Ingress Default Backend?](#What-is-Ingress-Default-Backend)
+ [How to run Kubernetes locally?](#How-to-run-Kubernetes-locally)
+ [What is Kubernetes Load Balancing?](#What-is-Kubernetes-Load-Balancing)
+ [What the following in the Deployment configuration file mean?](#What-the-following-in-the-Deployment-configuration-file-mean)
+ [What is the difference between Docker Swarm and Kubernetes?](#What-is-the-difference-between-Docker-Swarm-and-Kubernetes)
+ [How to troubleshoot if the POD is not getting scheduled?](#How-to-troubleshoot-if-the-POD-is-not-getting-scheduled)
+ [How to run a POD on a particular node?](#How-to-run-a-POD-on-a-particular-node)
+ [What are the different ways to provide external network connectivity to K8?](#What-are-the-different-ways-to-provide-external-network-connectivity-to-K8)
+ [How can we forward the port 8080 container to 8080 service to 8080 ingress to 80 browser and how it can be done?](#How-can-we-forward-the-port-8080-container-to-8080-service-to-8080-ingress-to-80-browser-and-how-it-can-be-done)
+ [How do you configure liveness, readiness, and startup probes?](#How-do-you-configure-liveness-readiness-and-startup-probes)
+ [How do you use node selectors, affinity, and tolerations?](#How-do-you-use-node-selectors-affinity-and-tolerations)
+ [How do you autoscale a data workload with the Horizontal Pod Autoscaler?](#How-do-you-autoscale-a-data-workload-with-the-Horizontal-Pod-Autoscaler)
+ [How do you run Spark on Kubernetes?](#How-do-you-run-Spark-on-Kubernetes)
+ [How do you run Airflow workers on Kubernetes?](#How-do-you-run-Airflow-workers-on-Kubernetes)
+ [How do you manage secrets and configuration for data workloads?](#How-do-you-manage-secrets-and-configuration-for-data-workloads)
+ [How do you run a scheduled data pipeline with a CronJob?](#How-do-you-run-a-scheduled-data-pipeline-with-a-CronJob)
+ [Real world use cases for Kubernetes](#Real-world-use-cases-for-Kubernetes)

## Why is Kubernetes useful for data engineering workloads?

Kubernetes provides a consistent way to run containerized jobs, services, schedulers, and workers. Data teams use it for Airflow workers, Spark on Kubernetes, dbt jobs, custom ingestion services, and APIs around data products.

Example:

```text
CronJob -> runs daily Python ingestion container -> writes to object storage
```

The value is reproducible runtime packaging, resource limits, scaling, secrets management, and deployment consistency.

For data engineering specifically, four properties matter:

+ **Per-job resource isolation.** A Spark executor that needs 8 GiB and 4 CPU gets exactly that, and a run-away Python job cannot take the whole node.
+ **Elastic compute.** Jobs are scheduled on demand and nodes can be scaled up or down, so a cluster is not sized for peak batch load.
+ **One deployment model.** The same image and manifests move from dev to prod, and the same primitives (Jobs, CronJobs, Deployments) run batch and services.
+ **Ecosystem.** Spark, Flink, Airflow, dbt, Trino, Kafka, and most data tools already ship Helm charts or operators.

The trade-off is operational complexity: someone still owns upgrades, node pools, autoscaling, ingress, and the observability stack. A managed service (Databricks, EMR on EKS, Confluent Cloud) trades that complexity for cost and vendor coupling.

[Table of Contents](#Kubernetes)

## What is the difference between a Kubernetes Job, CronJob, Deployment, and StatefulSet?

A Job runs a task to completion. A CronJob runs Jobs on a schedule. A Deployment manages stateless long-running services. A StatefulSet manages stateful services that need stable identities and persistent volumes.

Example choices:

+ Job: one-off backfill
+ CronJob: daily data extract
+ Deployment: metadata API service
+ StatefulSet: Kafka, Cassandra, or another clustered stateful service

A run-to-completion Job:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: backfill-orders-2026-09
  namespace: data
spec:
  backoffLimit: 3
  ttlSecondsAfterFinished: 86400
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: backfill
          image: registry.example.com/data/orders-etl:1.14.2
          args: ["--start-date", "2026-09-01", "--end-date", "2026-09-30"]
          resources:
            requests:
              cpu: "2"
              memory: 4Gi
            limits:
              cpu: "4"
              memory: 8Gi
```

A scheduled Job:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: orders-daily-extract
  namespace: data
spec:
  schedule: "0 2 * * *"
  timeZone: "America/New_York"
  concurrencyPolicy: Forbid          # never overlap two loads of the same target
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  startingDeadlineSeconds: 600
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: extract
              image: registry.example.com/data/orders-etl:1.14.2
```

A Deployment manages stateless replicas; a StatefulSet adds stable identity, ordered rollout, and per-pod storage:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: catalog-api, namespace: data}
spec:
  replicas: 3
  selector: {matchLabels: {app: catalog-api}}
  template:
    metadata: {labels: {app: catalog-api}}
    spec:
      containers:
        - name: api
          image: registry.example.com/data/catalog-api:2.3.0
          ports: [{containerPort: 8080}]
---
apiVersion: apps/v1
kind: StatefulSet
metadata: {name: kafka-broker, namespace: streaming}
spec:
  serviceName: kafka-headless
  replicas: 3
  selector: {matchLabels: {app: kafka}}
  template:
    metadata: {labels: {app: kafka}}
    spec:
      containers:
        - name: kafka
          image: registry.example.com/data/kafka:3.9
          volumeMounts: [{name: data, mountPath: /var/lib/kafka/data}]
  volumeClaimTemplates:
    - metadata: {name: data}
      spec:
        accessModes: ["ReadWriteOnce"]
        resources: {requests: {storage: 500Gi}}
```

For data pipelines, Jobs and CronJobs are common for batch tasks, while Deployments are common for always-on services. Use a StatefulSet only when the workload genuinely needs stable network identity or its own persistent volume; a job that reads and writes object storage is not stateful.

[Table of Contents](#Kubernetes)

## How to do maintenance activity on the K8 node?

Whenever there are security patches available the Kubernetes administrator has to perform the maintenance task to apply the security patch to the running container in order to prevent it from vulnerability, which is often an unavoidable part of the administration. The following two commands are useful to safely drain the K8s node.

```bash
kubectl cordon <node-name>
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

The first command moves the node to maintenance mode or makes the node unavailable, followed by `kubectl drain` which will finally discard the pod from the node. After the drain command is a success you can perform maintenance.

Note: If you wish to perform maintenance on a single pod following two commands can be issued in order:

```bash
kubectl get nodes                  # list all the nodes
kubectl drain <node-name>          # drain a particular node
kubectl uncordon <node-name>       # return it to service afterwards
```

Operational notes that matter for data workloads:

+ `--ignore-daemonsets` is required because DaemonSet pods cannot be moved.
+ Draining respects PodDisruptionBudgets, so a Kafka cluster with `minAvailable: 2` will block eviction if only two brokers are healthy.
+ A Spark executor pod is usually evicted cleanly; the driver retries the task. A long-running stateful pod needs its operator or a manual leader step-down first.
+ On managed platforms, node auto-repair and maintenance windows do this for you; use `kubectl get events` and the node conditions (`MemoryPressure`, `DiskPressure`) to confirm.

[Table of Contents](#Kubernetes)

## How do we control the resource usage of POD?

With the use of limit and request resource usage of a POD can be controlled.

Request: The number of resources being requested for a container. If a container exceeds its request for resources, it can be throttled back down to its request.

Limit: An upper cap on the resources a single container can use. If it tries to exceed this predefined limit it can be terminated if K8's decides that another container needs these resources. If you are sensitive towards pod restarts, it makes sense to have the sum of all container resource limits equal to or less than the total resource capacity for your cluster.

Example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo
spec:
  containers:
    - name: example1
      image: example/example1
      resources:
        requests:
          memory: "512Mi"
          cpu: "250m"
        limits:
          memory: "1Gi"
          cpu: "500m"
```

How the scheduler and the kernel actually use these values:

+ **requests** decide scheduling and are the minimum guaranteed share. CPU requests set `cpu.shares`; memory requests influence eviction ordering.
+ **limits** set the hard ceiling. A container that exceeds a memory limit is OOM-killed; a container that exceeds a CPU limit is throttled, not killed.
+ **QoS class** follows from the combination:
  + `Guaranteed` - requests equal limits on every container. Last to be evicted.
  + `Burstable` - requests set but below limits (the common case).
  + `BestEffort` - nothing set. First to be evicted, and a bad choice for production data jobs.
+ **Namespaces and quotas** cap an entire team, not one pod:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: data-team-quota
  namespace: data
spec:
  hard:
    requests.cpu: "200"
    requests.memory: 800Gi
    limits.cpu: "400"
    limits.memory: 1600Gi
    count/jobs.batch: "50"
```

A realistic Spark executor block sizes both values so the JVM heap, off-heap memory, and container limit line up:

```yaml
resources:
  requests:
    cpu: "4"
    memory: "16Gi"
  limits:
    cpu: "8"
    memory: "18Gi"
```

Interview point: memory requests and limits must account for JVM overhead, not just `spark.executor.memory`. If the container limit is below the JVM's total footprint, the pod restarts with exit code 137 (OOMKilled) even though Spark shows no OOM.

[Table of Contents](#Kubernetes)

## What are the various K8's services running on nodes and describe the role of each service?

Mainly K8 cluster consists of two types of nodes, executor and master.

Executor node:

Kube-proxy: This service is responsible for the communication of pods within the cluster and to the outside network, which runs on every node. This service is responsible to maintain network protocols when your pod establishes a network communication.

kubelet: Each node has a running kubelet service that updates the running node accordingly with the configuration(YAML or JSON) file. NOTE: kubelet service is only for containers created by Kubernetes.

Master services:

Kube-apiserver: Master API service which acts as an entry point to K8 cluster.

Kube-scheduler: Schedule PODs according to available resources on executor nodes.

Kube-controller-manager: is a control loop that watches the shared state of the cluster through the apiserver and makes changes attempting to move the current state towards the desired stable state.

The container runtime (containerd, CRI-O) is the piece that actually pulls images and runs containers; kubelet talks to it through the CRI interface. On managed clouds the master nodes are hidden behind an SLA, but the same components exist.

```bash
kubectl get pods -n kube-system
kubectl get componentstatuses        # apiserver, scheduler, controller-manager health
kubectl top nodes
kubectl top pods -n data
```

For a data engineer, the actionable version is: if pods stay `Pending`, check the scheduler; if they stay `ContainerCreating`, check kubelet events and image pulls; if the API server is down, nothing in your pipeline can be reconciled.

[Table of Contents](#Kubernetes)

## What is PDB (Pod Disruption Budget)?

A Kubernetes administrator can create a deployment of a kind: PodDisruptionBudget for high availability of the application, it makes sure that the minimum number is running pods are respected as mentioned by the attribute minAvailable spec file. This is useful while performing a drain where the drain will halt until the PDB is respected to ensure the High Availability(HA) of the application. The following spec file also shows minAvailable as 2 which implies the minimum number of an available pod (even after the election).

Example: YAML Config using minAvailable:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: zk-pdb
  namespace: streaming
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: zookeeper
```

The alternative is `maxUnavailable`:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: trino-worker-pdb
  namespace: analytics
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: trino-worker
```

Notes:

+ A PDB only protects against *voluntary* disruptions (drain, node upgrade). It cannot stop a node crash or an OOM kill.
+ `minAvailable` as a percentage (`80%`) scales better than a fixed number as replicas change.
+ Pair a PDB with anti-affinity so the replicas are actually on different nodes; otherwise the budget can never be satisfied.
+ PDBs are how a broker or a query worker survives a rolling node upgrade without a full outage.

[Table of Contents](#Kubernetes)

## What's the init container and when it can be used?

init containers will set a stage for you before running the actual POD: they run to completion, in order, before any app container starts, and each must succeed before the next begins.

Common uses:

+ Wait for a dependency (a database, a schema version, a lock) before the app starts.
+ Clone a git repository or download a model artifact into a shared volume.
+ Fix ownership/permissions on a mounted volume (run as root, then drop to a non-root user).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dbt-runner
spec:
  initContainers:
    - name: fetch-dbt-project
      image: registry.example.com/data/git-sync:1.2
      command: ["git", "clone", "--depth", "1",
                "https://github.com/acme/analytics-dbt.git", "/workspace"]
      volumeMounts:
        - name: workspace
          mountPath: /workspace
  containers:
    - name: dbt
      image: registry.example.com/data/dbt:1.9
      command: ["dbt", "run", "--project-dir", "/workspace"]
      volumeMounts:
        - name: workspace
          mountPath: /workspace
  volumes:
    - name: workspace
      emptyDir: {}
```

When *not* to use one: init containers add startup time and are per-pod, not per-container. For a fast health check on a long-running service, use a readiness probe instead, because an init container that blocks delays the whole pod rather than removing it from load balancing.

[Table of Contents](#Kubernetes)

## What is the role of Load Balance in Kubernetes?

Load balancing is a way to distribute the incoming traffic into multiple backend servers, which is useful to ensure the application available to the users.

In Kubernetes, all the incoming traffic lands to a single IP address on the load balancer which is a way to expose your service to outside the internet which routes the incoming traffic to a particular pod (via service) using an algorithm known as round-robin. Even if any pod goes down load balances are notified so that the traffic is not routed to that particular unavailable node. Thus load balancers in Kubernetes are responsible for distributing a set of tasks (incoming traffic) to the pods.

Three load-balancing layers exist, and interviewers like candidates who separate them:

+ **kube-proxy / Service (L4).** A `ClusterIP` service is a virtual IP; kube-proxy programs iptables/IPVS rules so each connection is forwarded to one healthy endpoint selected by round-robin (or session affinity if configured).
+ **Cloud load balancer (L4).** A `Service` of `type: LoadBalancer` asks the cloud provider to provision an external LB that targets the nodes or the pod IPs.
+ **Ingress / Gateway (L7).** An ingress controller terminates HTTP(S), routes by host/path, and can do TLS, retries, and header-based rules.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: warehouse-api
  namespace: data
spec:
  type: ClusterIP
  selector:
    app: warehouse-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

Readiness probes are what make load balancing correct: a pod that is not `Ready` is removed from the endpoint list, so traffic only reaches pods that can serve it.

[Table of Contents](#Kubernetes)

## What are the various things that can be done to increase Kubernetes security?

By default, POD can communicate with any other POD, we can set up network policies to limit this communication between the PODs.

RBAC (Role-based access control) to narrow down the permissions.

Use namespaces to establish security boundaries.

Set the admission control policies to avoid running the privileged containers.

Turn on audit logging.

Concrete controls a data platform should actually enable:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-data-to-warehouse-only
  namespace: data
spec:
  podSelector:
    matchLabels: {app: orders-etl}
  policyTypes: [Egress]
  egress:
    - to:
        - namespaceSelector:
            matchLabels: {kubernetes.io/metadata.name: warehouse}
      ports:
        - port: 5432
    - to:
        - ipBlock:
            cidr: 10.0.0.0/8
      ports:
        - port: 443
```

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
  seccompProfile:
    type: RuntimeDefault
```

Also worth stating: least-privilege service accounts with short-lived credentials (IRSA, Workload Identity) instead of long-lived cloud keys in Secrets; image scanning and a signed-image policy; `ResourceQuota` and `LimitRange` to stop crypto-miner-style abuse; and namespace-level RBAC so a notebook user cannot read production Secrets. The most common real incident is not a cluster break-in - it is a job with a wildcard cloud role and a plaintext credential in a ConfigMap.

[Table of Contents](#Kubernetes)

## How to monitor the Kubernetes cluster?

Prometheus is used for Kubernetes monitoring. The Prometheus ecosystem consists of multiple components.

Mainly Prometheus server which scrapes and stores time-series data.

Client libraries for instrumenting application code.

Push gateway for supporting short-lived jobs.

Special-purpose exporters for services like StatsD, HAProxy, Graphite, etc.

An alert manager to handle alerts on various support tools.

The modern stack on top of that is:

+ **kube-state-metrics** for object state: desired vs available replicas, Job failures, Pending pods, PVC status, CronJob last-successful time.
+ **node-exporter** for node CPU, memory, disk, and network.
+ **cAdvisor / metrics-server** for per-container usage, which powers `kubectl top` and the HPA.
+ **Grafana** for dashboards, **Alertmanager** for routing.

Signals a data platform should alert on:

| Signal | Why it matters |
|---|---|
| Job `Failed` / `backoffLimitExceeded` | a pipeline run failed silently |
| CronJob `lastSuccessfulTime` too old | the schedule stopped firing |
| Pod `OOMKilled` (exit 137) | executor memory is under-provisioned |
| `Pending` pods for more than N minutes | unschedulable: capacity or taints |
| Node `MemoryPressure` / `DiskPressure` | an imminent eviction storm |
| HPA at max replicas | capacity ceiling reached |

```text
# pods OOM-killed in the last hour, by workload
sum by (namespace, pod) (
  kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}
)
```

[Table of Contents](#Kubernetes)

## How to get the central logs from POD?

This architecture depends upon the application and many other factors. Following are the common logging patterns:

Node level logging agent.

Streaming sidecar container.

Sidecar container with the logging agent.

Export logs directly from the application.

In the setup, journalbeat and filebeat are running as daemonset. Logs collected by these are dumped to the kafka topic which is eventually dumped to the ELK stack. The same can be achieved using EFK stack and fluentd-bit.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
  namespace: logging
spec:
  selector:
    matchLabels: {app: fluent-bit}
  template:
    metadata:
      labels: {app: fluent-bit}
    spec:
      tolerations:
        - operator: Exists          # run on every node, including tainted ones
      containers:
        - name: fluent-bit
          image: cr.fluentbit.io/fluent/fluent-bit:3.1
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: containers
              mountPath: /var/lib/docker/containers
              readOnly: true
      volumes:
        - name: varlog
          hostPath: {path: /var/log}
        - name: containers
          hostPath: {path: /var/lib/docker/containers}
```

Practical guidance for data jobs:

+ Prefer stdout/stderr logging from the container; the node agent collects it without any app change.
+ Add a correlation key (`run_id`, `dag_id`, `task_id`, `spark.app.id`) to every line so a distributed job is searchable across driver and executors.
+ Kubernetes log retention on the node is short. Ship logs to durable storage (object storage, ClickHouse, Elasticsearch, Loki) before they roll.
+ For Spark on Kubernetes, enable the log aggregation (or the Spark history server) or the executor logs disappear with the pod.

```bash
kubectl logs deploy/orders-etl -n data --since=1h
kubectl logs -l spark-role=executor -n data --tail=200
```

[Table of Contents](#Kubernetes)

## How to turn the service defined below in the spec into an external one?

Starting spec:

```yaml
spec:
  selector:
    app: some-app
  ports:
    - protocol: UDP
      port: 8080
      targetPort: 8080
```

Explanation: with no `type`, this is a `ClusterIP` service and is only reachable inside the cluster. Adding `type: LoadBalancer` (with an optional `nodePort`) makes it external:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: some-app
spec:
  selector:
    app: some-app
  type: LoadBalancer
  ports:
    - protocol: UDP
      port: 8080
      targetPort: 8080
      nodePort: 32412        # optional; omit to let Kubernetes allocate one
```

Complete the following configuration spec file to make it an Ingress:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: someapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: my.host
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: some-app
                port:
                  number: 8080
```

One of the several ways to answer this question. Choose by protocol and layer: `NodePort` for quick tests (one port on every node), `LoadBalancer` for a raw L4 endpoint, `Ingress` for HTTP routing, TLS, and host/path rules. The old `serviceName`/`servicePort` fields shown in older docs were replaced by the nested `service.name`/`service.port.number` shape in `networking.k8s.io/v1`.

[Table of Contents](#Kubernetes)

## How to configure TLS with Ingress?

Add `tls` and `secretName` entries. The secret must be a `kubernetes.io/tls` secret containing `tls.crt` and `tls.key`.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: someapp-ingress
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - some_app.com
      secretName: someapp-secret-tls
  rules:
    - host: some_app.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: some-app
                port:
                  number: 8080
```

```bash
# create the TLS secret (or let cert-manager do it)
kubectl create secret tls someapp-secret-tls \
  --cert=tls.crt --key=tls.key -n data

# redirect HTTP to HTTPS
# annotation: nginx.ingress.kubernetes.io/ssl-redirect: "true"
```

For production, do not manage certificates by hand: install cert-manager and issue `Certificate` resources from Let's Encrypt or your internal CA, and let it rotate the secret. Note that TLS terminates at the ingress; if you also want encryption inside the cluster, configure the backend protocol (`nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"`) or a service mesh.

[Table of Contents](#Kubernetes)

## Why use namespaces? What is the problem with using the default namespace?

While using the default namespace alone, it becomes hard over time to get an overview of all the applications you can manage in your cluster. Namespaces make it easier to organize the applications into groups that make sense, like a namespace of all the monitoring applications and a namespace for all the security applications, etc.

Namespaces can also be useful for managing Blue/Green environments where each namespace can include a different version of an app and also share resources that are in other namespaces (namespaces like logging, monitoring, etc.).

Another use case for namespaces is one cluster with multiple teams. When multiple teams use the same cluster, they might end up stepping on each other's toes. For example, if they end up creating an app with the same name it means one of the teams overrides the app of the other team because there can't be two apps in Kubernetes with the same name (in the same namespace).

Namespaces are also the unit of the controls a data platform cares about most:

+ `ResourceQuota` and `LimitRange` per team.
+ RBAC `Role`/`RoleBinding` scoped to a team.
+ NetworkPolicy isolation between tenants.
+ A `default` namespace gets none of this and is shared by every chart that forgets to set `namespace:`, which is exactly why workloads there are painful to attribute, budget, or delete safely.

[Table of Contents](#Kubernetes)

## In the following file which service and in which namespace is referred?

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: some-configmap
data:
  some_url: silicon.chip
```

Answer - It's referencing the service "silicon" in the namespace called "chip". The `name.namespace` form is the DNS shorthand used inside a cluster; a fully qualified name would be `silicon.chip.svc.cluster.local`. A bare `silicon` would mean the service in the *same* namespace as the pod doing the lookup.

[Table of Contents](#Kubernetes)

## What is an Operator?

"Operators are software extensions to K8s which make use of custom resources to manage applications and their components. Operators follow Kubernetes principles, notably the control loop."

In practice an Operator = Custom Resource Definition (CRD) + a controller that reconciles the desired state. Data-platform examples: Strimzi (Kafka), Flink Kubernetes Operator, Spark Operator, CloudNativePG, Airflow's official Helm chart plus community operators.

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: events
  namespace: streaming
spec:
  kafka:
    replicas: 3
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 1Ti
          deleteClaim: false
    config:
      min.insync.replicas: 2
  zookeeper:
    replicas: 3
```

Applying that one object creates StatefulSets, Services, ConfigMaps, and PDBs, and the controller keeps them converged - including safe rolling restarts and rebalancing.

[Table of Contents](#Kubernetes)

## Why do we need Operators?

The process of managing applications in Kubernetes isn't as straightforward as managing stateless applications, where reaching the desired status and upgrades are both handled the same way for every replica. In stateful applications, upgrading each replica might require different handling due to the stateful nature of the app, each replica might be in a different status. As a result, we often need a human operator to manage stateful applications. Kubernetes Operator is supposed to assist with this.

This will also help with automating a standard process on multiple Kubernetes clusters.

What an operator buys you for a data system:

+ **Domain-aware rolling upgrades.** Strimzi drains a Kafka broker and waits for under-replicated partitions before moving on; a plain Deployment would restart all brokers at once.
+ **Ordering and quorum.** ZooKeeper/KRaft, Cassandra, and Elasticsearch need a specific start order and cluster-formation logic.
+ **Day-2 tasks.** Scaling a cluster, rebalancing, taking a snapshot, and triggering a backup become CRD fields instead of runbooks.
+ **Drift correction.** The control loop re-creates a deleted broker or re-attaches a lost volume.

The cost is that an operator is code you did not write; pin its version, review its CRDs on upgrade, and understand its failure modes before you trust it with a tier-1 cluster.

[Table of Contents](#Kubernetes)

## What is GKE?

GKE is Google Kubernetes Engine that is used for managing and orchestrating systems for Docker containers. With the help of Google Public Cloud, we can also orchestrate the container cluster. It is a managed control plane: Google runs the API server, scheduler, and controller-manager, and you pay for the worker node pools (or use Autopilot, where Google also manages the nodes).

Data-platform equivalents: **EKS** on AWS and **AKS** on Azure. The relevant managed features for data workloads are node auto-provisioning, spot/preemptible node pools, workload identity for passwordless access to object storage and warehouses, and cluster autoscaling that lets a Spark backfill burst and then release the nodes.

[Table of Contents](#Kubernetes)

## What is Ingress Default Backend?

It specifies what to do with an incoming request to the Kubernetes cluster that isn't mapped to any backend i.e what to do when no rules being defined for the incoming HTTP request. If the default backend service is not defined, it's recommended to define it so that users still see some kind of message instead of an unclear error.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: catch-all
spec:
  ingressClassName: nginx
  defaultBackend:
    service:
      name: maintenance-page
      port:
        number: 80
```

A default backend returns a controlled 404 or a maintenance page for unknown hosts/paths. Without one, users see the ingress controller's raw default (nginx 404), which is confusing and can leak controller details.

[Table of Contents](#Kubernetes)

## How to run Kubernetes locally?

Kubernetes can be set up locally using the Minikube tool. It runs a single-node bunch in a VM on the computer. Therefore, it offers the perfect way for users who have just ongoing learning Kubernetes.

Current options and when to use each:

| Tool | Shape | Good for |
|---|---|---|
| minikube | single-node VM/container | full-feature learning, addons (ingress, metrics-server) |
| kind | Kubernetes in Docker | CI, testing manifests quickly |
| k3d / k3s | lightweight distribution | edge, low-resource labs |
| Docker Desktop | bundled single node | quick local service testing |

```bash
minikube start --cpus=4 --memory=8g
minikube addons enable ingress
minikube addons enable metrics-server
kubectl create namespace data
kubectl apply -f manifests/orders-job.yaml -n data
kubectl get pods -n data -w
```

A local Spark run with `spark-submit --master k8s://...` against minikube is a good way to learn the manifest shape before touching a shared cluster.

[Table of Contents](#Kubernetes)

## What is Kubernetes Load Balancing?

Load Balancing is one of the most common and standard ways of exposing the services. There are two types of load balancing in K8s and they are:

Internal load balancer - This type of balancer automatically balances loads and allocates the pods with the required incoming load.

External Load Balancer - This type of balancer directs the traffic from the external loads to backend pods.

Concretely:

+ **Internal**: `ClusterIP` services plus cluster DNS. Pod-to-pod and service-to-service traffic, load balanced by kube-proxy.
+ **External**: `NodePort` (L4, one port per node), `LoadBalancer` (cloud LB), or `Ingress`/Gateway (L7).

```bash
kubectl get svc -n data
kubectl get endpointslices -n data     # the actual pod IPs behind a service
kubectl describe svc warehouse-api -n data
```

For data workloads, "load balancing" also describes distributing work across pods - for example an Airflow Celery queue routed to a worker pool, or Spark task scheduling. Kubernetes service load balancing distributes *connections*, not work items, and a long-lived gRPC/streaming connection can pin to one pod. That is what service meshes and headless services with client-side balancing solve.

[Table of Contents](#Kubernetes)

## What the following in the Deployment configuration file mean?

Given:

```yaml
spec:
  containers:
    - name: app
      env:
        - name: USER_PASSWORD
          valueFrom:
            secretKeyRef:
              name: some-secret
              key: password
```

Explanation - USER_PASSWORD environment variable will store the value from the password key in the secret called "some-secret" In other words, you reference a value from a Kubernetes Secret.

Related reference styles:

```yaml
env:
  - name: USER_PASSWORD
    valueFrom:
      secretKeyRef:
        name: some-secret
        key: password
        optional: false
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: log_level
  - name: POD_NAME
    valueFrom:
      fieldRef:
        fieldPath: metadata.name
```

```bash
kubectl create secret generic some-secret \
  --from-literal=password='...' -n data
```

Caution: environment variables are visible in `kubectl describe pod` output to anyone with read access to the pod (not the value, but `envFrom`/`secretKeyRef` can be misconfigured), are baked into the container process, and do not rotate without a restart. Prefer mounting Secrets as files for credentials that rotate, and prefer workload identity over static keys entirely.

[Table of Contents](#Kubernetes)

## What is the difference between Docker Swarm and Kubernetes?

Below are the main difference between Kubernetes and Docker:

The installation procedure of the K8s is very complicated but if it is once installed then the cluster is robust. On the other hand, the Docker swarm installation process is very simple but the cluster is not at all robust.

Kubernetes can process the auto-scaling but the Docker swarm cannot process the auto-scaling of the pods based on incoming load.

Kubernetes is a full-fledged Framework. Since it maintains the cluster states more consistently so autoscaling is not as fast as Docker Swarm.

| Aspect | Docker Swarm | Kubernetes |
|---|---|---|
| Setup | one command | many components, or a managed control plane |
| Autoscaling | limited | HPA/VPA/cluster autoscaler |
| Ecosystem | Docker-native only | huge: operators, Helm, service mesh, CNI/CSI |
| Stateful workloads | basic | StatefulSets, PDBs, operators |
| Scheduling | simple spread | rich affinity, taints, priorities, preemption |
| Best fit | small/simple deployments | data platforms and multi-tenant clusters |

For data engineering the deciding factor is not raw scheduling but the surrounding ecosystem: Spark's native Kubernetes backend, Airflow's KubernetesExecutor, and the Strimzi/Flink/Trino operators all target the Kubernetes API. That is why Swarm is rarely the answer in a data-platform interview.

[Table of Contents](#Kubernetes)

## How to troubleshoot if the POD is not getting scheduled?

In K8's scheduler is responsible to spawn pods into nodes. There are many factors that can lead to unstartable POD. The most common one is running out of resources, use the commands like `kubectl describe <POD> -n <Namespace>` to see the reason why POD is not started. Also, keep an eye on `kubectl get events` to see all events coming from the cluster.

```bash
kubectl get pods -n data -o wide            # find the Pending pod
kubectl describe pod orders-etl-abc -n data # look at the Events section
kubectl get events -n data --sort-by=.lastTimestamp
kubectl get nodes -o custom-columns=\
NAME:.metadata.name,CPU:.status.allocatable.cpu,MEM:.status.allocatable.memory,TAINTS:.spec.taints
```

Read the event message; it names the cause:

| Event | Meaning | Fix |
|---|---|---|
| `Insufficient cpu` / `memory` | no node has the requested capacity | lower requests, add a node pool, or free capacity |
| `0/N nodes are available ... node(s) had taint` | node selector/toleration mismatch | add the toleration or change the selector |
| `node(s) didn't match Pod's node affinity` | affinity rules exclude all nodes | relax the affinity |
| `volume node affinity conflict` | PVC is bound to another zone | schedule into that zone or use a zonal-scoped claim |
| `exceeded quota` | namespace ResourceQuota hit | raise the quota or free resources |
| `Unschedulable: PodDisruptionBudget` | not scheduling, but eviction blocked | restore replicas or relax the PDB |

Also check the topology spread constraints and the priority class: a low-priority pod waits behind a higher-priority one when the cluster is full.

[Table of Contents](#Kubernetes)

## How to run a POD on a particular node?

Various methods are available to achieve it.

nodeName: specify the name of a node in POD spec configuration, it will try to run the POD on a specific node.

nodeSelector: Assign a specific label to the node which has special resources and use the same label in POD spec so that POD will run only on that node.

nodeaffinities: required DuringSchedulingIgnoredDuringExecution, preferredDuringSchedulingIgnoredDuringExecution are hard and soft requirements for running the POD on specific nodes. This will be replacing nodeSelector in the future. It depends on the node labels.

```yaml
spec:
  nodeName: ip-10-0-3-17.ec2.internal    # bypasses the scheduler; avoid in production
```

```yaml
spec:
  nodeSelector:
    node-pool: spark
    topology.kubernetes.io/zone: us-east-1a
```

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: node-pool
                operator: In
                values: ["spark"]
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 80
          preference:
            matchExpressions:
              - key: lifecycle
                operator: In
                values: ["spot"]
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            topologyKey: kubernetes.io/hostname
            labelSelector:
              matchLabels: {app: kafka}
```

For data workloads, `nodeSelector` for a GPU pool plus a toleration for the pool's taint is the standard pattern; a Spark executor that needs an instance type should express it as affinity, not as a hard `nodeName`, so the scheduler can still pack and scale the pool.

[Table of Contents](#Kubernetes)

## What are the different ways to provide external network connectivity to K8?

By default, POD should be able to reach the external network but vice-versa we need to make some changes. Following options are available to connect with POD from the outer world.

Nodeport (it will expose one port on each node to communicate with it)

Load balancers (L4 layer of TCP/IP protocol)

Ingress (L7 layer of TCP/IP Protocol)

Another method is to use Kube-proxy which can expose a service with only cluster IP on the local system port.

```bash
kubectl proxy --port=8080
# then: http://localhost:8080/api/v1/namespaces/data/services/warehouse-api:http/proxy/
```

Two more options worth naming: **Gateway API** (the successor to Ingress, with richer routing and multi-team ownership) and **port-forward** for debugging only:

```bash
kubectl port-forward svc/warehouse-api 8080:80 -n data
```

For egress to the outside world, the pattern is the reverse: a NAT gateway, an egress gateway with a static IP (when a vendor allow-lists an IP), or a NetworkPolicy that permits only the destinations a job needs.

[Table of Contents](#Kubernetes)

## How can we forward the port 8080 container to 8080 service to 8080 ingress to 80 browser and how it can be done?

The ingress is exposing port 80 externally for the browser to access, and connecting to a service that listens on 8080. The ingress will listen on port 80 by default. An "ingress controller" is a pod that receives external traffic and handles the ingress and is configured by an ingress resource. For this you need to configure the ingress selector and if no 'ingress controller selector' is mentioned then no ingress controller will manage the ingress.

Simple ingress config will look like:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: abc-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: abc.org
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: abc-service
                port:
                  number: 8080
```

Then the service will look like:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: abc-service
spec:
  selector:
    app: abc
  ports:
    - protocol: TCP
      port: 8080          # port the service listens on
      targetPort: 8080    # port the container listens on
```

Finally, the container declares the same port:

```yaml
spec:
  containers:
    - name: abc
      image: registry.example.com/data/abc:1.0.0
      ports:
        - containerPort: 8080
```

The chain in one line: browser `http://abc.org:80` -> ingress controller (80) -> Service `abc-service:8080` -> pod endpoint `:8080` -> container process. Each hop has its own port number and they do not have to match; the `targetPort` is what ties the service to the container. If the browser times out, check in order: DNS resolves, the ingress has an external address, the ingress controller is running, the Service has endpoints, and the container is actually listening.

[Table of Contents](#Kubernetes)

## How do you configure liveness, readiness, and startup probes?

Probes are how Kubernetes decides whether a container is alive and whether it should receive traffic. Getting them wrong is a classic cause of cascading restarts.

+ **readinessProbe** - gates traffic. A failing readiness probe removes the pod from the Service endpoints but leaves it running.
+ **livenessProbe** - restarts the container when it is stuck (deadlock, exhausted thread pool). It must not fail during normal slow operation.
+ **startupProbe** - protects a slow-starting container; until it succeeds, liveness and readiness are disabled.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: warehouse-api
  namespace: data
spec:
  replicas: 3
  selector:
    matchLabels: {app: warehouse-api}
  template:
    metadata:
      labels: {app: warehouse-api}
    spec:
      containers:
        - name: api
          image: registry.example.com/data/warehouse-api:2.3.0
          ports:
            - containerPort: 8080
          startupProbe:
            httpGet: {path: /healthz, port: 8080}
            failureThreshold: 30
            periodSeconds: 10          # up to 5 minutes to start
          readinessProbe:
            httpGet: {path: /ready, port: 8080}
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 3
          livenessProbe:
            httpGet: {path: /healthz, port: 8080}
            periodSeconds: 20
            timeoutSeconds: 3
            failureThreshold: 3
```

Guidance that prevents incidents:

+ A liveness probe should check the process is responsive, not that a downstream dependency is up. If the liveness probe fails when the warehouse is briefly unreachable, Kubernetes restarts every pod and the outage gets worse.
+ Readiness is where you check dependencies: the API is not ready to serve until its metadata database is reachable.
+ Use `exec` probes only when HTTP/TCP cannot express the check; a shell-based probe needs the binary inside the image and is easy to get wrong.
+ For batch Jobs, probes are usually unnecessary: the process either exits 0 or it does not.

[Table of Contents](#Kubernetes)

## How do you use node selectors, affinity, and tolerations?

Selectors and affinity attract a pod to a node; taints and tolerations are the node-side counterpart that repels pods unless they explicitly tolerate the taint.

```bash
# label a dedicated Spark pool, then taint it so only Spark jobs land there
kubectl label node ip-10-0-3-17 node-pool=spark
kubectl taint node ip-10-0-3-17 workload=spark:NoSchedule
```

```yaml
spec:
  nodeSelector:
    node-pool: spark
  tolerations:
    - key: workload
      operator: Equal
      value: spark
      effect: NoSchedule
  containers:
    - name: spark-executor
      image: registry.example.com/data/spark:3.5.3
```

Choose the mechanism deliberately:

| Mechanism | Strength | Use for |
|---|---|---|
| `nodeSelector` | hard, exact label match | simple pool placement |
| `nodeAffinity` required | hard, expressive | instance type / zone / GPU |
| `nodeAffinity` preferred | soft | cost preference (spot over on-demand) |
| `podAntiAffinity` | avoids co-location | spread brokers/executors across nodes |
| `topologySpreadConstraints` | even spread across zones | multi-AZ resilience |
| taints + tolerations | reserves nodes | dedicated Spark, GPU, or licensing pools |

```yaml
# spread executor pods evenly across zones
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels: {app: spark-executor}
```

The classic interview answer: use a taint on a dedicated pool so no random pod consumes it, give your Spark/Airflow pods the matching toleration, and use pod anti-affinity to avoid all executors on one node.

[Table of Contents](#Kubernetes)

## How do you autoscale a data workload with the Horizontal Pod Autoscaler?

The HPA scales the replica count of a Deployment or StatefulSet (and, with newer APIs, custom resources) based on metrics. It needs the metrics-server or a custom-metrics adapter.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: warehouse-api
  namespace: data
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: warehouse-api
  minReplicas: 3
  maxReplicas: 30
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 30
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 65
    - type: Pods
      pods:
        metric: {name: kafka_consumer_lag}
        target:
          type: AverageValue
          averageValue: "10000"
```

Important limitations for data engineering:

+ The HPA does **not** replace the cluster autoscaler. If no node has capacity, new pods stay Pending; the cluster autoscaler (or Karpenter) adds nodes.
+ The HPA is poorly suited to batch Jobs - a Job already declares its parallelism, and a run is not a long-lived service. Scale batch work with `spark.executor.instances`, dynamic allocation, or job queueing instead.
+ Queue-driven scaling (Kafka lag, SQS depth, Airflow queue length) is the right trigger for streaming consumers and worker pools; CPU utilization alone lags the real backlog.
+ Always set `minReplicas` above one for a tier-1 service and a `stabilizationWindowSeconds` long enough to avoid flapping.

[Table of Contents](#Kubernetes)

## How do you run Spark on Kubernetes?

Spark has a native Kubernetes backend: `spark-submit` talks to the Kubernetes API server, creates a driver pod, and the driver creates executor pods. There is no Spark master or worker process to manage.

```bash
spark-submit \
  --master k8s://https://<api-server>:443 \
  --deploy-mode cluster \
  --name orders-daily \
  --conf spark.kubernetes.namespace=data \
  --conf spark.kubernetes.container.image=registry.example.com/data/spark:3.5.3 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.executor.instances=20 \
  --conf spark.executor.cores=4 \
  --conf spark.executor.memory=12g \
  --conf spark.driver.cores=2 \
  --conf spark.driver.memory=4g \
  --conf spark.kubernetes.executor.request.cores=4 \
  --conf spark.kubernetes.executor.limit.cores=6 \
  --conf spark.dynamicAllocation.enabled=true \
  --conf spark.dynamicAllocation.minExecutors=2 \
  --conf spark.dynamicAllocation.maxExecutors=60 \
  --conf spark.kubernetes.executor.deleteOnTermination=true \
  --conf spark.kubernetes.driver.podTemplateFile=driver-pod-template.yaml \
  --conf spark.kubernetes.executor.podTemplateFile=executor-pod-template.yaml \
  s3://acme-code/jobs/orders_daily.py
```

A pod template is how you attach node selectors, tolerations, volumes, and sidecars to the driver and executors:

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: spark
spec:
  nodeSelector:
    node-pool: spark
  tolerations:
    - key: workload
      operator: Equal
      value: spark
      effect: NoSchedule
  containers:
    - name: spark-kubernetes-executor
      resources:
        requests:
          cpu: "4"
          memory: "16Gi"
        limits:
          cpu: "6"
          memory: "18Gi"
      volumeMounts:
        - name: shuffle
          mountPath: /tmp/spark-local
  volumes:
    - name: shuffle
      emptyDir:
        sizeLimit: 100Gi
```

Operational reality:

+ **Use cluster mode**, not client mode, for production: the driver runs in-cluster and survives your laptop disconnecting.
+ **`spark.kubernetes.executor.request.cores` is the request; `spark.executor.cores` must not exceed it**, or executors get throttled and shuffle throughput collapses.
+ Executors are separate pods, so a node failure kills several executors at once; Spark retries the stages, but shuffle data on `emptyDir` is lost.
+ Pod startup adds 10-60 seconds per executor. For short jobs the overhead dominates; for the same workload check whether a managed runtime (Databricks, EMR, Dataproc) is cheaper in engineering time.
+ Use image pull secrets and pre-pulled images on the node pool to avoid the startup penalty, and set `spark.kubernetes.executor.deleteOnTermination` deliberately.

[Table of Contents](#Kubernetes)

## How do you run Airflow workers on Kubernetes?

Two patterns coexist. With `KubernetesExecutor`, each task gets its own pod (or the whole DAG, with `pod_override`). With `CeleryKubernetesExecutor` (Airflow 2) or multi-executor config (Airflow 3), long-running workers are Celery pods and only heavy tasks go to Kubernetes.

Worker deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airflow-worker
  namespace: airflow
spec:
  replicas: 4
  selector:
    matchLabels: {app: airflow-worker}
  template:
    metadata:
      labels: {app: airflow-worker}
    spec:
      serviceAccountName: airflow-worker
      terminationGracePeriodSeconds: 120
      containers:
        - name: worker
          image: registry.example.com/data/airflow:3.3.0
          command: ["airflow", "celery", "worker"]
          env:
            - name: AIRFLOW__CELERY__BROKER_URL
              valueFrom:
                secretKeyRef: {name: airflow-broker, key: url}
            - name: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
              valueFrom:
                secretKeyRef: {name: airflow-metadata, key: url}
          resources:
            requests: {cpu: "1", memory: 2Gi}
            limits: {cpu: "2", memory: 4Gi}
          readinessProbe:
            exec:
              command: ["airflow", "jobs", "check", "--job-type", "CeleryWorker"]
            initialDelaySeconds: 30
            periodSeconds: 30
```

Per-task pod template for KubernetesExecutor:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: placeholder
spec:
  serviceAccountName: airflow-worker
  nodeSelector:
    node-pool: general
  containers:
    - name: base
      image: registry.example.com/data/airflow:3.3.0
      resources:
        requests: {cpu: "500m", memory: 1Gi}
        limits: {cpu: "2", memory: 4Gi}
  restartPolicy: Never
```

Guidance:

+ Set the worker `terminationGracePeriodSeconds` longer than the longest task, and use `[celery] worker_autoscale` or KEDA to scale on queue depth.
+ Give the pod template a service account that can only create pods in the Airflow namespace - `KubernetesExecutor` needs pod create/delete permissions, and a wildcard role there is a real privilege-escalation risk.
+ Mount `dags/`, `logs/`, and `plugins/` from object storage or a PVC; the scheduler and workers must see the same DAG files and log directory, or tasks fail with import errors.
+ Log to stdout and ship to the central stack; `remote_logging` to S3/GCS is the alternative and is what makes task logs survive pod deletion.

[Table of Contents](#Kubernetes)

## How do you manage secrets and configuration for data workloads?

ConfigMaps hold non-sensitive configuration; Secrets hold credentials, but a Kubernetes Secret is only base64-encoded by default, so encryption at rest and RBAC matter.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: orders-etl-config
  namespace: data
data:
  LOG_LEVEL: "INFO"
  TARGET_TABLE: "analytics.orders"
  spark-defaults.conf: |
    spark.sql.shuffle.partitions=400
    spark.sql.adaptive.enabled=true
---
apiVersion: v1
kind: Secret
metadata:
  name: warehouse-credentials
  namespace: data
type: Opaque
stringData:
  username: etl_user
  password: "REPLACE_WITH_SECRET"
```

Mount configuration as a file when the tool expects a config file, and as env vars only for simple scalars:

```yaml
spec:
  containers:
    - name: orders-etl
      image: registry.example.com/data/orders-etl:1.14.2
      envFrom:
        - configMapRef: {name: orders-etl-config}
        - secretRef: {name: warehouse-credentials}
      volumeMounts:
        - name: spark-config
          mountPath: /opt/spark/conf
          readOnly: true
  volumes:
    - name: spark-config
      configMap: {name: orders-etl-config}
```

Best practice in order of preference:

1. **Workload identity / IRSA / Workload Identity Federation** - the pod assumes a cloud role and gets short-lived credentials. No static secret at all.
2. **External secret manager** (Vault, AWS Secrets Manager, GCP Secret Manager) synced into a Secret by an operator, with rotation.
3. **Sealed/encrypted GitOps secrets** (Sealed Secrets, SOPS) so the ciphertext can live in git.
4. Plain `kubectl create secret` - acceptable for a lab, not for a multi-team cluster.

Also restrict access with RBAC (`get` on Secrets is powerful), enable encryption at rest with a KMS key, and never put a credential in a ConfigMap or an image layer.

[Table of Contents](#Kubernetes)

## How do you run a scheduled data pipeline with a CronJob?

A CronJob is the Kubernetes-native scheduler for a containerized batch job. It is a good fit for self-contained jobs (an extract, a compaction, a small load) and a poor fit for pipelines with many dependent steps - that is what Airflow, Dagster, or Argo Workflows are for.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: orders-hourly-load
  namespace: data
spec:
  schedule: "15 * * * *"
  timeZone: "UTC"
  concurrencyPolicy: Forbid
  suspend: false
  startingDeadlineSeconds: 300
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 5
  jobTemplate:
    spec:
      activeDeadlineSeconds: 5400
      backoffLimit: 2
      ttlSecondsAfterFinished: 172800
      template:
        spec:
          restartPolicy: OnFailure
          serviceAccountName: orders-loader
          containers:
            - name: load
              image: registry.example.com/data/orders-loader:1.7.0
              args:
                - "--window-start"
                - "$(date -u -d '1 hour ago' +%Y-%m-%dT%H:00:00Z)"
              resources:
                requests: {cpu: "1", memory: 2Gi}
                limits: {cpu: "2", memory: 4Gi}
              envFrom:
                - secretRef: {name: warehouse-credentials}
```

Fields that matter:

+ `concurrencyPolicy: Forbid` prevents a slow run from overlapping the next one - essential when both write the same target.
+ `startingDeadlineSeconds` + `activeDeadlineSeconds` bound a stuck job instead of letting it run for days.
+ `suspend: true` is the kill switch during an incident, without deleting the object.
+ `ttlSecondsAfterFinished` cleans up completed Job objects so the namespace does not accumulate thousands of them.
+ Use `schedule` in UTC unless the business window is genuinely in a local timezone; `timeZone` exists but timezone-aware schedules surprise people during DST changes.

For anything with more than two or three dependent steps, put the orchestration in Airflow and let Kubernetes run the tasks, rather than encoding dependencies with multiple CronJobs.

[Table of Contents](#Kubernetes)

## Real world use cases for Kubernetes

### 1. Spark batch platform on EKS with spot node pools

A retail data team runs 300-500 Spark jobs a night (2-40 minutes each, 30-80 executors) over a 900 TB lake on S3. Steady-state on-demand capacity would be idle most of the day.

```bash
spark-submit \
  --master k8s://https://<eks-api>:443 \
  --deploy-mode cluster \
  --conf spark.kubernetes.namespace=spark-batch \
  --conf spark.kubernetes.container.image=registry.example.com/data/spark:3.5.3 \
  --conf spark.kubernetes.executor.podTemplateFile=spot-executor.yaml \
  --conf spark.dynamicAllocation.enabled=true \
  --conf spark.dynamicAllocation.maxExecutors=200 \
  s3://acme-code/jobs/nightly_batch.py
```

```yaml
# spot-executor.yaml
apiVersion: v1
kind: Pod
metadata:
  labels: {app: spark-executor}
spec:
  nodeSelector:
    capacity-type: spot
  tolerations:
    - key: capacity-type
      operator: Equal
      value: spot
      effect: NoSchedule
  terminationGracePeriodSeconds: 120
```

Why this design: executors are ephemeral, so spot interruption is tolerable - Spark retries the lost tasks. Cluster autoscaler + Karpenter add nodes for the nightly burst and release them by morning, which is the cost lever. Drivers run in-cluster so CI and laptops can disconnect. The trade-off is task re-execution and shuffle loss on interruption, which is why jobs checkpoint to S3 and use dynamic allocation instead of fixed executor counts.

### 2. Multi-tenant Airflow on Kubernetes with per-team isolation

A fintech central platform team serves 14 data teams on one Airflow deployment. Each task runs in its own pod with the team's image and service account, and each namespace has a quota.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-payments-quota
  namespace: airflow-payments
spec:
  hard:
    requests.cpu: "40"
    requests.memory: 160Gi
    limits.cpu: "80"
    limits.memory: 320Gi
    pods: "120"
```

```yaml
# the task pod template points at the team's service account
spec:
  serviceAccountName: airflow-payments
  nodeSelector:
    node-pool: general
```

Why this design: KubernetesExecutor gives per-task image and resource isolation, so the payments team can pin a different Spark client or Python version without breaking another team. RBAC plus namespace quotas stop one team's runaway backfill from starving the rest. The trade-off is 10-30 seconds of pod startup per task - fine for distributed stores, painful for thousands of tiny tasks, which is why small tasks stay on a Celery pool.

### 3. Streaming ingestion with Kafka/Flink operators

A logistics company ingests 120k events/second from 40k vehicles through Kafka (retention 7 days) and enriches them with a Flink job. Both clusters are managed by operators rather than hand-written StatefulSets.

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: vehicle-enrichment
  namespace: streaming
spec:
  image: registry.example.com/data/flink:1.20
  flinkVersion: v1_20
  serviceAccount: flink
  jobManager:
    resource: {cpu: 2, memory: "4g"}
    replicas: 2
  taskManager:
    resource: {cpu: 4, memory: "8g"}
  job:
    jarURI: s3://acme-code/flink/vehicle-enrichment.jar
    parallelism: 24
    upgradeMode: savepoint
    state: running
```

Why this design: the operator handles the ordered rolling upgrade with a savepoint, restarts on failure, and rebalances partitions - the work a plain Deployment cannot do safely. A 2-JM / 24-TM shape tolerates one JM loss and scales with the event rate. The trade-off is that operator CRDs are another upgrade surface and the team must understand savepoint compatibility before changing parallelism or state.

### 4. Self-service dbt runs as Kubernetes Jobs

A 60-person analytics org has 900 dbt models. Instead of a central Airflow DAG, a service accepts a run request and creates a Kubernetes Job with the requested selector.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: dbt-run-
  namespace: analytics
spec:
  backoffLimit: 0
  ttlSecondsAfterFinished: 3600
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: dbt
          image: registry.example.com/data/dbt:1.9
          command: ["dbt", "build", "--select", "tag:finance", "--target", "prod"]
          env:
            - name: DBT_PROFILES_DIR
              value: /opt/dbt
            - name: DBT_SNOWFLAKE_PASSWORD
              valueFrom:
                secretKeyRef: {name: dbt-snowflake, key: password}
          resources:
            requests: {cpu: "500m", memory: 1Gi}
            limits: {cpu: "1", memory: 2Gi}
```

Why this design: each run is isolated, logged, and garbage-collected by TTL, and the image pins the dbt version so a model change cannot break another team's run. `backoffLimit: 0` makes a failed run fail fast and surface the error instead of silently retrying a bad model. The trade-off is no built-in DAG-level dependency management; the caller (Airflow, a CI job, or a small control plane) owns ordering.

[Table of Contents](#Kubernetes)
