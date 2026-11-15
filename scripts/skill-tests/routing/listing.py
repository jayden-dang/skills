#!/usr/bin/env python3
"""listing.py [--out FILE] — the skill listing a session sees: every model-invocable skill, name: description."""
import glob, sys, yaml
rows = []
for f in sorted(glob.glob("skills/*/*/SKILL.md")):
    d = yaml.safe_load(open(f).read().split("---", 2)[1])
    if not d.get("disable-model-invocation"):
        rows.append(f"- {d['name']}: {' '.join(str(d['description']).split())}")
text = "\n".join(rows) + "\n"
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
open(out, "w").write(text) if out else sys.stdout.write(text)
print(f"{len(rows)} skills, {len(text)} chars", file=sys.stderr)
