# Architecture domain: Workflows

Status: Approved
Date: 2026-07-22
Part of: [`INDEX.md`](./INDEX.md) (architecture SSOT)

End-to-end process chains and known limits of the model.

## Main flow: idea → ship (tier 2)

```
using-skills (session gate)
→ brainstorm            grilling + domain-modeling; docs/specs/ overlap search;
                        research/prototype detours; tier decision  [HARD GATE: no code]
→ write-requirements    EARS + IDs; approval gate on the file
→ write-design          Satisfies: per section; seams agreed; approval gate
→ write-plan            tasks with _Requirements:_ footers; trace coverage check
→ worktrees             isolated workspace, clean baseline
→ execute-plan          per task: brief → implementer (tdd) → review bundle →
                        two-verdict review → fixes → ledger
                        [debug on failures; verify before any claim]
→ code-review           whole-branch, two-axis (Standards + Spec-by-ID) + overlap search
→ acceptance-check      drive the running system through the spec's user-facing
                        behaviors (API + UI); promote to tagged tests (+ dogfood)
→ finish-branch         merge / PR / keep / discard / block
→ release               when shipping: verify + trace gate, changelog, tag, build
→ sync-spec             mark requirements Implemented/Shipped
```

## Bugfix flow (tier 1)

```
debug (red-capable command → root cause → fix via tdd)
→ mini-spec: fix REQ + SHALL-CONTINUE-TO guard in the owning requirements.md
→ tagged regression test → verify → code-review (spec axis) → finish-branch
```

## Maintenance loop

```
amend → tier 0: tdd / tier 1: mini-spec → tdd / new scope: escalate to brainstorm
improve-architecture (periodic) → picked candidate → brainstorm → ...
triage (incoming issues) → ready-for-agent brief → execute or implement directly
```

## Boundaries

Known limits of the model, stated plainly so adopters can judge them:

- **Feature overlap is best-effort search, not a registry.** `brainstorm` and
  `code-review` find neighbors by searching `docs/specs/`; two runs may surface them
  in a different order or miss a subtly shared path. Overlap detection is advisory
  and never blocks a gate, so this is an acceptable bound.
- **There is no mandatory headless gate.** CI and git hooks run without an agent and
  cannot invoke a skill, so the trace discipline depends on the agent running
  `verify`/`release`, not on a build that fails on its own. Teams that want a hard
  gate opt into a documented CI job, outside the default path.
- **Skill-authoring QA is agent-run.** Frontmatter shape, naming, and trigger
  should-fire/should-not-fire checks live in the `writing-skills` deployment
  checklist as steps the agent performs, not a separate harness.
