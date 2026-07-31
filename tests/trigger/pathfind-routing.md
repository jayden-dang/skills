# pathfind — user discovery / routing notes

`pathfind` is **user-invoked** (`disable-model-invocation: true`). The agent
never auto-loads it from description keywords. Discovery is:

1. User types `/pathfind` or the skill name  
2. `ask-me-bro` / teach-pack **names** `/pathfind` for multi-session fog  
3. AGENTS.md inventory

## should-suggest `/pathfind` (ask-me-bro / agent advice)

- “This effort is too big for one session and we still don’t know the route”
- “Chart a decision map before we spec”
- “Multi-session fog / pathfind this platform rethink”
- “wayfinder-style decision tickets but in our pack”

## should-not-suggest pathfind (near misses)

| Query | Prefer |
|---|---|
| “Fix the null crash in checkout” | `root-cause` |
| “Recolor the button” / typo | tier 0 / `amend-feature` / `test-first` |
| “Write requirements for auth — we already decided everything” | `frame-change` → `specify-behavior` |
| “Publish these agreed stories as issues” | `/publish-issues` |
| “Plan milestones for the product” | `plan-milestones` / `/define-project` |
| “Grill me on this feature” (single session, clear scope) | `clarify-decisions` / `frame-change` |

## Description (user-facing, not routing keywords)

Plain line naming the deliverable only, e.g.:

> Chart or advance a multi-session decision map until the route to a destination is clear.

No Chart/Work step summary in frontmatter (PFIND-1.3).
