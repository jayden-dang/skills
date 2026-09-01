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
| **Version** | 1.1.0 |

## Modes

| Mode | Use when |
|---|---|
| `atlas` | Orient on capabilities (INDEX + OBS); without INDEX, tree signals only — no invented CODEs |
| `tour` | Deepen one CODE/path/term via neighbors + ordered stops |
| `journey` | Trace one real user/CLI path end-to-end |
| `change-impact` | Comprehend a **ResolvedRange** (coexists with `/study-change` until retirement gate) |

Named surface without a mode → short atlas, then one journey/tour on that surface.

## Learning rule

No production at every file. **One** graded production when closing a
**semantic checkpoint** or a **journey**: own-words purpose + reachability claim
(+ optional blast), verified with source/test/runtime.

If `.skills/` is not gitignored: warn once and name `/configure-repo` — do not
silently patch the consumer `.gitignore`.

See `skills/discovery/tour-system/SKILL.md` and its `references/`.

## Related

- Catalog build / reverse + dispose: [`map-features`](map-features.md)
- Ask-time neighbors: [`load-subgraph`](load-subgraph.md)
- Concept drill: [`teach-pack`](teach-pack.md) (kept)
- Diff HTML quiz packet: [`study-change`](study-change.md) (coexistence until gate)
