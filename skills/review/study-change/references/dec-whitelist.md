# DEC field whitelist (read-only)

WHEN `study-change` is enriching a packet from `.skills/decisions/` or citing
a DEC, read this file and follow it exactly.

## Selection

- **No-op** if no `.skills/decisions/` or no records (and no adoption substrate).
- **Auto:** forward-cite only — mechanical `DEC-YYYYMMDD-XXXXXX` in commit messages, PR body (if local), branch notes, or files in the **resolved range**. Cap auto set at **≤5**, newest-by-id first.
- **Explicit** user DEC ids always included when files exist (explicit wins over cap if needed).
- **Never:** same-feature fill, recent-N fill, reverse-link (record → commits), LLM “relatedness”.

## Fields to surface (RECORD.md tokens)

| Token | Rule |
|---|---|
| `DEC-*` id / filename stem | Always cite when used |
| `Scope:` | Include when present |
| `Boundary-Type:` | Include when present |
| `Verdict:` | Include when present |
| `Human-Accepted-Risk:` | Quote **verbatim**; label human-authored |
| `Human-Response-If-Wrong:` | Quote **verbatim**; label human-authored |
| `Evidence:` | kinds ∈ `commit` \| `tag` \| `pr` \| `ci` \| `cut-release` only |
| `Promoted-Evidence:` | Optional; never present as human judgment |
| Withheld sentinel | Show withheld honestly; never invent risk prose |

## Forbidden

Create, edit, reissue, supersede, or `validate-records.sh --mode=publish`. Never rewrite payload or envelope bytes. Never invoke `record-verdict`.
