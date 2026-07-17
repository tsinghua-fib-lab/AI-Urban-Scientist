# Routing Rules

## Priority

1. Exact source aliases beat every other signal.
2. URL and domain fingerprints beat topic similarity.
3. Platform fingerprints route to platform skills only after the host or syntax is clear.
4. Do not include family or discovery skills in this integrated package; `urban-data-seeker` is the only router.
5. If no bundled source or platform route is viable, report `external_candidate_required`.

## Scoring Signals

- Exact alias or named source: +120
- URL/domain match: +110
- Platform fingerprint: +90
- Topic phrase match: +45
- Geography/action compatibility: +15
- Concrete source when explicitly named: +20
- Platform when request is broad: +15
- Do not score non-executable support entries in this package.
- Auth-required or restricted source when user asks for direct download: -40
- Homepage-only or interactive selection required: return a boundary, not a download claim.

## Access Boundary Rules

- Treat API keys as optional only when public bounded reads are documented or a probe confirms unauthenticated access.
- Treat login, institutional access, terms gates, embargoes, or commercial restrictions as access boundaries.
- Treat WAF/browser blocking separately from authorization failures.
- Do not classify a platform mismatch as an auth failure.

## Bundle Boundary

This package intentionally contains 25 selected platform/source skills, not the full 144-skill native universe. If the request needs an unbundled source, report `external_candidate_required` or route to the closest bundled platform skill for metadata probing.
