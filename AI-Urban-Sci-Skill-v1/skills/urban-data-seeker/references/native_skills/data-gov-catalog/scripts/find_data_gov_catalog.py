from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.catalog_json_configs import get_catalog_json_config
from open_data_skills.repository_metadata_family import build_repository_payload, run_find_cli


CONFIG = get_catalog_json_config("data_gov_catalog")


def build_payload(*, need_id: str, need_text: str, query: str, geography: str, time_range: str) -> dict[str, object]:
    return build_repository_payload(
        CONFIG,
        need_id=need_id,
        need_text=need_text,
        query=query,
        geography=geography,
        time_range=time_range,
    )


def main() -> None:
    run_find_cli(CONFIG, build_payload)


if __name__ == "__main__":
    main()
