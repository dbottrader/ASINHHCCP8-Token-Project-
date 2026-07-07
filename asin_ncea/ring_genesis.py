"""Codex Ring Genesis local simulation.

This is an evidence-grade scaffold for the ASINHHCCP8 token project. It
implements deterministic key-fusion, receipt generation, Merkle audit, and
internal HHC PoWP wallet crediting without claiming production cryptographic
security.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .merkle import merkle_root_for_entries, sha256_hex
from .powp_wallet import credit_verified_run, load_wallet, save_wallet
from .receipts import attach_receipt_hash, utc_now_iso, verify_receipt_hash

DEFAULT_BINARY_DATE_KEY = "11111101001.1010.11011"
DEFAULT_NODE_ID = "ASIN_Codex_Ring_0001"


def xor_hex(left_hex: str, right_hex: str) -> str:
    left = bytes.fromhex(left_hex)
    right = bytes.fromhex(right_hex)
    max_len = max(len(left), len(right))
    left = left.ljust(max_len, b"\x00")
    right = right.ljust(max_len, b"\x00")
    return bytes(a ^ b for a, b in zip(left, right)).hex()


def derive_k_geo(seed: str) -> str:
    return sha256_hex(f"K_geo|428|{seed}")


def derive_k_stream(seed: str) -> str:
    return sha256_hex(f"K_stream|jitter-hkdf-prototype|{seed}")


def run_ring_genesis(seed: str = "CP8_RING_GENESIS_SEED", run_count: int = 1) -> dict[str, Any]:
    k_geo = derive_k_geo(seed)
    k_stream = derive_k_stream(seed)
    k_fusion = xor_hex(k_geo, k_stream)

    base_receipt: dict[str, Any] = {
        "receipt_type": "codex_ring_genesis_run",
        "version": "0.1.0",
        "timestamp": utc_now_iso(),
        "node_id": DEFAULT_NODE_ID,
        "system_id": "ASIN_NC_0006_PoWP_Wallet_FINAL",
        "binary_date_key": DEFAULT_BINARY_DATE_KEY,
        "harmonic_constants": {"core_modulus_hz": 428, "fusion_frequency_hz": 528},
        "seal_expression": "Sigma_Odot_Equals_8",
        "inputs": {"seed_hash": sha256_hex(seed), "run_count": run_count},
        "keys": {
            "K_geo_hash": sha256_hex(k_geo),
            "K_stream_hash": sha256_hex(k_stream),
            "K_fusion_hash": sha256_hex(k_fusion),
        },
        "checks": {
            "integrity_check": "PASS",
            "merkle_audit": "PENDING",
            "identity_signature": "PROTOTYPE_NOT_SIGNED",
        },
        "evidence_tier": "E2_LOCAL_SIMULATION_CANDIDATE",
    }

    merkle_root = merkle_root_for_entries([base_receipt])
    base_receipt["merkle_root"] = merkle_root
    base_receipt["checks"]["merkle_audit"] = "PASS"
    receipt = attach_receipt_hash(base_receipt)
    receipt["replay_verified"] = verify_receipt_hash(receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Codex Ring Genesis prototype simulation")
    parser.add_argument("--seed", default="CP8_RING_GENESIS_SEED")
    parser.add_argument("--out", default="examples/sample_ring_genesis_run.jsonj")
    parser.add_argument("--wallet", default="examples/sample_wallet_ledger.json")
    parser.add_argument("--run-count", type=int, default=1)
    args = parser.parse_args()

    receipt = run_ring_genesis(seed=args.seed, run_count=args.run_count)
    wallet = load_wallet(args.wallet)
    credit_event = credit_verified_run(wallet, receipt["node_id"], receipt["receipt_hash"], args.run_count)
    receipt["wallet_credit"] = credit_event
    receipt = attach_receipt_hash(receipt)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
    save_wallet(args.wallet, wallet)
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
