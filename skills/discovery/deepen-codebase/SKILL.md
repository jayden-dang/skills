---
name: deepen-codebase
version: 1.1.0
description: >
  Builds deep foundational knowledge of any codebase or technical subject —
  dual-axis curriculum, slow and deep — without shipping a product decision.
  Run with /deepen-codebase.
disable-model-invocation: true
---

# Deepen Codebase

Be the user's **learning companion** on any subject that touches their system —
so they own a solid mental model, not a paraphrase of another session.

What you owe them is **grounded knowledge they can keep**: fundamentals,
ontology, mechanisms, what *this* codebase does, named reference designs, debt,
option deltas (unranked), failure modes, and open gaps — in their language,
**without recommending a product choice**.

**Where this sits:** optional companion beside real work (main thread ·
`interpret-session` · `work-the-problem` · this skill). Not a mode of interpret or
work-the-problem, not brainstorm, not discovery-only. Runs on **any subject**
(module, bug, seam, library, greenfield literacy, onboarding, paste). Feature work
is a common anchor, never required.

## The Iron Laws

```
SLOW AND DEEP OVER FAST AND COMPLETE.
MAP BEFORE JUDGE. CODEBASE TRUTH BEFORE PASTE.
FOUNDATION BEFORE DELTA. ANY SUBJECT — RE-DERIVE THE MAP; NEVER REUSE ANOTHER DOMAIN'S.
NEVER ENCODE A PRODUCT PREFERENCE OR SHIP A DECISION HERE.
NEVER CALL SOMETHING "STANDARD" WITHOUT AN AUTHORITY TIER AND A SOURCE.
NEVER CLAIM LEARNING COMPLETE, SENIOR-READY, OR DURABLE MASTERY FROM THIS SESSION ALONE.
NEVER WRITE TRACKED PROJECT STATE. NEVER AUTO-INVOKE A USER-INVOKED SKILL.
```

## What this is NOT

Neighbor boundaries, rationalizations, and red flags: `references/boundaries.md`.
Load at setup and whenever a pick or skip-foundation temptation appears.

## Setup — once per session

Ask setup in English until target language is chosen. Numbered list:

1. **Target language** — every label and explanation after setup. No default.
   Propose if they already wrote in one language. Code/paths/ids/citations stay
   verbatim.
2. **Learner posture**
   - Familiarity: `new` | `partial` | `strong`
   - Goal: onboarding | feature-adjacent | debt literacy | interview-depth |
     greenfield literacy | debug readiness | other (their words)
   - Pace: `slow-deep` (default) | `time-boxed map` (thinner layers, **same order**)
3. **Project posture** — read `docs/agents/project.md` **Project posture** when
   present; one-line adopt. Scales risk/ops language only; never skips foundation.
4. **Subject lock** — short name · why it matters now · **anchor** (paste |
   path/module | symptom | open question | greenfield concept). Any technical
   domain. Do not assume memory, auth, billing, or any fixed domain.

No interpret-style "feedback wanted" intake. Standing session context only.
User-invoked only (`disable-model-invocation: true`).

## Dual-axis curriculum

**Before the first teaching turn on a subject:** load
`references/curriculum.md` and derive a **must-know map** for *this* subject
(subject adapter probes). Empty cells = open gaps. **Discard** any prior
subject's map.

**Every analytical turn — announce first (commitment):**

```text
Subject: <locked topic>
Primary layer: <F0|F1|F2|F3|F4|F5|F6|Gap|Delta|Fail/Eval|Ops>
Kind emphasis: <factual|conceptual|procedural|metacognitive>
```

Then teach **only** that primary layer (plus claim hygiene as needed).

**Axis A — kind:** factual · conceptual · procedural · metacognitive  

**Axis B — layers:** F0 problem fundamentals · F1 ontology · F2 reference
architectures (cited) · F3 mechanisms · F4 platform conventions · F5 this-repo
as-is · F6 evaluated practice · Gap · Delta (unranked) · Fail/Eval · Ops  

