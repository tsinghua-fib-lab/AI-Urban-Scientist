from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from find_microsoft_building_footprints import CONFIG
from open_data_skills.catalog_csv_family import inspect_catalog_csv, run_probe_cli


def inspect_microsoft_building_footprints_catalog(name: str, data: bytes):
    return inspect_catalog_csv(CONFIG, name, data)


def main() -> None:
    run_probe_cli(CONFIG)


if __name__ == "__main__":
    main()
