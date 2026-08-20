# SYNC Transformer: task map

## How to read this list

SYNC is not presented as a general-purpose model for all forecasting or control problems. It is most plausible when the target contains repeated temporal motifs, comparable past episodes, and a safe fallback forecast or controller. The tasks below are candidate applications, not completed benchmark claims.

Every new task must compare SYNC against a Vanilla Transformer under the same split, horizon, seed, parameter budget, and compute budget. A task is only considered supported after improvement, uncertainty, abstention/fallback behavior, and failure cases are reported.

## Ten candidate tasks

| # | Task | Why SYNC may fit | Primary target | Candidate benchmark | Current status |
|---:|---|---|---|---|---|
| 1 | Building electricity-load forecasting | Daily/weekly cycles and recurring occupancy patterns | Load at 15–60 min horizon | UCI ElectricityLoadDiagrams, ASHRAE, or Pecan Street | Three UCI client series measured; client-dependent and not generalised |
| 2 | Renewable-power forecasting | Day/night and weather-regime recurrence | Solar/wind power | GEFCom or public solar/wind series | Candidate; not tested |
| 3 | Road-traffic forecasting | Rush-hour and weekday motifs | Flow/speed/occupancy | METR-LA, PEMS-BAY | Candidate; not tested |
| 4 | HVAC/control-demand forecasting | Occupancy and thermal cycles | Zone temperature/load | Building Data Genome 2 | Three BDG2 meters measured; series-dependent |
| 5 | Server/workload forecasting | Daily and weekly request patterns | Requests/CPU/latency | Alibaba cluster or public workload traces | Candidate; not tested |
| 6 | Retail/inventory demand forecasting | Calendar, promotion, and replenishment recurrence | SKU demand | M5 or Favorita | Candidate; not tested |
| 7 | Industrial sensor forecasting | Repeated operating cycles and fault precursors | Sensor trajectory/residual | NASA C-MAPSS or industrial telemetry | Candidate; not tested |
| 8 | Repetitive robot manipulation | Similar successful demonstrations can supply residual corrections | End-effector/action trajectory | RoboMimic or Open X-Embodiment subset | Candidate; not tested |
| 9 | Mobile-robot trajectory tracking | Repeated routes and recoverable local deviations | Pose/velocity/action | KITTI/nuScenes trajectory subsets or simulator logs | Candidate; not tested |
| 10 | Fleet/vehicle energy or demand forecasting | Route, shift, and daily recurrence | Energy/flow/arrival demand | Public fleet or mobility traces | Candidate; not tested |

## Priority order

The first non-ETT benchmark should be electricity load or traffic because they preserve the current forecasting formulation and have strong seasonal/recurrent structure. Robotics is a promising second-stage application, but it requires a control/action formulation, safety constraints, and a simulator or real-robot dataset; current ETT evidence does not establish robotics performance.

## Standard benchmark row

For each task, the repository should add one row with:

```text
dataset | horizon | split | seeds | Vanilla Transformer MSE | SYNC MSE/delta
bootstrap CI | improvement fraction | abstention/fallback rate | latency | failure analysis
```

Until a row is filled by an actual experiment, the task remains a hypothesis and must not be described as a validated use case.
