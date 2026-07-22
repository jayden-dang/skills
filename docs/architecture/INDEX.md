# Architecture: Skills

Status: Draft
Date: 2026-07-22

<!--
The architecture spine: the small set of INVARIANTS that keep independently-built
features consistent — not a diagram doc. Optional. Each invariant is a bold
**ARCH-N** ID plus ONE imperative sentence (the rule). Feature design.md files cite
the ones they rely on as `Respects: ARCH-N`, and the `trace` check verifies those
citations point at a live invariant.

Rules:
- ID grammar: **ARCH-<n>**, flat and repo-wide (unique forever, never reuse).
- One rule per invariant. If it needs "and", it is usually two invariants.
- IDs are immutable once relied upon. Retire by strikethrough, never renumber:
    ~~**ARCH-3**~~ superseded by ARCH-7
  The `trace` check treats a struck invariant as retired — a design still citing it
  surfaces as an error.
- Large project? Split invariants into per-domain files (`docs/architecture/<domain>.md`)
  and list them under "Domains" below; the ARCH-N namespace stays flat across files.
-->

## Invariants

- **ARCH-1** Requirement IDs of the form `CODE-N.M` are first-class runtime objects: every covering test, task, and commit trailer must use the same greppable string as the requirements file.
- **ARCH-2** Skills never invent project configuration — they read `docs/agents/` (or stop and suggest `/setup-repo`).
- **ARCH-3** User-invoked skills (`disable-model-invocation: true`) are never auto-invoked by agents; model-invoked skills never invoke user-invoked skills.
- **ARCH-4** Iron Law gates (NO-CODE, TEST-FIRST, ROOT-CAUSE, EVIDENCE) are not weakened by workflow band, ceremony tier, or convenience.

## Domains

None — all invariants live above.
