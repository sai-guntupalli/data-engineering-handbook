# SQL and PySpark challenge regression checks

The notebooks contain the problem, readable sample tables, an exercise cell and a hidden runnable solution.
These fixtures preserve the regression checks without displaying them in the learner's notebook.

Run `make verify-challenges` with Java 17+ available. The verifier executes temporary notebook copies and compares
every published expected-output table with the current solution's result, including column names, row order and
null values. It leaves the source notebooks output-free. `make validate` runs this target in CI.

Each solution cell ID maps to a SHA-256 of its stripped source and regression blocks placed after numbered Python
statements. Checks run at their original point, before reused variables such as `q` change. Test-only helpers and
standalone demonstrations are restored only in memory. The fixtures do not contain copies of the reference answers.

When changing a solution, review its regression cases, update statement positions and the source hash, and run the
verifier. A stale recipe fails explicitly. `examples` links the question's expected-output cell to the SQL result
indices or PySpark DataFrame expressions that produce those tables. Add a corresponding entry whenever adding
an output or a solution.
