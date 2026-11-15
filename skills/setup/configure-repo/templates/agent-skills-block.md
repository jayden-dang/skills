## Agent skills

This repo is configured for a spec-driven skill set.

- Feature flow: `frame-change` → `specify-behavior` → `design-solution` →
  `plan-tasks` → `build` (wave mode)
- Vague ask you want turned into a prompt for a fresh session: `forge-prompt`
- Work you want an agent to keep doing unattended until it is verifiably done: `forge-prompt`
- Bug on-ramp: `root-cause` (clear unexpected behavior first, then a guarded fix);
  deployed env: `debug-remote` then `root-cause`; telemetry readiness:
  `assess-observability`
- Incoming issues and PRs: `triage`
- Traceability check: the docs-only `audit-trace` skill — run by `prove-claim` and `cut-release`;
  keep it clean
- Project docs (layer enabled): `/define-project` maintains
  `docs/product/vision.md`, the `docs/architecture/` invariant spine, and
  `docs/product/guidelines.md`; the feature skills consult them

Repo config the skills read:

- verify commands, release steps, Remote environments: `docs/agents/project.md`
- cold-start drive (Launch / Doctor / Drive / Evidence): `docs/agents/verify.md`
- Team composition (roster, ownership notes, workflow band): `docs/agents/project.md` (`## Team`)
- Issue tracker operations: `docs/agents/issue-tracker.md`. Read its **Issue format** before creating any issue. It has none: name `/configure-repo`, show the draft, create nothing.
- Triage label mapping: `docs/agents/triage-labels.md`
