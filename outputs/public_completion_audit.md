# Public benchmark completion audit

This audit is intentionally conservative: a task is marked measured only when
Vanilla Transformer and SYNC artifacts, per-seed query metrics, uncertainty,
and failure notes are present.

| Requirement | Evidence | Status |
|---|---|---|
| Ten-task manifest | `outputs/data_manifest.json` contains 10 task entries | met |
| Same-condition ETT comparison | `outputs/benchmark_runs/ett/` (4 datasets) | met |
| Same-condition Electricity comparison | `outputs/benchmark_runs/electricity/` (3 clients) | met |
| Same-condition HVAC comparison | `outputs/benchmark_runs/hvac/` (3 meters) | met |
| Same-condition traffic comparison | `outputs/benchmark_runs/traffic/` (2 sensors) | met |
| Forecasting/trajectory metric separation | `sync_experiments/trajectory_metrics.py` and forecasting summaries | met |
| Query-level uncertainty | Bootstrap CI fields in measured task summaries | met |
| Abstention/fallback reporting | `gate_use_rate` / trajectory fallback fields | met for measured forecasting tasks; trajectory tasks pending |
| Failure-case notes | `failure_notes` in measured summaries | met for measured tasks |
| CPU ETT regression | `work/validate_public_benchmark.py` and test suite | met |
| Raw data excluded from Git | `git ls-files data/raw` is empty | met |
| GPU artifacts isolated | `outputs/runtime_manifest.json` and CUDA overwrite guard | met |
| All ten tasks measured | Renewable, server, retail, industrial, and robot trajectory remain constrained; RoboMimic manipulation data/adapter are ready but ADE/FDE comparison is pending | not yet met |

Current measured scope is ETT, three electricity clients, three BDG2 meters,
and two METR-LA sensors. RoboMimic manipulation data and its adapter are now
ready, but the trajectory benchmark is not measured until Vanilla/SYNC,
ADE/FDE, fallback, and safety evaluation are run.
