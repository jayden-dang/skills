---
name: define-system-doc
description: >
  Use when the user wants to author or update one Hybrid 1A system-documentation
  artifact (catalog entry) — e.g. Codebase Map — via /define-system-doc <entry-key>,
  or when a consumer skill names that command because a standing doc is missing.
disable-model-invocation: true
---

# Define System Doc

Author **exactly one** pack-catalog entry per invocation. Unfinished work stays under
`.skills/system-docs/<entry-key>/`. Canonical consumer files are written only after
explicit human approval of a validator-passing proposal.

**Pack catalog SSOT (not installed into consumers):** this skill directory's
`catalog/CATALOG.md` and `catalog/entries/`.

## Resolve entry (bounded)

1. `SKILL_DIR` = directory containing this `SKILL.md`.
2. Read only `SKILL_DIR/catalog/CATALOG.md`; find the row for `<entry-key>`.
3. Load only the entry package path from that row (under `SKILL_DIR/`).
4. Load only template/validator paths named by the package (under `SKILL_DIR/`).
5. Do **not** load the full catalog body, every template, or the whole docs tree by default.

If the entry is not First-class or has no template, stop and say so — do not invent content.

## Ephemera

Unfinished work only under:

```
.skills/system-docs/<entry-key>/
  state.md
  evidence.md
  proposal.md
```

(entry-key path mirroring: `codebase/map` → `.skills/system-docs/codebase/map/`).

- `state.md` — catalog entry, canonical target, phase, confirmed decisions, None slots, open slots/blockers, rejected assumptions, defer condition, last verified revision.
- `evidence.md` — claims with grade Verified | Inference | Open; source; revision/env; slot.
- `proposal.md` — preview only; **never** SSOT; consumers must not read it as standing fact.

Resume: load entry package + state + canonical if present + open-slot evidence + template/validator. Do not replay chat, full catalog, or whole-repo rescan by default.

## Procedure (codebase/map and other First-class template entries)

1. **Start from one artifact** — never ask to configure the whole Hybrid 1A tree; never create empty consumer dirs/files just to start.
2. **Resume or init** ephemera.
3. **Evidence before facts** — separate Verified / Inference / Open. Cite file:line when Verified. Do not promote Inference about compliance, SLO targets, trust boundaries, ownership, runtime topology, or ops procedures without explicit human confirmation.
4. **Fill required template slots** — each ends as confirmed content, `None — <reason>`, or named `Blocker:`.
5. **Propose** full file or **targeted patch** (add/modify/remove selected content; preserve unrelated content). Complete replacement only as a fully reviewed new file body.
6. **Validate** with the entry's structural validator. If fail → do not offer approval; fix slots.
7. **Explicit human approval** required before any canonical write.
8. **Write** only the canonical consumer path for this entry. Set `Status: Approved` for single-file entries like `docs/codebase/map.md`. Never write mediated `Status: Draft` at canonical path. Never create sibling Hybrid 1A artifacts in the same write. Never whole-file clobber without a reviewed complete replacement proposal.
9. Prior Approved content stays authoritative until the new patch is approved and applied.
10. Mark digest **complete** in `state.md` after successful write. Canonical Approved + validator pass is the only SSOT for the subject.

## Authority (codebase/map)

- **Absent** — no `docs/codebase/map.md`
- **Non-authoritative** — file present but Status ≠ Approved or validator fail (including external Draft)
- **Approved** — `Status: Approved` and structural validator pass

## Forbidden

- Auto-invocation by model-invoked skills (this skill is user-invoked only)
- Empty-forest seeding
- Treating `proposal.md` or ephemera as standing project truth
- Claiming First-class readers that lack real consult hooks
