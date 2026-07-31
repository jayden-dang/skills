# Cross-skill connectivity — unknowns loop

How the upgraded pieces connect (artifact paths, not chat memory).

```text
frame-change step 1
  → .skills/<slug>-scan.md  (Blindspot section)
  → .skills/<slug>-knowns.md  (locks / KU / UK / assumptions)
  → probe-decisions (blast-radius first; uses inventory as context)
  → research (criteria-first when user must pick)
  → run-spike (unknown knowns / multi-variant)
  → specify-behavior (locks only as SHALLs; assumptions stay design-open)
  → design-solution
  → plan-tasks
        task **Risk** + **Decision surface**
        ## Human review order  (human attention)
        Depends-on               (build-continuous waves)
  → build-continuous
        implementer → .skills/implementation-notes.md on deviations
        DONE_WITH_CONCERNS → controller reads notes → reroute-plan if plan false
  → land-branch
        names /study-change (user-invoked)
        points at implementation-notes when present
  → write-handoff
        knowns + deviations + suggested /study-change
```

## Integration checks run this campaign

| Link | Evidence |
|---|---|
| frame-change → knowns + blindspot files | GREEN S-BS-STRUCT |
| plan-tasks Risk + Human review order | GREEN S-WP-U2 |
| implementer → implementation-notes.md | GREEN S-IMP-U2 |
| research criteria-first under pressure | GREEN S-RES-U2 |
| build-continuous controller row cites notes + reroute-plan | text shipped; full loop not re-run |
| write-handoff / AGENTS / land-branch naming | text shipped; no pressure RED |

## Shared vocabulary

See `tests/unknowns/PROGRAM.md` and `AGENTS.md` (Unknowns loop paragraph).
