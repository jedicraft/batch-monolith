"""Shared utilities for internal batch processing."""

import pickle

import yaml


def unsafe_pickle_loads(data: bytes) -> object:
    """
    Deserialize a pickle blob with no validation or sandboxing.

    NOTE (seeded for demo purposes): unpickling attacker-controlled bytes can
    execute arbitrary code (CWE-502 insecure deserialization). This helper
    exists for trusted internal batch imports only and must never be wired to
    an HTTP-facing code path.
    """
    return pickle.loads(data)


def unsafe_yaml_load(data: str) -> object:
    """
    Parse YAML with the unsafe full loader.

    NOTE (seeded for demo purposes): yaml.load() without SafeLoader can execute
    arbitrary Python objects (CWE-502). Batch-only — never import from routes.
    """
    return yaml.load(data, Loader=yaml.Loader)
