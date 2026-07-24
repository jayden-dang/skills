# DEC field whitelist (read-only)

Load when enriching a packet from `docs/decisions/`.

## Selection

- **No-op** if no `docs/decisions/` or no records (and no adoption substrate).
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
| `Evidence:` | kinds ∈ `commit` \| `tag` \| `pr` \| `ci` \| `release` only |
| `Promoted-Evidence:` | Optional; never present as human judgment |
| Withheld sentinel | Show withheld honestly; never invent risk prose |

## Forbidden

Create, edit, reissue, supersede, or `validate-records.sh --mode=publish`. Never rewrite payload or envelope bytes. Never invoke `record-decision`.
