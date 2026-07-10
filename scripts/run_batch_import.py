#!/usr/bin/env python3
"""
Internal admin/batch job — not exposed via Flask.

Reads trusted pickle exports dropped into data/batch/incoming/ and processes
them offline. This is the only supported caller of unsafe_pickle_loads().
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.deserialization import unsafe_pickle_loads, unsafe_yaml_load  # noqa: E402
from src.utils.reporting import build_status_filter_sql  # noqa: E402


def process_incoming_batch(incoming_dir: Path) -> int:
    processed = 0
    for pickle_path in sorted(incoming_dir.glob("*.pkl")):
        payload = pickle_path.read_bytes()
        record = unsafe_pickle_loads(payload)
        print(f"imported {pickle_path.name}: {record!r}")
        processed += 1
    for yaml_path in sorted(incoming_dir.glob("*.yaml")):
        document = unsafe_yaml_load(yaml_path.read_text(encoding="utf-8"))
        print(f"imported {yaml_path.name}: {document!r}")
        processed += 1
    if processed:
        print(f"export filter SQL template: {build_status_filter_sql('pending')}")
    return processed


def main() -> int:
    incoming = ROOT / "data" / "batch" / "incoming"
    incoming.mkdir(parents=True, exist_ok=True)
    count = process_incoming_batch(incoming)
    print(f"batch import complete ({count} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
