# Ledger check

Loaded from `SKILL.md` **Ledger check**, applied by every execute-family
route before the first dispatch or Task 1.

Make `.skills/` local-only:

```
grep -qxF '.skills/' .gitignore 2>/dev/null || { printf '.skills/\n' >> .gitignore && git commit -m 'chore: ignore local skills artifacts' -- .gitignore; }
```

Read `.skills/<CODE>/progress.md` if it exists. Every task (and, on
story-unit, every unit) it marks complete IS complete — resume at the first
item it does not list.

A `Verified:` line is a completion claim. REQUIRED SUB-SKILL: use
`prove-claim`. The line itself is the slot: `Verified: <what holds> — by
<command>, covering <what>`. An ID alone is not a checkpoint.
