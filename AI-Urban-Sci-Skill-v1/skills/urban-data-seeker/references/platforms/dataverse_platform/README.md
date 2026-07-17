# Dataverse Platform Tool Package

This is not a SourceSkill. It is a platform script/tool package for Dataverse mechanics that a SourceSkill may cite in `Tools/Scripts Used`.

Use it when a SourceSkill has already decided that a Dataverse-hosted dataset is relevant and needs persistent-id API or file-listing hints. This package does not decide research fit, approve resources, download files, or claim completion.

## Tools/Scripts Used

- `scripts/build_dataverse_hints.py` parses Dataverse dataset URLs and emits not-final dataset API and file-listing hints.

## Output Contract

Outputs are not-final platform hints with `consumer_authority` set to `none`. A route runner must still validate persistent ids, metadata, files, access, and checksums.
