# Tasks: Outbound comprehend-change (self-check)

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: XDIFF
Status: Approved
Date: 2026-07-24
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Ship a user-invoked `comprehend-change` skill that builds one
self-contained Background → Intuition → Code → Quiz HTML packet for an outbound
git change (D!/A+ range, optional DREC read-only enrichment), without ship gates
or decision-record emission.

**Architecture:** Skill package under `skills/review/comprehend-change/` with
`SKILL.md` workflow, checked-in `shell/packet.html`, and `references/*` doctrine.
Agent fills the shell and writes HTML outside the target worktree. Inventory
surfaces (plugin, AGENTS, architecture skills list, guide) register the skill.
Verification is structural unittest + scenario greps (no consumer runtime
renderer).

**Tech Stack:** Markdown skills + static HTML/CSS/JS shell; Python `unittest` +
`rg` structural scenarios under `tests/comprehend-change/`. Leading words:
**comprehend-change**, **packet**, **resolved range**, **pure-untracked**,
**forward-cite**, **shell template**.

## Global Constraints

Copied for every implementer brief:

1. **writing-skills quality bar** on every skill edit: description = trigger +
   outcome only (no workflow dump); `disable-model-invocation: true`; body under
   ~300 lines preferred / 500 max; progressive disclosure into
   `references/` and `shell/`; hard gates + rationalization rows only for real
   pressure; **Done when** on steps; `REQUIRED SUB-SKILL:` prose only; no `@`
   skill links.

2. **RED before GREEN** for skill prose: baseline structural asserts / scenarios
   against current tree first; record expected RED; then implement; re-run GREEN.

3. **ARCH invariants:** ARCH-1 (trace = textual presence); ARCH-2 (absent
   config no-op); ARCH-3 (no mandatory consumer Python/SaaS); ARCH-4 (stable
   IDs); ARCH-5 (user-invoked never auto-invoked; may call model-invoked
   `design-page` only); ARCH-6 (no policing external/unmediated work).

4. **Neighbor isolation:** do **not** modify `finish-branch`, `release`,
   `code-review`, `execute-plan`, or `record-decision` to soft-prompt, require,
   or emit for this skill. Negative tests must stay green.

5. **DREC hard boundary:** read-only optional enrichment; never create/edit
   records; never invoke `record-decision`; never rewrite DEC payload/envelope.

6. **Verify commands** (from `docs/agents/project.md`):
   - Lint: `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py`
   - Unit: `python3 -m unittest discover -s tests`
   - Feature unit: `python3 -m unittest tests.test_comprehend_change_surfaces`
   - Full suite must pass before any completion claim on a task that touches
     plugin/skills.

7. **Test annotations:** greppable bare `XDIFF-N.M` in
   `tests/comprehend-change/scenarios.md` and/or method names / docstrings in
   `tests/test_comprehend_change_surfaces.py`. Add
   `tests/comprehend-change/red-baselines.md` to project.md trace ignore when
   created (Task 1).

8. **Commits:** one commit per task preferred; trailers
   `Implements: XDIFF-N.M` (list all IDs the task footer claims).

9. **Solo packaging:** no invented peer reviewers; agent-as-pair tone.

10. **Forbidden:** Notion/SaaS product path; dual MD+HTML deliverable; content
    JSON + renderer as primary path; ship/merge gates; inbound PR primary job;
    renaming feature code away from XDIFF; primary skill `name: explain-diff`.

11. **Terminology:** prefer **resolved range** over “explained range” in new
    prose.

## File Structure

