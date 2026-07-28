# 0004 — Commits that already exist are never rewritten

A skill that structures commits is most valuable on a branch whose history is already
messy, which is exactly where rewriting is required. **Decision:** `prepare-change`
holds full authority over commits it creates and none over commits it finds; where
existing commits read poorly it emits an advisory commit map — groups, order, subjects,
bodies, rationale, trailers to preserve — carrying no runnable `reset`, `rebase`, or
force-push command. **Why:** a rewrite discards the `Implements:`/`Guards:` trailers
`release` groups the changelog on, orphans the `commits <base7>..<head7>`
correspondence recorded in `.skills/progress.md`, and on a pushed branch demands the
force-push `finish-branch` forbids an agent from initiating; automated rewriting is
deferred to `ROAD-4` behind an explicit gate rather than assumed here.
