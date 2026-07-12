# Phase 5 — Ship and maintain

**Skills:** [`finish-branch`](../skills/finish-branch.md) · [`release`](../skills/release.md) · [`sync-spec`](../skills/sync-spec.md) · [`amend`](../skills/amend.md) · [`triage`](../skills/triage.md) · [`improve-architecture`](../skills/improve-architecture.md) · [`handoff`](../skills/handoff.md)

## `finish-branch` — the integration decision

**Gate first.** `verify` runs every verify command from `docs/agents/project.md` fresh, **and** confirms the trace check is clean — a branch must not merge with untraced requirements, the same gate `release` enforces. If the branch has user-facing behavior that has not been driven through the running system, `acceptance-check` runs *before* Merge or PR is even offered.

**Any failure means stop.** Show the failures. Do not present the menu.

**Then exactly four options, verbatim, with no added commentary:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

Three details make this safe rather than merely tidy:

- **Merge re-verifies on the merged result, before removing any worktree.** A failed merge with the worktree already gone loses the work.
- **PR keeps the worktree.** The user needs it to iterate on review feedback.
- **Discard requires the user to literally type `discard`.** Anything else — including "yes", "confirm", "do it" — is not confirmation.

Worktree cleanup happens only for merge and discard, and only for a worktree whose path sits under `.worktrees/` or `worktrees/`. That provenance means this skill set created it. Anything else, including harness-owned workspaces, is not yours to remove.

## `release` — nine gates, no partial releases

User-invoked (`/release`). Distinct from `finish-branch`, which only integrates a branch.

> **The stop rule:** any step that fails means STOP. There are no partial releases: no tag without a passing build, no notes for artifacts that do not exist, no "we'll fix it after tagging."

| Gate | What it does |
|---|---|
| **a. Verify** | every verify command, fresh, plus the trace check **clean**. An implemented requirement with no covering test is an untraced requirement, and untraced requirements block a release |
| **b. Changelog** | group `git log <last-tag>..HEAD` by requirement-ID trailers; look up each ID's requirement text so the entry reads as *shipped behavior* |
| **c. Version bump** | reason in semver from the changelog. **The user approves the number** — never proceed on silence |
| **d. Update files** | version files + changelog, committed together |
| **e. Build** | the ordered release steps from `docs/agents/project.md`, **exactly**. No improvised flags |
| **f. Smoke-check** | exercise the built **artifact**, not the source tree |
| **g. Tag and push** | only after explicit user approval. **Never push a tag on your own initiative** |
| **h. Release notes** | the tracker's format, keeping the requirement-grouped structure. Left as a **draft** |
| **i. Flip status** | `sync-spec` moves shipped requirements to `Status: Shipped` |

### The payoff of the trace spine

Gate **b** is where the whole system cashes out. Commits carry `Implements: SHELL-1.2` and `Guards: SHELL-1.3` trailers. `release` groups by those IDs, looks up each requirement's text in `docs/specs/`, and writes:

```markdown
### Shipped behavior
- Module selection persists across launches — SHELL-1.2

### Protected behavior
- Unsaved editor state survives a module switch — SHELL-1.3
```

Not commit prose. **Requirement-level release notes, derived.** `Guards:` trailers become their own grouping. Untrailered commits go under **Misc**.

Nobody wrote those lines, and nobody could have, without the ID being the same string in the requirement, the test, and the commit.

## `sync-spec` — the anti-rot skill

> Specs that are not resynced after change become fiction, and fiction is worse than no spec.

Run it whenever a spec'd feature changes outside its plan: requirements changed mid-implementation, the implementation deviated, the feature just shipped, or the trace check comes back dirty.

**Iron rules.** Never renumber requirement IDs — everything downstream cites them. Never delete a requirement; retire it as `~~**CODE-N.M**~~ <reason>`, so struck-through IDs stop counting as defined while the history stays legible.

**Steps.** Capture a trace-check baseline. Compare requirements against tasks (a live requirement no task cites gets a covering task). Compare requirements against the design's `Satisfies:` lines — and *flag* gaps to the user rather than inventing design content silently. List orphans: task footers and test annotations citing struck-through or nonexistent IDs, each with a suggested disposition, because **orphans are decisions, not cleanup.**

**Status transitions, with evidence only:**

| Transition | Required evidence |
|---|---|
| Draft → Approved | the user explicitly approved the spec — never inferred |
| Approved → Implemented | every task box checked **and** the trace check shows every live requirement covered by a test |
| Implemented → Shipped | the feature went out in a release |

If evidence is partial, say exactly what is missing instead of transitioning.

