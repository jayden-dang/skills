# Engineering Guidelines: Skills

Status: Draft
Date: 2026-07-22

<!--
The human-facing engineering rules features must follow — coding standards,
conventions, house rules. Optional. When present, `write-plan` sources the
engineering rules for its Global Constraints from HERE rather than from
`docs/agents/project.md` (which then holds only machine-config + a pointer to this
file). Every heading is a REQUIRED slot — fill it or write `None`.
-->

## Coding standards

- Skill bodies: imperative voice; hard gates in dedicated blocks; rationalization tables in `| Thought | Reality |` form.
- SKILL.md under 500 lines (prefer under 300); split implementer/reviewer prompts into sibling files when needed.
- Python linters for this repo only: frontmatter parse safety, dead handoffs to user-invoked skills, Context7 references on library-reasoning skills.
- No production app code in this repository — content is skills, templates, hooks, and docs.

## Naming and i18n

- Skills: verb-first kebab-case (`write-requirements`, `execute-plan`).
- Feature codes: short uppercase prefix registered in `docs/specs/INDEX.md`.
- Requirement IDs: `CODE-N.M` — never renumber; retire with strikethrough.
- User-facing install docs in English; no i18n pipeline.

## House rules

- Cross-skill references use `REQUIRED SUB-SKILL:` prose, never `@`-links.
- Skill `description` frontmatter states triggering conditions only — never summarize the workflow.
- Additive edits to consumer-facing config: never clobber existing user content when writing templates.
- Pre-push gate (lefthook): frontmatter lint, handoffs lint, context7 lint, full unit suite.
