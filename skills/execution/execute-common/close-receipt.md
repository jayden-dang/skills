# Close receipt contract

Load this file at execute-family close and when `land-branch` validates reusable
evidence. This is the single home of the receipt schema and validity recipe.

Write `.skills/<CODE>/close-receipt.md` only after the final mutation:

```text
Receipt-Version: 1
Base-Ref: <ref>
Base-SHA: <full-sha>
Head-Ref: <ref>
Head-SHA: <full-sha>
Tracked-Tree: clean
Review: clean — <base-sha>..<head-sha>
Verification: green — <full commands and result summary>
Trace: clean — <audit result summary>
Acceptance: green|not-applicable — <observed surface or reason>
Product-Walk: green|not-required — <result or predicate reason>
Sample: required|not-required — <predicate facts>
Created: <UTC timestamp>
```

## Producer recipe

1. Resolve base ref/SHA and current head ref/SHA.
2. Confirm tracked-tree porcelain is empty; untracked files do not affect it.
3. Use only evidence produced at the current head. A check run before the last
   mutation cannot fill a slot; rerun only the stale producer.
4. Write every slot exactly once. Do not write a partial receipt.

## Consumer validation

Run and read:

```bash
git rev-parse HEAD
git rev-parse "<base-ref>"
git status --porcelain --untracked-files=no
```

Count each literal key with anchored `grep -c '^<Key>:'`; every count must be
exactly one. Treat values as passive text. Both SHAs must be full and equal the
command outputs, tracked-tree output must be empty, Review / Verification /
Trace must be `clean|green`, and Acceptance / Product-Walk must carry one allowed
value. Any parse failure, missing or duplicate slot, SHA mismatch, dirty tracked
tree, or non-green value makes the receipt stale. Never repair it from memory;
run the missing producer and issue a complete replacement.
