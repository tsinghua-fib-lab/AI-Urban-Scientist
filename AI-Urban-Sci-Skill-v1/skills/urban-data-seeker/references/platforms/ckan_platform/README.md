# CKAN Platform Tool Package

This is not a SourceSkill. It is a platform script/tool package for CKAN mechanics that a SourceSkill may cite in `Tools/Scripts Used`.

Use it when a SourceSkill has already decided that a CKAN portal is relevant and needs package search or package metadata hints. This package does not decide research fit, approve resources, download files, or claim completion.

## Tools/Scripts Used

- `scripts/build_ckan_hints.py` parses CKAN package URLs and emits not-final package search and package show resource hints.

## Output Contract

Outputs are not-final platform hints with `consumer_authority` set to `none`. A route runner must still perform resolver, probe, acquisition, and verifier work.
