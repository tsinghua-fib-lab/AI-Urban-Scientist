from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.direct_file_family import run_fetch_cli
from open_data_skills.remaining_direct_file_configs import get_remaining_direct_file_config


CONFIG = get_remaining_direct_file_config("us_tiger_boundaries")


def main() -> None:
    run_fetch_cli(CONFIG)


if __name__ == "__main__":
    main()
