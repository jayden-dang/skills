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
3. **WHEN unit is `feature`:** create **exactly one** issue:
   - **Title:** `[CODE] <feature outcome>` (same sense as the plan Goal).
   - **Body** (behavior and interfaces, never file paths):
     - first line: `> *This issue was drafted by AI with \`plan-tasks\`.*`
     - What ships (end-to-end), high-level acceptance
     - `Requirements covered:` — **union** of every task footer ID
     - `Plan:` path to this `tasks.md`
     - `Roadmap:` `ROAD-N` / `MILE-N` when INDEX binds them; else omit
     - Optional: task checklist as plain markdown (not tracker issues)
   - Label only this issue with the frontier role (`ready-for-agent` mapped
     string) when it is grabbable.
   - Record the issue id under `.skills/<CODE>/` for execute / `land-branch`.
4. **WHEN unit is `tasks` (legacy only):** one issue per plan task in dependency
   order, each with its own `Requirements covered:` from that task's footer;
   record all ids under `.skills/<CODE>/`. Still no silent invent of this unit.

Work that never went through the triad uses `/publish-issues` (multi-slice) —
do not re-file this plan there, and do not re-split a triad plan into
publish-issues slices under unit `feature`.
