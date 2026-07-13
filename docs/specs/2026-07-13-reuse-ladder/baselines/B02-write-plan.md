# B02 — write-plan skill

Baseline for Task 2: editing `skills/spec/write-plan/SKILL.md` to carry the design layer's
`Reuse:` line down into each task, and to teach the Step-4 coverage check to flag a task that
rebuilds what already exists. Each scenario is walked by hand against the edited skill body
(this repo verifies skills by baseline scenario, not an automated harness — see Global
Constraints). RED = walked before the edit existed (no `Reuse:` task field and no
component-level reuse checks in Step 4, every scenario fails by definition); GREEN = walked
after editing, confirmed to hold.

## S1 — task Reuse line

Step 3's per-task field list gains a `Reuse:` bullet, immediately after **Files** and before
**Interfaces**, naming the concrete existing code, library, or pattern the task builds on —
carried down from the design section's `Reuse:` line — so the implementer is told to build on
it, not reimplement it.

**Walk:** Read Step 3's task field list. Confirm a `- **Reuse:**` bullet appears right after
the **Files** bullet and before **Interfaces**. Confirm it names existing code/lib/pattern as
the thing the task builds on, gives an example (`Reuse: src/util/dates (parseISO), zod`), and
states it is carried down from the design section's `Reuse:` line.

`[REUSE-3.1]`

## S2 — design↔task consistency

The `Reuse:` bullet's text states the task's `Reuse:` line must stay consistent with the
`Reuse:` line of the design section the task implements — so a task cannot silently drift
from what its design section already decided to build on.

**Walk:** Read the same `Reuse:` bullet from S1. Confirm its closing sentence instructs
keeping it "consistent with the `Reuse:` line of the design section this task implements."

`[REUSE-3.2]`

## S3 — component-level reuse-miss

Step 4's check list gains a bullet, right after "Type/name consistency across tasks," that
flags any task whose Files **Create** something the scan digest or an already-installed
dependency already provides. It is named as the task-granularity sibling of the `reuse-miss`
finding `code-review` raises for feature-level overlap, and it is explicitly advisory, not a
hard block.

**Walk:** Read Step 4's check list immediately after the "Type/name consistency across tasks"
bullet. Confirm a **Component-level reuse-miss** bullet is present. Confirm it names the
condition (a task's Files Create something the scan digest or an installed dependency already
provides) and instructs building on it instead of rebuilding it. Confirm it names itself as
the task-granularity sibling of `code-review`'s `reuse-miss` finding, and states it is
advisory, not a hard block.

`[REUSE-4.2]`

## S4 — reuse consistency check

Immediately after the component-level reuse-miss bullet, Step 4 gains a second bullet that
flags any task whose `Reuse:` line disagrees with the `Reuse:` line of the design section it
implements — the enforcement half of the S2 authoring instruction.

**Walk:** Read the bullet immediately following the "Component-level reuse-miss" bullet from
S3. Confirm a **Reuse consistency** bullet is present and states it flags a task whose
`Reuse:` line disagrees with the `Reuse:` line of the design section it implements.

`[REUSE-4.3]`

## Coverage self-check

Every one of Task 2's 4 IDs appears in at least one tag above: 3.1, 3.2, 4.2, 4.3 — 4 of 4,
none missing, none double-defined.
