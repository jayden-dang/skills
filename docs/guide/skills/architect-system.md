# `architect-system`

Use this when the system's architecture needs choosing or rethinking for the
whole codebase: how the code is structured, who owns which data, how modules
and services talk, how work is handed off, what is cached, how it recovers,
and the principles every feature builds by. When the project has a client (web,
desktop or mobile), it also covers the front end: rendering and the UI thread,
client state, data access, version skew, accessibility, i18n, performance budget,
client security, offline, packaging and updates. It works for a new project, a
running codebase, a takeover or a migration.

It decides and does not record. Production code and `docs/architecture/`
stay untouched until you approve; then `define-project` writes the approved
invariants down.

| Starting point | First question |
|---|---|
| New project | What's the first useful flow, and what could invalidate the chosen foundation? |
| Running codebase | What does the code already do consistently, and where do two places disagree? |
| Takeover | Which version of the system can we verify, and who owns data, releases and recovery? |
| Migration | How do the old and new paths run side by side, and what makes rollback safe? |

## What you get

- The forces each choice turns on, sourced from the repo, and the questions
  only you can answer (a product policy, a budget), asked before the choice
  that depends on them.
- A **Parts** table covering structure, data, permissions, communication,
  messaging, caching, recovery, observability, deployment, test architecture,
  evolution and principles. Each part is decided, already settled, deferred
  with a trigger, or not needed yet.
- For each decided part, the options compared, the choice, what was rejected
  and why, and an architecture diagram.
- Disposable probes in scratch for the claims the decision turns on, each
  saying what it exercised and what it leaves open.
- Proposed `ARCH-N` invariants, each with the check that fails when someone
  breaks it.
- A start-or-hold call, and the list `define-project` will record once you
  approve.

Try: "We're three developers on one Postgres and the CTO wants Kafka. Decide
how the parts of this system should talk to each other and hand off work."

[Define Project](define-project.md) records the approved invariants and
documents. [Design Solution](design-solution.md) designs one feature against
them. [Draft UI](draft-ui.md) explores a particular screen or interaction.
A project-wide UI design system (tokens, components) is not covered yet.
