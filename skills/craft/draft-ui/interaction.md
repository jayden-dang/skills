# Draft UX

Requirements do not imply an interaction. Handed the same Approved
requirements, the same component kit, and the same locked look, two competent
runs shipped **opposite** answers — one removed the rows on click and offered
six seconds of undo, the other held the list frozen until the call returned —
and each wrote up its own answer as the one the requirements forced. Whichever
one gets built is a decision. This skill makes it the user's decision, felt in
the browser before it is spec'd, and puts it where the build reads it.

## 1. List the moments

From the requirements and the existing brief, write one line per **moment** —
an action whose outcome is not implied: `<trigger> → <what the user should be
able to feel>`. Every moment carries its branches: what happens instantly,
what happens while the system is working, what happens on success, what
happens when it fails, and how the user gets back out.

*Done when: every requirement ID with a verb in it has at least one moment, no
moment is missing its failure branch or its way back, and the list is written
where the user can read it — not held in your head while you build.*

## 2. Diverge on when the world changes

Build **2–3 takes of the same flow**, named. They differ in *when the world
changes and what the user owes for it* — commit-on-click with a way back;
hold-until-confirmed with a busy state; ask-first. They do **not** differ in
markup, color, or component: the look is settled, and a take that needs a
component the repo does not have is out of scope — say so and build a
different take instead.

Serve them the way `draft-ui` §2 serves variants: in the project's own UI
stack, one switch, one switcher, real data, real components. Latency is part of the take, not an
accident of it — simulate the call with a named delay constant and give the
failure branch a hook you can flip, both inside the fake `draft-ui` §2 puts
behind the app's client, so the takes call it the way the real call will be
called.

*Done when: each take runs end to end including its failure branch, and any
two takes differ in when the list changes — not in how it looks.*

## 3. Every number is a decision

Each take carries its own numbers, and each number carries a reason and a
slow-path answer: the delay it simulates, the window it gives (undo,
auto-dismiss), and **what the user sees when the real call outruns the
budget**. Roughly: work that finishes in about a tenth of a second reads as
instant; past about a second of silence the user needs a pending state; a
window too short to read the toast in is not a window.

A constant whose reason is *"it made the failure path demoable"* is a
prototype artifact about to be spec'd as a requirement.

*Done when: every number in every take has a one-line reason, and every moment
has an answer for the call that takes far longer than its budget.*

## 4. Show, recommend, then wait for the go

Hand over the URL — or the launch command, for a native app — and one line per take naming **what it costs the user** —
not what it does. Recommend one, with the reason, in your own voice. Anything
you gave *every* take — a retry action, a focus rule, a line of copy — is not
part of the pick: name it on its own line, because the user is not choosing it
and silence makes it look chosen. Then
loop: collect the pick — a take, or a hybrid — **and the amendments** that come
with it; apply them to the live takes; show again; repeat until the user gives
an explicit go.

**An instruction to decide is an instruction to recommend. It is never
authority to lock.** "Decide, don't hand me a menu" is answered by naming your
pick and your reason at hand-over — with the takes still live and the brief
still unwritten. When the go does not come in this turn, the turn **ends
here**: steps 5 and 6 do not run in a turn where the user has not answered.

**An absent user is the case this rule is for, not an exception to it.** Away,
in meetings, back on Monday, "get it to a finished state" — none of these is a
go. A written brief is what the build lifts and nobody re-opens a decision
already written down, so filing one while they are away does not preserve
their choice, it spends it. Leaving the takes runnable alongside it changes
nothing: the lift reaches the file, not the prototype.

*Done when: the user has said go on a specific take or hybrid — or the turn
ended at the hand-over with every take still running and `git status` showing
no brief touched.*

## 5. Lock into the file the build already reads

After the go, and not before it. Write `## Interaction` **into this feature's
`ui-brief.md`** — the same file the visual sections live in, created if it does
not exist yet. One `###` per
moment, filling the same five slots the visual sections fill (`Layout:`,
`Components:`, `States:`, `Type & color:`, `A11y:`), so `design-solution` Step
2b lifts them with the rest. On the section head:

