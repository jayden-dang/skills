# The review page

One self-contained `RUN/review.html`, written when the spec is closed. The operator reads it, then types `approve`
or says what to change. It has no input controls: no radio buttons, no checkboxes, no text box to copy. REQUIRED
SUB-SKILL: use `craft-page`, treatment Utilitarian, with a sequence or flowchart as the primary figure. Write it in the
language the operator writes to you in. Code identifiers stay verbatim. Every value comes from a file or a command output you read.

Parts 1 to 5 stay open and hold under 800 words together; a real page ran to 5,310. The rest stay collapsed.

1. **Header.** Feature, ticket, branch at commit, and in one sentence: agents closed this spec, the operator has not read it.
2. **What changes for you.** Today and after, side by side, in the person's words, with what they will newly see.
3. **Needs you.** At most 5 items, biggest consequence first, from `agent-decided` lines where reversing changes what
   the person sees or does, or where the final review could not settle it. Each: what was picked, the risk, what
   reversing changes, your lean labelled as yours. When `work` declined any OPTIONAL cut, one item is always the largest
   it declined, by plan lines, with its IDs: authors judged their own text, and one run declined all 7. None → say so.
4. **What the final review changed.** From `RUN/final-review.md`: how many items, how many applied or rejected, and the two or three that
   changed the spec most, each as what it found and what it did.
5. **When it runs.** The primary figure of one normal path.

Collapsed:

6. **Decided for you.** Every other `agent-decided` and Weigh value: one table row each, with its IDs.
7. **What it touches.** Files outside the repo, with what each holds today from reading it, and when it changes. Repo areas with
   the guard protecting each. What it leaves alone. What it does not do.
8. **When something fails.** Situation, what the person sees, requirement.
9. **How far to trust this.** Each gate's rounds; the receipt's `ran`, `subagents`, `missing` lines verbatim; every final-review
   item with its outcome; Lock-required items the advisor would cut, one line each; the limits (same model, picks it approved itself); what nobody has verified.
10. **The report after the build.** A frame marked as not yet run: what the person can do, the test that will prove it, an empty
    result cell per row; slots for where code left the spec and what agents decided while building; the checks only the operator can run, each with its command and what right looks like.
11. **Detail.** Stories with their ID ranges, the task list, the spec's paths.

The page ends on one line: type `approve`, or say what to change in plain words.
