# `tour-system`

> Path-verified learning tours over a codebase or capability — atlas, tour,
> journey, or change-impact — with a local ledger instead of a quiz novel.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked — `/tour-system` |
| **Reads** | `docs/specs/INDEX.md`, OBS overlay, git range (change-impact), code/tests |
| **Writes** | `.skills/study/<slug>/` ledger only (gitignored); optional export file outside success-critical paths |
| **Calls** | `load-subgraph` (advisory); names `/configure-repo`, `/map-features`, `/teach-pack`, `/deepen-codebase`, `/study-change` — never auto-invokes them |

## Modes

| Mode | Use when |
|---|---|
| `atlas` | Orient on capabilities (INDEX + OBS) |
| `tour` | Deepen one CODE/path/term via neighbors + ordered stops |
| `journey` | Trace one real user/CLI path end-to-end |
| `change-impact` | Comprehend a **ResolvedRange** (coexists with `/study-change` until retirement gate) |

## Learning rule

No production at every file. **One** graded production when closing a
**semantic checkpoint** or a **journey**: own-words purpose + reachability claim
(+ optional blast), verified with source/test/runtime.

See `skills/discovery/tour-system/SKILL.md` and its `references/`.

## Related

- Catalog build: [`reconcile-features`](reconcile-features.md), [`map-features`](map-features.md)
- Ask-time neighbors: [`load-subgraph`](load-subgraph.md)
- Concept drill: [`teach-pack`](teach-pack.md) (kept)
- Diff HTML quiz packet: [`study-change`](study-change.md) (coexistence until gate)
