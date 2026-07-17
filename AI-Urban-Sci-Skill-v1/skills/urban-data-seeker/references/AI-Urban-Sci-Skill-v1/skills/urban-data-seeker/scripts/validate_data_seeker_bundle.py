#!/usr/bin/env python3
"""Validate the urban-data-seeker integrated skill bundle."""

from __future__ import annotations

import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_TOP = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/route_index.compact.jsonl",
    "references/selected_skills.json",
    "references/routing_rules.md",
]
REQUIRED_SKILL_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/source_card.json",
    "references/tool_capabilities.json",
]
REQUIRED_SECTIONS = [
    "## Workflow",
    "## Tools",
    "## References",
    "## Access And Download Rules",
    "## Validation Focus",
    "## Output Contract",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> None:
    errors: list[str] = []
    for rel in REQUIRED_TOP:
        if not (ROOT / rel).exists():
            fail(errors, f"missing top-level file: {rel}")

    selected_path = ROOT / "references" / "selected_skills.json"
    if selected_path.exists():
        selected = json.loads(selected_path.read_text())["skills"]
    else:
        selected = []

    route_names = []
    route_path = ROOT / "references" / "route_index.compact.jsonl"
    if route_path.exists():
        for line_no, line in enumerate(route_path.read_text().splitlines(), 1):
            try:
                item = json.loads(line)
            except Exception as exc:
                fail(errors, f"invalid route index line {line_no}: {exc}")
                continue
            route_names.append(item.get("name"))

    selected_names = [item["name"] for item in selected]
    if len(selected_names) != 25:
        fail(errors, f"expected 25 selected skills, found {len(selected_names)}")
    if selected_names != route_names:
        fail(errors, "selected_skills.json order does not match route_index.compact.jsonl")

    for name in selected_names:
        skill_root = ROOT / "references" / "native_skills" / name
        for rel in REQUIRED_SKILL_FILES:
            if not (skill_root / rel).exists():
                fail(errors, f"{name}: missing {rel}")
        skill_md = skill_root / "SKILL.md"
        if skill_md.exists():
            text = skill_md.read_text()
            if not re.match(r"---\nname:\s*", text):
                fail(errors, f"{name}: invalid or missing YAML frontmatter")
            for section in REQUIRED_SECTIONS:
                if section not in text:
                    fail(errors, f"{name}: missing section {section}")
        for rel in ["references/source_card.json", "references/tool_capabilities.json"]:
            path = skill_root / rel
            if path.exists():
                try:
                    json.loads(path.read_text())
                except Exception as exc:
                    fail(errors, f"{name}: invalid {rel}: {exc}")

    pycache = [str(p.relative_to(ROOT)) for p in ROOT.rglob("__pycache__")]
    if pycache:
        fail(errors, f"__pycache__ directories present: {pycache[:5]}")

    platform_root = ROOT / "references" / "platforms"
    for platform in [
        "socrata_platform",
        "arcgis_platform",
        "ckan_platform",
        "dataverse_platform",
        "stac_platform",
        "sdmx_platform",
        "odata_platform",
        "document_portal_platform",
        "legistar_platform",
    ]:
        if not (platform_root / platform).exists():
            fail(errors, f"missing platform resource: {platform}")

    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps({"ok": True, "selected_skill_count": len(selected_names)}, indent=2))


if __name__ == "__main__":
    main()
