# ASINHHCCP8 Token Project

**Status:** initial Drive-backed public technical scaffold  
**Steward:** Dennis Christie / CP8  
**Import date:** 2026-07-07  
**Origin spine:** `dbottrader/Holbrook-CP8-HHC`  

This repository is the dedicated token / proof-of-work-process side of the ASIN-HHC / CP8 / ASINHHCCP8 architecture.

It collects the Drive-indexed **Codex Ring Genesis**, **ASIN-NCEA v2.0**, **HHC Wallet**, **PoWP**, **PoG ledger**, **Human Node**, and **ACE GEM** materials into a testable project surface.

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
Prototype ASINHHCCP8 / ASIN-NCEA token project for deterministic key-fusion simulation, Merkle receipts, replay, and internal HHC PoWP ledger crediting.
```

Non-claims:

```text
Not production-certified cryptography.
Not an externally traded token by itself.
Not an externally audited financial instrument.
Not external platform endorsement.
Not empirical physical-frequency proof without instrumentation data.
```

---

## Quick local run

```bash
python -m asin_ncea.ring_genesis --out examples/sample_ring_genesis_run.jsonj
python -m pytest tests
```

The code is intentionally dependency-light for reproducibility. It implements the receipt/ledger/replay structure without claiming production security.

---

## Drive provenance

See:

```text
external_artifacts/drive/drive_provenance_index.json
external_artifacts/drive/drive_provenance_index.md
```

These record the Google Drive files found for the Ring Genesis / ASIN-NCEA / HHC Wallet / PoWP chain, including v0.1–v2.0 ASIN-NCEA prototype lineage candidates and supporting ACE/Human Node records.
