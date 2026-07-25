# Scenarios — `write-roadmap`

Behavior coverage for the authoring skill. Each scenario names the requirement IDs it
verifies as bare greppable tokens. RED baselines for these live in `red-baselines.md`
(Trace-ignored); the observed GREEN outcomes are recorded there too.

Run a scenario by giving a fresh agent the request text against a repo that has the skill
and `templates/roadmap-INDEX.md`, then checking the expectations.

---

## S-WR-1 — Author a roadmap from a spoken decomposition

**Request.** "Plan the next few milestones for a note-taking app. The work: offline note
capture, full-text search, sharing a note by link, mobile sync. Search and sharing both
need the note storage layer reworked. Mobile sync depends on offline capture existing
first."

**Expect.**
- The file is written to `docs/roadmap/INDEX.md`, from `templates/roadmap-INDEX.md`, with
  every REQUIRED slot filled or `None`. Covers RMAP-1.1.
- Each milestone carries a one-sentence `Outcome:` naming what a person can do, plus a
  `Commitment:` of `Planned`, `Committed`, or `Closed`. Covers RMAP-1.2.
- Each item is a `ROAD-N` plus a slug under exactly one milestone. Covers RMAP-1.3.
- No feature code appears anywhere in the file. Covers RMAP-1.4.
- Each item carries a `Surfaces:` line, or `None` with a reason. Covers RMAP-1.20.
- A milestone whose only outcome would be work performed — "the storage layer is
  rewritten" — is folded into the milestone it enables rather than standing alone.
  Covers RMAP-1.2.
- **No progress column, no per-milestone status field, no change log, no percent
  complete.** Covers RMAP-3.14.
- `docs/specs/INDEX.md` is not modified. Covers RMAP-1.14.
- The whole file is presented and `Status:` stays `Draft` absent an explicit approval.
  Covers RMAP-1.17.

## S-WR-2 — Author with a vision present

**Request.** Same as S-WR-1, in a repo whose `docs/product/vision.md` carries live
`**GOAL-N**` IDs.

**Expect.**
- Each milestone's `Goals:` cites the live `GOAL-N` IDs it serves. Covers RMAP-1.8.
- Every live goal no milestone cites appears under `## Goal dispositions` as `Deferred` or
  `Out-of-scope` with a date and a reason. Covers RMAP-1.15.

## S-WR-3 — Author with no vision

**Request.** Same as S-WR-1, in a repo with no `docs/product/vision.md`, or one whose
goals carry no IDs.

**Expect.**
- `Goals: None` on every milestone and an empty dispositions table, with the reason
  stated. Covers RMAP-1.9.

## S-WR-4 — Drop an item from an approved roadmap

**Request.** Against an `Approved` roadmap: "Drop ROAD-4 search-ui from MILE-2 entirely —
we are not doing a custom search UI."

**Expect.**
- `ROAD-4` is struck through in place with a date and a reason, not deleted. Covers
  RMAP-1.7.
- `Status:` is demoted to `Draft` and the gate re-entered. Covers RMAP-1.19.
- The whole revised file is presented; `Approved` is not restored without an explicit
  approval. Covers RMAP-1.17.

## S-WR-5 — Reorder an approved roadmap

**Request.** Against an `Approved` roadmap: "Sharing matters more than search now. Move
Sharing ahead of Search."

**Expect.**
- Row and section order change; **no** `MILE-N` changes number. Covers RMAP-1.11.
- A `ROAD-N` moved between milestones keeps its ID. Covers RMAP-1.12.
- `Status:` is demoted to `Draft`. Covers RMAP-1.19.

## S-WR-6 — Close a milestone

**Request.** "MILE-1 shipped in v0.4.0."

**Expect.**
- `Commitment:` becomes `Closed` and the `Closed:` slot records the release tag or commit.
  Covers RMAP-1.10.

## S-WR-7 — Structural defect withholds the gate

**Request.** Ask for approval of a roadmap carrying, one at a time: a duplicate `MILE-N`;
a `ROAD-N` under two milestones; a milestone with an empty `Outcome:`; a `Depends-on`
naming a later row; a `Depends-on` naming an undefined milestone; a live `GOAL-N` neither
cited nor dispositioned.

**Expect.**
- Each defect is reported against its `S1`–`S7` rule and the roadmap is **not** presented
  for approval until resolved. Covers RMAP-1.18.

## S-WR-8 — Frontmatter is model-invocable

**Expect.**
- `skills/project/write-roadmap/SKILL.md` frontmatter carries no `disable-model-invocation`,
  so `brainstorm` can reach it. Covers RMAP-1.13.
- Registered in `AGENTS.md` §3, §8, §11 and the guide index — in this repo that index is
  the discovery surface, not the description alone. Covers RMAP-1.13.
