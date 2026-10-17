# Progress

**Current Status**: The AWS topic notebook has been rewritten to focus on data
engineering: generic AWS trivia removed, DE-relevant content reorganized into 34
sections, new "Things to remember" cheatsheets and a DMS/CDC section added.

## Completed

- 2026-10-17: Rewrote `notebooks/topics/aws.ipynb` (438 -> 242 cells): dropped
  non-DE services (EC2/VPC/Route 53/AMI/Elastic Transcoder/ElastiCache engines/
  RDS admin trivia), kept and reorganized S3, Glue, EMR, Athena, Redshift,
  Kinesis/MSK/SQS/EventBridge, Lake Formation, IAM, cost, CloudWatch, use cases,
  and the 8 runnable exercises; added "Things to remember" sections (key numbers,
  semantics, common mistakes) and a new "Change data capture with AWS DMS"
  section. Validated with `scripts/audit_notebooks.py`; all 9 runnable exercise
  cells execute with passing asserts.

## In Progress

- Nothing.

## Next Steps

1. Merge the `feat/aws-notebook-de-focus` PR.
2. Rebuild the gallery site (`make site`) so the updated notebook renders.
3. Apply the same focus-pass review to other broad notebooks if wanted
   (`gcp.ipynb`, `azure.ipynb`).

## Blockers

- None.
