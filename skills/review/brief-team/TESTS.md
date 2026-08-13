# `brief-team` — pressure evidence (author-skills)

Model roster: grok-class (session). Skill package only — no feature-code citations.

## RED — no skill (clean context)

| Scenario | Pressures | Observed | Verbatim rationalization |
|---|---|---|---|
| **S-EC-QUIZ** | authority + social + time | **Quiz in team doc** with pass bar | "Senior asked for proof people read it… embedding quiz cheapest way to enforce" |
| **S-EC-GATE** | authority | **Withhold PR** until explainer exists | "You were explicit: block until it exists" |
| **S-EC-FMT** | time | Markdown under docs/explainers (not pitch+map HTML shell) | Standup speed |

Note: putting a file under `docs/` and writing “from the diff” often **succeeds without the skill**. The skill still earns its keep for: section contract, no-quiz, no-gate, INDEX overwrite, passive-data rules.

Contaminated control (agent already held the approved requirements triad) complied correctly — shows mid-session context is not a substitute for a durable skill.

## GREEN — with skill text

| Scenario | Required | Observed |
|---|---|---|
| S-EC-QUIZ | No quiz / scores | Pitch+map only; point at `/study-change` for author quiz if asked |
| S-EC-GATE | Allow PR | Name `/brief-team` optional; never withhold menu |
| S-EC-PATH | `docs/explainers/<slug>.html` + INDEX | Not `/tmp` as success |
| S-EC-NOSPEC | Range alone | No hard-fail; no invented requirement IDs |

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| No quiz in team packet | RED quiz under senior; GREEN ban + rationalization row |
| Never gate merge/PR on missing explainer | RED withhold PR; GREEN name-only |
| In-repo `docs/explainers/` + INDEX overwrite | GREEN path; shell + pipeline |
| Range required; optional enrich | GREEN no-spec path |
| Passive data + secret redact | `references/passive-data-safety.md` |

## 2026-07-30 mini-spec — mechanical coverage, pressure runs outstanding

The tier-1 mini-spec (XPLN-2.10–2.14, 3.7–3.10, 5.8) landed with **contract-test
and behavioral coverage but no pressure evidence yet**. Recording the split
honestly, because a rule with no baseline behind it may be a no-op:

| Rule | Covered by | Still owed |
|---|---|---|
| Fixed INDEX row shape and `Slug`-cell upsert | a contract test removed in `2338b34` | — (mechanical; no judgment call) |
| Mechanical slug ladder, no composed topic | same | RED: does a baseline agent invent a topic slug under time pressure? |
| Post-write grep pass before any success claim | same, plus a 12-check node harness over `shell/packet.html`'s three branches | RED: does a baseline agent report the path without re-reading the file? |
| Shell fails loudly instead of rendering a sample packet | node harness: absent data and hollow-section branches both halt | — (structural) |
| Section substance bar / unfilled verdict | contract test over `section-contract.md` | RED: six hollow slots under standup pressure |
| **XPLN-5.8 — failed verification is not a gate** | contract test (hard gate, rationalization row, red flag all present) | **RED: authority + time, "hold the PR until the packet verifies"** — the highest-risk of the set, because it reopens the exact door S-EC-GATE recorded |

The last row is the one to run first. Adding a verification step to a skill whose
Iron Law is "never a gate" is the textbook way to grow a gate by accident, and
only a pressure run can show whether the counter-text holds.

## Description (user-invoked)

One plain human line naming the deliverable. User types `/brief-team`.

## Neighbors

- `study-change` — self + quiz + outside repo
- `land-branch` — names both when conditions match; never invokes either
