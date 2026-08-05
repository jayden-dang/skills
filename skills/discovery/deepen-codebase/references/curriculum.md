# Curriculum — dual axis (any subject)

Load when: choosing depth order, building a must-know map for a new subject, or
checking whether a turn invents "canonical" claims.

## TOC

1. Axes (quick)
2. Subject adapter — derive a must-know map
3. Default depth order
4. Change lens (four comparison layers)
5. Authority ladder
6. Worked sketches (illustrative only — never hard-code as the skill's domain)

---

## 1. Axes (quick)

**Axis A — kind:** factual · conceptual · procedural · metacognitive  
**Axis B — layer:** F0 fundamentals · F1 ontology · F2 reference architectures ·
F3 mechanisms · F4 platform conventions · F5 repo as-is · F6 evaluated practice ·
Gap · Delta · Fail/Eval · Ops

A good turn fills **one primary Axis B layer** and is honest about which Axis A
kinds it actually built.

---

## 2. Subject adapter — derive a must-know map

For **every** new subject, answer these probes *in this subject's vocabulary*
before deep teaching. Do not import a checklist from another domain.

| Probe | Fills |
|---|---|
| What problem does this exist to solve? What goes wrong if it is absent or wrong? | F0 |
| What are the 5–12 terms experts use? Which pairs are commonly collapsed by mistake? | F1 |
| What is the happy-path sequence (step by step) when the system works? | F3 procedural |
| What state is stored, where, and who owns the write path vs the read path? | F1 + F3 |
| What are the hard constraints (consistency, latency, security, scale, human factors)? | F0 + Ops |
| What named external designs or papers do practitioners use as *lenses* (not gospels)? | F2 |
| What does **this** repo/docs/runtime actually do? | F5 |
| How would you detect a wrong mental model (test, probe, production signal)? | Fail/Eval |
| If option X lands, what technical surfaces move? | Delta |

**Output of the adapter:** a compact must-know map (bullet cells). Empty cells
are open knowledge gaps — teach toward them; do not invent filler.

Greenfield (no repo): F5 may be "none yet — design literacy only"; still run
F0/F1/F3 before comparing design options.

---

## 3. Default depth order

Matches SKILL.md Iron path:

```text
slow-deep / time-boxed (same order; time-boxed only thins prose):
  F0 → F1 → F5 (if repo) → F2/F3 (cited) → Gap → Fail/Eval → Ops
  → Delta only if ≥2 real options already present
  → foundation cards + open map
```

Familiarity `strong`: one-turn F0/F1 hole-check; fill holes only.  
Familiarity `new` / `partial`: never open Delta without F0+F1 delivered **or**
user-recorded `foundation: explicitly_skipped`. Urgency ≠ skip.

---

## 4. Change lens

When a live product/design option exists (often from a parallel session):

1. Finish or explicitly skip foundation the learner lacks  
2. **As-is (F5)** for surfaces the option touches  
3. **Reference (F2/F3)** for the *class* of problem — cited  
4. **Gap** intentional vs debt  
5. **Delta** unranked before/after table — no pick  

The four layers do **not** replace F0/F1/Fail/Ops.

---

## 5. Authority ladder

| Speech | Allowed when |
|---|---|
| "Fundamental constraint…" | F0/F1, generally accepted in the discipline, or labeled inference |
| "Reference architecture X (source)…" | F2 with paper/docs URL or citation |
| "Common mechanism pattern…" | F3 + tradeoff; source when material |
| "In stack S the docs say…" | F4 + current docs (Context7 / research) |
| "In this repo…" | F5 + `file:line` or honest "not found" |
| "We measured…" | F6 + evidence |
| "Industry standard is…" | **Forbidden** without tier + source |

---

## 6. Worked sketches (illustrative only)

These show **shape**, not the skill's fixed curriculum. Replace entirely for
other subjects.

### Sketch A — "Session" inside a hypothetical AI memory system

*Only an example of how a must-know map looks.*

| Layer | Example content |
|---|---|
| F0 | Finite context; persist ≠ quality recall; isolation is load-bearing |
| F1 | session ≠ turn ≠ actor ≠ working buffer ≠ long-term fact |
| F3 | start → append events → compact? → end → extract? |
| F2 | CoALA working vs LTM modules; MemGPT main vs external context (cite papers) |
| F5 | *(whatever the repo defines)* |
| Fail | cross-tenant leak; bad resume; summary drift |
| Delta | if "add memory": session schema / lifecycle changes — describe only |

### Sketch B — "Idempotency" in a payments API

| Layer | Example content |
|---|---|
| F0 | Networks retry; double-charge is catastrophic |
| F1 | idempotency key ≠ request id ≠ transaction id ≠ at-least-once delivery |
| F3 | client key → server store → replay safe response → TTL/conflict rules |
| F2 | HTTP idempotency patterns; provider docs (Stripe-style keys) as F4 if used |
| F5 | middleware, storage table, key scope |
| Fail | key reuse across different bodies; TTL too short; partial commit |
| Ops | storage growth, multi-region key visibility |

### Sketch C — "Authn vs authz" onboarding a brownfield app

| Layer | Example content |
|---|---|
| F0 | Identity proof vs permission; confuse them → broken threat model |
| F1 | authentication ≠ authorization ≠ session cookie ≠ API token ≠ role ≠ policy |
| F3 | login → token/session issue → request path checks permission |
| F2 | OAuth2/OIDC roles as F2/F4 when applicable — cite RFCs/docs |
| F5 | middleware order, role tables, route guards |
| Fail | IDOR, confused deputy, missing check on one route |

When the user's subject is none of the above, **discard these tables** and run
the subject adapter probes only.
