# Engineering standards index

Status: Approved
Date: 2026-08-02

## Purpose and boundary

Canonical engineering standards for this repository (skill-set authoring and pack quality).

## Standards catalog

| Document | Path | Scope |
|---|---|---|
| Testing | `docs/standards/testing.md` | Test-first, suite commands, mock boundaries |
| Errors and logging | `docs/standards/errors-logging.md` | Error and log conventions for pack tooling |
| Coding / naming / house rules | *(this INDEX)* | Skill authoring standards formerly in guidelines |

## Coding standards

- Skill bodies: imperative voice; hard gates in dedicated blocks; rationalization tables in `| Thought | Reality |` form.
- SKILL.md under 500 lines (prefer under 300); split implementer/reviewer prompts into sibling files when needed.
- Python linters for this repo only: frontmatter parse safety, dead handoffs to user-invoked skills, Context7 references on library-reasoning skills.
- No production app code in this repository — content is skills, templates, hooks, and docs.
- Deterministic checks driven by an LLM (fixed `grep`/`git` under a precise skill) are a first-class form — do not replace them with freeform judgment when a set-difference will do.
- **Comments (default zero):** write no new comments unless a future editor would mis-change behavior without them.
- **No process IDs in code:** do not embed `CODE-N.M` or feature codes in application source, test titles, or commits; IDs live in `docs/specs/**`.

## Naming and i18n

- Skills: verb-first kebab-case (`specify-behavior`, `build-in-waves`).
- Feature codes: short uppercase prefix registered in `docs/specs/INDEX.md`.
- Requirement IDs: `CODE-N.M` — never renumber; retire with strikethrough.
- Architecture invariants: `ARCH-N` — same immutability rules; cite as `Respects: ARCH-N` from feature `design.md`.
- User-facing install docs in English; no i18n pipeline.

## House rules

- Cross-skill references use `REQUIRED SUB-SKILL:` prose, never `@`-links.
- Skill `description` frontmatter states triggering conditions only — never summarize the workflow.
- Additive edits to consumer-facing config: never clobber existing user content when writing templates.
- Skills never invent project configuration — they read `docs/agents/` (or stop and suggest `/configure-repo`).
- Iron Law gates (NO-CODE, TEST-FIRST, ROOT-CAUSE, EVIDENCE) are not weakened by workflow band, ceremony tier, or convenience.
- Pre-push gate (lefthook): frontmatter lint, handoffs lint, context7 lint, full unit suite.

## Source of truth rule

Canonical engineering standards live under `docs/standards/`. `docs/product/guidelines.md` is a **pointer only**. Never maintain parallel SSOTs.

## Not ARCH-N

Standards docs do **not** redefine greppable `ARCH-N` architecture invariants.
