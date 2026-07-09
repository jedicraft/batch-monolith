"""Shared utilities for internal batch processing."""

import pickle


def unsafe_pickle_loads(data: bytes) -> object:
    """
    Deserialize a pickle blob with no validation or sandboxing.

    NOTE (seeded for demo purposes): unpickling attacker-controlled bytes can
    execute arbitrary code (CWE-502 insecure deserialization). This helper
    exists for trusted internal batch imports only and must never be wired to
    an HTTP-facing code path.
    """
    return pickle.loads(data)
