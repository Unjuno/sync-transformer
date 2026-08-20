# Electricity MT_002 benchmark

This is the second UCI ElectricityLoadDiagrams client series, using the same
CPU protocol as the MT_001 report: context 720, horizon 96, query step 96,
three seeds (163/164/165), 20 epochs, and the documented small Vanilla
Transformer configuration.

| model | mean normalized MSE | gate use |
|---|---:|---:|
| Vanilla Transformer small | 0.301197 [0.295259, 0.307587] | n/a |
| SYNC base head | 0.236906 [0.230601, 0.243506] | n/a |
| SYNC deployed external residual | 0.237559 [0.231607, 0.244159] | 10.27% |
| seasonal persistence | 0.167883 [0.167883, 0.167883] | n/a |

The gate is no longer completely abstinent on this client (10.27% of test
queries), but the deployed residual is slightly worse than the SYNC base head
on average and both learned models are worse than seasonal persistence. This
is negative evidence against a general SYNC advantage, while demonstrating
that gate behavior is series-dependent. It does not justify aggregating MT_001
and MT_002 into a positive result.

The pooled query-level bootstrap uses 876 test queries and a fixed seed. The
external-minus-base delta is `+0.000653` (95% CI `[0.000163, 0.001154]`), so
the residual transport is detectably harmful under this protocol.

Artifacts: `vanilla_Electricity_MT002_20.json`,
`common_runner_Electricity_MT002_q96_c48_lbfull_k8_rich0_end_sf_vg0.079168.json`.
The reproducible CI command is `work/bootstrap_electricity.py`.