| Path | Responsibility |
|---|---|
| `skills/review/comprehend-change/SKILL.md` | User-invoked workflow, gates, cascade, pointers |
| `skills/review/comprehend-change/shell/packet.html` | Interactive shell template (TOC + quiz JS) |
| `skills/review/comprehend-change/references/quiz-quality.md` | Quiz pedagogy rules |
| `skills/review/comprehend-change/references/dec-whitelist.md` | RECORD field whitelist + cite rules |
| `skills/review/comprehend-change/references/html-constraints.md` | Offline HTML / a11y / pre-wrap |
| `skills/review/comprehend-change/references/passive-data-safety.md` | Passive-data / escape doctrine |
| `.claude-plugin/plugin.json` | Register skill directory |
| `docs/architecture/skills.md` | Inventory entry under review/ |
| `AGENTS.md` | User-invoked list + §11 table + skill count |
| `docs/guide/skills/comprehend-change.md` | Human guide |
| `docs/guide/skills/README.md` | Index row |
| `docs/agents/project.md` | Trace ignore for red-baselines (and optional Output-dir docs only if template seed added — not required) |
| `tests/comprehend-change/scenarios.md` | Tagged structural/scenario checks |
| `tests/comprehend-change/red-baselines.md` | RED baselines (trace-ignored) |
| `tests/test_comprehend_change_surfaces.py` | Unittest structural greps |

---

### Task 1: Package skeleton, plugin registration, test harness

**Files:**
- Create: `skills/review/comprehend-change/SKILL.md` (frontmatter + stub body)
- Create: `tests/comprehend-change/scenarios.md`
- Create: `tests/comprehend-change/red-baselines.md`
- Create: `tests/test_comprehend_change_surfaces.py`
- Modify: `.claude-plugin/plugin.json` — add `"./skills/review/comprehend-change"`
- Modify: `docs/agents/project.md` — append
  `tests/comprehend-change/red-baselines.md` to Trace ignore list
- Test: `tests/test_comprehend_change_surfaces.py`,
  `tests/comprehend-change/scenarios.md`

**Reuse:** existing — plugin dir registration +
`tests/test_plugin_manifest.py` set equality; user-invoked frontmatter pattern
from `skills/meta/teach/SKILL.md` (rung 2)

**Interfaces:**
- Consumes: design §1 frontmatter shape
- Produces: installable skill path; harness partitions for later tasks

**Depends-on:** none

- [ ] **Step 1: Write the failing tests**

Create `tests/test_comprehend_change_surfaces.py` with methods that will fail
until files exist (docstrings or names must include greppable IDs):

```python
"""Structural surfaces for comprehend-change (XDIFF)."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/review/comprehend-change/SKILL.md"
PLUGIN = ROOT / ".claude-plugin/plugin.json"


class TestComprehendChangeSurfaces(unittest.TestCase):
    def test_XDIFF_1_1_1_2_skill_frontmatter(self):
        """XDIFF-1.1 XDIFF-1.2 skill name and user-invoked flag."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("name: comprehend-change", text)
        self.assertIn("disable-model-invocation: true", text)
        self.assertRegex(text, r"(?i)comprehend|self-check")

    def test_XDIFF_8_1_8_2_package_and_plugin(self):
        """XDIFF-8.1 XDIFF-8.2 package path registered in plugin."""
        self.assertTrue(SKILL.is_file())
        data = json.loads(PLUGIN.read_text(encoding="utf-8"))
        self.assertIn("./skills/review/comprehend-change", data["skills"])

    def test_XDIFF_8_4_no_saas_requirement_in_skill(self):
        """XDIFF-8.4 skill must not require Notion/SaaS as product path."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertNotRegex(text, r"(?i)required.*notion|must use notion")
```

Create `tests/comprehend-change/scenarios.md`:

```markdown
# XDIFF / comprehend-change — structural and scenario checks

## S-package
<!-- XDIFF-1.1 XDIFF-1.2 XDIFF-8.1 XDIFF-8.2 XDIFF-8.4 -->
Assert skill path `skills/review/comprehend-change/SKILL.md` exists with
`name: comprehend-change`, `disable-model-invocation: true`, description
keywords comprehend/self-check (not review/verify alone).
Assert plugin.json lists `./skills/review/comprehend-change`.

## S-shell
<!-- Task 2 -->

## S-references
<!-- Task 3 -->

## S-skill-body
<!-- Task 4 -->

## S-dec-narrative
<!-- Task 5 -->

## S-output-guide
<!-- Task 6 -->

## S-neighbors
<!-- Task 6 -->

## Coverage
<!-- Task 6 fills full ID list -->
```

Create `tests/comprehend-change/red-baselines.md` with stub `## RED-package`.