- **Decision:** the chosen take in one line, plus why in the user's words
- **Grounding:** the requirement IDs it satisfies and the components it uses
- **Timings:** each number, its reason, and its slow-path answer
- **Amendments:** what the user changed during review, as decided constraints

Not a sibling `interaction-brief.md`, not the commit message, and not a
pointer added to an Approved `requirements.md` — a decision the build's lift
step does not reach is a decision that gets made again from scratch.

*Done when: `## Interaction` is in `ui-brief.md`, every moment has its five
slots, and every number carries its reason.*

## 6. Keep the winning take, or delete the prototype

The lock is what starts this step. Before it, every take stays live and
runnable, which is how the user keeps clicking them.

**Screens exist, or a stack is declared:** the winning take stays. Follow
`keep.md` beside this file, the same as for a look. The take's delay constants
and failure hooks stay inside the fake, behind its switch. Its lock tests cover
each moment's branches.

**No stack is declared:** delete the losing takes and the winning one, the
switcher, the simulated delays and the failure hooks. Restore every file the
prototype touched. The build writes the flow from the brief under
`test-first`.

On either path, a real bug found in a file outside the surface is **reported,
not fixed here**. A fix made here rides into the tree inside a draft commit,
and nobody reviews it as a fix.

*Done when: `keep.md`'s checks hold. On the delete path, `git status` is clean
except for the brief and its screenshots, and the cleanup commit references the
brief path.*

## Hand-off

`design-solution` Step 2b lifts `## Interaction`'s per-surface slots 1:1
alongside the visual ones; Decision, Timings, and Amendments stay in the brief,
which the design cites.

## Rationalizations

| Thought | Reality |
|---|---|
| "The requirements already imply the interaction" | Two runs on these exact requirements built opposite flows, each certain the requirements forced it. What they force is a decision, not an answer |
| "Undo is the standard pattern — no need to show the alternative" | Standard for whom, at what cost, on this data? The user finds out by feeling both for ten seconds, which is cheaper than finding out after it ships |
| "You told me to decide, not to hand you a menu" | The recommendation is the decision. The takes are what make it yours to overrule |
| "They're away and the implementer needs this next week — write it now, they can override later" | Nobody re-opens a written decision. A brief filed in their absence *is* the spec, so this trades their choice for a day of lead time |
| "All three takes are still runnable, so the pick stays open" | The build lifts the brief, not the takes. Whatever is still running, the written section is what gets built |
| "I wrote the deviation into Amendments, so it stays overrulable" | The build lifts that section; a confession inside it does not stop the lift. A user overrules a recommendation in conversation, not a spec section they never saw |
| "They asked to feel it, so the winning take stays in `app.js`" | Then nothing is locked yet either. Takes stay live until the go, and only the go starts step 6 |
| "A separate `interaction-brief.md` is cleaner" | Cleaner and unread. The lift step reaches `ui-brief.md`; a sibling file is a decision the build never sees |
| "Pointing `requirements.md` at the decision keeps it findable" | It edits an Approved document to compensate for filing the decision in the wrong place. Put it in the brief instead |
| "500ms is a reasonable placeholder" | The placeholder becomes the spec'd number. Give it a reason or leave it out |
| "I found a real bug while prototyping — fixing it is a courtesy" | A fix to a file outside the surface rides in a draft commit nobody reviews as a fix. Report it |

## Red Flags

- One take, and a write-up explaining why it was the only possible one
- A brief written while the user is away, so the implementer "has it regardless"
- A brief written at all before the go — a turn that ends with `## Interaction` on disk and no answer from the user in between
- A take left running in a production file after the lock, or deleted before it
- `## Interaction` living anywhere but this feature's `ui-brief.md`
- A simulated delay or an undo window with no reason next to it
- No answer anywhere for the call that takes ten seconds
- Simulated delays or failure hooks anywhere but the fake after the lock, or a winning take deleted in a repo with a stack
- Takes that differ in how they look rather than in when the world changes
- An affordance added to every take and never named at hand-over
