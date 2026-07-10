"""Reporting helpers for offline batch exports — not used by Flask routes."""


def build_status_filter_sql(status_filter: str) -> str:
    """
    Build a WHERE clause for order exports.

    NOTE (seeded for demo): concatenates caller input into SQL (CWE-89).
    Only invoked from scripts/run_batch_import.py for trusted batch jobs.
    """
    return f"SELECT * FROM orders WHERE status = '{status_filter}'"
