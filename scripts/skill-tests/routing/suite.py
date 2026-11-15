#!/usr/bin/env python3
"""suite.py build <outdir> | score <outdir> <file> <answers.txt> — the frozen routing set and its expected owners.

Messages come from the four cluster files, the trim-check file, and the older skills' own trigger evals.
Owners follow the 2026-11-15 merges. A message whose skill was deleted is dropped.
"""
import glob, json, os, re, sys
R = "scripts/skill-tests/routing/"
MERGED = {"show-run-status": "board", "chart-progress": "refresh-roadmap-status", "brief-road": "refresh-roadmap-status",
          "forge-goal": "forge-prompt", "define-system-doc": "define-project", "assess-pivot-impact": "define-project",
          "bootstrap-repo": "configure-repo", "reflect": "author-skills", "no-comments": "polish-diff", "deliver-issues": "go",
          "amend-feature": "frame-change", "draft-ux": "draft-ui", "validate-api": "validate-feature", "validate-ui": "validate-feature",
          "build-by-story": "build", "build-in-waves": "build", "build-inline": "build"}
GONE = {"zone-mode", "sweep-backlog", "publish-issues"}
KEYS = {
 "a": "board show-run-status refresh-roadmap-status chart-progress brief-road board root-cause plan-milestones show-run-status board frame-change refresh-roadmap-status inspect-change chart-progress understand speak-outer board show-run-status refresh-roadmap-status chart-progress craft-page|NONE|frame-change plan-milestones",
 "b": "idea triage sweep-backlog publish-issues write-handoff assess-milestone audit-shipped record-debt scan-architecture evolve-system frame-change root-cause board inspect-change vet-feedback plan-milestones speak-outer polish-diff assess-observability plan-tasks idea triage sweep-backlog publish-issues write-handoff assess-milestone audit-shipped record-debt scan-architecture evolve-system understand frame-change|design-solution",
 "c": "forge-goal forge-prompt interpret-session reflect define-project define-system-doc assess-pivot-impact map-features bootstrap-repo configure-repo tune-rust-loop frame-change understand why vet-source root-cause define-domain plan-milestones write-handoff clarify-decisions research forge-goal forge-prompt interpret-session reflect define-project define-system-doc assess-pivot-impact map-features bootstrap-repo configure-repo tune-rust-loop",
 "e": "shape shape go go cut-release cut-release tend-pr tend-pr no-comments zone-mode author-skills author-skills polish-diff NONE|frame-change|clarify-decisions|forge-prompt|understand deliver-issues vet-feedback land-branch specify-behavior|frame-change root-cause polish-diff brief-road idea",
 "t": "plan-milestones plan-milestones plan-milestones plan-milestones inspect-ui inspect-ui craft-page craft-page understand understand validate-feature validate-feature debug-remote research make-video reroute-plan reroute-plan audit-trace load-subgraph inspect-invariants run-dogfood write-dogfood realign-spec interpret-session",
 "o": "clarify-decisions frame-change define-domain !research !research research understand assess-observability debug-remote build-by-story build-in-waves build-in-waves build-by-story build-inline build-inline debug-remote root-cause speak-outer !speak-outer vet-source !vet-source land-branch !land-branch plan-tasks design-solution brief-road",
}
live = {os.path.basename(os.path.dirname(p)) for p in glob.glob("skills/*/*/SKILL.md")}
def owner(e):
    return "|".join(sorted({("!" if x.startswith("!") else "") + MERGED.get(x.lstrip("!"), x.lstrip("!")) if MERGED.get(x.lstrip("!"), x.lstrip("!")) in live | {"NONE"} else x for x in e.split("|")}))
def msgs(k):
    f = R + f"cluster-{k}-messages.md" if k != "o" else R + "older-trigger-evals.md"
    return [m[1] for m in re.findall(r"^(\d+)\. (.*)$", open(f).read(), re.M)]
def build(out):
    rows = []
    for k in "abceto":
        for m, e in zip(msgs(k), KEYS[k].split()):
            if set(e.lstrip("!").split("|")) & GONE: continue
            rows.append((m, owner(e)))
    half = (len(rows) + 1) // 2
    for name, part in (("s1", rows[:half]), ("s2", rows[half:])):
        open(f"{out}/{name}.md", "w").write("\n".join(f"{i+1}. {m}" for i, (m, _) in enumerate(part)) + "\n")
        json.dump(part, open(f"{out}/{name}-key.json", "w"), indent=1)
    print(len(rows), "messages:", half, len(rows) - half)
def score(out, name, ans):
    key = json.load(open(f"{out}/{name}-key.json"))
    got = dict((int(n), s) for n, s in re.findall(r"^\s*(\d+)\.\s*`?([A-Za-z-]+)`?", open(ans).read(), re.M))
    bad = []
    for i, (m, e) in enumerate(key, 1):
        g = got.get(i)
        ok = (g not in [x[1:] for x in e.split("|")]) if e.startswith("!") else (g in e.split("|"))
        if not ok: bad.append((i, e, g, m[:70]))
    print(f"{name}: {len(key)-len(bad)}/{len(key)}"); [print("  miss", b) for b in bad]
if sys.argv[1] == "build": build(sys.argv[2])
else: score(*sys.argv[2:5])
