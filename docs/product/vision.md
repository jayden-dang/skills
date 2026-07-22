# Product Vision: Skills

Status: Draft
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
ideation to release with requirements as first-class runtime objects.

## Users

- Developers and small teams adopting agentic development on any harness
- Authors of skills who need gates, traceability, and ceremony that survive pressure
- Maintainers packaging this set as a Claude plugin or `npx skills` install

## Goals

- Ship a complete ideation-to-release skill set with requirements traceability as the spine
- Keep gates (NO-CODE, TEST-FIRST, ROOT-CAUSE, EVIDENCE) enforceable under agent pressure
- Stay harness-portable (plain SKILL.md + AGENTS.md), zero runtime vendored into consumer repos
- Make `/setup-repo` configure each consumer repo so skills stop guessing

## Non-goals

- Replacing the consumer app's product code or framework choices
- Bundling linters, CI, or language toolchains into adopting repos
- Building a hosted SaaS control plane for agent runs

## Scope boundaries

- In scope: skills, templates, hooks for this set, agent-facing config, human guide
- Deferred: fill via `/establish-project` as the product deepens
- Hard constraints: pure documentation/skill artifacts; Python linters only for *this* repo's quality
