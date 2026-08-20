"""Materialize an OPSD renewable generation series for the common runner."""
from pathlib import Path
import argparse
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--column', default='solar_DE_generation')
    args = ap.parse_args()
    src = ROOT / 'data' / 'raw' / 'opsd_time_series_2016.csv'
    frame = pd.read_csv(src, usecols=['utc-timestamp', args.column])
    frame['ts'] = pd.to_datetime(frame['utc-timestamp'], errors='coerce', utc=True)
    frame = frame[frame['ts'].dt.year.between(2012, 2015)].copy()
    y = pd.to_numeric(frame[args.column], errors='coerce').interpolate(limit=3, limit_direction='both')
    keep = y.notna()
    out = ROOT / 'outputs' / 'OPSD_solar_DE.csv'
    pd.DataFrame({'date': frame.loc[keep, 'utc-timestamp'].astype(str), 'OT': y.loc[keep].astype('float32')}).to_csv(out, index=False)
    print({'column': args.column, 'rows': int(keep.sum()), 'output': str(out)})

if __name__ == '__main__':
    main()
