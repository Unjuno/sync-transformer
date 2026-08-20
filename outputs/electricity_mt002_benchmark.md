# Electricity MT_002 benchmark

This is the second UCI ElectricityLoadDiagrams client series, using the same
CPU protocol as the MT_001 report: context 720, horizon 96, query step 96,
three seeds (163/164/165), 20 epochs, and the documented small Vanilla
Transformer configuration.

| model | mean normalized MSE | gate use |
|---|---:|---:|
| Vanilla Transformer small | 0.301197 | n/a |
| SYNC base head | 0.236906 | n/a |
| SYNC deployed external residual | 0.237559 | 10.27% |
| seasonal persistence | 0.167883 | n/a |

The gate is no longer completely abstinent on this client (10.27% of test
queries), but the deployed residual is slightly worse than the SYNC base head
on average and both learned models are worse than seasonal persistence. This
is negative evidence against a general SYNC advantage, while demonstrating
that gate behavior is series-dependent. It does not justify aggregating MT_001
and MT_002 into a positive result.

Artifacts: `vanilla_Electricity_MT002_20.json` and
`common_runner_Electricity_MT002_q96_c48_lbfull_k8_rich0_end_sf_vg0.079168.json`.
