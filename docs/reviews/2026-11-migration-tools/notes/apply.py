import importlib.util, json, re, sys
from pathlib import Path
sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
import restructure
ROOT = Path("/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/review/notebooks/topics")
spec = importlib.util.spec_from_file_location("n", sys.argv[1]); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
path = ROOT / mod.PATH
nb = json.loads(path.read_text())
for old, new in getattr(mod, "REPLACE", []):
    hits = 0
    for c in nb["cells"]:
        s = "".join(c["source"])
        if old in s:
            c["source"] = s.replace(old, new); hits += 1
    if hits != 1: print("REPLACE hits", hits, repr(old[:60]))
path.write_text(json.dumps(nb, indent=1) + "\n")
missing = restructure.add_notes(path, mod.NOTES)
print(mod.PATH, "notes:", len(mod.NOTES), "missing:", missing)
