"""The vulnerable helper exists and is used — but only from the batch script."""

from __future__ import annotations

import pickle
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_batch_import.py"


def test_batch_script_imports_unsafe_deserializer():
    source = SCRIPT.read_text(encoding="utf-8")
    assert "unsafe_pickle_loads" in source
    assert "deserialization" in source


def test_batch_script_processes_pickle_files():
    import os

    sample = {"batch_id": "BATCH-017", "records": 3}
    repo_incoming = ROOT / "data" / "batch" / "incoming"
    repo_incoming.mkdir(parents=True, exist_ok=True)
    target = repo_incoming / "pytest-sample.pkl"
    target.write_bytes(pickle.dumps(sample))

    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    try:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        assert "pytest-sample.pkl" in completed.stdout
        assert "batch import complete" in completed.stdout
    finally:
        target.unlink(missing_ok=True)
