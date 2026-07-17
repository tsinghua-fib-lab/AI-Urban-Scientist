# Validation Rules

- Match requested vehicle type before treating a file as a candidate resource.
- Match requested year and month before emitting a monthly file candidate.
- Preserve `finality=not_final` and `consumer_authority=none`.
- Do not emit approved URLs, resource plans, downloaded paths, byte counts, or verifier success.
