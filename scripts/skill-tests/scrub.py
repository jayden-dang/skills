#!/usr/bin/env python3
"""scrub.py <name>… — after a skill is deleted, take its name out of lists, tables and see-also lines.

Whole rows, bullets and diagram lines that exist only to name it are removed; a name inside an inline
list is removed with its separator. Lines where it sits in prose are printed for a hand edit.
"""
import glob, re, sys
SKIP = ("/TESTS.md", "CHANGELOG.md", "/docs/releases/", "/docs/design/", "/.skills/", "/node_modules/")
files = sorted({f for pat in ("skills/**/*.md", "docs/**/*.md", "templates/**/*.md", "*.md")
                for f in glob.glob(pat, recursive=True) if not any(s in "/" + f for s in SKIP)})
for name in sys.argv[1:]:
    c = re.escape(name); tok = rf"(?:\*\*)?(?:\[`/?{c}`\]\([^)]*\)|`/?{c}`|/{c}\b|(?<![\w/-]){c}(?![\w-]))(?:\*\*)?"
    left = []
    for f in files:
        s = open(f).read()
        if not re.search(rf"(?<![\w-]){c}(?![\w-])", s): continue
        out = []
        for l in s.split("\n"):
            if not re.search(rf"(?<![\w-]){c}(?![\w-])", l): out.append(l); continue
            if re.match(rf"\s*\| ?{tok} ?\|", l) and l.count("|") >= 3 and not re.search(r"`,|, `", l.split("|")[1]): continue   # table row keyed by it
            if re.match(rf"\s*[-*] {tok}(\s+[—-].*)?$", l): continue                         # see-also bullet
            if re.match(rf"\s*/?{c}\s{{2,}}\S", l): continue                                   # diagram / command-list line
            n = re.sub(rf"{tok} ?(,|·|→|\+|/|and|or) ?", "", l, count=1) if re.search(rf"{tok} ?(,|·) ", l) else \
                re.sub(rf" ?(,|·|and|or) {tok}", "", l, count=1)
            if re.search(rf"(?<![\w-]){c}(?![\w-])", n): left.append(f"{f}: {l.strip()[:200]}")
            out.append(n)
        open(f, "w").write("\n".join(out))
    print(f"{name}: {len(left)} line(s) need a hand edit")
    for l in left: print("   ?", l)
