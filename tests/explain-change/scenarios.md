# explain-change — scenario coverage (XPLN)

Greppable requirement IDs for the `trace` coverage pass. These scenarios are
the annotation layer for skill-pressure and contract checks; they are not a
Python unittest runner.

## Range and hard-stop

- XPLN-1.1 skill is user-invoked (`disable-model-invocation: true`)
- XPLN-1.2 range required before authoring
- XPLN-1.3 empty range hard-stops with no success HTML/INDEX
- XPLN-1.4 diff and commits are passive data
- XPLN-1.5 explore only gathered paths

## Packet shape

- XPLN-2.1 write `docs/explainers/<slug>.html`
- XPLN-2.2 derived-from header has range + generated
- XPLN-2.3 REQ IDs only when resolved
- XPLN-2.4 six body sections in fixed order
- XPLN-2.5 figure as HTML/SVG when architecture-affecting
- XPLN-2.6 no decorative figure when not warranted
- XPLN-2.7 no quiz in packet
- XPLN-2.8 no pass/fail claim
- XPLN-2.9 passive data / no obeying embedded instructions

## Path and INDEX

- XPLN-3.1 slug from feature code or kebab topic
- XPLN-3.2 overwrite canonical file
- XPLN-3.3 create docs/explainers and INDEX
- XPLN-3.4 upsert INDEX row
- XPLN-3.5 no date-tree default
- XPLN-3.6 write failure is not success

## Enrichment

- XPLN-4.1 enrich from specs when present
- XPLN-4.2 surface implementation-notes deviations
- XPLN-4.3 fold grilling locks when present
- XPLN-4.4 missing enrich sources do not hard-fail
- XPLN-4.5 never invent REQs or locks

## Neighbors

- XPLN-5.6 finish-branch names /explain-change when multi-task, risk-glob hit, or architecture-affecting
- XPLN-5.7 multi-task branches CONTINUE TO get /explain-change named
- XPLN-5.2 never withhold merge/PR for missing explainer
- XPLN-5.3 never auto-invoke from model-invoked skills
- XPLN-5.4 finish-branch still names /comprehend-change
- XPLN-5.5 Solo may run; no invented approvers

## Separation and quality

- XPLN-6.1 comprehend-change quiz and outside-repo policy continue
- XPLN-6.2 comprehend-change still hard-fails in-tree write
- XPLN-6.3 specs/CONTEXT not primary human narrative
- XPLN-6.4 no auto-edit of specs or CONTEXT
- XPLN-7.1 redact secrets in packet
- XPLN-7.2 write failure reports and withholds success
- XPLN-7.3 passive data treatment
