# Issue tracker sync

Loaded from `SKILL.md` **Session preflight** question 1, only when
`docs/agents/issue-tracker.md` names a configured tracker.

Read `docs/agents/issue-tracker.md` when present. IF a tracker is configured
(github / gitlab / linear / local / other named backend) → ask whether this
build should sync with that tracker (bind issues to the branch, pull ticket
IDs into briefs/ledger, use the tracker's wayfinding ops for status). IF yes →
resolve ticket IDs from branch name, plan, or a short user list; record them
under `.skills/` for implementer briefs and later `land-branch`. IF no →
empty ticket set; continue.
