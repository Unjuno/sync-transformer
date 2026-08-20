# Same-budget comparison status

## Scope

The current reconstruction fixes the forecast head, seeds (163/164/165), chronological 60/20/20 split, query arrays, candidate stride, and gate threshold. K=1 is a single-neighbor/local-memory control; K=8 is the multi-candidate ordered-aggregation variant; raw future transport is a mechanism control that removes residual transport. These are controlled internal baselines, not exact RAFT or PFRP implementations.

## Fixed-gate query-level results

| Dataset | K=1 mean delta | K=8 mean delta | Interpretation |
|---|---:|---:|---|
| ETTh1 | +0.005931 | +0.001905 | K=8 reduces degradation, but does not beat Head |
| ETTh2 | 0.000000 | 0.000000 | Both configurations abstain completely |
| ETTm1 | +0.001207 | -0.010439 | Multi-candidate aggregation improves |
| ETTm2 | +0.007227 | -0.004928 | Multi-candidate aggregation improves |

Values are External minus Head MSE; negative is better. Each row pools 435 test queries across three seeds. Bootstrap intervals and gate-use rates are in `outputs/k_ablation_fixed_gate_summary.json`.

## Claim boundary

The table supports a conditional statement: ordered multi-candidate residual aggregation is useful on the two tested minute-scale datasets, while hourly conditions are neutral or negative under the frozen gate. It does not establish superiority over RAFT/PFRP. A publishable superiority claim still requires capacity-matched implementations of those methods, identical candidate budgets, and the same held-out protocol.
## Status clarification (2026-08-14)

The current raw-transport control uses the same causal candidate bank, query arrays, K, and seed budget as SYNC and therefore serves as a controlled nearest-future retrieval baseline. It is **RAFT-like only as an internal control**, not an exact RAFT reproduction: no multi-scale RAFT architecture, no published implementation, and no RAF/TSFM integration are used. The raw-vs-SYNC bootstrap is significant on ETTh1/ETTm1 and inconclusive on ETTm2. A true same-budget RAFT/RAF reproduction remains open and is required before any comparative novelty claim.