Finally, re-run the trace check and print the before and after reports side by side, and update the feature's `docs/specs/INDEX.md` entry. Feature overlap is answered by searching `docs/specs/` directly, so the refreshed spec and its `INDEX.md` registration are all the next feature's `brainstorm` reads — there is nothing to harvest or regenerate.

## `amend` — the maintenance fast lane

A small in-scope change to an already-shipped, spec'd feature. **A fast lane, not a gate bypass**: every path still exits through `tdd`.

Ground the change in the existing spec, then classify **out loud**:

- **Tier 0** — no behavior change (a recolor, an icon, a label, a copy edit); every existing acceptance criterion still reads true unchanged → `tdd`.
- **Tier 1** — changes or extends existing spec'd behavior, ≤ ~half a day → mini-spec via `write-requirements` (amend the requirement, add a `SHALL CONTINUE TO` guard) → `tdd`.
- **Genuinely new scope** → stop amending. Escalate to `brainstorm`.

The honest test for escalation: **does the existing spec's intent already cover this behavior?** If you are inventing what it should do, it is new scope.

If the feature has no spec at all, `amend` is the wrong skill — a brand-new capability is `brainstorm`, a break is `debug`.

## `/triage` — the incoming queue

Issues (and, when configured, external PRs — *a PR is an issue with attached code*) move through a two-axis state machine. Every triaged issue carries **exactly one label from each axis**:

- **Category:** `bug` or `enhancement`
- **State:** `needs-triage` → one of `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`

Every comment posted to the tracker opens with the exact line `> *This was generated by AI during triage.*`

Two checks run before any recommendation. **Redundancy:** search the codebase for an existing implementation, by *domain concept*, not the reporter's wording. **Prior rejection:** read `.out-of-scope/*.md` and match by *idea*, not keyword.

Then **verify the claim** — reproduce the bug from the reporter's steps, or check out a PR's diff and run its tests. First-hand evidence, not the reporter's word.

Two rules that are easy to get backwards:

- **Issues born agent-ready are out of scope.** Anything published from a plan (recognizable by a `Requirements covered:` section) already has a real spec. Running it through triage adds a second, weaker one.
- **An "already implemented" close does not write to `.out-of-scope/`.** That knowledge base records *rejections*; logging built features there poisons future dedup checks.

## `/improve-architecture` — the periodic scan

Codebase-wide, not a single diff. The goal is testability and navigability — modules deep enough that their interface is the test surface.

Its vocabulary is strict throughout — **module, interface, implementation, seam, adapter** — and it never drifts into "component", "service", "layer", or "boundary". Precision in the nouns is what keeps findings comparable run over run.

Four kinds of friction: shallow modules, poor locality, missing or weak seams (including a seam with exactly one *hypothetical* adapter), and code only testable by reaching past its interface. Anything suspect gets the **deletion test**: if this module vanished, how much would its callers need to know to rebuild the behavior? "Almost everything" means it was shallow, and deleting it would *concentrate* complexity rather than lose it. That concentration point is the candidate.

The output is a self-contained HTML report written to the **OS temp directory**, not the repo. One card per candidate, each with a before/after structure sketch that carries the argument — *if it needs a paragraph to explain, redraw it* — and a confidence badge of exactly `Strong`, `Worth exploring`, or `Speculative`.

The report names **directions, not designs**. Interface shape belongs to the `grilling` step, with the user in the loop.

And then: tier 0 proceeds under `tdd`/`verify`; anything tier 1 or above goes to `brainstorm`. **Architecture work earns no exemption from the spec gate.**

## `/handoff` — when the session ends

Compact the conversation into a document a fresh agent can resume from. Written to the **OS temp directory**, never into the workspace — a handoff is session ephemera, not a project artifact.

Five sections: **Goal**, **Current state** (exact branch and worktree, whether the tree is dirty), **Tried and rejected** (every approach attempted or dropped, each with *why* — usually the most valuable section, because it saves the successor from re-walking dead ends), **Next actions** (concrete, ordered, starting with the very next command), and **Suggested skills** (which skill to invoke, at which step).

Two rules: **reference, never duplicate** — cite specs, plans, ADRs, issues, and commits by path or hash, because copying content bloats the handoff and *forks the truth*. And **redact secrets**, because the document may become another agent's prompt.

The completion criterion is a skeptic's read: could a fresh agent, given only this file plus the artifacts it references, resume the work without asking anything already answered?

## See also

- [Traceability](../concepts/traceability.md) — why `release` can derive its own changelog
- [Ceremony tiers](../methodology/ceremony-tiers.md) — where `amend` routes each change
- [`sync-spec`](../skills/sync-spec.md) — the skill that keeps specs from becoming fiction
