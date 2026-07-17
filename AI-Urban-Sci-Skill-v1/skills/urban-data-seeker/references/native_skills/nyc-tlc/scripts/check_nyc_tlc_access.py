from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.generic_resource_tools import run_access_check


if __name__ == "__main__":
    run_access_check(
        source_skill_id="nyc_tlc",
        publisher="New York City Taxi and Limousine Commission",
        metadata_url="https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page",
        access_status="open",
        authorization_required=False,
        not_open_download=False,
        used_platform_tools=[],
    )