Run: `python3 -m unittest tests.test_comprehend_change_surfaces` — expect:
**FAIL** (missing skill and/or plugin entry).

- [ ] **Step 2: Implement skeleton**

Write minimal `SKILL.md`:

```yaml
---
name: comprehend-change
description: >
  Use when the user wants to comprehend or self-check a code change — their
  branch, diff, commit, working tree, or named range — and wants a rich
  Background / Intuition / Code / Quiz HTML packet. Triggers on
  /comprehend-change, "comprehend this change", "self-check this branch",
  "help me understand my diff before I ship". Not for code-review verdicts,
  verify evidence, or teach lessons.
disable-model-invocation: true
---

# Comprehend change

Stub — full workflow lands in Task 4. Do not implement range/packet here.
```

Add plugin entry (alphabetically near other `review/` entries is fine).
Update `docs/agents/project.md` Trace ignore line to include
`tests/comprehend-change/red-baselines.md`.

Run: `python3 -m unittest tests.test_comprehend_change_surfaces` — expect: **PASS**.  
Run: `python3 -m unittest tests.test_plugin_manifest` — expect: **PASS**.  
Run: `python3 scripts/lint-skill-frontmatter.py` — expect: **PASS**.

- [ ] **Step 3: Commit**

`git commit` with trailers `Implements: XDIFF-1.1, XDIFF-1.2, XDIFF-8.2, XDIFF-8.4`.

_Requirements: XDIFF-1.1, XDIFF-1.2, XDIFF-8.2, XDIFF-8.4_

---

### Task 2: Interactive shell template contract

**Files:**
- Create: `skills/review/comprehend-change/shell/packet.html`
- Modify: `tests/test_comprehend_change_surfaces.py` — shell contract tests
- Modify: `tests/comprehend-change/scenarios.md` — append only `## S-shell`
- Test: unit + scenarios

**Reuse:** none — first checked-in HTML/JS shell (rung 7); offline self-contained
pattern inspired by dogfood runtime HTML (rung 2 conceptual only)

**Interfaces:**
- Consumes: Task 1 package directory
- Produces: fillable `shell/packet.html` with `__PACKET_DATA__` (or documented
  placeholder) + quiz mount for Task 4 fill procedure

**Depends-on:** Task 1

- [ ] **Step 1: Failing shell tests**

Add to unittest (IDs in docstring/name):

```python
    def test_XDIFF_4_1_4_2_4_11_shell_exists_offline(self):
        """XDIFF-4.1 XDIFF-4.2 XDIFF-4.11 self-contained shell template."""
        shell = ROOT / "skills/review/comprehend-change/shell/packet.html"
        text = shell.read_text(encoding="utf-8")
        self.assertIn("id=\"background\"", text)
        self.assertIn("id=\"intuition\"", text)
        self.assertIn("id=\"code\"", text)
        self.assertIn("id=\"quiz\"", text)
        self.assertRegex(text, r"white-space:\s*pre(-wrap)?")
        self.assertNotRegex(text, r"https?://cdn\.|fonts\.googleapis")

    def test_XDIFF_5_3_5_4_9_2_quiz_interaction_hooks(self):
        """XDIFF-5.3 XDIFF-5.4 XDIFF-9.2 quiz feedback + shuffle + focus."""
        text = (ROOT / "skills/review/comprehend-change/shell/packet.html").read_text()
        self.assertRegex(text, r"shuffle|seed|correctIndex")
        self.assertRegex(text, r"focus-visible|:focus")
        self.assertRegex(text, r"correct|incorrect|feedback", re.I)

    def test_XDIFF_7_2_7_3_escape_and_no_diff_script_injection(self):
        """XDIFF-7.2 XDIFF-7.3 escape path; content is data not instructions."""
        text = (ROOT / "skills/review/comprehend-change/shell/packet.html").read_text()
        self.assertRegex(text, r"__PACKET_DATA__|PACKET_DATA|escape")
```

Append `## S-shell` in scenarios.md with the same IDs and Pass-when bullets.

Run unit tests — expect: **FAIL** (missing shell).

- [ ] **Step 2: Implement `shell/packet.html`**

