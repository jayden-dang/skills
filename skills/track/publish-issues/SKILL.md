---
name: publish-issues
version: 1.1.0
description: Turns a conversation, an approved spec, or a rough idea into agent-ready tracker issues
  — tracer-bullet slices with blocking edges, published to the configured tracker. Run it
  with /publish-issues.
disable-model-invocation: true
---

# Publish Issues

Turn what is in front of you — this conversation, a spec, or an idea the user just described — into a set of **tracer-bullet issues** on the repo's tracker, each declaring the issues that **block** it. This is the outgoing counterpart to `triage`'s incoming queue.

Read the tracker operations from `docs/agents/issue-tracker.md` and the label strings from `docs/agents/triage-labels.md`. Write each issue as `docs/agents/issue-tracker.md` **Issue format** says. No such section, or either file missing: name `/configure-repo`, show the draft, create nothing.

## Where this sits

Pick the right skill before drafting; do not duplicate a heavier one.

| You have | Use | Not |
|---|---|---|
| A conversation / idea / spec to capture as grabbable work | **`publish-issues`** (this) | — |
| A tier-2 feature needing traceable `requirements.md` → `design.md` → `tasks.md` | `plan-tasks` (publishes **one feature issue** by default) | `publish-issues` |
| A raw incoming issue or external PR to evaluate | `/triage` — user-invoked; name it for the user to run | `publish-issues` |

If the user already ran the full spec triad, `plan-tasks` publishes **one feature issue** with union `Requirements covered:` — do not re-file plan tasks here. `publish-issues` is for work that never went through the triad.

## Process

### 1. Gather context

Work from what is already in the conversation. If the user passes a reference — a spec path, an issue number or URL — read its full body and comments first. **Done when:** every reference the user passed has been read in full, and the scope to be filed is written down as an explicit in/out list.

### 2. Explore the codebase

If you have not already, explore the code so titles and descriptions use the project's **domain glossary** (`CONTEXT.md`) and respect the ADRs in the area you touch. Look for **prefactoring** that makes the later work easier — "make the change easy, then make the easy change"; a prefactor becomes its own first issue. **Done when:** every domain noun in the slice titles appears in `CONTEXT.md`, and a prefactor is either filed as the first slice or explicitly ruled out.

### 3. Draft vertical slices

Break the work into **tracer-bullet** issues.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT a horizontal slice of one layer.
- A completed slice is demoable or verifiable on its own.
- Each slice is sized to fit in a single fresh context window.
- Any prefactoring is sequenced first.

</vertical-slice-rules>

Give each slice its **blocking edges** — the other slices that must complete before it can start. A slice with no blockers can start immediately.

**Wide refactors are the exception.** A wide refactor is one mechanical change — rename a column, retype a shared symbol — whose blast radius fans across the codebase, so a single edit breaks thousands of call sites at once and no vertical slice lands green. Sequence it as **expand → migrate → contract**: first add the new form beside the old (nothing breaks); then migrate call sites in batches sized by blast radius (per package, per directory), each batch an issue blocked by the expand, CI green batch to batch because the old form still exists; finally delete the old form in an issue blocked by every migrate batch. If even the batches cannot stay green alone, let them share an integration branch that all block a final integrate-and-verify issue — green is promised only there.

**Done when:** every slice is vertical (or a justified refactor batch) and carries its blocking edges.

### 4. Quiz the user

Present the breakdown as a numbered list. Per slice show **Title**, **Blocked by**, and **What it delivers** (the end-to-end behavior it makes work). Then ask:

- Is the granularity right — too coarse, too fine?
- Are the blocking edges correct — does each slice depend only on slices that genuinely gate it?
- Should any be merged or split?

When a slice is underspecified in a way only the user can resolve, REQUIRED SUB-SKILL: use `clarify-decisions` to shape it one question at a time before publishing. Iterate until the user approves the breakdown. **Done when:** the user has approved the slices and their edges.

### 5. Publish

Publish the approved slices to the configured tracker in **dependency order — blockers first** — so each slice's edges can reference real identifiers. The slices are the same on every tracker; only the shape of the blocking edge changes.

- **Local files** → one file per slice under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order. Never a single combined file.
- **Remote tracker (github / gitlab / linear)** → one issue per slice, in dependency order, with its blocking edge as **Issue format** says.

**Every slice carries the same state role**, `ready-for-agent` (its mapped string from `docs/agents/triage-labels.md`). The blocking edge holds a blocked slice back: `/board` and `/go` read it from the tracker's relation or the `Blocked by:` line. A baseline on a tracker with no relation left the blocked slice with a category label alone, against the repo's one-state rule. Local `.scratch/` files have no such reader, so their `Status:` reads `ready-for-agent` on the frontier and `blocked` behind it.

Work the **frontier**: publish any slice whose blockers are already published. For a purely linear chain that is top to bottom. **Do not close or modify any parent issue.** **Done when:** every approved slice exists on the tracker with its edges wired and its one state role, and the read-back shows them.

An issue filed from an existing one uses the tracker's parent relation where `docs/agents/issue-tracker.md` names one, else a last line `Parent: #N`. Where specs are shared and an existing spec covers the work, the last line is `Requirements covered:` with its IDs.

## Exit

Tell the user the frontier — which slices can start now. Point them at the next step: work each slice with the execute family (`build-in-waves` / `build-by-story` / `build-inline`) or standalone `test-first`, clearing context between slices.
