# Architecture domain: Workflows

Status: Approved
Date: 2026-07-22
Part of: [`INDEX.md`](./INDEX.md) (architecture SSOT)

End-to-end process chains and known limits of the model.

## Main flow: idea → ship (tier 2)

```
gate-session (session gate)
→ frame-change            clarify-decisions + define-domain; docs/specs/ overlap search;
                        research/run-spike detours; tier decision  [HARD GATE: no code]
→ specify-behavior    EARS + IDs; approval gate on the file
→ design-solution          Satisfies: per section; seams agreed; approval gate
→ plan-tasks            tasks with _Requirements:_ footers; audit-trace coverage check
→ isolate-workspace             isolated workspace, clean baseline
→ execute family        pick one from Execution-mode + route:
                        build-in-waves   (continuous + subagent waves)
                        build-by-story  (story-unit + human unit barriers)
                        build-inline (controller TDD, no implementer subagents)
                        [debug on failures; prove-claim before any claim]
→ inspect-change           whole-branch, two-axis (Standards + Spec-by-ID) + overlap search
→ validate-feature      drive the running system through the spec's user-facing
                        behaviors (API + UI); promote to tagged tests (+ review-product-flow)
→ land-branch         merge / PR / keep / discard / block
→ cut-release               when shipping: prove-claim + audit-trace gate, changelog, tag, build
→ realign-spec             mark requirements Implemented/Shipped
```

## Bugfix flow (tier 1)

```
root-cause (red-capable command → root cause → fix via test-first)
→ mini-spec: fix REQ + SHALL-CONTINUE-TO guard in the owning requirements.md
→ tagged regression test → prove-claim → inspect-change (spec axis) → land-branch
```

## Maintenance loop

```
amend-feature → tier 0: test-first / tier 1: mini-spec → test-first / new scope: escalate to frame-change
scan-architecture (periodic) → picked candidate → frame-change → ...
triage (incoming issues) → ready-for-agent brief → execute or implement directly
```

## Boundaries

Known limits of the model, stated plainly so adopters can judge them:

- **Feature overlap is best-effort search, not a registry.** `frame-change` and
  `inspect-change` find neighbors by searching `docs/specs/`; two runs may surface them
  in a different order or miss a subtly shared path. Overlap detection is advisory
  and never blocks a gate, so this is an acceptable bound.
- **There is no mandatory headless gate.** CI and git hooks run without an agent and
  cannot invoke a skill, so the audit-trace discipline depends on the agent running
  `prove-claim`/`cut-release`, not on a build that fails on its own. Teams that want a hard
  gate opt into a documented CI job, outside the default path.
- **Skill-authoring QA is agent-run.** Frontmatter shape, naming, and trigger
  should-fire/should-not-fire checks live in the `author-skills` deployment
  checklist as steps the agent performs, not a separate harness.
