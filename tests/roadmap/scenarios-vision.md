# Scenarios — `GOAL-N` identity in the vision

Behavior coverage for `define-project`'s goal-ID handling. Structure is asserted by
`tests/test_vision_goal_ids.py`; these cover the judgment. IDs are bare greppable tokens.

---

## S-VN-1 — Create mode assigns IDs as it writes

**Setup.** A repo with no `docs/product/vision.md`.

**Request.** Run `/define-project` create mode through to writing the vision.

**Expect.**
- Every bullet under `## Goals` carries a unique bold `**GOAL-N**`, assigned while writing
  rather than added afterwards. Covers RMAP-2.7.
- IDs are flat and repo-wide, matching the `**ARCH-N**` grammar so the same strikethrough
  handling applies. Covers RMAP-2.7.

## S-VN-2 — Update mode migrates un-IDed goals

**Setup.** A repo whose `docs/product/vision.md` has goals written as bare bullets with no
IDs — the state every repo adopting this change starts from.

**Request.** Run `/define-project` update mode against any change signal.

**Expect.**
- IDs are assigned in **document order**: the first bullet becomes `GOAL-1`. Covers
  RMAP-2.8.
- The migration is reported to the user, naming each goal and the ID it received — not
  applied silently. Covers RMAP-2.8.
- Two agents migrating the same file independently produce the same assignment, because
  document order leaves nothing to judgment. Covers RMAP-2.8.

## S-VN-3 — An approved goal is immutable

**Setup.** A vision at `Status: Approved` carrying `GOAL-1` … `GOAL-5`.

**Request.** "We're dropping the third goal, and adding two new ones."

**Expect.**
- The dropped goal is struck through with a reason, not deleted and not renumbered. Covers
  RMAP-2.9.
- The new goals take fresh IDs continuing past the highest in use — including past the
  retired one, which is never reused. Covers RMAP-2.9.
- The surviving goals keep their original numbers even though a gap now exists in the
  sequence. Covers RMAP-2.9.

## S-VN-4 — A struck goal cannot satisfy a citation

**Setup.** A roadmap milestone citing `GOAL-3`, and a vision in which `GOAL-3` is struck.

**Expect.**
- The citation is reported as dangling rather than resolving to the retired goal — the same
  rule `audit-trace` applies to a `Respects: ARCH-N` naming a struck invariant. Covers RMAP-2.9.

## S-VN-5 — This repo's own migration

**Setup.** This repository, whose `docs/product/vision.md` is `Status: Approved` and whose
five goals carried no IDs before this feature.

**Expect.**
- The five goals are now `GOAL-1` … `GOAL-5` in their original document order, and those
  assignments are immutable from the moment they landed. Covers RMAP-2.8.
