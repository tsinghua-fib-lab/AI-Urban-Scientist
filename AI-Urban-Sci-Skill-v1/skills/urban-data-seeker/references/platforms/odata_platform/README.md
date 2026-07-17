# OData Platform Tool Package

This is a platform script/tool package, not a SourceSkill.

It handles Open Data Protocol mechanics such as parsing service roots, metadata document URLs, entity sets, and capped query templates. A SourceSkill may list this package under `Tools/Scripts Used`, but this package does not decide whether an OData entity set satisfies a research need.

## Usage

```powershell
python scripts\build_odata_hints.py --need-id need-health-indicator --url https://ghoapi.azureedge.net/api --entity-set Indicator
```

Outputs are neutral platform resource hints only. They are not approvals, plans, completed acquisitions, or validation results.

## Boundaries

- Does not import ai-scientist integrations.
- Does not call route-agent service/UI/downloader/verifier.
- Does not judge research fit.
- Does not claim an entity set is the right table or that query filters are valid.
- Does not write local files or byte counts.
