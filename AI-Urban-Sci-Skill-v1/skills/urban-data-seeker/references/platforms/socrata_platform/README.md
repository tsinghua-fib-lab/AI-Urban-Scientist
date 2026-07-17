# Socrata Platform Tool Package

This is a platform script/tool package, not a SourceSkill.

It handles Socrata mechanics such as parsing dataset URLs, extracting domains and view ids, and emitting not-final export/search hints. A SourceSkill may list this package under `Tools/Scripts Used`, but this package does not decide whether a Socrata dataset is suitable for a research need.

## Usage

```powershell
python scripts\build_socrata_hints.py --need-id need-open-data-table --url https://data.cityofnewyork.us/Transportation/Taxi-Zone-Lookup/755u-8jsi --query "taxi zone lookup"
```

Outputs are neutral platform resource hints only. They are not approvals, plans, completed acquisitions, or validation results.

## Boundaries

- Does not import ai-scientist integrations.
- Does not call route-agent service/UI/downloader/verifier.
- Does not judge research fit.
- Does not claim that rows exports are available.
- Does not write local files or byte counts.
