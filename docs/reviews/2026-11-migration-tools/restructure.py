"""Turn 'Practice questions / Answers / Summary' endings into Check yourself (hidden answers), Key takeaways, Next."""
import ast
import json
import re
import sys
from pathlib import Path


def src(c):
    return "".join(c["source"]) if isinstance(c["source"], list) else c["source"]


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n")}


def code(text, solution=False):
    return {"cell_type": "code", "metadata": {"tags": ["solution"]} if solution else {}, "source": text.strip("\n"), "outputs": [], "execution_count": None}


def split_sections(text):
    """Split a markdown cell at '## ' headings (outside fences) into [(heading or None, text)]."""
    parts, current, fence = [], [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
        if not fence and re.match(r"## [^#]", line) and current:
            parts.append("\n".join(current))
            current = []
        current.append(line)
    if current:
        parts.append("\n".join(current))
    return [p.strip("\n") for p in parts if p.strip()]


def strip_asserts(code_text):
    try:
        tree = ast.parse(code_text)
    except SyntaxError:
        return code_text
    lines = code_text.splitlines(keepends=True)
    spans = [(n.lineno - 1, n.end_lineno) for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    for start, end in sorted(spans, reverse=True):
        indent = re.match(r"\s*", lines[start]).group(0)
        # an assert alone in a block body would leave it empty
        lines[start:end] = [f"{indent}pass\n"] if indent and (start == 0 or lines[start - 1].rstrip().endswith(":")) else []
    out = re.sub(r"\n{3,}", "\n\n", "".join(lines)).strip("\n")
    if "show(" not in out and "print(" not in out:
        names = re.findall(r"^(\w+)\s*=\s*(?:\"\"\"|\")", out, re.M)
        if names:
            out += f"\nspark.sql({names[-1]}).show()"
    return out


def parse_questions(body):
    body = re.sub(r"^## Practice questions\s*", "", body).strip()
    items = re.split(r"(?m)^(\d+)\.\s+", body)
    intro, qs = items[0].strip(), {}
    for i in range(1, len(items), 2):
        qs[int(items[i])] = "\n".join(l[3:] if l.startswith("   ") else l for l in items[i + 1].strip().splitlines())
    return intro, qs


def restructure(path, takeaways=None, next_line=None, notes=None, stub="# Write your query here.", intro_text="Write each query in the empty cell under its question, run it, then open the answer to compare."):
    nb = json.loads(Path(path).read_text())
    cells = nb["cells"]
    # explode combined markdown cells into one cell per '## ' section
    exploded = []
    for c in cells:
        if c["cell_type"] == "markdown" and len(re.findall(r"(?m)^## [^#]", src(c))) > 1:
            exploded += [md(p) for p in split_sections(src(c))]
        else:
            exploded.append(c)
    cells = exploded
    head = lambda c: src(c).split("\n")[0] if c["cell_type"] == "markdown" else ""
    qi = next(i for i, c in enumerate(cells) if head(c).startswith("## Practice questions"))
    ai = next(i for i, c in enumerate(cells) if head(c).startswith("## Answers"))
    summary = next((src(c) for c in cells if head(c).startswith("## Summary")), None)
    intro, questions = parse_questions(src(cells[qi]))
    # answers run until the next '## ' heading
    end = next((i for i in range(ai + 1, len(cells)) if head(cells[i]).startswith("## ")), len(cells))
    answers, current = {}, None
    for c in cells[ai + 1:end]:
        m = re.match(r"### Question (\d+)", head(c))
        if m:
            current = int(m.group(1))
            answers[current] = {"explain": src(c).split("\n", 1)[1].strip() if "\n" in src(c) else "", "code": []}
        elif current is not None:
            if c["cell_type"] == "code":
                answers[current]["code"].append(src(c))
            else:
                answers[current]["explain"] += "\n\n" + src(c)
    trailing = cells[end:]
    keep = [c for i, c in enumerate(cells[:ai]) if i != qi and not head(c).startswith("## Summary")]
    out = keep + trailing
    out.append(md("## Check yourself\n\n" + intro_text + (f"\n\n{intro}" if intro else "")))
    for n in sorted(questions):
        out.append(md(f"**Q{n}.** {questions[n]}"))
        out.append(code(stub))
        ans = answers.get(n, {"explain": "", "code": []})
        comment = "\n".join("# " + l if l.strip() else "#" for l in ans["explain"].strip().splitlines())
        body = "\n\n".join(strip_asserts(c) for c in ans["code"])
        out.append(code((comment + "\n" if comment else "") + body, solution=True))
    if takeaways is None and summary:
        takeaways = re.sub(r"^## Summary\s*", "", summary).strip()
    if takeaways:
        out.append(md("## Key takeaways\n\n" + takeaways.strip()))
    if next_line:
        out.append(md("**Next:** " + next_line))
    nb["cells"] = out
    Path(path).write_text(json.dumps(nb, indent=1) + "\n")
    return len(questions), len(answers), bool(takeaways)


def add_notes(path, notes):
    """notes: {code_cell_source_prefix: note text}; inserts a What to notice cell after each matching code cell."""
    nb = json.loads(Path(path).read_text())
    out, used = [], set()
    for c in nb["cells"]:
        out.append(c)
        if c["cell_type"] != "code" or "solution" in c.get("metadata", {}).get("tags", []):
            continue
        s = src(c)
        for key, note in notes.items():
            if key not in used and key in s:
                out.append(md("**What to notice:** " + note.strip()))
                used.add(key)
                break
    missing = [k for k in notes if k not in used]
    nb["cells"] = out
    Path(path).write_text(json.dumps(nb, indent=1) + "\n")
    return missing


if __name__ == "__main__":
    print(restructure(sys.argv[1]))
