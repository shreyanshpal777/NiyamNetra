import hashlib
import json
from pathlib import Path


def hash_bytes(data: bytes) -> str:
    """Return SHA-256 hex digest of raw bytes."""
    return hashlib.sha256(data).hexdigest()


def hash_file(path: str) -> str:
    """Return SHA-256 hex digest of a file in chunks (memory-safe)."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_json(data: dict) -> str:
    """Return SHA-256 of a dict, deterministically serialized.

    sort_keys + compact separators so identical data always hashes identically.
    """
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_file_hash(path: str, expected_hash: str) -> bool:
    """Confirm a file matches a previously recorded hash (audit check)."""
    return hash_file(path) == expected_hash
