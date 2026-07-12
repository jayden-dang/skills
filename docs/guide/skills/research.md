# `research`

> Background investigation that turns "we'd have to check" into a cited note the team can trust. It informs the decision; it never makes it.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | primary sources only — official docs, library source, published specs and RFCs, first-party APIs and changelogs |
| **Writes** | exactly one markdown file, every claim cited, ending in an "Open decisions" section |
| **Calls** | `deep-research` (preferred for high-stakes questions, when installed); fan-out search subagents |
| **Called by** | [`brainstorm`](brainstorm.md) (evidence detour); any design, planning, or implementation skill facing an external-fact question |

## When it fires

When a design, planning, or implementation question turns on **external facts** — how a library or API actually behaves, what a standard, spec, or RFC says, platform limits, version differences — rather than opinion.

It also fires when the user asks to look into or investigate a topic and write it up with citations.

This is the "we'd have to check" detour: a question surfaces that no amount of preference can settle, so the work is handed off and the answer comes back as a note the team can trust.

The skill prefers dispatching a background subagent so the main conversation keeps moving, running inline only when the harness has no subagents. Either way the output is the same — a cited file — so the caller can pick up the answer whenever it lands rather than blocking on it.

## Primary sources only

There is a single organizing principle: answer from the source that *owns* the fact — official documentation, the library's actual source code, published specs and RFCs, first-party APIs and changelogs.

The owning source is the one that would be *right by definition* — the RFC defines the protocol, the library's source defines what the library does, the changelog defines when a behavior arrived. Everything downstream of it is a report that can be stale or wrong.

Tutorials, blog posts, and aggregated summaries are **leads, not evidence**. When one makes a claim, chase the claim back to the primary source and cite that instead. If a claim cannot be traced to an owning source, report it as unverified, not as fact — a plausible-sounding number with no owner is exactly what turns into a bug three sprints later.

## The output contract

The deliverable is fixed: exactly **one markdown file**, no more and no less, so the investigation lands as a single citable artifact rather than scattered across a chat.

- Every claim carries a citation to its primary source — a URL, or a file path plus symbol when the source is code being read.
- What the sources say is kept separate from what you conclude; anything unverified is marked as such.
- It is placed where the repo already keeps such notes, matching the existing convention. If none exists, pick a sensible spot (e.g. `docs/research/<date>-<topic>.md`) and state where you put it and why.
- It **ends with an "Open decisions" section**: the judgment calls the findings surface but do not settle. This is the seam between research and deciding — the note carries the facts right up to the decision and then stops, leaving the call to whoever owns it.

The point of placing it by convention rather than by rule is that a future reader — including a future you — finds it where they would look, not where this one run happened to drop it.

## High-stakes questions

Not every question deserves the same rigor. When the answer will steer an architecture choice or something else expensive to reverse, escalate.

If a `deep-research` skill is installed, prefer it — it already implements this fan-out and adversarial-verify loop end to end, so there is no reason to hand-roll it. Otherwise do it inline:

1. **Fan out 2–4 parallel search angles** — e.g. official docs, source code, issue tracker, spec text — as separate subagents, so no single source silently sets the answer.
2. **Adversarially verify before reporting.** For each key claim, actively look for a source that contradicts it, or a version or context in which it stops being true. Note conflicts explicitly rather than silently picking a side — a disagreement between two primary sources is itself a finding the decision needs to see.

## Research feeds thinking — it does not replace deciding

The note informs; it never decides. This is the line that keeps research from quietly becoming design.

Bring the findings back to the user (or the orchestrating skill, e.g. [`brainstorm`](brainstorm.md)) and put the resulting decision to them.

If the research was serving an interview, the decision goes through [`grilling`](grilling.md) like any other — the note supplies the fact, and the fact/decision split still applies.

## Worked example

During a `brainstorm` interview, a question surfaces that no one can answer from preference: "Does the Web Share API's `files` field work on desktop Safari, or only mobile?" That is a fact about an external system, so `brainstorm` detours to `research`.

Because a wrong answer would only cost a feature flag, not an architecture, the standard (not high-stakes) path applies — no fan-out, just a careful trace to the owning source. A background subagent reads the primary sources: the WHATWG spec text, the MDN compatibility data table, and the WebKit source. It writes one file, `docs/research/2026-07-10-web-share-files.md`:

> **Finding.** `navigator.canShare({ files })` returns `false` on desktop Safari 17 through the current build. *Source: [WebKit `Navigator.cpp`, `canShare()`](https://github.com/WebKit/WebKit/...), MDN compat table (retrieved 2026-07-10).*
>
> **Conclusion (mine, not the source's).** A desktop share-with-file flow needs a download fallback.
>
> **Open decisions.** Ship the download fallback for all desktop browsers, or feature-detect and hide the share button on desktop entirely? (Product call.)

The note is short by design — one finding, one conclusion, one open decision — because the value is in the citation trail and the honest labels, not in length.

Three details make this a trustworthy note rather than a guess. The finding is cited to the owning source — WebKit — while the MDN table, a lead, was used to point there and then confirmed against it. The conclusion is labelled as the author's, not the spec's, so no reader mistakes an inference for a fact. And the file ends on the one thing research must not settle — the product decision — which goes back through `grilling`.

## Why it is written the way it is

Two failure modes shape the skill.

The first is **citing a blog as if it were fact**. Aggregated summaries drift, lag versions, and repeat each other's errors, so the skill demotes them to leads and forces every claim back to the owning source. A citation to the source that *owns* the fact is the difference between a note the team can build on and one that quietly ages into a bug.

The second is **research quietly deciding**. An investigation that returns "so we should do X" has overstepped, because it never held the trade-offs the user does. Separating source claims from conclusions, and ending every note on "Open decisions", keeps the deciding where it belongs.

The one-file output contract ties both together: the investigation leaves a durable, checkable artifact instead of an answer buried in chat, and that artifact carries its own evidence and its own limits on its face.

## See also

- [`brainstorm`](brainstorm.md) — the caller that detours here for evidence
- [`grilling`](grilling.md) — where the decision goes after the note lands
- [`prototype`](prototype.md) — the other evidence detour, for "does it feel right" questions
- [Artifacts](../concepts/artifacts.md) — how the cited note fits the durable-record model
