# Contributing

Please keep experiments reproducible and claims narrow.

- Do not commit raw datasets, archives, credentials, or model checkpoints.
- Add source, version, license, and SHA256 provenance to `data/manifest.json`.
- Compare SYNC and Vanilla under the same split, horizon, seeds, and epoch budget.
- Include uncertainty, fallback/abstention behavior, latency, and failure notes.
- Do not describe open-loop trajectory metrics as closed-loop control success.
- Run `python -m pytest -q`, `python work/validate_public_benchmark.py`, and
  `python work/audit_metric_completeness.py` before submitting changes.
