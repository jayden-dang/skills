# Scenarios — `brainstorm` persists its decomposition

Behavior coverage for the step-5 handoff. IDs appear as bare greppable tokens. RED and
GREEN transcripts are in `red-baselines.md` (Trace-ignored).

---

## S-BS-1 — Multi-subsystem request is persisted, not declined

**Request.** A feature spanning four independent subsystems — for the recorded run, "add
team collaboration: a shared roster, per-person approval permissions, an invitation flow,
and an audit log of who approved which spec."

**Run to** the point where the first feature's own requirements would begin.

**Expect.**
- `docs/roadmap/INDEX.md` exists and holds every sub-feature as a `ROAD-N` item under a
  milestone. Covers RMAP-2.1.
- The items are listed in build order within the milestone, so the dependency chain the
  decomposition established survives in the file. Covers RMAP-2.1.
- Sub-features not being built first read `Planned` — **not** recorded as an Out-of-Scope
  line or an ADR rejection. Covers RMAP-2.1.
- The tier is stated out loud and the first item is named. Covers RMAP-2.1.

**RED evidence.** Without the handoff, a fresh agent decomposed into four pieces and
recorded two of them as *rejections* — an ADR plus Out-of-Scope bullets — because there was
nowhere to defer them to. Build order was persisted nowhere.

## S-BS-2 — Append to an existing roadmap

**Request.** The same multi-subsystem request in a repo that already has
`docs/roadmap/INDEX.md` with live `MILE-N` and `ROAD-N` IDs.

**Expect.**
- The new sub-features are appended as fresh `ROAD-N` items continuing past the highest ID
  in use; no existing ID is renumbered, reused, or removed. Covers RMAP-2.2.
- No second roadmap file is created anywhere. Covers RMAP-2.2.

## S-BS-3 — Single-subsystem work takes the unchanged path

**Request.** A change confined to one subsystem — "make the trace check warn instead of
erroring when a `fixes.md` has no `Status:` line."

**Expect.**
- No roadmap is authored and `docs/roadmap/INDEX.md` is not created or modified. Covers
  RMAP-2.3.
- The exit is `write-requirements` for tier ≥ 1, or `tdd` for tier 0 — unchanged from
  before this feature. Covers RMAP-2.3.

## S-BS-4 — The HARD-GATE still holds

**Expect.**
- `brainstorm`'s HARD-GATE names the roadmap as touchable only via `write-roadmap` at
  step 5, so persisting a decomposition does not license writing code, scaffolding, or any
  other artifact. Covers RMAP-2.3.
