# TheCakeIsALieInc/batch-monolith

**Aperture Labs · Test Subject #017** — Python/Flask monolith in the batch tier of
The Cake Is A Lie Inc.'s polyglot fleet.

## Seeded vulnerabilities (for demo purposes)

All three helpers are used by `scripts/run_batch_import.py` only — **not**
reachable from Flask HTTP routes.

| # | Class | Component | CWE |
|---|-------|-----------|-----|
| 1 | Unsafe pickle deserialization | `unsafe_pickle_loads()` | CWE-502 |
| 2 | Unsafe YAML load | `unsafe_yaml_load()` | CWE-502 |
| 3 | Dynamic SQL concatenation | `build_status_filter_sql()` | CWE-89 |

Expected fleet-triage outcome: **report only, no PR** (for each alert).

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python -m src.app
```
