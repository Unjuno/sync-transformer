# Task benchmark matrix

This is the public roadmap for evaluating SYNC against a Vanilla Transformer. It separates validated evidence from proposed applications.

| Task family | Dataset | Vanilla Transformer | SYNC | Evidence status |
|---|---|---:|---:|---|
| Electricity/traffic-like periodic forecasting | ETT hourly/minute datasets | measured | measured as conditional deltas | **Current CPU evidence** |
| Electricity demand | UCI ElectricityLoadDiagrams (`MT_001`, `MT_002`, `MT_003`) | measured | gate use 0%, 10.27%, 100%; transport outcomes differ by client | **Three single-series replications; no general advantage** |
| Building load | TBD | pending | pending | Candidate |
| Solar/wind power | TBD | pending | pending | Candidate |
| Road traffic | METR-LA (2 sensors) | measured | measured | Sensor-dependent; spatial multivariate effects not evaluated |
| HVAC | BDG2 (three meters) | measured | measured | Series-dependent; no building-wide claim |
| Server workload | TBD | pending | pending | Candidate |
| Retail demand | TBD | pending | pending | Candidate |
| Industrial sensor | TBD | pending | pending | Candidate |
| Robot manipulation | RoboMimic/Open X subset | pending | pending | Candidate; requires control formulation |
| Mobile-robot trajectory | Simulator/log dataset | pending | pending | Candidate; requires control formulation |
| Fleet/mobility demand | TBD | pending | pending | Candidate |

The current repository has canonical ETT evidence, three measured electricity client series, two measured METR-LA sensors, and three measured BDG2 HVAC meters. The remaining rows are a falsifiable experiment roadmap, not claims of performance.
