# `design-page`

> The visual-craft gate before any human-facing HTML. The question is never *whether* to design — a memo deserves the same craft as a landing page. What changes is the treatment that craft is delivered in.

|  |  |
|---|---|
| **Bucket** | craft |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the design system already in the repo — `CLAUDE.md`, `docs/agents/*.md`, a tokens or theme file, existing component styles |
| **Writes** | a three-slot design plan (color / type / layout) before any markup, then the page derived from it |
| **Called by** | [`dogfood`](dogfood.md) (required, before building the test-guide artifact), [`improve-architecture`](improve-architecture.md) (required, before the architecture report's markup) |

## Where it comes from

This skill is a rewrite of Claude Code's built-in `artifact-design`, renamed so both can coexist — the built-in stays available and untouched, and this one carries the house conventions plus two changes of scope:

- **Medium-agnostic.** The built-in assumes the Artifact tool. `design-page` also covers the plain `.html` file a skill hands over when artifact tooling is absent — which is why the no-webfont-CDN rule cites two failure modes, not one: a published artifact's CSP blocks font hosts, and a handed-over file gets opened offline.
- **Precedence made explicit.** The user's own words, then the project's existing system, then the agent's choices. In a repo running this skill set there usually *is* an existing system, so "look before inventing" is a step, not an aside.

## When it fires

Before the first line of markup for any HTML a human will look at: a dogfood test guide, a report, a dashboard, a landing page, a published artifact, a standalone `.html` handoff. Also when a page's colors, typography, dark mode, spacing, or visual treatment need deciding — or when a page has come out looking generic and needs a reason why.

## 1. Name the treatment

Two treatments, said out loud before anything else:

- **Utilitarian** — a test guide, plan, memo, report, internal dashboard, demo. Real typographic hierarchy, considered spacing, a proper palette; no gigantic hero, flourishes tasteful and few. Most pages this skill set produces are here.
- **Editorial** — a landing page, a game, a tool the user will keep or share. Section 5 of the skill runs only for these.

The tie-break, when it is genuinely unclear: a well-composed page is never the wrong answer; an over-designed visual identity sometimes is.

## 2. Precedence, then the plan

Precedence is fixed — **the user's words → the project's existing system → your choices.** When a design system already exists in the repo, apply it; the fundamentals fill its gaps and never override it.

Then three REQUIRED slots, filled in before any markup:

| Slot | Contents |
|---|---|
| **Color** | 4–6 named hex values |
| **Type** | typefaces for 2+ roles — a characterful display face used with restraint, a complementary body face, a utility face for captions or data if the page has any |
| **Layout** | the layout concept, one or two sentences |

The step is done when the plan is written and every color and type decision in the page traces back to a slot in it. This is the mechanism that keeps the output from being generic: a palette assembled tag by tag as the CSS is written is exactly the one that comes out looking like every other page.

## 3. The fundamentals

Every page, every treatment. The skill carries them in full; the load-bearing ones:

- **Ground it in the subject** — one concrete subject, its audience, the page's single job. Real content throughout, never lorem.
- **Pair typefaces, and inline them** — no webfont URL, because it fails *silently* to a fallback face and takes the type plan with it. `@font-face` data URI, or design deliberately with the system stack.
- **Choose neutrals** — a grey biased slightly toward the accent's hue reads as chosen; a pure mid-grey reads as inherited.
- **Design both themes at the token level** — palette as custom properties on `:root`, redefined under `@media (prefers-color-scheme: dark)` and again under `:root[data-theme="dark"]` / `:root[data-theme="light"]` so an explicit toggle overrides the OS preference in both directions. Components are styled through the tokens, never inside the media query.
- **Let layout do the spacing** — flex/grid with `gap`, `overflow-x: auto` on wide content's own container, `tabular-nums` where digits line up.
- **Watch selector specificity** — a `.section` rule fighting a `.cta` rule silently undoes your spacing.
- **Build cleanly** — closed elements, quoted attributes, visible focus state, `prefers-reduced-motion`, Canvas or WebGL over hand-authored SVG path data, everything self-contained.
- **Copy is design material** — named from the user's side of the screen, active voice, a control that says exactly what happens.
- **Structure encodes something true** — numbered markers (01 / 02 / 03) are right only when the content actually is a sequence.
- **UI ≠ document** — a dashboard is scanned and operated: summary before detail, state encoded in form as well as number, semantic color kept separate from the accent.

Two conditional hand-offs: `dataviz` before writing any chart code, and `artifact-capabilities` before declaring runtime capabilities on a published artifact.

## 4. The house style to avoid

AI-generated design currently clusters on a handful of looks — warm cream with a serif display and terracotta accent; near-black with one acid-green pop; the purple-to-blue gradient hero; Inter or Space Grotesk as the "safe" face; emoji section markers; everything centered; `rounded-lg` everywhere.

The rule is not a ban. Where the user pins a direction, follow it exactly — their words win, including when they ask for one of these. Where nothing is specified, that freedom is the whole budget, and spending it on the default look wastes it.

## 5. Editorial

The stance shifts: the client has already rejected proposals that felt templated. Review the plan from step 2 against the subject first — any part that reads like the generic default gets revised, with a note on what changed and why — and only then write the code.

The principles: the hero is a thesis; typography carries the personality; motion is deliberate and orchestrated rather than scattered; complexity matches the vision; boldness is spent in one place with everything around it quiet.

## Related

- [`dogfood`](dogfood.md) — a caller. Its deliverable is a persistent, checkable HTML artifact, which is why the design gate is required rather than suggested.
- [`improve-architecture`](improve-architecture.md) — the other caller. Its ephemeral HTML report is the UI-not-a-document case: cards scanned for a badge and a structure sketch, not read in order.
- [`writing-skills`](writing-skills.md) — the standard this skill is written against.
