from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.generic_resource_tools import run_access_check


if __name__ == "__main__":
    run_access_check(
        source_skill_id="nasa_earthdata_cmr",
        publisher="NASA",
        metadata_url="https://cmr.earthdata.nasa.gov/search/site/docs/search/api",
        access_status="registration_required",
        authorization_required=True,
        not_open_download=True,
        used_platform_tools=[],
    )
