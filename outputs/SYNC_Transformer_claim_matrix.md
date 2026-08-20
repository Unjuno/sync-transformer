# SYNC Transformer claim matrix

| Claim | Status | Evidence |
|---|---|---|
| External residual transport improves ETTm1/ETTm2 under the primary frozen protocol | Rejected for the canonical deterministic rerun; both are non-improving (+0.001070 / +0.008027) | Canonical artifacts and `same_budget_control_summary.json` |
| Endpoint-preserving representation improves the learned head on some datasets | Supported conditionally: ETTh1 -0.025849 and ETTm1 -0.008600; ETTh2 abstains and ETTm2 +0.015014 | Endpoint-feature canonical artifacts |
| Explicit seasonal lags improve endpoint representation | Conditional support with query-bootstrap CIs: ETTh1 -0.033155 [-0.04198,-0.02457], ETTm1 -0.009465 [-0.01556,-0.00354]; ETTm2 +0.013750 [0.00641,0.02090], ETTh2 abstains | `_end_sf_` artifacts and `endpoint_feature_bootstrap.json` |
| The pooled gate improves every dataset | Rejected | ETTh1 split aggregate, Phase 245 |
| The method is universally better than raw retrieval | Rejected | Phase 242 (ETTm2) |
| Residual transport is relevant beyond retrieval alone | Supported only as a mechanism/safety hypothesis; it reduces raw-transport error on ETTh1/ETTm1 but does not beat the head | `same_budget_control_summary.json` |
| Residual transport/fusion is better than raw candidate transport | Supported conditionally: significant on ETTh1 and ETTm1, inconclusive on ETTm2 | `raw_vs_sync_bootstrap.json` |
| Internal E2E/Ranked currently beats External | Rejected | Phase 223/224 |
| Historical retrieval itself is novel | Not claimed | Literature audit |
| Exact initial SYNC_CORE table is reproduced | Not established | Artifact search / readiness audit |
| Prototype is reproducible from public data and condition-keyed artifacts | Supported; deterministic CPU rerun now verified | Tests, validator, public audit, canonical reruns |
| Gate improvement is split-robust on ETTh1/ETTm1 | Rejected | Phase 247/248 sign-reversal probe |
