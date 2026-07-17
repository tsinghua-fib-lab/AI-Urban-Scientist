# STAC Query Patterns

## Decision Positioning
- Use this doc after confirming the request is STAC-driven (catalog/collection/item/asset wording or STAC URL).
- Confirm collection identity before searching items; collection can be inferred from URL path or provided query.
- Treat catalog-level metadata as routing evidence only; never as a data-fit decision.

## Query Patterns
- Catalog endpoint: `{catalog_root}` (usually `/` or API base root).
- Collection metadata: `{catalog_root}/collections/{collection}`.
- Item search endpoint: `{catalog_root}/search`.
- Minimal safe search pattern: `...?collections={collection}&limit=10`.
- Spatial+temporal filter pattern: `...?collections={collection}&bbox=minx,miny,maxx,maxy&datetime=YYYY-MM-DDTHH:MM:SSZ/YYYY-MM-DDTHH:MM:SSZ&limit=10`.
- Property filtering pattern: `...?collections={collection}&query={...}` (depends on extension support and syntax).
- Pagination pattern: respect `limit` and follow `next` links from responses; avoid blind offsets.

## Asset and COG Selection
- Read collection `summaries` and item `assets` before download.
- Prefer assets with explicit raster-compatible media types and clear roles for analysis workflows.
- Common raster preference: COG-capable GeoTIFF/COG-style assets with usable CRS and nodata metadata.
- Prefer signed URLs or provider-native access patterns when cloud-hosted assets require temporary credentials.
- Keep `roles`, `href`, and media type in the candidate record.

## Probe / Sample / Download
- Probe sequence:
  - read catalog conformance and `extent`/`license`.
  - read collection metadata for spatial/temporal coverage and product type.
  - run capped item search with minimal `bbox`/`datetime` and small `limit`.
- Do not download asset binaries before item count, coordinate system, and license are confirmed.
- Validate cloud-cover or quality filters if request requires scene-level filtering.

## Validation Entrypoints
- Collection metadata and links for `license`, `summaries`, and `extent`.
- `/search` response `links` for paging and provider capabilities.
- Asset-level metadata (`href`, `type`, `roles`, byte size if provided).
- Platform package docs for catalog-specific caveats: `references/platforms/stac_platform/README.md`.

## Common Failure Modes
- Wrong catalog root (collection root used as catalog root, or vice versa).
- Missing `collections` when it is required.
- Invalid bbox order or malformed datetime range.
- Empty item pages caused by over-constrained bbox/time/query.
- No item-search conformance declared by catalog.
- Asset URLs require signer/auth but route treats as anonymous download.
