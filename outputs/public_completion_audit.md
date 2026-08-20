# Public benchmark completion audit

This audit distinguishes measured dataset/formulation evidence from broad
domain claims. Raw data is not committed.

| Requirement | Evidence | Status |
|---|---|---|
| Ten-task manifest | `outputs/data_manifest.json` | met |
| Vanilla/SYNC forecasting comparisons | ETT, electricity, HVAC, traffic, renewable, server, retail, industrial artifacts | met |
| Vanilla/SYNC trajectory artifacts | `outputs/benchmark_runs/robot_manipulation/*` and `robot_trajectory/*` | met; open-loop formulation |
| Forecasting metrics | MSE, MAE, query bootstrap CI, gate/fallback, latency | met; see `metric_completeness_audit.json` |
| Trajectory metrics | ADE, FDE, tracking error, open-loop success, fallback, safety, latency | met; no closed-loop claim |
| Failure notes | `failure_notes` in every summary | met |
| ETT CPU regression | `work/validate_public_benchmark.py`, `pytest -q` | met |
| Raw data exclusion | `git ls-files data/raw` is empty | met |
| GPU isolation | runtime manifest and CUDA overwrite guard | met |

## Interpretation boundary

SYNC is supported as a conditional residual-transport and abstention mechanism.
It is not supported as a universally superior forecaster, a general-purpose
robot controller, or a closed-loop safety guarantee. Retail and pedestrian
trajectory alternatives are explicit negative/limiting cases.

The measured alternatives are not relicensed by this repository. Users must
accept each upstream dataset's terms independently.
