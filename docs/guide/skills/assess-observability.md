# `assess-observability`

> A readiness finding set for deployed telemetry. Never a completeness stamp. Never a Hybrid 1A file.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable |
| **Reads** | live telemetry (read-only), `docs/agents/project.md` Remote environments |
| **Writes** | a finding set in the session only |
| **Calls** | [`debug-remote`](debug-remote.md) if a live symptom appears; names `/define-system-doc` and `/configure-repo` |
| **Called by** | description match; on-ramp “is tracing complete enough?” |

## When it fires

Production or staging telemetry may be insufficient: “is tracing complete”, upgrade tracing, OpenObserve/OTLP enough, head vs tail, span status, golden signals, log-trace join. A **live** 500/trace hunt is [`debug-remote`](debug-remote.md). A local failing test is [`root-cause`](root-cause.md).

## The Iron Law

```
NO COMPLETENESS STAMP WITHOUT A GREEN FINDING SET
NO CANONICAL OPS OR STANDARDS FILE FROM THIS SKILL
```

OTLP to a backend is one row. `docs/ops/observability.md` is authored by `/define-system-doc`, never here — including not as Draft.

## Finding set

Must rows (identity, version, environment, propagation, current semconv, SERVER 4xx unset, log join, golden signals, sampling that keeps rare errors, searchable backend, PII, black-box). `pass` needs a proving **read**. Any `fail` or `unresolved` Must row → verdict `not-complete`. Profiles are not-must (Alpha).

Failed rows become `frame-change` / `amend-feature`, promoted local → dev → staging → prod. Do not PR 4xx → Error “for the board.”

## Why it is written the way it is

Open stamp RED **refused** the VP stamp — the gate already held. The recorded failure was **shape and home**: agents wrote `docs/ops/observability.md` as Draft, and the readiness question routed to `solve-problem`. The recipe puts the set in session, forbids the canonical path, and owns the trigger.

## See also

- [`debug-remote`](debug-remote.md) — incident, not readiness
- [`define-system-doc`](define-system-doc.md) — Approved ops/standards maps
- [On-ramps](../process/on-ramps.md)
