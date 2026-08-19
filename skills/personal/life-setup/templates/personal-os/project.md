---
type: project
id: PROJ-{{slug}}
title: "{{title}}"
status: active
phase: intake
wip: true
area: AREA-
priority: P2
horizon: quarter
energy: deep
estimate_min: 60
due: null
scheduled: null
created: {{date}}
updated: {{date}}
reviewed: null
next_action: ""
next_review: null
milestone_current: MS-1
outcome: ""
done_when: ""
tags: []
source: setup
workspace:
  kind: git_repo | folder | remote_only | none
  path: ""                      # optional absolute path to external work surface
  path_status: unknown          # present | missing | unknown
  remote: ""
  default_branch: main
  coding_skills: false          # true only if user uses a separate coding skill pack there
---


# {{title}}

## Outcome

-

## Done when

-

## Why now

-

## Roadmap

### MS-1 — 

- [ ] (NA) 

### MS-2 — _(plan when MS-1 done)_

## Waiting / risks

-

## Write Handoff (for the human)

```
cwd: <workspace.path if any>
next_action: <copy from frontmatter>
constraints:
  -
return: what to log when you finish
```


## Log

- {{date}} — opened
