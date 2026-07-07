"""Internal HHC Proof-of-Work-Process wallet ledger prototype.

This module intentionally models an internal prototype ledger, not an externally
traded token or production settlement layer.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_POWP_REWARD = 10.0


def load_wallet(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {"wallets": {}, "events": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save_wallet(path: str | Path, wallet: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(wallet, indent=2, sort_keys=True), encoding="utf-8")


def credit_verified_run(wallet: dict[str, Any], node_id: str, receipt_hash: str, run_count: int) -> dict[str, Any]:
    reward = BASE_POWP_REWARD * (1.0 + (run_count * 0.001))
    wallets = wallet.setdefault("wallets", {})
    account = wallets.setdefault(node_id, {"balance": 0.0, "total_runs": 0})
    account["balance"] = round(float(account.get("balance", 0.0)) + reward, 12)
    account["total_runs"] = int(account.get("total_runs", 0)) + 1
    event = {
        "type": "powp_credit",
        "node_id": node_id,
        "receipt_hash": receipt_hash,
        "run_count": run_count,
        "reward": reward,
        "ledger_mode": "internal_prototype",
    }
    wallet.setdefault("events", []).append(event)
    return event
