# Product Vision: Skills

Status: Approved
Date: 2026-07-22

<!--
The repo-level north star: WHAT this project is and for whom, above any single
feature. Optional — only large/long-lived projects need it. `brainstorm` reads it
to check a new idea's scope; it never gates. Keep each section tight; every heading
is a REQUIRED slot — fill it or write `None`.
-->

## Problem

LLM agents are stochastic: intent evaporates on compaction, agents rationalize past
their own rules, "done" gets claimed without evidence, and unit tests go green while
the feature is broken. Teams lack a single portable skill set that carries work from
ideation to release with requirements as first-class runtime objects — enforced by
deterministic primitives the agent already has (`grep`, `git`, file reads), not by
vendored toolchains.

## Users

- Developers and small teams adopting agentic development on any harness
- Authors of skills who need gates, traceability, and ceremony that survive pressure
- Maintainers packaging this set as a Claude plugin or `npx skills` install

## Goals

- Ship a complete ideation-to-release skill set with requirements traceability as the spine
- Keep gates (NO-CODE, TEST-FIRST, ROOT-CAUSE, EVIDENCE) enforceable under agent pressure
- Stay harness-portable (plain SKILL.md + AGENTS.md) and LLM-native: enforcement is skill-specified `grep`/`git` passes, not bundled linters
- Make `/setup-repo` configure each consumer repo once so skills stop guessing (tracker-agnostic)
- Keep ceremony proportional (tiers 0–2) so trivial changes do not require pages of spec

## Non-goals

- Replacing the consumer app's product code or framework choices
- Bundling linters, CI, or language toolchains into adopting repos as a mandatory path
- Building a hosted SaaS control plane for agent runs
- A mandatory headless (agent-free) merge gate — teams that want one opt into a documented CI job outside the default path
- Perfect feature-overlap detection — neighbor search is advisory best-effort, never a hard gate

## Scope boundaries

- **In scope:** skills, templates, hooks for this set, agent-facing config (`docs/agents/`), optional project-docs layer (`docs/product/`, `docs/architecture/`), human guide, this repo's own quality linters/tests for skill authoring
- **Deferred:** multi-harness packaging polish beyond Claude plugin + skills.sh; optional hard CI gate recipes as first-class product surface; deep multi-team collaboration rituals beyond Team packaging bands
- **Hard constraints:** pure documentation/skill artifacts for adopters (zero mandatory executable vendored into consumer repos); Python linters only for *this* repo's skill-set quality; Iron Law gates are never weakened by workflow band, ceremony tier, or convenience
