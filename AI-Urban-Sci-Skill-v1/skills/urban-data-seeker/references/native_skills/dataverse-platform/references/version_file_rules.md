# Dataverse Version and File Rules

## Decision Positioning
- Use this doc when routing Dataverse URLs, DOI/persistent IDs, file listings, or versioned downloads.
- Treat persistent ID resolution as platform-level pre-work, not final dataset acceptance.
- Separate dataset-level authorization from file-level authorization.

## Identifier Handling
- Primary identifier: `persistentId` query parameter or DOI-style identifier in URL.
- `https://{host}/api/datasets/:persistentId/?persistentId={persistentId}` resolves dataset metadata.
- If URL has no `persistentId` query, parse a `doi:` value from the path before routing.
- Use URL encoding for special characters in identifier strings.

## Version Rules
- `:latest` is a convenience default for metadata and file listing, but is not a reproducibility anchor.
- For reproducible results, resolve explicit dataset version (for example, `:2`, `:latest` intentionally chosen by user, or explicit versioned DOI).
- Validate version intent in route output before allowing download.
- Verify citation/provenance:
  - dataset title/version mapping,
  - release date,
  - DOI/persistentId consistency between dataset metadata and landing page.

## File Selection Rules
- File listing comes from dataset API endpoint: `/api/datasets/:persistentId/versions/{version}/files?persistentId=...`.
- File IDs are version-scoped for download routing and should be selected from the matching version file list.
- Confirm chosen file role/format fits task (CSV, parquet, shapefile, raster, etc.).
- Do not use a file ID from a different version without re-validating.
- Download routes normally use a file-level API path with the selected file ID and the same `persistentId` context.

## Probe / Sample / Download
- Probe metadata endpoint first:
  - confirm dataset title, version, access status, license, terms.
- Probe file-list endpoint for each required file:
  - `restricted` flag,
  - size/checksum/type,
  - access role.
- Sample using metadata-only validation before download.
- Before download, confirm whether restricted/embargoed files require explicit terms agreement.

## Validation Entrypoints
- Dataset metadata: `https://{host}/api/datasets/:persistentId/?persistentId={persistentId}`
- Versioned file list: `https://{host}/api/datasets/:persistentId/versions/{version}/files?persistentId={persistentId}`
- Platform package README: `references/platforms/dataverse_platform/README.md`
- Platform notes: `references/platforms/dataverse_platform/references/platform_notes.md`
  
## Common Failure Modes
- Missing identifier in URL and fallback parsing fails.
- Resolver defaults to `latest` but user needs exact reproducible version.
- File ID not present in selected version file list.
- Restricted file flagged in listing but treated as public.
- 401/403 download refusal from access/terms mismatch.
