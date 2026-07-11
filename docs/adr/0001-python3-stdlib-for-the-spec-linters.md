# 0001 — Python 3.9 stdlib for the spec linters

**Context.** The linters (`check-trace`, `check-graph`, `vendor-linters`) are vendored into
every consuming repo and run in its hooks and CI, so their runtime is a tax on every user —
and Claude Code is a native binary that puts no `node` on PATH. On macOS, `/usr/bin/python3`
and `/usr/bin/git` are byte-identical Command Line Tools shims, so anyone who can run this
git-based skill set already has Python 3; Node is a separate, deliberate install. Node also
ships no XML parser, and the next feature (COVER) must tolerantly parse JUnit XML — a format
with no formal specification — under a zero-dependency rule.

**Decision.** The three linters are Python 3.9+, stdlib only. The bash scripts (`task-brief`,
`review-package`, `link-skills.sh`, `session-start.sh`) stay bash: they are already
runtime-free, and porting them would *add* a dependency.

**Why 3.9, and what it costs.** 3.9.6 is what macOS CLT ships, so it is the floor — no `match`
statement, no `X | Y` runtime unions. Windows ships neither runtime, and `npx skills@latest`
still touches Node once, so `git clone` + `link-skills.sh` and the Claude Code plugin become
the primary install paths. We use `xml.etree.ElementTree` despite Python's entity-expansion
warning and decline `defusedxml`: the input is a JUnit report our own suite generated seconds
earlier, not untrusted data.
