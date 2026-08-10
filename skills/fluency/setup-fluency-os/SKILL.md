---
name: setup-fluency-os
description: Install or remap a fluency practice vault — config, profile, capability map, lexicon, error log, and dashboard.
disable-model-invocation: true
---

# Setup Fluency OS

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Contract

Setup leaves six files and seven directories, every one of them structured so the **other
twelve skills can read it**. They address the vault by exact key path and exact column name,
so the structure comes from `templates/fluency-os/` verbatim — values are the learner's, names
are not negotiable. Setup is finished when the contract check passes with zero misses, not
when the files look right.

## Recipe

1. Confirm the vault root with the learner. Existing folder of notes → map their folders to roles; greenfield → propose the shape below and get consent before creating anything.
2. **REQUIRED before writing anything: read `vault-contract.md` beside this file, and open each template in `templates/fluency-os/`.** Every file below is that template with values filled in. Renaming a key, re-nesting it, or changing its unit produces a vault the readers cannot see — and they fail silently, doing nothing rather than erroring.
3. Interview for `config.md`. Every value comes from the learner or is the template default, marked `(default)`. Nothing about the target language, the accent, or the level framework is inferred from who the learner appears to be. Extra keys of your own are safe; changed ones are not.
4. Seed `capability-map.md` **complete for `languages.target`**: grammar `G-*`, communicative functions `F-*`, phonology `P-*`, covering everything the learner needs up to the ceiling in `cycle.benchmarks` — or, with no benchmark named, up to advanced everyday plus their professional domain. Every row opens at R0 (understands the rule), empty `evidence`, empty `next_due`. Completeness here is what makes the avoidance set visible later; a map grown from errors alone can only ever contain what already went wrong.
5. Seed `profile.md`, `errors.md`, `lexicon.md` — empty of data, complete in structure. Their empty tables are where the first session writes; a ledger missing a column silently discards what belongs in it.
6. Write `README.md` as the dashboard: current state, live focus, links to every ledger and the newest event notes.
7. Create the directories: `cycles/`, `sessions/`, `reviews/`, `assessments/`, `sources/`, `artifacts/`, `lexicon/`.
8. **Run the contract check** from `vault-contract.md` at the vault root. Report the miss count. `misses: 0` → continue. Anything else → fix the named items and re-run. A miss is never resolved by editing the contract.
9. REQUIRED SUB-SKILL: use `plan-cycle` to open cycle 1.

## Vault shape (proposal, not a mandate)

```text
<vault>/
  README.md            config.md    profile.md
  capability-map.md    lexicon.md   errors.md
  cycles/  sessions/  reviews/  assessments/  sources/  artifacts/  lexicon/
```

## Rationalizations

| Thought | Reality |
|---|---|
| "That key name is clearer — rename it" | Twelve skills grep for the old one. Clearer to you, invisible to them |
| "Minutes make more sense than a count here" | `limits.forced_production` is read as a count of capabilities. Changing the unit changes the behaviour, silently |
| "The templates are examples, I'll write it fresh" | They are the schema. Freehand config is how a vault ends up unreadable |
| "Reverse-engineer the names from the skill bodies" | That was tried; it caught one key out of eleven. Read the contract instead |
| "The files look right, skip the check" | Looking right is what a mis-keyed vault does. Run it |
| "One miss is close enough to start" | One missing key is one skill that quietly does nothing all cycle |

## Red flags

- A key renamed, re-nested, or given a different unit from the template
- A capability map seeded with a handful of example rows instead of full coverage
- A target language, accent, or framework filled in without the learner saying it
- A ledger written without frontmatter, or missing a column the contract names
- Setup declared done without the check output shown

## Done when

Contract check reports `misses: 0`; `capability-map.md` complete for the target language and entirely at R0; no folder created without consent; cycle 1 opened.
