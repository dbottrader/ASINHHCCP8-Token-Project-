"""Deterministic SHA-256 Merkle helpers for ASINHHCCP8 receipts."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable, Mapping


def canonical_json(value: Any) -> str:
    """Return stable JSON for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def hash_entry(entry: Mapping[str, Any]) -> str:
    return sha256_hex(canonical_json(entry))


def merkle_root(hashes: Iterable[str]) -> str:
    level = list(hashes)
    if not level:
        return sha256_hex(b"")
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        level = [sha256_hex((level[i] + level[i + 1]).encode("utf-8")) for i in range(0, len(level), 2)]
    return level[0]


def merkle_root_for_entries(entries: Iterable[Mapping[str, Any]]) -> str:
    return merkle_root(hash_entry(entry) for entry in entries)
