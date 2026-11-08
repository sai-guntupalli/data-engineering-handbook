# Progress

**Current Status**: All notebooks are Colab-runnable and executed by CI on PySpark 4.0 (JDK 17). The 14-chapter SQL path is on master (PR #34).
The design mockups (PR #43) are live at `/mockups/`, and the site has been rebuilt to match them (PR #44, merged):
learning map, in-site notebook reader, ⌘K search, reading progress. It replaces the editorial design from PRs #35 and #39.

## Completed

- 2026-11-07: SQL path explained from first principles (`feat/sql-path-explanations`): all 14 chapters `sql-01` to
  `sql-14` reviewed. Terms are defined before use, rules that were only stated now have hand-worked examples and
  asserts (SQL path asserts rose from about 100 to about 490), every concept section has a "Where you'll use it" note,
  and practice questions that copied the worked examples were replaced. Factual fixes: `INSERT OVERWRITE` on a
  partitioned table replaces the whole table in Spark's default static mode (sql-12); Spark prunes partition columns
  even through a function (sql-11, sql-14); the SCD2 overlap check missed equal start dates (sql-11); the "strictly
  newer" dedup wording contradicted its query (sql-09). No `##` heading was renamed, so saved reading progress is kept.

- 2026-11-07: Content widens when panels collapse (`feat/wide-content-collapsed`): with the sidebar collapsed the page
  grows to `--content-wide` (1480px), and with either panel collapsed the reader's article fills its column instead
  of keeping its 740px reading width. Measured at 1600px: article 740 (both open), 984 (sidebar collapsed), 1056
  (contents collapsed), 1220 (both collapsed).

- 2026-11-07: Collapsible sidebars (`feat/collapsible-sidebars`, PR #45): the sidebar folds into a 68px icon rail with hover and
  focus labels (top-bar button or <kbd>[</kbd>), and the reader's table of contents folds into a button (<kbd>]</kbd>).
  Both states are saved in localStorage and applied before first paint; phones keep their existing layout. Fixed a
  bug on master: the theme boot script was exported from a `"use client"` module, so the layout inlined a client
  reference instead of the script, which threw a syntax error and never restored a saved theme. The script now lives
  in `site/lib/boot.ts` with a vitest that runs it in a sandbox. Verified in the browser at 1360px (collapse, expand,
  reload persistence, labels, clean console) and 375px.

- 2026-11-07: Collections grouping and counting explained (`fix/python-collections-explained`): the section in
  `python-02-collections` now has one subsection per method with a worked example and assertions: the manual `if`
  check, `dict.setdefault`, `defaultdict(list)` and `defaultdict(int)`, `Counter`, `most_common`, `update`, `+`/`-`,
  `subtract`, `elements` and `total`. Interview notes cover setdefault's per-call default and defaultdict's read-inserts.

- 2026-11-07: Site rebuilt from the mockups (`feat/app-pipeline-redesign`, PR #44). Design tokens, Instrument Sans and a
  light/dark toggle in `site/app/globals.css` and `components/theme.tsx`; app shell with a group sidebar
  (`components/AppShell.tsx`). Home: learning map drawn from `lib/learning-map.ts` (validated against the registry),
  resume cards and weekly activity, and a catalog table filtered by `?group=` (sidebar links set it). New reader at
  `/notebooks/<slug>/`: markdown via `marked`, code highlighted at build time with highlight.js, a cell map
  (explanation, code, self-check), a table of contents that marks a section read when you scroll from it into the next
  heading (jumps do not count), mark-as-done, previous/next. Each `.ipynb` is served at `/files/<slug>.ipynb` for
  downloading. ⌘K / Ctrl+K / `/` open a search palette over notebooks and section headings, loaded from
  `/search-index.json`; `/search?q=` lists everything. Progress lives in localStorage like stars. Tailwind removed (it
  was unused). 43 vitest tests for the pure data layer in `site/tests/`, run by `make test`. Verified with lint,
  typecheck, a Pages-style build (80 notebook pages) and browser checks at 1360px and 375px in light and dark.

- 2026-11-07: Design mockups (`feat/handbook-mockups`, PR #43): static HTML in `docs/mockups/` with no build step.
  Library with a learning map drawn as a DAG (green passed, amber in progress, hollow not started), resume cards and a
  catalog table; notebook reader with a cell map, stage diagram, rendered DataFrame output, takeaways and self-checks;
  a search palette with a live preview and arrow-key navigation; an index with live thumbnails. Shared tokens in
  `styles.css` (Instrument Sans, lagoon accent), light/dark toggle in `theme.js`, focus styles and reduced motion.
  Checked at 1360px and 375px in light and dark. The mockups assume per-reader progress tracking and show section
  counts and reading time, which the `feat/redesign-site` direction removed; that needs a product decision.
- 2026-11-07: Mockups ship to GitHub Pages at `/data-engineering-handbook/mockups/` (`feat/handbook-mockups`, PR #43).
  New Makefile targets `mockups` (serve locally) and `mockups-bundle` (copy into `site/out/mockups`); `make build` and
  the Pages workflow both bundle them. Pages are `noindex`. `tests/test_mockups.py` checks that local links are relative
  and resolve. Verified with a Pages-style build (`NEXT_PUBLIC_BASE_PATH=/data-engineering-handbook make build`) served
  under the prefix: the site and all mockup routes return 200 and render. Goes live once PR #43 merges, because only
  `master` may deploy to the `github-pages` environment.

- 2026-11-07: SQL topic engine labels and site configuration docs (`fix/sql-topic-engine-labels`): six engine-specific
  SQL sections are marked *(engine-specific)* with a legend in the intro, and the Dialect differences table is named as
  the syntax reference. README has a Site URLs section on `NEXT_PUBLIC_BASE_PATH` and `NEXT_PUBLIC_SITE_URL`, and the
  `site.ts` comment says when both must be set. Removed leftover merge-conflict markers from PROGRESS.md.

- 2026-11-07: Notebook depth and real-world coverage (`feat/real-world-sections`): the classes chapter starts from
  what a class is and how to create one; chapters 3, 6 and 8 define decorators, context managers and threads or
  coroutines; every Python and SQL concept section has a "Where you'll use it" section. Seven topic notebooks (docker,
  kubernetes, llm, looker, scala, superset, tableau) gained one per main part. Airflow, Kafka and dbt have one per
  question. Spark, Delta and Iceberg are in progress.

- 2026-11-07: Restyled the site (`feat/site-cool-palette`): a cool, light-first palette with one blue accent, Geist for
  headings instead of the serif, drawn-out kicker labels removed, primary buttons in the accent, and matching dark theme.
  Layout, content and behaviour are unchanged. The design detector reports no findings. `PRODUCT.md` records the product
  context for future design work.

- 2026-11-07: Real-world coverage (`feat/python-learning-path`): seven topic notebooks that had no use-case section
  (docker, kubernetes, llm, looker, scala, superset, tableau) gained a "Where you'll use it" section for each main
  part. Every SQL chapter 14 question now has one, and chapter 13 has one for its concept block. The other topic
  notebooks already had a notebook-level "Real world use cases" section; their question-by-question sections are not
  yet written.

- 2026-11-07: Notebook depth pass (`feat/python-learning-path`): the classes chapter now starts from what a class is,
  how to define one, `__init__`, methods, `__repr__`, `__eq__`, class versus instance attributes, properties,
  inheritance, dataclasses by hand and with `@dataclass`, and enums. Chapters 3, 6 and 8 gained short definitions of
  decorators, context managers and threads or coroutines. Every Python and SQL concept section now has a
  "Where you'll use it" section with real-world uses. The other topic notebooks have not been done yet.

- 2026-11-07: Python learning path (`feat/python-learning-path`): the single `topics/python` notebook is replaced by nine
  chapters, following the SQL path. Chapters 1-8 cover values and types, collections, control flow and functions,
  iterators and generators, classes and dataclasses, files and formats, errors, logging and testing, and concurrency.
  Chapter 9 covers data-engineering patterns with the standard library only: config, validation and quarantine,
  idempotent upserts, watermarks, retries with backoff, partitioned output, content hashes, deduplication and run
  summaries. Each chapter runs top to bottom on Python 3.13 and passes the audit. The old notebook's Parquet and pandas
  content is not carried over; see the Parquet and Data quality notebooks.

- 2026-11-07: Library listing fixes (`fix/library-listing`): the practice group is now "Interview practice" (its six
  notebooks are interview prep kept outside the topic folders); descriptions read whole paragraphs, so they no longer
  stop mid-sentence; leading index numbers are dropped from titles; topic groups renamed to Data Engineering, Lakehouse
  Formats, Cloud Platforms, Streaming and Distributed Systems, Warehousing and BI, AI Foundations and Other Tools; the SQL
  index says fourteen chapters. Site builds, lint passes.

- 2026-11-07: Fixed the failing notebook run in CI (`fix/pyspark-4-recursive-cte`). The CI extra pinned PySpark below 4,
  so CI ran Spark 3.5, which has no recursive CTEs and failed `sql-02`. The extra and the six PySpark setup cells now pin
  `pyspark>=4.0,<4.1`, the version Colab installs. Spark 4.0.x fails to plan a recursive CTE (an internal `UnionLoop`
  error, seen on 4.0.0 through 4.0.5), so `sql-02` shows that query as reference and walks the hierarchy with a self-join.
  This corrects the earlier "all pass on 4.0.2" note for that query. `sql-02`'s ROLLUP query now sorts through a subquery.
  `spark` uses `try_cast` for the malformed cast, because ANSI mode is on by default in 4.0. `spark-tuning` reads Spark 4
  event logs, which are a directory of files, and writes them uncompressed. All 72 notebooks pass with PySpark 4.0.5 on
  JDK 17, the CI setup. Recursive CTE execution is verified only on 4.1.0 (in a sandbox probe).

- 2026-11-07: Redesigned the website (`feat/redesign-site`): an editorial look (warm paper, serif display type, one
  burnt-sienna accent) with dark mode. The home page has a hero with a static notebook preview, a Read / Run / Check
  strip and a library with a sticky topic index. Notebook rows replace the cards. Removed all counts (notebooks, code
  cells, checks, reading time) from the UI and the data layer. Header search, starring, /search and the license page
  keep their behaviour. The topics dropdown is gone; the topic index replaces it. Verified with lint, typecheck, the
  static build, and visual checks at desktop and phone width in light and dark themes.
- 2026-11-07: SQL path extended to 14 chapters (`feat/sql-missing-topics`): new `sql-03` types, functions, dates and
  JSON; `sql-07` set operations; `sql-12` views and changing data (INSERT, INSERT OVERWRITE, UPDATE/DELETE/MERGE as
  reference for table formats); `sql-14` interview concepts. Added GROUPING() and CUBE, RIGHT JOIN, LEAD, moving averages,
  FIRST_VALUE, LAST_VALUE, NTILE, WINDOW, time-zone setting, and an interview-notes section per chapter. Fixed the
  drills' DuckDB demos and stale Part 7 references. All 15 notebooks pass on Spark 4.0.2. Delta Lake could not be
  verified here (Maven is unreachable from the sandbox), so UPDATE, DELETE and MERGE are shown as reference SQL.

- 2026-11-07: Merged the WHERE vs HAVING notebook into `sql-01-basics` (new section 7). Replaced it with
  `sql-02-aggregations-and-ctes`: more aggregates, `ROLLUP`, subqueries, CTEs and a recursive CTE, with five practice
  questions and answers. Both run on Spark 4.0.2.
- 2026-11-07: Untangled the non-notebook code (`chore/untangle-codebase`):
  - One registry: each group in `site/lib/notebook-groups.ts` declares its folder. The build fails on a missing or
    unregistered notebook (the "Other notebooks" fallback is gone).
  - One repository identity: `site/lib/site.ts` holds the branch, author and license URL; a test keeps the Python
    formatter's copies in step with it.
  - One notebook list and one search rule: `site/lib/search.ts` defines what matches; header suggestions and /search
    share it, so they agree on the fields searched.
  - Removed dead special cases: the "How to use" boilerplate removal, the `.py`-module allowance in the audit, the
    hard-coded setup-helper list (the setup cell is now exempt from the import check), and the description prefixes.
  - CI runs `make validate`, the same target as local development.
  - Comments that restated the code were removed; tests that checked implementation details were rewritten to check
    behaviour.
  - Rendered gallery text is unchanged versus master. Intended change: header suggestions also match description text.

- 2026-11-07: SQL path review (feedback round): dropped the filtering-and-grouping notebook. Added `sql-01-basics`, a
  book-style notebook covering tables, SELECT, WHERE, sorting, aggregates, GROUP BY, HAVING, joins, CASE and NULL,
  with ten practice questions and answers. Reworked `sql-05-joins` in the same style. Both install PySpark with
  `!pip install -q pyspark` and run on Spark 4.0.2 (Colab's version) and locally. The audit now accepts
  `!pip install` lines. The approved style is then applied to every SQL notebook: plain Spark SQL cells, no setup
  helpers, each chapter ends with practice questions and answers. Drills keep their 22 checked answers. All SQL
  notebooks pass on Spark 4.0.2 from a clean install.
- 2026-11-07: Added `notebooks/06_pyspark_coding_challenges.ipynb`: five interview-style PySpark problems
  (latest-record dedupe, grain-aware joins, SCD as-of join, sessionization, salted skew join) with fixtures, reference
  solutions and 19 asserts; runs locally in 13s. Recovered from the old WIP in `notebooks/04_pyspark_concepts.ipynb`.
- 2026-11-07: SQL learning path split (`feat/sql-notebook-split`):
  - `03_sql_interview_questions` is now the index/navigation page; its DuckDB content moved into ten notebooks in
    `topics/sql-01…sql-10`: filtering and grouping, WHERE vs HAVING, NULL handling, CASE, joins, window functions,
    deduplication, time-series, modeling and optimization, and interview drills.
  - Every teaching notebook explains its topic first, then runs examples with asserted expected results. The drills
    port all 22 coding problems and 14 concept questions to Spark SQL, after the teaching material.
  - Execution backend is PySpark SQL on temporary views. The setup cell installs PySpark when it is missing, and a
    bootstrap cell detects PySpark and Java (`SPARK_AVAILABLE`). Without Java, every example prints `SKIPPED`.
  - Verified: audit passes on 67 notebooks; the 10 new notebooks execute end to end with Spark 3.5 on JDK 21; all 10
    run to completion with Spark unavailable; `make lint` and the Next.js build pass with the new gallery group.
- 2026-11-07: Verified PR #28: GitHub Checks green (all 57 notebooks executed on Linux + Java 17, 2m32s);
  smoke-tested in a real Google Colab runtime with "Run all": `topics/dynamodb` (30/30 cells), `topics/spark`
  (51/51, setup cell installed PySpark), `topics/iceberg` (22/22) — no errors.
- 2026-11-07: Colab-runnable restructure (PR #28, merged):
  - Merged the open per-notebook cleanup PRs (#1–#22) and the notebook parts of #26 (DuckDB SQL) and #27
    (PySpark story); the interactive viewer (#24/#25) was intentionally dropped.
  - Moved the Next.js gallery into `site/`; upgraded Next.js to 16.4.5 (critical advisory on ≤16.4.0); fixed the
    Topics menu links ignoring the GitHub Pages base path.
  - Removed bloat: merged practice copies inside topics/python, sql, spark (~1,000 duplicated cells) and
    `sync_merged_copies.py`; the watermark tooling and per-notebook metadata (incl. email); the duplicate
    `topics/python-basics` and `topics/python-coding` notebooks (unique content folded into 01/02); committed
    outputs; "How to use" boilerplate; repeated prose (21,532 → 5,467 cells; many notebooks 40–80% fewer words).
  - Every `# ILLUSTRATIVE` cell became runnable code on an in-process stand-in or a markdown code fence.
  - Each notebook with third-party imports starts with a version-aware setup cell (`PACKAGES`), so Colab installs
    or upgrades exactly what it needs.
  - New tooling: `notebook_format.py`, Colab-rule `audit_notebooks.py`, parallel `run_notebooks.py`, pytest suite,
    ruff, Makefile `install/dev/test/lint/format/check/notebooks/build/validate`; CI runs every notebook with Java 17.
- 2026-10-17/18: Per-notebook dedupe sweep and DuckDB/PySpark rewrites (open PRs #1–#27, now folded in).

## In Progress

- None.

## Next Steps

1. Review and merge the SQL path explanations PR (`feat/sql-path-explanations`). Decide whether to fix
   the stale "fourteen concept questions" sentence in the intro cell of `sql-13-interview-drills` (those questions
   now live in `sql-14`); it was left alone because intro cells were out of scope.
2. Check the deployed site after PR #44: home learning map, a notebook page, ⌘K search, the download link and dark
   mode.
3. Notebooks are stored without outputs, so the reader shows code but no results. If results are wanted on the site,
   decide whether CI should execute notebooks into a build-only copy with outputs for the reader to render.
4. `PRODUCT.md` still describes a counts-free, stateless site; update it to describe reading progress and the reader.
5. Run one SQL notebook in a real Colab runtime with "Run all" (requires the user's Google sign-in). Colab's bundled
   Java version is not verified; if Colab has no Java, the examples print `SKIPPED` there.
6. Decide on the older DuckDB reference `topics/sql.ipynb` (61K words, 74 cells). It overlaps the new path, so it is
   a candidate to trim or to link from the index.
7. Reconcile the uncommitted WIP in the main checkout: `notebooks/03_sql_interview_questions.ipynb` (a SQLite-based
   split), `notebooks/04_pyspark_concepts.ipynb` (exercise edits), and untracked `scripts/split_sql_notebooks.py`,
   `scripts/add_core_sql_topics.py` and `topics/sql-*` drafts. None of them are on master.
8. Review PR #29 (PySpark coding challenges, `feat/pyspark-coding-problems`).
9. Optional deeper trims: `04_pyspark_concepts` (12.9K words), `snowflake` (13.1K), `bigquery` (12.3K),
   `02_python_coding_problems` (12K).

## Blockers

- None.
