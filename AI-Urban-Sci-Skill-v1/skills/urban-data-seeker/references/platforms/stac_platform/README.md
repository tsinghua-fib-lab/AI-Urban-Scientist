# STAC Platform Tool Package

This is a platform script/tool package, not a SourceSkill.

It handles SpatioTemporal Asset Catalog mechanics such as parsing catalog/API roots, collection ids, and item-search parameters, then emitting not-final catalog, collection, and search hints. A SourceSkill may list this package under `Tools/Scripts Used`, but this package does not decide whether a STAC collection or item satisfies a research need.

## Usage

```powershell
python scripts\build_stac_hints.py --need-id need-imagery --url https://planetarycomputer.microsoft.com/api/stac/v1 --collection sentinel-2-l2a --bbox "-74.1,40.6,-73.7,40.9"
```

Outputs are neutral platform resource hints only. They are not approvals, plans, completed acquisitions, or validation results.

## Boundaries

- Does not import ai-scientist integrations.
- Does not call route-agent service/UI/downloader/verifier.
- Does not judge research fit.
- Does not claim item-search requestability or asset usability.
- Does not write local files or byte counts.
