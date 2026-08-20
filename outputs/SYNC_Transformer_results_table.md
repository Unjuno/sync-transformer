# SYNC Transformer: final pooled-gate result table

固定閾値 `volatility <= 0.079168`、K=8、3 seeds、query-level paired differences。MSE差は `gated - head`（負が改善）。

| Dataset | Mean delta | 95% bootstrap CI | External use rate | Interpretation |
|---|---:|---:|---:|---|
| ETTh1 | +0.001905 | [-0.000403, +0.004244] | 0.628 | no significant gain |
| ETTh2 | 0.000000 | [0.000000, 0.000000] | 0.000 | complete fallback |
| ETTm1 | -0.010439 | [-0.012956, -0.007974] | 1.000 | significant gain |
| ETTm2 | -0.004928 | [-0.008420, -0.001404] | 1.000 | significant gain |
| Pooled | -0.003365 | [-0.004625, -0.002141] | — | conditional pooled gain |

この表は「全データセットで勝つ」主張ではなく、regime gateが改善可能なデータでExternalを使い、改善が確認できないETTh2ではheadへ戻ることを示す。
