from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.api_payload_family import classify_api_payload, run_probe_cli
from open_data_skills.public_api_payload_configs import get_public_api_payload_config


CONFIG = get_public_api_payload_config("open_aq")


def classify_open_aq_payload(payload):
    return classify_api_payload(CONFIG, payload)


def main() -> None:
    run_probe_cli(CONFIG)


if __name__ == "__main__":
    main()
