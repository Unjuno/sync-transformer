"""Prepare one reproducible UCI electricity client series for the benchmark.

The raw UCI file is semicolon-separated with comma decimals. We use MT_001 as
the declared single-series target for the first benchmark, preserving the raw
file outside Git and writing only a local normalized-schema CSV.
"""
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="data/raw/electricity/LD2011_2014.txt")
    ap.add_argument("--client", default="MT_001")
    ap.add_argument("--output", default="outputs/Electricity.csv")
    args = ap.parse_args()
    raw = Path(args.raw); out = Path(args.output)
    frame = pd.read_csv(raw, sep=";", decimal=",", usecols=[0, 1],
                        index_col=0, parse_dates=True)
    series = pd.to_numeric(frame.iloc[:, 0], errors="coerce").dropna()
    if len(series) < 1000:
        raise ValueError(f"too few valid electricity observations: {len(series)}")
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"date": series.index, "OT": series.to_numpy()}).to_csv(out, index=False)
    print({"output": str(out), "client": args.client, "rows": len(series),
           "start": str(series.index.min()), "end": str(series.index.max())})

if __name__ == "__main__": main()
