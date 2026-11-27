# The parts of a system architecture

One row of the note's **Parts** table per part below, in this order. A part
depends on the parts above it: decide data authority before caching it, and
communication before messaging over it.

| # | Part | Pin before choosing | A keeping check usually looks like |
|---|---|---|---|
| 1 | **Code structure** — modules, layers, dependency direction, where business rules live | Team size, how features are split, what is shared | An import or dependency lint that fails on a forbidden edge |
| 2 | **Data** — the owner and source of truth for each kind of data, transactions, consistency, schema migrations, tenancy | Which writes must be atomic together, which reads must never be stale, how data is split between customers | Schema constraints, a test that a second writer is rejected, a migration check in CI |
| 3 | **Identity and permissions** — authentication, where each permission is enforced, tenant isolation | Who the actors are, what one tenant must never see of another | A test that an unscoped query or an unauthenticated call fails |
| 4 | **Communication** — synchronous calls, protocols, contracts and their versioning, the error model, timeouts | Latency budget, which callers need an answer now, who owns each contract | A contract test, a lint that every outbound call has a timeout |
| 5 | **Messaging and background work** — queues, events, delivery guarantees, idempotency, ordering, retries, dead letters, scheduled jobs | The delivery guarantees of every outside system, what a duplicate or a lost message costs, peak volume | A test that a redelivered message has one effect, a unique key on each side effect |
| 6 | **Caching** — what is cached, where, its expiry and invalidation, stampede protection, what happens when the cache is down | How stale each value may be, how often the source changes, the source's rate limits | A test or `grep` that fails when a never-cache value is read through the cache |
| 7 | **Failure and recovery** — retries and backoff, degraded modes, backup and restore, the recovery owner | What must survive a crash, how much data loss and downtime is acceptable | A restore drill with its date, a test of each degraded path |
| 8 | **Observability** — logs, traces and metrics conventions, the identifiers that tie them together, alerts | What an on-call person needs to tell a broken request from a slow one | A test or lint that each entry point carries the request identifier |
| 9 | **Configuration, secrets and deployment** — environments, where secrets live, the process and host topology | Hosting, who deploys, what differs between environments | A secret scan in CI, a check that config is read only at startup |
| 10 | **Test architecture** — the seams tests run against, where fakes are allowed, what runs against real infrastructure | Which boundaries are expensive or nondeterministic | A rule in the test setup that rejects a fake of an internal module |
| 11 | **Evolution** — versioning, feature flags, backward compatibility, deprecation | Who consumes each interface, how old clients can be | A compatibility test against the previous contract version |
| 12 | **Principles** — the cross-cutting rules not owned by one part above | The project's recurring trade-off (speed, cost, safety, simplicity) | Each principle points at the check of the part it governs, or names the review step |
