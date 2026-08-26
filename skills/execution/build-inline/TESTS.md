# `build-inline` — test evidence

## RED — shared runtime binding contract (baseline, 2026-08-26)

`execute-common` defines runtime binding and canonical constraint references, but
the inline route loaded only session preflight, ledger, and todos. Its setup
still captured and copied Global Constraints directly, so inline execution could
miss the runtime snapshot and price/context safety policy.

## GREEN — shared runtime binding contract (structural, 2026-08-26)

The inline route now loads runtime binding before the ledger, records the runtime
snapshot, and carries the canonical constraint path/hash into its task capsule.
Live provider telemetry was unavailable; this is structural GREEN pending a
live harness run.

**Protocol:** `author-skills` / `pressure-testing.md`  
**Scenario files:** removed in `2338b34` ("remove test scenarios") — the runnable prompts now live in `eval.json` beside this file.  

## RED (2026-07-30, grok-4.5) — before skill existed

| Scenario | Observed | Failure for new skill |
|---|---|---|
| S-INLINE-1 tools exist, user chose inline | **A** via build-in-waves Inline Fallback | Gate text works when loaded; **no first-class trigger** |
| Routing "no subagents, implement yourself" | **build-in-waves** (fallback buried) | Distinct-trigger miss — description cannot fire |
| Plan gap + demo pressure | **A** stop and ask | Keep in iron law |
| One-line + skip TDD pressure | **A** still test-first | Keep REQUIRED SUB-SKILL test-first |

**Authoring target:** elevate fallback to its own skill (routing) + full recipe
(setup, ledger, stop conditions, no unit barriers, no reviewer subagent).

## GREEN retest log (2026-07-30, grok-4.5)

| Scenario | CHOICE / result | Cite? |
|---|---|---|
| S-INLINE-1 tools exist + user inline | **A** self + test-first | yes — Iron Law |
| Routing 7 queries | plan/story/inline/root-cause correct split | yes |
| story-unit header + inline route | **A** no unit barrier | yes — sequential only |
| Plan gap + demo | **A** stop and ask | yes |
| One-line TDD pressure | **A** test-first first | yes |
| build-in-waves opened + user inline | **A** hand off build-inline | yes — build-in-waves Inline route |

## Ship gate

- [x] First-class skill + description for inline route
- [x] No implementer subagent under tool pressure
- [x] No unit barriers even if header is story-unit
- [x] Stop-on-blocker + test-first iron laws hold
- [x] build-in-waves redirects to build-inline (Inline Fallback removed)
- [x] Mode unset → write header for bookkeeping and proceed
- [x] Setup preflight is tracker sync + workspace
- [x] plan-tasks / AGENTS / templates family wire (downstream)

## Edit — polish-diff always + setup todo (2026-08-07)

Same failure class and form as `build-in-waves` / `build-by-story` (shared
After-the-last-task family): Setup Todos GATE includes **Polish Diff**;
mandatory step + red flags + rationalization rows.

## Edit — polish predicate + execute-common (2026-08-16)

Supersedes the always-polish GREEN. Close sequence / preflight / todos live
in `../execute-common/SKILL.md`. Terminal todo is **Close branch**. Polish is an
observable conditional; silent skip and EOD-as-predicate remain red flags.

## Render check pointer (v1.2.0, 2026-08-18)

Per-task loop gains step 7 **Render check** — a pointer to the one home in
`../build-in-waves/implementer-prompt.md` (same shape as the existing
Deviations pointer). RED/GREEN evidence lives in build-in-waves TESTS.md
§ Render check (sonnet, 2 RED omission reps, 2 GREEN reps incl. the
should-not-fire pure-logic case). Steps 8–11 renumbered; evidence bundle
(step 9) now carries the Visual check line when the check ran.
