#!/usr/bin/env python3
"""One-shot v1.0 skill rename. Run from repo root. No old-name residue."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Longest-first. Kept names omitted (research, triage, assess-milestone).
RENAMES: list[tuple[str, str]] = [
    ("drive-dogfood", "drive-walk"),
    ("acceptance-check", "validate-feature"),
    ("acceptance-api", "validate-api"),
    ("acceptance-ui", "validate-ui"),
    ("write-requirements", "specify-behavior"),
    ("improve-architecture", "scan-architecture"),
    ("check-invariants", "judge-invariants"),
    ("domain-modeling", "define-domain"),
    ("comprehend-change", "study-change"),
    ("allocate-attention", "sample-attention"),
    ("establish-project", "anchor-project"),
    ("scaffold-project", "bootstrap-repo"),
    ("execute-inline", "build-inline"),
    ("execute-story", "build-story-units"),
    ("execute-plan", "build-continuous"),
    ("record-decision", "record-verdict"),
    ("prepare-change", "package-change"),
    ("finish-branch", "land-branch"),
    ("receive-review", "vet-feedback"),
    ("explain-change", "brief-team"),
    ("correct-course", "reroute-plan"),
    ("check-roadmap", "status-roadmap"),
    ("repoint-project", "dispose-pivot"),
    ("writing-skills", "author-skills"),
    ("using-skills", "gate-session"),
    ("write-roadmap", "plan-milestones"),
    ("write-design", "design-solution"),
    ("write-plan", "plan-tasks"),
    ("setup-repo", "configure-repo"),
    ("file-issues", "publish-issues"),
    ("code-review", "inspect-change"),
    ("design-page", "craft-page"),
    ("sync-spec", "realign-spec"),
    ("worktrees", "isolate-workspace"),
    ("brainstorm", "frame-change"),
    ("grilling", "probe-decisions"),
    ("prototype", "run-spike"),
    ("interpret", "interpret-native"),
    ("dogfood", "walk-product"),
    ("handoff", "write-handoff"),
    ("release", "cut-release"),  # careful: mostly via token patterns
    ("polish", "polish-diff"),
    ("amend", "amend-feature"),
    ("verify", "prove-claim"),
    ("debug", "root-cause"),
    ("trace", "audit-trace"),
    ("tdd", "test-first"),
    ("ask", "route-work"),
    ("teach", "teach-pack"),
]

# Tokens that must NOT be global bare-word replaced (use citation patterns only).
CITATION_ONLY = {
    "ask",
    "teach",
    "debug",
    "verify",
    "release",
    "polish",
    "amend",
    "trace",
    "tdd",
    "handoff",
    "dogfood",
    "interpret",
    "research",  # kept but listed if present
}

SKIP_DIR_NAMES = {".git", "node_modules", ".venv", "venv", "__pycache__", ".skills"}
BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".ico",
    ".woff",
    ".woff2",
    ".zip",
    ".tar",
    ".gz",
    ".pyc",
    ".so",
    ".dylib",
    ".mp4",
    ".mp3",
}


def is_skipped(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIR_NAMES:
        return True
    if path.suffix.lower() in BINARY_SUFFIXES:
        return True
    return False


def rename_path_component(name: str, mapping: dict[str, str]) -> str:
    """Replace whole path components that equal an old skill name."""
    if name in mapping:
        return mapping[name]
    # handle name with extension: using-skills.mdc, scenarios-brainstorm.md
    for old, new in sorted(mapping.items(), key=lambda x: -len(x[0])):
        if name == old:
            return new
        # prefix/suffix patterns
        if name.startswith(old + ".") or name.startswith(old + "-") or name.startswith(old + "_"):
            return new + name[len(old) :]
        if name.endswith("-" + old) or name.endswith("_" + old) or name.endswith("." + old):
            return name[: -len(old)] + new
        # embedded in slug: 2026-07-28-prepare-change
        if f"-{old}" in name:
            name = name.replace(f"-{old}", f"-{new}")
        if f"{old}-" in name:
            name = name.replace(f"{old}-", f"{new}-")
        if f"_{old}_" in name:
            name = name.replace(f"_{old}_", f"_{new}_")
        if f"_{old}." in name:
            name = name.replace(f"_{old}.", f"_{new}.")
        if f"/{old}/" in name:  # shouldn't happen for single component
            pass
    return name


def collect_renames(root: Path, mapping: dict[str, str]) -> list[tuple[Path, Path]]:
    """Return (src, dst) pairs deepest-first for files and dirs whose names need change."""
    pairs: list[tuple[Path, Path]] = []
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        p = Path(dirpath)
        if is_skipped(p):
            dirnames[:] = []
            continue
        # files
        for fn in filenames:
            new_fn = rename_path_component(fn, mapping)
            if new_fn != fn:
                pairs.append((p / fn, p / new_fn))
        # directory itself
        if p == root:
            continue
        new_name = rename_path_component(p.name, mapping)
        if new_name != p.name:
            pairs.append((p, p.parent / new_name))
    # deepest first already from topdown=False walk order for dirs;
    # re-sort by path depth descending
    pairs.sort(key=lambda x: len(x[0].parts), reverse=True)
    return pairs


def apply_fs_renames(pairs: list[tuple[Path, Path]]) -> int:
    n = 0
    for src, dst in pairs:
        if not src.exists():
            continue
        if dst.exists():
            print(f"SKIP exists: {src} -> {dst}", file=sys.stderr)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        n += 1
        print(f"mv {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    return n


def replace_citations(text: str, old: str, new: str) -> str:
    """Replace skill citations without eating common English / domain phrases."""
    if old == new:
        return text

    # Backticks (possibly with trailing punctuation already outside)
    text = text.replace(f"`{old}`", f"`{new}`")

    # Double-backtick edge / markdown code in tables already covered

    # Frontmatter name:
    text = re.sub(
        rf"(?m)^(name:\s*){re.escape(old)}\s*$",
        rf"\g<1>{new}",
        text,
    )

    # skills:old / plugin style
    text = text.replace(f"skills:{old}", f"skills:{new}")
    text = text.replace(f"skill:{old}", f"skill:{new}")

    # Slash command: /old not followed by more path-ish chars
    # Negative lookbehind: not part of URL path segment mid-word
    text = re.sub(
        rf"(?<![\w/-])/{re.escape(old)}(?![\w-])",
        f"/{new}",
        text,
    )

    # Path segments /old/ or /old" or /old' or end
    text = re.sub(
        rf"(?<=/)({re.escape(old)})(?=/|[\"'\s\)]|$)",
        new,
        text,
    )

    # ./old or skills/cat/old at end of path-ish
    text = re.sub(
        rf"(?<=[\s\"'(=])(\./)?({re.escape(old)})(?=/|[\"'\s\)]|$)",
        lambda m: (m.group(1) or "") + new
        if m.group(2) == old
        else m.group(0),
        text,
    )

    # Title-ish: # Old Name variations — handle kebab as words
    old_title = old.replace("-", " ").title()
    new_title = new.replace("-", " ").title()
    if old_title != new_title:
        text = text.replace(old_title, new_title)
        text = text.replace(old_title.upper(), new_title.upper())

    # ALL-CAPS acronym style for tdd/TDD already handled via title; keep TDD as concept

    if old not in CITATION_ONLY:
        # Safe global for multi-hyphen / distinctive names
        text = text.replace(old, new)
    else:
        # Citation-only tokens: never bare-word replace (breaks English).
        # Extra safe skill-invocation phrases without backticks:
        text = re.sub(
            rf"\b(REQUIRED SUB-SKILL:\s*use\s+){re.escape(old)}\b",
            rf"\1{new}",
            text,
            flags=re.I,
        )
        text = re.sub(
            rf"\b{re.escape(old)}\s+(skill|gate)\b",
            rf"{new} \1",
            text,
            flags=re.I,
        )
        # Diagram / inventory lines that list skills with " / " separators
        # only when the whole line looks like a skill chain (no English verbs)
        def slash_chain(m: re.Match[str]) -> str:
            return m.group(0).replace(old, new)

        text = re.sub(
            rf"(?m)^[ \t]*{re.escape(old)}[ \t]*/[ \t]*\w.*$",
            slash_chain,
            text,
        )
        text = re.sub(
            rf"(?m)^.*[ \t]/[ \t]*{re.escape(old)}[ \t]*/[ \t]*.*$",
            slash_chain,
            text,
        )
        text = re.sub(
            rf"(?m)^.*[ \t]*/[ \t]*{re.escape(old)}[ \t]*(/|◄|→).*$",
            slash_chain,
            text,
        )

    return text


def protect_phrases(text: str) -> tuple[str, list[str]]:
    """Shield domain phrases that must not become skill renames."""
    shields: list[str] = []
    patterns = [
        r"verify commands?",
        r"verify suite",
        r"verify step",
        r"verify output",
        r"release steps?",
        r"release notes?",
        r"release branch(?:es)?",
        r"tagged release",
        r"cut a release",
        r"shipping a release",
        r"adversarial verify",
        r"independently verifiable",
        r"system verification",
        r"trace spine",
        r"trace links?",
        r"trace matrix",
        r"traceability",
        r"untraced",
        r"the trace stays",
        r"keep the trace",
        r"TDD\b",
        r"test-driven development",
        r"product walking",
    ]
    out = text

    def make_repl():
        def repl(m: re.Match[str]) -> str:
            shields.append(m.group(0))
            return f"\x00SHIELD{len(shields) - 1}\x00"

        return repl

    for pat in patterns:
        out = re.sub(pat, make_repl(), out)
    return out, shields


def unprotect(text: str, shields: list[str]) -> str:
    def repl(m: re.Match[str]) -> str:
        return shields[int(m.group(1))]

    return re.sub(r"\x00SHIELD(\d+)\x00", repl, text)


def transform_text(text: str, ordered: list[tuple[str, str]]) -> str:
    text, shields = protect_phrases(text)
    for old, new in ordered:
        text = replace_citations(text, old, new)
    text = unprotect(text, shields)

    # Phrase-level cleanups after skill renames
    phrase_map = [
        ("the trace check", "the audit-trace check"),
        ("The trace check", "The audit-trace check"),
        ("trace check", "audit-trace check"),
        ("Dogfood CLI", "Walk-product CLI"),
        ("dogfood CLI", "walk-product CLI"),
        ("dogfood run", "walk-product run"),
        ("dogfood guide", "walk-product guide"),
        ("Dogfood guide", "Walk-product guide"),
        ("-dogfood.json", "-walk-product.json"),
        ("dogfood-guide", "walk-product-guide"),
        ("notes-dogfood", "notes-walk-product"),
    ]
    for a, b in phrase_map:
        text = text.replace(a, b)
    return text


def iter_text_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        p = Path(dirpath)
        # prune skip dirs
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        if is_skipped(p):
            continue
        for fn in filenames:
            fp = p / fn
            if is_skipped(fp):
                continue
            # skip this script itself mid-run? allow rewrite of other scripts
            if fp.resolve() == Path(__file__).resolve():
                continue
            try:
                data = fp.read_bytes()
            except OSError:
                continue
            if b"\0" in data[:8192]:
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    text = data.decode("utf-8", errors="surrogateescape")
                except Exception:
                    continue
            yield fp, text


def main() -> int:
    mapping = dict(RENAMES)
    ordered = list(RENAMES)

    print("=== Phase 1: filesystem renames ===")
    pairs = collect_renames(ROOT, mapping)
    n_mv = apply_fs_renames(pairs)
    print(f"Renamed {n_mv} paths")

    print("=== Phase 2: text rewrite ===")
    n_files = 0
    n_changed = 0
    for fp, text in iter_text_files(ROOT):
        n_files += 1
        new_text = transform_text(text, ordered)
        if new_text != text:
            fp.write_text(new_text, encoding="utf-8")
            n_changed += 1
            print(f"edit {fp.relative_to(ROOT)}")
    print(f"Scanned {n_files} text files, changed {n_changed}")

    print("=== Phase 3: residual scan (old skill basenames) ===")
    # After rename, scan for remaining old multi-hyphen names and backticked singles
    residuals = []
    for old, new in ordered:
        if old == new:
            continue
        for fp, text in iter_text_files(ROOT):
            if f"`{old}`" in text or f"/{old}" in text or f"name: {old}" in text:
                residuals.append((old, str(fp.relative_to(ROOT))))
            elif old in mapping and "-" in old and old in text:
                # multi-hyphen bare remaining
                residuals.append((old, str(fp.relative_to(ROOT))))
    if residuals:
        print("RESIDUALS:")
        for old, path in residuals[:80]:
            print(f"  {old} still in {path}")
        print(f"Total residual hits: {len(residuals)}")
    else:
        print("No citation residuals for old skill names.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
