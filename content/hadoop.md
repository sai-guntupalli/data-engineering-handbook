## [Main title](../README.md)
### [Interview questions](full.md)

# HADOOP

**Notebook:** [`notebooks/topics/hadoop.ipynb`](../notebooks/topics/hadoop.ipynb) - runnable version of this topic with self-checking exercises.

+ [What are the main components of a Hadoop Application?](#What-are-the-main-components-of-a-Hadoop-Application)
+ [What is the role of HDFS in a big data platform?](#What-is-the-role-of-HDFS-in-a-big-data-platform)
+ [Why are small files a problem in Hadoop?](#Why-are-small-files-a-problem-in-Hadoop)
+ [What is the core concept behind Apache Hadoop framework?](#What-is-the-core-concept-behind-Apache-Hadoop-framework)
+ [What is Hadoop Streaming?](#What-is-Hadoop-Streaming)
+ [What is the difference between Nodes in HDFS?](#What-is-the-difference-between-Nodes-in-HDFS)
+ [What is the optimum hardware configuration to run Apache Hadoop?](#What-is-the-optimum-hardware-configuration-to-run-Apache-Hadoop)
+ [What do you know about Block and Block scanner in HDFS?](#What-do-you-know-about-Block-and-Block-scanner-in-HDFS)
+ [What are the default port numbers on which Nodes run in Hadoop?](#What-are-the-default-port-numbers-on-which-Nodes-run-in-Hadoop)
+ [How will you disable a Block Scanner on HDFS DataNode?](#How-will-you-disable-a-Block-Scanner-on-HDFS-DataNode)
+ [How will you get the distance between two nodes in Apache Hadoop?](#How-will-you-get-the-distance-between-two-nodes-in-Apache-Hadoop)
+ [Why do we use commodity hardware in Hadoop?](#Why-do-we-use-commodity-hardware-in-Hadoop)
+ [How does inter cluster data copying works in Hadoop?](#How-does-inter-cluster-data-copying-works-in-Hadoop)
+ [How can we update a file at an arbitrary location in HDFS?](#How-can-we-update-a-file-at-an-arbitrary-location-in-HDFS)
+ [What is Replication factor in HDFS?](#What-is-Replication-factor-in-HDFS)
+ [What is the difference between NAS and DAS in Hadoop cluster?](#What-is-the-difference-between-NAS-and-DAS-in-Hadoop-cluster)
+ [What are the two messages that NameNode receives from DataNode?](#What-are-the-two-messages-that-NameNode-receives-from-DataNode)
+ [How does indexing work in Hadoop?](#How-does-indexing-work-in-Hadoop)
+ [What data is stored in a HDFS NameNode?](#What-data-is-stored-in-a-HDFS-NameNode)
+ [What would happen if NameNode crashes in a HDFS cluster?](#What-would-happen-if-NameNode-crashes-in-a-HDFS-cluster)
+ [What are the main functions of Secondary NameNode?](#What-are-the-main-functions-of-Secondary-NameNode)
+ [What happens if HDFS file is set with replication factor of 1 and DataNode crashes?](#What-happens-if-HDFS-file-is-set-with-replication-factor-of-1-and-DataNode-crashes)
+ [What is the meaning of Rack Awareness in Hadoop?](#What-is-the-meaning-of-Rack-Awareness-in-Hadoop)
+ [How will you check if a file exists in HDFS?](#How-will-you-check-if-a-file-exists-in-HDFS)
+ [Why do we use fsck command in HDFS?](#Why-do-we-use-fsck-command-in-HDFS)
+ [What will happen when NameNode is down and a user submits a new job?](#What-will-happen-when-NameNode-is-down-and-a-user-submits-a-new-job)
+ [What are the core methods of a Reducer in Hadoop?](#What-are-the-core-methods-of-a-Reducer-in-Hadoop)
+ [What are the primary phases of a Reducer in Hadoop?](#What-are-the-primary-phases-of-a-Reducer-in-Hadoop)
+ [What is the use of Context object in Hadoop?](#What-is-the-use-of-Context-object-in-Hadoop)
+ [How does partitioning work in Hadoop?](#How-does-partitioning-work-in-Hadoop)
+ [What is a Combiner in Hadoop?](#What-is-a-Combiner-in-Hadoop)
+ [What is the default replication factor in HDFS?](#What-is-the-default-replication-factor-in-HDFS)
+ [How much storage is allocated by HDFS for storing a file of 25 MB size?](#How-much-storage-is-allocated-by-HDFS-for-storing-a-file-of-25-MB-size)
+ [Why does HDFS store data in Block structure?](#Why-does-HDFS-store-data-in-Block-structure)
+ [How will you create a custom Partitioner in a Hadoop job?](#How-will-you-create-a-custom-Partitioner-in-a-Hadoop-job)
+ [What is a Checkpoint node in HDFS?](#What-is-a-Checkpoint-node-in-HDFS)
+ [What is a Backup Node in HDFS?](#What-is-a-Backup-Node-in-HDFS)
+ [What is the meaning of term Data Locality in Hadoop?](#What-is-the-meaning-of-term-Data-Locality-in-Hadoop)
+ [What is a Balancer in HDFS?](#What-is-a-Balancer-in-HDFS)
+ [What are the important points a NameNode considers before selecting the DataNode for placing a data block?](#What-are-the-important-points-a-NameNode-considers-before-selecting-the-DataNode-for-placing-a-data-block)
+ [What is Safemode in HDFS?](#What-is-Safemode-in-HDFS)
+ [How will you replace HDFS data volume before shutting down a DataNode?](#How-will-you-replace-HDFS-data-volume-before-shutting-down-a-DataNode)
+ [What are the important configuration files in Hadoop?](#What-are-the-important-configuration-files-in-Hadoop)
+ [How will you monitor memory used in a Hadoop cluster?](#How-will-you-monitor-memory-used-in-a-Hadoop-cluster)
+ [Why do we need Serialization in Hadoop map reduce methods?](#Why-do-we-need-Serialization-in-Hadoop-map-reduce-methods)
+ [What is the use of Distributed Cache in Hadoop?](#What-is-the-use-of-Distributed-Cache-in-Hadoop)
+ [How will you synchronize the changes made to a file in Distributed Cache in Hadoop?](#How-will-you-synchronize-the-changes-made-to-a-file-in-Distributed-Cache-in-Hadoop)
+ [Can you elaborate about Mapreduce job?](#Can-you-elaborate-about-Mapreduce-job)
+ [Why compute nodes and the storage nodes are the same?](#Why-compute-nodes-and-the-storage-nodes-are-the-same)
+ [What is the configuration object importance in Mapreduce?](#What-is-the-configuration-object-importance-in-Mapreduce)
+ [Where Mapreduce not recommended?](#Where-Mapreduce-not-recommended)
+ [What is Namenode and it’s responsibilities?](#What-is-Namenode-and-its-responsibilities)
+ [What is Jobtracker’s responsibility?](#What-is-Jobtrackers-responsibility)
+ [What are the Jobtracker and Tasktracker?](#What-are-the-Jobtracker-and-Tasktracker)
+ [What is Job scheduling importance in Hadoop Mapreduce?](#What-is-Job-scheduling-importance-in-Hadoop-Mapreduce)
+ [When used Reducer?](#When-used-Reducer)
+ [Where the Shuffle and Sort process does?](#Where-the-Shuffle-and-Sort-process-does)
+ [Java is mandatory to write Mapreduce Jobs?](#Java-is-mandatory-to-write-Mapreduce-Jobs)
+ [What methods can controle the Map And Reduce function’s output?](#What-methods-can-controle-the-Map-And-Reduce-functions-output)
+ [What is the main difference between Mapper And Reducer?](#What-is-the-main-difference-between-Mapper-And-Reducer)
+ [Why compute Nodes and the Storage Nodes are same?](#Why-compute-Nodes-and-the-Storage-Nodes-are-same)
+ [What is difference between mapside join and reduce side join?](#What-is-difference-between-mapside-join-and-reduce-side-join)
+ [What happen if number of Reducer is 0?](#What-happen-if-number-of-Reducer-is-0)
+ [When we are goes to Combiner?](#When-we-are-goes-to-Combiner)
+ [What is the main difference between Mapreduce Combiner and Reducer?](#What-is-the-main-difference-between-Mapreduce-Combiner-and-Reducer)
+ [What is partition?](#What-is-partition)
+ [When we goes to Partition?](#When-we-goes-to-Partition)
+ [What are the important steps when you are partitioning table?](#What-are-the-important-steps-when-you-are-partitioning-table)
+ [Can you elaborate Mapreduce Job architecture?](#Can-you-elaborate-Mapreduce-Job-architecture)
+ [Why task Tracker launch child Jvm?](#Why-task-Tracker-launch-child-Jvm)
+ [Why Jobclient and Job Tracker submits job resources to file system?](#Why-Jobclient-and-Job-Tracker-submits-job-resources-to-file-system)
+ [How many Mappers and Reducers can run?](#How-many-Mappers-and-Reducers-can-run)
+ [What is Inputsplit?](#What-is-Inputsplit)
+ [How to configure the split value?](#How-to-configure-the-split-value)
+ [How much ram required to process 64mb data?](#How-much-ram-required-to-process-64mb-data)
+ [What is difference between block And split?](#What-is-difference-between-block-And-split)
+ [Why Hadoop Framework reads a file parallel why not sequential?](#Why-Hadoop-Framework-reads-a-file-parallel-why-not-sequential)
+ [If I am change block size from 64 to 128?](#If-I-am-change-block-size-from-64-to-128)
+ [What is Issplitable()?](#What-is-Issplitable)
+ [How much Hadoop allows maximum block size and minimum block size?](#How-much-Hadoop-allows-maximum-block-size-and-minimum-block-size)
+ [What are the Job Resource files?](#What-are-the-Job-Resource-files)
+ [What’s the Mapreduce Job consists?](#Whats-the-Mapreduce-Job-consists)
+ [What is the data locality?](#What-is-the-data-locality)
+ [What is speculative execution?](#What-is-speculative-execution)
+ [What is chain Mapper?](#What-is-chain-Mapper)
+ [How to do value level comparison?](#How-to-do-value-level-comparison)
+ [What is setup and clean up methods?](#What-is-setup-and-clean-up-methods)
+ [How many slots allocate for each task?](#How-many-slots-allocate-for-each-task)
+ [Why Tasktracker launch child Jvm to do a task?](#Why-Tasktracker-launch-child-Jvm-to-do-a-task)
+ [What main configuration parameters are specified in Mapreduce?](#What-main-configuration-parameters-are-specified-in-Mapreduce)
+ [What is identity Mapper?](#What-is-identity-Mapper)
+ [What is RecordReader in a MapReduce?](#What-is-RecordReader-in-a-MapReduce)
+ [What is OutputCommitter?](#What-is-OutputCommitter)
+ [What are the parameters of Mappers and Reducers?](#What-are-the-parameters-of-Mappers-and-Reducers)
+ [Explain Jobconf in Mapreduce?](#Explain-Jobconf-in-Mapreduce)
+ [Explain Job scheduling through Jobtracker?](#Explain-Job-scheduling-through-Jobtracker)
+ [What is SequenceFileInputFormat?](#What-is-SequenceFileInputFormat)
+ [Explain how input and output data format of the Hadoop Framework?](#Explain-how-input-and-output-data-format-of-the-Hadoop-Framework)
+ [What are the restriction to the Key and Value Class?](#What-are-the-restriction-to-the-Key-and-Value-Class)
+ [Explain the wordcount implementation via Hadoop Framework?](#Explain-the-wordcount-implementation-via-Hadoop-Framework)
+ [How Mapper is instantiated in a running Job?](#How-Mapper-is-instantiated-in-a-running-Job)
+ [Which are the methods in the Mapper Interface?](#Which-are-the-methods-in-the-Mapper-Interface)
+ [What happens if You don't Override the Mapper methods and keep them as it is?](#What-happens-if-You-dont-Override-the-Mapper-methods-and-keep-them-as-it-is)
+ [What is the use of context Object?](#What-is-the-use-of-context-Object)
+ [How can you Add the arbitrary Key value pairs in your Mapper?](#How-can-you-Add-the-arbitrary-Key-value-pairs-in-your-Mapper)
+ [How does Mapper's run method works?](#How-does-Mappers-run-method-works)
+ [Which Object can be used to get the progress of a particular Job?](#Which-Object-can-be-used-to-get-the-progress-of-a-particular-Job)
+ [What is next step after Mapper Or Maptask?](#What-is-next-step-after-Mapper-Or-Maptask)
+ [How can we control particular Key should go in a specific Reducer?](#How-can-we-control-particular-Key-should-go-in-a-specific-Reducer)
+ [What is the use of Combiner?](#What-is-the-use-of-Combiner)
+ [How many Maps are there in a particular Job?](#How-many-Maps-are-there-in-a-particular-Job)
+ [What is the Reducer used for?](#What-is-the-Reducer-used-for)
+ [Explain the core methods of the Reducer?](#Explain-the-core-methods-of-the-Reducer)
+ [What are the primary phases of the Reducer?](#What-are-the-primary-phases-of-the-Reducer)
+ [Explain the Shuffle?](#Explain-the-Shuffle)
+ [Explain the Reducer's sort phase?](#Explain-the-Reducers-sort-phase)
+ [Explain the Reducer's reduce phase?](#Explain-the-Reducers-reduce-phase)
+ [How many Reducers should be configured?](#How-many-Reducers-should-be-configured)
+ [It can be possible that a Job has 0 Reducers?](#It-can-be-possible-that-a-Job-has-0-Reducers)
+ [What happens if number of Reducers are 0?](#What-happens-if-number-of-Reducers-are-0)
+ [How many instances of Jobtracker can run on a Hadoop Cluster?](#How-many-instances-of-Jobtracker-can-run-on-a-Hadoop-Cluster)
+ [What is the Jobtracker and what it performs in a Hadoop Cluster?](#What-is-the-Jobtracker-and-what-it-performs-in-a-Hadoop-Cluster)
+ [How a task is scheduled by a Jobtracker?](#How-a-task-is-scheduled-by-a-Jobtracker)
+ [How many instances of Tasktracker run on a Hadoop Cluster?](#How-many-instances-of-Tasktracker-run-on-a-Hadoop-Cluster)
+ [How many maximum Jvm can run on a Slave Node?](#How-many-maximum-Jvm-can-run-on-a-Slave-Node)
+ [What is Nas?](#What-is-Nas)
+ [How Hdfs differs with Nfs?](#How-Hdfs-differs-with-Nfs)
+ [How does a NameNode handle the failure of the Data Nodes?](#How-does-a-NameNode-handle-the-failure-of-the-Data-Nodes)
+ [Can Reducer talk with each other?](#Can-Reducer-talk-with-each-other)
+ [Where the Mapper's intermediate data will be stored?](#Where-the-Mappers-intermediate-data-will-be-stored)
+ [What is the Hadoop Mapreduce api contract for a Key and Value Class?](#What-is-the-Hadoop-Mapreduce-api-contract-for-a-Key-and-Value-Class)
+ [What is a IdentityMapper and IdentityReducer in Mapreduce?](#What-is-a-IdentityMapper-and-IdentityReducer-in-Mapreduce)
+ [What is the meaning of Speculative Execution in Hadoop?](#What-is-the-meaning-of-Speculative-Execution-in-Hadoop)
+ [How Hdfs is different from traditional File Systems?](#How-Hdfs-is-different-from-traditional-File-Systems)
+ [What is Hdfs block size and how is it different from Traditional File System block size?](#What-is-Hdfs-block-size-and-how-is-it-different-from-Traditional-File-System-block-size)
+ [What is a NameNode and how many instances of NameNode run on a Hadoop Cluster?](#What-is-a-NameNode-and-how-many-instances-of-NameNode-run-on-a-Hadoop-Cluster)
+ [How the client communicates with Hdfs?](#How-the-client-communicates-with-Hdfs)
+ [How the Hdfs blocks are replicated?](#How-the-Hdfs-blocks-are-replicated)
+ [Can you give some examples of Big Data?](#Can-you-give-some-examples-of-Big-Data)
+ [What is the basic difference between traditional Rdbms and Hadoop?](#What-is-the-basic-difference-between-traditional-Rdbms-and-Hadoop)
+ [What is structured and unstructured Data?](#What-is-structured-and-unstructured-Data)
+ [Since the data is replicated thrice in Hdfs so does it mean that any calculation done on One Node will also be replicated on the other Two?](#Since-the-data-is-replicated-thrice-in-Hdfs-so-does-it-mean-that-any-calculation-done-on-One-Node-will-also-be-replicated-on-the-other-Two)
+ [What is throughput and how does Hdfs get a good throughput?](#What-is-throughput-and-how-does-Hdfs-get-a-good-throughput)
+ [What is streaming access?](#What-is-streaming-access)
+ [What is a Commodity Hardware so does Commodity Hardware include Ram?](#What-is-a-Commodity-Hardware-so-does-Commodity-Hardware-include-Ram)
+ [Is NameNode also a Commodity?](#Is-NameNode-also-a-Commodity)
+ [What is a Metadata?](#What-is-a-Metadata)
+ [What is a Daemon?](#What-is-a-Daemon)
+ [What is a Heartbeat in Hdfs?](#What-is-a-Heartbeat-in-Hdfs)
+ [How indexing is done in Hdfs?](#How-indexing-is-done-in-Hdfs)
+ [If a Data Node is full how it's identified?](#If-a-Data-Node-is-full-how-its-identified)
+ [If DataNodes increase then do we need to upgrade NameNode?](#If-DataNodes-increase-then-do-we-need-to-upgrade-NameNode)
+ [Are Job Tracker and Task Trackers present in separate machines?](#Are-Job-Tracker-and-Task-Trackers-present-in-separate-machines)
+ [On what basis NameNode will decide which DataNode to write on?](#On-what-basis-NameNode-will-decide-which-DataNode-to-write-on)
+ [Who is a user in Hdfs?](#Who-is-a-user-in-Hdfs)
+ [Is client the end user in Hdfs?](#Is-client-the-end-user-in-Hdfs)
+ [What is the Communication Channel between client and NameNode/DataNode?](#What-is-the-Communication-Channel-between-client-and-NameNodeDataNode)
+ [What is a Rack?](#What-is-a-Rack)
+ [On what basis Data will be stored on a Rack?](#On-what-basis-Data-will-be-stored-on-a-Rack)
+ [Do we need to place 2nd and 3rd Data in Rack 2 only?](#Do-we-need-to-place-2nd-and-3rd-Data-in-Rack-2-only)
+ [What if Rack 2 and DataNode fails?](#What-if-Rack-2-and-DataNode-fails)
+ [What is the difference between Gen1 and Gen2 Hadoop with regards to the NameNode?](#What-is-the-difference-between-Gen1-and-Gen2-Hadoop-with-regards-to-the-NameNode)
+ [Do we require two servers for the NameNode and the DataNodes?](#Do-we-require-two-servers-for-the-NameNode-and-the-DataNodes)
+ [Why are the number of splits equal to the number of Maps?](#Why-are-the-number-of-splits-equal-to-the-number-of-Maps)
+ [Is a Job split into maps?](#Is-a-Job-split-into-maps)
+ [Which are the two types of writes In Hdfs?](#Which-are-the-two-types-of-writes-In-Hdfs)
+ [Why reading is done in parallel and writing is not in Hdfs?](#Why-reading-is-done-in-parallel-and-writing-is-not-in-Hdfs)
+ [Can Hadoop be compared to Nosql Database like Cassandra?](#Can-Hadoop-be-compared-to-Nosql-Database-like-Cassandra)
+ [How JobTracker schedules a task?](#How-JobTracker-schedules-a-task)
+ [What is a Task Tracker in Hadoop and how many instances of Task Tracker run on a Hadoop Cluster?](#What-is-a-Task-Tracker-in-Hadoop-and-how-many-instances-of-Task-Tracker-run-on-a-Hadoop-Cluster)
+ [What is a task instance in Hadoop and where does it run?](#What-is-a-task-instance-in-Hadoop-and-where-does-it-run)
+ [What is configuration of a typical Slave Node on Hadoop Cluster and how many Jvms run on a Slave Node?](#What-is-configuration-of-a-typical-Slave-Node-on-Hadoop-Cluster-and-how-many-Jvms-run-on-a-Slave-Node)
+ [How NameNode handles DataNode failures?](#How-NameNode-handles-DataNode-failures)
+ [Does Mapreduce programming model provide a way for Reducers to communicate with each other and in a Mapreduce Job can a Reducer communicate with another Reducer?](#Does-Mapreduce-programming-model-provide-a-way-for-Reducers-to-communicate-with-each-other-and-in-a-Mapreduce-Job-can-a-Reducer-communicate-with-another-Reducer)
+ [Can I set the number of Reducers to Zero?](#Can-I-set-the-number-of-Reducers-to-Zero)
+ [Where is the Mapper Output intermediate Kay value data stored?](#Where-is-the-Mapper-Output-intermediate-Kay-value-data-stored)
+ [If Reducers do not start before all Mappers finish then why does the progress on Mapreduce Job shows something like Map 50 percents Reduce 10 percents and why Reducers progress percentage is displayed when Mapper is not Finished yet?](#If-Reducers-do-not-start-before-all-Mappers-finish-then-why-does-the-progress-on-Mapreduce-Job-shows-something-like-Map-50-percents-Reduce-10-percents-and-why-Reducers-progress-percentage-is-displayed-when-Mapper-is-not-Finished-yet)
+ [Explain in brief the three Modes in which Hadoop can be run?](#Explain-in-brief-the-three-Modes-in-which-Hadoop-can-be-run)
+ [Explain what are the features of Standalone local Mode?](#Explain-what-are-the-features-of-Standalone-local-Mode)
+ [What are the features of fully distributed mode?](#What-are-the-features-of-fully-distributed-mode)
+ [Explain what are the main features Of pseudo mode?](#Explain-what-are-the-main-features-Of-pseudo-mode)
+ [What are the port numbers of NameNode and JobTracker and TaskTracker?](#What-are-the-port-numbers-of-NameNode-and-JobTracker-and-TaskTracker)
+ [Tell us what is a spill factor with respect to the ram?](#Tell-us-what-is-a-spill-factor-with-respect-to-the-ram)
+ [Is fs.mapr working for a single directory?](#Is-fs.mapr-working-for-a-single-directory)
+ [Which are the three main Hdfs-site.xml properties?](#Which-are-the-three-main-Hdfs-site.xml-properties)
+ [How can I restart Namenode?](#How-can-I-restart-Namenode)
+ [How can we check whether Namenode is working or not?](#How-can-we-check-whether-Namenode-is-working-or-not)
+ [At times you get a connection refused Java Exception when you run the file system check command Hadoop fsck?](#At-times-you-get-a-connection-refused-Java-Exception-when-you-run-the-file-system-check-command-Hadoop-fsck)
+ [What is the use of the command Mapred.job.tracker?](#What-is-the-use-of-the-command-Mapred.job.tracker)
+ [What does etc/init.d do?](#What-does-etc.init.d-do)
+ [How can we look for the Namenode in the browser?](#How-can-we-look-for-the-Namenode-in-the-browser)
+ [What do masters and slaves consist of?](#What-do-masters-and-slaves-consist-of)
+ [What is the function Of Hadoop-env.sh and where is it present?](#What-is-the-function-Of-Hadoop-env.sh-and-where-is-it-present)
+ [Can we have multiple entries in the master files?](#Can-we-have-multiple-entries-in-the-master-files)
+ [In Hadoop_pid_dir and what does pid stands for?](#In-Hadoop_pid_dir-and-what-does-pid-stands-for)
+ [What does Hadoop-metrics and properties file do?](#What-does-Hadoop-metrics-and-properties-file-do)
+ [What are the network requirements for hadoop?](#What-are-the-network-requirements-for-hadoop)
+ [Why do we need a passwordless ssh in fully distributed environment?](#Why-do-we-need-a-passwordless-ssh-in-fully-distributed-environment)
+ [What will happen if a NameNode has no data?](#What-will-happen-if-a-NameNode-has-no-data)
+ [What happens to job tracker when NameNode is down?](#What-happens-to-job-tracker-when-NameNode-is-down)
+ [Explain what do you mean by formatting of the Dfs?](#Explain-what-do-you-mean-by-formatting-of-the-Dfs)
+ [We use Unix variants for hadoop and can we use Microsoft Windows for the same?](#We-use-Unix-variants-for-hadoop-and-can-we-use-Microsoft-Windows-for-the-same)
+ [Which one decides the input split hdfs client or NameNode?](#Which-one-decides-the-input-split-hdfs-client-or-NameNode)
+ [Can you tell me if we can create a hadoop cluster from scratch?](#Can-you-tell-me-if-we-can-create-a-hadoop-cluster-from-scratch)
+ [Explain the significance of ssh and what is the port on which port does ssh work and why do we need password in ssh local host?](#Explain-the-significance-of-ssh-and-what-is-the-port-on-which-port-does-ssh-work-and-why-do-we-need-password-in-ssh-local-host)
+ [What is ssh and explain in detail about ssh communication between masters and the slaves?](#What-is-ssh-and-explain-in-detail-about-ssh-communication-between-masters-and-the-slaves)
+ [Can you tell is what will happen to a NameNode and when Job tracker is not up and running?](#Can-you-tell-is-what-will-happen-to-a-NameNode-and-when-Job-tracker-is-not-up-and-running)
+ [What are the key trade-offs in Hadoop and when should you move off it?](#What-are-the-key-trade-offs-in-Hadoop-and-when-should-you-move-off-it)
+ [Real world use cases for Hadoop](#Real-world-use-cases-for-Hadoop)

## What are the main components of a Hadoop Application?
Over the time, there are various forms in which a Hadoop application is defined. But in most of the cases there are following four core components of Hadoop application:
+ HDFS: This is the file system in which Hadoop data is stored. It is a distributed file system with very high bandwidth.
+ Hadoop Common: This is common set of libraries and utilities used by Hadoop.
+ Hadoop MapReduce: This is based on MapReduce algorithm for providing large-scale data processing.
+ Hadoop YARN: This is used for resource management in a Hadoop cluster. It can also schedule tasks for users.

```text
HDFS          - distributed storage: NameNode, DataNodes, blocks, replicas
YARN          - cluster resource manager: ResourceManager, NodeManagers, containers
MapReduce     - batch execution: Mapper, Reducer, shuffle and sort
Hadoop Common - shared libraries, RPC, configuration, filesystem abstraction

Modern clusters often keep HDFS/YARN for storage and scheduling but replace
MapReduce with Spark or Tez as the execution engine.
```

[Table of Contents](#HADOOP)

## What is the role of HDFS in a big data platform?
HDFS stores large files across a cluster by splitting them into blocks and replicating those blocks for fault tolerance. It is optimized for high-throughput reads and writes of large datasets, not low-latency updates to many small files.

Example:

```text
1 TB file -> blocks distributed across DataNodes -> NameNode tracks metadata
```

The NameNode manages file metadata, while DataNodes store the actual blocks. Modern cloud platforms often replace HDFS storage with object storage, but the same concepts of partitioning, file sizing, and distributed reads still matter.

```bash
# HDFS shell commands that come up in almost every interview
hdfs dfs -mkdir -p /data/orders/ds=2026-10-04
hdfs dfs -put ./orders.json /data/orders/ds=2026-10-04/
hdfs dfs -ls -h /data/orders/ds=2026-10-04/
hdfs dfs -du -s -h /data/orders
hdfs dfs -cat /data/orders/ds=2026-10-04/part-00000 | head -5
hdfs dfs -get /data/orders/ds=2026-10-04/part-00000 ./local.json
hdfs dfs -rm -r -skipTrash /data/orders/ds=2026-10-04/
```

[Table of Contents](#HADOOP)

## Why are small files a problem in Hadoop?
Small files create metadata pressure on the NameNode and reduce processing efficiency. Each file has metadata, and many tiny files create too many tasks with too little work per task. This hurts Spark, Hive, and MapReduce jobs.

Example fix:

```text
many 1 MB JSON files -> compact into fewer 256 MB Parquet files
```

Compaction improves scan efficiency, reduces file listing overhead, and makes downstream jobs more stable.

```bash
# First measure the damage: file count and average size per partition
hdfs dfs -count -q -h /data/logs/2026/10/04
hdfs dfs -ls /data/logs/2026/10/04 | wc -l

# Option 1 - Hadoop Archive (HAR) packs many files into one archive
hadoop archive -archiveName logs.har -p /data/logs/2026/10/04 /data/archive

# Option 2 - preferred: rewrite into a few large Parquet files
spark-submit --class com.acme.CompactLogs /opt/jobs/compact-logs.jar \
  --input  hdfs:///data/logs/2026/10/04 \
  --output hdfs:///data/logs_compact/2026/10/04 \
  --target-files 8
```

[Table of Contents](#HADOOP)

## What is the core concept behind Apache Hadoop framework?
Apache Hadoop is based on the concept of MapReduce algorithm. In MapReduce algorithm, Map and Reduce operations are used to process very large data set.
    In this concept, Map method does the filtering and sorting of data. Reduce method performs the summarizing of data.
    This is a concept from functional programming.
    The key points in this concept are scalability and fault tolerance. In Apache Hadoop these features are achieved by multi-threading and efficient implementation of MapReduce.

[Table of Contents](#HADOOP)

## What is Hadoop Streaming?
Hadoop distribution provides a Java utility called Hadoop Streaming. It is packaged in a jar file. With Hadoop Streaming, we can create and run Map Reduce jobs with an executable script.
    We can create executable scripts for Mapper and Reducer functions. These executable scripts are passed to Hadoop Streaming in a command.
    Hadoop Streaming utility creates Map and Reduce jobs and submits these to a cluster. We can also monitor these jobs with this utility.

```python
# mapper.py - read lines from stdin and emit "word\t1"
import sys

for line in sys.stdin:
    for word in line.strip().split():
        print(f"{word}\t1")
```

```python
# reducer.py - sum the counts that arrive sorted by key
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split("\t", 1)
    count = int(count)
    if word == current_word:
        current_count += count
    else:
        if current_word is not None:
            print(f"{current_word}\t{current_count}")
        current_word, current_count = word, count

if current_word is not None:
    print(f"{current_word}\t{current_count}")
```

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -D mapreduce.job.name=wordcount-streaming \
  -D mapreduce.job.reduces=4 \
  -files mapper.py,reducer.py \
  -mapper  "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input  /data/books \
  -output /data/wordcount-out
```

[Table of Contents](#HADOOP)

## What is the difference between Nodes in HDFS?
The differences between NameNode, BackupNode and Checkpoint NameNode are as follows:
+ NameNode: NameNode is at the heart of the HDFS file system that manages the metadata i.e. the data of the files is not stored on the NameNode but rather it has the directory tree of all the files present in the HDFS file system on a Hadoop cluster. NameNode uses two files for the namespace:
    + fsimage file: This file keeps track of the latest checkpoint of the namespace.
    + edits file: This is a log of changes made to the namespace since checkpoint.
+ Checkpoint Node:	Checkpoint Node keeps track of the latest checkpoint in a directory that has same structure as that of NameNode’s directory.
            Checkpoint node creates checkpoints for the namespace at regular intervals by downloading the edits and fsimage file from the NameNode and merging it locally. The new image is then again updated back to the active NameNode.
+ BackupNode: This node also provides check pointing functionality like that of the Checkpoint node but it also maintains its up-to-date in-memory copy of the file system namespace that is in sync with the active NameNode.

[Table of Contents](#HADOOP)

## What is the optimum hardware configuration to run Apache Hadoop?
To run Apache Hadoop jobs, it is recommended to use dual core machines or dual processors. There should be 4GB or 8GB RAM with the processor with Error-correcting code (ECC) memory.
    Without ECC memory, there is high chance of getting checksum errors.
    For storage high capacity SATA drives (around 7200 rpm) should be used in Hadoop cluster.
    Around 10GB bandwidth Ethernet networks are good for Hadoop.

[Table of Contents](#HADOOP)

## What do you know about Block and Block scanner in HDFS?
A large file in HDFS is broken into multiple parts and each part is stored on a different Block. By default a Block is 128 MB in Hadoop 2/3 (64 MB in Hadoop 1.x).
    Block Scanner is a program that every Data node in HDFS runs periodically to verify the checksum of every block stored on the data node.
    The purpose of a Block Scanner is to detect any data corruption errors on Data node.

[Table of Contents](#HADOOP)

## What are the default port numbers on which Nodes run in Hadoop?
Default port numbers of Name Node, Job Tracker and Task Tracker are as follows:
    NameNode UI runs on port 9870 (50070 on Hadoop 2)
    Task Tracker (Hadoop 1.x) runs on port 50060
    Job Tracker (Hadoop 1.x) runs on port 50030

```text
Component                     Hadoop 3     Hadoop 2 / 1.x
NameNode UI                   9870         50070
NameNode RPC                  8020         9000
DataNode data transfer        9866         50010
YARN ResourceManager UI       8088         -
YARN ResourceManager RPC      8032         -
MapReduce JobHistory UI       19888        -
JobTracker (Hadoop 1.x)       -            50030
TaskTracker (Hadoop 1.x)      -            50060
```

[Table of Contents](#HADOOP)

## How will you disable a Block Scanner on HDFS DataNode?
In HDFS, there is a configuration dfs.datanode.scan.period.hours in hdfs-site.xml to set the number of hours interval at which Block Scanner should run.
    We can set dfs.datanode.scan.period.hours=0 to disable the Block Scanner. It means it will not run on HDFS DataNode.

```xml
<!-- hdfs-site.xml -->
<configuration>
  <property>
    <name>dfs.datanode.scan.period.hours</name>
    <value>0</value>
    <description>0 disables the block scanner; default 504 hours (21 days).</description>
  </property>
</configuration>
```

[Table of Contents](#HADOOP)

## How will you get the distance between two nodes in Apache Hadoop?
In Apache Hadoop we can use NetworkTopology.getDistance() method to get the distance between two nodes.
    Distance from a node to its parent is considered as 1.

[Table of Contents](#HADOOP)

## Why do we use commodity hardware in Hadoop?
Hadoop does not require a very high-end server with large memory and processing power. Due to this we can use any inexpensive system with average RAM and processor. Such kind of system is called commodity hardware.
    Since there is parallel processing in Hadoop MapReduce, it is convenient to distribute a task among multiple servers and then do the execution. It saves cost as well as it is much faster compared to other options. Another benefit of using commodity hardware in Hadoop is scalability. Commodity hardware is readily available in market. Whenever we need to scale up our operations in Hadoop cluster we can obtain more commodity hardware. In case of high-end machines, we have to raise purchase orders and get them built on demand.

[Table of Contents](#HADOOP)

## How does inter cluster data copying works in Hadoop?
In Hadoop, there is a utility called DistCP (Distributed Copy) to perform large inter/intra-cluster copying of data. This utility is also based on MapReduce. It creates Map tasks for files given as input.
    After every copy using DistCP, it is recommended to run crosschecks to confirm that there is no data corruption and copy is complete.

```bash
# DistCp between two HDFS clusters, preserving files, permissions and checksums
hadoop distcp -m 20 -bandwidth 100 \
  hdfs://src-nn:8020/data/orders/ds=2026-10-04 \
  hdfs://dst-nn:8020/data/orders/ds=2026-10-04

# DistCp to object storage (S3A); verify file count and sizes afterwards
hadoop distcp -Dfs.s3a.access.key="$AWS_ACCESS_KEY_ID" \
  -Dfs.s3a.secret.key="$AWS_SECRET_ACCESS_KEY" \
  hdfs:///data/orders s3a://acme-lake/orders
```

[Table of Contents](#HADOOP)

## How can we update a file at an arbitrary location in HDFS?
This is a trick question. In HDFS, it is not allowed to update a file at an arbitrary location. All the files are written in append only mode. It means all writes are done at the end of a file.
    So there is no possibility of updating the files at any random location.

```bash
# HDFS is append-only: you can add at the end, never edit in the middle
hdfs dfs -appendToFile local_delta.txt /data/orders/orders.csv

# For real updates, write a new file and atomically swap the partition/table
hdfs dfs -mv /data/orders_new/ds=2026-10-04 /data/orders/ds=2026-10-04
```

[Table of Contents](#HADOOP)

## What is Replication factor in HDFS?
Replication factor in HDFS is the number of copies of a file in file system. A Hadoop application can specify the number of replicas of a file it wants HDFS to maintain. This information is stored in NameNode. We can set the replication factor in following ways:
    We can use Hadoop fs shell, to specify the replication factor for a file. Command as follows:
+ hdfs dfs -setrep -w 5 /file_name
    In above command, replication factor of file_name  file is set as 5.
    We can also use Hadoop fs shell, to specify the replication factor of all the files in a directory.
+ hdfs dfs -setrep -w 2 /dir_name
    In above command, replication factor of all the files under directory dir_name is set as 2.

```bash
# Set replication for one file and for a whole directory tree
hdfs dfs -setrep -w 5 /data/orders/ds=2026-10-04/part-00000
hdfs dfs -setrep -w 2 /data/orders

# Verify the effective replication of every block
hdfs fsck /data/orders -files -blocks -locations
```

[Table of Contents](#HADOOP)

## What is the difference between NAS and DAS in Hadoop cluster?
NAS stands for Network Attached Storage and DAS stands for Direct Attached Storage.
    In NAS, compute and storage layers are separated. Storage is distributed over different servers on a network.
    In DAS, storage is attached to the node where computation takes place.
    Apache Hadoop is based on the principle of moving processing near the location of data. So it needs storage disk to be local to computation.
    With DAS, we get very good performance on a Hadoop cluster. Also DAS can be implemented on commodity hardware. So it is more cost effective.
    Only when we have very high bandwidth (around 10 GbE) it is preferable to use NAS storage.

[Table of Contents](#HADOOP)

## What are the two messages that NameNode receives from DataNode?
NameNode receives following two messages from every DataNode:
+  Heartbeat: This message signals that DataNode is still alive. Periodic receipt of Heartbeat is vey important for NameNode to decide whether to use a DataNode or not.
+  Block Report: This is a list of all the data blocks hosted on a DataNode. This report is also very useful for functioning of NameNode. With this report, NameNode gets information about what data is stored on a specific DataNode.

[Table of Contents](#HADOOP)

## How does indexing work in Hadoop?
Indexing in Hadoop has two different levels.
    Index based on File URI: In this case data is indexed based on different files. When we search for data, index will return the files that contain the data.
    Index based on InputSplit: In this case, data is indexed based on locations where input split is located.

[Table of Contents](#HADOOP)

## What data is stored in a HDFS NameNode?
NameNode is the central node of an HDFS system. It does not store any actual data on which MapReduce operations have to be done. But it has all the metadata about the data stored in HDFS DataNodes.
    NameNode has the directory tree of all the files in HDFS filesystem. Using this meta data it manages all the data stored in different DataNodes.

[Table of Contents](#HADOOP)

## What would happen if NameNode crashes in a HDFS cluster?
There is only one NameNode in a HDFS cluster. This node maintains metadata about DataNodes. Since there is only one NameNode, it is the single point of failure in a HDFS cluster. When NameNode crashes, system may become unavailable.
    We can specify a secondary NameNode in HDFS cluster. The secondary
    NameNode takes the periodic checkpoints of the file system in HDFS. But it is not the backup of NameNode. We can use it to recreate the NameNode and restart it in case of a crash.

[Table of Contents](#HADOOP)

## What are the main functions of Secondary NameNode?
Main functions of Secondary NameNode are as follows:
+ FsImage: It stores a copy of FsImage file and EditLog.
+ NameNode crash: In case NameNode crashes, we can use Secondary NameNode's FsImage to recreate the NameNode.
+ Checkpoint: Secondary NameNode runs Checkpoint to confirm that data is not corrupt in HDFS.

Update: It periodically applies the updates from EditLog to FsImage file. In this way FsImage file on Secondary NameNode is kept up to date. This helps in saving time during NameNode restart.

[Table of Contents](#HADOOP)

## What happens if HDFS file is set with replication factor of 1 and DataNode crashes?
Replication factor is same as the number of copies of a file on HDFS. If we set the replication factor of 1, it means there is only 1 copy of the file.
    In case, DataNode that has this copy of file crashes, the data is lost. There is no way to recover it. It is essential to keep replication factor of more than 1 for any business critical data.

[Table of Contents](#HADOOP)

## What is the meaning of Rack Awareness in Hadoop?
In Hadoop, most of the components like NameNode, DataNode etc are rack- aware. It means they have the information about the rack on which they exist. The main use of rack awareness is in implementing fault-tolerance.
    Any communication between nodes on same rack is much faster than the communication between nodes on two different racks.
    In Hadoop, NameNode maintains information about rack of each DataNode. While reading/writing data, NameNode tries to choose the DataNodes that are closer to each other. Due to performance reasons, it is recommended to use close data nodes for any operation. So Rack Awareness is an important concept for high performance and fault- tolerance in Hadoop.
    If we set Replication factor 3 for a file, does it mean any computation will also take place 3 times?
    No. Replication factor of 3 means that there are 3 copies of a file. But computation takes place only one the one copy of file. If the node on which first copy exists, does not respond then computation will be done on second copy.

```xml
<!-- core-site.xml: call an external script to resolve the rack of each host -->
<property>
  <name>net.topology.script.file.name</name>
  <value>/etc/hadoop/conf/topology.sh</value>
</property>
```

```bash
#!/usr/bin/env bash
# topology.sh - receives one host name per argument, prints its rack
while [ -n "$1" ]; do
  case "$1" in
    nn1|dn1|dn2) echo "/dc1/rack1" ;;
    dn3|dn4)     echo "/dc1/rack2" ;;
    *)           echo "/dc1/rack3" ;;
  esac
  shift
done
```

[Table of Contents](#HADOOP)

## How will you check if a file exists in HDFS?
The hdfs dfs -test options check the existence, length and type of a path. They are mainly used inside scripts because they return an exit code instead of printing output:
+ hdfs dfs -test -e file_uri checks that the path exists.
+ hdfs dfs -test -z file_uri checks that the file has zero length.
+ hdfs dfs -test -d file_uri checks that the path is a directory.

```bash
# -e exists, -z zero length, -d directory; the exit code is what scripts use
hdfs dfs -test -e /data/orders/ds=2026-10-04/_SUCCESS && echo "exists"
hdfs dfs -test -z /data/orders/ds=2026-10-04/part-00000 && echo "empty"
hdfs dfs -test -d /data/orders && echo "directory"

if hdfs dfs -test -e /data/orders/ds=2026-10-04/_SUCCESS; then
  echo "partition complete"
else
  echo "partition missing or still running"
  exit 1
fi
```

[Table of Contents](#HADOOP)

## Why do we use fsck command in HDFS?
fsck command is used for getting the details of files and directories in HDFS. Main uses of fsck command in HDFS are as follows:
+ delete: We use this option to delete files in HDFS.
+ move: This option is for moving corrupt files to lost/found.
+ locations: This option prints all the locations of a block in HDFS.
+ racks: This option gives the network topology of data-node locations.
+ blocks: This option gives the report of blocks in HDFS.

```bash
hdfs fsck /data/orders -files -blocks -locations   # file and block report
hdfs fsck /data/orders -list-corruptfileblocks     # names of corrupt files
hdfs fsck /data/orders -move                       # move corrupt blocks to /lost+found
hdfs fsck /data/orders -delete                     # delete corrupt replicas
hdfs fsck /data/orders -openforwrite               # files left open by failed writers
```

[Table of Contents](#HADOOP)

## What will happen when NameNode is down and a user submits a new job?
Since NameNode is the single point of failure in Hadoop, user job cannot execute. The job will fail when the NameNode is down. User will have to wait for NameNode to restart and come up, before running a job.

[Table of Contents](#HADOOP)

## What are the core methods of a Reducer in Hadoop?
The main task of Reducer is to reduce a larger set of data that shares a key to a smaller set of data. In Hadoop, Reducer has following three core methods:
+ setup(): At the start of a task, setup() method is called to configure various parameters for Reducer.
+ reduce(): This is the main operation of Reducer. In reduce() method we define the task that has to be done for a set of values that share a key.
+ cleanup(): Once reduce() task is done, we can use cleanup() to clean any intermediate data or temporary files.

[Table of Contents](#HADOOP)

## What are the primary phases of a Reducer in Hadoop?
In Hadoop, there are three primary phases of a Reducer:
+ Shuffle: In this phase, Reducer copies the sorted output from each Mapper.
+ Sort: In this phase, Hadoop framework sorts the input to Reducer by same key. It uses merge sort in this phase. Sometimes, shuffle and sort phases occur at the same time.
+ Reduce: This is the phase in which output values associated with a key are reduced to give output result. Output from Reducer is not re-sorted.

[Table of Contents](#HADOOP)

## What is the use of Context object in Hadoop?
Hadoop uses Context object with Mapper to interact with rest of the system. Context object gets the configuration of the system and job in its constructor.
    We use Context object to pass the information in setup(), cleanup() and map() methods. This is an important object that makes the important information available during the map operations.

```java
@Override
protected void setup(Context context) throws IOException, InterruptedException {
    Configuration conf = context.getConfiguration();   // job configuration
    context.getCounter("etl", "records").increment(1);
    context.setStatus("loading reference data");
}
```

[Table of Contents](#HADOOP)

## How does partitioning work in Hadoop?
Partitioning is the phase between Map phase and Reduce phase in Hadoop workflow. Since partitioner gives output to Reducer, the number of partitions is same as the number of Reducers.
    Partitioner will partition the output from Map phase into distinct partitions by using a user-defined condition.
    Partitions can be like Hash based buckets.
    E.g. If we have to find the student with the maximum marks in each gender in each subject. We can first use Map function to map the keys with each gender. Once mapping is done, the result is passed to Partitioner. Partitioner will partition each row with gender on the basis of subject. For each subject there will be a different Reducer. Reducer will take input from each partition and find the student with the highest marks.

```java
// Default partitioner: hash(key) % numReduceTasks
public class HashPartitioner<K, V> extends Partitioner<K, V> {
    @Override
    public int getPartition(K key, V value, int numReduceTasks) {
        return (key.hashCode() & Integer.MAX_VALUE) % numReduceTasks;
    }
}
```

```text
Key design rule: partition on the same key you group by. A poorly chosen
partitioner sends all hot keys to one reducer and creates data skew.
```

[Table of Contents](#HADOOP)

## What is a Combiner in Hadoop?
Combiner is an optional step between Map and Reduce. Combiner is also called Semi-Reducer. Combiner takes output from Map, creates Key-value pairs and passes these to Reducer.
    Combiner's task is to summarize the outputs from Map into summary records with same key.
    By using Combiner, we can reduce the data transfer between Mapper and
    Reducer. Combiner does the task similar to reduce but it is done on the Map machine itself.

```java
// Sum is commutative and associative, so it is safe to use as a combiner
job.setCombinerClass(IntSumReducer.class);
job.setReducerClass(IntSumReducer.class);
```

```text
Safe as a combiner : sum, max, min, count (and average if you emit sum+count)
Unsafe as a combiner: median, exact distinct count, order-dependent logic
```

[Table of Contents](#HADOOP)

## What is the default replication factor in HDFS?
Default replication factor in HDFS is 3. It means there will be 3 copies of each data.
    We can configure it with dfs.replication in hdfs-site.xml file.
    We can even set it from command line in Hadoop fs command.

[Table of Contents](#HADOOP)

## How much storage is allocated by HDFS for storing a file of 25 MB size?
This is a question to test the basic concepts of HDFS. In HDFS, all the data is stored in blocks. The size of block can be configured in HDFS.In Hadoop 2/3 the default block size is 128 MB (Hadoop 1.x used 64 MB). A file of 25 MB still occupies one whole block, so one block of capacity is reserved for it, and with replication factor 3 the physical usage is three blocks.

```text
Block size defaults:
  Hadoop 1.x : 64 MB
  Hadoop 2/3 : 128 MB (dfs.blocksize), configurable per file

A 25 MB file occupies exactly one block, so the reserved capacity is one
block (64 MB on Hadoop 1.x, 128 MB on Hadoop 2/3) rather than 25 MB.
With replication factor 3 the physical usage is 3 x block size.
```

[Table of Contents](#HADOOP)

## Why does HDFS store data in Block structure?
HDFS stores all the data in terms of Blocks. With Block structure there are some benefits that HDFS gets. Some of these are as follows:
        Fault Tolerance: With Block structure, HDFS implements replication. By replicating same block in multiple locations, fault tolerance of the system increases. Even if some copy is not accessible, we can get the data from another copy.
        Large Files: We can store very large files that cannot be even stored one disk, in HDFS by using Block structure. We just divide the data of file in multiple Blocks. Each Block can be stored on same or different machines.
        Storage management: With Block storage it is easier for Hadoop nodes to calculate the data storage as well as perform optimization in the algorithm to minimize data transfer across the network.

[Table of Contents](#HADOOP)

## How will you create a custom Partitioner in a Hadoop job?
Partition phase runs between Map and Reduce phase. It is an optional phase. We can create a custom partitioner by extending the org.apache.hadoop.mapreduce.Partitio class in Hadoop. In this class, we have to override getPartition(KEY key, VALUE value, int numPartitions) method.
    This method takes three inputs. In this method, numPartitions is same as the number of reducers in our job. We pass key and value to get the partition number to which this key,value record will be assigned. There will be a reducer corresponding to that partition. The reducer will further handle to summarizing of the data.Once custom Partitioner class is ready, we have to set it in the Hadoop job. We can use following method to set it:
        job.setPartitionerClass(CustomPartitioner)

```java
public class GenderSubjectPartitioner extends Partitioner<Text, IntWritable> {
    @Override
    public int getPartition(Text key, IntWritable value, int numPartitions) {
        String[] parts = key.toString().split("\\|");   // gender|subject
        return (parts[0].hashCode() & Integer.MAX_VALUE) % numPartitions;
    }
}
```

```java
job.setPartitionerClass(GenderSubjectPartitioner.class);
job.setNumReduceTasks(4);   // getPartition must return a value in [0, numPartitions)
```

[Table of Contents](#HADOOP)

## What is a Checkpoint node in HDFS?
A Checkpoint node in HDFS periodically fetches fsimage and edits from NameNode, and merges them. This merge result is called a Checkpoint. Once a Checkpoint is created, Checkpoint Node uploads the Checkpoint to NameNode. Secondary node also takes Checkpoint similar to Checkpoint Node. But it does not upload the Checkpoint to NameNode.
    Main benefit of Checkpoint Node is in case of any failure on NameNode. A NameNode does not merge its edits to fsimage automatically during the runtime. If we have long running task, the edits will become huge. When we restart NameNode, it will take much longer time, because it will first merge the edits. In such a scenario, Checkpoint node helps for a long running task.
    Checkpoint nodes performs the task of merging the edits with fsimage and then uploads these to NameNode. This saves time during the restart of NameNode.

```bash
# Force the active NameNode to write a new fsimage and start a fresh edits file
hdfs dfsadmin -saveNamespace
hdfs dfsadmin -rollEdits

# Inspect the checkpoint directory on the Secondary/Checkpoint NameNode
hdfs oiv -i fsimage_0000000000000001234 -p XML -o fsimage.xml
```

[Table of Contents](#HADOOP)

## What is a Backup Node in HDFS?
Backup Node in HDFS is similar to Checkpoint Node. It takes the stream of edits from NameNode. It keeps these edits in memory and also writes these to storage to create a new checkpoint. At any point of time, Backup Node is in sync with the Name Node.
    The difference between Checkpoint Node and Backup Node is that Backup Node does not upload any checkpoints to Name Node. Also Backup node takes a stream instead of periodic reading of edits from Name Node.

[Table of Contents](#HADOOP)

## What is the meaning of term Data Locality in Hadoop?
In a Big Data system, the size of data is huge. So it does not make sense to move data across the network. In such a scenario, Hadoop tries to move computation closer to data. So the Data remains local to the location wherever it was stored. But the computation tasks will be moved to data nodes that hold the data locally.
    Hadoop follows following rules for Data Locality optimization:
+ Hadoop first tries to schedule the task on node that has an HDFS file on a local disk. If it cannot be done, then Hadoop will try to schedule the task on a node on the same rack as the node that has data. If this also cannot be done, Hadoop will schedule the task on the node with same data on a different rack. The above method works well, when we work with the default replication factor of 3 in Hadoop.

[Table of Contents](#HADOOP)

## What is a Balancer in HDFS?
In HDFS, data is stored in blocks on a DataNode. There can be a situation when data is not uniformly spread into blocks on a DataNode. When we add a new DataNode to a cluster, we can face such a situation. In such a case, HDFS provides a useful tool Balancer to analyze the placement of blocks on a DataNode. Some people call it as Rebalancer also. This is an administrative tool used by admin staff. We can use this tool to spread the blocks in a uniform manner on a DataNode.

```bash
# Check capacity and usage per node, then rebalance
hdfs dfsadmin -report | grep -E "Name:|DFS Used%|Remaining"
hdfs balancer -threshold 10

# Limit the bandwidth used so balancing does not starve production jobs
hdfs dfsadmin -setBalancerBandwidth 104857600   # 100 MB/s
```

[Table of Contents](#HADOOP)

## What are the important points a NameNode considers before selecting the DataNode for placing a data block?
Some of the important points for selecting a DataNode by NameNode are as follows:
        NameNode tries to keep at least one replica of a Block on the same node that is writing the block.
        It tries to spread the different replicas of same block on different racks, so that in case of one rack failure, other rack has the data.
        One replica will be kept on a node on the same node as the one that it writing it. It is different from point 1. In Point 1, block is written to same node. In this point block is written on a different node on same rack. This is important for minimizing the network I/O. NameNode also tries to spread the blocks uniformly among all the DataNodes in a cluster.

[Table of Contents](#HADOOP)

## What is Safemode in HDFS?
Safemode is considered as the read-only mode of NameNode in a cluster. During the startup of NameNode, it is in SafeMode. It does not allow writing to file-system in Safemode. At this time, it collects data and statistics from all the DataNodes. Once it has all the data on blocks, it leaves Safemode.
    The main reason for Safemode is to avoid the situation when NameNode starts replicating data in DataNodes before collecting all the information from DataNodes. It may erroneously assume that a block is not replicated well enough, whereas, the issue is that NameNode does not know about whereabouts of all the replicas of a block. Therefore, in Safemode, NameNode first collects the information about how many replicas exist in cluster and then tries to create replicas wherever the number of replicas is less than the policy.

```bash
hdfs dfsadmin -safemode get
hdfs dfsadmin -safemode enter     # force read-only mode during maintenance
hdfs dfsadmin -safemode leave
hdfs dfsadmin -report             # capacity, live/dead DataNodes, under-replicated blocks
```

[Table of Contents](#HADOOP)

## How will you replace HDFS data volume before shutting down a DataNode?
In HDFS, DataNode supports hot swappable drives. With a swappable drive we can add or replace HDFS data volumes while the DataNode is still running. The procedure for replacing a hot swappable drive is as follows:
    First we format and mount the new drive. We update the DataNode configuration dfs.datanode.data.dir to reflect the data volume directories. Run the "dfsadmin -reconfig datanode HOST:PORT start" command to start the reconfiguration process Once the reconfiguration is complete, we just unmount the old data volume After unmount we can physically remove the old disks.

```bash
# 1. Mount the new disk and add it to dfs.datanode.data.dir in hdfs-site.xml
# 2. Reload the DataNode configuration without a full restart
hdfs dfsadmin -reconfig datanode dn5:9867 start
hdfs dfsadmin -reconfig datanode dn5:9867 status

# 3. Wait until the old volume drains, then unmount and physically remove it
hdfs dfsadmin -report
```

[Table of Contents](#HADOOP)

## What are the important configuration files in Hadoop?
There are two important configuration files in a Hadoop cluster:
+ Default Configuration: There are core-default.xml, hdfs-default.xml and mapred-default.xml files in which we specify the default configuration for Hadoop cluster. These are read only files.
+ Custom Configuration: We have site-specific custom files like core-site.xml, hdfs-site.xml, mapred-site.xml in which we can specify the site-specific configuration.

All the Jobs in Hadoop and HDFS implementation uses the parameters defined in the above-mentioned files. With customization we can tune these processes according to our use case. In Hadoop API, there is a Configuration class that loads these files and provides the values at run time to different jobs.

```xml
<!-- core-site.xml -->
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://nn1:8020</value>
  </property>
  <property>
    <name>io.file.buffer.size</name>
    <value>131072</value>
  </property>
</configuration>
```

```xml
<!-- hdfs-site.xml -->
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>3</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/data/1/dfs/nn,/data/2/dfs/nn</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/data/1/dfs/dn,/data/2/dfs/dn</value>
  </property>
</configuration>
```

```xml
<!-- mapred-site.xml -->
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>yarn.app.mapreduce.am.resource.mb</name>
    <value>2048</value>
  </property>
</configuration>
```

[Table of Contents](#HADOOP)

## How will you monitor memory used in a Hadoop cluster?
In Hadoop, TaskTracker is the one that uses high memory to perform a task. We can configure the TastTracker to monitor memory usage of the tasks it creates. It can monitor the memory usage to find the badly behaving tasks, so that these tasks do not bring the machine down with excess memory consumption. In memory monitoring we can also limit the maximum memory used by a tasks. We can even limit the memory usage per node. So that all the tasks executing together on a node do not consume more memory than a limit. Some of the parameters for setting memory monitoring in Hadoop are as follows:
        mapred.cluster.map.memory.mb, mapred.cluster.reduce.memory.mb: This is the size of virtual memory of a single map/reduce slot in a cluster of Map-Reduce framework. mapred.job.map.memory.mb, mapred.job.reduce.memory.mb: This is the default limit of memory
        set on each map/reduce task in Hadoop. mapred.cluster.max.map.memory.m mapred.cluster.max.reduce.memory This is the maximum limit of memory set on each map/reduce task in Hadoop.

```xml
<!-- yarn-site.xml: physical memory and vcores offered by each NodeManager -->
<configuration>
  <property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>98304</value>   <!-- 96 GB usable by containers on a 128 GB node -->
  </property>
  <property>
    <name>yarn.nodemanager.resource.cpu-vcores</name>
    <value>32</value>
  </property>
  <property>
    <name>yarn.scheduler.minimum-allocation-mb</name>
    <value>1024</value>
  </property>
  <property>
    <name>yarn.scheduler.maximum-allocation-mb</name>
    <value>32768</value>
  </property>
</configuration>
```

[Table of Contents](#HADOOP)

## Why do we need Serialization in Hadoop map reduce methods?
In Hadoop, there are multiple data nodes that hold data. During the processing of map and reduce methods data may transfer from one node to another node. Hadoop uses serialization to convert the data from Object structure to Binary format. With serialization, data can be converted to binary format and with de-serialization data can be converted back to Object format with reliability.

```java
public class Temperature implements WritableComparable<Temperature> {
    private String city;
    private double celsius;

    public Temperature() { }   // no-arg constructor is required for deserialization

    @Override
    public void write(DataOutput out) throws IOException {
        out.writeUTF(city);
        out.writeDouble(celsius);
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        city = in.readUTF();
        celsius = in.readDouble();
    }

    @Override
    public int compareTo(Temperature other) {
        return Double.compare(this.celsius, other.celsius);
    }
}
```

[Table of Contents](#HADOOP)

## What is the use of Distributed Cache in Hadoop?
Hadoop provides a utility called Distributed Cache to improve the performance of jobs by caching the files used by applications. An application can specify which file it wants to cache by using JobConf configuration. Hadoop framework copies these files to the nodes one which a task has to be executed. This is done before the start of execution of a task. DistributedCache supports distribution of simple read only text files as well as complex files like jars, zips etc.

```java
// Hadoop 2/3 API: ship a small read-only lookup file to every task
job.addCacheFile(new URI("hdfs:///data/reference/country_codes.csv#country_codes.csv"));

// Load it once per task in setup() instead of once per record
@Override
protected void setup(Context context) throws IOException {
    try (BufferedReader reader = new BufferedReader(
            new FileReader(new File("country_codes.csv")))) {
        String line;
        while ((line = reader.readLine()) != null) {
            String[] parts = line.split(",", 2);
            codes.put(parts[0], parts[1]);
        }
    }
}
```

[Table of Contents](#HADOOP)

## How will you synchronize the changes made to a file in Distributed Cache in Hadoop?
It is a trick question. In Distributed Cache, it is not allowed to make any changes to a file. This is a mechanism to cache read-only data across multiple nodes.Therefore, it is not possible to update a cached file or run any synchronization in Distributed Cache.

[Table of Contents](#HADOOP)

##  Can you elaborate about Mapreduce job?
Based on the configuration, the MapReduce Job first splits the input data into independent chunks called Blocks. These blocks processed by Map() and Reduce() functions. First Map function process the data, then processed by reduce function. The Framework takes care of sorts the Map outputs, scheduling the tasks.

A minimal driver shows the full contract of a job:

```java
Configuration conf = new Configuration();
Job job = Job.getInstance(conf, "orders-etl");
job.setJarByClass(OrdersJob.class);
job.setMapperClass(OrdersMapper.class);
job.setCombinerClass(OrdersCombiner.class);
job.setPartitionerClass(RegionPartitioner.class);
job.setReducerClass(OrdersReducer.class);
job.setOutputKeyClass(Text.class);
job.setOutputValueClass(IntWritable.class);
FileInputFormat.addInputPath(job, new Path(args[0]));
FileOutputFormat.setOutputPath(job, new Path(args[1]));
job.setNumReduceTasks(8);
System.exit(job.waitForCompletion(true) ? 0 : 1);
```

[Table of Contents](#HADOOP)

##  Why compute nodes and the storage nodes are the same?
Compute nodes for processing the data, Storage nodes for storing the data. By default Hadoop framework tries to minimize the network wastage, to achieve that goal Framework follows the Data locality concept. The Compute code execute where the data is stored, so the data node and compute node are the same.

[Table of Contents](#HADOOP)

##  What is the configuration object importance in Mapreduce?
It’s used to set/get of parameter name & value pairs in XML file.It’s used to initialize values, read from external file and set as a value parameter.Parameter values in the program always overwrite with new values which are coming from external configure files.Parameter values received from Hadoop’s default values.

```java
Configuration conf = new Configuration();   // loads *-default.xml, then *-site.xml
conf.set("etl.run_date", "2026-10-04");     // programmatic values win over files
conf.addResource(new Path("/etc/hadoop/conf/core-site.xml"));

String runDate = conf.get("etl.run_date");  // available in Mapper/Reducer Context
```

[Table of Contents](#HADOOP)

##  Where Mapreduce not recommended?
MapReduce is not recommended for iterative processing. It means repeat the output in a loop manner.To process Series of Mapreduce jobs, MapReduce not suitable. each job persists data in local disk, then again load to another job. It’s costly operation and not recommended.

```text
Good fit    : one-pass batch scans, huge inputs, fault-tolerant batch ETL
Poor fit    : iterative ML, interactive queries, graph algorithms, streaming,
              low-latency lookups
Spark, Tez or Flink replace MapReduce when the same data is revisited many
times, because they keep intermediate state in memory instead of on disk.
```

[Table of Contents](#HADOOP)

##  What is Namenode and it’s responsibilities?
Namenode is a logical daemon name for a particular node. It’s heart of the entire Hadoop system. Which store the metadata in FsImage and get all block information in the form of Heartbeat.

[Table of Contents](#HADOOP)

##  What is Jobtracker’s responsibility?
Scheduling the job’s tasks on the slaves. Slaves execute the tasks as directed by the JobTracker. Monitoring the tasks, if failed, re­execute the failed tasks.

[Table of Contents](#HADOOP)

##  What are the Jobtracker and Tasktracker?
MapReduce Framework consists of a single Job Tracker per Cluster, one Task Tracker per node. Usually A cluster has multiple nodes, so each cluster has single Job Tracker and multiple TaskTrackers.JobTracker can schedule the job and monitor the Task Trackers. If Task Tracker failed to execute tasks, try to re-execute the failed tasks.
    TaskTracker follow the JobTracker’s instructions and execute the tasks. As a slave node, it report the job status to Master JobTracker in the form of Heartbeat.

[Table of Contents](#HADOOP)

##  What is Job scheduling importance in Hadoop Mapreduce?
Scheduling is a systematic procedure of allocating resources in the best possible way among multiple tasks. Hadoop task tracker performing many procedures, sometime a particular procedure should finish quickly and provide more prioriety, to do it few job schedulers come into the picture. Default Schedule is FIFO. Fair scheduling, FIFO and CapacityScheduler are most popular hadoop scheduling in hadoop.

```xml
<!-- capacity-scheduler.xml: department queues with guaranteed capacity -->
<configuration>
  <property>
    <name>yarn.scheduler.capacity.root.queues</name>
    <value>etl,bi,adhoc</value>
  </property>
  <property><name>yarn.scheduler.capacity.root.etl.capacity</name><value>60</value></property>
  <property><name>yarn.scheduler.capacity.root.bi.capacity</name><value>25</value></property>
  <property><name>yarn.scheduler.capacity.root.adhoc.capacity</name><value>15</value></property>
  <property>
    <name>yarn.scheduler.capacity.root.etl.maximum-capacity</name>
    <value>80</value>
  </property>
  <property>
    <name>yarn.scheduler.capacity.root.etl.maximum-am-resource-percent</name>
    <value>20</value>
  </property>
</configuration>
```

```bash
# Submit a job to the etl queue
yarn jar wordcount.jar com.acme.WordCount \
  -D mapreduce.job.queuename=etl \
  /data/books /data/wordcount-out
```

[Table of Contents](#HADOOP)

##  When used Reducer?
To combine multiple mapper’s output used reducer. Reducer has 3 primary phases sort, shuffle and reduce. It’s possible to process data without reducer, but used when the shuffle and sort is required.

[Table of Contents](#HADOOP)

##  Where the Shuffle and Sort process does?
After Mapper generate the output temporary store the intermediate data on the local File System. Usually this temporary file configured at core­site.xml in the Hadoop file. Hadoop Framework aggregate and sort this intermediate data, then update into Hadoop to be processed by the Reduce function. The Framework deletes this temporary data in the local system after Hadoop completes the job.

[Table of Contents](#HADOOP)

##  Java is mandatory to write Mapreduce Jobs?
No, By default Hadoop implemented in JavaTM, but MapReduce applications need not be written in Java. Hadoop support Python, Ruby, C++ and other Programming languages. Hadoop Streaming API allows to create and run Map/Reduce jobs with any executable or script as the mapper and/or the reducer.Hadoop Pipes allows programmers to implement MapReduce applications by using C++ programs.

[Table of Contents](#HADOOP)

## What methods can controle the Map And Reduce function’s output?
 setOutputKeyClass() and setOutputValueClass()
    If they are different, then the map output type can be set using the methods.
    setMapOutputKeyClass() and setMapOutputValueClass()

[Table of Contents](#HADOOP)

## What is the main difference between Mapper And Reducer?
Map method is called separately for each key/value have been processed. It process input key/value pairs and emits intermediate key/value pairs.
    Reduce method is called separately for each key/values list pair. It process intermediate key/value pairs and emits final key/value pairs.
    Both are initialize and called before any other method is called. Both don’t have any parameters and no output.

[Table of Contents](#HADOOP)

##  Why compute Nodes and the Storage Nodes are same?
Compute nodes are logical processing units, Storage nodes are physical storage units (Nodes). Both are running in the same node because of “data locality” issue. As a result Hadoop minimize the data network wastage and allows to process quickly.

[Table of Contents](#HADOOP)

## What is difference between mapside join and reduce side join?
Join multple tables in mapper side, called map side join. Please note mapside join should has strict format and sorted properly. If dataset is smaller tables, goes through reducer phrase. Data should partitioned properly.
    Join the multiple tables in reducer side called reduce side join. If you have large amount of data tables, planning to join both tables. One table is large amount of rows and columns, another one has few number of tables only, goes through Rreduce side join. It’s the best way to join the multiple tables

```java
// Map-side join: broadcast the small dimension table to every mapper
job.addCacheFile(new URI("hdfs:///data/dim/customers.csv#customers.csv"));
job.setMapperClass(CustomerJoinMapper.class);
job.setNumReduceTasks(0);   // no shuffle needed
```

```sql
-- Reduce-side join: both sides are shuffled and sorted by the join key
SELECT o.order_id, c.country
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

[Table of Contents](#HADOOP)

##  What happen if number of Reducer is 0?
Number of reducer = 0 also valid configuration in MapReduce. In this scenario, No reducer will execute, so mapper output consider as output, Hadoop store this information in separate folder.

[Table of Contents](#HADOOP)

##  When we are goes to Combiner?
Mappers and reducers are independent they dont talk each other. When the functions that are commutative(a.b = b.a) and associative {a.(b.c) = (a.b).c} we goes to combiner to optimize the mapreduce process. Many mapreduce jobs are limited by the bandwidth, so by default Hadoop framework minimizes the data bandwidth network wastage. To achieve it’s goal, Mapreduce allows user defined “Cominer function” to run on the map output. It’s an MapReduce optimization technique, but it’s optional.

[Table of Contents](#HADOOP)

##  What is the main difference between Mapreduce Combiner and Reducer?
Both Combiner and Reducer are optional, but most frequently used in MapReduce. There are three main differences such as:
    combiner will get only one input from one Mapper. While Reducer will get multiple mappers from different mappers.
    If aggregation required used reducer, but if the function follows commutative (a.b=b.a) and associative a.(b.c)= (a.b).c law, use combiner.
    Input and output keys and values types must same in combiner, but reducer can follows any type input, any output format.

[Table of Contents](#HADOOP)

##  What is partition?
After combiner and intermediate map­output the Partitioner controls the keys after sort and shuffle. Partitioner divides the intermediate data according to the number of reducers so that all the data in a single partition gets executed by a single reducer. It means each partition can executed by only a single reducer. If you call reducer, automatically partition called in reducer by automatically.

[Table of Contents](#HADOOP)

## When we goes to Partition?
By default Hive reads entire dataset even the application have a slice of data. It’s a bottleneck for mapreduce jobs. So Hive allows special option called partitions. When you are creating table, hive partitioning the table based on requirement.

[Table of Contents](#HADOOP)

##  What are the important steps when you are partitioning table?
Don’t over partition the data with too small partitions, it’s overhead to the namenode.
    if dynamic partition, atleast one static partition should exist and set to strict mode by using given commands.
+ SET hive.exec.dynamic.partition = true;
+ SET hive.exec.dynamic.partition.mode = nonstrict;

first load data into non­partitioned table, then load such data into partitioned table. It’s not possible to load data from local to partitioned table.
insert overwrite table table_name partition(year) select * from non­partition­table;

[Table of Contents](#HADOOP)

## Can you elaborate Mapreduce Job architecture?
First Hadoop programmer submit Mpareduce program to JobClient.
    Job Client request the JobTracker to get Job id, Job tracker provide JobID, its’s in the form of Job_HadoopStartedtime_00001. It’s unique ID.
    Once JobClient receive received Job ID copy the Job resources (job.xml, job.jar) to File System (HDFS) and submit job to JobTracker. JobTracker initiate Job and schedule the job.
    Based on configuration, job split the input splits and submit to HDFS. TaskTracker retrive the job resources from HDFS and launch Child JVM. In this Child JVM, run the map and reduce tasks and notify to the Job tracker the job status.

[Table of Contents](#HADOOP)

##  Why task Tracker launch child Jvm?
Most frequently, hadoop developer mistakenly submit wrong jobs or having bugs. If Task Tracker use existent JVM, it may interrupt the main JVM, so other tasks may influenced. Where as child JVM if it’s trying to damage existent resources, TaskTracker kill that child JVM and retry or relaunch new child JVM.

[Table of Contents](#HADOOP)

##  Why Jobclient and Job Tracker submits job resources to file system?
Data locality. Move competition is cheaper than moving Data. So logic/ competition in Jar file and splits. So Where the data available, in File System Datanodes. So every resources copy where the data available.

[Table of Contents](#HADOOP)

##  How many Mappers and Reducers can run?
By default Hadoop can run 2 mappers and 2 reducers in one datanode. also each node has 2 map slots and 2 reducer slots. It’s possible to change this default values in Mapreduce.xml in conf file.

```xml
<!-- mapred-site.xml: per-task memory and the number of tasks in the job -->
<configuration>
  <property><name>mapreduce.map.memory.mb</name><value>2048</value></property>
  <property><name>mapreduce.reduce.memory.mb</name><value>4096</value></property>
  <property><name>mapreduce.job.maps</name><value>200</value></property>
  <property><name>mapreduce.job.reduces</name><value>50</value></property>
</configuration>
```

```text
Containers per node = min(yarn.nodemanager.resource.memory-mb / task memory,
                         yarn.nodemanager.resource.cpu-vcores)
On a 96 GB / 32 vcore node with 2 GB map tasks, roughly 32 maps can run
concurrently, bounded by vcores.
```

[Table of Contents](#HADOOP)

##  What is Inputsplit?
A chunk of data processed by a single mapper called InputSplit. In another words logical chunk of data which processed by a single mapper called Input split, by default inputSplit = block Size.

```text
block = physical partition of a file on HDFS (for example 128 MB)
split = logical range of input handed to a single map task

The number of map tasks equals the number of InputSplits. A split usually
aligns with a block so the task can be scheduled data-local.
```

[Table of Contents](#HADOOP)

## How to configure the split value?
By default block size = 128 MB on Hadoop 2/3 (64 MB on Hadoop 1.x), but to process the data, job tracker split the data. Hadoop architect use these formulas to know split size.
+ split size = min (max_splitsize, max (block_size, min_split_size));
+ split size = max(min_split_size, min (block_size, max_split, size));

    by default split size = block size. Always No of splits = No of mappers.
    Apply above formula:
+ split size = Min (max_splitsize, max (128, 512kB) // max _splitsize = depends on env, may 1gb or 10gb split size = min (10gb (let assume), 128) split size = 128 MB.
+ split size = max(min_split_size, min (block_size, max_split, size)); split size = max (512kb, min (128, 10GB)); split size = max (512kb, 128);split size = 128 MB;

[Table of Contents](#HADOOP)

##  How much ram required to process 64mb data?
Leg assume. 64 block size, system take 2 mappers, 2 reducers, so 64*4 = 256 MB memory and OS take atleast 30% extra space so atleast 256 + 80 = 326MB Ram required to process a chunk of data.So in this way required more memory to process un­structured process.

[Table of Contents](#HADOOP)

##  What is difference between block And split?
+ Block: How much chunk data to stored in the memory called block.
+ Split: how much data to process the data called split.

[Table of Contents](#HADOOP)

## Why Hadoop Framework reads a file parallel why not sequential?
To retrieve data faster, Hadoop reads data parallel, the main reason it can access data faster. While, writes in sequence, but not parallel, the main reason it might result one node can be overwritten by other and where the second node. Parallel processing is independent, so there is no relation between two nodes, if writes data in parallel, it’s not possible where the next chunk of data has. For example 100 MB data write parallel, 64 MB one block another block 36, if data writes parallel first block doesn’t know where the remaining data. So Hadoop reads parallel and write sequentially.

[Table of Contents](#HADOOP)

## If I am change block size from 64 to 128?
Even you have changed block size not effect existent data. After changed the block size, every file chunked after 128 MB of block size. It means old data is in 64 MB chunks, but new data stored in 128 MB blocks.

[Table of Contents](#HADOOP)

## What is Issplitable()?
By default this value is true. It is used to split the data in the input format. if un­structured data, it’s not recommendable to split the data, so process entire file as a one split. to do it first change isSplitable() to false.

```java
public class WholeFileInputFormat extends FileInputFormat<NullWritable, BytesWritable> {
    @Override
    protected boolean isSplitable(JobContext context, Path filename) {
        return false;   // one mapper reads the whole file (e.g. gzip, images)
    }
}
```

[Table of Contents](#HADOOP)

##  How much Hadoop allows maximum block size and minimum block size?
+ Minimum: 1 MB (dfs.namenode.fs-limits.min-block-size, default 1048576 bytes in Hadoop 2/3); the NameNode rejects smaller blocks at create time.
+ Maximum: Depends on environment. There is no upper­bound.

[Table of Contents](#HADOOP)

##  What are the Job Resource files?
job.xml and job.jar are core resources to process the Job. Job Client copy the resources to the HDFS.

[Table of Contents](#HADOOP)

##  What’s the Mapreduce Job consists?
MapReduce job is a unit of work that client wants to be performed. It consists of input data, MapReduce program in Jar file and configuration setting in XML files. Hadoop runs this job by dividing it in different tasks with the help of JobTracker

[Table of Contents](#HADOOP)

##  What is the data locality?
Whereever the data is there process the data, computation/process the data where the data available, this process called data locality. “Moving Computation is Cheaper than Moving Data” to achieve this goal follow data locality. It’s possible when the data is splittable, by default it’s true.

```text
Task placement priority:
  1. node-local  - data on the same DataNode, no network transfer
  2. rack-local  - data on the same rack, one switch hop
  3. off-switch  - data on another rack, slowest and last resort
```

[Table of Contents](#HADOOP)

##  What is speculative execution?
Hadoop run the process in commodity hardware, so it’s possible to fail the systems also has low memory. So if system failed, process also failed, it’s not recommendable.Speculative execution is a process performance optimization technique.Computation/logic distribute to the multiple systems and execute which system execute quickly. By default this value is true. Now even the system crashed, not a problem, framework choose logic from other systems.
+ Eg: logic distributed on A, B, C, D systems, completed within a time.

System A, System B, System C, System D systems executed 10 min, 8 mins, 9 mins 12 mins simultaneously. So consider system B and kill remaining system processes, framework take care to kill the other system process.

```xml
<property><name>mapreduce.map.speculative</name><value>true</value></property>
<property><name>mapreduce.reduce.speculative</name><value>true</value></property>
<!-- Disable for jobs whose tasks have non-idempotent side effects -->
```

[Table of Contents](#HADOOP)

##  What is chain Mapper?
Chain mapper class is a special mapper class sets which run in a chain fashion within a single map task. It means, one mapper input acts as another mapper’s input, in this way n number of mapper connected in chain fashion.

[Table of Contents](#HADOOP)

##  How to do value level comparison?
Hadoop can process key level comparison only but not in the value level comparison.

[Table of Contents](#HADOOP)

##  What is setup and clean up methods?
If you don’t no what is starting and ending point/lines, it’s much difficult to solve those problems. Setup and clean up can resolve it. N number of blocks, by default 1 mapper called to each split. each split has one start and clean up methods. N number of methods, number of lines. Setup is initialize job resources.
    The purpose of clean up is close the job resources. Map is process the data. once last map is completed, cleanup is initialized. It Improves the data transfer performance. All these block size comparison can do in reducer as well. If you have any key and value, compare one key value to another key value use it. If you compare record level used these setup and cleanup. It open once and process many times and close once. So it save a lot of network wastage during process.

```java
@Override
protected void setup(Context context) {
    // runs once per task, before any map() call: open connections, load lookups
}

@Override
protected void map(LongWritable key, Text value, Context context) {
    // runs once per record
}

@Override
protected void cleanup(Context context) {
    // runs once per task, after the last map() call: flush buffers, close handles
}
```

[Table of Contents](#HADOOP)

##  How many slots allocate for each task?
By default each task has 2 slots for mapper and 2 slots for reducer. So each node has 4 slots to process the data.

[Table of Contents](#HADOOP)

##  Why Tasktracker launch child Jvm to do a task?
Sometime child threads currupt parent threads. It means because of programmer mistake entired MapReduce task distruped. So task tracker launch a child JVM to process individual mapper or tasker. If tasktracker use existent JVM, it might damage main JVM. If any bugs occur, tasktracker kill the child process and relaunch another child JVM to do the same task. Usually task tracker relaunch and retry the task 4 times.

[Table of Contents](#HADOOP)

##  What main configuration parameters are specified in Mapreduce?
 The MapReduce programmers need to specify following configuration parameters to perform the map and reduce jobs:
+ The input location of the job in HDFs.
+ The output location of the job in HDFS.
+ The input’s and output’s format.
+ The classes containing map and reduce functions, respectively.
+ The .jar file for mapper, reducer and driver classes

[Table of Contents](#HADOOP)

##  What is identity Mapper?
Identity Mapper is the default Mapper class provided by Hadoop. when no other Mapper class is defined, Identify will be executed. It only writes the input data into output and do not perform and computations and calculations on the input data. The class name is org.apache.hadoop.mapred.lib.IdentityMapper.

[Table of Contents](#HADOOP)

##  What is RecordReader in a MapReduce?
RecordReader is used to read key/value pairs form the InputSplit by converting the byte-oriented view  and presenting record-oriented view to Mapper.

[Table of Contents](#HADOOP)

## What is OutputCommitter?
OutPutCommitter describes the commit of MapReduce task. FileOutputCommitter is the default available class available for OutputCommitter in MapReduce. It performs the following operations:
    Create temporary output directory for the job during initialization.
    Then, it cleans the job as in removes temporary output directory post job completion.
    Sets up the task temporary output. Identifies whether a task needs commit. The commit is applied if required.
    JobSetup, JobCleanup and TaskCleanup are important tasks during output commit.

[Table of Contents](#HADOOP)

##  What are the parameters of Mappers and Reducers?
The four parameters for mappers are:
+ LongWritable (input)
+ text (input)
+ text (intermediate output)
+ IntWritable (intermediate output)

The four parameters for reducers are:
+ Text (intermediate output)
+ IntWritable (intermediate output)
+ Text (final output)
+ IntWritable (final output)

```java
// Word count generics: mapper<LongWritable, Text, Text, IntWritable>
public class TokenizerMapper extends Mapper<LongWritable, Text, Text, IntWritable> { }

// reducer<Text, IntWritable, Text, IntWritable>: the input pair mirrors
// the mapper output pair, and the output pair is the final result type
public class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> { }
```

[Table of Contents](#HADOOP)

## Explain Jobconf in Mapreduce?
It is a primary interface to define a map-reduce job in the Hadoop for job execution. JobConf specifies mapper, Combiner, partitioner, Reducer,InputFormat , OutputFormat implementations and other advanced job faets liek Comparators.

[Table of Contents](#HADOOP)

## Explain Job scheduling through Jobtracker?
JobTracker communicates with NameNode to identify data location and submits the work to TaskTracker node. The TaskTracker plays a major role as it notifies the JobTracker for any job failure. It actually is referred to the heartbeat reporter reassuring the JobTracker that it is still alive. Later, the JobTracker is responsible for the actions as in it may either resubmit the job or mark a specific record as unreliable or blacklist it.

[Table of Contents](#HADOOP)

## What is SequenceFileInputFormat?
A compressed binary output file format to read in sequence files and extends the FileInputFormat.It passes data between output-input (between output of one MapReduce job to input of another MapReduce job)phases of MapReduce jobs.

```java
// SequenceFile stores binary key/value pairs and is splittable
job.setInputFormatClass(SequenceFileInputFormat.class);
job.setOutputFormatClass(SequenceFileOutputFormat.class);
// Typical use: the output of one MapReduce stage feeds the next without parsing text
```

[Table of Contents](#HADOOP)

##  Explain how input and output data format of the Hadoop Framework?
The MapReduce framework operates exclusively on pairs, that is, the framework views the input to the job as a set of pairs and produces a set of pairs as the output of the job, conceivably of different types.
    See the flow mentioned below:
+ (input) -> map -> -> combine/sorting -> -> reduce -> (output)

[Table of Contents](#HADOOP)

##  What are the restriction to the Key and Value Class?
The key and value classes have to be serialized by the framework. To make them serializable Hadoop provides a Writable interface. As you know from the java itself that the key of the Map should be comparable, hence the key has to implement one more interface Writable Comparable.

```java
public interface Writable {
    void write(DataOutput out) throws IOException;
    void readFields(DataInput in) throws IOException;
}

// Keys must additionally be comparable so the framework can sort them
public interface WritableComparable<T> extends Writable, Comparable<T> { }
```

[Table of Contents](#HADOOP)

##  Explain the wordcount implementation via Hadoop Framework?
We will count the words in all the input file flow as below
    input Assume there are two files each having a sentence Hello World Hello World (In file 1) Hello World Hello World (In file 2)
Mapper : There would be each mapper for the a file For the given sample input the first map output:
        < Hello, 1>
        < World, 1>
        < Hello, 1>
        < World, 1>
The second map output:
        < Hello, 1>
        < World, 1>
        < Hello, 1>
        < World, 1>
Combiner/Sorting (This is done for each individual map) So output looks like this The output of the first map:
        < Hello, 2>
        < World, 2>
The output of the second map:
        < Hello, 2>
        < World, 2>
Reducer : It sums up the above output and generates the output as below
        < Hello, 4>
        < World, 4>

Output
    Final output would look like
        Hello 4 times
        World 4 times

```java
// WordCount.java - mapper, reducer and driver
import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {

    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, IntWritable> {

        private final IntWritable one = new IntWritable(1);
        private final Text word = new Text();

        @Override
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    public static class IntSumReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private final IntWritable result = new IntWritable();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable value : values) {
                sum += value.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

```bash
# Compile locally, package the jar, submit to YARN
hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
yarn jar wc.jar WordCount -D mapreduce.job.reduces=4 /data/books /data/wordcount-out
```

[Table of Contents](#HADOOP)

##  How Mapper is instantiated in a running Job?
The Mapper itself is instantiated in the running job, and will be passed a MapContext object which it can use to configure itself.

[Table of Contents](#HADOOP)

##  Which are the methods in the Mapper Interface?
The Mapper contains the run() method, which call its own setup() method only once, it also call a map() method for each input and finally calls it cleanup() method. All above methods you can override in your code.

[Table of Contents](#HADOOP)

##  What happens if You don't Override the Mapper methods and keep them as it is?
If you do not override any methods (leaving even map as-is), it will act as the identity function, emitting each input record as a separate output.

[Table of Contents](#HADOOP)

##  What is the use of context Object?
The Context object allows the mapper to interact with the rest of the Hadoop system. It Includes configuration data for the job, as well as interfaces which allow it to emit output.

[Table of Contents](#HADOOP)

##  How can you Add the arbitrary Key value pairs in your Mapper?
You can set arbitrary (key, value) pairs of configuration data in your Job, e.g. with
    Job.getConfiguration().set("myKey", "myVal"), and then retrieve this data in your mapper with
    Context.getConfiguration().get("myKey"). This kind of functionality is typically done in the Mapper's setup() method.

[Table of Contents](#HADOOP)

##  How does Mapper's run method works?
The Mapper.run() method then calls map(KeyInType, ValInType, Context) for each key/value pair in the InputSplit for that task

[Table of Contents](#HADOOP)

##  Which Object can be used to get the progress of a particular Job?
Context

[Table of Contents](#HADOOP)

##  What is next step after Mapper Or Maptask?
The output of the Mapper are sorted and Partitions will be created for the output. Number of partition depends on the number of reducer.

[Table of Contents](#HADOOP)

## How can we control particular Key should go in a specific Reducer?
Users can control which keys (and hence records) go to which Reducer by implementing a custom Partitioned.

[Table of Contents](#HADOOP)

##  What is the use of Combiner?
It is an optional component or class, and can be specify via Job.setCombinerClass(ClassName), to perform local aggregation of the intermediate outputs, which helps to cut down the amount of data transferred from the Mapper to the Reducer.

[Table of Contents](#HADOOP)

##  How many Maps are there in a particular Job?
The number of maps is usually driven by the total size of the inputs, that is, the total number of blocks of the input files.
    Generally it is around 10-100 maps per-node. Task setup takes awhile, so it is best if the maps take at least a minute to execute.
    Suppose, if you expect 10TB of input data and have a block size of 128MB, you'll end up with 82,000 maps, to control the number of block you can use the mapreduce.job.maps parameter (which only provides a hint to the framework). Ultimately, the number of tasks is controlled by the number of splits returned by the InputFormat.getSplits() method (which you can override).

[Table of Contents](#HADOOP)

##  What is the Reducer used for?
Reducer reduces a set of intermediate values which share a key to a (usually smaller) set of values. The number of reduces for the job is set by the user via Job.setNumReduceTasks(int).

[Table of Contents](#HADOOP)

##  Explain the core methods of the Reducer?
The API of Reducer is very similar to that of Mapper, there's a run() method that receives a Context containing the job's configuration as well as interfacing methods that return data from the reducer itself back to the framework. The run() method calls setup() once, reduce() once for each key associated with the reduce task, and cleanup() once at the end. Each of these methods can access the job's configuration data by using Context.getConfiguration().
    As in Mapper, any or all of these methods can be overridden with custom implementations. If none of these methods are overridden, the default reducer operation is the identity function; values are passed through without further processing.
    The heart of Reducer is its reduce() method. This is called once per key; the second argument is an Iterable which returns all the values associated with that key.

[Table of Contents](#HADOOP)

##  What are the primary phases of the Reducer?
Shuffle, Sort and Reduce.

[Table of Contents](#HADOOP)

## Explain the Shuffle?
Input to the Reducer is the sorted output of the mappers. In this phase the framework fetches the relevant partition of the output of all the mappers, via HTTP.

[Table of Contents](#HADOOP)

##  Explain the Reducer's sort phase?
The framework groups Reducer inputs by keys (since different mappers may have output the same key) in this stage. The shuffle and sort phases occur simultaneously; while map-outputs are being fetched they are merged (It is similar to merge-sort).

[Table of Contents](#HADOOP)

##  Explain the Reducer's reduce phase?
In this phase the reduce(MapOutKeyType, Iterable, Context) method is called for each pair in the grouped inputs. The output of the reduce task is typically written to the FileSystem via Context.write (ReduceOutKeyType, ReduceOutValType). Applications can use the Context to report progress, set application-level status messages and update Counters, or just indicate that they are alive. The output of the Reducer is not sorted.

[Table of Contents](#HADOOP)

##  How many Reducers should be configured?
The right number of reduces seems to be 0.95 or 1.75 multiplied by
        (number of nodes * mapreduce.tasktracker.reduce.tasks.maximum).
        With 0.95 all of the reduces can launch immediately and start transferring map outputs as the maps finish. With 1.75 the faster nodes will finish their first round of reduces and launch a second wave of reduces doing a much better job of load balancing. Increasing the number of reduces increases the framework overhead, but increases load balancing and lowers the cost of failures.

```java
// Rule of thumb: 0.95 x (reduce slots per node) x (nodes) for a single wave,
// 1.75 x the same when you want a second wave for better load balancing
int reduceSlotsPerNode = 8;
int nodes = 100;
job.setNumReduceTasks((int) (1.75 * reduceSlotsPerNode * nodes));
```

[Table of Contents](#HADOOP)

##  It can be possible that a Job has 0 Reducers?
It is legal to set the number of reduce-tasks to zero if no reduction is desired.

[Table of Contents](#HADOOP)

##  What happens if number of Reducers are 0?
In this case the outputs of the map-tasks go directly to the FileSystem, into the output path set by setOutputPath(Path). The framework does not sort the map-outputs before writing them out to the FileSystem.

[Table of Contents](#HADOOP)

##  How many instances of Jobtracker can run on a Hadoop Cluster?
Only one

[Table of Contents](#HADOOP)

##  What is the Jobtracker and what it performs in a Hadoop Cluster?
JobTracker is a daemon service which submits and tracks the MapReduce tasks to the Hadoop cluster. It runs its own JVM process. And usually it run on a separate machine, and each slave node is configured with job tracker node location. The JobTracker is single point of failure for the Hadoop MapReduce service. If it goes down, all running jobs are halted.
    JobTracker in Hadoop performs following actions
    Client applications submit jobs to the Job tracker.
    The JobTracker talks to the NameNode to determine the location of the data
    The JobTracker locates TaskTracker nodes with available slots at or near the data
    The JobTracker submits the work to the chosen TaskTracker nodes.
    A TaskTracker will notify the JobTracker when a task fails. The JobTracker decides what to do then: it may resubmit the job elsewhere, it may mark that specific record as something to avoid, and it may may even blacklist the TaskTracker as unreliable.
    When the work is completed, the JobTracker updates its status.
    The TaskTracker nodes are monitored. If they do not submit heartbeat signals often enough, they are deemed to have failed and the work is scheduled on a different TaskTracker.
    A TaskTracker will notify the JobTracker when a task fails. The JobTracker decides what to do then: it may resubmit the job elsewhere, it may mark that specific record as something to avoid, and it may may even blacklist the TaskTracker as unreliable.
    When the work is completed, the JobTracker updates its status.
    Client applications can poll the JobTracker for information.

In Hadoop 2/3 the JobTracker role is split: the ResourceManager schedules
containers on NodeManagers, and each application runs its own ApplicationMaster.

```xml
<!-- yarn-site.xml -->
<property><name>yarn.resourcemanager.hostname</name><value>rm1</value></property>
<property><name>yarn.nodemanager.aux-services</name><value>mapreduce_shuffle</value></property>
```

[Table of Contents](#HADOOP)

##  How a task is scheduled by a Jobtracker?
The TaskTrackers send out heartbeat messages to the JobTracker, usually every few minutes, to reassure the JobTracker that it is still alive. These messages also inform the JobTracker of the number of available slots, so the JobTracker can stay up to date with where in the cluster work can be delegated. When the JobTracker tries to find somewhere to schedule a task within the MapReduce operations, it first looks for an empty slot on the same server that hosts the DataNode containing the data, and if not, it looks for an empty slot on a machine in the same rack.

[Table of Contents](#HADOOP)

## How many instances of Tasktracker run on a Hadoop Cluster?
There is one Daemon Tasktracker process for each slave node in the Hadoop cluster.

[Table of Contents](#HADOOP)

##  How many maximum Jvm can run on a Slave Node?
One or Multiple instances of Task Instance can run on each slave node. Each task instance is run as a separate JVM process. The number of Task instances can be controlled by configuration. Typically a high end machine is configured to run more task instances.

[Table of Contents](#HADOOP)

##  What is Nas?
It is one kind of file system where data can reside on one centralized machine and all the cluster member will read write data from that shared database, which would not be as efficient as HDFS.

[Table of Contents](#HADOOP)

##  How Hdfs differs with Nfs?
Following are differences between HDFS and NAS
    In HDFS Data Blocks are distributed across local drives of all machines in a cluster. Whereas in NAS data is stored on dedicated hardware.
    HDFS is designed to work with MapReduce System, since computation is moved to data. NAS is not suitable for MapReduce since data is stored separately from the computations.
    HDFS runs on a cluster of machines and provides redundancy using replication protocol. Whereas NAS is provided by a single machine therefore does not provide data redundancy.

[Table of Contents](#HADOOP)

##  How does a NameNode handle the failure of the Data Nodes?
HDFS has master/slave architecture. An HDFS cluster consists of a single
    NameNode, a master server that manages the file system namespace and regulates access to files by clients.
    In addition, there are a number of DataNodes, usually one per node in the cluster, which manage storage attached to the nodes that they run on. The NameNode and DataNode are pieces of software designed to run on commodity machines.
    NameNode periodically receives a Heartbeat and a Block report from each of the DataNodes in the cluster. Receipt of a Heartbeat implies that the DataNode is functioning properly. A Blockreport contains a list of all blocks on a DataNode. When NameNode notices that it has not received a heartbeat message from a data node after a certain amount of time, the data node is marked as dead. Since blocks will be under replicated the system begins replicating the blocks that were stored on the dead DataNode. The NameNode Orchestrates the replication of data blocks from one DataNode to another. The replication data transfer happens directly between DataNode and the data never passes through the NameNode.

[Table of Contents](#HADOOP)

##  Can Reducer talk with each other?
No, Reducer runs in isolation.

[Table of Contents](#HADOOP)

##  Where the Mapper's intermediate data will be stored?
The mapper output (intermediate data) is stored on the Local file system (NOT HDFS) of each individual mapper nodes. This is typically a temporary directory location which can be setup in config by the Hadoop administrator. The intermediate data is cleaned up after the Hadoop Job completes.

[Table of Contents](#HADOOP)

##  What is the Hadoop Mapreduce api contract for a Key and Value Class?
The Key must implement the org.apache.hadoop.io.WritableComparable interface.
    The value must implement the org.apache.hadoop.io.Writable interface.

[Table of Contents](#HADOOP)

##  What is a IdentityMapper and IdentityReducer in Mapreduce?
+ org.apache.hadoop.mapred.lib.IdentityMapper: Implements the identity function, mapping inputs directly to outputs. If MapReduce programmer does not set the Mapper Class using JobConf.setMapperClass then IdentityMapper.class is used as a default value.
+ org.apache.hadoop.mapred.lib.IdentityReducer : Performs no reduction, writing all input values directly to the output. If MapReduce programmer does not set the Reducer Class using JobConf.setReducerClass then IdentityReducer.class is used as a default value.

[Table of Contents](#HADOOP)

##  What is the meaning of Speculative Execution in Hadoop?
Speculative execution is a way of coping with individual Machine performance. In large clusters where hundreds or thousands of machines are involved there may be machines which are not performing as fast as others.
    This may result in delays in a full job due to only one machine not performaing well. To avoid this, speculative execution in hadoop can run multiple copies of same map or reduce task on different slave nodes. The results from first node to finish are used.

[Table of Contents](#HADOOP)

## How Hdfs is different from traditional File Systems?
HDFS, the Hadoop Distributed File System, is responsible for storing huge data on the cluster. This is a distributed file system designed to run on commodity hardware.
    It has many similarities with existing distributed file systems. However, the differences from other distributed file systems are significant.
    HDFS is highly fault-tolerant and is designed to be deployed on low-cost hardware.
    HDFS provides high throughput access to application data and is suitable for applications that have large data sets.
    HDFS is designed to support very large files. Applications that are compatible with HDFS are those that deal with large data sets. These applications write their data only once but they read it one or more times and require these reads to be satisfied at streaming speeds. HDFS supports write-once-read-many semantics on files.

[Table of Contents](#HADOOP)

##  What is Hdfs block size and how is it different from Traditional File System block size?
In HDFS data is split into blocks and distributed across multiple nodes in the cluster. Each block is typically 64Mb or 128Mb in size. Each block is replicated multiple times. Default is to replicate each block three times. Replicas are stored on different nodes. HDFS utilizes the local file system to store each HDFS block as a separate file. HDFS Block size can not be compared with the traditional file system block size.

[Table of Contents](#HADOOP)

##  What is a NameNode and how many instances of NameNode run on a Hadoop Cluster?
The NameNode is the centerpiece of an HDFS file system. It keeps the directory tree of all files in the file system, and tracks where across the cluster the file data is kept. It does not store the data of these files itself.
    There is only One NameNode process run on any hadoop cluster. NameNode runs on its own JVM process. In a typical production cluster its run on a separate machine.
    The NameNode is a Single Point of Failure for the HDFS Cluster. When the NameNode goes down, the file system goes offline.
    Client applications talk to the NameNode whenever they wish to locate a file, or when they want to add /copy /move /delete a file. The NameNode responds the successful requests by returning a list of relevant DataNode servers where the data lives.

[Table of Contents](#HADOOP)

##  How the client communicates with Hdfs?
The Client communication to HDFS happens using Hadoop HDFS API. Client applications talk to the NameNode whenever they wish to locate a file, or when they want to add/copy/move/delete a file on HDFS. The NameNode responds the successful requests by returning a list of relevant DataNode servers where the data lives. Client applications can talk directly to a DataNode, once the NameNode has provided the location of the data.

[Table of Contents](#HADOOP)

##  How the Hdfs blocks are replicated?
HDFS is designed to reliably store very large files across machines in a large cluster. It stores each file as a sequence of blocks; all blocks in a file except the last block are the same size. The blocks of a file are replicated for fault tolerance. The block size and replication factor are configurable per file. An application can specify the number of replicas of a file. The replication factor can be specified at file creation time and can be changed later. Files in HDFS are write-once and have strictly one writer at any time.
    The NameNode makes all decisions regarding replication of blocks. HDFS uses rack-aware replica placement policy. In default configuration there are total 3 copies of a datablock on HDFS, 2 copies are stored on datanodes on same rack and 3rd copy on a different rack.

[Table of Contents](#HADOOP)

##  Can you give some examples of Big Data?
There are many real life examples of Big Data! Facebook is generating 500+ terabytes of data per day, NYSE (New York Stock Exchange) generates about 1 terabyte of new trade data per day, a jet airline collects 10 terabytes of censor data for every 30 minutes of flying time. All these are day to day examples of Big Data!

[Table of Contents](#HADOOP)

##  What is the basic difference between traditional Rdbms and Hadoop?
Traditional RDBMS is used for transactional systems to report and archive the data, whereas Hadoop is an approach to store huge amount of data in the distributed file system and process it. RDBMS will be useful when you want to seek one record from Big data, whereas, Hadoop will be useful when you want Big data in one shot and perform analysis on that later.

[Table of Contents](#HADOOP)

##  What is structured and unstructured Data?
Structured data is the data that is easily identifiable as it is organized in a structure. The most common form of structured data is a database where specific information is stored in tables, that is, rows and columns. Unstructured data refers to any data that cannot be identified easily. It could be in the form of images, videos, documents, email, logs and random text. It is not in the form of rows and columns.

[Table of Contents](#HADOOP)

##  Since the data is replicated thrice in Hdfs so does it mean that any calculation done on One Node will also be replicated on the other Two?
Since there are 3 nodes, when we send the MapReduce programs, calculations will be done only on the original data. The master node will know which node exactly has that particular data. In case, if one of the nodes is not responding, it is assumed to be failed. Only then, the required calculation will be done on the second replica.

[Table of Contents](#HADOOP)

##  What is throughput and how does Hdfs get a good throughput?
Throughput is the amount of work done in a unit time. It describes how fast the data is getting accessed from the system and it is usually used to measure performance of the system. In HDFS, when we want to perform a task or an action, then the work is divided and shared among different systems. So all the systems will be executing the tasks assigned to them independently and in parallel. So the work will be completed in a very short period of time. In this way, the HDFS gives good throughput. By reading data in parallel, we decrease the actual time to read data tremendously.

[Table of Contents](#HADOOP)

##  What is streaming access?
As HDFS works on the principle of ‘Write Once, Read Many‘, the feature of streaming access is extremely important in HDFS. HDFS focuses not so much on storing the data but how to retrieve it at the fastest possible speed, especially while analyzing logs. In HDFS, reading the complete data is more important than the time taken to fetch a single record from the data.

[Table of Contents](#HADOOP)

##  What is a Commodity Hardware so does Commodity Hardware include Ram?
Commodity hardware is a non-expensive system which is not of high quality or high-availability. Hadoop can be installed in any average commodity hardware. We don’t need super computers or high-end hardware to work on Hadoop. Yes, Commodity hardware includes RAM because there will be some services which will be running on RAM.

[Table of Contents](#HADOOP)

##  Is NameNode also a Commodity?
No. Namenode can never be a commodity hardware because the entire HDFS rely on it. It is the single point of failure in HDFS. Namenode has to be a high-availability machine.

[Table of Contents](#HADOOP)

##  What is a Metadata?
Metadata is the information about the data stored in data nodes such as location of the file, size of the file and so on.

[Table of Contents](#HADOOP)

##  What is a Daemon?
Daemon is a process or service that runs in background. In general, we use this word in UNIX environment. The equivalent of Daemon in Windows is “services” and in Dos is ” TSR”.

[Table of Contents](#HADOOP)

##  What is a Heartbeat in Hdfs?
A heartbeat is a signal indicating that it is alive. A datanode sends heartbeat to Namenode and task tracker will send its heart beat to job tracker. If the Namenode or job tracker does not receive heart beat then they will decide that there is some problem in datanode or task tracker is unable to perform the assigned task.

[Table of Contents](#HADOOP)

##  How indexing is done in Hdfs?
Hadoop has its own way of indexing. Depending upon the block size, once the data is stored, HDFS will keep on storing the last part of the data which will say where the next part of the data will be. In fact, this is the base of HDFS.

[Table of Contents](#HADOOP)

##  If a Data Node is full how it's identified?
When data is stored in datanode, then the metadata of that data will be stored in the Namenode. So Namenode will identify if the data node is full.

[Table of Contents](#HADOOP)

##  If DataNodes increase then do we need to upgrade NameNode?
While installing the Hadoop system, Namenode is determined based on the size of the clusters. Most of the time, we do not need to upgrade the Namenode because it does not store the actual data, but just the metadata, so such a requirement rarely arise.

[Table of Contents](#HADOOP)

##  Are Job Tracker and Task Trackers present in separate machines?
Yes, job tracker and task tracker are present in different machines. The reason is job tracker is a single point of failure for the Hadoop MapReduce service. If it goes down, all running jobs are halted.

[Table of Contents](#HADOOP)

## On what basis NameNode will decide which DataNode to write on?
As the Namenode has the metadata (information) related to all the data nodes, it knows which datanode is free.

[Table of Contents](#HADOOP)

##  Who is a user in Hdfs?
A user is like you or me, who has some query or who needs some kind of data.

[Table of Contents](#HADOOP)

##  Is client the end user in Hdfs?
No, Client is an application which runs on your machine, which is used to interact with the Namenode (job tracker) or datanode (task tracker).

[Table of Contents](#HADOOP)

##  What is the Communication Channel between client and NameNode/DataNode?
The mode of communication is SSH.

[Table of Contents](#HADOOP)

##  What is a Rack?
Rack is a storage area with all the datanodes put together. These datanodes can be physically located at different places. Rack is a physical collection of datanodes which are stored at a single location. There can be multiple racks in a single location.

[Table of Contents](#HADOOP)

##  On what basis Data will be stored on a Rack?
When the client is ready to load a file into the cluster, the content of the file will be divided into blocks. Now the client consults the Namenode and gets 3 datanodes for every block of the file which indicates where the block should be stored. While placing the datanodes, the key rule followed is “for every block of data, two copies will exist in one rack, third copy in a different rack“. This rule is known as “Replica Placement Policy“.

[Table of Contents](#HADOOP)

##  Do we need to place 2nd and 3rd Data in Rack 2 only?
Yes, this is to avoid datanode failure.

[Table of Contents](#HADOOP)

##  What if Rack 2 and DataNode fails?
If both rack2 and datanode present in rack 1 fails then there is no chance of getting data from it. In order to avoid such situations, we need to replicate that data more number of times instead of replicating only thrice. This can be done by changing the value in replication factor which is set to 3 by default.

[Table of Contents](#HADOOP)

##  What is the difference between Gen1 and Gen2 Hadoop with regards to the NameNode?
In Gen 1 Hadoop, Namenode is the single point of failure. In Gen 2 Hadoop, we have what is known as Active and Passive Namenodes kind of a structure. If the active Namenode fails, passive Namenode takes over the charge.

```xml
<!-- core-site.xml: NameNode HA in Hadoop 2/3 with automatic failover -->
<configuration>
  <property><name>fs.defaultFS</name><value>hdfs://acme-ns</value></property>
  <property><name>dfs.nameservices</name><value>acme-ns</value></property>
  <property><name>dfs.ha.namenodes.acme-ns</name><value>nn1,nn2</value></property>
  <property>
    <name>dfs.namenode.rpc-address.acme-ns.nn1</name>
    <value>nn1:8020</value>
  </property>
  <property>
    <name>dfs.namenode.rpc-address.acme-ns.nn2</name>
    <value>nn2:8020</value>
  </property>
  <property><name>ha.zookeeper.quorum</name><value>zk1:2181,zk2:2181,zk3:2181</value></property>
  <property><name>dfs.ha.automatic-failover.enabled</name><value>true</value></property>
</configuration>
```

[Table of Contents](#HADOOP)

##  Do we require two servers for the NameNode and the DataNodes?
Yes, we need two different servers for the Namenode and the datanodes. This is because Namenode requires highly configurable system as it stores information about the location details of all the files stored in different datanodes and on the other hand, datanodes require low configuration system.

[Table of Contents](#HADOOP)

##  Why are the number of splits equal to the number of Maps?
The number of maps is equal to the number of input splits because we want the key and value pairs of all the input splits.

[Table of Contents](#HADOOP)

##  Is a Job split into maps?
No, a job is not split into maps. Spilt is created for the file. The file is placed on datanodes in blocks. For each split, a map is needed.

[Table of Contents](#HADOOP)

##  Which are the two types of writes In Hdfs?
There are two types of writes in HDFS:
+ Posted and non-posted write. Posted Write is when we write it and forget about it, without worrying about the acknowledgement.
        It is similar to our traditional Indian post.
+  Non-posted Write, we wait for the acknowledgement. It is similar to the today’s courier services. Naturally, non-posted write is more expensive than the posted write. It is much more expensive, though both writes are asynchronous.

[Table of Contents](#HADOOP)

##  Why reading is done in parallel and writing is not in Hdfs?
Reading is done in parallel because by doing so we can access the data fast. But we do not perform the write operation in parallel. The reason is that if we perform the write operation in parallel, then it might result in data inconsistency. For example, you have a file and two nodes are trying to write data into the file in parallel, then the first node does not know what the second node has written and vice-versa. So, this makes it confusing which data to be stored and accessed.

[Table of Contents](#HADOOP)

##  Can Hadoop be compared to Nosql Database like Cassandra?
Though NOSQL is the closet technology that can be compared to Hadoop, it has its own pros and cons. There is no DFS in NOSQL. Hadoop is not a database. It’s a file system (HDFS) and distributed programming framework (MapReduce).

[Table of Contents](#HADOOP)

##  How JobTracker schedules a task?
The TaskTrackers send out heartbeat messages to the JobTracker, usually every few minutes, to reassure the JobTracker that it is still alive. These message also inform the JobTracker of the number of available slots, so the JobTracker can stay up to date with where in the cluster work can be delegated. When the JobTracker tries to find somewhere to schedule a task within the MapReduce operations, it first looks for an empty slot on the same server that hosts the DataNode containing the data, and if not, it looks for an empty slot on a machine in the same rack.

[Table of Contents](#HADOOP)

##  What is a Task Tracker in Hadoop and how many instances of Task Tracker run on a Hadoop Cluster?
A TaskTracker is a slave node daemon in the cluster that accepts tasks (Map, Reduce and Shuffle operations) from a JobTracker. There is only One Task Tracker process run on any hadoop slave node. Task Tracker runs on its own JVM process. Every TaskTracker is configured with a set of slots, these indicate the number of tasks that it can accept. The TaskTracker starts a separate JVM processes to do the actual work (called as Task Instance) this is to ensure that process failure does not take down the task tracker. The TaskTracker monitors these task instances, capturing the output and exit codes. When the Task instances finish, successfully or not, the task tracker notifies the JobTracker. The TaskTrackers also send out heartbeat messages to the JobTracker, usually every few minutes, to reassure the JobTracker that it is still alive. These message also inform the JobTracker of the number of available slots, so the JobTracker can stay up to date with where in the cluster work can be delegated.

[Table of Contents](#HADOOP)

##  What is a task instance in Hadoop and where does it run?
Task instances are the actual MapReduce jobs which are run on each slave node. The TaskTracker starts a separate JVM processes to do the actual work (called as Task Instance) this is to ensure that process failure does not take down the task tracker. Each Task Instance runs on its own JVM process. There can be multiple processes of task instance running on a slave node. This is based on the number of slots configured on task tracker. By default a new task instance JVM process is spawned for a task.

[Table of Contents](#HADOOP)

##  What is configuration of a typical Slave Node on Hadoop Cluster and how many Jvms run on a Slave Node?
Single instance of a Task Tracker is run on each Slave node. Task tracker is run as a separate JVM process.
    Single instance of a DataNode daemon is run on each Slave node. DataNode daemon is run as a separate JVM process.
    One or Multiple instances of Task Instance is run on each slave node. Each task instance is run as a separate JVM process. The number of Task instances can be controlled by configuration. Typically a high end machine is configured to run more task instances.

[Table of Contents](#HADOOP)

##  How NameNode handles DataNode failures?
NameNode periodically receives a Heartbeat and a Blockreport from each of the DataNodes in the cluster. Receipt of a Heartbeat implies that the DataNode is functioning properly. A Blockreport contains a list of all blocks on a DataNode. When NameNode notices that it has not recieved a hearbeat message from a data node after a certain amount of time, the data node is marked as dead. Since blocks will be under replicated the system begins replicating the blocks that were stored on the dead datanode. The NameNode Orchestrates the replication of data blocks from one datanode to another. The replication data transfer happens directly between datanodes and the data never passes through the namenode.

[Table of Contents](#HADOOP)

## Does Mapreduce programming model provide a way for Reducers to communicate with each other and in a Mapreduce Job can a Reducer communicate with another Reducer?
Nope, MapReduce programming model does not allow reducers to communicate with each other. Reducers run in isolation.

[Table of Contents](#HADOOP)

##  Can I set the number of Reducers to Zero?
Yes, Setting the number of reducers to zero is a valid configuration in Hadoop. When you set the reducers to zero no reducers will be executed, and the output of each mapper will be stored to a separate file on HDFS.This is different from the condition when reducers are set to a number greater than zero and the Mappers output (intermediate data) is written to the Local file system(NOT HDFS) of each mappter slave node.

[Table of Contents](#HADOOP)

##  Where is the Mapper Output intermediate Kay value data stored?
The mapper output (intermediate data) is stored on the Local file system (NOT HDFS) of each individual mapper nodes. This is typically a temporary directory location which can be setup in config by the hadoop administrator. The intermediate data is cleaned up after the Hadoop Job completes.

[Table of Contents](#HADOOP)

##  If Reducers do not start before all Mappers finish then why does the progress on Mapreduce Job shows something like Map 50 percents Reduce 10 percents and why Reducers progress percentage is displayed when Mapper is not Finished yet?
Reducers start copying intermediate key-value pairs from the mappers as soon as they are available. The progress calculation also takes in account the processing of data transfer which is done by reduce process, therefore the reduce progress starts showing up as soon as any intermediate key-value pair for a mapper is available to be transferred to reducer. Though the reducer progress is updated still the programmer defined reduce method is called only after all the mappers have finished.

[Table of Contents](#HADOOP)

## Explain in brief the three Modes in which Hadoop can be run?
 The three modes in which Hadoop can be run are:
+ Standalone (local) mode - No Hadoop daemons running, everything runs on a single Java Virtual machine only.
+ Pseudo-distributed mode - Daemons run on the local machine, thereby simulating a cluster on a smaller scale.
+ Fully distributed mode - Runs on a cluster of machines.

[Table of Contents](#HADOOP)

## Explain what are the features of Standalone local Mode?
In stand-alone or local mode there are no Hadoop daemons running,  and everything runs on a single Java process. Hence, we don't get the benefit of distributing the code across a cluster of machines. Since, it has no DFS, it utilizes the local file system. This mode is suitable only for running MapReduce programs by developers during various stages of development. Its the best environment for learning and good for debugging purposes.

[Table of Contents](#HADOOP)

##  What are the features of fully distributed mode?
In Fully Distributed mode, the clusters range from a few nodes to 'n' number of nodes. It is used in production environments, where we have thousands of machines in the Hadoop cluster. The daemons of Hadoop run on these clusters. We have to configure separate masters and separate slaves in this distribution, the implementation of which is quite complex. In this configuration, Namenode and Datanode runs on different hosts and there are nodes on which task tracker runs. The root of the distribution is referred as HADOOP_HOME.

[Table of Contents](#HADOOP)

##  Explain what are the main features Of pseudo mode?
In Pseudo-distributed mode, each Hadoop daemon runs in a separate Java process, as such it simulates a cluster though on a small scale. This mode is used both for development and QA environments. Here, we need to do the configuration changes.

[Table of Contents](#HADOOP)

##  What are the port numbers of NameNode and JobTracker and TaskTracker?
The port number for Namenode is ’70′, for job tracker is ’30′ and for task tracker is ’60′.

```text
The old shorthand "70", "30", "60" refers to the 50070 / 50030 / 50060 UIs.
Use the full numbers, and remember that Hadoop 2/3 moved the NameNode UI
to 9870 and the RPC port to 8020.
```

[Table of Contents](#HADOOP)

##  Tell us what is a spill factor with respect to the ram?
Spill factor is the size after which your files move to the temp file. Hadoop-temp directory is used for this. Default value for io.sort.spill.percent is 0.80. A value less than 0.5 is not recommended.

[Table of Contents](#HADOOP)

##  Is fs.mapr working for a single directory?
Yes, fs.mapr.working.dir it is just one directory.

[Table of Contents](#HADOOP)

##  Which are the three main Hdfs-site.xml properties?
The three main hdfs-site.xml properties are:
+ dfs.namenode.name.dir gives the local directories where the NameNode stores the fsimage and edits files (for example /data/1/dfs/nn,/data/2/dfs/nn).
+ dfs.datanode.data.dir gives the local directories where a DataNode stores block files.
+ dfs.namenode.checkpoint.dir gives the checkpoint directory used by the Secondary NameNode.

[Table of Contents](#HADOOP)

##  How can I restart Namenode?
Use the HDFS daemon control scripts, then confirm that the NameNode left safe mode:

```bash
hdfs --daemon stop namenode
hdfs --daemon start namenode
hdfs dfsadmin -safemode get
```

On older packaged installs the equivalent is `service hadoop-hdfs-namenode restart`.

[Table of Contents](#HADOOP)

##  How can we check whether Namenode is working or not?
To check whether Namenode is working or not, use the command /etc/init.d/hadoop- 0.20-namenode status or as simple as jps’.

[Table of Contents](#HADOOP)

##  At times you get a connection refused Java Exception when you run the file system check command Hadoop fsck?
The most possible reason is that the Namenode is not working on your VM.

[Table of Contents](#HADOOP)

##  What is the use of the command Mapred.job.tracker?
The command mapred.job.tracker is used by the Job Tracker to list out which host and port that the MapReduce job tracker runs at. If it is "local", then jobs are run in-process as a single map and reduce task.

```properties
# mapred-site.xml values in the old (Hadoop 1.x) configuration style
mapred.job.tracker=nn1:8021
# local - run the whole job in-process as one map and one reduce task
```

[Table of Contents](#HADOOP)

## What does etc/init.d do?
/etc /init.d specifies where daemons (services) are placed or to see the status of these daemons. It is very LINUX specific, and nothing to do with Hadoop.

[Table of Contents](#HADOOP)

##  How can we look for the Namenode in the browser?
If you have to look for Namenode in the browser, you don’t have to give localhost: 8021, the port number to look for Namenode in the browser is 50070.

[Table of Contents](#HADOOP)

## What do masters and slaves consist of?
Masters contain a list of hosts, one per line, that are to host secondary namenode servers. Slaves consist of a list of hosts, one per line, that host datanode and task tracker servers.

[Table of Contents](#HADOOP)

##  What is the function Of Hadoop-env.sh and where is it present?
This file contains some environment variable settings used by Hadoop; it provides the environment for Hadoop to run. The path of JAVA_HOME is set here for it to run properly. Hadoop-env.sh file is present in the conf/hadoop-env.sh location. You can also create your own custom configuration file conf/hadoop-user-env.sh, which will allow you to override the default Hadoop settings.

[Table of Contents](#HADOOP)

##  Can we have multiple entries in the master files?
Yes, we can have multiple entries in the Master files.

[Table of Contents](#HADOOP)

##  In Hadoop_pid_dir and what does pid stands for?
PID stands for ‘Process ID’.

[Table of Contents](#HADOOP)

## What does Hadoop-metrics and properties file do?
Hadoop-metrics Properties is used for ‘Reporting‘purposes. It controls the reporting for hadoop. The default status is ‘not to report‘.

[Table of Contents](#HADOOP)

##  What are the network requirements for hadoop?
The Hadoop core uses Shell (SSH) to launch the server processes on the slave nodes. It requires password-less SSH connection between the master and all the slaves and the Secondary machines.

[Table of Contents](#HADOOP)

##  Why do we need a passwordless ssh in fully distributed environment?
We need a password-less SSH in a Fully-Distributed environment because when the cluster is LIVE and running in Fully Distributed environment, the communication is too frequent. The job tracker should be able to send a task to task tracker quickly.

[Table of Contents](#HADOOP)

##  What will happen if a NameNode has no data?
If a Namenode has no data it cannot be considered as a Namenode. In practical terms, Namenode needs to have some data.

[Table of Contents](#HADOOP)

##  What happens to job tracker when NameNode is down?
Namenode is the main point which keeps all the metadata, keep tracks of failure of datanode with the help of heart beats. As such when a namenode is down, your cluster will be completely down, because Namenode is the single point of failure in a Hadoop Installation.

[Table of Contents](#HADOOP)

##  Explain what do you mean by formatting of the Dfs?
Like we do in Windows, DFS is formatted for proper structuring of data. It is not usually recommended to do as it format the Namenode too in the process, which is not desired.

[Table of Contents](#HADOOP)

##  We use Unix variants for hadoop and can we use Microsoft Windows for the same?
In practicality, Ubuntu and Red Hat Linux are the best Operating Systems for Hadoop. On the other hand, Windows can be used but it is not used frequently for installing Hadoop as there are many support problems related to it. The frequency of crashes and the subsequent restarts makes it unattractive. As such, Windows is not recommended as a preferred environment for Hadoop Installation, though users can give it a try for learning purposes in the initial stage.

[Table of Contents](#HADOOP)

##  Which one decides the input split hdfs client or NameNode?
The HDFS Client does not decide. It is already specified in one of the configurations through which input split is already configured.

[Table of Contents](#HADOOP)

##  Can you tell me if we can create a hadoop cluster from scratch?
Yes, we can definitely do that.  Once we become familiar with the Apache Hadoop environment, we can create a cluster from scratch.

[Table of Contents](#HADOOP)

## Explain the significance of ssh and what is the port on which port does ssh work and why do we need password in ssh local host?
SSH is a secure shell communication, is a secure protocol and the most common way of administering remote servers safely, relatively very simple and inexpensive to implement. A single SSH connection can host multiple channels and hence can transfer data in both directions. SSH works on Port No. 22, and it is the default port number. However, it can be configured to point to a new port number, but its not recommended. In local host, password is required in SSH for security and in a situation where password less communication is not set.

[Table of Contents](#HADOOP)

##  What is ssh and explain in detail about ssh communication between masters and the slaves?
Secure Socket Shell or SSH is a password-less secure communication that provides administrators with a secure way to access a remote computer and data packets are sent across the slave. This network protocol also has some format into which data is sent across. SSH communication is not only between masters and slaves but also between two hosts in a network.  SSH appeared in 1995 with the introduction of SSH - 1. Now SSH 2 is in use, with the vulnerabilities coming to the fore when Edward Snowden leaked information by decrypting some SSH traffic.

[Table of Contents](#HADOOP)

##  Can you tell is what will happen to a NameNode and when Job tracker is not up and running?
When the job tracker is down, it will not be in functional mode, all running jobs will be halted because it is a single point of failure. Your whole cluster will be down but still Namenode will be present. As such the cluster will still be accessible if Namenode is working, even if the job tracker is not up and running. But you cannot run your Hadoop job.

[Table of Contents](#HADOOP)

## What are the key trade-offs in Hadoop and when should you move off it?

+ **Shuffle cost.** MapReduce and Hive both write intermediate data to disk between stages. A job with five stages reads and writes the shuffle data five times, so fewer, wider stages beat many narrow ones.
+ **Data skew.** A single hot key (a null `customer_id`, one huge tenant) lands on one reducer and turns a 20-minute job into a 4-hour job. Fix it with `hive.optimize.skewjoin`, salting the key, or splitting the hot value into its own pipeline.
+ **Small files.** Every file costs NameNode memory and one task. Compacting to 128-512 MB files is the single highest-leverage storage fix.
+ **Block size versus split size.** Maps equal splits, not blocks; a non-splittable codec (gzip) forces one mapper per file.
+ **Slot-based scheduling is coarse.** YARN allocates whole containers; a task asking for 2 GB on a 1.5 GB container fails with a container error rather than degrading gracefully.
+ **When to move off Hadoop/Hive.** Move to object storage plus Spark/Trino or a lakehouse table format when: most data is cold, clusters are idle most of the day, you need sub-minute dashboards, or the operational cost of an HDFS/YARN cluster exceeds the compute you actually use. Keep HDFS for very large, repeatedly scanned datasets that justify dedicated hardware.
+ **When Hadoop still wins.** Petabyte-scale batch ETL with predictable schedules, strict data residency, and a large installed Hive SQL base is often cheaper on dedicated YARN than paying cloud egress and per-query costs.

[Table of Contents](#HADOOP)

## Real world use cases for Hadoop

### 1. Nightly batch ETL for a retail data platform

A retailer lands 8 TB of point-of-sale and clickstream data per day. The batch layer runs on YARN, reads JSON from HDFS, joins against dimension files held in the distributed cache, and writes partitioned, ORC or Parquet facts that downstream Hive and Spark jobs consume.

```bash
yarn jar etl.jar com.acme.DailyEtl \
  -D mapreduce.job.queuename=etl \
  -D mapreduce.job.reduces=200 \
  -D mapreduce.map.memory.mb=4096 \
  /data/raw/2026-10-04 /data/curated/orders/ds=2026-10-04
```

Why this design: the data is large, append-only and scanned by many downstream jobs, so columnar storage plus a scheduled batch window is both cheap and predictable.

### 2. Web and application log processing

A SaaS platform writes ~2 TB/day of access and application logs. Flume or Kafka lands them in HDFS, a MapReduce or Spark job parses and enriches them, and only a handful of columns are kept; the raw payload stays in a compressed cold prefix.

```text
hdfs:///logs/raw/ds=2026-10-04/      (gzipped text, compressed)
hdfs:///logs/parsed/ds=2026-10-04/   (ORC/Parquet, typed columns)
```

Why this design: log data is write-once and read-many; compression and column projection cut both storage and query cost.

### 3. Multi-tenant YARN cluster with department queues

A shared cluster serves ETL, BI and ad-hoc workloads. Capacity Scheduler queues guarantee 60/25/15 percent of the cluster, forbid ad-hoc jobs from consuming more than their share, and cap the ApplicationMaster resources so a runaway job cannot starve the cluster.

```xml
<property><name>yarn.scheduler.capacity.root.queues</name><value>etl,bi,adhoc</value></property>
<property><name>yarn.scheduler.capacity.root.adhoc.maximum-capacity</name><value>40</value></property>
```

Why this design: without queues, a single ad-hoc query can consume the whole cluster and delay the nightly SLA.

### 4. Offloading an enterprise data warehouse

A bank exports 300 TB of historical facts and slowly changing dimensions from a commercial warehouse to HDFS, keeps five years online in Hive external tables, and retires the most expensive warehouse storage tier.

```bash
# One-time bulk load, then incremental daily partitions
sqoop import --connect jdbc:oracle:thin:@dw:1521/DW \
  --table FACT_TRANSACTIONS --target-dir /data/dw/fact_transactions \
  --as-parquetfile --split-by txn_id --num-mappers 32
```

Why this design: HDFS gives cheap storage and Hive keeps the SQL interface analysts already know, so the migration does not require retraining.

### 5. Migrating an on-premises Hadoop cluster to object storage and Spark

An organisation moves its cold partitions to S3, keeps Iceberg as the table format, and runs Spark on Kubernetes. HDFS and YARN are retired only after every job has an owner, a runtime and a target format.

```bash
# Validate the copy before switching producers to the new path
hadoop distcp -m 40 hdfs:///data/orders s3a://acme-lake/orders
hdfs dfs -count -q -h /data/orders
aws s3 ls s3://acme-lake/orders/ --recursive --summarize --human-readable
```

Why this design: object storage removes the capacity-planning cycle and separates storage cost from compute, but only makes sense once jobs are decoupled from the old cluster.

[Table of Contents](#HADOOP)
