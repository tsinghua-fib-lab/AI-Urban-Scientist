# Document Portal Platform Tool Package

This is a platform script/tool package, not a SourceSkill.

It handles common mechanics for official planning and document portals that expose HTML landing pages and linked PDF/HTML documents. A SourceSkill may list this package under `Tools/Scripts Used`, but this package does not decide whether a document is the right plan, report, or policy artifact for a research need.

## Usage

```powershell
python scripts\build_document_portal_hints.py --need-id need-city-plan --url https://generalplan.sfplanning.org/ --document-url https://www.london.gov.uk/sites/default/files/the_london_plan_2021.pdf
```

Outputs are neutral platform resource hints only. They are not approvals, plans, completed acquisitions, or validation results.

## Boundaries

- Does not import ai-scientist integrations.
- Does not call route-agent service/UI/downloader/verifier.
- Does not judge research fit.
- Does not certify whether a PDF or HTML page is the final governing document.
- Does not write local files or byte counts.
