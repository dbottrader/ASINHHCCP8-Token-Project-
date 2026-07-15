# ASINHHCCP8 Public UI Lineage

This directory imports the public browser-based prototypes that preceded the runnable worker/validator node package.

The demos are preserved as engineering lineage and public review surfaces. They are not evidence that any proposed physical, medical, propulsion, quantum, or energy-harvesting mechanism has been experimentally validated.

## Included demonstrations

### STF-1 Harmonic Ring

A compact ring-sector rendering of a binary payload with browser audio playback.

- Local file: [`stf1-harmonic-ring/index.html`](stf1-harmonic-ring/index.html)
- Source Gist: https://gist.github.com/dbottrader/5086c109525a72bb3a3be3721dc2cb3c
- CodePen lineage: https://codepen.io/dennismchristie222/pen/KwVZqQr

### STF-1 Pipeline Hub

A single-file browser application for text/binary conversion, ring rendering, STF-1 bundle generation, SHA-256 sealing, decoding, import/export, and audio playback.

- Local file: [`stf1-pipeline-hub/index.html`](stf1-pipeline-hub/index.html)
- Source Gist: https://gist.github.com/dbottrader/390821c9f5262c06311698849bd440ba
- CodePen lineage: https://codepen.io/dennismchristie222/pen/bNEaRLM

### Spiral Roadmap

An interactive UI roadmap for Devices 1–15 and the original STF-1 mini-spec.

- Local file: [`spiral-roadmap/index.html`](spiral-roadmap/index.html)
- Source Gist: https://gist.github.com/dbottrader/be9d086891fafd806c67f984768c9f64
- CodePen lineage: https://codepen.io/dennismchristie222/pen/qEbpjPO
- Additional public revision supplied by the author: https://codepen.io/dennismchristie222/pen/PwZEjKJ

## Relationship to the operational node MVP

The UI lineage expresses the earlier `Compose -> Seal -> Play -> Verify` workflow. The runnable [`../node_network/`](../node_network/) package converts that idea into a narrower auditable execution path:

```text
input
  -> deterministic task
  -> canonical claim
  -> SHA-256 commitment
  -> Ed25519 signature
  -> append-only receipt
  -> independent replay verification
```

The browser demos and node runtime therefore have different evidence roles:

- browser demos: visual encoding, interaction design, bundle concepts, and public lineage;
- node runtime: executable receipt generation, signature verification, and deterministic replay;
- future work: authenticated peer enrollment, governed capability registry, GPU task adapters, resource metering, sandboxing, monitoring, and independent reproduction.

## Run locally

Each demo is a single HTML file. Open it directly in a modern browser, or serve the repository root:

```bash
python -m http.server 8080
```

Then open:

```text
http://localhost:8080/public_demos/stf1-harmonic-ring/
http://localhost:8080/public_demos/stf1-pipeline-hub/
http://localhost:8080/public_demos/spiral-roadmap/
```

Browser audio requires a user gesture. SHA-256 sealing uses the Web Crypto API and may require a secure context on some browsers.
