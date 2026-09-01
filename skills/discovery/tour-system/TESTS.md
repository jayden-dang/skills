# `tour-system` — system learning tours (v1.1.0)

**Roster:** grok-4.5 (weaker), grok-4.6.  
**Scenarios:** `.skills/_pending-tour-system/red-scenarios.md`.  
**Type:** technique / recipe (with gates against prose-quiz and fake graphs).

## Failure class

**Wrong learning shape.** Without this skill, agents (and the prior
`study-change` / `teach-pack` surfaces the user rejected for system learning)
default to long prose and/or quiz Q&A, skip path-verified reachability, invent
persisted graphs, or auto-run teaching remediation. They do not produce an
ordered tour + honest ledger over INDEX/OBS/ask-time subgraphs.

### RED (no skill / wrong skill / pre-1.1.0 wording)

| Scenario | Observed / expected non-compliant shape |
|---|---|
| T-ATLAS — learn OSS fast | README paraphrase; no INDEX/OBS atlas; no stops |
| T-TOUR — explain one CODE | Chat wall; skip load-subgraph; demonstrated without evidence |
| T-JOURNEY — trace CLI | Per-file quiz; load-subgraph as proof |
| T-CHANGE — dirty worktree | study-change-like quiz HTML; invent range; no hard-stop |
| T-HAND — wrong claim | Auto teach-pack / inline remediation |
| T-IGNORE — `.skills` not ignored (dogfood open-code-review @ 89ec55b) | Silently patch consumer `.gitignore`; skip naming `/configure-repo` |
| T-CODE — no INDEX | Invent Feature CODEs from `internal/agent` folder names |
| T-MODE — "just run it" + named CLI | Prose dump; skip atlas; no journey stops |

Verbatim pressures to counter (from red-scenarios.md + dogfood): "chat is
faster"; "load-subgraph proved it"; "quiz each file"; "write GRAPH.md"; "run
teach-pack for them"; "mark demonstrated — they got it"; "I'll fix gitignore
while I'm here"; "mint CODE from the folder".

### GREEN (v1.1.0 skill present)

Compliant shape:

- Mode explicit: atlas | tour | journey | change-impact (or named-surface default:
  atlas then one journey/tour)
- Ordered path stops; ledger under `.skills/study/`
- One graded production only at semantic checkpoint / journey close
- Claims verified with source/test/runtime; load-subgraph advisory only
- Handoff = name-only + one capsule route
- change-impact uses ResolvedRange hard-stops; export opt-in with privacy denylist
- study-change / teach-pack named when appropriate — never auto-invoked; not deleted
- Missing `.skills` ignore → warn + name `/configure-repo`; no silent `.gitignore` edit
- No INDEX → tree atlas only; no invented CODEs

**Dogfood note (2026-08-27):** open-code-review journey closed with path cites;
pre-1.1.0 run had patched `.gitignore` — that path is now a red flag / rationalization
row. Re-runs must warn + name configure-repo instead.

### Description trigger (hold-out style)

**should-fire:** "learn this codebase", "tour the system", "how does REVW connect",
"trace the review CLI", "what does this diff mean for features", "onboard to
open-code-review via capabilities".

**should-not-fire:** quiz HTML for a ship range → `study-change`; graded concept
drill → `teach-pack`; dispose OBS → `map-features`; reverse-track only →
`/map-features` (user-run); ask-time neighbors alone → `load-subgraph`.
