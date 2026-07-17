# GTFS Feed Validation Rules

- Treat feed URLs as not-final leads.
- Future validation must open the GTFS zip and require `stops.txt`, `routes.txt`, and `trips.txt`.
- Do not claim schedule coverage until service dates and requested modes are checked.
- Do not use this skill to validate downloads or local files.
