# understand

> Explains how a feature, component, function, or change works — from the real
> code, in a form you can take in at a glance. Replaces the five earlier
> learning skills (see `CHANGELOG.md`, 2026-10-06).

| | |
|---|---|
| **Invocation** | Model-invocable — just ask ("how does refunds work?", "walk me through this PR"). `/understand <subject>` also works |
| **Calls** | `craft-page` (the diagram and page design); `research` when an outside fact decides the answer |
| **Writes** | `.skills/understand/<slug>.html` (local, git-ignored), only when the subject spans 3+ files |
| **Source** | [`skills/discovery/understand/SKILL.md`](../../../skills/discovery/understand/SKILL.md) |

## How to use it

Ask in your own words and your own language. There is no setup, no mode to
pick, and no questions before the answer.

| You ask | You get |
|---|---|
| How does the refunds feature work? | The gist in chat, a page link, one question |
| What does `gateway.refund` do? | A short chat answer about the function, its calls, and its callers; a page only if that crosses 3+ files |
| What does this diff / PR / branch change? | The page marks changed nodes; the walk shows before → after |
| Teach me this build (after `.skills/<CODE>/` exists) | The page adds **How it was built** from `implementation-notes.md` |
| How does OAuth PKCE work? (not in the repo) | Same shape; outside facts carry source links |
| Quiz me on it | One question at a time, graded against the code |
| Go deeper on the worker | The worker becomes the new subject |

Answer the closing question if you want to check yourself. The reply says right
or wrong and cites the line that settles it.

## The page

Five sections, in order: **In short** · **Map** (the path as a diagram, each
box labelled `file:line`) · **Walk one example** (Back / Next through real
code with real values) · **Surprises** · **Check yourself** (3 questions,
answers hidden).

## Why it looks like this

The shape follows Andrej Karpathy's ladder for reading LLM output (Oct 2026):
plain controlled language (a softened ASD-STE100), then a diagram, then an
interactive page — each easier to take in than the last. Two things the ladder
leaves out are added: every claim is tied to a line of code you can open, and
the answer ends on a question, because watching an explanation feels like
understanding long before it is.

Baselines (see `TESTS.md`) found the old learning skills already *found* the
right things in the code. What failed was the delivery: prose only, no picture,
setup questions before any answer, and process words in the reply.

## Not this skill

- **Why** the code was designed this way → [`why`](why.md)
- Choosing between options in a live discussion → [`interpret-session`](interpret-session.md)
- Working a problem to a decision → [`work-the-problem`](work-the-problem.md)
