"""Query-level bootstrap summaries for the published electricity artifacts."""
import argparse, json
from pathlib import Path
import numpy as np

def ci(values, rng, reps=2000):
    x = np.asarray(values, dtype=float)
    draws = rng.choice(x, size=(reps, x.size), replace=True).mean(axis=1)
    return {"mean": float(x.mean()), "ci95": [float(np.quantile(draws, .025)), float(np.quantile(draws, .975))], "n": int(x.size)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sync", required=True)
    ap.add_argument("--vanilla", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    sync = json.loads(Path(args.sync).read_text())['rows']
    vanilla = json.loads(Path(args.vanilla).read_text())['rows']
    rng = np.random.default_rng(20260820)
    ext, base, pers, van, deltas = [], [], [], [], []
    for s, v in zip(sync, vanilla):
        ext.extend(s['external_query_mse']); base.extend(s['head_query_mse']); pers.extend([s['persistence_mse']] * len(s['head_query_mse']))
        van.extend(v['query_mse'])
        deltas.extend(np.asarray(s['external_query_mse']) - np.asarray(s['head_query_mse']))
    result = {"protocol": "pooled test queries; bootstrap resamples queries with seed 20260820",
              "sync_external_mse": ci(ext, rng), "sync_base_mse": ci(base, rng),
              "seasonal_persistence_mse": ci(pers, rng), "vanilla_small_mse": ci(van, rng),
              "external_minus_base_delta": ci(deltas, rng),
              "gate_use_rate_mean": float(np.mean([r['gate_use_rate'] for r in sync]))}
    Path(args.output).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
