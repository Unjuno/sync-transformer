# SYNC Transformer paper handoff

## Recommended contribution statement

SYNC Transformer is a causal, auditable episodic-residual transport protocol. It retrieves only temporally eligible historical episodes, transports residual information rather than raw futures, and falls back to the base forecast when calibration signals indicate risk. Endpoint and seasonal-lag features recover information lost by patch averaging.

## Strongest current evidence

- Endpoint+seasonal features versus the learned head, primary split: ETTh1 ΔMSE `-0.033155` (95% query-bootstrap CI `[-0.04198,-0.02457]`), ETTm1 `-0.009465` (CI `[-0.01556,-0.00354]`); ETTh2 abstains; ETTm2 worsens by `+0.013750` (CI `[+0.00641,+0.02090]`).
- Same candidate bank: residual transport versus raw transport is significant on ETTh1 (`-0.060598`, CI `[-0.07700,-0.04485]`) and ETTm1 (`-0.064815`, CI `[-0.08067,-0.04944]`), inconclusive on ETTm2.
- K=8 is modestly better than K=1 on ETTh1/ETTm1 under endpoint+seasonal features.

## Required caveats

- Gains reverse on the 70/15/15 late-origin split.
- Seasonal-naive beats all current SYNC configurations on the canonical ETT tasks.
- Multi-scale retrieval does not improve the endpoint+seasonal configuration.
- Official RAFT/RAF controlled ports are not complete; the current raw transport is only an internal retrieval control.
- The initial SYNC_CORE table is not exactly reproduced.

## Reproduction and audit

Primary scripts: `work/sync_core_runner.py`, `work/run_canonical_suite.py`, `work/bootstrap_endpoint_features.py`, `work/bootstrap_raw_vs_sync.py`, `work/validate_reconstruction_artifacts.py`, `work/audit_public_sync.py`.

Current verification: 44 pytest tests passed; artifact validator passed with 62 files/180 rows; public audit passed. Use deterministic CPU execution and `_end_sf_` artifacts for the endpoint+seasonal claims. Do not cite historical nondeterministic artifacts as headline results.

## Novelty boundary

Do not claim first retrieval-augmented forecasting or universal accuracy. The defensible novelty hypothesis is the combination of causal eligibility, residual transport, explicit abstention/fallback, and query-level auditability; it requires direct RAFT/RAF comparison before being presented as comparative novelty.
