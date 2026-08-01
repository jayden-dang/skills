# ADR-0009: Vet product flow is judgment, not an ARCH-1 vertical check

**Context:** Guide “completeness before dogfood” could be implemented as a
mechanical schema/kind/req-id pass (audit-trace style) or as an LLM map of
shipped user-observable surfaces. ARCH-1 forbids claiming LLM judgment as a
vertical check.

**Decision:** `vet-product-flow` is an isolated **judgment** skill. Its product
claim is code-grounded missing-situation findings. Freshness of the report uses
an exact authored-cases fingerprint recipe; that recipe is not sold as
“complete for real users.” Optional CLI hygiene stays out of v1 claim.

**Why:** Mechanical counts create false confidence under Production posture;
same-agent self-check fails isolation; dogfood still owns novelty, feel, and
FE+BE evidence.
