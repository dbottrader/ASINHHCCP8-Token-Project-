# Official ASIN-HHC Ecosystem Receiving Wallet

**Designation date:** 2026-11-02  
**Network:** Base Mainnet (chain ID 8453)  
**Asset accepted at this address:** Native ETH on Base  
**Role:** Public ecosystem receiving address designated by the project owner for project operations and ecosystem donations. It is not designated as a personal-donation address.

## Canonical address

```text
0xC9a22B7685f14683A98a0f174BF5F1C92C7125DD
```

Explorer: https://basescan.org/address/0xC9a22B7685f14683A98a0f174BF5F1C92C7125DD

## Important distinctions

- This is a receiving wallet address, **not** an HHC token contract address.
- Do not use this address in place of an ERC-20 contract, mint authority, signing key, verifier address, or any other technically distinct address.
- Send only the asset and network supported by the receiving wallet instructions.
- The address designation is owner-provided. This document does not independently establish custody, signing authority, token issuance, or any on-chain transaction.
- Never publish private keys, seed phrases, or signing credentials.

## Current implementation evidence (checked 2026-11-02)

The live Supabase ledger-backend configuration reports `simulated` as active with note `Default. HMAC-signed DSSE receipts. No mint.`; `onchain` is inactive and marked locked pending later migration/legal review. The `cp8_moltbook_ledger_onchain_emit` routine raises `onchain_backend_disabled_no_mint`.

The token project's `node_network/README.md` says its runnable worker/validator MVP does not yet implement token issuance. Therefore this wallet designation must not be presented as proof that an HHC token contract has been deployed or that on-chain minting is active. Internal HHC credits/PoWP claims must be labeled separately from ERC-20 tokens and Base transactions.
