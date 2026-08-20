"""Summarize rolling-origin common-runner artifacts.

The script intentionally reports paired SYNC-minus-head deltas, improvement
fractions, and gate use rates without changing any experiment artifacts.
"""
import argparse, glob, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"

def summarize(pattern):
    rows = []
    for path in sorted(OUT.glob(pattern)):
        d = json.loads(path.read_text())
        deltas = np.concatenate([
            np.asarray(r["external_query_mse"]) - np.asarray(r["head_query_mse"])
            for r in d["rows"]
        ])
        rows.append({
            "artifact": path.name,
            "dataset": d["rows"][0]["dataset"],
            "eval_start_frac": d.get("eval_start_frac"),
            "eval_end_frac": d.get("eval_end_frac"),
            "n_queries": int(len(deltas)),
            "mean_sync_minus_head": float(deltas.mean()),
            "median_sync_minus_head": float(np.median(deltas)),
            "improvement_fraction": float(np.mean(deltas < 0)),
            "gate_use_rate_mean": float(np.mean([r["gate_use_rate"] for r in d["rows"]])),
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default="common_runner_*_ev*.json")
    ap.add_argument("--output", default="rolling_origin_summary.json")
    args = ap.parse_args()
    rows = summarize(args.pattern)
    target = OUT / args.output
    target.write_text(json.dumps({"pattern": args.pattern, "rows": rows}, indent=2))
    print(json.dumps({"output": str(target), "rows": rows}, indent=2))

if __name__ == "__main__":
    main()
