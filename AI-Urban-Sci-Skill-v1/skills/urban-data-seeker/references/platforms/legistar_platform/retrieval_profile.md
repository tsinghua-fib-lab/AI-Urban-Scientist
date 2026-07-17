# Retrieval Profile

## One-line capability
Not-final platform hints for Legistar legislation search, calendar, and record-entry mechanics across municipal portals.

## Best for
- Resolving Legistar portal URLs into Legislation and Calendar entrypoints
- Emitting legislation search and calendar hints for known Legistar portals
- Deriving record-entry normalization hints once a Legistar portal is identified

## Provides
- Platform metadata for Legistar Legislation and Calendar endpoint parsing
- Mechanism hints for legislation search and calendar record entries
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any Legistar portal worldwide, primarily U.S. municipalities)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether a given ordinance, resolution, agenda, or attachment satisfies a research need (source skills do that)
- Document-portal HTML/PDF planning documents (use document_portal_platform for that)
- Socrata, CKAN, ArcGIS, or other data-portal mechanics (use the relevant platform tool)
- Certifying whether portal copies are official or current (this package emits hints only)

## Typical user expressions
- 我需要解析一个Legistar门户的立法搜索和日历接口
- Parse this Legistar portal URL into legislation and calendar hints
- 帮我了解Legistar平台的立法搜索和日历记录机制

## Nearby alternatives
- document_portal_platform: Pick when the need is planning/document portal HTML/PDF candidates rather than legislation
- socrata_platform: Pick when the portal is Socrata-based open data rather than legislation tracking
- ckan_platform: Pick when the portal is CKAN-based open data rather than legislation tracking

## Retrieval notes
- Positive distinctions: Handles Legistar-specific Legislation and Calendar endpoint normalization for municipal governance portals. Evidence: README.md names Legistar legislation search/calendar/record-entry mechanics; manifest supported_domains confirms scope.
- Negative distinctions: Exclude document_portal_platform for planning document portals; exclude socrata_platform for Socrata data portals; exclude ckan_platform for CKAN data portals.
