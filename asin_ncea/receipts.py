"""Receipt helpers for Ring Genesis prototype runs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .merkle import canonical_json, sha256_hex


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def attach_receipt_hash(receipt: dict[str, Any]) -> dict[str, Any]:
    copy = dict(receipt)
    copy.pop("receipt_hash", None)
    copy["receipt_hash"] = sha256_hex(canonical_json(copy))
    return copy


def verify_receipt_hash(receipt: dict[str, Any]) -> bool:
    expected = receipt.get("receipt_hash")
    if not expected:
        return False
    copy = dict(receipt)
    copy.pop("receipt_hash", None)
    return sha256_hex(canonical_json(copy)) == expected
