# B03 — cross-cutting additivity audit

Baseline for Task 3: a cross-cutting audit (no new content edit) confirming Task 1's edit to
`skills/spec/write-design/SKILL.md` and Task 2's edit to `skills/spec/write-plan/SKILL.md` are
additive and advisory — a feature with no reuse opportunity still produces today's structure
unchanged, with no new hard approval gate. Verified by baseline scenario, not an automated
harness (see Global Constraints). RED = walked before Tasks 1–2 existed (n/a — this is a
post-hoc audit of already-committed edits); GREEN = walked against the current file bodies,
confirmed to hold.

## S1 — No-reuse feature, structure unchanged, no new gate

Take a feature with no reuse opportunity (every component is genuinely new, rung 7). Walk it
through the edited `write-design` and `write-plan`.

**Walk — write-design:**

- Step 2 ("Architecture with Satisfies lines") still produces one `###` section per
  component, each carrying its `Satisfies:` line, unchanged. The "design it twice" guidance
  for genuinely hard parts is unchanged. The deletion test (rescoped to rung-7 components by
  Task 1's S5) is unchanged in mechanics.
- The added `Reuse:` line for a rung-7 component reads `Reuse: none — new code (rung 7)` with
  a one-line reason no lower rung held — a line beside `Satisfies:`, not a replacement for it
  and not a precondition for it.
- Step 4 ("Coverage self-check, then the approval gate") still walks requirements.md top to
  bottom checking every ID appears in a Satisfies line; the added "Reuse coverage:" bullet
  only checks that the (already-required) `Reuse:` line and rung-7 justification are present —
  it does not gate the Satisfies-line walk or the approval gate itself.
- `write-design/SKILL.md:50` — grep confirms: "are advisory — surfaced for the user, never a
  hard blocker."

**Walk — write-plan:**

- Step 3 ("Tasks as vertical slices") still produces each task with Files
  Create/Modify/Test, Interfaces, Depends-on, Steps, and the `_Requirements:_` footer, all
  unchanged. The added `Reuse:` task bullet sits between **Files** and **Interfaces** and, for
  a rung-7 task, names the few or no existing things it builds on (carried down from the
  design section's `Reuse:` line) — it does not block a task from being written when nothing
  existing applies.
- Step 4 ("Coverage and consistency check") still runs the trace check, the test-coverage
  check, and the seam-table reconciliation unchanged. The added "Component-level reuse-miss"
  and "Reuse consistency" bullets are two more items on the same advisory check list as
  "Type/name consistency across tasks" — findings to fix before offering execution, not a
  distinct approval step.
- `write-plan/SKILL.md:97` — grep confirms: "it is an advisory finding, not a hard block."

**Walk — no new gate:**

- `grep -n "^## Step" skills/spec/write-design/SKILL.md skills/spec/write-plan/SKILL.md` lists
  only the steps that predate this feature (write-design Steps 1–4; write-plan Steps 1–5,
  Step 5 optional) — no new `## Step` heading was added by either edit.
- `git show --stat` on Task 1's commit (`c2b507f`, write-design) and Task 2's commit
  (`dc803e5`, write-plan) shows insertion-only diffs to existing paragraphs and bullet lists;
  neither introduces a new `STOP` or a new "approval gate" — the one `STOP` in write-design
  (line 133, "Present the FILE to the user... and STOP") and the one `approval gate` phrase
  (Step 4's own heading) both predate the reuse feature.
- The Step-4 reuse findings in both skills surface at the existing approval gate/STOP and
  never block approval or a commit on their own — same standing as the pre-existing
  "Type/name consistency across tasks" and "placeholder scan" checks they sit beside.

Confirmed: the write-design and write-plan structure a no-reuse feature produces — Satisfies
lines, Files Create/Modify/Test, Interfaces, Depends-on, Steps, footers — is unchanged, and no
new hard approval gate exists.

`[REUSE-5.3]`

## Coverage self-check

Task 3's one ID appears in the tag above: 5.3 — 1 of 1, none missing, none double-defined.
