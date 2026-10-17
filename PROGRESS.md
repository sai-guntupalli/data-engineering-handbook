# Progress

**Current Status**: Reviewed all 59 notebooks one at a time. 17 topic notebooks
were rewritten/tightened to focus on data engineering content (irrelevant or
duplicated legacy Q&A removed, "Things to remember" sections added); each has
its own PR waiting for review. The remaining 37 notebooks were reviewed and
verified already focused.

## Completed

- 2026-10-17: Rewrote `notebooks/topics/aws.ipynb` (438 -> 242 cells): dropped
  non-DE services (EC2/VPC/Route 53/AMI/Elastic Transcoder/ElastiCache engines/
  RDS admin trivia), kept and reorganized S3, Glue, EMR, Athena, Redshift,
  Kinesis/MSK/SQS/EventBridge, Lake Formation, IAM, cost, CloudWatch, use cases,
  and the 8 runnable exercises; added "Things to remember" sections (key numbers,
  semantics, common mistakes) and a new "Change data capture with AWS DMS"
  section. Validated with `scripts/audit_notebooks.py`; all 9 runnable exercise
  cells execute with passing asserts.

- 2026-10-17: Full notebook sweep completed. Rewrites/cleanups, one PR each:
  - Rewrites: azure (313->180), gcp (501->347), dwha (839->361), sql (1629->735),
    data-structure (674->301)
  - Dedupes: bigquery (649->465), redshift (752->367), bigtable (479->237),
    greenplum (439->265), looker (583->309), superset (480->329), hive (509->285),
    hbase (458->285), hadoop (754->285), flink (412->294), impala (437->341),
    cassandra (388->288)
  - Light cleanups: tableau (281->264), flume (341->254), avro (251->245),
    hudi (310->299)
  - Reviewed, no changes needed: airflow, cdc, cassandra-adjacent, clickhouse,
    cost-optimization, data-governance, data-modeling, data-quality, databricks,
    dbt, delta, docker, dynamodb, elasticsearch, iceberg, kafka, kubernetes, llm,
    mongo, nifi, observability, parquet, python-basics, python-coding, python,
    redis, scala, snowflake, spark, spark-tuning, statistics, superset-adjacent,
    system-design, tableau-adjacent, trino
  - Every PR verified with audit_notebooks.py, nbformat validation, and execution
    of runnable cells; sql.ipynb additionally passed sync_merged_copies --check.

## In Progress

- Nothing.

## Next Steps

1. Review and merge the open PRs in dependency order: #1 (aws, carries
   PROGRESS.md), then this branch, then #2-#22 in any order.
2. After merges, run `make site` to rebuild the gallery.
3. Spot-check a rendered notebook on the GitHub Pages site.

## Blockers

- None.
