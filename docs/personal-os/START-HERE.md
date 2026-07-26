# Personal OS — Start here

Personal OS is an **independent** skill package for managing life and multi-project attention with an AI companion.

You do not need any other skill package from this repository to use it.

## 1. Install the skills

See [skills/personal/README.md](../../skills/personal/README.md#install).

Confirm your agent can list skills such as `using-personal-os`, `plan-day`, and `review-week`.

## 2. Point the agent at your vault

Open a session whose working context is your notes vault (any markdown tree).  
Obsidian, plain folders, or another PKM host all work.

## 3. Run setup once

Invoke **`setup-personal-os`**.

- Detect your folders  
- Write a config that maps logical roles → *your* paths  
- Optionally adopt the suggested tree  
- Never bulk-rename without your consent  

## 4. Daily loop

| When | Skill |
|---|---|
| Session start | `using-personal-os` (gate) |
| “Where am I?” | `orient` |
| Morning | `plan-day` |
| Start / end focus | `execute-session` (log + handoff for *you*) |
| Raw thoughts | `capture` → later `process-inbox` |
| End of week | `review-week` |
| End of quarter | `review-quarter` |

## 5. Role reminder

The companion **manages and coaches**. You **do** the work (or explicitly ask for a scoped act).

Full product description, skill index, and iron laws: [skills/personal/README.md](../../skills/personal/README.md).

Package relationship to engineering skills (optional monorepo mates only): [docs/packages.md](../packages.md).
'''

