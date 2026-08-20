# SYNC Transformer experiment index

## Core comparison

- `phase215_primary_artifacts.md`: four-dataset External vs head matrix.
- `phase223_direct_external_internal_bootstrap.md`: same-query External vs Internal E2E.
- `phase224_ranked_direct_comparison.md`: same-query External vs Internal Ranked.

## Candidate and aggregation studies

- `phase229_ettm1_k_sweep.md`: ETTm1 benefits from larger K.
- `phase230_cross_dataset_k_sweep.md`: K effect reverses across datasets.
- `phase231_calibration_selected_k.md`: calibration-selected K is not sufficient under shift.

## Safety and selection studies

- `phase233_regime_volatility_gate.md`: volatility gate reduces ETTh1 negative transfer.
- `phase234_combined_regime_distance_gate.md`: adding distance increases selection overfit.
- `phase235_crossfit_regime_gate.md`: cross-fitting improves validity but loses ETTm1 benefit.
- `phase236_pooled_regime_gate.md`: one calibration-frozen threshold across datasets.
- `phase237_pooled_gate_four_dataset_check.md`: ETTh2 fallback and ETTm2 transfer check.
- `phase239_pooled_gate_bootstrap.md`: paired bootstrap intervals for the final gate.
- `phase243_alternate_split_robustness.md`: ETTh1 alternate chronological split.
- `phase246_ettm1_alternate_split.md`: ETTm1 alternate split reverses the primary effect.
- `phase247_split_probe_automated.md`: automated three-split probe for ETTh1/ETTm1.
- `phase247_split_probe_summary.json`: machine-readable output from the automated probe.
- `phase248_split_level_aggregate.md`: conservative split-level aggregation.
- `phase204_reranker_diagnostic.md`: simple learned reranker is not transferable.
- `phase240_raw_retrieval_baseline.md`: raw future retrieval control isolates the residual-transport contribution.
- `SYNC_Transformer_baseline_protocol.md`: frozen same-budget comparison protocol for future patch-retrieval baselines.
- `SYNC_Transformer_same_budget_comparison.md`: controlled K=1/K=8/raw controls and explicit RAFT/PFRP claim boundary.

## Reproducibility and publication

- `SYNC_Transformer_short_draft.md`: paper-style summary and novelty boundary.
- `SYNC_Transformer_public_profile.md`: concise public description.
- `phase214_reproducibility_ledger.md`: protocol ledger.
- `phase218_artifact_validator.md`: artifact validation contract.
- `SYNC_Transformer_results_table.md`: final publication-ready result table.
