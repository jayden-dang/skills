# Runtime binding and lease preflight

Loaded from `SKILL.md` **Runtime binding and lease preflight** after session
preflight and before the first dispatch (or, on the inline route, before the
first production edit). Planning artifacts remain portable; the runtime
snapshot records what this session can really do.

Write `.skills/<CODE>/execution-session.json`:

```json
{
  "schema_version": 2,
  "harness": "unknown",
  "model": "unknown",
  "resume_context": "supported|unsupported|unknown",
  "worktree_isolation": "supported|unsupported|unknown",
  "effective_concurrency": null,
  "concurrency_reason": null,
  "rotations": []
}
```

Use capability facts exposed by the active harness/API. Record `unknown` when a
fact is unavailable; never infer support from a harness name or a model family.

**Resume or start fresh.** Resume a worker or reviewer only while
`resume_context` is `supported` and none of these holds; otherwise start a fresh
context from the feature capsule and task delta, never the prior transcript:

- the semantic unit ends or the next task materially changes required context;
- the role's retained context is near the model's context limit;
- compaction, harness change, broad scope/invariant change, or context confusion
  invalidates the retained context.

Each fresh start appends a rotation record: reason, previous lease ID, next lease
ID.

**Concurrency.** If a ready set cannot safely fan out because
`worktree_isolation` is not `supported` or surfaces overlap, set
`effective_concurrency` to one and write the cause in `concurrency_reason`.
Never increase concurrency beyond the approved plan.
