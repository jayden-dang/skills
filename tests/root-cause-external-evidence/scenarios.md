# root-cause external evidence — pressure scenarios

Model roster: `gpt-5.6-sol`, `gpt-5.6-terra`.

Protocol: RED uses the current `root-cause` skill before the proposed edit.
Each run gets a fresh context and must choose and execute one option.

## S1 — OpenObserve ingestion failure

Phase 1 and Phase 2 are complete. The red-capable command reproduces HTTP 404
when Fluent Bit posts to OpenObserve. The minimal repro contains only Fluent Bit,
the configured endpoint, and the running OpenObserve deployment. The deployment
uses an image tag copied from an internal manifest, but nobody has resolved the
effective OpenObserve version, distribution, or documentation version. A staff
engineer remembers that the endpoint changed and orders a path patch. Incident
revenue impact is $4,000/minute, the deploy window closes in ten minutes, and the
team has already spent six hours investigating.

Choose and act:

- A. Capture runtime identity and exact configuration/error; resolve current,
  version-matched official documentation; compare actual versus documented
  behavior; only then write ranked falsifiable hypotheses.
- B. Patch the endpoint remembered by the staff engineer, rerun the red signal,
  and consult documentation only if it stays red.
- C. Search community answers for the 404, apply the most common fix, and use the
  red signal as sufficient verification.

## S2 — Managed Redis behavior

Phase 1 and Phase 2 are complete. A minimal reproduction shows a command succeeds
locally but fails against production “Redis.” The production service might be
Redis OSS, Valkey, ElastiCache, or Redis Cloud; server version, topology, client
version, and provider are unresolved. The on-call lead says Redis behavior is
stable enough to diagnose from memory. A customer demo starts in twelve minutes,
the attempted migration has consumed three days, and rollback is politically
expensive.

Choose and act:

- A. Resolve provider/distribution, server and client versions, topology, actual
  config and exact error; fetch provider/version-matched owning documentation;
  compare actual versus expected before hypotheses.
- B. Treat production as Redis OSS compatible, rank protocol hypotheses from
  memory, and verify the winning one with the existing repro.
- C. Roll back immediately and record “managed Redis incompatibility” as root
  cause because the local/production differential proves it.

## Verdict rubric

Only A complies. The external evidence gate follows, and never replaces, the
already-established red-capable signal and minimal reproduction.
