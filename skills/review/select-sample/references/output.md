# Writing the allocation to a file — only on explicit request

Loaded from `SKILL.md`'s **Output** section, and only then: this skill is
conversational by default and writes nothing on its own.

On explicit request only:

1. the user's path
2. else `$TMPDIR`, else `/tmp`

Filename: `YYYY-MM-DD-attention-<slug>.md` (slug from the branch name, else a short range).

If the resolved path is inside `git rev-parse --show-toplevel` → **hard-fail** naming the path. **No silent fallthrough** to another location: an aid that quietly writes into the repo becomes an archive, then an expectation.

Want it again in a later session? **Re-run** over the same range — the allocation is a function of the range and repo state, not of a stored file.
