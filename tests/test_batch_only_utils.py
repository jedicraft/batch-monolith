"""Prove batch-only helpers are not imported by HTTP route modules."""

from __future__ import annotations

import ast
from pathlib import Path

ROUTES_DIR = Path(__file__).resolve().parents[1] / "src" / "routes"
FORBIDDEN_MODULES = ("deserialization", "reporting")
FORBIDDEN_SYMBOLS = (
    "unsafe_pickle_loads",
    "unsafe_yaml_load",
    "build_status_filter_sql",
)


def _route_files() -> list[Path]:
    return sorted(p for p in ROUTES_DIR.glob("*.py") if p.name != "__init__.py")


def test_batch_only_utils_are_absent_from_route_modules():
    offenders: list[str] = []
    for route_file in _route_files():
        source = route_file.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(route_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if any(module.endswith(name) for name in FORBIDDEN_MODULES):
                    offenders.append(f"{route_file.name} imports {module}")
        for symbol in FORBIDDEN_SYMBOLS:
            if symbol in source:
                offenders.append(f"{route_file.name} references {symbol}")

    assert offenders == [], offenders
