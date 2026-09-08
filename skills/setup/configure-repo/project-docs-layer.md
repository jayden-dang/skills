# Project-docs layer recipe

Load this file **only when Decision I (Project-docs layer) is offered**.

Explainer: large or long-lived projects can add an optional repo-level layer above the feature workflow — a product vision (`docs/product/vision.md`), an IDed architecture-invariant spine (`docs/architecture/`), and engineering guidelines (`docs/product/guidelines.md`), all authored by `define-project`. When these exist, `frame-change`, `design-solution`, `plan-tasks`, `build-in-waves`, and `inspect-change` consult them; when they do not, nothing changes. Small repos should decline — it can be added later with `/define-project`.

If **Yes**: note it for Step 4 (seed the three docs + the Agent-skills line). If `docs/agents/project.md` or an existing `CLAUDE.md`/`AGENTS.md` already carries engineering guidelines, offer to migrate them into `docs/product/guidelines.md`, leaving a pointer behind.
