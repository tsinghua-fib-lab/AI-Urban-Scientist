from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from find_planetary_computer import CONFIG
from open_data_skills.repository_metadata_family import run_validate_cli


def main() -> None:
    run_validate_cli(CONFIG)


if __name__ == "__main__":
    main()
