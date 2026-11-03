Read-only. Change no file, spawn no subagent, send no message.

You audit the scope of a feature spec before it is built. Follow these steps in order.

Repo: {WT}
Read `docs/product/vision.md`, the roadmap's milestone block for {ROAD}, and {SPEC}/requirements.md, design.md, tasks.md. Open the code when a step needs it. Read nothing under `.skills/`, except the Lock list in {RUN}/charter.md.

1. Write the person's task from the milestone outcome as numbered real steps, from first setup through a normal day and one failure. Use only what the repo states. Invent no quotes or personas.
2. For each story, and any requirement that looks separable, name the task step it serves, or "none".
3. Deletion test: if this were removed, what concretely breaks for that person, and how often? Cite `file:line` or a requirement. "It would be less complete" is not breaking. Read every trigger the requirement lists before you say when it matters.
4. Check whether existing code, or a tool the harness or OS ships, already does the job. Cite it.
5. Class each: REQUIRED for the outcome / SAFETY the outcome depends on / OPTIONAL. For each OPTIONAL give the IDs and tasks removed if cut, what the person loses, and whether a Lock requires it.
6. Walk the task from the first step: name anything it needs that no requirement covers, with the step it fails at.

Under 350 words: the task list, a table for step 5, then the missing items. If nothing is optional, say so plainly.
