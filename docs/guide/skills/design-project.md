# `design-project`

Use this when the design system and architecture of a project need to be
chosen or reconsidered together. Start with greenfield work, a running
app with scattered UI conventions, a takeover, or a foundation change.

| Starting point | First question |
|---|---|
| New project | What's the first useful flow, and what could invalidate the chosen foundation? |
| Running app | Which shared patterns can be extracted without changing what existing workflows mean? |
| Takeover | Which version of the system can we verify, and who owns data, releases and recovery? |
| Migration or expansion | Can the existing seam handle the new use, and how would both paths run during transition? |

## What you get

- A comparison of the viable designs on the same flow. It covers the shared
  experience as well as modules, state, runtime and integration boundaries.
- An architecture diagram and any sequence, state, design-system or migration
  views needed to make the decision. The note contains editable Mermaid or
  links to the diagram source. The figures distinguish observed, reported and
  proposed paths.
- A small, reproducible experiment for the main flow, a consequential failure,
  and one follow-on change or consumer. Each result says what was exercised
  and what remains unverified.
- A build decision with three possible outcomes. Start the named slice, start
  only the independent work, or run a named check first. Every held item has a
  condition and a role to follow up.

Try: “We just inherited a dispatch app. Work out a shared design system and
architecture, show the local and reported live paths, and tell us what we can
start building this week.”

[Define Project](define-project.md) maintains accepted standards and architecture
records. [Draft UI](draft-ui.md) explores a particular screen or interaction.
[Design Solution](design-solution.md) designs a feature against approved requirements.
