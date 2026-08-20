# SYNC Transformer: experiments

## Canonical protocol

- Public ETT datasets: ETTh1, ETTh2, ETTm1, ETTm2
- Seeds: 163, 164, 165
- Chronological train/calibration/test split
- Dataset-specific horizons: 24 for hourly data and 96 for minute data
- Normalized MSE and query-level paired comparisons
- Current primary representation: endpoint plus seasonal features, K=8, width=80

## Completed CPU experiments

- Canonical reconstruction and deterministic reruns
- Endpoint and seasonal feature ablations
- K and candidate-bank controls
- Raw retrieval versus fused residual transport
- Seasonal-naive baseline
- Distance/volatility gate sweeps
- Same-budget controls
- Rolling-origin windows across all four datasets
- Internal E2E/Ranked diagnostic reruns
- Conventional Vanilla Transformer benchmark (CPU, 3 seeds)
- Capacity-control Vanilla Transformer benchmark
- Bootstrap summaries and artifact audits

## Main empirical pattern

The effect is conditional. Some ETTm2 windows improve, ETTh1/ETTm1 can degrade, and ETTh2 often abstains completely. Rolling-origin windows can reverse the sign of the paired difference. These observations prevent a universal accuracy claim.

## Reproduction commands

```powershell
python -m pytest -q
python work/run_canonical_suite.py
python work/summarize_rolling_origin.py --pattern "common_runner_*_ev*.json"
python work/validate_reconstruction_artifacts.py
python work/audit_public_sync.py
```

The authoritative summary is `outputs/SYNC_Transformer_results_and_experiment_plan.md`. Individual JSON artifacts are condition-keyed; do not average incompatible protocols together.

The initial benchmark table is `outputs/benchmark_comparison_table.md`. It explicitly separates absolute Vanilla Transformer MSE from SYNC's canonical paired deltas because the two protocols use different model sizes and training budgets.

The task-level roadmap is `docs/TASKS.md`, and its public status matrix is `outputs/task_benchmark_matrix.md`. Candidate tasks are hypotheses until both Vanilla Transformer and SYNC have been evaluated on the same benchmark.

## Deferred CUDA experiment

RAFT and other external-baseline comparisons are intentionally deferred to a CUDA-capable machine. The CUDA experiment must clone this repository, reproduce the CPU baseline, preserve the fixed split/seed/horizon protocol, and add GPU artifacts in a separate commit.
