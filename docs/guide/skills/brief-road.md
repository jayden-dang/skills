# `brief-road`

> One roadmap item, read for you before you frame it: what it delivers, where it stops, and whether it can start today.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/brief-road ROAD-N` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/roadmap/INDEX.md` (the entry and its milestone block), `docs/specs/INDEX.md` and `docs/specs/catalog/*.md` (the "Roadmap item" cell), `.skills/<CODE>/` and `.skills/_pending-road<N>/`, cited `.skills/…` paths and ADRs, `CONTEXT.md`, the Surfaces paths the entry names |
| **Writes** | nothing — the brief is a chat message |
| **Calls** | nothing |
| **Called by** | nobody — it is user-invoked |

## Why it exists

A klynt roadmap entry runs to a median of 157 words and up to 755, with its history, its exclusions and its locks folded into one line. Asked to explain one before framing it, four baseline answers on Sonnet — with and without `understand` — all listed the build order and none looked up its status. Each listed the order ahead of ROAD-81 — eight items Implemented, ROAD-44 not built — without saying which was which, and one answer ran to about 900 words without saying whether the item could start. None split what was decided from what was open, and none defined a term.

## What you get

A fixed eight-slot brief, each slot capped (about 45 lines in practice):

1. **In short** — who can do what once it ships, in plain words
2. **Scope now** — at most five deliverables, plus one dated history line
3. **Not this item** — each excluded piece and where it lives
4. **Terms** — the words a newcomer would not know
5. **Ready?** — **Ready**, **Blocked by** …, **In flight**, or **Built**, with one catalog row per predecessor
6. **Decided / open** — locks and ADRs by number and file; what framing must settle
7. **Code today** — what exists at `file:line`, or "new"
8. **One question** — one question to answer before you frame it

The verdict comes from fixed `grep` passes over the roadmap and catalog, not from reading the member list: an item with an `After:` waits on what that line names, and an item without one waits on every member above it.

## What it is not

Choosing which item to build next is [`/board`](board.md) or [`/chart-progress`](chart-progress.md). How an already-built feature works is [`understand`](understand.md). Editing the roadmap is [`plan-milestones`](plan-milestones.md). Framing it is [`frame-change`](frame-change.md), which the brief leaves to you.
