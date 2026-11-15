
## 1.1.0 — an unconfirmed bug goes to `shaping` (2026-10-19), closed workflow W10

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). It already asks for the operator's go-ahead before it touches the tracker, so the body is unchanged.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 32 first messages (`cluster-b-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 52 listed) | after (62 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (2, 22) | `root-cause` for the customer issue, NONE for the external PR (haiku) | `triage` on all | `triage` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "issue #44 came in overnight from a customer, can you look at whether it's real" · "someone opened an external PR adding dark mode, what do we do with it". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "the late fee comes out wrong for refunded invoices, fix it" (`root-cause`), "review the refund branch before I merge it" (`inspect-change`), "the reviewer left six comments on my PR" (`vet-feedback`), "reorder the roadmap so sharing comes before search" (`plan-milestones`), "clean up the duplication in this diff" (`polish-diff`), "what's waiting on me this morning?" (`board`).

Found by the klynt dogfood, W9. `/triage` put #242 ("Soft-deleted users stay
authenticated on existing sessions") into `ready-for-agent` with a brief, and the brief
itself said the fix needs a root-cause investigation first. `/go` and `/board` count a
ticket as Ready only once its spec is approved, so #242 sat in Ready and nothing could
build it. The owner chose to send such bugs to Shaping, where `/shape` runs `root-cause`
and writes the tier-1 mini-spec (option A).

**RED (1.0.0), on the real klynt board, read-only.** The run used the sandbox clone and
`/tmp/klynt-dogfood/bin/gh`: reads go to GitHub and writes are logged. Prompt:
"/triage #242 — re-triage it from scratch as if it were new … Recommend its state; do not
change the tracker."
- The original W9 run (sonnet): `ready-for-agent`.
- Re-runs: haiku `ready-for-agent`, haiku `ready-for-human`, sonnet `ready-for-agent`.

That is 3 of 4 runs recommending `ready-for-agent` for a bug whose cause was still open.

A fixture probe did not reproduce the failure: on harbor-ledger, #28 is a same-day booking
that cannot be invoiced, and triage gave `needs-info` or `ready-for-human` 3/3. That fix
turns on a pricing decision, so the probe cannot show this failure.

**GREEN (1.1.0).** `shaping` is a state triage may choose: "a confirmed bug whose root cause
is not yet established", with the brief marking the cause as open and naming `/shape #N`.
On the same re-triage, all 3 runs (2 haiku, 1 sonnet) recommended `status:shaping` and
said to remove `ready-for-agent`. 0 writes reached GitHub.

## 2026-11-01 — select by state, brief in the issue format (1.1.0 → 1.2.0)

Design: `docs/design/2026-11-01-issue-format.md`. Fixture: a generated repo with an in-repo tracker CLI, the new
`Issue format` seed, and five issues: unlabeled, `enhancement` only, `needs-triage`, `needs-info` with a reply,
and a planned `status:shaping` ticket with no marker.

**RED, 1.1.0** (sonnet 1, haiku 1). 2/2 opened the comment with the AI line and used the old brief shape, on a
file whose seed forbids it. 2/2 left the `enhancement`-only issue out of the buckets; one called it "an inconsistent
issue and I left it alone". 2/2 left assignee, priority and estimate empty on the ticket they made ready.

**Form.** An observable predicate on state, and the brief's sections pointed at the seed.

**GREEN, 1.2.0** (sonnet 1, haiku 1). 2/2 listed all four in-scope issues, skipped the planned ticket with a
reason, and posted a brief with the bug sections plus Acceptance and Out of scope, with no AI line, type, function
or path. 2/2 also set all four fields. Direct state change, haiku 1: stated the edits and waited for a yes.

