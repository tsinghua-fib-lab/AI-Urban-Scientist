# Retrieval Profile

## One-line capability
Official U.S. Census TIGER/Line boundary geometry — tracts, block groups, counties, places, roads, and related geographies — organized by vintage year and geography level with GEOID join keys.

## Best for
- Obtaining the official Census boundary polygons needed to join ACS, decennial census, or other attribute data by GEOID
- Mapping U.S. administrative geographies (counties, tracts, block groups, places) for a specific TIGER/Line vintage year
- Acquiring Census road centerline or water boundary geometry for spatial analysis within the United States

## Provides
- Candidate resource hints for TIGER/Line shapefiles by vintage and geography level
- Metadata evidence on vintage, geography level, state scope, CRS, and GEOID join-key structure
- Probe evidence for boundary availability and sample shapefile fetches to confirm geometry before full download

## Coverage and constraints
- Geography: United States and territories (50 states, DC, Puerto Rico, island areas)
- Spatial level: National to subnational (block group, tract, county, place, state)
- Time: Annual vintages (snapshot per vintage year)
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Needs for American Community Survey demographic or economic attributes — use census_acs for attribute data, not boundary geometry alone
- Needs for global or non-U.S. administrative boundaries — use gadm, geoboundaries, or natural_earth instead
- Needs for OSM-derived street networks or building footprints — use osm_features instead

## Typical user expressions
- 我需要2022年TIGER/Line的普查区(tract)边界数据，用来连接ACS人口数据
- Download TIGER/Line county boundary shapefiles for all 50 states, 2023 vintage
- 需要美国block group级别的边界多边形，用于做环境正义空间分析

## Nearby alternatives
- gadm: Choose when the need is for global subnational boundaries outside the U.S.
- geoboundaries: Choose when the need is for non-U.S. harmonized ADM boundaries by ISO3
- osm_features: Choose when the need is for OSM-derived road networks or building footprints rather than official Census geometry

## Retrieval notes
- Positive distinctions: Official Census geometry with GEOID join keys; vintage-year specificity; Evidence: SKILL.md specifies vintage and geography as required params; probe and fetch_sample scripts available
- Negative distinctions: U.S.-only — not usable for international boundaries; geometry only, no demographic attributes (census_acs is separate); easily confused with ACS attribute delivery which requires a separate skill
