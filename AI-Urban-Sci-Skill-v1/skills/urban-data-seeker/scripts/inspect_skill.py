#!/usr/bin/env python3
"""Inspect one bundled downstream skill without loading the whole bundle."""

from __future__ import annotations

import argparse
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
NATIVE_ROOT = ROOT / "references" / "native_skills"


def frontmatter(text: str) -> dict:
    match = re.match(r"---\n(.*?)\n---\n", text, flags=re.S)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def inspect(name: str) -> dict:
    root = NATIVE_ROOT / name
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        raise SystemExit(f"Unknown bundled skill: {name}")
    text = skill_path.read_text()
    sections = re.findall(r"^##\s+(.+)$", text, flags=re.M)
    scripts = sorted(str(p.relative_to(root)) for p in (root / "scripts").glob("*.py")) if (root / "scripts").exists() else []
    refs = sorted(str(p.relative_to(root)) for p in (root / "references").glob("*")) if (root / "references").exists() else []
    return {
        "skill": name,
        "path": str(skill_path.relative_to(ROOT)),
        "frontmatter": frontmatter(text),
        "sections": sections,
        "scripts": scripts,
        "references": refs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill")
    args = parser.parse_args()
    print(json.dumps(inspect(args.skill), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
