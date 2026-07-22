# 0001 — Architecture docs are the system-design SSOT

Repo-root `DESIGN.md` duplicated the project-docs architecture layer and drifted
from it. **Decision:** system design lives only under `docs/architecture/`
(INDEX invariants + domain files); product intent under `docs/product/`; root
`DESIGN.md` is deleted (no redirect stub). **Why:** one place for agents and
humans to read and update architecture, with greppable ARCH-N still isolated in
INDEX for `trace` / `check-invariants`.
