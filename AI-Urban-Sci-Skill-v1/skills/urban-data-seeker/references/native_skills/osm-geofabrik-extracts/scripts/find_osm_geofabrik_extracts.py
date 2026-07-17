from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.curated_source_tools import run_curated_find


if __name__ == "__main__":
    run_curated_find(source_skill_id="osm_geofabrik_extracts")
