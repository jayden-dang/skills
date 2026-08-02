# Errors and logging standards

Status: Approved
Date: 2026-08-02

## Purpose and boundary

Error and logging conventions for pack tooling and guidance for consumer apps.

## Error handling

| Context | Convention |
|---|---|
| Skill procedure | Surface blockers clearly; do not invent standing project facts (ARCH-2) |
| Pack Python scripts | Fail loud with non-zero exit; print actionable paths |
| Consumer apps | Prefer domain errors at boundaries; map to HTTP/UI as design specifies |

## Logging

| Level / field | When / content |
|---|---|
| skill dialogue | Imperative status to the user; no fake success |
| pack scripts | stderr for errors; stdout for primary output when piped |

## Sensitive data

- Never log secrets, API keys, tokens, or credentials.
- Do not paste secret-bearing env dumps into specs or guides.

## Not ops observability map

Conventions only. Dashboards/alerts live in `docs/ops/observability.md` when present.
