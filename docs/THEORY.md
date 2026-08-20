# SYNC Transformer: theory and scope

## Status of the theory

This document defines the proposed mechanism. It is not a proof that the mechanism is universally optimal. The current repository supports a conditional mechanism hypothesis, not a universal forecasting theorem.

## Definition

Given a causal history (x_{t-P:t}), a forecasting head produces a base forecast (\hat y^{base}_{t:t+H}). A causal candidate bank contains historical episodes whose future is available before the current query. A retrieval function selects compatible candidates using only information available at query time.

SYNC transports the ordered future residual of the selected episode into the current forecast:

```text
candidate residual = future(candidate) - base(candidate)
SYNC forecast = base(current) + alpha * fused(candidate residuals)
```

The transport preserves the candidate's temporal offset. Reversing the future trajectory is an intervention that tests whether ordering, rather than merely candidate content, matters.

An abstention gate may return the base forecast instead of applying transport when the candidate distance or regime signal indicates insufficient support.

## Falsifiable hypotheses

1. Ordered residual transport can improve a base forecast on some regimes.
2. Candidate retrieval alone is not sufficient; fusion and residual transport determine the effect.
3. Explicit abstention can limit negative transfer, but cannot guarantee universal improvement.
4. External/lightweight retrieval can be computationally preferable to evaluating every candidate through a neural selector.

## What is not claimed

- SYNC is not claimed to dominate seasonal-naive or learned baselines on every dataset.
- Retrieval-augmented forecasting as a broad idea is not claimed as novel.
- The earliest missing SYNC_CORE implementation is not claimed to be exactly reproduced.
- The initial Phase 4A–4B internal-search result is retained as historical evidence, not silently promoted to the current canonical result.

## Candidate interpretation

The current safe interpretation is: **SYNC is a conditional residual-transport and abstention mechanism whose utility depends on temporal regime, representation, gate calibration, and candidate quality.**
