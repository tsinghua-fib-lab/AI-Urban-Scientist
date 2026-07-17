from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.generic_resource_tools import run_access_check


if __name__ == "__main__":
    run_access_check(
        source_skill_id="us_tiger_boundaries",
        publisher="U.S. Census Bureau",
        metadata_url="https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html",
        access_status="open",
        authorization_required=False,
        not_open_download=False,
        used_platform_tools=[],
    )
