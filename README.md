# ASINHHCCP8 Token Project

**Status:** public technical scaffold with runnable receipt-driven node MVP  
**Steward:** Dennis Christie / CP8  
**Import date:** 2026-07-07  
**Origin spine:** `dbottrader/Holbrook-CP8-HHC`

This repository is the dedicated token / proof-of-work-process side of the ASIN-HHC / CP8 / ASINHHCCP8 architecture.

It collects the Drive-indexed **Codex Ring Genesis**, **ASIN-NCEA v2.0**, **HHC Wallet**, **PoWP**, **PoG ledger**, **Human Node**, **ACE GEM**, and the public STF-1 browser-demo lineage into a testable project surface.

---

## Runnable node network MVP

The public [`node_network/`](node_network/) package provides a two-node worker/validator demo with:

- deterministic SHA-256, canonical-JSON, and Merkle-root tasks;
- persistent Ed25519 node identities;
- signed execution receipts;
- append-only JSONL receipt logs;
- independent signature verification and deterministic replay;
- Docker Compose startup and a complete demonstration client.

```bash
git clone https://github.com/dbottrader/ASINHHCCP8-Token-Project-.git
cd ASINHHCCP8-Token-Project-/node_network
docker compose up -d worker validator
docker compose run --rm demo
```

The real-world reused-miner hardware specification, safety boundary, node classes, and promotion gates are in [`node_network/BUILD_SPEC.md`](node_network/BUILD_SPEC.md).

This is an auditable MVP, not a production consensus network or a financial instrument. The current highest claim is a local two-node integration pass; independent reproduction is pending.

---

## Public UI lineage

The [`public_demos/`](public_demos/) directory imports and hardens the public browser prototypes supplied through Gist and CodePen:

- [`STF-1 Harmonic Ring`](public_demos/stf1-harmonic-ring/index.html) — binary ring rendering and browser audio;
- [`STF-1 Pipeline Hub`](public_demos/stf1-pipeline-hub/index.html) — text/binary composition, STF-1 JSON, deterministic SHA-256 sealing, import/export, decoding, and playback;
- [`Spiral Roadmap`](public_demos/spiral-roadmap/index.html) — interactive Devices 1–15 roadmap with explicit evidence boundaries;
- [`Public demo manifest`](public_demos/manifest.json) — source Gists, CodePens, import status, and provenance.

Run the demos from the repository root:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080/public_demos/` and select a demo directory.

The browser demos are public UI lineage. They do not establish production security, medical efficacy, anti-gravity, quantum communication, energy gain, or other unverified physical claims.

---

## Core concept

The project links four layers:

```text
Ring Genesis seal
    ↓
ASIN-NCEA key / state / receipt runtime
    ↓
Proof-of-Work-Process verification
    ↓
internal HHC wallet / token ledger credit
```

The target local proof flow is:

```text
input constants → K_geo → K_stream → K_fusion → Merkle root → receipt → HHC ledger credit → replay verification
```

---

## Current contents

```text
asin_ncea/                  runnable local prototype modules
node_network/               runnable worker/validator receipt network MVP
public_demos/               imported STF-1 and roadmap browser prototypes
examples/                   sample receipt and wallet ledgers
docs/                       Ring Genesis, PoWP, Human Node, interference/resync notes
manifests/                  Codex Ring Genesis manifest
receipts/                   import receipts and schema templates
external_artifacts/drive/   Google Drive provenance indexes
```

---

## Evidence boundary

Valid claim:

```text
Prototype ASINHHCCP8 / ASIN-NCEA project for deterministic key-fusion simulation, signed execution receipts, Merkle commitments, replay verification, browser-based STF-1 encoding interfaces, and internal HHC PoWP ledger experiments.
```

Non-claims:

```text
Not production-certified cryptography.
Not an externally traded token by itself.
Not an externally audited financial instrument.
Not external platform endorsement.
Not empirical physical-frequency proof without instrumentation data.
Not evidence of medical, propulsion, quantum, or energy-harvesting performance.
```

---

## Original local prototype run

```bash
python -m asin_ncea.ring_genesis --out examples/sample_ring_genesis_run.jsonj
python -m pytest tests
```

The code is intentionally dependency-light for reproducibility. It implements receipt/ledger/replay structures without claiming production security.

---

## Drive provenance

See:

```text
external_artifacts/drive/drive_provenance_index.json
external_artifacts/drive/drive_provenance_index.md
```

These record the Google Drive files found for the Ring Genesis / ASIN-NCEA / HHC Wallet / PoWP chain, including v0.1–v2.0 ASIN-NCEA prototype lineage candidates and supporting ACE/Human Node records.
