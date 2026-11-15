"""Inventory every notebook under notebooks/topics: structure markers per notebook."""
import json, re, sys, csv
from pathlib import Path

root = Path(sys.argv[1])
rows = []
for p in sorted((root / "notebooks/topics").rglob("*.ipynb")):
    nb = json.loads(p.read_text())
    cells = nb["cells"]
    src = lambda c: "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    md = [src(c) for c in cells if c["cell_type"] == "markdown"]
    code = [c for c in cells if c["cell_type"] == "code"]
    allmd = "\n".join(md)
    first_code = src(code[0]) if code else ""
    if "PACKAGES" in first_code:
        setup = "long"
    elif first_code.lstrip().startswith("# Setup") and "!pip install" in first_code:
        setup = "two-line" if len([l for l in first_code.strip().splitlines() if l.strip()]) <= 2 else "setup+extra"
    elif "!pip install" in first_code:
        setup = "pip-other"
    else:
        setup = "none"
    sol = sum(1 for c in code if "solution" in c.get("metadata", {}).get("tags", []))
    learner = [c for c in code if "solution" not in c.get("metadata", {}).get("tags", [])]
    asserts = sum(len(re.findall(r"^\s*assert\b", src(c), re.M)) for c in learner)
    assert_cells = sum(1 for c in learner if re.search(r"^\s*assert\b", src(c), re.M))
    h2 = re.findall(r"^## (.+)$", allmd, re.M)
    h3 = re.findall(r"^### (.+)$", allmd, re.M)
    title = (re.findall(r"^# (.+)$", allmd, re.M) or [""])[0]
    rows.append({
        "folder": str(p.parent.relative_to(root / "notebooks/topics")),
        "slug": p.stem,
        "title": title,
        "cells": len(cells), "md": len(md), "code": len(code),
        "setup": setup,
        "h2": len(h2), "h3": len(h3),
        "wtn": len(re.findall(r"\*\*What to notice", allmd)),
        "where": len(re.findall(r"(?i)where (it|this) matters|\*\*Where", allmd)),
        "watch": len(re.findall(r"(?i)watch out", allmd)),
        "check": int(bool(re.search(r"(?im)^#+ .*check yourself", allmd))),
        "takeaways": int(bool(re.search(r"(?im)^#+ .*key takeaways", allmd))),
        "next": int(bool(re.search(r"(?im)^#+ *(next|what'?s next|where next)|\*\*Next", allmd))),
        "sample_data": int(bool(re.search(r"(?im)^#+ .*(sample data|setup and sample|the data)", allmd))),
        "difficulty": len(re.findall(r"\*\*Difficulty:\*\*", allmd)),
        "solutions": sol,
        "asserts": asserts, "assert_cells": assert_cells,
        "words": len(allmd.split()),
        "h2_list": " | ".join(h2),
    })
out = Path(sys.argv[2])
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(len(rows), "notebooks")
