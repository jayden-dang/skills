# Testing standards

Status: Approved
Date: <YYYY-MM-DD>

## Purpose and boundary

<What this standards document covers. Or: None — <reason>>

## Strategy

| Layer | Purpose | When required |
|---|---|---|
| unit | <purpose> | <when> |
| integration / e2e | <purpose> | <when> |

Or: `None — <reason>`

### Verification scope (when the project uses selective checks)

| Change or input | Behavior and layer | Project command reference | When to widen |
|---|---|---|---|
| <source, fixture, contract, configuration> | <observable outcome and test layer> | <heading in docs/agents/project.md> | <unknown impact, shared input, or other trigger> |

If the project chooses a feedback target, state the workload, runner and
measurement interval. Cite the observed baseline separately. Use the repo's
own test runners and names.

## Test-first rules

- <rule, e.g. no production code without a failing test first>

Or: `None — <reason>`

## Mocks and boundaries

- <what may be mocked>

Or: `None — <reason>`

## Not a substitute for acceptance

Unit conventions here do not replace `validate-feature` / e2e acceptance.

