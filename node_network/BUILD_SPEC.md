# ASIN-HHC ↔ CP8 Real-World Node Build Specification

**Specification status:** E2 local integration pass in the authoring environment; independent reproduction pending.

## 1. Node classes

### NODE-LITE — reused mining or desktop hardware

- CPU: 4 physical cores or better
- RAM: 16 GB minimum
- GPU: optional; one or more cards with 6 GB+ VRAM for later inference workers
- Storage: 500 GB SSD minimum
- Network: stable 50 Mbps connection
- Power: measured at the wall; configure a conservative card power limit
- Role: hashing, receipt verification, replay, lightweight evaluation

### NODE-WORKER — multi-GPU rig

- CPU: 8+ cores
- RAM: 32–64 GB
- GPU: 2–8 NVIDIA or AMD cards; record exact model, VRAM, VBIOS, driver, and power limit
- Storage: 1–2 TB NVMe for model/artifact cache
- Network: 100 Mbps+; wired Ethernet preferred
- Power: dedicated correctly rated circuits, breakers, cabling, and ventilation
- Role: batched inference, evaluation, rendering, proof generation, scientific workloads

### NODE-VALIDATOR

- CPU: 8+ cores
- RAM: 32 GB
- GPU: optional
- Storage: mirrored SSD/NVMe preferred
- Security: TPM 2.0, HSM, or hardware-backed keys targeted for production
- Role: policy enforcement, signature verification, deterministic replay, registry decisions

## 2. Minimum software baseline

- Linux: Ubuntu Server 24.04 LTS, Debian 12, or NixOS
- Python: 3.11+
- Container runtime: Docker or Podman
- Serialization: canonical JSON now; deterministic CBOR is a future option
- Hash: SHA-256 now; SHA-3 may be added as a protocol-negotiated suite
- Signature: Ed25519
- Receipt storage: append-only JSONL in MVP; content-addressed replicated log later
- Observability target: Prometheus metrics and Grafana dashboards
- Peer transport target: authenticated TLS plus libp2p or a comparably auditable transport

## 3. Reused ETH-miner conversion checklist

1. Inventory each GPU, riser, power connector, PSU, breakout board, and cable.
2. Remove damaged risers, overheated connectors, and mixed unsafe power paths.
3. Do not power a GPU and its riser from conflicting PSUs without correct common-ground design.
4. Set conservative GPU power limits before sustained compute.
5. Record wall power, GPU temperature, hotspot temperature, fan speed, and error rate.
6. Run memory and workload stability tests before registering the node as available.
7. Publish capabilities honestly: GPU model, VRAM, supported runtime, benchmark, and failure rate.
8. Keep the validator role separate from untrusted workload execution where practical.

Electrical work and high-current GPU rigs can cause fire, shock, or equipment damage. Circuit sizing and mains wiring must be handled by a qualified person under local electrical code.

## 4. Registration document

Every node should eventually publish a signed capability document containing:

```json
{
  "node_id": "asin-hhc-cp8-node-001",
  "roles": ["worker"],
  "cpu": {"cores": 8, "architecture": "x86_64"},
  "memory_gb": 32,
  "gpus": [
    {"vendor": "NVIDIA", "model": "P106-100", "vram_gb": 6, "count": 4}
  ],
  "tasks": ["sha256", "canonical_json", "merkle_root"],
  "protocol": "asin-hhc-cp8-receipt-v1",
  "public_key_ed25519": "BASE64_PUBLIC_KEY",
  "evidence_grade": "E2_LOCAL"
}
```

The document describes capability only. It does not automatically confer authority.

## 5. Promotion gates

### Gate A — local execution

- node starts from documented commands;
- self-test passes;
- receipt is signed;
- append-only log is written.

### Gate B — two-node replay

- worker and validator use different keys;
- validator verifies signature;
- validator re-executes task;
- output and commitments match.

### Gate C — independent reproduction

- outside reviewer clones a tagged release;
- reviewer records hardware and software environment;
- reviewer reproduces the demo without unpublished files;
- reviewer publishes receipt hashes and failures.

### Gate D — hardened pilot

- TLS and authenticated peer enrollment;
- governed key registry;
- resource limits and sandboxing;
- metrics, alerting, and incident records;
- signed releases and SBOM;
- adversarial and fault-injection testing.

No claim should be promoted beyond the highest gate actually passed.
