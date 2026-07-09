"""Prove the insecure deserializer is not reachable from any live Flask route."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from src.app import create_app

ROUTES_DIR = Path(__file__).resolve().parents[1] / "src" / "routes"
VULN_SYMBOL = "unsafe_pickle_loads"
VULN_MODULE_SUFFIX = "deserialization"


def _route_source_files() -> list[Path]:
    return sorted(p for p in ROUTES_DIR.glob("*.py") if p.name != "__init__.py")


def _module_imports_deserialization(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.endswith(VULN_MODULE_SUFFIX):
                return True
            for alias in node.names:
                if alias.name == VULN_SYMBOL:
                    return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if VULN_MODULE_SUFFIX in alias.name:
                    return True
    return False


def test_route_modules_do_not_import_unsafe_deserializer():
    offenders: list[str] = []
    for route_file in _route_source_files():
        tree = ast.parse(route_file.read_text(encoding="utf-8"), filename=str(route_file))
        if _module_imports_deserialization(tree):
            offenders.append(str(route_file.relative_to(ROUTES_DIR.parents[1])))
        source = route_file.read_text(encoding="utf-8")
        if VULN_SYMBOL in source:
            offenders.append(f"{route_file.name} references {VULN_SYMBOL}")

    assert offenders == [], f"route modules must not touch deserializer: {offenders}"


def test_registered_view_functions_do_not_reference_unsafe_deserializer():
    app = create_app()
    offenders: list[str] = []

    for endpoint, view_func in app.view_functions.items():
        if VULN_MODULE_SUFFIX in (view_func.__module__ or ""):
            offenders.append(f"{endpoint} defined in {view_func.__module__}")
            continue
        try:
            source = inspect.getsource(view_func)
        except OSError:
            continue
        if VULN_SYMBOL in source or VULN_MODULE_SUFFIX in source:
            offenders.append(f"{endpoint} references deserializer in source")

    assert offenders == [], f"live Flask views must not reach deserializer: {offenders}"


def test_every_http_route_is_accounted_for():
    app = create_app()
    rules = sorted(
        rule.rule for rule in app.url_map.iter_rules() if rule.endpoint != "static"
    )
    assert rules == ["/api/orders", "/api/orders/<order_id>", "/api/orders/search", "/health"]
