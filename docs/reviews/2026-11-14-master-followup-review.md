# Follow-up review of `master` (2026-11-14)

This review covers `master` at `2264e82`, after PRs #93 and #94 merged the work from
`docs/reviews/2026-11-14-handbook-review.md`. It looks at the commits made after the first handover:

- `c6dce85`: the DataFrames track
- `2bc6bcf`: the tool courses and the ingestion labs
- `98ee92c`: the dbt microbatch and Airflow labs
- `1b96ff6`: the baseline migration
- `788051d`: CI warms the Delta dependencies before the notebook run

It also checks the live site.

## Verdict

The handbook is broader and more consistent than it was. Everything runs. But the second half of the work met
the standards check's wording, not its intent. The new tool courses are skeletons of 150–300 words each. The
42 notebooks migrated off the baseline got one note and one generic exercise prompt each. The deep Kafka, dbt and
Airflow notebooks were dropped from the learning path in favour of the thinner lessons.

**The headline number, "168 of 169 notebooks meet the standard", is accurate for the check but overstates the
teaching quality.**

Overall score: **7/10**, up from 6.5. Coverage and consistency rose a lot. Depth on the main learning path went
down for Kafka, dbt and Airflow.

## What was checked

| Check | Result |
|---|---|
| `audit_notebooks.py --quiet` | Pass: 169 notebooks |
| `pytest -q` | 63 passed |
| `notebook_standards.py` | 168 of 169 pass; only `llm.ipynb` is baselined |
| `run_notebooks.py` on the 26 new notebooks | All 26 ran cleanly (dbt, Airflow 3.4, dlt, moto, Pandera, Polars, Arrow) |
| Live site: home, `/tools/kafka/`, `/tools/dbt/` | Deployed: 169 notebooks, 7 stages, 129 notebooks on the path |

## What went well

- **Real tools, running.** The dbt lessons drive `dbtRunner` against DuckDB. The Airflow lessons run real Airflow 3
  DAGs with `dag.test`, assets and data intervals. The ingestion lessons use `httpx.MockTransport`, moto and dlt.
  None of these existed before, and all of them run in CI.
- **Tracks the handbook was missing now exist:** DataFrames (4), ingestion (4), dbt (5), Airflow (3), Kafka (5),
  stream processing, Git and shell, Pandera, and three capstones.
- **The baseline was fully cleared.** No learner `assert` remains outside `llm.ipynb`, and the long setup cells are gone.
- **The CI hardening is sound.** Resolving the Delta Ivy dependencies once, with retries, before notebooks run in
  parallel removes a real source of flaky failures.
- **The notes checked against real output are correct.** I re-ran the Kafka, dbt, Airflow and capstone examples, and
  every What to notice note matched its output.

## Findings

### F1. The new course lessons are skeletons (high)

Every one of the 26 new notebooks was built from the same template:

- one topic;
- 2–4 example cells;
- one What to notice note;
- one exercise, always titled "Exercise 1: Apply the pattern" and marked "Easy · about 5 min";
- one or two takeaway bullets, copied word for word from "Where it matters".

| Track | Words of prose per lesson | Example cells | Exercises |
|---|---|---|---|
| Kafka 1–5 | 173–185 | 2 | 1 |
| dbt 1–4 | 149–202 | 3 | 1 |
| Airflow 1–3 | 192–228 | 3 | 1 |
| Ingestion 1–4 | 173–241 | 3 | 1 |
| Capstones (3) | 190–269 | 2–4 | 1 |
| DataFrames 2–4 | 263–303 | 4 | 1 |

For comparison, the reference notebooks they sit beside are much longer:

- `kafka.ipynb`: 5,600 words
- `dbt.ipynb`: 5,000 words
- `airflow.ipynb`: 9,600 words

The live site shows the result plainly. The Kafka page lists five "1 min" lessons, and all five cards carry the same
description: "This lesson runs a pure-Python model of the relevant behavior…" The four dbt cards share one description too.

Specific examples:

- **Kafka 4, "Delivery guarantees and transactions".** It shows no transactions, no `acks`, no
  `enable.idempotence` and no isolation level. The whole example is a dictionary `setdefault` over three tuples.
- **The capstones are not capstones.** `streaming-orders-capstone` is a four-line loop over three tuples.
  `cdc-to-scd2-capstone` is a list comprehension. A capstone should join several stages, for example ingestion →
  dbt → quality checks → an Airflow schedule. These are drills.
- **The dbt 3 title doesn't match its content.** "Incremental models and microbatch" demonstrates only a merge.
  Microbatch is covered in dbt 5.
- **Solutions that are only prose.** 19 of the 26 solution cells are `print("some sentence")`. The answer is prose
  pretending to be code, and you cannot run it to compare against your own attempt.

### F2. The deep notebooks left the learning path (high)

`site/lib/learning-map.ts` replaced `kafka`, `dbt` and `airflow` in their path steps with the new numbered lessons.
The reference notebooks still exist and link forward to lesson 1, but **no step on the path reaches them**.

A learner following the path now gets about 900 words of Kafka instead of about 5,600. The step labels still say
"Kafka", "dbt" and "Orchestration", so nothing tells the learner that the depth is elsewhere.

### F3. The baseline migration is mechanical and generic (high)

`1b96ff6` cleared 42 notebooks. Each one received the same changes:

