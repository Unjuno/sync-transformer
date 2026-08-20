# Electricity MT_003 benchmark

MT_003 uses the same protocol as MT_001 and MT_002: context 720, horizon 96,
query step 96, chronological 60/20/20 split, seeds 163/164/165, and 20
epochs.

| model | mean normalized MSE | 95% query bootstrap CI |
|---|---:|---:|
| Vanilla Transformer small | 0.011009 | [0.010941, 0.011081] |
| SYNC base head | 0.013187 | [0.012956, 0.013444] |
| SYNC deployed external residual | 0.003625 | [0.003573, 0.003686] |
| Seasonal persistence diagnostic | 0.000690 | fixed diagnostic |

The gate used the transport on 100% of test queries. Unlike MT_002, the
deployed residual substantially improved over the SYNC base head
(`-0.009562`, 95% CI `[-0.009767, -0.009347]`) and over the Vanilla baseline,
but it remained worse than seasonal persistence. This is positive evidence for
conditional transport on one client, not evidence of a general electricity
advantage.

Artifacts: `vanilla_Electricity_MT003_20.json`,
`common_runner_Electricity_MT003_q96_c48_lbfull_k8_rich0_end_sf_vg0.079168.json`,
and `electricity_mt003_bootstrap.json`.
