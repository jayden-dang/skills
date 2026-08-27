---
name: tour-system
version: 1.1.0
description: Produces a path-verified learning tour and local ledger. Run with /tour-system.
disable-model-invocation: true
---

# Tour System

Learn a **codebase or capability** by walking an ordered, evidence-backed tour —
not a prose lecture and not a quiz packet.

**Leading words:** atlas · stop · checkpoint · reachability · ledger ·
`ResolvedRange`.

## The Iron Law

```
NO DEMONSTRATED WITHOUT SOURCE/TEST/RUNTIME EVIDENCE
NO QUIZ PACKET AS THE PRIMARY OUTCOME
NO PERSISTED FEATURE GRAPH / GRAPHIFY REQUIREMENT
NO USER-INVOKED SKILL AUTO-INVOKE
```

`load-subgraph` is **advisory** context. It never alone proves a claim.

## What you produce

| Always | On request (change-impact) |
|---|---|
| Ordered **stops** + `.skills/study/<slug>/` **ledger** | `--export` Markdown (default) or `--export html` |

Hard-stop → diagnostic only; never partial success export or fake `demonstrated`.

## Modes

Ask which mode when unclear. If the user named a **surface** (CLI, path, CODE)
without a mode: short atlas (INDEX or tree), then one `journey` or `tour` on
that surface.

| Mode | Question |
|---|---|
| `atlas` | What capabilities exist? (INDEX + active OBS) |
| `tour` | How does this CODE/path/term hang together? |
| `journey` | Trace one user/CLI action end-to-end |
| `change-impact` | What does this **ResolvedRange** mean for the system? |

**Load when needed:**

| Topic | File |
|---|---|
| Range resolve / hard-stops | `references/resolved-range.md` |
| Ledger states / production | `references/ledger.md` |
| Blocking gap capsule | `references/handoff.md` |
| Portable export | `references/export.md` |

## Procedure

1. **Preflight.** Consuming-repo root.
   - Prefer live `docs/specs/INDEX.md`; if missing, name `/configure-repo` and
     continue atlas only from visible tree signals (packages, cmd/entrypoints) —
     do not invent CODEs from folder names.
   - Confirm `.skills/` is gitignored (`git check-ignore -v .skills/` or
     equivalent). If not: warn once, name `/configure-repo`; still write under
     `.skills/study/` — do **not** patch the consumer `.gitignore` unless the
     user asked or `/configure-repo` is running.
   - For `change-impact`, WHEN resolving range, load
     `references/resolved-range.md` and follow it exactly.
2. **Build the tour.**
   - `atlas`: INDEX rows + pending OBS; orientation stops only. Tree-only atlas:
     entrypoints and package surfaces — never invented Feature CODEs.
   - `tour`: REQUIRED SUB-SKILL: use `load-subgraph` (neighbors/cluster/blast as
     fits); order stops by path evidence.
   - `journey`: pick entry → persistence/output; cite real paths each hop.
   - `change-impact`: inventory from `ResolvedRange`; map paths → CODE/OBS
     (both rename sides); order stops; old→new behavior with cites.
3. **Walk stops.** Open cited paths. Mark `visited` / `in_progress`. **No**
   graded production per file stop.
4. **Close a semantic checkpoint** (meaningful unit, not file count) or end a
   journey: WHEN closing, load `references/ledger.md` and require **one** graded
   production (own-words purpose + one reachability claim + optional blast).
   Verify with source/test/runtime. Record `demonstrated` / `contradicted` /
   `unverified` correctly.
5. **Gaps.** Non-blocking `open_gap` → ledger + continue. Blocking → stop;
   WHEN emitting handoff, load `references/handoff.md` (name-only + one route +
   capsule). Never inline remediation. Name `/teach-pack`, `/deepen-codebase`,
   or `/study-change` for the user when the capsule says so — do **not** run
   those skills yourself.
6. **Export (change-impact only).** Only if requested; WHEN exporting, load
   `references/export.md`.
7. **Neighbors.** Name `/study-change` or `/teach-pack` when the ask is their
   job (HTML quiz packet / concept drill with oracle). Do not absorb their
   contracts — routing table in `references/handoff.md`.

## Rationalization

| Thought | Reality |
|---|---|
| "Chat explanation is faster than a tour" | Tour forces path-backed reachability; chat is low scent |
| "load-subgraph proved the claim" | Advisory only — need source/test/runtime |
| "Quiz after each file keeps them honest" | One production per checkpoint/journey close |
| "Write GRAPH.md / feature-graph" | Ask-time subgraph only; catalog is INDEX |
| "I'll run teach-pack for them" | Name `/teach-pack`; never auto-invoke |
| "They said got it — mark demonstrated" | No evidence → not demonstrated |
| "Missing evidence means contradicted" | Use `unverified` / `open_gap` |
| "Pure untracked — summarize the branch" | Hard-stop per ResolvedRange |
| "Alias /study-change to this skill" | Forbidden — no user→user invoke alias |
| "I'll add `.skills/` to gitignore while I'm here" | Warn + name `/configure-repo`; this skill does not own consumer ignore |
| "Folders look like features — mint CODE AGENT" | Tree atlas uses path labels only; CODEs come from INDEX |
| "User said run it — skip mode and dump prose" | Named surface → atlas then one journey/tour; else ask |

## Red Flags

- Prose dump or quiz HTML as the primary deliverable
- `demonstrated` without source/test/runtime cites
- Per-file-stop mandatory production
- Treating load-subgraph as sole proof
- Persisted graph / Graphify as required
- Running `/deepen-codebase`, `/teach-pack`, or `/study-change` instead of naming them
- Inline explain-then-reprobe after `contradicted`
- Partial success export or success ledger after hard-stop
- Inventing Feature CODEs
- Patching consumer `.gitignore` from this skill without user ask / `/configure-repo`

## Done when

Mode completed with ordered stops; ledger states honest; every
`demonstrated`/`contradicted` has evidence; blocking gaps emitted a single-route
capsule; export (if any) respects privacy; hard-stops left no success artifact.
