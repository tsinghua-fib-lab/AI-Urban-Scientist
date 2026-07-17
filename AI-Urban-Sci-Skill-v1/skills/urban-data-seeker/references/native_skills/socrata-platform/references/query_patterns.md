# Socrata Query Patterns

## Decision Positioning
- Use this document when the user path contains a Socrata domain plus 4x4 view id, or when a query must be prepared for table exports.
- Confirm fingerprints before routing: domain + valid Socrata view id format (`xxxx-xxxx`).
- Treat all export or catalog hints as non-final until field and schema checks pass.

## Query Patterns
- Dataset metadata endpoint: `https://{domain}/api/views/{view_id}.json`
- Rows export endpoint: `https://{domain}/resource/{view_id}.csv`
- Catalog search endpoint: `https://{domain}/browse?limitTo=datasets&q={search_terms}`
- SoQL-style fields for `rows.csv`: `?$select=col1,col2&$where=...&$order=...&$limit=10`
- SoQL pagination is usually `&$offset=...` on exports; fallback to smaller request windows when unknown.
- Optional app token:
  - include `$$app_token={token}` in exported queries when a token is available.
  - expect stricter limits/429 throttling without a token.

## Probe / Sample / Download
- Probe before download:
  - validate dataset id/domain, then read metadata first.
  - prefer `GET` sample with small `$limit` and tight `$select`.
- `HEAD` checks alone are not authoritative for rows export eligibility.
- Do not mark as ready-to-download until response shape, field names, and row counts are validated.

## Field Discovery
- Use `/api/views/{view_id}.json` to read:
  - column IDs/names
  - row counts / last updated
  - row data types and access restrictions.
- If column names are ambiguous, resolve via query aliasing with `$select`.

## Common Failure Modes
- Invalid view id format or domain mismatch.
- Response is not CSV or includes error payload.
- Missing `limit` with wide columns causing timeout.
- Token missing in rate-limited environments.
- Mistaking catalog search output as downloaded data.
