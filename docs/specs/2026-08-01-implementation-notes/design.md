# Design: Mid-build implementation notes

Feature code: IMPN
Status: Approved
Date: 2026-08-01
Requirements: ./requirements.md

## Context

Execute family already logs plan/territory disagreements to
`.skills/<CODE>/implementation-notes.md` with Task / Deviation / Cause / Choice /
Revisit (see `implementer-prompt.md`, `build-inline`). That matches Thariq’s
“implementation notes / Deviations” pattern but omits unknown classification and
map impact — so a reader cannot tell *what kind* of fog appeared or whether the
approved map still holds.

Discovery already owns pre-impl knowns (`frame-change` inventory +
`clarify-decisions` card closes). This feature **extends the mid-build log only**;
it does not merge discovery and execute into one file or auto-edit the triad.

**Binding constraint:** ARCH-3 — prose contract + source tests only; no runtime
parser in the consumer repo.

**Rejected:** a second `unknowns.md` mid-build file (duplicates SKNS single notes
path; IMPN-2.3).

## Decisions

1. **One file** — `.skills/<CODE>/implementation-notes.md` only (SKNS).
2. **Nine required fields** per entry (IMPN-1.2).
3. **Closed enums** for Unknown class and Map impact (IMPN-1.3–1.4).
4. **Map impact ≥ reroute-plan** → stop / `reroute-plan`; do not “log and pretend DONE.”
5. **Legacy five-field entries** — not rewritten; new writes use full set. Tests
   assert skill bodies prescribe the new set.
6. **Surface only** on write-handoff / package-change / land — no hard land block
   on open revisit (Out of Scope).
7. **SSOT snippet** — optional short recipe in
   `templates/skills-ephemera-paths.md` under implementation-notes basename, or
   a one-screen example in `build-in-waves/TESTS.md` / implementer-prompt.

## Architecture

### 1. Entry schema (normative example)

Satisfies: IMPN-1.1, IMPN-1.2, IMPN-1.3, IMPN-1.4, IMPN-1.5, IMPN-5.1
Reuse: rung 2 — extend existing implementation-notes contract
Respects: ARCH-3
Interface: append-only markdown entries; agents write by recipe
Depth: n/a — extends log shape
Locality: implementer-prompt + build-inline Deviations; leave discovery knowns

```markdown
### Task 4 — 2026-08-01

- **Task:** 4
- **Unknown class:** unknown-unknown
- **Map said:** Persist module id in Tauri store with sync flush
- **Territory showed:** plugin store flushes async; hard-kill can drop last write
- **Deviation:** write then await explicit flush; document hard-kill in Revisit
- **Cause:** store API does not guarantee durability on kill
- **Choice:** await flush; no new persistence backend
- **Map impact:** revisit-only
- **Revisit:** confirm SHELL-1.2 wording after dogfood hard-kill case
```

Append only — never overwrite prior `### Task` blocks (IMPN-5.1).

**Unknown class:** `known-unknown` | `unknown-known` | `unknown-unknown` |
`assumption-break` | `blindspot`

**Map impact:**

| Value | Meaning | Controller move |
|---|---|---|
| `none` | map still fine; local impl detail | continue |
| `revisit-only` | map ok for now; human/later check | continue; surface in handoff |
| `reroute-plan` | plan/design/req falsified or shared contract | stop → `reroute-plan` |
| `realign-spec` | shipped/approved text wrong as written | stop → name `realign-spec` / human |

### 2. Execute family wiring

Satisfies: IMPN-1.6, IMPN-1.7, IMPN-2.1, IMPN-2.2, IMPN-2.3, IMPN-4.2, IMPN-4.3, IMPN-4.4
Reuse: rung 2 — build-in-waves / build-by-story / build-inline
Respects: ARCH-5 (no new user-invoked skill)
Interface: same Deviations section text across routes
Depth: n/a
Locality: extend execute skills + TESTS.md; leave pathfind/research

| File | Change |
|---|---|
| `skills/execution/build-in-waves/implementer-prompt.md` | Replace five-field list with nine-field recipe + enums + map-impact stop rule |
| `skills/execution/build-in-waves/SKILL.md` | DONE_WITH_CONCERNS: incomplete without notes path; reroute when Map impact requires |
| `skills/execution/build-by-story/SKILL.md` | Same DONE_WITH_CONCERNS row language |
| `skills/execution/build-inline/SKILL.md` | Deviations step lists full field set |
| `skills/execution/build-in-waves/TESTS.md` | Pressure: legacy 5-field only = incomplete; map impact reroute must stop |

### 3. Post-build surface

Satisfies: IMPN-3.1, IMPN-3.2, IMPN-3.3
Reuse: rung 2 — write-handoff, package-change, land-branch
Interface: path + counts, not full dump
Depth: n/a
Locality: extend those three skills only

| Skill | Behavior |
|---|---|
| `write-handoff` | Path + count of entries with Map impact ≠ `none` |
| `package-change` | If any ≠ `none`, mention notes path once as mid-build why authority |
| `land-branch` | Mention path when deviations present; call out unresolved `reroute-plan` / `realign-spec` impacts |

### 4. Docs / SSOT pointer

Satisfies: IMPN-2.3, IMPN-4.1, IMPN-4.4
Reuse: rung 2 — templates/skills-ephemera-paths.md basename row already names the file
Locality: one short “entry fields” blurb under that basename; AGENTS one-liner optional

### 5. Verification

Satisfies: all IDs via source contract
Reuse: rung 2 — unittest like SKNS/FSUB

| Seam | Kind | Covers |
|---|---|---|
| implementer-prompt lists all 9 field names + both enums | unit | IMPN-1.2–1.4, 2.1 |
| build-inline Deviations lists same fields | unit | IMPN-2.2 |
| build-in-waves + build-by-story mention incomplete-without-notes / Map impact stop | unit | IMPN-1.6, 1.7 |
| write-handoff / package-change / land mention notes + map impact surface | unit | IMPN-3.1–3.3 |
| path remains `.skills/<CODE>/implementation-notes.md` | unit | IMPN-2.3, 4.4 |
| scenarios.md greps every IMPN-N.M | unit | coverage |
| pressure: 5-field-only incomplete; silent stretch forbidden | scenario | IMPN-1.5–1.7 |
| pressure: append two entries | scenario | IMPN-5.1 |
| discovery skills still own knowns inventory language | unit | IMPN-4.1 |

## Coverage check

| IDs | Section |
|---|---|
| 1.1–1.5, 5.1 | §1 schema |
| 1.6–1.7, 2.1–2.3, 4.2–4.4 | §2 execute |
| 3.1–3.3 | §3 surface |
| 4.1 | §4 docs + discovery leave |
| all | §5 seams |

No unmapped IDs.
