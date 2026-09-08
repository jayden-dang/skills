# zone-mode — recorded test evidence

## 1.1.0 — user-invoked; SessionStart injector removed (2026-09-08)

**RED:** leftover `SessionStart` hooks (plugin `hooks/hooks.json`, vendored
`.claude/hooks/session-start.sh`, Cursor `alwaysApply` rule) still injected
this skill at session start, including copies that named the deleted
`gate-session` skill. Auto-injection fought the user's preference that the
gate load only when they run `/zone-mode`.

**GREEN:** `disable-model-invocation: true`. No pack SessionStart hook, no
consumer-repo session-start template, no Cursor always-apply rule. Agents
name `/zone-mode` for the user; they do not auto-invoke it. `AGENTS.md`
carries the 1% rule without a hook.

## 1.0.0 — formed from gate-session and ask-me-bro (2026-09-08)

This skill is a merge, not a new gate. Its content and the evidence behind it come
from the two skills it replaces.

**From `gate-session`.** The `<SUBAGENT-EXEMPT>` block, the 1% `<NON-NEGOTIABLE>`,
`## The Rule`, the six-row rationalization table, and `## Precedence` are carried
over unchanged. `gate-session`'s contract eval cited `SKILL.md § The Rule`; that
heading and that eval survive here.

**From `ask-me-bro`.** `## Handing off` carries its one load-bearing rule — invoke
a model-invocable target, name a user-invoked one for the user to run — plus its
context-hygiene line and its instruction not to execute the chosen flow from
inside the router. Its eval is carried over, re-anchored to the new heading, and
extended with the invocability assertion, which is the part
`scripts/lint-write-handoffs.py` also guards mechanically.

**What was cut before shipping, and why.** Two lines were drafted and removed for
having no baseline behind them, on the same standard that killed eight other
proposals in this branch:

- A rationalization row countering an agent that names the right skill and then
  acts as the skill would instead of reading it. Plausible, unobserved. Not
  written.
- A sentence declaring the mode sticky across every turn. The `SessionStart` hook
  already injects this file on startup, `/clear` and compaction, so the sentence
  restates a mechanism rather than adding one.

**What was deliberately not ported.** The mode skill this was modelled on is a
Cursor skill using `mode:` and `reminder:` frontmatter. This set ships to five
harnesses, and stickiness here is the hook, which survives the two moments context
is lost. No harness-specific field was added.

**Verification.** The hook was run end to end and its output parsed: valid
`SessionStart` JSON, naming `skills:zone-mode`, carrying the 1% rule, `## The
Rule` and `## Handing off`. Both eval anchors resolve. The sweep that removed the
old names covered the hook, the Cursor always-apply rule, three plugin manifests,
the consumer-repo `session-start.sh` template pair, and twenty documentation
references; `CHANGELOG.md` and other skills' `TESTS.md` keep the old names because
they record what was true when written.
