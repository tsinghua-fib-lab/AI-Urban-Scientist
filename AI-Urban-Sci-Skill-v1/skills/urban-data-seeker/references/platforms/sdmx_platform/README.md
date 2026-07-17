# SDMX Platform Tool Package

This is a platform script/tool package, not a SourceSkill.

It handles Statistical Data and Metadata eXchange mechanics such as parsing REST base URLs, agency ids, dataflow ids, and series keys, then emitting not-final dataflow metadata and data-query hints. A SourceSkill may list this package under `Tools/Scripts Used`, but this package does not decide whether an SDMX series satisfies a research need.

## Usage

```powershell
python scripts\build_sdmx_hints.py --need-id need-indicator --url https://sdmx.oecd.org/public/rest/v1 --agency OECD.SDD.TPS --dataflow DF_POP_HIST --key A....
```

Outputs are neutral platform resource hints only. They are not approvals, plans, completed acquisitions, or validation results.

## Boundaries

- Does not import ai-scientist integrations.
- Does not call route-agent service/UI/downloader/verifier.
- Does not judge research fit.
- Does not claim a dataflow, key, or structure is requestable.
- Does not write local files or byte counts.
