# SYNC Transformer canonical result table

All values below use deterministic CPU execution, three seeds (163/164/165), causal candidate banks, and query-level MSE deltas relative to the stated base. Negative is better.

| Condition | ETTh1 | ETTh2 | ETTm1 | ETTm2 |
|---|---:|---:|---:|---:|
| Original mean-patch + fixed gate | +0.008479 | 0.000000 (abstain) | +0.001070 | +0.008027 |
| Endpoint + seasonal-lag features | **-0.033155** | 0.000000 (abstain) | **-0.009465** | +0.013750 |
| Endpoint+seasonal, 50/25/25 split | -0.030759 | — | -0.018494 | — |
| Endpoint+seasonal, 70/15/15 split | +0.031582 | — | +0.008979 | — |
| Endpoint+seasonal, K=1 | -0.030688 | — | -0.005328 | +0.016084 |
| Endpoint+seasonal, K=8 | **-0.033155** | — | **-0.009465** | +0.013750 |
| Seasonal-naive baseline (absolute MSE) | 0.0691 | 0.1590 | 0.0698 | 0.1588 |

Interpretation: endpoint/seasonal features produce statistically clear but split- and frequency-dependent gains over the weak learned head. They do not beat the seasonal-naive baseline, and the residual mechanism is disabled when the strong seasonal base is supplied. The defensible contribution is therefore causal, auditable transport with safe fallback, plus a conditional representation ablation—not universal forecasting superiority.

Historical nondeterministic values are excluded from this table.
