# SYNC Transformer

**SYNC Transformer** is a causal episodic-residual forecasting prototype. It retrieves compatible historical episodes, preserves the temporal order of their future trajectories, and transports a residual signal into a learned forecasting head.

## What has been demonstrated

- On the primary public ETT reconstruction split, External residual transport improves the matched forecasting head on ETTm1 and ETTm2; an ETTm1 alternate split reverses the sign, so this is not yet a split-robust claim.
- The benefit depends on sampling frequency and regime: always-on retrieval degrades ETTh1 and ETTh2.
- Candidate aggregation (`K`) is data dependent; endpoint+seasonal K=8 is modestly better than K=1 on ETTh1/ETTm1, while ETTm2 remains negative and ETTh2 abstains.
- A low-dimensional volatility gate reduces negative transfer on ETTh1, but does not eliminate it.
- Query-level paired bootstrap gives a pooled four-dataset delta of -0.003365 (95% CI [-0.004625, -0.002141]); the ETTh1 interval crosses zero, while ETTm1 and ETTm2 intervals remain below zero.
- Same-query comparisons currently show External selection outperforming the implemented Internal E2E and Ranked variants.
- A raw-future retrieval control is strongly worse than the head on ETTm1 (+0.096050, bootstrap 95% CI [+0.080476,+0.112230]), while SYNC residual transport improves it; this separates the prototype from retrieval-only behavior.
- Across three ETTh1 chronological splits and three seeds, the pooled gate delta is +0.003811 with a wide seed-level range [-0.001564,+0.012845]; ETTh1 is therefore treated as a stress condition rather than a stable gain condition.

## Honest scope

This is a reproducible prototype and research direction, not a claim of universal forecasting improvement or a complete reproduction of the initially supplied SYNC_CORE table. Historical retrieval itself is not claimed as novel. The research hypothesis is the combination of causal provenance constraints, ordered future residual transport, regime-conditioned use, and explicit negative-transfer reporting.

## Current status

The core artifacts, ablations, paired query-level results, and validation scripts are in `outputs/` and `work/`. The next research milestone is a cross-fitted regime gate that remains conservative under dataset shift.
