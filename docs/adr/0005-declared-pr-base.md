# 0005 — The PR base branch is declared, never inferred

Repositories that stage work through `dev` or `staging` break every topology-based
guess: `origin/HEAD` names the default branch, so a diff, a narrative, and a PR target
computed from it are wrong together and wrong silently. **Decision:** `setup-repo`
persists `Default PR base:` in `docs/agents/project.md`; `prepare-change` resolves
explicit argument → base of an existing PR → that configured value → ask, and consults
no topology at any rung. **Why:** a nearest-fork-point heuristic was the cheaper
alternative and was rejected because a confidently wrong base is worse than a question,
and this is the one value no evidence in the repository can settle — accepting that
cost reopened the `GOAL-4` deferral in the roadmap.
