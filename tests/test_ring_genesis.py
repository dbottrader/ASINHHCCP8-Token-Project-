from asin_ncea.merkle import merkle_root_for_entries
from asin_ncea.ring_genesis import derive_k_geo, derive_k_stream, run_ring_genesis, xor_hex
from asin_ncea.receipts import verify_receipt_hash
from asin_ncea.powp_wallet import credit_verified_run


def test_key_derivation_is_deterministic():
    assert derive_k_geo("x") == derive_k_geo("x")
    assert derive_k_stream("x") == derive_k_stream("x")
    assert derive_k_geo("x") != derive_k_stream("x")


def test_xor_hex_is_deterministic():
    assert xor_hex("0f", "f0") == "ff"
    assert xor_hex("00", "ff") == "ff"


def test_ring_genesis_receipt_verifies():
    receipt = run_ring_genesis(seed="test", run_count=1)
    assert receipt["checks"]["integrity_check"] == "PASS"
    assert receipt["checks"]["merkle_audit"] == "PASS"
    assert receipt["replay_verified"] is True
    assert verify_receipt_hash(receipt) is True


def test_merkle_root_changes_with_entry_content():
    one = merkle_root_for_entries([{"a": 1}])
    two = merkle_root_for_entries([{"a": 2}])
    assert one != two


def test_wallet_credit_event():
    wallet = {"wallets": {}, "events": []}
    event = credit_verified_run(wallet, "node", "receipt", 1)
    assert event["type"] == "powp_credit"
    assert wallet["wallets"]["node"]["total_runs"] == 1
    assert wallet["wallets"]["node"]["balance"] > 10.0
