# 0003 — Change authoring is split from the publication crossing

`land-branch` already owns every branch crossing behind a prove-claim/audit-trace/acceptance
gate, a verbatim five-option menu, and a record-before-crossing rule, but it authors
no commit message and no PR body. **Decision:** `package-change` authors content and
mutates only local git, handing a file-based package to `land-branch`, which alone
pushes and opens the pull request. **Why:** a self-contained ship skill would need its
own copy of the publication gate — a second copy that drifts from the first, and one
that could not ask for a missing ticket to be filed anyway, since ARCH-5 forbids a
model-invoked skill from invoking user-invoked `/publish-issues`.
