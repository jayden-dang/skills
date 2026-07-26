# Cross-skill connectivity — unknowns loop

How the upgraded pieces connect (artifact paths, not chat memory).

```text
brainstorm step 1
  → .skills/<slug>-scan.md  (Blindspot section)
  → .skills/<slug>-knowns.md  (locks / KU / UK / assumptions)
  → grilling (blast-radius first; uses inventory as context)
  → research (criteria-first when user must pick)
  → prototype (unknown knowns / multi-variant)
  → write-requirements (locks only as SHALLs; assumptions stay design-open)
  → write-design
  → write-plan
        task **Risk** + **Decision surface**
        ## Human review order  (human attention)
        Depends-on               (execute-plan waves)
  → execute-plan
        implementer → .skills/implementation-notes.md on deviations
        DONE_WITH_CONCERNS → controller reads notes → correct-course if plan false
  → finish-branch
        names /comprehend-change (user-invoked)
        points at implementation-notes when present
  → handoff
        knowns + deviations + suggested /comprehend-change
```

## Integration checks run this campaign

| Link | Evidence |
|---|---|
| brainstorm → knowns + blindspot files | GREEN S-BS-STRUCT |
| write-plan Risk + Human review order | GREEN S-WP-U2 |
| implementer → implementation-notes.md | GREEN S-IMP-U2 |
| research criteria-first under pressure | GREEN S-RES-U2 |
| execute-plan controller row cites notes + correct-course | text shipped; full loop not re-run |
| handoff / AGENTS / finish-branch naming | text shipped; no pressure RED |

## Shared vocabulary

See `tests/unknowns/PROGRAM.md` and `AGENTS.md` (Unknowns loop paragraph).
