# SYNC Transformer

Reproducible research implementation of **SYNC Transformer**, a causal episodic-residual forecasting framework combining historical episode retrieval, ordered residual transport, conditional fusion, and explicit abstention.

> **Research status:** CPU experiments and reproducibility audits are complete. GPU experiments, including CUDA-based external-baseline comparisons, are planned for a separate machine and are not included in the current claims.

## What this repository contains

- A transparent common-protocol reconstruction of the SYNC mechanism.
- Deterministic experiments on the public ETT datasets (ETTh1, ETTh2, ETTm1, ETTm2).
- Feature, candidate-count, gate, retrieval-control, and rolling-origin studies.
- Query-level result artifacts, bootstrap summaries, reproducibility manifests, and research notes.
- A documented GPU/CUDA extension plan for later RAFT and external-baseline comparisons.

The original SYNC_CORE implementation was not recovered. Therefore, this repository does **not** claim exact reproduction of the earliest Phase 4A–4B table. Historical Phase 4A–4B results are retained as separate, explicitly labeled evidence.

## Current evidence

The primary public-data reconstruction shows positive transfer on ETTm1/ETTm2 and negative transfer on ETTh1/ETTh2. An alternate ETTm1 split reverses the sign, so all gains are treated as conditional rather than split-robust. Candidate aggregation and regime gating are therefore not universal components. The implemented Internal E2E/Ranked variants do not yet outperform the External pathway in same-query tests.

ETTh1 is especially split-sensitive: the fixed gate produced -0.001330, +0.001905, and +0.010858 on 50/25/25, 60/20/20, and 40/20/40 chronological splits (pooled seed mean +0.003811). It is treated as a stress condition, not a stable gain condition.

With the calibration-frozen pooled volatility gate, the four-dataset paired query bootstrap is -0.003365 (95% CI [-0.004625, -0.002141]); ETTh1 alone remains statistically inconclusive.

The supported interpretation is:

> SYNC is a conditional residual-transport and abstention mechanism, not a universally superior forecasting model.

Internal-search results remain protocol-sensitive. The repository records both the initial Phase 4A–4B report and later reconstruction diagnostics rather than selecting one outcome without reconciliation.

## What can SYNC be used for?

SYNC is intended for recurring or seasonal processes where comparable past episodes exist and a fallback is available. Plausible application families include electricity load, renewable power, traffic, HVAC, server workload, retail demand, industrial sensors, and repetitive robot trajectories. The public ETT suite and a first single-series UCI electricity benchmark are measured; the remaining applications are hypotheses and are listed in [the task map](docs/TASKS.md). The electricity result is limited by 100% gate abstention (see [the report](outputs/electricity_benchmark.md)).

Each new application must be compared with a Vanilla Transformer under the same data split, horizon, seeds, parameter budget, and compute budget. The public roadmap is [the task benchmark matrix](outputs/task_benchmark_matrix.md). No candidate task should be described as validated until its benchmark row has been filled.

The common task registry and Phase-A orchestrator are available as `sync_experiments`. The current `--tasks all` command executes the validated ETT CPU suite, records measured electricity artifacts when present, and reports the remaining eight tasks as `pending_adapter`; it does not fabricate results for datasets that have not been downloaded and licensed.

```powershell
python -m sync_experiments.run_all --tasks all --track all --seeds 163,164,165 --epochs 20 --device cpu
```

## Reproducibility

```powershell
python -m pytest -q
python work/run_canonical_suite.py
python work/summarize_rolling_origin.py --pattern "common_runner_*_ev*.json"
python work/validate_reconstruction_artifacts.py
python work/audit_public_sync.py
```

See `outputs/SYNC_Transformer_results_and_experiment_plan.md` for the protocol and interpretation.

## Research structure

- [Theory and scope](docs/THEORY.md): definitions, hypotheses, and non-claims.
- [Experiments](docs/EXPERIMENTS.md): fixed protocol, completed CPU studies, and reproduction commands.
- [Benchmark table](outputs/benchmark_comparison_table.md): conventional Transformer versus the existing baselines.
- [Limitations](docs/LIMITATIONS.md): missing implementation, statistical limits, baseline limits, and CUDA handoff.

## GPU/CUDA extension

GPU experiments are intentionally deferred. On a separate CUDA-capable machine:

1. Clone this repository.
2. Install the CUDA/PyTorch environment and external baseline dependencies.
3. Re-run the fixed CPU baseline first.
4. Run RAFT under the same dataset, horizon, split, seed, and metric protocol.
5. Commit and push GPU artifacts separately, without overwriting the CPU baseline.

See `outputs/SYNC_Transformer_GPU_extension_plan.md` for the handoff.

## License

Apache License 2.0. See [LICENSE](LICENSE).
