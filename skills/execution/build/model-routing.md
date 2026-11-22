# Model routing

The model and reasoning effort for every session and subagent this skill set opens: `shape`'s peers
and advisor, the `/go` build session, and `build`'s implementers and reviewers. Read the role's row,
in the column of the harness **this** session runs in, and pass both values on the launch or dispatch.

## Roles

| Role | Codex | Claude Code |
|---|---|---|
| `work` (shape: frame through `tasks.md`) | `gpt-6.2-sol` high | `opus` high |
| `interpret` (shape: forks and spec review) | `gpt-6.2-sol` high | `opus` high |
| `advisor` (shape step 8) | `gpt-6.2-sol` medium | `sonnet` medium |
| `build` session (`/go` controller, shape `--go`) | `gpt-6.2-sol` medium | `sonnet` medium |
| implementer | `gpt-6.2-sol` medium | `sonnet` medium |
| implementer, task touching 4+ files or a refactor | `gpt-6.2-sol` high | `sonnet` high |
| implementer, one-file mechanical change (rename, transcription) | `gpt-6-luna` low | `haiku` low |
| task reviewer, fixer | `gpt-6.2-sol` medium | `sonnet` medium |
| reviewer of a diff touching auth, signatures, concurrency or a migration | `gpt-6.2-sol` high | `sonnet` high |
| whole-branch review (close step 1) | `gpt-6.2-sol` high | `sonnet` high |
| acceptance drive, UI walk, reading screenshots | `gpt-6.1-terra` medium | `sonnet` medium |
| log summary, classification, transcription | `gpt-6-luna` low | `haiku` low |
| PR text, ticket comments, docs | `gpt-6.2-sol` low | `sonnet` low |

A dispatch that fits two rows takes the higher one. The row is the default: an override comes from
the operator's flag (`--work=codex-gpt-6.2-sol@high`, `--build=claude-sonnet@medium`), then the
`Model routing:` line in `docs/agents/project.md` (`work=opus@high, advisor=haiku@low`), then this table.

## Raising costs money: only the operator raises

Order, low to high. Codex: `gpt-6-luna` < `gpt-6.1-terra` < `gpt-6.2-sol` < `gpt-6.2-astra`.
Claude: `haiku` < `sonnet` < `opus` < `claude-fable-5-2`. Effort: low < medium < high < xhigh < max.

- **At or below the role's row** (a cheaper model, a lower effort): take it, ask nobody.
- **Above the row** (a stronger model, or more effort on the same one): only on the operator's word,
  meaning their own flag or the `Model routing:` line in `project.md`. Without it, run the row. Then put
  the raise you would make on the operator's list, one line: role, from → to, why, and that it costs more.
  That list is the reply when they are at the keyboard, and `Needs a decision before merge` in the PR when
  they are not. Wait for a yes before you use it.

Baseline controllers raised on their own and asked nobody: one Sonnet build put five dispatches on Opus
("I would not ask for any of these"), and one Codex build put the security task, its review and the
whole-branch review on `gpt-6.2-astra` high ("no separate approval gate"). The operator pays for that.

A raise is worth putting on the list when: the role came back BLOCKED at its row twice; the spec changes
an `ARCH-N` invariant or migrates persisted data; or `root-cause` has failed three fixes. The raise is
`gpt-6.2-astra` high (xhigh for architecture or a system trade-off) on Codex. On Claude it is `opus` at a
medium row, and `claude-fable-5-2` high for architecture, a system trade-off or deep research. A Mythos
model runs only when the operator names it.

## Launching

| | Codex | Claude Code |
|---|---|---|
| peer or build session | `spawn_agent` with `model` and `reasoning_effort` | `claude --model <m> --effort <e>` |
| subagent | `spawn_agent` with `model` and `reasoning_effort` | `Agent`: the row's effort in `effort`; the model in `model` where the tool lists that parameter, else an agent type whose definition runs that model. A value the tool cannot carry → say so in the report |
| check a value before a run | `codex exec -m <m> -c model_reasoning_effort=<e> --skip-git-repo-check "ok"` | `claude -p --model <m> --effort <e> "ok"` |

A value for the other harness's vendor (`codex-…` typed in Claude Code, `claude-…` in Codex) stops the
run, naming it: sessions run on the harness the operator typed in. A check that fails stops the run, naming it.
