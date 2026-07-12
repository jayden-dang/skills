# `dogfood`

> A human driving the real app through every user-facing ability and judging what they see. The deliverable is a persistent, checkable HTML artifact — not a chat message.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the spec triad — `requirements.md`, `design.md`, `tasks.md`; the source (theme tokens, CSS, keyword and label definitions); `docs/agents/project.md` (the `## Run locally (dev)` command) |
| **Writes** | a self-contained, theme-aware HTML artifact published with the Artifact tool (or an `.html` file when artifact tooling is absent) |
| **Calls** | `artifact-design` (required, loaded before building the page) |
| **Called by** | [`acceptance-check`](acceptance-check.md), [`verify`](verify.md) |

## When it fires

When you are manually exercising a finished feature in the real running app from the user's seat — a hands-on pass, case by case, over every user-facing ability, including the visuals, feel, and edge cases a human must eyeball rather than an automated test or a quick launch. Reach for it to try a feature for real, to walk the whole user-facing surface, or to produce a checkable, resumable test guide kept open beside the app and ticked off as you go — not a one-off run.

It complements [`acceptance-ui`](acceptance-ui.md), which automates flows into tests. `dogfood` is the manual, eyeball-it sibling for the judgment a test cannot make: does the badge color read right, does the interaction feel wrong, does the empty state look finished.

The deliverable is a **persistent, checkable HTML artifact**. A chat message is explicitly not the deliverable, for three concrete reasons the skill names:

- it saves no progress — every tick is lost when the conversation moves on,
- it cannot show the real badge the user checks against — only describe it,
- it scrolls away — the guide has to stay open beside the app, not slide up the transcript.

The artifact answers all three: it persists ticks, renders the real thing, and lives in its own tab.

## 1. Scope every ability from the spec

Read the feature's `requirements.md`, `design.md`, and `tasks.md`, and list every user-observable ability keyed to its requirement ID. That means three kinds of case, not one:

- the happy path — the feature doing what it is for,
- the edge cases — the empty input, the duplicate, the boundary,
- the deliberate non-behaviors — what should NOT happen, the Out-of-Scope decisions.

The third kind is what makes the pass an acceptance instrument rather than a demo: an Out-of-Scope decision is a claim about the build, and a claim deserves a checkbox.

Include the adjacent capabilities in the same user workflow, not only the new feature, because the user exercises the whole surface in one sitting. The step is done when every user-facing requirement ID has at least one case.

## 2. Ground each case in the real code

For each case, read the code to get what the user will ACTUALLY see: the exact vocabulary — keywords, command names, labels — the keyboard shortcuts, and the real rendering — badge colors, chip styles, icons — pulled from the source (theme tokens, CSS), **never guessed**. The artifact's "Expect" mirrors that rendering so the user checks against a true picture rather than a description you imagined.

Where the code reveals an honest caveat — a delimiter dimmed not removed, a status with no UI yet — the case says so. The point of grounding is that the guide tells the truth about the build, including where the build is unfinished. A guessed badge color or an invented label is worse than useless: the user checks their screen against the guide, and a wrong picture either flags a non-bug or hides a real one.

This is also why a behavior with no screen still gets a real observation method rather than a described one. If the only honest way to see a persisted flag is a devtools `invoke(...)` or a read-only peek at the store, the case says exactly that. It never draws a pretend screen for a surface that does not exist yet.

## 3. Boot the real app and find the honest observation point

Start the app with the `## Run locally (dev)` command from `docs/agents/project.md`, discovering and recording it if missing — the same contract [`acceptance-ui`](acceptance-ui.md) follows. Surface any degraded area up front: a feature needing a key, a sub-feature not built yet. The user should learn which parts are dimmed before they start ticking, not discover it mid-pass and mistake a known gap for a bug.

A behavior with no UI surface still gets a case — with a **real** way to observe it, a devtools `invoke(...)` or a read-only DB peek, never a pretend screen. The step is done when the app is running and every not-yet-visible behavior has an observation method.

## 4. Build the checkable artifact

The **required sub-skill** is `artifact-design`, loaded before building the page. Then build a self-contained HTML page and publish it with the Artifact tool. The contract:

