---
type: config
id: POS-CONFIG
title: Personal OS config
status: active
---

# Personal OS — profile (example)

Copy into your vault (path chosen at setup). **Edit for your machine.** Skills read this file; they must not hardcode layout.

```yaml
personal_os_version: 1

# Named external roots (optional) — only paths the user provides
roots:
  code: null              # e.g. a parent folder of product repositories
  sandbox: null           # ephemeral experiments; never auto-WIP
  eng_learning: null      # craft study materials outside the vault

layout:
  system_dir: 00-System/personal-os
  inbox_dir: 01-Inbox
  daily_dir: 02-Daily
  reviews_dir: 03-Reviews
  areas_dir: 10-Areas
  projects_dir: 20-Projects
  projects_active: 20-Projects/active
  projects_waiting: 20-Projects/waiting
  projects_done: 20-Projects/done
  learning_dir: 30-Learning
  learning_tracks: 30-Learning/tracks
  learning_logs: 30-Learning/logs
  resources_dir: 40-Resources
  archive_dir: 50-Archive
  registry_dir: 00-System/personal-os/registry
  templates_dir: 00-System/personal-os/templates
  dashboards_dir: 00-System/personal-os/dashboards
  charter_path: 00-System/personal-os/life-charter.md

limits:
  max_active_projects: 5
  max_daily_focus: 3
  max_weekly_p0: 3
  deep_block_min: 45

integrations:
  git_status_in_weekly_review: false
  agent_may_implement_projects: false
  sync_workspaces_auto_create: false

sync_workspaces:
  scan_roots: []
  max_depth: 4
  ignore_globs:
    - "**/node_modules/**"
    - "**/.git/**"
```

If your vault uses different folder names, change `layout.*` only — do not fork skill bodies.
'''

