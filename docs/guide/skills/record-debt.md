# `record-debt`

> Banks a finding that was judged real and consciously left unfixed into the durable ledger at `docs/quality/debt.md`. A decision, not an observation.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/record-debt` — user-invoked; the agent cannot call it |
| **Reads** | findings named in the invocation, `docs/agents/issue-tracker.md` |
| **Writes** | `docs/quality/debt.md` (created from `templates/quality-debt.md` when absent) |
| **Calls** | [`prove-claim`](prove-claim.md) (before an entry may be closed) |
| **Called by** | nothing — see *The gap worth knowing about* below |

## When it fires

When a finding has been judged real and someone decided not to fix it now. The premise is one sentence:

> A finding that was judged real and consciously left unfixed is a **decision**. Decisions survive the session that made them; observations do not need to.

Everything it writes goes to a tracked file in `docs/` — not `.skills/` (git-ignored and reconstructed from `git log`, and a finding is not in `git log`), not a session report, not a commit message body.

## What earns an entry

All three, or there is nothing to record:

1. **A named finding** — a specific defect, smell, gap, or risk at a specific place.
2. **A judgment that it is real** — someone evaluated it and did not dismiss it as a false positive.
3. **A decision not to fix it now**, with a reason.

| Situation | Entry? |
|---|---|
| [`polish-diff`](polish-diff.md) dropped it as "outside the pinned diff" | **Yes** — real, judged, deferred |
| `polish-diff` dropped it as a false positive | No — fails (2); the drop reason is the record |
| [`inspect-change`](inspect-change.md) Minor nobody will action this branch | **Yes** |
| `inspect-change` Critical or Important | No — those are fixed before merge, not banked |
| [`configure-repo`](configure-repo.md) step 6 **content** failure (pre-existing red suite) | **Yes** |
| `configure-repo` step 6 **wiring** failure | No — that is a config bug, fix it |
| [`vet-feedback`](vet-feedback.md) item confirmed correct but deferred | **Yes** |
| Code you think could be nicer, that no pass flagged | No — *a ledger that admits opinions stops being read* |

Given nothing to bank, the skill asks. It does **not** go read the code and invent findings — a fresh reading produces observations, and observations fail the admission test.

## The entry

Every entry fills every slot; a slot with no answer gets `Unknown` rather than being omitted.

```markdown
### **DEBT-7** `src/report-builder.ts` — buildMonthlyReport nests four levels deep on `opts: any`

- **Found:** 2026-08-10 · polish-diff on `feat/csv-export`
- **Cost:** every new report option adds another branch; the tax rule is duplicated
  between the paid and pending arms, so a rate change must find both
- **Deferred because:** outside the pinned diff; restructuring it is its own change
- **Fix shape:** extract the row-builder, type `opts`
- **Ticket:** none
- **Status:** open
```

**Found** is the line a later reader cannot reconstruct, and the reason the ledger exists at all. **Cost** must be concrete — an entry whose cost you cannot state in one line does not earn a row.

IDs follow the pack's ID grammar, the same rules `ARCH-N` and `GOAL-N` obey: bold `**DEBT-N**`, flat and repo-wide, never renumbered and never reused. Retire by strikethrough with a reason (`~~**DEBT-3**~~ fixed in a1b2c3d`), never by deletion — a struck row is how a reader learns the debt was paid.

## It is not a second issue tracker

| Tracker state | What happens |
|---|---|
| Configured, and the item is big enough to schedule | The row records the *decision*; a ticket records the *work*. Write the row, then name `/publish-issues` for the user to run, and put the returned ID on the **Ticket** line |
| Configured, item too small to schedule | Row only, `Ticket: none` |
| No tracker, or `local` | Row only — the ledger is the tracker for this class of item |

The skill never opens a ticket itself. A row without a ticket is normal, not a gap.

## Reading the ledger

Asked what debt the repo carries, answer from this file — the open rows, with their `Found` dates. Do **not** substitute a fresh read of the code: a smell spotted just now is an observation, and reporting it as known debt erases the distinction between what the team decided and what you noticed. If the file is absent, say the repo keeps no ledger rather than improvising one.

Closing an entry needs the same proof any other completion claim does — [`prove-claim`](prove-claim.md), then strike the ID and cite the commit. Never close one because it is old, because nobody complained, or because the ledger is getting long.

## The gap worth knowing about

Nothing can *invoke* this skill, and nothing ever will — it is user-invoked, and directing an agent to invoke a `disable-model-invocation` target is a dead-end hand-off. So the connection had to be the other legal one: a skill **names it for the user to run**, the same way `root-cause` names `/scan-architecture`.

Two skills now do, at the exact moment a bankable finding is created:

| Skill | Slot | What it routes |
|---|---|---|
| [`polish-diff`](polish-diff.md) | step 7, **banked** | drops whose reason was *scope* — "outside the pinned diff". False-positive drops are excluded: their reason already records them fully |
| [`inspect-change`](inspect-change.md) | step 5, **banked** | **Minor** findings nobody will action on this branch. Critical and Important are excluded — they are fixed before the merge they are holding up |

Both were added on recorded evidence: asked to write the report, 2 of 3 baseline models produced fixed / dropped / referred-out and simply omitted the routing, one of them describing the drops as *"debt left on the table"* in the same breath. It is a template slot rather than a prose reminder for that reason.

Intake used to list a second source — a build's `.skills/<CODE>/deferrals.md` carrier. **No skill ever wrote that file**, so the branch sent the agent looking for something that never existed; it was removed in v1.1.0. Every other `.skills/<CODE>/*` artifact in the set has a producer, which is what made this one findable.

**One gap remains, and it may be by design:** nothing *reads* the ledger. No skill consults `docs/quality/debt.md`. It informs humans — planning, prioritisation, "what have we been carrying?" — not other agents.

And the timing constraint the routing exists to serve: **bank in the same session as the pass that produced the finding.** A drop list stated in a report that nobody banks is gone when the context closes, and running `/record-debt` later from memory does not work — the `Found` line is precisely what a later reader cannot reconstruct.

## See also

- [`polish-diff`](polish-diff.md) — the commonest source of bankable drops
- [`inspect-change`](inspect-change.md) — Minors that will not be actioned this branch
- [`publish-issues`](publish-issues.md) — for the subset someone will actually schedule
