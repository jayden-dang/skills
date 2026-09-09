# The deeper detail pass

Read this for either of two reasons: a drawing is due (`SKILL.md`'s trigger — a `Locality` naming
more than one component, or an `Invariant` naming a shared resource), or the fork turns on
ownership, boundary, lifecycle, distributed state, trust, or compatibility, where the four blocks
carry the decision but not yet the evidence behind it. Neither holds → skip this file.

**Contents:** [What a drawing looks like](#what-a-drawing-looks-like) ·
[Decision boundary](#decision-boundary) · [The evidence pass](#the-evidence-pass) ·
[Where implementation detail goes](#where-implementation-detail-goes)

## What a drawing looks like

The picture describes **the system**, not the menu. Its job is to make the argument legible: the
reader should be able to point at the box where the problem happens. Pick the kind the fork turns
on — one picture, whichever kind fits.

Name the job before the first mark, from the set this repo already uses for figures
(`craft-page`'s recipes) — do not invent a fifth name for one of these:

| Job | Use it when the fork is about |
|---|---|
| **topology / architecture** | what calls what, where work happens, which layer owns a rule. A question about *who decides* a value is this job with the owner labelled on the box |
| **sequence** | order, blocking, a window, a race — anything whose argument is "and then" |
| **before/after structure** | the change moves a boundary, and the point is which side something lands on |
| **flowchart** | a process with branches that the reader has to walk |

### Which form — ASCII or mermaid

Keyed to where the drawing is read, not to taste:

- **Stays in the companion turn** → ASCII. It is read in a terminal, and a terminal renders no
  mermaid. Every drawing measured here was ASCII.
- **Travels into something that renders it** — a doc, a PR body, an artifact, a repo markdown
  file → mermaid, which is versionable and renders in GitHub, VS Code and Notion.

Two mermaid mechanics worth knowing before you write one: an unknown word breaks the diagram, and
a bad parameter **fails silently** rather than erroring — so a diagram that renders is not proof
the diagram says what you meant. Braces inside a `%%` comment break it too.

### Worked — flow, for a fork about a shared worker

```
  ingest ──▶ deliveries(pending) ──▶ drain() ──▶ dispatch() ──▶ partner endpoint
                                       │            │
                                       │            └─ retries inline: sleep 2,4,8,16,32s
                                       └─ one worker, 100 rows a pass, strictly in order:
                                          row N+1 starts only once row N's retries end
```

Everything the argument needs is now pointable. The retry budget lives in the box on the right;
the cost of raising it lands in the box on the left, which belongs to everyone. That sentence is
read off the picture rather than asserted at the reader.

### Worked — sequence, same system, different question

```
  t=0      partner stops answering
  t=0      delivery 1 starts its 5 attempts   ─┐
  t=62s    delivery 1 gives up, marked dead    │  deliveries 2..100 sit idle,
  t=62s    delivery 2 starts                   │  nothing wrong with any of them
  t=2h04m  delivery 100 finally starts        ─┘
```

Same code, and the second drawing answers a question the first cannot: how long the queue is
behind, which is what the incident was actually about. Draw the state that changes; leave out the
architecture that does not.

## Decision boundary

After the stance, state what locks if they accept the pick and what stays open. Write it whenever
adjacent constraints could ride in on a one-word approval — a schema shape that fixes a migration
path, a boundary that fixes who validates. This is what the carry-back's **Lock** slot is built
from later, so an imprecise boundary here becomes an over-broad lock there.

## The evidence pass

Label each block with the claim it is making, so the user can tell what you checked from what you
concluded:

- **Source claim** — what the paste asserts.
- **Verified fact** — what you read, cited `file:line` or a commit, ending in `→` and what the
  fact does to the live choice. A fact whose consequence the reader must assemble is homework.
- **Inference** — supported by the evidence but not stated by it. Say which pieces.
- **Open question** — no source answers it, and it matters.

Cover, where they apply:

| Element | Covers |
|---|---|
| **Where the paste and the repo disagree** | every claim about current behaviour that the code contradicts, with the citation |
| **What the history settled** | the commit, incident, or revert that already bounded this decision, and whether either shape respects it |
| **Alternatives** | at least one genuinely different shape neither the paste nor the stance led with |
| **Hidden assumptions** | what the paste takes for granted that does not hold in this repo |
| **Risks** | where each shape bites later, tied to the posture |
| **A concrete walk when the territory leaves the repo** | a card argued on an external standard or library gets one real artifact — a sample log line, a trace sketch, the query they would run. The walk does for external territory what `file:line` does for the repo |

## Where implementation detail goes

Version pins, shutdown ordering, retry constants, test lists — the grade of detail the
implementing session consumes, not the deciding user. Collapse them into a short *for the spec*
tail at the end, or carry them as **Weigh** items in the carry-back. They do not belong mid-argument.
