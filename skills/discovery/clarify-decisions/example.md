# Clarify Decisions — end-to-end shape

Load this example before the first card or close package when no parent supplies
a confirmed exemplar, or when the required output shape is uncertain. The rules
and slots in `SKILL.md` remain authoritative.

## Card

```text
**architecture** · export generation locus

Thread
- Locked so far: comment API stays stable; posture = Run Spike
- This card: where PDF generation runs
- Still open after: guest export auth · stroke storage · plan quota

Territory
- Export is `POST /api/reviews/:id/export`, session-auth only today.
- Gateway idle timeout is 30s; large reviews with drawings already time out
  similar heavy handlers on the request thread.
- Workers already exist for transcode (`jobs/transcode`); no export job yet.

Where should export generation run?

Why it matters
- Wrong pick rewrites API shape and operations mid-build: queue versus sync
  versus client-only, with a 30s gateway limit on the request thread.

Closes: known-unknown

Criteria (graders)
- A 400-comment export with drawings completes without the gateway 30s kill.
- Unpredictable size stays within an existing operations pattern.

- **Sync in the API request** — simplest; large exports time out.
- **Background job on the existing queue** (Recommended) — reuses transcode
  worker patterns; needs a ready notification.
- **Client-side only** — zero backend; limits formats and supportability.

Recommended: background job — meets both graders; sync fails the timeout
grader; client-only fails format coverage.
```

## Close excerpt when Coverage ON

(Only when `SKILL.md` Production coverage gate is ON and
`production-coverage.md` was loaded.)

```text
Success / done signal
- Creators open drafts from Finder without publishing.
- Entitled learners continue reading published courses unchanged.

Boundaries
- Off limits: widen the learner route; treat menu visibility as authz.
- Must keep working: ARCH-3 learner projection; server reauth on mutations.

Spine touch
- Respects: ARCH-3

Coverage final
- Frame Clear · Journey Clear · Contract Clear · Reliability Clear
- Failure Accepted-risk (IC) · Operate Clear · Freeze Clear

Owned unknowns
- none

Accepted risks
- Single-AZ cache miss may elevate latency within the SLO burn; signer: IC.

Operability touch
- Rollback: revert the catalog route feature flag.
- Page: on-call for catalog 5xx burn above the approved threshold.

Is this the shared picture?
```
