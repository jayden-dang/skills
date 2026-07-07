# Requirements: <Feature Name>

Feature code: <CODE>
Status: Draft
Date: <YYYY-MM-DD>

<!--
Rules:
- Feature code: 2-12 chars, A-Z0-9, starts with a letter, unique repo-wide.
  Register it in docs/specs/INDEX.md before use.
- Every acceptance criterion gets a hierarchical ID: <CODE>-<story>.<criterion>.
- Criteria use EARS phrasing:
    WHEN <event/condition> THE SYSTEM SHALL <behavior>          (event-driven)
    WHILE <state> THE SYSTEM SHALL <behavior>                   (state-driven)
    IF <unwanted condition> THEN THE SYSTEM SHALL <behavior>    (unwanted behavior)
    WHERE <feature is included> THE SYSTEM SHALL <behavior>     (optional feature)
    THE SYSTEM SHALL <behavior>                                 (ubiquitous)
- Guard requirements protect existing behavior this feature touches:
    WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing behavior>
- IDs are immutable once Status is Approved. Retire a requirement by striking it
  through (~~**CODE-N.M**~~ reason) — never renumber.
-->

## 1. <Story title>

**Story:** As a <actor>, I want <capability>, so that <benefit>.

- **<CODE>-1.1** WHEN <event> THE SYSTEM SHALL <behavior>.
- **<CODE>-1.2** IF <unwanted condition> THEN THE SYSTEM SHALL <behavior>.

## 2. <Story title>

**Story:** ...

- **<CODE>-2.1** ...
- **<CODE>-2.2** (guard) WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing behavior>.

## Out of Scope

- <explicitly excluded behavior — protects against scope creep during implementation>

## Open Questions

- <resolved before Status: Approved; delete this section when empty>
