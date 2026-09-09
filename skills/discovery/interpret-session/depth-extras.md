# The deeper detail pass

Read this when the fork turns on ownership, boundary, lifecycle, distributed state, trust, or
compatibility — the cases where the four blocks in `SKILL.md` carry the decision but not yet
the evidence behind it. On a plain two-option fork, skip this file entirely.

**Contents:** [Decision boundary](#decision-boundary) · [The evidence pass](#the-evidence-pass) ·
[Where implementation detail goes](#where-implementation-detail-goes)

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
