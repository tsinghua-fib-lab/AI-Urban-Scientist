# ArcGIS Platform Tool Package

This is a platform script/tool package, not a SourceSkill.

It handles ArcGIS REST mechanics such as parsing FeatureServer/MapServer service URLs, layer ids, and service names, then emitting not-final query and metadata hints. A SourceSkill may list this package under `Tools/Scripts Used`, but this package does not decide whether an ArcGIS layer is suitable for a research need.

## Usage

```powershell
python scripts\build_arcgis_hints.py --need-id need-feature-layer --url https://services.arcgis.com/example/ArcGIS/rest/services/Parcels/FeatureServer/0 --query "parcel polygons"
```

Outputs are neutral platform resource hints only. They are not approvals, plans, completed acquisitions, or validation results.

## Boundaries

- Does not import ai-scientist integrations.
- Does not call route-agent service/UI/downloader/verifier.
- Does not judge research fit.
- Does not claim a FeatureServer query returns the requested layer or geometry.
- Does not write local files or byte counts.
