from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.direct_file_family import inspect_direct_file, run_probe_cli
from open_data_skills.remaining_direct_file_configs import get_remaining_direct_file_config


CONFIG = get_remaining_direct_file_config("us_tiger_boundaries")


def inspect_us_tiger_boundaries_file(name: str, data: bytes):
    return inspect_direct_file(CONFIG, name, data)


def main() -> None:
    run_probe_cli(CONFIG)


if __name__ == "__main__":
    main()
