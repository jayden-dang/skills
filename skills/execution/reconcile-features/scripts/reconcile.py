"""Deterministic reconcile-features runner (rfeat-1.0).

Pure classification + envelope builder. Optional git/CLI wrappers for
mechanical runs. Never mints Feature CODEs or writes docs/specs/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from cluster import cluster_unowned_paths, domain_slug, surface_roots
from owns import load_owns, owners_for_path

FINDINGS_MAX = 12
EVIDENCE_MAX = 8
KNOWN_IMPACT_SOFT_MIN = 4  # reserve slots so OBS fill cannot erase known CODEs
RECIPE_ID = "rfeat-1.0"
SCHEMA_VERSION = "1"

GENERATED_BASENAMES = {
    "pnpm-lock.yaml",
    "package-lock.json",
    "yarn.lock",
    "Cargo.lock",
    "poetry.lock",
    "Gemfile.lock",
    "composer.lock",
}
GENERATED_SEGMENTS = {
    "node_modules",
    "target",
    "dist",
    "build",
    "vendor",
    "generated",
    "__generated__",
}
DOCS_PREFIXES = ("docs/", ".skills/", "README", "CHANGELOG", "LICENSE")
SOURCE_EXTS = (
    ".rs",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".py",
    ".go",
    ".move",
    ".java",
    ".kt",
    ".swift",
    ".rb",
    ".php",
    ".cs",
    ".sql",
    ".proto",
    ".graphql",
    ".vue",
    ".svelte",
)


def obs_id(locators: list[str]) -> str:
    uniq = sorted(set(locators))
    digest = hashlib.sha256("\n".join(uniq).encode("utf-8")).hexdigest()
    return f"OBS-{digest[:6]}"


def is_generated(path: str) -> bool:
    base = path.rsplit("/", 1)[-1]
    if base in GENERATED_BASENAMES or base.endswith(".lock"):
        return True
    parts = path.split("/")
    if any(seg in GENERATED_SEGMENTS for seg in parts):
        return True
    if any(p.endswith(".pb.go") for p in (path, base)):
        return True
    return False


def _is_docs_or_meta(path: str) -> bool:
    if path.startswith(DOCS_PREFIXES):
        return True
    base = path.rsplit("/", 1)[-1]
    if base in {"README.md", "CHANGELOG.md", "LICENSE", "AGENTS.md"}:
        return True
    if path.startswith(".github/"):
        return True
    return False


def _is_behavior_source(path: str) -> bool:
    if is_generated(path) or _is_docs_or_meta(path):
        return False
    base = path.rsplit("/", 1)[-1]
    return any(base.endswith(ext) for ext in SOURCE_EXTS) or "/src/" in f"/{path}/"


def _evidence(locators: list[str], kind: str = "path") -> dict[str, Any]:
    items = [
        {"kind": kind, "locator": loc, "status": "observed"}
        for loc in sorted(set(locators))[:EVIDENCE_MAX]
    ]
    return {"items": items, "truncated": len(set(locators)) > EVIDENCE_MAX}


def classify_paths(
    paths: list[str],
    owns: dict[str, set[str]],
) -> list[dict[str, Any]]:
    """Classify candidate paths into finding rows (≤ FINDINGS_MAX).

    Cap priority: new-capability-candidate, uncertain, known-impact,
    no-spec-impact. Known-impact is one row per CODE (not per CODE-tuple) so
    combo explosion cannot starve OBS candidates.
    """
    candidates = [p for p in paths if not is_generated(p)]
    owned_by_code: dict[str, list[str]] = defaultdict(list)
    unowned_behavior: list[str] = []
    docs_only: list[str] = []
    uncertain: list[str] = []

    for p in candidates:
        codes = owners_for_path(p, owns)
        if codes:
            for code in codes:
                owned_by_code[code].append(p)
        elif _is_docs_or_meta(p):
            docs_only.append(p)
        elif _is_behavior_source(p):
            unowned_behavior.append(p)
        else:
            uncertain.append(p)

    new_caps: list[dict[str, Any]] = []
    clusters = cluster_unowned_paths(unowned_behavior)
    for key in sorted(clusters, key=lambda k: (-len(clusters[k]), k)):
        locs = clusters[key]
        new_caps.append(
            {
                "change_class": "new-capability-candidate",
                "confidence": "medium",
                "codes": [],
                "observation_id": obs_id(locs),
                "evidence": _evidence(locs),
                "disposition": "pending",
                "domain": domain_slug(locs),
                "surface_roots": surface_roots(locs),
                "cluster_key": key,
            }
        )

    uncertain_rows: list[dict[str, Any]] = []
    if uncertain:
        uncertain_rows.append(
            {
                "change_class": "uncertain",
                "confidence": "low",
                "codes": [],
                "observation_id": None,
                "evidence": _evidence(uncertain),
                "disposition": "pending",
            }
        )

    known: list[dict[str, Any]] = []
    for code, locs in sorted(owned_by_code.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        known.append(
            {
                "change_class": "known-impact",
                "confidence": "high",
                "codes": [code],
                "observation_id": None,
                "evidence": _evidence(locs),
                "disposition": "pending",
            }
        )

    docs_rows: list[dict[str, Any]] = []
    if docs_only:
        docs_rows.append(
            {
                "change_class": "no-spec-impact",
                "confidence": "high",
                "codes": [],
                "observation_id": None,
                "evidence": _evidence(docs_only),
                "disposition": "pending",
            }
        )

    # Balanced budget: surface OBS first, but reserve room for known CODEs.
    uncertain_take = uncertain_rows[:1]
    reserve_known = min(len(known), KNOWN_IMPACT_SOFT_MIN) if known else 0
    new_budget = max(0, FINDINGS_MAX - len(uncertain_take) - reserve_known)
    new_take = new_caps[:new_budget]
    remaining = FINDINGS_MAX - len(uncertain_take) - len(new_take)
    known_take = known[:remaining]
    leftover = FINDINGS_MAX - len(uncertain_take) - len(new_take) - len(known_take)
    docs_take = docs_rows[:leftover]
    return new_take + uncertain_take + known_take + docs_take


def build_envelope(
    *,
    mode: str,
    base: str,
    head: str,
    previous: str | None,
    advanced_to: str | None,
    owns: dict[str, set[str]],
    owns_coverage: dict[str, Any],
    paths: list[str],
) -> dict[str, Any]:
    findings = classify_paths(paths, owns)
    uncapped = _uncapped_finding_count(paths, owns)
    return {
        "advisory": True,
        "schema_version": SCHEMA_VERSION,
        "recipe_id": RECIPE_ID,
        "mode": mode,
        "base": base,
        "head": head,
        "checkpoint": {"previous": previous, "advanced_to": advanced_to},
        "owns_coverage": {
            "with_owns": owns_coverage.get("with_owns", 0),
            "registered": owns_coverage.get("registered", 0),
            "ratio": owns_coverage.get("ratio", 0.0),
        },
        "findings": findings,
        "findings_truncated": uncapped > FINDINGS_MAX,
        "notes": [],
    }


def _uncapped_finding_count(paths: list[str], owns: dict[str, set[str]]) -> int:
    """Count findings without applying FINDINGS_MAX (for truncation flag)."""
    candidates = [p for p in paths if not is_generated(p)]
    owned_codes: set[str] = set()
    unowned_behavior: list[str] = []
    docs = False
    unc = False
    for p in candidates:
        codes = owners_for_path(p, owns)
        if codes:
            owned_codes.update(codes)
        elif _is_docs_or_meta(p):
            docs = True
        elif _is_behavior_source(p):
            unowned_behavior.append(p)
        else:
            unc = True
    n = len(owned_codes) + len(cluster_unowned_paths(unowned_behavior))
    if docs:
        n += 1
    if unc:
        n += 1
    return n


def reconcile_repo(
    repo_root: Path,
    *,
    specs_dir: str = "docs/specs",
    paths: list[str] | None = None,
    mode: str = "full",
    base: str = "",
    head: str = "",
    write_overlay: bool = False,
) -> dict[str, Any]:
    root = Path(repo_root)
    owns, cov = load_owns(root, specs_dir=specs_dir)
    if paths is None:
        paths = git_name_only(root, base, head) if base and head else []
    advanced_to = None
    env = build_envelope(
        mode=mode,
        base=base or "unknown",
        head=head or "unknown",
        previous=None,
        advanced_to=advanced_to,
        owns=owns,
        owns_coverage=cov,
        paths=paths,
    )
    if write_overlay:
        # Overlay write is a separate step; default off for pure tests.
        pass
    return env


def git_name_only(repo_root: Path, base: str, head: str) -> list[str]:
    out = subprocess.check_output(
        ["git", "diff", "--name-only", "-M", f"{base}..{head}"],
        cwd=repo_root,
        text=True,
    )
    return [p for p in out.splitlines() if p]


def render_envelope(env: dict[str, Any]) -> str:
    banner = (
        "Advisory reverse-track — not merge enforcement. Observations are not "
        "Feature CODEs. Unresolved `pending` candidates must be surfaced before "
        "framing or realigning the touched surfaces."
    )
    return banner + "\n\n" + json.dumps(env, indent=2, sort_keys=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="reconcile-features rfeat-1.0 runner")
    p.add_argument("--repo", type=Path, default=Path.cwd())
    p.add_argument("--specs-dir", default="docs/specs")
    p.add_argument("--base", default="")
    p.add_argument("--head", default="HEAD")
    p.add_argument("--mode", default="full", choices=["full", "changes-since-checkpoint", "brownfield-bootstrap"])
    p.add_argument("--paths-file", type=Path, default=None, help="Optional path list (skips git)")
    args = p.parse_args(argv)

    repo = args.repo.resolve()
    if args.paths_file:
        paths = [ln.strip() for ln in args.paths_file.read_text().splitlines() if ln.strip()]
        base, head = args.base or "paths-file", args.head
    else:
        head = args.head
        if not args.base:
            # default: since checkpoint or HEAD~1 — keep simple for CLI
            base = subprocess.check_output(
                ["git", "rev-parse", "HEAD~1"], cwd=repo, text=True
            ).strip()
        else:
            base = args.base
        paths = git_name_only(repo, base, head)
        base = subprocess.check_output(["git", "rev-parse", base], cwd=repo, text=True).strip()
        head = subprocess.check_output(["git", "rev-parse", head], cwd=repo, text=True).strip()

    env = reconcile_repo(
        repo,
        specs_dir=args.specs_dir,
        paths=paths,
        mode=args.mode,
        base=base,
        head=head,
        write_overlay=False,
    )
    sys.stdout.write(render_envelope(env))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
