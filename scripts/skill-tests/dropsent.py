#!/usr/bin/env python3
"""dropsent.py <name>… — in prose and table rows that still name a deleted skill, drop the sentence or the row."""
import glob, re, sys
SKIP = ("/TESTS.md", "CHANGELOG.md", "/docs/releases/", "/docs/design/", "/.skills/", "/node_modules/")
files = sorted({f for pat in ("skills/**/*.md", "docs/**/*.md", "templates/**/*.md", "*.md")
                for f in glob.glob(pat, recursive=True) if not any(s in "/" + f for s in SKIP)})
for name in sys.argv[1:]:
    pat = re.compile(rf"(?<![\w-]){re.escape(name)}(?![\w-])")
    for f in files:
        s = open(f).read()
        if not pat.search(s): continue
        out = []
        for l in s.split("\n"):
            if not pat.search(l): out.append(l); continue
            if l.lstrip().startswith("|"):
                print(f"  row- {f}: {l.strip()[:150]}"); continue
            if l.lstrip().startswith("#"):
                print(f"  HEAD {f}: {l.strip()[:150]}"); out.append(l); continue
            parts = re.split(r"(?<=[.!?:])\s+", l)
            kept = [p for p in parts if not pat.search(p)]
            n = " ".join(kept)
            print(f"  sent {f}: {l.strip()[:110]}  =>  {n.strip()[:90] or '(line removed)'}")
            if n.strip(): out.append(n)
        open(f, "w").write("\n".join(out))
