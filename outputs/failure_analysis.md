# Benchmark failure analysis

This file separates observed model failures from data/acquisition blockers.
Pending tasks have no performance result.

| task | status | observed failure or blocker |
|---|---|---|
| ETT | measured | Transfer sign is dataset/split dependent; ETTh1 is a stress condition. |
| Electricity MT_001 | measured | Gate abstained on 100% of test queries; no deployed transport was used. |
| Electricity MT_002 | measured | Gate used 10.27%; deployed residual worsened base head (bootstrap delta +0.000653). |
| Electricity MT_003 | measured | Gate used 100% and improved base head, but seasonal persistence remained stronger. |
| Renewable | source_public_license_unresolved | IEEE source is public but its license field is N/A; no benchmark is run before terms are clarified. |
| Traffic | pending_adapter | Dataset source/license and adapter not completed. |
| HVAC | pending_adapter | Dataset source/license and adapter not completed. |
| Server | pending_adapter | Dataset source/license and adapter not completed. |
| Retail | pending_adapter | Dataset source/license and adapter not completed. |
| Industrial | blocked_source_unavailable | NASA C-MAPSS is unavailable in the official catalog and has no specified license; no unproven mirror is used. |
| Robot manipulation | pending_adapter | Dataset acquisition and trajectory/action formulation not completed. |
| Robot trajectory | pending_adapter | Dataset acquisition and pose-trajectory formulation not completed. |

The measured failures are not converted into aggregate “wins.” In particular,
the MT_003 improvement is conditional and does not validate the electricity
task family generally.
