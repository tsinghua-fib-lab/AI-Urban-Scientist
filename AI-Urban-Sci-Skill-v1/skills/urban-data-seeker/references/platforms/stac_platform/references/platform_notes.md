# STAC Platform Notes

STAC describes geospatial assets with catalog, collection, item, and asset metadata. A STAC API commonly exposes a root catalog, `/collections/{collection_id}`, and `/search` item-search endpoint.

This platform package only builds route-ready hints:

- catalog metadata;
- collection metadata;
- capped item-search templates using collection, bbox, datetime, and limit parameters.

It does not decide whether the assets are appropriate for a domain need. A SourceSkill or route runner must validate collection identity, spatial and temporal coverage, license, asset roles, media types, cloud access requirements, and downstream sampling policy.

## References

- STAC overview: https://stacspec.org/
- STAC specification overview: https://stacspec.org/en/about/stac-spec/
- OGC STAC API community standard: https://docs.ogc.org/cs/25-005/25-005.html
