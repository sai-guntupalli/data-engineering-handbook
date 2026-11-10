# Python practice verification

These fixtures hold regression checks removed from the reading experience. The notebook remains the source of
the question and reference answer. `scripts/verify_practice_answers.py` reconstructs temporary executable copies
using stable cell IDs, substitutes the current hidden answers, and checks both reference and wrong answers.
The coding workbook executes its current hidden implementations against its original regression cases.

`order` records execution order; `cells` stores removed test helpers and cases. Workbook `solutions` maps each
original implementation cell to a fenced Python block in the current collapsed solution. When adding or removing
an exercise, update the fixture IDs along with the notebook, then run the verifier. Source notebooks stay output-free.