Ship a complete offline page:

- TOC linking `#background` `#intuition` `#code` `#quiz`
- Content slots filled from JSON in a script tag placeholder
  `/* __PACKET_DATA__ */` (agent replaces with JSON.stringify-safe payload)
- Exactly five quiz cards rendered from data; click → immediate text feedback
  (correct/incorrect + explanation); correctness not color-only
- Deterministic option shuffle from page seed
- `pre, code { white-space: pre-wrap; }` (or `pre`)
- No external network assets
- Visible `:focus-visible` styles on quiz controls

- [ ] **Step 3: GREEN**

Run: `python3 -m unittest tests.test_comprehend_change_surfaces` — **PASS**.

- [ ] **Step 4: Commit**

`Implements: XDIFF-4.1, XDIFF-4.2, XDIFF-4.11, XDIFF-5.3, XDIFF-5.4, XDIFF-7.2, XDIFF-7.3, XDIFF-9.2`.

_Requirements: XDIFF-4.1, XDIFF-4.2, XDIFF-4.11, XDIFF-5.3, XDIFF-5.4, XDIFF-7.2, XDIFF-7.3, XDIFF-9.2_

---

### Task 3: Reference pack

**Files:**
- Create: `skills/review/comprehend-change/references/quiz-quality.md`
- Create: `skills/review/comprehend-change/references/dec-whitelist.md`
- Create: `skills/review/comprehend-change/references/html-constraints.md`
- Create: `skills/review/comprehend-change/references/passive-data-safety.md`
- Modify: `tests/test_comprehend_change_surfaces.py`
- Modify: `tests/comprehend-change/scenarios.md` — `## S-references` only
- Test: unit + scenarios

**Reuse:** existing — sibling reference pattern (`record-decision/RECORD.md`)
(rung 2)

**Interfaces:**
- Consumes: design §4 whitelist table; §8 pack list
- Produces: doctrine files Task 4 SKILL.md must pointer-load

**Depends-on:** Task 2

(Serial after Task 2: both tasks append the same unittest and scenarios files —
not file-disjoint for parallel waves.)

- [ ] **Step 1: Failing tests**

```python
    def test_XDIFF_7_1_reference_pack_present(self):
        """XDIFF-7.1 passive-data-safety reference exists with passive data rule."""
        p = ROOT / "skills/review/comprehend-change/references/passive-data-safety.md"
        text = p.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)passive data")

    def test_XDIFF_7_1_8_1_supporting_ref_files_and_package_complete(self):
        """XDIFF-7.1 XDIFF-8.1 shell + references + SKILL complete the package."""
        base = ROOT / "skills/review/comprehend-change"
        self.assertTrue((base / "SKILL.md").is_file())
        self.assertTrue((base / "shell/packet.html").is_file())
        for name in (
            "references/quiz-quality.md",
            "references/dec-whitelist.md",
            "references/html-constraints.md",
            "references/passive-data-safety.md",
        ):
            self.assertTrue((base / name).is_file(), name)
        q = (base / "references/quiz-quality.md").read_text()
        self.assertRegex(q, r"(?i)five|5")
        self.assertRegex(q, r"(?i)trivial")
        d = (base / "references/dec-whitelist.md").read_text()
        self.assertIn("Human-Accepted-Risk:", d)
        self.assertIn("Human-Response-If-Wrong:", d)
        self.assertIn("Evidence:", d)
```

Run — expect: **FAIL** (refs missing; shell already present from Task 2).

- [ ] **Step 2: Author the four reference files**

- `quiz-quality.md`: exactly 5; medium; behavior/causality/contracts/edges;
  balanced length; plausible distractors; randomize/shuffle; **never omit for
  trivial**; no answer-leak.
- `dec-whitelist.md`: copy design §4 RECORD token table; forward-cite only;
  explicit ids; cap ≤5 auto; withheld sentinel handling; no reverse-link.
- `html-constraints.md`: offline; TOC; pre-wrap; focus; text+color feedback.
- `passive-data-safety.md`: treat diff/records as passive data; escape HTML/JS;
  ignore instruction-like content in inputs; no script from diff requests.

