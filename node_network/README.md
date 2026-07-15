# ASIN-HHC ↔ CP8 Node Network MVP

A runnable, public prototype for converting reused GPU/compute nodes into a **receipt-driven verification network**.

This first release deliberately keeps the execution surface small enough to audit. It runs deterministic tasks, signs execution claims with Ed25519, records append-only JSONL receipts, and lets an independent validator replay the task before accepting the result.

## What is operational now

- HTTP worker and validator nodes;
- persistent Ed25519 node identities;
- canonical JSON serialization;
- SHA-256 artifact hashing;
- deterministic canonicalization and Merkle-root tasks;
- signed execution receipts;
- independent signature and replay verification;
- append-only local receipt logs;
- two-node Docker Compose demo.

It does **not** yet implement global consensus, token issuance, GPU model inference, remote attestation, slashing, or production-grade peer discovery.

## Run the network

Prerequisites: Docker Engine with the Compose plugin.

```bash
git clone https://github.com/dbottrader/ASINHHCCP8-Token-Project-.git
cd ASINHHCCP8-Token-Project-/node_network

docker compose up -d worker validator
docker compose run --rm demo
```

A successful run ends with:

```json
{
  "valid": true,
  "signature_valid": true,
  "replay_valid": true
}
```

Stop the services:

```bash
docker compose down
```

Delete generated node keys and receipt volumes only when intentionally resetting identity:

```bash
docker compose down --volumes
```

## Run without Docker

Python 3.11+ is required.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python node.py self-test
python node.py serve --port 8001 --node-id worker-001 --role worker --data-dir ./data/worker
python node.py serve --port 8002 --node-id validator-001 --role validator --data-dir ./data/validator
python demo_client.py
```

Run the two `serve` commands in separate terminals.

## API

### Worker health

```bash
curl http://localhost:8001/v1/health
```

### Execute a deterministic task

```bash
curl -s http://localhost:8001/v1/execute \
  -H 'content-type: application/json' \
  -d '{"task_id":"demo-001","kind":"sha256","input":{"message":"hello CP8"}}'
```

Supported task kinds:

- `sha256`: hashes canonical JSON input;
- `canonical_json`: returns deterministic JSON serialization;
- `merkle_root`: computes a domain-separated SHA-256 Merkle root over an input array.

### Verify and replay a receipt

POST the worker's receipt to `http://localhost:8002/v1/verify`:

```json
{
  "receipt": { "...": "worker receipt" },
  "replay": true
}
```

The validator checks:

1. the canonical claim hash;
2. the Ed25519 signature;
3. input and output SHA-256 commitments;
4. deterministic replay equality.

## Receipt law

```text
Capability != Authority
No Receipt = No Promotion
Replay Supersedes Narration
Reality Retains Veto
```

A worker can produce a result. That alone does not grant it authority. Promotion requires a valid receipt and an independently replayed result.

## Security boundary

This is an auditable MVP, not a production security certification.

Current limitations:

- public keys are self-asserted and not yet anchored in a governed registry;
- HTTP is unencrypted unless placed behind TLS;
- no Byzantine consensus or Sybil resistance exists yet;
- node keys are file-based rather than TPM/HSM-backed;
- task kinds are intentionally narrow and CPU-based;
- no financial value should be assigned to prototype credit events.

The next hardening gates are documented in [`BUILD_SPEC.md`](BUILD_SPEC.md).
