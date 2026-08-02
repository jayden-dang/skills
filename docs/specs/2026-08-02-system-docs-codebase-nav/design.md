# Design: System-docs codebase navigation

Feature code: SDCN
Status: Approved
Date: 2026-08-02
Requirements: ./requirements.md

## Context

SDOC shipped the pack catalog, `/define-system-doc`, structural validators, and plan-tasks Codebase Map hooks. `codebase/modules|ownership|dependencies` remain Recognized. ROAD-8 promotes those three to First-class and adds conditional consult hooks on design-solution, plan-tasks, and inspect-change — reusing the SDOC authority and hard-constraint precedence model.

**Spine:** ARCH-2, ARCH-3, ARCH-5, ARCH-4.

## Decisions

1. Reuse define-system-doc + structural validator pattern from SDOC; no new author skill.
2. Authority per file: Status Approved + entry structural validator (same as map).
3. Hard constraints outrank all navigation docs (same precedence as map).
4. Readers: plan-tasks, design-solution, inspect-change — each with full reader tests.
5. Inventory stays 36 keys; only maturity and packages change for the three entries.

## Architecture

### Templates and validators for three entries

Satisfies: SDCN-1.1, SDCN-1.3, SDCN-1.4, SDCN-1.5, SDCN-1.6
Reuse: rung 2 — extend SDOC map template/validator pattern
Respects: ARCH-3
Interface: template + validate_*(text)->pass|fail per entry
Depth: Structural checks only.
Locality: create under define-system-doc templates/validators/codebase/

**modules** slots: Purpose; Module inventory table (name|path|responsibility) or None; Boundaries; Not feature registry disclaimer; Status.

**ownership** slots: Purpose; Ownership table (path-or-module|owner) or None; Notes; Advisory-only disclaimer; Status.

**dependencies** slots: Purpose; Allowed dependency directions (from|to|rule) table or None; Forbidden edges or None; Not runtime enforcer disclaimer; Status.

### Entry packages and catalog maturity

Satisfies: SDCN-1.2, SDCN-7.2
Reuse: rung 2 — CATALOG.md
Interface: maturity First-class when package complete
Locality: update three entry packages + CATALOG rows

### define-system-doc (no body fork)

Satisfies: SDCN-2.1, SDCN-2.2, SDCN-2.3, SDCN-8.1
Reuse: rung 2 — existing SKILL.md (generic First-class entries)
Interface: invoke with entry key
Locality: leave skill procedure; ensure packages point at new templates

### plan-tasks navigation hooks

Satisfies: SDCN-3.1–3.7, SDCN-8.2
Reuse: rung 2 — extend Codebase Map consult section
Respects: ARCH-2, ARCH-5
Interface: per-entry authority + consult/suggest/conflict
Locality: plan-tasks SKILL.md

### design-solution navigation hooks

Satisfies: SDCN-4.1–4.4
Reuse: rung 2 — design-solution Step 1/2
Respects: ARCH-2, ARCH-5
Interface: when designing cross-module structure, consult Approved modules/dependencies
Locality: design-solution SKILL.md

### inspect-change navigation hooks

Satisfies: SDCN-5.1–5.4
Reuse: rung 2 — inspect-change context collection
Respects: ARCH-2, ARCH-5
Interface: when diff paths hit nav surfaces, load Approved docs as review context
Locality: inspect-change SKILL.md

### Guide

Satisfies: SDCN-6.1, SDCN-6.2
Reuse: rung 2 — system-docs.md
Locality: docs/guide/concepts/system-docs.md

### Pack tests

Satisfies: SDCN-8.3, SDCN-8.4, SDCN-7.1
Verification for: all First-class and reader criteria
Reuse: rung 2 — extend test_sdoc or new test_sdcn_*.py

## Seams for testing

| Seam | Kind | Covers |
|---|---|---|
| templates/validators + fixtures | unit | SDCN-1.1, 1.3–1.5 |
| CATALOG First-class ×3 | unit | SDCN-1.2, 1.6, 7.2, 8.3 |
| define-system-doc package pointers | unit | SDCN-2.1–2.3, 8.1 |
| plan-tasks nav section | unit | SDCN-3.*, 8.2 |
| design-solution nav section | unit | SDCN-4.* |
| inspect-change nav section | unit | SDCN-5.* |
| guide sync | unit | SDCN-6.* |
| advisory ownership disclaimer | unit | SDCN-7.1 |
| no TB/SLO claim | unit | SDCN-8.4 |

## Coverage check

Every SDCN-* ID has exactly one primary Satisfies section above.