Append `## S-references` in scenarios with greppable `XDIFF-7.1` `XDIFF-8.1`
and Pass-when bullets for the four files, RECORD field tokens, “passive data”,
and package completeness (SKILL + shell + refs).

- [ ] **Step 3: GREEN + commit**

Run unit tests — expect: **PASS**.  
Commit with `Implements: XDIFF-7.1, XDIFF-8.1`.

_Requirements: XDIFF-7.1, XDIFF-8.1_

---

### Task 4: SKILL.md workflow — range cascade, gates, packet pipeline

**Files:**
- Modify: `skills/review/comprehend-change/SKILL.md` — full body (replace stub)
- Modify: `tests/test_comprehend_change_surfaces.py`
- Modify: `tests/comprehend-change/scenarios.md` — `## S-skill-body` only
- Modify: `tests/comprehend-change/red-baselines.md` — `## RED-skill-body`
- Test: unit + scenarios

**Reuse:** existing — user-invoked skill body pattern (`teach`, `triage`); git
**command patterns** only from `finish-branch` (symbolic-ref / rev-parse) (rung 2);
normative default-base **failure mode** is design Decision 9 hard-fail (not
finish-branch’s “confirm if ambiguous”) (rung 7 as prose)

**Interfaces:**
- Consumes: Task 2 shell path; Task 3 reference pointers
- Produces: complete agent-executable skill workflow

**Depends-on:** Task 2, Task 3

- [ ] **Step 1: RED baselines + failing asserts**

Record in `red-baselines.md` expected agent failures without skill body:
pure-untracked falls through to branch packet; dirty+branch-ahead omits scope
notice; invents empty explainer; claims quiz pass; writes under docs/.

Add unit asserts that `SKILL.md` body contains (fail on stub):

| Grep / assert | IDs |
|---|---|
| `pure_untracked` or “pure untracked” before branch default | XDIFF-2.2, 3.4 |
| `tracked_dirty` / working tree vs HEAD | XDIFF-2.3, 3.1, 3.5 |
| `truly clean` / default base..HEAD | XDIFF-2.5 |
| empty hard-fail / nothing to comprehend | XDIFF-2.6 |
| scope notice when branch ahead | XDIFF-2.4 |
| default base local-only: symbolic-ref origin/HEAD → main/master rev-parse → **hard-fail** ask explicit base (not confirm-and-guess) | XDIFF-2.7 |
| include-untracked / gitignore | XDIFF-3.2, 3.3 |
| explicit range skips cascade | XDIFF-2.1 |
| no auto-run / no soft-prompt / no ship gate language | XDIFF-1.3, 1.4, 1.5 |
| outbound self-check; job-agnostic range | XDIFF-1.6 |
| exactly five quiz / never omit trivial | XDIFF-5.1, 5.2 |
| never claim pass / no score file | XDIFF-5.8, 5.9 |
| never record-decision / no write docs/decisions | XDIFF-6.6, 6.7 |
| design-page optional only | XDIFF-4.12 |
| no partial HTML on hard-fail | XDIFF-9.1 |
| output outside worktree + hard-fail in-tree user path | XDIFF-4.7, 4.8 |
| YYYY-MM-DD-comprehension- + absolute path handoff | XDIFF-4.9, 4.10 |
| output resolution order env/project/durable/temp | XDIFF-4.8, 10.6 |
| pointer to shell/packet.html | XDIFF-4.11 (already shell; skill must fill) |
| Background / Intuition / Code / Quiz narrative rules | XDIFF-4.3, 4.4, 4.5, 4.6 |
| Intuition HTML primary not ASCII | XDIFF-4.5 |
| quiz quality pointer + 5.5–5.7 rules summary | XDIFF-5.5, 5.6, 5.7 |

Scenarios section `## S-skill-body` lists every ID above as greppable comments
and Pass-when: each string present in SKILL.md.

Run greps — expect: **RED** on stub.

- [ ] **Step 2: Implement full SKILL.md**

Replace stub with imperative workflow per design §2–§7 (concise; detail in
refs). Must include:

