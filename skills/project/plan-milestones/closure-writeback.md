# Closure write-back

WHEN a `Committed → Closed` transition has just passed the closure `<HARD-GATE>` in
`SKILL.md`'s Update section, follow this exactly.

Then write into `Closed:` the SHA **read from the assessment file**, verbatim — not the one
the write-handoff carried. Where the two ever diverge, the file is the record and the write-handoff is
hearsay. That marker is how a later reader resolves what shipped in the milestone.

Never re-run the assessment, and never append a block to the assessment file: this skill
reads that file and writes only the roadmap.

**WHEN you showed the close diff with the verdicts, and the reply accepts or overrides each
verdict with `Close` and says it approves that diff ("approve", "approved"):** write exactly
that diff. Before committing, read `git diff -- docs/roadmap/INDEX.md`. When it holds the lines you showed and nothing
else, `Status:` stays `Approved`: the demotion and the approval land in the same commit. Walk
S1–S10, commit, then REQUIRED SUB-SKILL: use `refresh-lanes`. Any other line in that diff means
Draft and **## The approval gate**. So does a reply that accepts without the word approve,
even when your last turn offered it as the approving reply.
In the baseline, the owner was told "approve the roadmap with those closes. I don't need to see
it again" before any diff had been shown. Both runs then emptied `## Focus`, one also rewrote
`Date:`, and both kept `Approved` over lines the owner had never seen.

Otherwise run **## The approval gate** as usual. The assessment gate is additive and precedes
it, never replaces it.

Every other update — a new milestone, a reorder, a reword, a commitment, a deferral — reaches
the approval gate exactly as before. This gate fires on closure alone.
