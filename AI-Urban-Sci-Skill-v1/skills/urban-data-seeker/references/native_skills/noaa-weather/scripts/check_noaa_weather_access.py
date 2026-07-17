from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.generic_resource_tools import run_access_check


if __name__ == "__main__":
    run_access_check(
        source_skill_id="noaa_weather",
        publisher="NOAA National Centers for Environmental Information",
        metadata_url="https://www.ncei.noaa.gov/access",
        access_status="open_public_use_with_restricted_follow_up_available",
        authorization_required=True,
        not_open_download=False,
        used_platform_tools=[],
    )
