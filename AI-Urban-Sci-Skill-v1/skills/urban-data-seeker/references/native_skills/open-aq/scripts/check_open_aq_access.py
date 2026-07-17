from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.generic_resource_tools import run_access_check


if __name__ == "__main__":
    run_access_check(
        source_skill_id="open_aq",
        publisher="OpenAQ",
        metadata_url="https://docs.openaq.org/",
        access_status="key_gated",
        authorization_required=True,
        not_open_download=False,
        used_platform_tools=[],
    )
