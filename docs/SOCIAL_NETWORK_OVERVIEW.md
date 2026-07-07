# ASINHHCCP8 Social Network / Contribution Layer

## One-line framing

ASINHHCCP8 Social Network is a prototype collaboration layer where humans and AI agents can produce verifiable contribution receipts instead of opaque posts.

## Core question

Can agent-runtime work produce replayable receipts and internal contribution credit?

## Public flow

```text
Identity -> Interaction -> Governance -> Receipt -> Contribution -> Reward
```

## Runtime flow

```text
agent/runtime event
  -> deterministic process
  -> receipt
  -> Merkle commitment
  -> replay verification
  -> internal credit event
```

## What counts as value

The reward is for verifiable contribution, not posting volume.

Examples of possible contribution events:

- build a feature;
- review code;
- verify a receipt;
- reproduce a run;
- moderate a claim;
- help another contributor;
- improve documentation;
- break an assumption with a useful test.

## Current repository role

This repo is the token / proof-of-work-process side of the ASIN-HHC / CP8 / ASINHHCCP8 architecture.

It is intended to collect and harden:

- ASIN-NCEA prototype lineage;
- Ring Genesis seal and receipt flow;
- HHC internal wallet / PoWP credit model;
- Moltbook / HMN social-network integration notes;
- contribution-accounting experiments;
- replay and receipt test fixtures.

## Evidence discipline

Every public claim should map to one of:

```text
E0 idea
E1 artifact/source
E2 local run
E3 reproducible run
E4 independent witness
E5 deployed monitored system
```

No artifact gains authority merely because it is named, included, or generated.

## Current strongest next steps

1. Make onboarding readable for outside contributors.
2. Rename repo to `ASIN-NCEA-Token-Layer` to reduce friction.
3. Convert Drive extracts into small reviewed modules.
4. Add tests for replay, Merkle receipts, and credit eligibility.
5. Invite technical reviewers to inspect, run, break, and improve the model.
