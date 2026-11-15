# no-comments

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). Its description fires only on an explicit ask for a comment-deletion pass, so the body is unchanged.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 22 first messages (`cluster-e-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 73 listed) | after (80 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (9) | not run: flagged skills are not listed, as the three earlier clusters showed | `no-comments` on all | `no-comments` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "strip the comments from this diff, I want none left". Near misses that stayed with their owners on both models: "clean up this diff before we merge" and "remove the dead code" (`polish-diff`), "not sure where to start with this one" (none), "build every ready ticket on the board and open PRs" (`deliver-issues`), "the reviewer left six comments on my PR" (`vet-feedback`), "merge this branch, it's done" (`land-branch`), "write the requirements for SMS reminders" (`specify-behavior`), the zero-amount 500 (`root-cause`). The same two runs re-checked all 86 messages of the three earlier clusters against the final 80-skill listing: every one still routed to its owner.

## v1.0.0 — OVERRIDE ship (2026-09-08)

**Prior judgment.** Overlap research and polish-diff already own a softer
default-zero comment pass. Pack criterion C3 said do not copy pstack
`no-comments` + Comment Sicko.

**Override.** User explicitly required the extreme skill anyway
("override, vẫn apply hết kể cả no-comments").

**What shipped.** User-invoked `/no-comments`: narrow keep-list, Comment Sicko
brief for a read-only subagent, parent applies deletions and encoding offers.
No RED failure transcript — OVERRIDE noted in SKILL.md HARD-GATE.

**Eval.** Contract anchors only (see `eval.json`).
