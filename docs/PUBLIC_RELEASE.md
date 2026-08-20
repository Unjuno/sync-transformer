# Public release guide

## What is included

The repository contains original source code, benchmark configuration, small
JSON/Markdown/CSV result artifacts, tests, and provenance manifests. The
canonical aggregate is `outputs/benchmark_matrix.csv`.

## What is intentionally excluded

Downloaded raw datasets, archives, model checkpoints, local environments, and
large generated scratch files are ignored. Reproduce them with the scripts in
`work/` after accepting the upstream terms.

## Claim boundary

The supported claim is conditional utility of historical episode retrieval,
ordered residual transport, and abstention on some recurring processes. The
results do not establish universal forecasting superiority, novelty of the
general retrieval-augmented forecasting idea, or closed-loop robot safety.

## Reproduction and review

```powershell
python -m pytest -q
python work/validate_public_benchmark.py
python work/audit_metric_completeness.py
```

Before publishing a new dataset result, add its source, license, version, and
hash to `data/manifest.json`, keep raw files outside Git, and add a failure
note when the result is negative or inconclusive.
