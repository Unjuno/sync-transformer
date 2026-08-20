# SYNC Transformer novelty audit (2026)

## Overlap

Recent retrieval-augmented forecasting papers already establish the broad idea of retrieving historical patterns and using their future values: RAFT directly retrieves similar training patterns and supplies their futures to the forecaster; RAF develops retrieval and integration strategies for time-series foundation models. Therefore “retrieval-augmented time-series forecasting” alone is not a novel claim.

## Potential differentiator

The potentially distinct combination in SYNC is narrower: causal candidate eligibility, residual (rather than raw-future) transport, explicit abstention/fallback, and query-level auditability. The current experiments support residual transport over raw transport on ETTh1/ETTm1, but only conditionally; they do not establish superiority to RAFT/RAF or other learned retrieval mixers.

## Required novelty evidence

1. Implement a true same-budget RAFT-like baseline and report paired query-level comparisons.
2. Compare against RAF/other retrieval mixers where code or an exact protocol is available.
3. Isolate the residual transport, causal eligibility, and fallback components with matched ablations.
4. Evaluate held-out frequency/dataset and rolling origins.

## Official implementation check

The official [RAFT repository](https://github.com/archon159/RAFT) is now vendored at `work/vendor/RAFT`. It requires Python 3.9.13, NumPy 1.24.3, and PyTorch 1.10.0, and uses a larger Time-Series-Library training stack with multivariate inputs and its own data layout. The current environment is Python 3.12/PyTorch 2.x and the project uses univariate canonical CSVs, so an exact run was not silently substituted. The repository is retained for a future controlled port; until that port is completed, the internal raw-transport baseline remains the only directly comparable control.

## Safe wording

“We study a causal residual-transport and abstention protocol for retrieval-augmented forecasting.” Avoid “first retrieval-augmented forecaster,” “novel retrieval,” or universal accuracy claims until the comparisons above are complete.