| Change | Count | Problem |
|---|---|---|
| Exactly **one** What to notice note, whatever the notebook's size | 41 of 42 | Snowflake has 15 examples and 16,900 words but one note. data-structures has 57 examples and one note |
| The same Check yourself text: *"Choose a worked example. Predict which result would change if you removed its filter or constraint, then run it with that change."* | 36 | It means nothing for Kubernetes, Docker, Tableau or Avro, and none of these sections has an exercise |
| A generic `**Where it matters** / **Watch out for**` pair placed inside the **Setup** cell rather than under a topic | 40 | The standard asks for these under each topic. Here they appear once, before any content. In Snowflake the "Watch out for" is a disclaimer about the stand-in, not a pitfall |
| Key takeaways are the same one or two sentences as that pair | most | They don't summarise the 30+ sections above them |
| Asserts turned into `print(f"{expr = }")` | all | Fine as a mechanical step, but no note explains what any of the values mean |
| Setup pins dropped (e.g. `fakeredis[lua]>=2.20` became `fakeredis[lua]`) | several | Colab installs could drift |

The FAQ-style headings were renamed ("How do you use Lua scripting in Redis?" became "Use Lua scripting in Redis"),
but the notebooks were not reordered into lessons.

### F4. The standards check is too easy to satisfy (medium; this is the cause of F1 and F3)

`scripts/notebook_standards.py`, which I wrote, checks only that each element exists:

- at least one What to notice note;
- a `## Check yourself` heading;
- a `## Key takeaways` heading.

So one note, a one-sentence Check yourself and a one-bullet takeaway list pass on a 17,000-word notebook. The
previous handover also said that substring and ratio checks were not implemented. This is my gap, and the second
round of work hit it exactly.

### F5. Smaller issues (low)

- **Placement on the learning path.** Ingestion and DataFrames sit in **Store**, ahead of Databases. Ingestion is
  registered in the `foundations` category, but on the path it follows DataFrames. A more natural order is
  Foundations → DataFrames → Store → Ingestion, or an "Ingest" stage of its own.
- **Identical intro sentences** across the Kafka and dbt lessons become identical search snippets and card descriptions.

## Recommendations

**Status:** R1 and R2 are done on branch `review/master-followup-2026-11-14`.

- **R1:** `kafka`, `dbt` and `airflow` are first in their path steps again, and `orchestration-patterns` now comes
  before Airflow. Airflow 3's Next link now points to Change data capture.
- **R2:** the check has seven new rules. The honest baseline is now 73 notebooks (96 of 169 pass, down from the
  reported 168).
- **Correction to this review:** an earlier draft listed "no stored outputs" as an issue. It was wrong. The site
  renders outputs from `make outputs` at build time.

| # | Priority | Action |
|---|---|---|
| R1 | P0 | Put `kafka`, `dbt` and `airflow` back as the **first** slug in their path steps, so the numbered lessons follow as labs. Alternatively, merge each reference notebook's sections into the numbered lessons and retire it with a `retired.ts` entry |
| R2 | P0 | Tighten `notebook_standards.py` (details below), then baseline the notebooks that fail honestly rather than at zero |
| R3 | P1 | Grow each numbered lesson to 3–5 topics and 800–1,500 words. Give each 2–4 exercises whose solutions are runnable code, and 3–5 takeaways that summarise the lesson. Give each card its own one-line description |
| R4 | P1 | **Kafka:** test librdkafka's built-in mock cluster (`confluent-kafka` with `test.mock.num.brokers`). If it runs in Colab and CI, the Kafka lessons can use a real producer, a real consumer group, idempotence and transactions instead of dictionary models. Keep the "model" label only where that fails |
| R5 | P1 | Rewrite the 36 generic Check yourself sections with 2–3 real exercises each. Move Where it matters and Watch out for out of the Setup cells and under the topics. Add notes in proportion to the number of examples, starting with the notebooks on the learning path (parquet, delta, iceberg, flink, data-quality, cost-optimization, system-design) |
| R6 | P1 | Replace the three capstones with one or two real end-to-end projects: an API source → dlt → DuckDB → dbt with tests → a Pandera gate → an Airflow DAG with a backfill. Rename the current three as drills |
| R7 | P2 | Fix the dbt 3 title. Re-pin setup versions where the migration dropped them. Reconsider where Ingestion and DataFrames sit on the path |

Suggested rules for R2:

- `notes-ratio`: at least one What to notice note per two example cells (solution and setup cells excluded), with a
  minimum of 3 for notebooks that have 6 or more examples.
- `exercises`: lessons need 2 or more exercises under Check yourself, each with a solution-tagged code cell.
- `prose-solution`: warn when a solution cell is nothing but `print("<string literal>")`.
- `takeaways`: 3 or more bullets, and none may repeat a Where it matters or Watch out for sentence word for word.
- `boilerplate`: warn when a markdown cell over 60 characters appears word for word in more than 3 notebooks. This
  needs to exempt the standard headers and the "Write each query…" instructions shared across a course.
- `topic-callouts`: a Where it matters / Watch out for pair must sit under a `##` topic heading, not under
  `## Setup and sample data`.

## Evidence

Commands run on a clean checkout of `origin/master` (`2264e82`):

```bash
uv run --no-project python scripts/audit_notebooks.py --quiet       # 169 notebooks, pass
uv run pytest -q                                                    # 63 passed
uv run --no-project python scripts/notebook_standards.py            # 168 of 169
git diff --name-only --diff-filter=A 13f097e origin/master -- '*.ipynb' \
  | JAVA_HOME=$(brew --prefix openjdk@17) xargs uv run --extra notebooks python scripts/run_notebooks.py --jobs 4
                                                                    # all 26 ran cleanly
```

The per-notebook depth table (prose words, example cells, notes, exercises, prose-only solutions, takeaway bullets,
repeated markdown cells) came from a short script over the notebook JSON. The two most repeated markdown cells are the
generic Check yourself (36 notebooks) and the shared Kafka setup line (5).
