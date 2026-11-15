#!/usr/bin/env python3
"""score.py <m1|m2> <answers.txt> — check a routing reply against the expected owner of each message."""
import re, sys
A="board show-run-status refresh-roadmap-status chart-progress brief-road board root-cause plan-milestones show-run-status board frame-change refresh-roadmap-status inspect-change chart-progress understand speak-outer board show-run-status refresh-roadmap-status chart-progress craft-page|NONE|frame-change plan-milestones".split()
B="idea triage sweep-backlog publish-issues write-handoff assess-milestone audit-shipped record-debt scan-architecture evolve-system frame-change root-cause board inspect-change vet-feedback plan-milestones speak-outer polish-diff assess-observability plan-tasks idea triage sweep-backlog publish-issues write-handoff assess-milestone audit-shipped record-debt scan-architecture evolve-system understand frame-change|design-solution".split()
C="forge-goal forge-prompt interpret-session reflect define-project define-system-doc assess-pivot-impact map-features bootstrap-repo configure-repo tune-rust-loop frame-change understand why vet-source root-cause define-domain plan-milestones write-handoff clarify-decisions research forge-goal forge-prompt interpret-session reflect define-project define-system-doc assess-pivot-impact map-features bootstrap-repo configure-repo tune-rust-loop".split()
E="shape shape go go cut-release cut-release tend-pr tend-pr no-comments zone-mode author-skills author-skills polish-diff NONE|frame-change|clarify-decisions|forge-prompt|understand deliver-issues vet-feedback land-branch specify-behavior|frame-change root-cause polish-diff brief-road idea".split()
exp = (A+B) if sys.argv[1]=="m1" else (C+E)
got = dict((int(n), s) for n, s in re.findall(r"^\s*(\d+)\.\s*`?([A-Za-z-]+)`?", open(sys.argv[2]).read(), re.M))
bad = [(i+1, e, got.get(i+1)) for i, e in enumerate(exp) if got.get(i+1) not in e.split("|")]
print(f"{len(exp)-len(bad)}/{len(exp)} as expected"); [print("  miss", b) for b in bad]
