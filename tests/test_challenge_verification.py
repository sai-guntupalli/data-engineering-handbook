"""Guard against silent gaps when moving checks outside the notebook reader."""

import hashlib
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "challenge_verifier", Path(__file__).resolve().parents[1] / "scripts/verify_challenge_answers.py"
)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def test_sample_parser_ignores_inputs_and_preserves_multiple_outputs():
    source = """**Sample input**
| id |
| --- |
| 99 |

**Expected output**
| id | label |
| --- | --- |
| 1 | a&#124;b |

**Totals**
| total |
| --- |
| 2 |
"""
    tables = verifier.expected_tables(source)
    assert tables == [
        {"columns": ["id", "label"], "rows": [["1", "a|b"]]},
        {"columns": ["total"], "rows": [["2"]]},
    ]


@pytest.mark.parametrize(
    "actual",
    [
        {"columns": ["wrong"], "rows": [[1], [2]]},
        {"columns": ["id"], "rows": [[2], [1]]},
        {"columns": ["id"], "rows": [[1]]},
        {"columns": ["id"], "rows": [[1], [None]]},
    ],
)
def test_sample_comparison_rejects_wrong_columns_values_order_and_missing_rows(actual):
    with pytest.raises(AssertionError):
        verifier.compare_table({"columns": ["id"], "rows": [["1"], ["2"]]}, actual)


def test_sample_comparison_keeps_null_zero_false_distinct():
    verifier.compare_table(
        {"columns": ["v"], "rows": [["null"], ["0.00"], ["false"]]},
        {"columns": ["v"], "rows": [[None], [0], [False]]},
    )
    with pytest.raises(AssertionError):
        verifier.compare_table({"columns": ["v"], "rows": [["false"]]}, {"columns": ["v"], "rows": [[0]]})


@pytest.mark.parametrize("expected,actual", [("010115", "10115"), ("+14155550100", "14155550100"), ("null", "null")])
def test_sample_comparison_preserves_string_content_and_real_nulls(expected, actual):
    with pytest.raises(AssertionError):
        verifier.compare_table({"columns": ["v"], "rows": [[expected]]}, {"columns": ["v"], "rows": [[actual]]})


def test_regressions_run_before_a_reused_query_variable_changes():
    source = "q = 1\nq = 2\n"
    recipe = {
        "fingerprint": hashlib.sha256(source.strip().encode()).hexdigest(),
        "blocks": [
            {"after_statement": 1, "source": "assert q == 1"},
            {"after_statement": 2, "source": "assert q == 2"},
        ],
    }
    exec(verifier.rebuild_solution(source, recipe), {})
    with pytest.raises(ValueError, match="implementation changed"):
        verifier.rebuild_solution("q = 3\nq = 2\n", recipe)


def test_all_published_answers_have_hidden_tags_and_matching_regression_recipes():
    import json

    for path in verifier.FIXTURES.glob("*.json"):
        fixture = json.loads(path.read_text())
        notebook_path, notebook = verifier.verified_notebook(fixture)
        assert notebook_path.exists()
        assert len(fixture["solutions"]) == len(fixture["examples"])
        assert notebook.cells[-1].source == "spark.stop()"
