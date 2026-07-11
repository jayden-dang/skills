# `prototype`

> Throwaway code whose only job is to answer one design question. The question decides the shape, and the answer is the only thing that survives.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the host project's stack and task runner (`docs/agents/project.md` when present); the surrounding code the question is about |
| **Writes** | throwaway code marked `prototype` in its path or filename; the captured answer into an ADR, requirement, or commit message |
| **Calls** | [`tdd`](tdd.md) when the validated piece is reimplemented as production code; the ADR gate in [`domain-modeling`](domain-modeling.md) |
| **Called by** | [`brainstorm`](brainstorm.md) (the "does this feel right?" evidence detour) |

## When it fires

When a design question needs a **runnable** answer — the user wants to prototype, spike, or mock up a state model, a piece of logic, or a screen to feel out whether it holds up before committing to a real implementation.

[`brainstorm`](brainstorm.md) detours here when a question can only be settled by driving something by hand, not by opinion. It is the sibling of [`research`](research.md): where research answers an external-fact question with a cited note, prototype answers a "does this feel right?" question with something you can actually use.

## Pick a branch

Identify the question first — from the request, the surrounding code, or by asking. It decides the whole shape of the prototype, so it is settled before any code is written:

- **"Does this logic / state model hold up?"** → **[LOGIC.md](../../../skills/discovery/prototype/LOGIC.md)**: an interactive terminal app over a pure logic module the user can drive by hand. Right when the question is about business rules, state transitions, data shape, or an API's feel — things that read fine on paper and break only when pushed through awkward cases.
- **"What should this look like?"** → **[UI.md](../../../skills/discovery/prototype/UI.md)**: several structurally different variants of one screen, mounted on a single route and flipped between with a floating switcher in the running app.

Picking the wrong branch wastes the whole prototype — a logic question answered with a screen, or a look question answered with a state machine, teaches nothing.

If it is genuinely ambiguous and the user is unreachable, choose by proximity — a backend module leans logic, a page or component leans UI — and record the assumption at the top of the prototype so it can be corrected.

## Rules for both branches

The two branches differ in what they build, but they share six rules that keep either from calcifying into production:

1. **Throwaway from day one, and marked as such.** Put it near the code it explores so context is obvious, but name it so nobody mistakes it for production (`prototype` in the path or filename). Follow the project's existing conventions — never invent new top-level structure for it.
2. **One command to run.** Register it with the project's existing task runner (read commands from `docs/agents/project.md` when present) so the user starts it without thinking.
3. **No persistence.** State lives in memory. Persistence is what the prototype is *testing an idea against*, not something it depends on. If storage itself is the question, use a scratch store with an unmistakable "prototype — safe to wipe" name.
4. **Skip the polish.** No tests, no abstractions, no error handling beyond staying runnable. Speed of learning is the whole point.
5. **Surface internal state.** After every action or variant switch, show the full relevant state — hidden state hides the answer.
6. **Delete or absorb when done.** Once the question is answered, remove the prototype or fold the validated piece into real code. Reimplementing it as production code is a REQUIRED SUB-SKILL call to [`tdd`](tdd.md) — the prototype's logic is a reference, not tested code. Never leave it to rot.

## The logic branch

The **[LOGIC.md](../../../skills/discovery/prototype/LOGIC.md)** branch builds a full-frame terminal app over a pure logic module.

The question is written down first, in one paragraph at the top of the prototype, because a logic prototype aimed at the wrong question is pure waste and the written question is what the verdict is checked against later. It uses the host project's stack — no new package manager, runtime, or styling library for a throwaway.

The part that answers the question is isolated behind a small pure interface — a reducer `(state, action) -> state`, an explicit state machine, a handful of pure functions, or a module owning internal state — chosen to fit the question, not to be easiest to wire. **The direction of dependency is absolute: the TUI imports the logic module and nothing flows back.** The logic module is the only part that may outlive the prototype; once validated it can be lifted into real code while the TUI shell is deleted. Each frame clears the screen and re-renders the current state (easy to diff by eye) plus a key legend, then reads one keystroke and dispatches it. Shipping the TUI shell, wiring a real database, and letting terminal codes leak into the logic module are named anti-patterns.

