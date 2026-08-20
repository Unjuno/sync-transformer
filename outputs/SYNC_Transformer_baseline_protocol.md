# SYNC Transformer: controlled baseline protocol

This protocol is frozen before implementing any additional retrieval baseline.

## Fixed conditions

- Datasets: ETTh1, ETTh2, ETTm1, ETTm2.
- Chronological split: 60% train, 20% calibration, 20% test.
- Seeds: 163, 164, 165.
- Context/horizon: ETTh `P=24,H=24`; ETTm `P=96,H=96`.
- Candidate budget: the same causal candidate pool and `K=8` for every method.
- No candidate may use observations at or after the query origin.
- Gate thresholds are selected on calibration only and frozen for test.
- Report paired query-level MSE deltas and bootstrap confidence intervals.

## Methods to compare

1. Forecast head only.
2. Raw retrieved-future average (retrieval-only control; already available).
3. SYNC ordered future-residual transport with the frozen gate.
4. A same-budget patch-retrieval baseline using the same candidate pool and aggregation budget.

The raw retrieval control is not treated as a full RAFT/PFRP reproduction. Until method 4 is implemented and evaluated under this protocol, no superiority claim against RAFT or PFRP is permitted.

## Acceptance rule

The SYNC claim may be strengthened only if its paired bootstrap interval is below zero against method 4 on at least three datasets, with no remaining dataset showing a practically material degradation. Otherwise the result is reported as conditional or null.
