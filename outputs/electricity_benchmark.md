# Electricity benchmark: first real non-ETT task

## Protocol

- Source: UCI ElectricityLoadDiagrams20112014, CC BY 4.0
- Series: `MT_001` only, selected before evaluation
- Resolution: 15 minutes
- Context: 720 steps
- Horizon: 96 steps (24 hours)
- Split: chronological 60/20/20
- Seeds: 163/164/165
- Vanilla: Transformer small, d_model=32, one layer, 20 epochs
- SYNC: endpoint+seasonal features, K=8, width=80, 20 epochs
- Metric: normalized test MSE

## Results

| Model | Mean normalized MSE | Notes |
|---|---:|---|
| Seasonal-naive (last observed value) | 1.063638 | 24-hour horizon baseline |
| Vanilla Transformer small | 1.097691 | 12,800 parameters |
| SYNC output | 0.795544 | 19,296 parameters; gate use rate 0% |
| Raw transport control | 0.728223 | Ungated diagnostic, not the deployed SYNC output |

The SYNC output is better than the small Vanilla Transformer in this first run, but the calibrated gate abstained on every test query. Therefore the result does **not** demonstrate successful residual transport on this task; it demonstrates that the learned base head was stronger than the selected transport under the current gate and protocol. The raw transport control is not a valid deployed comparison because it bypasses the calibrated gate.

Artifacts:

- `outputs/common_runner_Electricity_q96_c48_lbfull_k8_rich0_end_sf_vg0.079168.json`
- `outputs/vanilla_Electricity20.json`
- `work/prepare_electricity.py`

This is the first measured non-ETT task. It is not sufficient to validate all electricity-load settings or all clients.
