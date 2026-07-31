# Packages

This repository can host **more than one skill package**. Each package is installable on its own. Adopters take only what they need.

| Package | `npx skills` pack name | Location | Typical surface | Default install? |
|---|---|---|---|---|
| **Engineer Pack** | `engineer-pack` | `skills/{meta,discovery,spec,execution,review,acceptance,craft,ship,track,project,setup}/` | Software repositories | **Yes** (default plugin) |
| **Personal Pack** | `personal-pack` | `skills/personal/` | Personal / life markdown vaults | **No** (opt-in) |

They share a monorepo for maintenance convenience. They do **not** depend on each other at runtime.

`npx skills add jayden-dang/skills` lists both packs (from `.claude-plugin/marketplace.json`). Skills not listed in either pack would fall into an ungrouped **Other** bucket — keep the manifests complete.

---

## Engineer Pack

Spec-driven agentic development: ideation → requirements → design → plan → implementation → review → release, with requirements traceability and optional multi-milestone roadmap layer.

- Install: default `npx skills` / Claude plugin entry (`.claude-plugin/plugin.json`, name `engineer-pack`)
- Marketplace registry: `.claude-plugin/marketplace.json` (both packs)
- Config per code repo: `configure-repo`
- Constitution for engineering sessions: root `AGENTS.md` (Iron Laws for code work)

Details: root [README.md](../README.md), [docs/guide/START-HERE.md](guide/START-HERE.md).

---

## Personal Pack

Independent management skill set: capture, multi-scale planning, portfolio and life areas, learning cadence, weekly/quarterly review. Agent role = secretary / coach.

- Install: opt-in only — see [skills/personal/README.md](../skills/personal/README.md)
- Config per vault: `setup-personal-os` (maps *that user’s* folders; never force-renames)
- Templates: `templates/personal-os/`
- Plugin manifest: `.claude-plugin/personal-os.plugin.json` (name `personal-pack`)

Personal Pack does **not** require Engineer Pack. Engineer Pack installs should **not** inject Personal Pack skills unless the user chooses them.

---

## Install isolation

### Engineering only

Symlink or install only engineering categories (or use the default plugin list). Do not use a blind `skills/*/*` loop if you want to exclude Personal OS.

### Personal OS only

```bash
for d in skills/personal/*/; do
  [ -f "$d/SKILL.md" ] || continue
  ln -sfn "$PWD/$d" "${AGENT_SKILLS_DIR}/$(basename "$d")"
done
```

### Both

Install both packages into the agent skills directory. Keep **session context** separate when possible:

- Software work → engineering skills + code repo  
- Life/portfolio management → Personal OS skills + vault  

Skill **folder basenames** must remain unique across packages (they share one flat skills directory on most harnesses).

---

## Authoring boundaries

| Concern | Engineering package | Personal OS package |
|---|---|---|
| Primary user goal | Ship correct software | Manage attention and commitments |
| Default agent stance | Builder under process gates | Secretary; no project execution without grant |
| Config | Repo `docs/agents/*` | Vault Personal OS config (`layout`, `roots`, `limits`) |
| Private user data in repo | Never | Never |

Do not embed adopter-specific paths, vault names, or private registries into either package.
'''

