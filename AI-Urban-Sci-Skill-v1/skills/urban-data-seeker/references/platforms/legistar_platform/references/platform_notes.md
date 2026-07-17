# Legistar Platform Notes

Legistar portals commonly expose `Legislation.aspx`, `Calendar.aspx`, and `LegislationDetail.aspx` routes on a city-specific subdomain.

A platform helper can normalize those portal mechanics and emit search or record-entry hints, but the consuming SourceSkill or route runner still owns:

- source-family suitability
- official-copy validation
- attachment validation
- downstream resolver/probe/download/verifier decisions

These notes must not be treated as an answer table or known-source substitute.
