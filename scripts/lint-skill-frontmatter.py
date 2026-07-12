#!/usr/bin/env python3
"""Lint SKILL.md frontmatter so a malformed one can't silently vanish from the catalog.

The `skills` CLI (vercel-labs/skills, via gray-matter/js-yaml) discovers a skill by
parsing its SKILL.md frontmatter and *silently skips* any file whose YAML does not
parse. A single unquoted colon once dropped the `trace` skill from
`npx skills add jayden-dang/skills` with no error at all. This check fails loudly
instead, before the break ever reaches origin.

Checks per SKILL.md:
  - frontmatter block is present and closed (`---` … `---`)
  - the block parses as YAML and yields a mapping
  - `name` and `description` are present, non-empty strings
  - `name` matches the skill's directory (what the catalog keys off)

Usage:
  lint-skill-frontmatter.py                 # scan every skills/**/SKILL.md
  lint-skill-frontmatter.py FILE [FILE ...] # lint the given files (non-SKILL.md paths ignored)
"""
import glob
import os
import sys

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("lint-skill-frontmatter: PyYAML is required — `pip install pyyaml`")


def frontmatter(text):
    if not text.startswith("---"):
        raise ValueError("missing frontmatter: file does not start with '---'")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("missing frontmatter: no closing '---'")
    return text[3:end]


def check(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    try:
        block = frontmatter(text)
    except ValueError as e:
        return [str(e)]
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as e:
        msg = " ".join(str(e).split())
        return [f"frontmatter is not valid YAML — {msg} "
                "(common cause: an unquoted colon in the description)"]
    if not isinstance(data, dict):
        return ["frontmatter did not parse to a mapping"]

    errs = []
    for key in ("name", "description"):
        val = data.get(key)
        if not isinstance(val, str) or not val.strip():
            errs.append(f"missing or empty '{key}'")
    name = data.get("name")
    expected = os.path.basename(os.path.dirname(path))
    if isinstance(name, str) and name.strip() and name != expected:
        errs.append(f"name '{name}' does not match its directory '{expected}'")
    return errs


def main(argv):
    args = [a for a in argv if os.path.basename(a) == "SKILL.md"]
    files = args if args else sorted(glob.glob("skills/**/SKILL.md", recursive=True))
    if not files:
        return 0
    failed = 0
    for path in files:
        errs = check(path)
        if errs:
            failed += 1
            for e in errs:
                print(f"  ✗ {path}: {e}")
    if failed:
        print(f"\nlint-skill-frontmatter: {failed} of {len(files)} SKILL.md failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
