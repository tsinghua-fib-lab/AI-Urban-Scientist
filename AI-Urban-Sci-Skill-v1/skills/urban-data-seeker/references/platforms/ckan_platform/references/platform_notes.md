# CKAN Platform Notes

- CKAN portals usually expose `/api/3/action/package_search` and `/api/3/action/package_show`.
- A package slug can be parsed from many dataset URLs, but a resolver must validate it against the target portal.
- Package resources can include links, files, APIs, and stale metadata; do not treat package metadata as a final data file.
- SourceSkills use this package only for platform mechanics after source-family fit is established.
