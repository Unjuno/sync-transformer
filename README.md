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

The expanded public benchmark covers ten task classes using the named
alternative datasets in [`outputs/data_manifest.json`](outputs/data_manifest.json).
Results are conditional: SYNC is favorable on several HVAC, renewable,
server, and industrial series, while the retail and pedestrian alternatives
favor Vanilla or Persistence. These are dataset/formulation results, not
claims of domain-wide superiority.

Internal-search results remain protocol-sensitive. The repository records both the initial Phase 4A–4B report and later reconstruction diagnostics rather than selecting one outcome without reconciliation.

## What can SYNC be used for?

SYNC is intended for recurring or seasonal processes where comparable past episodes exist and a fallback is available. The public benchmark includes ETT, three UCI electricity clients, two METR-LA sensors, three BDG2 HVAC meters, OPSD solar, Microsoft Cloud Monitoring server and purchase-rate alternatives, UCI AI4I industrial sensors, and two open-loop trajectory alternatives. Electricity, traffic, HVAC, retail, and trajectory results remain series/formulation-dependent; see the [task map](docs/TASKS.md) and [benchmark matrix](outputs/benchmark_matrix.csv).

The measured-task matrix is in [`outputs/benchmark_matrix.csv`](outputs/benchmark_matrix.csv); the conservative requirement-by-requirement audit is in [`outputs/public_completion_audit.md`](outputs/public_completion_audit.md).

Each new application must be compared with a Vanilla Transformer under the same data split, horizon, seeds, parameter budget, and compute budget. The public roadmap is [the task benchmark matrix](outputs/task_benchmark_matrix.md). No candidate task should be described as validated until its benchmark row has been filled.

The common task registry and orchestrator are available as `sync_experiments`. Raw data is never required to be committed: fetch scripts and the data manifest record source, license, version, and hash. Generated benchmark artifacts can be regenerated locally with the task-specific scripts in `work/`.

Trajectory tasks use a separate contract from forecasting: `TrajectoryBatch`
and `TrajectoryMetrics` report ADE, FDE, tracking error, open-loop endpoint
success, fallback, safety violations, and latency. Open-loop success is not a
closed-loop robot-control guarantee.

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
python work/validate_public_benchmark.py
```

See `outputs/SYNC_Transformer_results_and_experiment_plan.md` for the protocol and interpretation. The metric completeness audit is [`outputs/metric_completeness_audit.json`](outputs/metric_completeness_audit.json).

## Public-release boundaries

- This repository licenses its original code and documentation under Apache-2.0.
- Datasets remain under their own licenses; raw files and downloaded archives are excluded.
- Alternative datasets are named explicitly in the manifest and are not relicensed by this repository.
- The theory documents hypotheses and non-claims; benchmark results do not establish universal superiority or closed-loop safety.

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
