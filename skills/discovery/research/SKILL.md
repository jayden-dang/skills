---
name: research
description: Use when a design, planning, or implementation question turns on external
  facts — how a library or API actually behaves, what a standard, spec, or RFC
  says, platform limits, version differences — rather than opinion, or when
  the user asks to look into or investigate a topic and write it up with
  citations.
---

# Research

Background investigation that turns "we'd have to check" into a cited note the team can trust.

Prefer dispatching a background subagent so the main conversation keeps moving; run inline if the harness has no subagents.

## Primary sources only

Answer from the source that *owns* the fact: official documentation, the library's actual source code, published specs and RFCs, first-party APIs and changelogs. Tutorials, blog posts, and aggregated summaries are leads, not evidence — when one makes a claim, chase the claim back to the primary source and cite that. If a claim cannot be traced to an owning source, report it as unverified, not as fact.

## Output contract

Exactly **one markdown file**:

- Every claim carries a citation to its primary source (URL, or file path + symbol for code reading).
- Separate what the sources say from what you conclude; mark anything unverified.
- Place it where the repo already keeps such notes — match the existing convention. If no convention exists, pick a sensible spot (e.g. `docs/research/<date>-<topic>.md`), and state where you put it and why.
- End the file with an "Open decisions" section: the judgment calls the findings surface but do not settle.

## High-stakes questions

When the answer will steer an architecture choice or something else expensive to reverse, escalate the rigor. Not every unknown qualifies: "which date-formatting library" feels weighty but is cheap to swap behind a thin wrapper, so it takes the standard path — a careful trace to the owning source, no fan-out. Reserve the escalation for facts that steer something costly to undo: a storage format, a concurrency model, a public API contract, a security boundary. If a `deep-research` skill is installed, prefer it — it already implements this fan-out + adversarial-verify loop end to end. Otherwise do it inline:

1. Fan out 2–4 parallel search angles (e.g. official docs, source code, issue tracker, spec text) as separate subagents.
2. Adversarially verify before reporting: for each key claim, actively look for a source that contradicts it or a version/context in which it stops being true. Note conflicts explicitly rather than picking a side silently.

## Research feeds thinking — it does not replace deciding

The note informs; it never decides. Bring the findings back to the user (or the orchestrating skill, e.g. `brainstorm`) and put the resulting decision to them. If the research was serving an interview, the decision goes through `grilling` like any other.
