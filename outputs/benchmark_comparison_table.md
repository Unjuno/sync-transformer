# Benchmark comparison: CPU baseline

This table adds a conventional TransformerEncoder baseline to the existing SYNC studies. Vanilla Transformer uses 30 causal patch means, `d_model=64`, 4 heads, 2 encoder layers, 10 epochs, seeds 163/164/165, and the same chronological 60/20/20 protocol. Its absolute MSE is normalized by the training-prefix standard deviation.

| Dataset | Seasonal naive MSE | Vanilla Transformer MSE | Vanilla Transformer (small) MSE | SYNC canonical result |
|---|---:|---:|---:|---|
| ETTh1 | 0.0691 | 0.202044 | 0.203762 | conditional; endpoint+seasonal delta over learned head -0.033155 |
| ETTh2 | 0.1590 | 0.573496 | 0.562090 | abstains in the canonical condition |
| ETTm1 | 0.0698 | 0.234096 | 0.217349 | conditional; endpoint+seasonal delta over learned head -0.009465 |
| ETTm2 | 0.1588 | 0.407707 | 0.395549 | conditional; endpoint+seasonal delta over learned head +0.013750 |

The standard Vanilla Transformer has 70,680 parameters on hourly datasets and 75,360 on minute datasets. The small model uses 10,424 and 12,800 parameters respectively and is trained for 20 epochs to match the SYNC head training budget. It is a capacity control, not a tuned state-of-the-art implementation. The SYNC deltas are from the canonical SYNC protocol and are reported as deltas rather than being mixed with the Vanilla absolute-MSE protocol.

Raw per-seed benchmark artifacts are in `outputs/vanilla_ETTh1.json`, `outputs/vanilla_ETTh2.json`, `outputs/vanilla_ETTm1.json`, `outputs/vanilla_ETTm2.json`, and the combined summary is `outputs/vanilla_transformer_benchmark.json`.

Capacity-control artifacts are `outputs/vanilla_small20_ETTh1.json`, `outputs/vanilla_small20_ETTh2.json`, `outputs/vanilla_small20_ETTm1.json`, `outputs/vanilla_small20_ETTm2.json`, and `outputs/vanilla_transformer_small20_benchmark.json`.
