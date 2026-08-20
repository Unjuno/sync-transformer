# SYNC Transformer reproducibility bundle

## Core implementation

- `work/sync_architecture.py`: causal memory, index, validation, ordered transport, hierarchical selector, safety gate
- `work/phase163_hybrid_internal.py`: Hybrid/Hierarchical residual prototype
- `work/test_sync_architecture.py`: contract tests

## Data

- `outputs/ETTh1.csv`
- `outputs/ETTh2.csv`
- `outputs/ETTm1.csv`
- `outputs/ETTm2.csv`
- Dataset details: `outputs/public_dataset_manifest.md`

## Key reports

- `outputs/phase180_matched_capacity_seeds.md`
- `outputs/phase181_capacity_matched_bootstrap.md`
- `outputs/phase184_hierarchical_3seed.md`
- `outputs/phase185_hierarchical_bootstrap.md`
- `outputs/SYNC_Transformer_short_draft.md`
- `outputs/SYNC_Transformer_research_brief.md`
- `outputs/phase201_four_dataset_matrix.md`
- `outputs/phase212_current_comparison_table.md`
- `outputs/phase215_primary_artifacts.md`

## Verification commands

```text
python -m pytest -q work/test_sync_architecture.py
python -m compileall -q work
python work/audit_public_sync.py
python work/sync_core_runner.py --dataset ETTm1 --seeds 163,164,165 --step 96 --candidate-step 48 --width 80 --epochs 100
python work/sync_core_runner.py --dataset ETTm2 --seeds 163,164,165 --step 96 --candidate-step 48 --width 80 --epochs 100
```

Expected current results: `5 passed`, compile success, and audit `passed: true`.

## Scope note

This bundle contains a capacity-matched episodic-residual prototype. It does not claim exact reproduction of the originally supplied full SYNC_CORE implementation.

The condition-keyed JSON artifacts prevent later experiments from overwriting primary results. The current short draft deliberately reports dataset dependence and does not claim universal improvement or a completed hierarchical result.
