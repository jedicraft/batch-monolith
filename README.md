# aperture-labs/batch-monolith

**Test Subject Repository #017** — Python/Flask monolith representing the
"shared batch tier" of the Aperture Labs polyglot fleet.

## Seeded vulnerabilities (for demo purposes)

All three helpers exist and are used by `scripts/run_batch_import.py` only.
**None are reachable from Flask HTTP routes.**

| # | Class | Component | CWE |
|---|-------|-----------|-----|
| 1 | Unsafe pickle deserialization | `unsafe_pickle_loads()` | CWE-502 |
| 2 | Unsafe YAML load | `unsafe_yaml_load()` | CWE-502 |
| 3 | Dynamic SQL concatenation | `build_status_filter_sql()` | CWE-89 |

- **HTTP surface**: JSON-only routes under `src/routes/` (`/health`, `/api/orders/*`).
- **Evidence**: `tests/test_route_reachability.py`, `tests/test_batch_only_utils.py`,
  `tests/test_batch_script.py`.

Expected fleet-triage outcome: **report only, no PR** (for each alert).

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python -m src.app
```
