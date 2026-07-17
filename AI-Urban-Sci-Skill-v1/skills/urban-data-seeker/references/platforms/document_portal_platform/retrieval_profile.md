# Retrieval Profile

## One-line capability
Not-final platform hints for official HTML/PDF document-portal landing and document-candidate normalization mechanics.

## Best for
- Resolving planning and document portal URLs into landing-page and document-candidate components
- Emitting document-candidate hints for known HTML/PDF planning portals
- Deriving document normalization hints once a portal landing page is identified

## Provides
- Platform metadata for document-portal landing-page parsing
- Mechanism hints for linked PDF/HTML document candidates
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any document portal worldwide)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether a document is the right plan, report, or policy artifact (source skills do that)
- Legistar legislation/ordinance search (use legistar_platform for that)
- Socrata, CKAN, ArcGIS, or other data-portal mechanics (use the relevant platform tool)
- Certifying whether a PDF or HTML page is the final governing document (this package emits hints only)

## Typical user expressions
- 我需要解析一个城市规划门户的文档候选
- Parse this planning portal URL into document-candidate hints
- 帮我了解文档门户的HTML/PDF文档候选规范化机制

## Nearby alternatives
- legistar_platform: Pick when the need is legislation/ordinance/resolution search rather than planning documents
- socrata_platform: Pick when the portal is Socrata-based data rather than HTML/PDF documents
- ckan_platform: Pick when the portal is CKAN-based data rather than planning documents

## Retrieval notes
- Positive distinctions: Handles document-portal-specific landing-page and PDF/HTML document-candidate normalization for official planning portals. Evidence: README.md names official HTML/PDF document-portal landing and document-candidate normalization; manifest supported_domains confirms scope.
- Negative distinctions: Exclude legistar_platform for legislation/ordinance search; exclude socrata_platform for Socrata data portals; exclude ckan_platform for CKAN data portals; exclude dataverse_platform for Dataverse dataset mechanics.
