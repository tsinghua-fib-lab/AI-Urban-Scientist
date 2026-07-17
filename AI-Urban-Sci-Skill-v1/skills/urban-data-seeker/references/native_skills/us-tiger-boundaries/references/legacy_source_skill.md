# U.S. TIGER Boundaries SourceSkill

## Purpose

Emit not-final source-prior hints for U.S. Census TIGER/Line boundary files, including tracts, block groups, counties, places, roads, and related geographies.

## When To Use

Use when a data need asks for official Census boundary geometry, geography join keys, or TIGER/Line shapefiles by vintage and geography level.

## Do Not Use

Do not use for ACS attributes, LODES employment files, local parcel polygons, or OSM-derived geometry. Never create resource plans, approve URLs, write downloaded files, or claim success.

## Inputs

- `need_id`: Route-agent need identifier.
- `need_text`: User-facing data need text.
- `vintage`: TIGER/Line vintage year.
- `geography`: Geography level such as tract, block group, county, place, or roads.
- `state`: Optional state FIPS or postal hint for state-scoped layers.

## Tools/Scripts Used

- `scripts/find_tiger_boundaries.py`: Emits TIGER/Line source-prior hints and ambiguity notes.
- Future scripts may construct candidate ZIP paths after vintage, geography, and state validation.

## Workflow

1. Match the need to Census TIGER/Line boundary products.
2. Emit the official TIGER/Line entrypoint as a candidate resource hint.
3. Preserve vintage, geography level, state scope, and join-key ambiguity.
4. Return RouteDossier and RouteResourceIntent fragments marked `not-final`.

## Outputs

- SourceSkill payload with `finality=not_final` and `consumer_authority=none`.
- Candidate resource hints that require resolver, probe, download, and verifier steps.
- Ambiguity notes for vintage, geography, and boundary product.

## Failure Rules

- If geography level or vintage is missing, emit ambiguity instead of fabricating a ZIP path.
- If the need asks for attributes, route separately to ACS, LODES, or another attribute SourceSkill.
- Do not claim boundary suitability until geometry and join keys are verified.

## Verification

Future verification must confirm vintage, geography level, state scope, file availability, geometry type, CRS, GEOID/join keys, and relationship to requested attributes before route acceptance.
