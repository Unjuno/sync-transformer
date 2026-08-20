# Limitations and reproducibility notes

## Implementation limitation

The original SYNC_CORE source and the exact earliest Phase 4A–4B artifact bundle were not recovered. The public code is a transparent common-protocol reconstruction. It should not be described as byte-for-byte reproduction of the initial implementation.

## Statistical limitation

Effects change sign across datasets and chronological windows. A positive pooled or dataset-level mean does not establish robustness. Report query-level paired uncertainty, split, gate use rate, and abstention rate together.

## Baseline limitation

Seasonal-naive is strong on these datasets and can beat current SYNC configurations. A complete external comparison against RAFT has not yet been run because the current machine has no CUDA GPU.

## Internal-search limitation

The initial report and later reconstruction diagnostics use different candidate construction, scaling, and evaluation protocols. Their numerical values must not be compared as if they were one experiment. The discrepancy is itself an open reproducibility issue.

## Data and artifact limitation

Large raw CSVs, generated logs, and vendor trees are excluded from the repository. The repository contains scripts, compact summaries, manifests, and the protocol needed to regenerate results when the public data are available.

## GPU handoff

The GPU experiment is an extension, not part of the current CPU claim. See `outputs/SYNC_Transformer_GPU_extension_plan.md` before running CUDA experiments on another machine.