1. Parse invocation (range, DEC ids, include-untracked, output path).
2. Range resolver first-match cascade (pure-untracked stop → tracked dirty +
   scope notice → truly clean → empty fail).
3. Context gather + surrounding code (resolved range terminology).
4. DREC forward-cite + explicit (summary + pointer to dec-whitelist.md).
5. Narrative content rules + always 5 quiz items.
6. Fill shell template; escape; write outside worktree; in-worktree user path
   **hard-fail**.
7. Handoff absolute path; never claim quiz pass.
8. Hard-gate table + rationalization rows for RED failures.
9. Optional `REQUIRED SUB-SKILL: use design-page` — not mandatory.
10. Done when: one openable HTML path or honest hard-stop with no partial success
    HTML.

Keep body lean with strong pointers to `references/*` and `shell/packet.html`.

- [ ] **Step 3: GREEN**

All S-skill-body greps pass; unit methods for body strings pass; lint frontmatter
pass.

- [ ] **Step 4: Commit**

Trailers for all IDs in the footer below.

_Requirements: XDIFF-1.3, XDIFF-1.4, XDIFF-1.5, XDIFF-1.6, XDIFF-2.1, XDIFF-2.2, XDIFF-2.3, XDIFF-2.4, XDIFF-2.5, XDIFF-2.6, XDIFF-2.7, XDIFF-3.1, XDIFF-3.2, XDIFF-3.3, XDIFF-3.4, XDIFF-3.5, XDIFF-4.3, XDIFF-4.4, XDIFF-4.5, XDIFF-4.6, XDIFF-4.7, XDIFF-4.8, XDIFF-4.9, XDIFF-4.10, XDIFF-4.12, XDIFF-5.1, XDIFF-5.2, XDIFF-5.5, XDIFF-5.6, XDIFF-5.7, XDIFF-5.8, XDIFF-5.9, XDIFF-6.6, XDIFF-6.7, XDIFF-9.1, XDIFF-10.6_

---

### Task 5: DEC enrichment protocol in skill + scenarios

**Files:**
- Modify: `skills/review/comprehend-change/SKILL.md` — DEC section completeness
  (if Task 4 left only a pointer, expand to full design §4 algorithm bullets)
- Modify: `tests/comprehend-change/scenarios.md` — `## S-dec-narrative` only
- Modify: `tests/test_comprehend_change_surfaces.py` — DEC protocol greps
- Test: unit + scenarios

**Reuse:** existing — RECORD.md field names (rung 2); design §4 (rung 7 prose)

**Interfaces:**
- Consumes: Task 3 `dec-whitelist.md`; Task 4 skill skeleton
- Produces: complete DREC read-only selection rules in skill body

**Depends-on:** Task 4

- [ ] **Step 1: Failing DEC asserts**

SKILL.md must contain greppable rules for:

| Content | IDs |
|---|---|
| no-op when no docs/decisions / no records | XDIFF-6.1 |
| forward-cite DEC- regex / mechanical only | XDIFF-6.2 |
| no same-feature / no recent-N auto | XDIFF-6.3 |
| explicit user DEC ids | XDIFF-6.4 |
| cap ≤5 auto; newest-by-id | XDIFF-6.5 |
| cite DEC-* in HTML when used | XDIFF-6.8 |
| Human-Accepted-Risk / Human-Response-If-Wrong verbatim | XDIFF-6.9 |
| no reverse-link required | XDIFF-6.10 |

Scenarios `## S-dec-narrative` tags all of the above.

Run — expect: **FAIL** if incomplete.

- [ ] **Step 2: Complete skill DEC section**

Implement design §4 algorithm bullets + forbidden list; load
`references/dec-whitelist.md` when enriching.

- [ ] **Step 3: GREEN + commit**

`Implements: XDIFF-6.1, XDIFF-6.2, XDIFF-6.3, XDIFF-6.4, XDIFF-6.5, XDIFF-6.8, XDIFF-6.9, XDIFF-6.10`.

_Requirements: XDIFF-6.1, XDIFF-6.2, XDIFF-6.3, XDIFF-6.4, XDIFF-6.5, XDIFF-6.8, XDIFF-6.9, XDIFF-6.10_