- Sectioned by ability area; **one row per case**, each carrying its requirement ID so a failing box routes straight back to the spec.
- Each row is **Try** — what to type or click, copy-pasteable — then **Expect** — shown in the app's real rendering, not described in prose.
- **Interactive checkboxes that persist** via localStorage, plus a progress counter, so the user closes and resumes.
- Theme-aware and fully self-contained: inline CSS and JS, no external assets.

No artifact tooling in your environment? Write the same page to an `.html` file and hand over its path.

## 5. Hand over

Give the fastest way in — a roughly 30-second first pass that lights the feature up — then the degraded-feature notes and how to enable them, and note that ticks save. The 30-second pass matters because a guide the user never starts checks nothing; the first win is what earns the rest of the walkthrough. The step, and the skill, is done when the artifact is published, grounded, resumable, and every ability and non-behavior is a checkable, ID-tagged case.

## Worked example

The note-taking app's `NOTE` feature is finished; dogfood produces the guide the user keeps open beside the app. Step 2 reads the source to ground the rendering: the "Add" button label comes from the component, the empty-note error text `Note cannot be empty` from the validation, and the error chip's red from a theme token, `--color-danger: #d4351c`. The artifact mirrors those exactly rather than paraphrasing them.

Step 3 boots the app and confirms every case has an honest observation point; the two `NOTE` behaviors are both visible on screen, so no devtools peek is needed here.

One grounded row, in the create-a-note section of the artifact:

| ✓ | ID | Try | Expect |
|---|---|---|---|
| ☐ | `NOTE-1.1` | Type `buy milk` in the New note field and click **Add** | The note appears at the top of the list as a card reading "buy milk"; the input clears. Reload the page — the card is still there. |
| ☐ | `NOTE-1.2` | Clear the field, type a single space, click **Add** | A red chip reads **Note cannot be empty** (danger red `#d4351c`); the space you typed stays in the field, not cleared. |

The `NOTE-1.2` "Expect" mirrors the real chip rather than paraphrasing it: the user sees the exact red they check against, so a mismatch is unambiguous.

The checkboxes persist in localStorage and a counter shows `0 / 2`, so the user can close the tab mid-pass and resume. The hand-off gives the 30-second first pass — create one note, then submit an empty one — that lights the feature up.

## Rationalizations

The skill carries a three-row table naming the shortcuts an agent takes to avoid building the artifact, each countered:

| Thought | Reality |
|---|---|
| "A markdown checklist in chat is enough" | It saves no tick, cannot show the real badge being checked against, and scrolls away. The deliverable is the persistent artifact. |
| "They're in a native desktop app, not a browser, so an artifact doesn't fit" | The artifact is a companion reference kept open beside the app; the app being native is no reason to inline the guide into chat. |
| "I'll describe the badge in words" | The user checks against what they SEE. Mirror the real rendering, or the Expect is unverifiable. |

## Why it is written the way it is

`dogfood` is the manual sibling of [`acceptance-ui`](acceptance-ui.md), and the split is principled: `acceptance-ui` automates the flows a machine can assert, and `dogfood` takes the judgment a machine cannot — whether the badge color reads right, whether the interaction feels wrong, whether the empty state looks finished. Neither replaces the other, which is why [`acceptance-check`](acceptance-check.md) can dispatch to both for the same feature.

Every rule in `dogfood` defends the same thing: a guide the user can actually check against. Grounding the "Expect" in real theme tokens rather than prose, mirroring the true rendering, and building a persistent artifact instead of a chat message all answer the failure of a dogfooding pass that describes what *should* appear and cannot be verified against what *does*. The persistence — checkboxes in localStorage, a progress counter — exists because a real pass over a whole surface is not done in one sitting; a guide that forgets your ticks is abandoned. And scoping the deliberate non-behaviors alongside the happy path is what makes it an acceptance instrument rather than a demo: the Out-of-Scope decisions are as much a claim about the build as the features are.

The three-row rationalization table above is the same shape the set uses wherever an agent is tempted to take a cheaper path than the skill demands: each row names the tempting thought and answers it with the reason it fails, so the shortcut is refused by name rather than rediscovered each run.

## See also

- [`acceptance-ui`](acceptance-ui.md) — the automated sibling that turns flows into committed specs
- [`acceptance-check`](acceptance-check.md) — the orchestrator that hands off eyeball qualities to it
- [Artifacts](../concepts/artifacts.md) — why the deliverable is a persistent, checkable page
- [`verify`](verify.md) — which names a manual `dogfood` pass as a way to earn "the feature works"
