# OECD Data Explorer SourceSkill

## Purpose

Emit not-final source-prior hints for OECD indicator, regional, labor, education, economy, and metropolitan statistics leads through OECD SDMX APIs.

## When To Use

Use when the need asks for global indicators/economy and this source family is a plausible publisher, catalog, repository, or provider.

## Do Not Use

Do not use when a more specific SourceSkill already matches the data family, when the user requires fully open reproducible data and this source is restricted, or when only generic platform mechanics are needed. Never create resource plans, approve URLs, write downloaded files, or claim success.

All emitted payloads must keep `finality=not_final` and `consumer_authority=none`.

## Inputs

- `need_id`
- `need_text`
- `query`
- `geography`
- `time_range`

## Tools/Scripts Used

- `scripts/find_oecd_data.py` emits not-final source-card route hints.
Platform mechanics may be delegated to: `sdmx_platform`.

## Workflow

1. Match the need to the source family, publisher, coverage, access status, and license constraints.
2. Emit the official landing/API/documentation lead from `references/source_card.json`.
3. Preserve missing parameters, authorization requirements, ambiguity, and validation notes.
4. Pass the hint to downstream resolver, probe, acquisition, and verifier stages.

## Outputs

SourceSkill payload with not-final candidate resources, route dossier fragments, and resource intent fragments.

## Failure Rules

If required source parameters, account/key/license approval, or dataset identifiers are missing, emit `needs_follow_up` or `source_landing` only. Do not invent IDs, bypass access controls, or treat commercial/restricted services as open downloads.

## Verification

Validate publisher, endpoint, dataset identity, geography, time coverage, variables, license, access terms, provenance, and downstream resolver/probe/download/verifier results before use.