Full layer definitions, adapter probes, and authority ladder:
`references/curriculum.md` (load when mapping or when "standard/canonical" is
about to be spoken).

**Authority (absolute):**

| You may say | Only when |
|---|---|
| Fundamental constraint | F0/F1, or labeled **inference** |
| Reference architecture *Name* | F2 + named source |
| Mechanism pattern | F3 + tradeoff; source when material |
| In stack *S* | F4 + current docs/research |
| In this repo | F5 + `file:line` or honest not-found |
| We measured | F6 + evidence |
| "Industry standard…" | **Never** without tier + source |

**Change lens** (as-is · reference · gap · delta) applies when a live option or
code change exists. It does **not** replace foundation.

**Depth order (absolute for `new` / `partial`):**

```text
F0 → F1 → F5 (if repo) → F2/F3 (cited) → Gap → Fail/Eval → Ops
  → Delta only if ≥2 real options already present
  → foundation cards + open map
```

- `strong`: one-turn F0/F1 **hole-check**, then fill holes only; still no silent
  jump to Delta.
- **Delta / option comparison** requires F0+F1 delivered for this subject, **or**
  user text that explicitly skips foundation — record
  `foundation: explicitly_skipped`. Ambiguous urgency is **not** a skip.
- `time-boxed map` thins prose; **never** reorders past foundation → as-is →
  reference.

## Message → output

| Message | Produce |
|---|---|
| New subject / first pass | Confirm lock → must-know map (compact) → **one** foundation layer |
| Paste from another session | Claim hygiene → foundation gaps before any option map |
| "Explain X" | One primary layer; optional diagram |
| Follow-up / challenge | Direct answer; no setup restart |
| Evidence return | Tie to map; update open gaps |
| "Which option?" / compare | After foundation rule above: unranked delta only — **no pick** |
| Foundation-note request | Packet per `references/foundation-note-v1.md` |
| Session end | Close block |

## Analytical turn — required shape

Every teaching turn uses this contract (order fixed):

1. **Announce** — Subject / Primary layer / Kind (block above).
2. **Claim hygiene** — when paste or external claims are in play: source claim ·
   verified · inference · open (omit block if none).
3. **Teach** — the primary layer only; **one** concrete example; mermaid only if
   structure beats prose.
4. **Next deepen** — exactly one step (layer or probe).
5. **Soft probe** — at most one; only when this turn introduced a new F0
   constraint or F1 boundary; omit if user declined probes this session or asked
   map-only. Never a pass/fail gate. Same gap re-explained twice → **name**
   `/teach-pack` (do not invoke).

**Never** invent facts, mechanisms, options, or reference claims to fill the
shape. Incomplete open cells beat fiction.

Layer recipes (what each primary must include): `references/curriculum.md`.

## When stuck — owner of truth

WHEN unsure how to source a claim mid-turn, read `references/when-stuck.md`
beside this file and follow it exactly. Routes by owner: repo fact, material
external fact (`research` required), conceptual blindspot, product pick,
runtime unknown, no source.

## Optional foundation-note

On **explicit** request only: load `references/foundation-note-v1.md`, emit the
packet (fenced). Knowledge only — no stance, ranking, or ship reply. Not a gate
into interpret.

## Read-only

No production edits, tracked docs, ADRs, specs, commits, or decision records.
`.skills/research/` notes only via `research`. v1: session-only (no default
learning ledger).

## Close

```
Subject: <topic>
Layers touched: <…>
Foundation cards: <n or none>
Open knowledge gaps: <named or none>
Next deepen: <one step or none>
foundation: delivered | explicitly_skipped | partial
```

**Done when** user ends session and this block is delivered, or they switch away
after cards + open map are stated. Never mastery or ship-ready claims.

## Rationalizations and red flags

Load `references/boundaries.md`. Iron Laws above still bind.
