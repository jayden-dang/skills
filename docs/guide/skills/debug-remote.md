# `debug-remote`

> Build a read-only remote evidence pack when the failure is on a deployed environment, then hand the pack to `root-cause`. Never write production.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `docs/agents/project.md` Remote environments (if present), live telemetry (read-only) |
| **Writes** | a remote evidence pack in the session; does **not** write the live environment |
| **Calls** | [`root-cause`](root-cause.md) (after the pack exists) |
| **Called by** | [`root-cause`](root-cause.md) when the failure is already deployed and no pack exists yet |

## When it fires

A failure is reported on **production, staging, or remote dev** and the red signal has to come from live telemetry or a non-prod replay — OpenObserve, traces, spans, a request id, error rate, incident, crash-loop, 500/502. A failing **local** test or CI job stays [`root-cause`](root-cause.md). “Is our tracing complete enough?” is [`assess-observability`](assess-observability.md).

## The Iron Law

```
NO WRITES TO A DEPLOYED ENVIRONMENT
NO MUTATING REPLAY AGAINST PRODUCTION
```

`kubectl exec`, `set image`, SSH, restart-to-add-logs, and `POST` that create carts or charges (including via `port-forward` onto prod) are writes. Promotion is local → `dev` → staging probe of the original symptom → production. A skip-rung hotfix is a **human** override.

## Evidence pack

Required slots: **Identity**, **Phase 1 signal**, **Trace / log join**, **Access**, **Refusals**. Unknowns stay `unresolved`. A missing remote-env block → name `/configure-repo` once.

Valid Phase 1: read-only error-rate / `span_status=ERROR` query; curl against a non-prod copy; captured replay **locally**. Invalid: empty single-id trace search as a close; `kubectl logs` alone as the loop; 100× checkout against production.

Then `root-cause` runs with the pack as its red-capable signal. Fix + `test-first` stay local.

## Why it is written the way it is

`root-cause` already stops guess-and-patch when it is loaded. The recorded failure was **shape**, not will: with only `root-cause`, grok-4.5 port-forwarded production and looped mutating `POST`s as “the red loop,” and both models treated OpenObserve as never Phase 1. The pack recipe names the legal remote signals and makes a mutating prod replay a named refusal.

## See also

- [`root-cause`](root-cause.md) — investigation after the pack
- [`assess-observability`](assess-observability.md) — readiness, not an incident
- [`configure-repo`](configure-repo.md) — where the Remote environments table is written
- [On-ramps](../process/on-ramps.md) — deployed failure vs local failure
