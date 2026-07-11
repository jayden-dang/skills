# EARS reference

EARS — the **Easy Approach to Requirements Syntax** — is a small constrained grammar for acceptance criteria. It exists to make a requirement mean exactly one thing.

Every acceptance criterion in a `requirements.md` uses one of five forms, and carries a [hierarchical ID](../concepts/requirement-ids.md).

## The five forms

| Form | Pattern | Use when |
|---|---|---|
| **Event-driven** | `WHEN <event> THE SYSTEM SHALL <behavior>` | something happens and the system must respond |
| **State-driven** | `WHILE <state> THE SYSTEM SHALL <behavior>` | a behavior holds for the duration of a state |
| **Unwanted behavior** | `IF <unwanted condition> THEN THE SYSTEM SHALL <behavior>` | error handling, invalid input, failure modes |
| **Optional feature** | `WHERE <feature is included> THE SYSTEM SHALL <behavior>` | behavior that exists only when a feature is enabled |
| **Ubiquitous** | `THE SYSTEM SHALL <behavior>` | an always-true invariant |

And one extension this skill set adds:

| Form | Pattern | Use when |
|---|---|---|
| **Guard** | `(guard) WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing behavior>` | protecting existing behavior the feature touches |

## Worked examples

```markdown
# Requirements: Module Shell

Feature code: SHELL
Status: Approved

## 1. Module switching

**Story:** As a user, I want a left icon rail so I can switch modules.

- **SHELL-1.1** WHEN the app starts with no persisted module THE SYSTEM SHALL
  activate the Notes module.
- **SHELL-1.2** WHEN the user selects a module THE SYSTEM SHALL persist the
  selection and restore it on next launch.
- **SHELL-1.3** (guard) WHEN the user switches modules THE SYSTEM SHALL
  CONTINUE TO preserve unsaved editor state.
- **SHELL-1.4** IF the persisted module id does not match any installed module
  THEN THE SYSTEM SHALL activate the Notes module and log a warning.
- **SHELL-1.5** WHILE a module is loading THE SYSTEM SHALL disable the rail.
- **SHELL-1.6** WHERE the developer-tools flag is enabled THE SYSTEM SHALL
  show a Debug module in the rail.
- **SHELL-1.7** THE SYSTEM SHALL render exactly one active module at a time.
```

## The rules that make it work

### One observable behavior per criterion

> If a sentence needs "and", it is usually two criteria.

`SHELL-1.2` above is borderline — "persist the selection **and** restore it on next launch" — and it survives only because persist-then-restore is one round-trip behavior a single test can observe. Split it the moment a test would need two assertions in two different runs.

The reason is mechanical, not aesthetic. A criterion is the unit a test tag points at. If `SHELL-1.2` names two behaviors, a test tagged `@SHELL-1.2` proves one of them and `check-trace` reports the requirement as covered.

### Every criterion must be independently verifiable

`write-requirements` runs a **testability scan** before the approval gate: *can each criterion be verified by an automated test or a concrete manual check?* Rewrite any that cannot.

This is what rules out the criteria people reach for by habit:

| Not a criterion | Why | Instead |
|---|---|---|
| "THE SYSTEM SHALL be fast" | Unverifiable | "WHEN the rail is clicked THE SYSTEM SHALL render the module within 100 ms" |
| "THE SYSTEM SHALL handle errors appropriately" | A placeholder | An `IF … THEN` criterion per error condition |
| "THE SYSTEM SHALL be user-friendly" | Not a behavior | Delete it, or name the behavior you mean |

### Ambiguity is resolved before approval, not after

The **ambiguity scan**: *could any criterion be read two different ways? Pick one reading and write it in.*

"WHEN the user selects a module THE SYSTEM SHALL persist the selection" — persist where? For how long? Across a reinstall? The criterion is approved, and then an implementer answers those questions by guessing, and the answer is now in the code and not in the spec.

### Code claims get verified against the code

If any criterion asserts how the system *currently* works — a data format, an existing behavior, a constraint — `write-requirements` dispatches a **review subagent** to check each such claim against real code, citing `file:line`.

The skill names the failure it is preventing: a criterion saying "the body is ProseMirror-JSON" when it is actually Markdown poisons the design, the plan, and the code that follows.

## Guards deserve their own section

A guard requirement is the only thing standing between an agent and load-bearing behavior nobody mentioned.

```markdown
- **SHELL-1.3** (guard) WHEN the user switches modules THE SYSTEM SHALL
  CONTINUE TO preserve unsaved editor state.
```

Three things follow from that ID existing:

1. Some task must cite it in a `_Requirements:_` footer.
2. Some test must be tagged with it, or `check-trace` reports **E2** once the feature is `Implemented`.
3. The commit that touches the behavior carries `Guards: SHELL-1.3`, and `release` files it under **Protected behavior** in the changelog.

`write-requirements` will not accept an empty guard section by default. Its completion criterion for that step:

> You have **actively searched** the touched surface for behaviors to guard — not merely found none by default.

Guards are also how a tier-1 bugfix becomes a spec: one fix requirement plus one guard *is* the whole mini-spec. See [Ceremony tiers](../methodology/ceremony-tiers.md).

## ID immutability

Once `Status: Approved`, a criterion's ID never changes meaning and is never renumbered. Retire it by strikethrough:

```markdown
- ~~**SHELL-1.2**~~ superseded by SHELL-1.8
```

`check-trace` treats a struck-through ID as **undefined**, so every test and task still citing it surfaces immediately as an E1 error. Retirement cannot happen quietly.

## Out of Scope is part of the spec

Not an EARS form, but it lives in the same file and it is read by three later skills:

```markdown
## Out of Scope

- Keyboard shortcuts for module switching — deferred; the rail is pointer-only in v1.
- Reordering modules in the rail.
```

[`code-review`](../skills/code-review.md)'s Spec axis reads it to identify scope creep. [`dogfood`](../skills/dogfood.md) turns each entry into a *deliberate non-behavior* the tester checks does **not** happen. And [`check-graph`](scripts.md#check-graph) harvests it into the feature's summary card, so a future `brainstorm` on an adjacent idea sees what this feature already declined.

## See also

- [Requirement IDs](../concepts/requirement-ids.md) — the grammar the IDs use
- [`write-requirements`](../skills/write-requirements.md) — the skill that writes these
- [Templates](templates.md) — the `requirements.md` seed
- [Specification phase](../process/specification.md) — where this fits in the chain
