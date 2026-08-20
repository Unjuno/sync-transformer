# Repository map

## Public surface

| Path | Purpose |
|---|---|
| `README.md` | Scope, results, limitations, and reproduction entry point |
| `sync_experiments/` | Small reusable adapters, task registry, orchestrator, and metrics |
| `work/` | Fetch, prepare, benchmark, export, and validation scripts |
| `data/manifest.json` | Dataset provenance and licensing metadata |
| `outputs/benchmark_matrix.csv` | Compact cross-task result index |
| `outputs/benchmark_runs/` | Reviewed per-task summaries and query/trajectory artifacts |
| `docs/` | Theory, experiment protocol, limitations, release guidance, and this map |
| `LICENSE`, `NOTICE`, `CITATION.cff` | Legal and citation metadata |

## Local-only surface

Raw downloads under `data/raw/`, model checkpoints, generated scratch sweeps,
phase experiments, smoke checks, and local run logs are ignored. They may be
regenerated locally but are not part of the public evidence surface.

## Evidence policy

Use `outputs/benchmark_matrix.csv` and the reviewed `summary.json` files as the
public result index. Historical phase notes may document discovery work, but
they do not override the current protocol or the claim boundaries in
`docs/THEORY.md` and `docs/LIMITATIONS.md`.