---

### Task 6: Guide, inventory surfaces, neighbor isolation, full coverage

**Files:**
- Create: `docs/guide/skills/comprehend-change.md`
- Modify: `docs/guide/skills/README.md` — review bucket row
- Modify: `docs/architecture/skills.md` — review/ entry
- Modify: `AGENTS.md` — §3 user-invoked list, §11 table, skill count
- Modify: `tests/comprehend-change/scenarios.md` — `## S-output-guide`,
  `## S-neighbors`, `## Coverage`
- Modify: `tests/test_comprehend_change_surfaces.py` — neighbor negatives +
  inventory
- Test: unit + scenarios + full suite

**Reuse:** existing — guide/README/AGENTS/architecture inventory patterns
(rung 2)

**Interfaces:**
- Consumes: completed skill from Tasks 4–5
- Produces: discoverable docs; negative isolation guarantees

**Depends-on:** Task 5

- [ ] **Step 1: Failing inventory + neighbor tests**

```python
    def test_XDIFF_8_3_guide_exists(self):
        """XDIFF-8.3 human guide path."""
        p = ROOT / "docs/guide/skills/comprehend-change.md"
        text = p.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)D!|cascade|untracked|quiz|decision record")

    def test_XDIFF_10_1_through_10_5_10_7_10_8_10_9_neighbors(self):
        """XDIFF-10.1 XDIFF-10.2 XDIFF-10.3 XDIFF-10.4 XDIFF-10.5 XDIFF-10.7 XDIFF-10.8 XDIFF-10.9
        neighbors must not soft-prompt or require comprehend-change."""
        forbidden_callers = [
            "skills/ship/finish-branch/SKILL.md",
            "skills/ship/release/SKILL.md",
            "skills/review/code-review/SKILL.md",
            "skills/execution/execute-plan/SKILL.md",
            "skills/ship/record-decision/SKILL.md",
        ]
        for rel in forbidden_callers:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotRegex(
                text,
                r"(?i)comprehend-change|REQUIRED SUB-SKILL: use `comprehend-change`",
            )
        skill = (ROOT / "skills/review/comprehend-change/SKILL.md").read_text()
        self.assertRegex(skill, r"(?i)digest")  # must say packets are NOT digests
        self.assertRegex(skill, r"(?i)not.*digest|never.*digest|not named.*digest")
```

Also assert AGENTS.md and architecture/skills.md mention `comprehend-change`.

Scenarios: guide documents D!, A+, output, quiz, DREC read-only, no ship gate
(`XDIFF-8.3`); neighbor isolation IDs; Solo no peer-reviewer invention
(`XDIFF-10.7`); design-page remains optional / shell alone sufficient
(`XDIFF-10.5` Pass-when pointing at skill prose).

Run — expect: **FAIL** until guide/inventory exist.

- [ ] **Step 2: Implement guide + inventory**

- `docs/guide/skills/comprehend-change.md` per design §9
- README row under review
- `docs/architecture/skills.md` entry `(U)`
- `AGENTS.md`: add to user-invoked list and quick-reference table; bump skill
  count on **all** count surfaces (header “41 Skills”, tree comment, §11
  heading) to the post-add total
- `docs/guide/skills/README.md`: bump human skill-count prose if present
  (“Forty” / similar) to match

Do **not** edit finish-branch/release/code-review/execute-plan/record-decision
except if a false positive requires clarifying they remain free of this skill
(should need zero edits). When editing `docs/architecture/skills.md`, **append**
`comprehend-change` under review/ only — do not “fix” pre-existing inventory
drift (e.g. missing `polish`) unless asked.

- [ ] **Step 3: Coverage matrix**

In `scenarios.md` `## Coverage`, list every XDIFF-1.1 … XDIFF-10.9 and assert
each appears in `tests/comprehend-change/scenarios.md` and/or
`tests/test_comprehend_change_surfaces.py`:

```bash
for id in \
  XDIFF-1.1 XDIFF-1.2 XDIFF-1.3 XDIFF-1.4 XDIFF-1.5 XDIFF-1.6 \
  XDIFF-2.1 XDIFF-2.2 XDIFF-2.3 XDIFF-2.4 XDIFF-2.5 XDIFF-2.6 XDIFF-2.7 \
  XDIFF-3.1 XDIFF-3.2 XDIFF-3.3 XDIFF-3.4 XDIFF-3.5 \
  XDIFF-4.1 XDIFF-4.2 XDIFF-4.3 XDIFF-4.4 XDIFF-4.5 XDIFF-4.6 XDIFF-4.7 \
  XDIFF-4.8 XDIFF-4.9 XDIFF-4.10 XDIFF-4.11 XDIFF-4.12 \
  XDIFF-5.1 XDIFF-5.2 XDIFF-5.3 XDIFF-5.4 XDIFF-5.5 XDIFF-5.6 XDIFF-5.7 \
  XDIFF-5.8 XDIFF-5.9 \
  XDIFF-6.1 XDIFF-6.2 XDIFF-6.3 XDIFF-6.4 XDIFF-6.5 XDIFF-6.6 XDIFF-6.7 \
  XDIFF-6.8 XDIFF-6.9 XDIFF-6.10 \
  XDIFF-7.1 XDIFF-7.2 XDIFF-7.3 \
  XDIFF-8.1 XDIFF-8.2 XDIFF-8.3 XDIFF-8.4 \
  XDIFF-9.1 XDIFF-9.2 \
  XDIFF-10.1 XDIFF-10.2 XDIFF-10.3 XDIFF-10.4 XDIFF-10.5 XDIFF-10.6 \
  XDIFF-10.7 XDIFF-10.8 XDIFF-10.9
do
  rg -q "$id" tests/comprehend-change/scenarios.md tests/test_comprehend_change_surfaces.py \
    || echo "MISSING test annotation: $id"
done
```

Expect: zero MISSING. Fix any gaps by adding greppable ID tokens to scenarios
(not by inventing production code).

- [ ] **Step 4: Full verify**

```bash
python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py
python3 -m unittest discover -s tests
```

Expect: all pass.

- [ ] **Step 5: Commit**

`Implements: XDIFF-8.3, XDIFF-10.1, XDIFF-10.2, XDIFF-10.3, XDIFF-10.4, XDIFF-10.5, XDIFF-10.7, XDIFF-10.8, XDIFF-10.9`.

_Requirements: XDIFF-8.3, XDIFF-10.1, XDIFF-10.2, XDIFF-10.3, XDIFF-10.4, XDIFF-10.5, XDIFF-10.7, XDIFF-10.8, XDIFF-10.9_

---

## Coverage map (author)

| IDs | Task footer | Tagged tests |
|---|---|---|
| 1.1, 1.2, 8.2, 8.4 | Task 1 | unit + S-package |
| 4.1, 4.2, 4.11, 5.3, 5.4, 7.2, 7.3, 9.2 | Task 2 | unit + S-shell |
| 7.1, 8.1 | Task 3 | unit + S-references |
| 1.3–1.6, 2.1–2.7, 3.1–3.5, 4.3–4.10, 4.12, 5.1–5.2, 5.5–5.9, 6.6–6.7, 9.1, 10.6 | Task 4 | unit + S-skill-body |
| 6.1–6.5, 6.8–6.10 | Task 5 | unit + S-dec-narrative |
| 8.3, 10.1–10.5, 10.7–10.9 | Task 6 | unit + S-output-guide + S-neighbors + Coverage |

**Count:** 67 requirement IDs; each has exactly one primary task footer above.

**Serial order:** Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 (Tasks 2/3
share unittest/scenarios Modify paths — not parallel).

**Plan review fixes** (`.skills/xdiff-plan-review.md`): I1 serial 2→3; I2
`import re`; I3 Decision 9 hard-fail base; I4 XDIFF-8.1 on Task 3; N1/N4 count
surfaces + N2 XDIFF-10.5 scenario bullet.

**Upstream:** requirements Status Approved; design Status Approved. INDEX stays
**Approved** until feature Implemented after execute-plan.

**Issue tracker:** none required for this skill-set repo task publish (optional
Step 5 skipped).
