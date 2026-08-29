#!/usr/bin/env python3
"""Assert Engineer Pack plugin identity is the jdk slug (jayden-dang-kit)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MARKET = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
CODEX_MARKET = ROOT / ".agents" / "plugins" / "marketplace.json"
SLUG = "jdk"
DISPLAY = "Engineer Pack"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    plugin = json.loads(PLUGIN.read_text())
    if plugin.get("name") != SLUG:
        fail(f"plugin.json name is {plugin.get('name')!r}, expected {SLUG!r}")
    if plugin.get("displayName") != DISPLAY:
        fail(
            f"plugin.json displayName is {plugin.get('displayName')!r}, "
            f"expected {DISPLAY!r}"
        )

    market = json.loads(MARKET.read_text())
    names = [p.get("name") for p in market.get("plugins", [])]
    if SLUG not in names:
        fail(f"marketplace.json plugins names={names!r}, missing {SLUG!r}")
    if "engineer-pack" in names:
        fail("marketplace.json still lists engineer-pack; Engineer Pack slug is jdk")
    if "personal-pack" not in names:
        fail("marketplace.json dropped personal-pack")

    eng = next(p for p in market["plugins"] if p["name"] == SLUG)
    if eng.get("displayName") != DISPLAY:
        fail(
            f"marketplace jdk displayName is {eng.get('displayName')!r}, "
            f"expected {DISPLAY!r}"
        )

    if not CODEX_PLUGIN.is_file():
        fail(f"missing {CODEX_PLUGIN.relative_to(ROOT)}")
    codex = json.loads(CODEX_PLUGIN.read_text())
    if codex.get("name") != SLUG:
        fail(f".codex-plugin/plugin.json name is {codex.get('name')!r}, expected {SLUG!r}")
    iface = codex.get("interface") if isinstance(codex.get("interface"), dict) else {}
    if iface.get("displayName") != DISPLAY:
        fail(
            f".codex-plugin interface.displayName is {iface.get('displayName')!r}, "
            f"expected {DISPLAY!r}"
        )
    if codex.get("skills") != "./skills/":
        fail(
            f".codex-plugin skills is {codex.get('skills')!r}, expected './skills/'"
        )

    if not CODEX_MARKET.is_file():
        fail(f"missing {CODEX_MARKET.relative_to(ROOT)}")
    cm = json.loads(CODEX_MARKET.read_text())
    cnames = [p.get("name") for p in cm.get("plugins", [])]
    if SLUG not in cnames:
        fail(f".agents/plugins/marketplace.json names={cnames!r}, missing {SLUG!r}")
    if "personal-pack" in cnames:
        fail("Codex marketplace listed personal-pack; Engineer Pack only")

    print(f"ok: plugin and marketplace Engineer Pack slug is {SLUG}")


if __name__ == "__main__":
    main()
