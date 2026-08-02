# Tasks: System-docs codebase navigation

Feature code: SDCN
Status: Approved
Date: 2026-08-02
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** First-class modules/ownership/dependencies with design/plan/inspect consult hooks.

**Architecture:** Extend SDOC pack catalog; structural templates/validators; reuse define-system-doc; hooks in plan-tasks, design-solution, inspect-change.

**Tech Stack:** Markdown skills; Python unittest.

## Global Constraints

Same pack verify commands and ARCH-1..6 as SDOC. Hard constraints outrank nav docs. Never auto-invoke define-system-doc.

## File Structure

See design Surfaces / SDOC skill tree under `skills/project/define-system-doc/`, plus plan-tasks, design-solution, inspect-change, guide, tests.

### Task 1: Templates, validators, packages, catalog

Implemented in continuous ship of ROAD-8.

_Requirements: SDCN-1.1, SDCN-1.2, SDCN-1.3, SDCN-1.4, SDCN-1.5, SDCN-1.6, SDCN-2.1, SDCN-2.2, SDCN-2.3, SDCN-7.2, SDCN-8.1, SDCN-8.3_

### Task 2: Reader hooks + guide + tests

Implemented in continuous ship of ROAD-8.

_Requirements: SDCN-3.1, SDCN-3.2, SDCN-3.3, SDCN-3.4, SDCN-3.5, SDCN-3.6, SDCN-3.7, SDCN-4.1, SDCN-4.2, SDCN-4.3, SDCN-4.4, SDCN-5.1, SDCN-5.2, SDCN-5.3, SDCN-5.4, SDCN-6.1, SDCN-6.2, SDCN-7.1, SDCN-8.2, SDCN-8.4_
