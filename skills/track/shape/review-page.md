# The review page

One self-contained `RUN/review.html` the operator can approve or reverse from. REQUIRED SUB-SKILL: use `craft-page`,
treatment Utilitarian, with a sequence or flowchart as the primary figure. Write it in the language the operator
writes to you in. Code identifiers stay verbatim. Every value comes from a file or a command output you read.

The parts, in this order, each one present:

1. **Header.** Feature, ticket, branch at commit, and in one sentence: agents reviewed this, the operator has not.
2. **What changes for you.** Today and after, side by side, in the person's words, with what they will newly see.
3. **What the agents got wrong.** Each `RUN/audit.md` finding: the claim, what the file really says. None → say what was checked.
4. **You decide.** One card per `agent-decided` line and per Weigh that reached a requirement, biggest consequence first:
   what was picked; the risk; if reversed, which IDs and tasks change; your lean, labelled as yours; radio buttons.
5. **Could this be smaller?** The advisor's OPTIONAL items as cards: IDs and tasks saved, what the person loses, the Lock
   that requires it, Keep / Cut, and your note on any claim the file contradicted. Below them, what the advisor found missing.
6. **What it touches.** Files outside the repo, with what each holds today from reading it, and when it changes. Repo areas with
   the guard protecting each. What it leaves alone, and what it does not do.
7. **When it runs.** The primary figure of one normal path, then a table: situation, what the person sees, requirement.
8. **Why trust this, and how far.** Each gate's rounds and what interpret made them change; the receipt's `ran`, `subagents`,
   `missing` lines verbatim; the limits (same model, picks it approved itself); what nobody has verified.
9. **The report after the build.** A frame marked as not yet run: what the person can do, the test that will prove it, an empty
   result cell per row; slots for where code left the spec and what agents decided while building; the checks only the operator can run, each with its command and what right looks like.
10. **Detail.** Stories with their ID ranges and the task list, collapsed. The spec's paths.

A panel that stays in view holds links to the parts, a count of open choices, and a read-only text box the choices write
into, with a copy button: the reply to paste back, naming each choice by its card and listing the audit findings to fix.
