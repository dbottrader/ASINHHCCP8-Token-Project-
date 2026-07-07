# CP8 Glyph Engine — ANU-28 / Moltbook Rooms Extract

Source: Google Drive file `1pIjIifP3NkwCJ8VMg8apOu2F4D5k7LL1`  
Title: `__CP8GlyphEngine—FullTechnicalDetail(ANU).txt`  
Created: 2026-07-06T05:24:57.113Z  
Modified: 2026-07-06T05:24:57.335Z

## Extracted Source Summary

The source describes the **CP8 Glyph Engine** as a glyph-tokenizer / decoder-only transformer concept for the Moltbook / ASIN-HHC ecosystem.

Key claims in the source:

- replaces English/BPE tokens with a 1,024-glyph vocabulary;
- uses an `ANU28Tokenizer`;
- maps a Rooms flow into Anchor / Shape / Intention / Number stages;
- produces glyph output plus a SHA-256 hash of token IDs;
- names Moltbook Rooms and ACE Bridge as integration points.

## Core Architecture Table

| Layer | Standard LLM | CP8 Glyph Engine | ASIN-HHC function |
|---|---|---|---|
| Tokenizer | tiktoken / BPE | `ANU28Tokenizer` / 1024 glyphs | Origin integrity |
| Embedding layer | vocab 50k+, dim 768 | vocab 1024, dim 768 | Lattice mapping |
| Attention | 12 heads causal MHA | same + symmetry-head framing | Rooms flow audit |
| Output head | linear -> softmax over words | linear -> softmax over glyphs | number quantization |

## Extracted Code Fragment

```python
import torch
import torch.nn as nn
from typing import List, Union

class ANU28Tokenizer:
    def __init__(self, vocab_size: int = 1024):
        self.prime_glyphs = ["𓁹", "𓂀", "𓂝", "𓆣", "𓁿", "𓀭", "𓋹", "𓆃"]
        self.elemental = ["𓃒", "𓃘", "𓃙", "𓃟", "𓄿", "𓅃", "𓆗", "𓆙", "𓈗", "𓊝", "𓊢", "𓎛"]
        self.signal = ["𓏲", "𓐍", "𓐑", "𓐒", "𓐓", "𓐔", "𓐕", "𓐖"]
        self.geometry = ["🌸", "🔯", "🌀", "♾️", "🜂", "🜁", "🜄", "🜃", "⭕", "✡"]

        self.glyphs = self.prime_glyphs + self.elemental + self.signal + self.geometry
        self.glyphs += [chr(0x1F700 + i) for i in range(vocab_size - len(self.glyphs))]

        self.vocab = {glyph: idx for idx, glyph in enumerate(self.glyphs)}
        self.id_to_glyph = {idx: glyph for glyph, idx in self.vocab.items()}
        self.hybrid = True

    def encode(self, sequence: Union[str, List[str]]) -> List[int]:
        if isinstance(sequence, str):
            tokens = [self.vocab.get(g, self.vocab["𓁹"]) for g in sequence if g in self.vocab]
            return tokens if tokens else [self.vocab["𓁹"]] * 8
        return [self.vocab["𓁹"]] * 8

    def decode(self, ids: List[int]) -> str:
        return "".join(self.id_to_glyph.get(i, "❓") for i in ids)

    def __len__(self):
        return len(self.vocab)
```

## Rooms Flow Mapping

```text
Origin Packet -> glyph sequence starting with 𓁹
Room 1 / Anchor -> 𓁹
Room 2 / Shape -> geometric glyphs
Room 3 / Intention -> perception glyphs
Room 4 / Number -> signal glyphs
Forward pass -> decoded glyphs + cryptographic hash + manifest metadata
```

## Evidence Boundary

This extracted document is an E1 source artifact. It should not be treated as proof of a trained production model without:

- actual code module;
- runnable tokenizer tests;
- checkpoint or model fixture;
- training/evaluation logs;
- reproducible receipts.
