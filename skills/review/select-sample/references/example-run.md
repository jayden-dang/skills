# Example run — attention allocation

Loaded from `SKILL.md`'s **The allocation** section: one worked instance of the
allocation shape stated abstractly there.

A real run, over this skill set's own 16-file branch:

```
Attention allocation — 72b8178..HEAD
10 units · 16 files · 2746 changed lines

SAMPLE — 5 of 10 units
  skills/review     B1 risk-path (skills/review/select-sample/SKILL.md, +1)  290 lines
    Claim:       the skill body implements the approved binding pass
    Refuted by:  python3 -m unittest tests.test_attn_surfaces
    Disposition: undispositioned
  skills/execution  B1 risk-path (skills/execution/build-in-waves/SKILL.md)  1 line
  docs/specs        B5 spec-or-invariant-surface (…/design.md, +3)  1920 lines
  AGENTS.md         B1 risk-path (AGENTS.md)  13 lines
  .claude-plugin/plugin.json  B2 dependency-surface  1 line

RESIDUE — 5 of 10 units, agent verdicts only
  CONTEXT.md                   1 files    22 lines
  docs/agents                  1 files     2 lines
  docs/guide                   2 files    91 lines
  tests/attention-allocation   2 files    98 lines
  tests/test_attn_surfaces.py  1 files   308 lines

Nothing above says the residue is correct.
```

Note what the residue holds: 308 lines of test code nobody read. That is the
point — it is stated, not hidden.
