# aperture-labs/batch-monolith

**Test Subject Repository #017** — Python/Flask monolith representing the
"shared batch tier" of the Aperture Labs polyglot fleet. Part of the fleet
vulnerability triage experiment.

## Seeded vulnerability (for demo purposes)

- **Class**: Insecure deserialization via `pickle.loads` on untrusted bytes
  (CWE-502).
- **Where**: `src/utils/deserialization.py` exposes `unsafe_pickle_loads()`,
  which unpickles arbitrary bytes with no validation.
- **Reachability**: The helper is **not reachable over HTTP**. It is imported
  only by the internal admin script `scripts/run_batch_import.py`, which reads
  trusted `.pkl` files from `data/batch/incoming/`. Flask routes under
  `src/routes/` handle JSON only and never import the deserializer.
- **Evidence**: `tests/test_route_reachability.py` statically inspects every
  route module and registered Flask view to prove no live endpoint can call
  `unsafe_pickle_loads`. `tests/test_batch_script.py` proves the vulnerable
  code path exists for offline batch use — so a triage agent's "not reachable"
  verdict is falsifiable, not asserted.

Expected fleet-triage outcome: **report only, no PR**.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python -m src.app
```

Health check: `GET http://127.0.0.1:5001/health`
