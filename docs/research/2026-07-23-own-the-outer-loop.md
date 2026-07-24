# Research: “Own the Outer Loop” and this skill set

Date: 2026-07-23

## What the primary source says

Addy Osmani’s article is **“Own the Outer Loop: Why loop engineering needs a
human at the boundary,” published July 9, 2026**. The X item is a cross-post;
the author identifies the complete article on his own Substack. [Primary
article](https://addyo.substack.com/p/own-the-outer-loop)

The article’s operating model is: an agent (model plus harness) runs an inner
loop of investigation, implementation, verification, and repetition; evidence
crosses an accountability boundary; a human then decides whether work proceeds.
It names the outer-loop responsibilities **Quality**, **Verdict**, and
**Answerability**. [Primary article](https://addyo.substack.com/p/own-the-outer-loop)

It also places humans in four decision loops—constraints, sampling, audit, and
ownership—and warns that an agent can produce more work than a person can
review. [Primary article](https://addyo.substack.com/p/own-the-outer-loop)

The article names three delegation costs: cognitive surrender, cognitive debt,
and orchestration tax. It proposes attention, bounded scopes, worktrees,
evidence, time-boxing, and opt-in change permissions as countermeasures.
[Primary article](https://addyo.substack.com/p/own-the-outer-loop)

Its codebase-level proposal is an accountability contract recording the
acceptance checklist, decision evidence, accountable person, and system status.
It closes by requiring someone to explain why a change should exist, why it is
safe enough, and what they will do if it is wrong. [Primary
article](https://addyo.substack.com/p/own-the-outer-loop)

## What the pasted summary gets right and misses

The pasted summary accurately captures the central inner/outer-loop framing,
the three named terms, the four human loops, the three delegation costs,
brownfield stewardship, the agency ladder, and the accountability-contract
proposal. [Primary article](https://addyo.substack.com/p/own-the-outer-loop)

It is not a word-complete reading. It omits or compresses substantive passages,
including: capability versus agency; the distinction between process and
quality/back pressure; alpha, decay, taste, and “signature”; the future
unbundling of engineering roles; the article’s “twelve pillars” heading; the
full brownfield inventory; and “New Work is Real Work.” It also blurs two
sources: the article uses Sonar for the 42% code statistic but cites GitLab for
governance moving after code creation. [Primary
article](https://addyo.substack.com/p/own-the-outer-loop)

## Fit with the current repository

The repository already implements much of the proposed evidence boundary:
`verify` requires fresh command evidence before a success claim; `trace` is
required for requirement coverage; `acceptance-check` drives the running system;
and `finish-branch` blocks integration until verification, trace, and acceptance
are satisfied. (`skills/execution/verify/SKILL.md`,
`skills/acceptance/acceptance-check/SKILL.md`,
`skills/ship/finish-branch/SKILL.md`)

The repository also already reserves important decisions for the user:
`finish-branch` presents merge/PR/keep/discard choices, and `release` requires
explicit approval for the version and for tag/push. (`skills/ship/finish-branch/SKILL.md`,
`skills/ship/release/SKILL.md`)

Therefore a separate generic `verdict` skill risks duplicating existing gates
and adding ceremony without changing control. The real gap is narrower: there
is no single durable, human-signed accountability artifact that packages
purpose, evidence, known risk, accountable owner, and response/rollback plan;
nor is there an explicit **narrow/redirect/block** decision before integration.
(`docs/architecture/workflows.md`)

## Conclusions

The strongest candidate is not yet “add a verdict skill.” First decide whether
the desired product is (a) a durable accountability artifact, (b) a mandatory
human authorization gate, (c) a risk-weighted sampling/comprehension loop, or
(d) a policy layer controlling autonomy. Those solve different failures.

For this Production / Active-development repository, a promising design is a
small **accountability-contract** capability integrated into `finish-branch` or
immediately before it. It should assemble existing evidence rather than rerun
checks, surface known unknowns and operational response, and obtain a human
decision. Whether it deserves a standalone skill depends on whether the same
boundary must serve non-branch outputs too; if only Git branches use it, extending
`finish-branch` may be the more coherent design.

## Open decisions

- Is the primary failure to prevent unsafe shipping, loss of human understanding,
  missing audit history, or excessive agent autonomy?
- Must the accountability contract be committed, attached to a PR/release, or
  remain ephemeral?
- Who is allowed to issue the verdict in Solo, Small, and Multi team bands?
- Does every change require the gate, or only changes above a risk threshold?
- Should the capability extend `finish-branch`, become a reusable sub-skill, or
  become a cross-cutting policy consulted by several skills?
