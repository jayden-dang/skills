# `work-the-problem`

> Works a design or framing problem to **closure**: multi-round breakdown, foundation→feature teaching, **disk artifacts**, then a carry-back brief for the main window — without enacting the decision. Time-boxed stance stays [`interpret-session`](interpret-session.md); pure learning stays [`deepen-codebase`](deepen-codebase.md).

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/work-the-problem`) — session mode, not auto-fired |
| **Reads** | pasted main-window content; repo when leaves touch code; research notes |
| **Writes** | session-local only: `.skills/work-the-problem/<slug>/*` (and research notes via `research`) |
| **Calls** | [`research`](research.md) when external fact is material; optionally `load-subgraph`; **names** `/run-spike` / `/deepen-codebase` (user runs) |
| **Called by** | — (user opens it beside the main session) |

## When it fires

You are shaping or deciding in another window and need more than an overview: the problem must be **worked** (tree of leaves, multi-round) and you want to **keep the mental model** (foundation → feature), not only a paste-back pick. Open `/work-the-problem`, lock the problem, work leaves until closed or explicitly deferred, then ask for the carry-back brief into `frame-change`.

**Not** the gấp path — that stays [`/interpret-session`](interpret-session.md).  
**Not** pure learning with no product close — that stays [`/deepen-codebase`](deepen-codebase.md).

## Companion trio (+ this skill)

| Session | Role |
|---|---|
| Main work | `frame-change` / `clarify-decisions` / … |
| `/interpret-session` | Fast committed stance + English (or main-window) reply |
| `/deepen-codebase` | Slow foundation; no product pick |
| **`/work-the-problem`** | Deep solve + in-service teaching + carry-back |

## Why disk artifacts

Long breakdown↔solve loops lose state in chat. The skill initializes and updates:

```text
.skills/work-the-problem/<slug>/
  session.md
  problem-tree.md
  foundation-cards.md
  leaf-log.md
  carry-back.md
```

Resume always reloads these files first.

## Act quality

- Read code before opining (`file:line`)
- `research` for external owning-source facts
- **Name** `/run-spike` when runtime feel matters — user runs it
- Suggestions for repo improvements stay non-binding in carry-back

## See also

- [`interpret-session`](interpret-session.md) — thin companion  
- [`deepen-codebase`](deepen-codebase.md) — pure learning sibling  
- [`frame-change`](frame-change.md) — usual main window  
- [`research`](research.md) — evidence detour  
- Skill source: `skills/discovery/work-the-problem/`
