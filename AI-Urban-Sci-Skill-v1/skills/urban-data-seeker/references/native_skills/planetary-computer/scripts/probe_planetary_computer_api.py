from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from find_planetary_computer import CONFIG
from open_data_skills.repository_metadata_family import classify_repository_payload, run_probe_cli


def classify_planetary_computer_payload(payload):
    return classify_repository_payload(CONFIG, payload)


def main() -> None:
    run_probe_cli(CONFIG)


if __name__ == "__main__":
    main()
