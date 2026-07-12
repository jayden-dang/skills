---
name: grilling
description: Use to interview the user to stress-test a plan, design, or feature idea
  before anything is built, when their intent is underspecified and the
  decisions must be drawn out of them, when the user asks to be grilled or
  interviewed, or when another skill calls for an interview.
---

# Grilling

Interview the user about every aspect of the plan until you both hold the same picture of it.

- **One question per message.** Ask, then wait for the answer before the next question. A wall of questions is bewildering; a single question gets a real answer.
- **Every question ships with your recommended answer** and a one-line reason. The user can accept in two words or push back.
- **Walk every branch of the decision tree.** Decisions depend on each other — an early answer opens some branches and closes others. Resolve them in dependency order and keep going until no unexplored branch remains.
- **Facts are yours; decisions are the user's.** If the answer already exists in the codebase or the docs, look it up — never ask the user to recall what you can read. Anything that is a judgment call goes to the user, one at a time, and you wait.
- **Do not enact anything** — no code, no files, no plan execution — until the user explicitly confirms you have reached a shared understanding.

## Done when

You have played the settled decisions back as a numbered list and the user has explicitly confirmed it, with no branch left unexplored. Silence is not confirmation; an assumption you never put to them is an unasked question.
