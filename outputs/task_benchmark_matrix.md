# Task benchmark matrix

This is the public roadmap for evaluating SYNC against a Vanilla Transformer. It separates validated evidence from proposed applications.

| Task family | Dataset | Vanilla Transformer | SYNC | Evidence status |
|---|---|---:|---:|---|
| Electricity/traffic-like periodic forecasting | ETT hourly/minute datasets | measured | measured as conditional deltas | **Current CPU evidence** |
| Electricity demand | UCI ElectricityLoadDiagrams (`MT_001`, `MT_002`, `MT_003`) | measured | gate use 0%, 10.27%, 100%; transport outcomes differ by client | **Three single-series replications; no general advantage** |
| Building load | TBD | pending | pending | Candidate |
| Solar/wind power | TBD | pending | pending | Candidate |
| Road traffic | TBD | pending | pending | Candidate |
| HVAC | TBD | pending | pending | Candidate |
| Server workload | TBD | pending | pending | Candidate |
| Retail demand | TBD | pending | pending | Candidate |
| Industrial sensor | TBD | pending | pending | Candidate |
| Robot manipulation | RoboMimic/Open X subset | pending | pending | Candidate; requires control formulation |
| Mobile-robot trajectory | Simulator/log dataset | pending | pending | Candidate; requires control formulation |
| Fleet/mobility demand | TBD | pending | pending | Candidate |

The current repository has canonical ETT evidence plus three measured electricity client series. The remaining rows are a falsifiable experiment roadmap, not claims of performance.
