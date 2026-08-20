# Task benchmark matrix

This is the public roadmap for evaluating SYNC against a Vanilla Transformer. It separates validated evidence from proposed applications.

| Task family | Dataset | Vanilla Transformer | SYNC | Evidence status |
|---|---|---:|---:|---|
| Electricity/traffic-like periodic forecasting | ETT hourly/minute datasets | measured | measured as conditional deltas | **Current CPU evidence** |
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

The current repository validates only the first row. The remaining rows are a falsifiable experiment roadmap, not claims of performance.
