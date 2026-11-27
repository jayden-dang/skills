---
name: design-project
version: 1.0.0
description: "Use when choosing or assessing a project-wide design system and technical foundation, from greenfield and legacy UI to project takeover (including CLI/API) and migrations. Produces a diagrammed design and an evidence-backed decision on what is ready to build. Established standards and invariant edits belong to define-project."
---

# Design Project

Design the shared experience and the system that makes it true. Judge both
through the same representative flow. Work at project scope, from product
behavior to data, process and integration boundaries. The user owns the
deliverable location. A filename alone means a file at the checkout root.
When the user leaves the location open, use the repo’s review-note convention.

Use this for foundation decisions. A feature's screen exploration belongs to
`draft-ui`, its technical design to `design-solution`, and canonical project
records to `define-project`.

## 1. Establish the starting point

Choose every applicable row. Lead with takeover verification when the current
owner or deployed behavior is uncertain. Read only the code, runtime records,
standards and handover material relevant to the decision.

| Situation | First move |
|---|---|
| Greenfield | Pick the first valuable flow and its hardest outcome. Identify existing platform constraints and the smallest useful pilot. |
| Running product, fragmented or missing design system | Trace two existing consumers from what users see to the component, state and system authority. Identify where their presentation repeats and where the business meanings differ. |
| Takeover | Reproduce one local path. Reconcile the handover, checkout and available deployed evidence. Name the release, data and recovery owners or mark them unconfirmed. A different local path leaves the reported live topology and process inventory unconfirmed. |
| Evolving or migrating a foundation | Find the extension seams, existing consumers and compatibility obligations. Identify how old and new instances coexist, and what makes cutover or rollback safe. |

**Done when:** the brief names a primary flow, a consequential failure and
one plausible next consumer or change. Mark constraints and unanswered
questions that could reverse the design.

## 2. Compare and draw

Compare viable directions on the same flow and failure. Use product fit,
accessibility where relevant, ownership, cost of change, and relevant
operating constraints. Name what would change the recommendation. When only
one option meets a confirmed constraint, state the constraint and test the
surviving option.

- **Shared experience:** choose what to adopt, compose or build. Specify
  semantic tokens or conventions, reusable primitives and patterns,
  extension points and ownership. Keep feature state and rules with the
  component or layer responsible for them. For CLI/API, use the shared command,
  response and error conventions the flow needs.
- **Architecture:** name callers, modules, dependency direction, runtime or
  integration seams, authoritative state, and where permission, mutation and
  recovery are enforced. Show how the selected experience gets its result.

Read `diagrams.md` and draw the views that carry the decision. Include an
architecture view in every decision. Put the comparison and figures in the
review note.

**Done when:** the reader can follow the same outcome from the interface to
its authority and see what the alternatives would change.

## 3. Prototype and challenge the design

Run the smallest representative slice that crosses the seams under decision.
Run the selected direction through success and the consequential failure. A
passing baseline or a rejected mockup alone tests a different direction. Use
the project's real entry point, toolkit or adapter wherever its behavior is
the question. Use existing harnesses first, then disposable code in the
authorized scratch area. Use the smallest input that distinguishes the
outcomes. Give new concurrent or external probes a deadline and keep
production files untouched during exploration.

When comparing a broad standardization with gradual adoption, prototype the
smallest viable shared interface with two existing consumers in scratch. For
a status display, extract presentation only. Feed it both features’ current
messages and states and check they keep their meanings. This gives evidence
for one-consumer rollout before any wider adoption.

**Exercise the next change.** Run a second consumer through the proposed
interface, or apply and run the selected change in the scratch slice. For
example, run the same status primitive with a second feature’s own state and
check that queued still means queued. Use an existing adopter as the second
consumer when available. An unbuilt screen can already have a runnable
consumer check: for list and detail, use the same reader to check an existing
record and a missing ID in scratch. Label this as interface evidence. Record
what was reused, what changed and where. If the check cannot run, name the
specific missing input, permission or environment and the work it holds.

Record each load-bearing claim with **scope, command or source, observed
result, and what it leaves open**. Retain the script or exact invocation for
any new probe. A fake or fixture is evidence for the part it exercised. Make
the observed boundary visible in the figure as well as the note.

**Done when:** the primary, failure and next-change checks each have an
outcome or an explicit open entry.

## 4. Decide what can start

Apply the same four questions to the supported scope: does it fit the product,
can a second consumer use it, do the ownership boundaries hold, and can
someone run, change and operate it? Mark each material answer **observed**,
**off-target** or **open**. A well-presented design does not clear a missing
result.

- **Ready:** start the named slice. Its foundation-changing risks are settled
  at the scope where they matter.
- **Ready within limits:** start the named independent work and enumerate what
  waits. A test at one seam can support a slice at that seam. It cannot prove
  rollout or other seams.
- **Needs another check:** identify the smallest check that can change the
  verdict. Name the settled work, if any, that can proceed meanwhile.

For each held item, name the evidence that releases it and an owner or role
to get that evidence. Report the recommendation and any remaining operator
decision. When authorized to record accepted foundations, hand canonical
standards and architecture decisions to `define-project`. Hand the first
feature to the repo's normal spec and build workflow.

## Red Flags

- Recommending the mockup's “Complete” for both a durable save and a queued send.
- Testing only the rejected design, then recommending untried shared code.
- Treating a later reuse plan as a second consumer result.
- Describing two local call sites as two active production writers.
- Counting a skipped restore or a passing local storage probe as release evidence.
- Ending with a project-wide yes when checks covered independent local work.

**No-op:** a request only to update a settled document, review a screen, or
design one feature stays with its existing owner.