## The UI branch

The **[UI.md](../../../skills/discovery/prototype/UI.md)** branch drafts several structurally different takes on one screen.

By default they are **embedded inside an existing page** — the route, data fetching, params, and auth all stay; only the rendered subtree swaps per variant — because a variant judged in a vacuum always looks fine, while against the real header, sidebar, data, and density the weak ones expose themselves. A new throwaway route is a last resort, only when there is genuinely no page to embed in.

Default **3 variants, never more than 5** — beyond that they stop being different and start being noise. Structurally different means different layout, information hierarchy, and primary affordance — not the same layout recolored; if two drafts converge, one is redone under an explicit structural constraint like "no card grid this time."

A single route reads a `?variant=` query param and renders the matching component alongside a floating switcher (bottom-center pill, arrow keys cycle except while an input is focused, styled to obviously not belong to the design, and **hidden in production builds** so an accidental merge can never show users the switcher). Data fetching stays above the switch so every variant gets identical real data, and variants stay read-only. The best feedback is usually a hybrid — "A's layout with C's detail panel" — and that hybrid is the real answer.

## The answer is the only deliverable

Nothing about the prototype's code matters afterward — only what it taught you. That is the one line to remember from the whole skill.

Capture the question and its answer somewhere durable: an ADR (if it clears the ADR gate in [`domain-modeling`](domain-modeling.md)), a requirement in the feature's requirements.md, or the commit message that deletes or absorbs the prototype. If the user is not around to give the verdict, leave a clearly-marked placeholder for it next to the prototype so it gets filled in before deletion — an un-captured answer is a prototype that ran for nothing.

## Worked example

During a `brainstorm`, the open question is "should a task's status be a free enum or an explicit state machine with guarded transitions?" That is about behavior under awkward cases, so the **logic branch** is chosen.

A one-paragraph question is written at the top of `src/tasks/prototype-status-machine.ts`. A pure `(state, action) -> state` reducer models the transitions; a ~40-line TUI in the same directory clears the screen each frame, prints the current task state, and offers `[s] start  [b] block  [d] done  [r] reopen  [q] quit`. The TUI imports the reducer and nothing flows back — so the reducer, and only the reducer, can graduate later.

It is wired into the existing task runner as `npm run proto:status`. The user drives it and immediately hits "wait — I could move a *done* task straight back to *blocked*, that shouldn't be allowed." That is a defect in the *idea*, exactly what the prototype is hunting.

The verdict — "guarded state machine; illegal transitions must be rejected, not silently applied" — is captured as a requirement in the feature's requirements.md.

The prototype is then deleted, and when the machine is built for real it goes through [`tdd`](tdd.md); the reducer serves only as reference, never as tested code. What survives is the answer and the requirement it became — not a single line the prototype ran.

## Why it is written the way it is

The failure the skill guards against is a prototype that quietly becomes production — untested code, written for speed of learning, drifting into the real system because it "already works." The throwaway-from-day-one marking, the no-tests rule, and the requirement that any real reimplementation pass through [`tdd`](tdd.md) all exist to keep that boundary hard.

Splitting into two branches keeps each honest. A logic question answered with a pretty screen, or a look-and-feel question answered with a state machine, both miss — so the skill forces the question to be named before any code, and lets that choice pick the shape.

Making "the answer is the only deliverable" explicit stops the effort from being measured by how much code was written instead of what was learned. The code is scaffolding around a single question; once the question is answered the scaffolding comes down.

## See also

- [`brainstorm`](brainstorm.md) — the caller that detours here for a runnable answer
- [`research`](research.md) — the other evidence detour, for external-fact questions
- [`tdd`](tdd.md) — the gate any validated piece passes through to become production code
- [`domain-modeling`](domain-modeling.md) — owns the ADR gate the answer may be captured in
