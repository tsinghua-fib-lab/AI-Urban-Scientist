# Legistar Platform Tool Package

This is a platform script/tool package, not a SourceSkill.

It handles common Legistar portal mechanics such as normalizing Legislation and Calendar entrypoints and emitting not-final portal hints. A SourceSkill may list this package under `Tools/Scripts Used`, but this package does not decide whether a given ordinance, resolution, agenda, or attachment satisfies a research need.

## Usage

```powershell
python scripts\build_legistar_hints.py --need-id need-city-ordinances --url https://phila.legistar.com/ --query zoning
```

Outputs are neutral platform resource hints only. They are not approvals, plans, completed acquisitions, or validation results.

## Boundaries

- Does not import ai-scientist integrations.
- Does not call route-agent service/UI/downloader/verifier.
- Does not judge research fit.
- Does not certify whether portal copies are official or current.
- Does not write local files or byte counts.
