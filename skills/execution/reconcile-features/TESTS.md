# `reconcile-features` — freeze reverse-track recipe (v1.0.0)

**Roster:** grok-4.6 (primary), grok-4.5 (weaker).
**Type:** technique / recipe (gate A/B/C/D controls all chose ethics-compliant A under AGENTS.md alone — those are not the failure this skill fixes).
**Scenarios:** `.skills/_pending-reconcile/red-rf-t{1,2,3}-*.md`.

## Failure class

**Complies on ethics, invents incompatible recipes.** Without a skill, both
models refuse to mint CODEs, write Approved SHALLs, or add consuming-repo CI —
AGENTS.md already carries those gates. They still diverge on durable shape:
overlay path, OBS id grammar, checkpoint advance, and envelope schema. A caller
cannot query a stable overlay; the next session cannot find what the last one
wrote.

Form: positive recipe / contract (envelope + on-disk layout + deterministic
passes) + hard prohibitions only for the remaining mint/CI/graph traps.

### RED (no skill)

| Scenario | Model | Shape verdict |
|---|---|---|
| T1 produce envelope | grok-4.6 | Overlay `.skills/reverse-features/` + `OBS-LABL` (proto-CODE id) + `state.json` advanced with unresolved findings |
| T1 produce envelope | grok-4.5 | Overlay `.skills/reconcile/` + `OBS-20260826-01` + freeform `disposition-*.md` — **different root and id grammar** |
| T2 frame after pull | grok-4.6 | `.skills/reverse-features/envelope.yaml`; also said **do not advance checkpoint past unresolved** — conflicts with locked advance-after-index policy |
| T2 frame after pull | grok-4.5 | `.skills/reconcile/disposition-<range>.md` — third spelling of the same artifact |
| T3 brownfield | grok-4.6 | Ad-hoc `.skills/_pending-rate-limit-auth-mail/observations.md` |
| T3 brownfield | grok-4.5 | Ad-hoc `.skills/observations/OBS-rate-limit-auth-mail.md` |

Verbatim shape failures:

- (4.5 T1) "Create `/tmp/mailgate-checkout/.skills/reconcile/checkpoint`" / "`disposition-c0c4e479..58104524.md`"
- (4.6 T2) "Do not advance the checkpoint past unresolved findings."
- (4.6 T3) "Write one read-only OBS candidate under `.skills/_pending-rate-limit-auth-mail/observations.md`"
- (4.5 T3) "`/tmp/opentickly-checkout/.skills/observations/OBS-rate-limit-auth-mail.md`"

Ethics held without the skill (not counted as RED wins for authoring): no CODE
mint, no `docs/specs/**` writes, no CI. Those stay in the skill as Red Flags so
a weaker future model cannot regress, but they are not the reason the skill
exists.

### Locked decisions feeding the recipe (2026-08-26)

1. Overlay root: `.skills/reverse-features/`
2. Checkpoint advances after findings are indexed into active overlay
3. Graphify adapter: deferred entirely for v1

### GREEN (v1.0.0 skill present)

Compliant = overlay root + schema/recipe ids + `OBS-<6hex>` + index-then-advance
+ no CODE/specs/CI.

| Scenario | Model | Choice / shape |
|---|---|---|
| T1 | grok-4.6 | `.skills/reverse-features/`; envelope 1 / rfeat-1.0; `OBS-5682de`; `advanced_to: 58104524`; no CODE/specs/CI |
| T1 | grok-4.5 | same `OBS-5682de` (identical locator hash); same root/schema/advance; `active/labels.md` |
| T2 | grok-4.6 | only `.skills/reverse-features/`; index then advance; no refuse-on-pending |
| T2 | grok-4.5 | same; NEXT_ARTIFACT points at reverse-features tree |

Meta (4.5 T1): hex rule + forbidden proto-CODE row made `OBS-LABL` unavailable;
index-then-advance row blocked the RED checkpoint refusal.

T3 not re-run in GREEN — ethics already held in RED; shape contract covered by T1/T2.

### Description trigger (v1.0.0)

10 queries × grok-4.5 / grok-4.6 — should-fire Q1–Q5 all `reconcile-features`;
should-not-fire Q6–Q10 → `audit-trace`, `load-subgraph`, `map-features`,
`realign-spec`, `root-cause` respectively. No misses either direction on this
held-out set.