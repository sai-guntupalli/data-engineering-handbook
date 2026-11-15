"""Insert What to notice notes after code cells given by index (indices of the notebook before any notes)."""
import importlib.util, json, sys
from pathlib import Path
ROOT = Path("/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/review/notebooks/topics")
spec = importlib.util.spec_from_file_location("n", sys.argv[1]); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
path = ROOT / mod.PATH
nb = json.loads(path.read_text())
for idx in sorted(mod.NOTES, reverse=True):
    cell = nb["cells"][idx]
    assert cell["cell_type"] == "code", (idx, cell["cell_type"])
    if mod.EXPECT.get(idx):
        assert mod.EXPECT[idx] in "".join(cell["source"]), (idx, mod.EXPECT[idx])
    nb["cells"].insert(idx + 1, {"cell_type": "markdown", "metadata": {}, "source": "**What to notice:** " + mod.NOTES[idx].strip()})
path.write_text(json.dumps(nb, indent=1) + "\n")
print(mod.PATH, "notes:", len(mod.NOTES))
