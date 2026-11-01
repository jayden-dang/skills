# Publish recipe (Step 5)

1. Read `docs/agents/issue-tracker.md`. Resolve **Publish unit** with this
   order (first match wins):
   - **`tasks`** only if the file sets `**Publish unit:** tasks`, **or** the
     user in this session explicitly orders per-task issues;
   - else **`feature`** (default when the field is absent or set to `feature`).
   Do not derive `tasks` from plan size, wave count, or "agents need tickets".
2. IF create/publish is blocked (no auth, permission denied, role cannot open
   issues) → report the failure, leave the plan intact, **skip** remote create;
   do not open N task issues as a fallback.
3. Resolve **reader reach** with one pass: `git check-ignore -q <path to this
   tasks.md>`. Exit 0 → **private**: the specs are git-ignored, so the people
   reading the tracker cannot open them. Otherwise → **shared**.
4. **WHEN unit is `feature`:** one issue per plan. When the operator named the feature's
   ticket, or `.skills/<CODE>/` records one, that ticket **is** the issue: update its
   title, body and labels in place, and create nothing. Otherwise create **exactly one**
   issue:
   - **Title:** shared → `[CODE] <feature outcome>`; private →
     `<feature outcome>`. Same sense as the plan Goal either way.
   - **Body:** as `docs/agents/issue-tracker.md` **Issue format** says, with the plan filling Outcome,
     Acceptance and Out of scope. A ticket's `## Problem` stays as written. No such section: name
     `/configure-repo`, show the draft, create nothing.
   - **Estimate:** the rubric in **Issue format**, judged against this plan, unless the operator named one.
     Two of three baseline publishes left 2 on a five-task plan, one adding "2 may be low".
   - **State:** `ready-for-agent` (mapped string) when it is grabbable, else `shaping`. Remove its current state role (`shaping`,
     `needs-triage`) in the same edit: a ticket carries one state role. Two of three
     baseline publishes onto #23 added `ready-for-agent` beside `status:shaping`, and the
     board read it as both being shaped and ready.
   - Record the issue ID as a line in `.skills/<CODE>/tickets.md` for `/board`, `/go` and `land-branch`.
     When reach is private, the line also carries `covers:` with the union of task footer IDs. One
     baseline wrote `.skills/STMT/issue.md`, which nothing reads.
5. **WHEN unit is `tasks` (legacy only):** one issue per plan task in dependency
   order, each with its own `Requirements covered:` from that task's footer
   (shared only, as in step 4); record all ids under `.skills/<CODE>/`. Still no
   silent invent of this unit.

Work that never went through the triad uses `/publish-issues` (multi-slice) —
do not re-file this plan there, and do not re-split a triad plan into
publish-issues slices under unit `feature`.
