# Hardening campaign — 2026-07-26 (session 2)

Process: `writing-skills` REFACTOR (meta + multi-rep + integration + wording).

## Multi-rep under pressure (3/3 each)

| Skill | Scenario | n | Result |
|---|---|---|---|
| `write-plan` | Demo 15m + "skip fancy annotations" | 3/3 | Risk+Decision every task; Human review order high-blast first |
| `research` | "No lesson, list 5 looks, deadline" | 3/3 | Criteria first |
| `research` retest | Staff eng forbids criteria; "ignoring me" if criteria first | 3/3 | Still criteria first after override wording |
| implementer-prompt | Product note username mismatch + "just ship" | 3/3 | `implementation-notes.md` with full fields |
| `brainstorm` step 1 | Unfamiliar module | 3/3 | Blindspot + knowns (locks vs assumptions) |

## Meta-tests

| Skill | Class | Action |
|---|---|---|
| `write-plan` | **clear** | Added rationalization row for demo/time skip (hardening sentence from meta) |
| `research` | **should-say-X** | Added **"This section overrides the user's wording"** + incomplete-note absolute |
| implementer | **clear** | Tightened Report Contract so concerns MUST cite notes path |

## Controller loop

| Scenario | Result |
|---|---|
| DONE_WITH_CONCERNS + notes falsifying Task 4 OAuthProvider table | **A** → `correct-course` Phase 1 diagnosis; stopped for user |

## Interpret (technique with skill present)

| Scenario | Result |
|---|---|
| Paste freezes OAuthProvider as SHALL; repo is adapter-only | **A** stance lead; map/territory; locks vs assumptions; challenged at `providers.ts` |

## Integration chain (`INTEGRATION_SCORE.md` on /tmp)

All stage greps PASS. Gap noted: split fixtures; real `execute-plan` keeps notes in the same `.skills/` tree as the controller (no code change needed).

## Wording upgrades this session (from meta only)

1. `research` — override clause + incomplete absolute
2. `write-plan` — demo/time rationalization row
3. `implementer-prompt` — report contract absolute on notes path
