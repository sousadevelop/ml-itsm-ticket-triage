# Data Directory

This directory is reserved for synthetic, sanitized, or experimentally derived datasets.

Rules:

- do not store real production tickets;
- keep raw data out of version control whenever possible;
- document provenance, anonymization, and sampling assumptions for every dataset used in experiments.

Suggested layout:

- `raw/` for non-versioned local inputs;
- `processed/` for derived artifacts;
- `reports/` for evaluation summaries and dataset notes.
