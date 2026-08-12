---
name: life-capture
description: Use when the user has a raw thought, task, link, or worry to park — creates one unprocessed inbox note without organizing it.
---

# Capture

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Recipe

1. Create one file under `layout.inbox_dir` (inbox template if available).
2. Frontmatter REQUIRED: `type: inbox`, `processed: false`, `created` date.
3. Body = raw user text only.

## Do not

- Classify, prioritize, open projects, or rewrite into "clean" tasks.

## Done when

Exactly one new inbox note exists with `processed: false`.
