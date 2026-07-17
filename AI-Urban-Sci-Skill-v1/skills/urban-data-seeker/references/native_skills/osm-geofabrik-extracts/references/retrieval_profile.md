# Retrieval Profile

## One-line capability
Geofabrik regional OpenStreetMap extract discovery for `.osm.pbf`, free shapefile ZIPs, OSM roads, buildings, POIs, land-use, and regional OSM bulk downloads.

## Best for
- Constructing or validating Geofabrik regional extract URLs such as `europe/germany-latest.osm.pbf`
- Finding OSM PBF or shapefile downloads for a country, state, or region
- Distinguishing regional bulk OSM extracts from Overpass feature queries

## Provides
- Geofabrik download server candidates
- Direct regional PBF and free shapefile URL templates
- Validation focus for region path, ODbL attribution, update date, file size, and metadata caveats

## Coverage and constraints
- Geography: global Geofabrik regional coverage where an extract path exists
- Spatial level: country, subregion, or other Geofabrik-defined extract region
- Time: regularly updated latest extracts; not an arbitrary historical archive unless explicitly available
- Access: open downloads under OSM/Geofabrik terms; full files can be large and require explicit full-fetch authorization
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Small custom OSM feature queries by bbox/tag; use `osm_features`
- Official government road, parcel, building permit, or facility records
- Address-only datasets; use `openaddresses_geocoding_base`
- Overture Maps products; use `overture_maps`

## Typical user expressions
- "download Geofabrik PBF for Germany"
- "OSM regional extract shapefile"
- "latest .osm.pbf for a country"
- "OpenStreetMap roads and buildings bulk extract"

## Nearby alternatives
- `osm_features`: Pick for Overpass/tag-level custom OSM queries
- `overture_maps`: Pick for Overture buildings, places, transportation, or base layers
- `openaddresses_geocoding_base`: Pick for address points rather than all OSM features
- `natural_earth` or `gadm`: Pick for cartographic or administrative boundaries

## Retrieval notes
- Positive distinctions: Geofabrik, `.osm.pbf`, OSM extract, shapefile ZIP, regional OpenStreetMap, latest extract, and ODbL attribution should boost this skill.
- Negative distinctions: Overpass-style tag queries and official government datasets should route elsewhere.
