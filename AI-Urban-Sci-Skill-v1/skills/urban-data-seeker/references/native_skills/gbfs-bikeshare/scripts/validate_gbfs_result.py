from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.api_payload_family import run_validate_cli
from open_data_skills.public_api_payload_configs import get_public_api_payload_config


CONFIG = get_public_api_payload_config("gbfs_bikeshare")


def main() -> None:
    run_validate_cli(CONFIG)


if __name__ == "__main__":
    main()
