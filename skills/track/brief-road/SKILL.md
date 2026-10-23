---
name: brief-road
version: 1.0.0
description: Explains one roadmap item in plain words — what it delivers, what it leaves out, and whether it is ready to frame, blocked, or already built. Run it with /brief-road ROAD-N.
disable-model-invocation: true
---

# Brief Road

Turn one `ROAD-N` entry into something a person can read in two minutes before
they frame it: what it delivers, where it stops, and whether it can start today.

## The Iron Law

```
"READY" OR "BLOCKED" IS SAID ONLY AFTER EVERY ITEM BEFORE IT WAS LOOKED UP IN THE CATALOG.
```

Four baseline briefs listed the build order and not one looked up its status. One
wrote "I have not checked that status" about ROAD-44 — the one unbuilt item ahead of
ROAD-81, whose eight other predecessors were all Implemented. The order was on the
page; the answer to "can I start?" was not.

## 1. Collect: these passes, from the repo root

No `docs/roadmap/INDEX.md`, or no line starting `- **ROAD-N**` (or `- ~~**ROAD-N**~~`)
in it → say which, in one line, and stop. A struck-through definition → the item is
closed: say whether its reason calls it delivered or dropped, quote the reason, and
stop. ROAD-72 is struck because it was delivered; a brief that called it "removed"
told the reader the opposite of its own quote.

1. **Entry.** `grep -n '^- \(~~\)\?\*\*ROAD-N\*\*' docs/roadmap/INDEX.md`. Its
   milestone is the nearest `## MILE-` heading above that line; from that block read
   the `**Outcome:**`, `**Goals:**`, `**Depends-on:**` and `**Blockers:**` lines and
   the Members list in order.
2. **Predecessors.** The entry line carries `— After: …` → the IDs it names
   (`none` → no predecessors; a `MILE-N` → every member of that milestone).
   Otherwise → every member listed above it in that block. Add each ROAD the entry
   says it *Needs*.
3. **Status.** For the item and each predecessor:
   `grep -rnE '\| *ROAD-X *\|' docs/specs/INDEX.md docs/specs/catalog/`. The row
   gives the feature CODE and Status. No row → not started.
4. **Decisions.** `ls -d .skills/<CODE> .skills/_pending-road<N>` (CODE from pass 3),
   every `.skills/…` path the entry cites, every folder
   `grep -rlE 'ROAD-N\b' .skills/` returns, and every `ADR-N` the entry cites under
   `docs/adr/`. Read the `decisions.md` / `close.md` found there for the locks about
   this item and what they left open. ROAD-170's locks sit in `.skills/CCOL/`, the
   frame-change that inserted it, which its entry never cites.
5. **Code.** Open each Surfaces path the entry names, and each consumer it says must
   be audited. Note what exists at `file:line`. Two Surfaces need a search first,
   and only an empty search makes either absent:
   - a path that does not resolve from the root → `find . -path '*<path>*' -not -path '*/node_modules/*' -not -path '*/dist/*' -not -path '*/target/*'`;
   - a Surface named in words ("the course browser's main pane") → its nouns as a
     name pattern: `find . -iname '*course*browser*' -not -path '*/node_modules/*' -not -path '*/dist/*' -not -path '*/target/*'`,
     then open the files that match.

   A Haiku brief called `apps/library/` absent — it is `frontend/src/apps/library/` —
   and never opened the course browser.

*Done when: every pass has run and you hold its output.*

## 2. Verdict

| Own catalog row | Predecessors | Verdict |
|---|---|---|
| Implemented or Shipped | — | **Built** as `<CODE>` |
| any other Status | — | **In flight** as `<CODE>` (`<Status>`) |
| none | all Implemented or Shipped | **Ready** to frame |
| none | any other | **Blocked by** each one that is not |

## 3. The brief: these slots, in this order

1. **In short** — at most 3 sentences: who can do what once it ships, and what they
   cannot do today. Lead with the person and the action, never with the milestone
   number, the item's position, or a term slot 4 has to define.
2. **Scope now** — at most 5 one-line bullets: the things the current version
   delivers, never their acceptance criteria. Its history — inserted, restated,
   narrowed, split — gets one more line with dates.
3. **Not this item** — at most 5 bullets: a piece left out, and the item or milestone
   that owns it.
4. **Terms** — at most 6: the terms from slots 1–3 a newcomer would least know, in
   10 words or fewer; use `CONTEXT.md`'s definition when it has one.
5. **Ready?** — the verdict, then one row per predecessor: `ROAD-X · CODE or — ·
   Status or not started`. Quote the milestone's Blockers line when it is not `None`.
6. **Decided / open** — *Decided:* at most 5 locks or ADRs that shape this item, each
   with its number and file, then the file that holds the rest. No decisions file →
   "nothing recorded". *Open:* at most 5 questions framing must settle, highest blast
   first — choices the entry defers ("set by the spec", "to decide"), forks it names
   without picking, risks it says are unproven.
7. **Code today** — at most 5 bullets, per pass-5 path: what exists at `file:line`,
   or "new".
8. **One question** — one question whose answer needs slots 2–6, inviting the reader
   to answer it.

*Done when: the message holds all eight slots, in order, each within its limit, and
ends on the question.* Without the limits, briefs ran to 50–55 lines against a
40-line target and no run met it.

## Red Flags

- A verdict with no status row behind each predecessor
- Slot 1 opening with "item 10 of 11", a milestone ID, or a term nobody defined
- Restating the entry clause by clause — one baseline brief ran to ~900 words and
  still never said whether the item could start; a draft of this skill copied
  ROAD-81's five groups of acceptance criteria into Scope now and ran to 65 lines
- A `file:line` you did not open this session — a Haiku brief copied
  `self-check.tsx:37` from a decision's text; line 37 is `useTranslation()`
