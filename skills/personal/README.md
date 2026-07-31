# Personal OS

An **independent agent skill set** for personal knowledge and multi-project **management**.

It helps a person (and their AI companion) run a closed loop over life and work:

**Capture → clarify → plan → (you) execute → review → replan**

The agent’s default role is **chief of staff / secretary / time coach** — not the person who implements product work. Project actions stay with the user unless they explicitly grant a scoped “do this for me” in that turn.

This package is **self-contained**: skills + templates + setup. It does not require any engineering/coding skill set. Install it only if you want life/vault management support.

---

## What it is for

| In scope | Out of scope |
|---|---|
| Priorities, WIP limits, multi-scale planning | Writing application code |
| Daily / weekly / quarterly reviews | Spec triads, TDD, PR workflows |
| Projects, life areas, learning tracks (as **notes**) | Owning a git monorepo of product source |
| Inbox capture and routing | Auto-registering every folder on disk as a project |
| Write Handoff cards *for the user* to take elsewhere | Silently performing that write-handoff work |

---

## Install

Copy or symlink each skill folder into your agent’s skills directory (paths depend on the harness: Claude Code, Codex, Cursor, Grok, etc.):

```bash
# from the root of this repository
for d in skills/personal/*/; do
  [ -f "$d/SKILL.md" ] || continue
  ln -sfn "$PWD/$d" "${AGENT_SKILLS_DIR:?}/$(basename "$d")"
done
```

Set `AGENT_SKILLS_DIR` to wherever your harness loads skills (for example `~/.claude/skills` or `~/.agents/skills`).

If this monorepo also ships other packages (e.g. Engineer Pack), **Personal Pack is optional**. Default engineering plugins/installers should not force these skills on coding-only users.

In `npx skills add jayden-dang/skills`, this package appears as **Personal Pack** (`personal-pack`). Plugin manifest: `.claude-plugin/personal-os.plugin.json`. Dual-pack registry: `.claude-plugin/marketplace.json`.

---

## First-time setup

1. Choose or create a **markdown vault** (any folder of notes; Obsidian is a common host, not required).
2. In an agent session with that vault as context, run **`setup-personal-os`** (user-invoked).
3. Map *your* existing folders → logical roles (`inbox`, `daily`, `projects`, …). The skill **suggests** a layout; it never force-renames without consent.
4. Set named **roots** for external workspaces only if you use them (code trees, learning folders) — values come from *you*, never assumed.
5. Optionally fill `life-charter`, then start with `orient` or `plan-day`.

Templates for notes live under `templates/personal-os/` at the repository root.

---

## Recommended vault shape (suggestion only)

Users keep any folder names they already use. When greenfield, this shape sorts cleanly:

```text
00-System/          # config, schema, dashboards (optional)
01-Inbox/
02-Daily/
03-Reviews/         # weekly, quarterly
10-Areas/           # ongoing responsibilities
20-Projects/        # outcomes with an end condition
30-Learning/
40-Resources/
50-Archive/
```

All skills resolve paths through the vault **config** (`layout.*`, `roots.*`, `limits.*`) written by `setup-personal-os` — never through hardcoded directory names.

---

## Skills

Shared stance (read once per session): **`ROLE.md`**.  
Eval scenarios for pressure-tests: **`EVAL.md`**.

| Skill | When |
|---|---|
| `using-personal-os` | Start of a Personal OS session (gate + role) |
| `setup-personal-os` | Install or remap a vault (user-invoked) |
| `sync-workspaces` | Advisory compare: disk roots vs project registry |
| `capture` | Park a raw thought quickly |
| `process-inbox` | Clarify and route inbox items |
| `orient` | Status snapshot + one suggested focus |
| `plan-day` | Daily focuses (≤3), energy, not-today |
| `execute-session` | Start/end a focus block — **log + write-handoff only**; user works |
| `open-project` / `plan-project` / `close-project` | Portfolio outcomes |
| `maintain-area` | Ongoing area standards |
| `open-learning-track` / `log-learning` | Learning cadence |
| `review-week` | Weekly closed-loop hinge (P0s **PROPOSED** until confirm) |
| `review-quarter` | Themes and commitments |
| `replan` | Plan invalidated mid-flight |
| `life-charter` | Roles, anti-goals, energy constraints |

---

## Role and permission

**Default: support only.**

- Management writes in the vault (daily notes, reviews, `next_action`, registry) when the skill or user asks.
- External project work (code, designs in product repos, shipping) is **not** performed unless the user clearly grants that act **in the current turn**.
- One grant is not a blank check. Silence after a suggestion is not permission.
- `workspace.path` on a project note is a **pointer for the human**, not a work order for the agent.

---

## Closed loop

```text
life-charter → review-quarter → portfolio intent
       ↓
  review-week (P0 ≤ 3)
       ↓
    plan-day (focus ≤ 3)
       ↓
  user executes (outside this skill set, or with explicit grant)
       ↓
  execute-session log ← user reports evidence
       ↓
  next_action update → review-week
```

---

## Iron laws (summary)

1. **Secretary default** — advise and structure; do not seize execution without permission  
2. **WIP limit** — cap active projects (config; default 5)  
3. **No ghost projects** — active projects need `done_when` + `next_action`  
4. **Evidence** — `done` only when the user confirms the outcome  
5. **Review feeds plan** — weekly P0s drive daily plans  
6. **Registry-first** — disk presence does not auto-create projects  
7. **Control ≠ code** — the vault is not the product monorepo  
8. **Suggest ≠ enact** — confirm material priority and status changes  

---

## What this package does not ship

- A user’s private project list, calendar, or credentials  
- Mandatory folder names for every adopter  
- Engineering/spec/TDD skills (install a separate package if you need those)  

---

## License

Same as the repository root (MIT unless otherwise noted).
