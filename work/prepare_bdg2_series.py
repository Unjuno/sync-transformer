"""Materialize one deterministic BDG2 meter as the common runner's CSV shape."""
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='data/raw/bdg2_electricity_cleaned.csv')
    ap.add_argument('--column', default='Panther_office_Hannah')
    ap.add_argument('--dataset', default='BDG2_Panther_office_Hannah')
    args = ap.parse_args()
    src = ROOT / args.input
    out = ROOT / 'outputs' / f'{args.dataset}.csv'
    frame = pd.read_csv(src, usecols=['timestamp', args.column])
    values = pd.to_numeric(frame[args.column], errors='coerce').interpolate(limit_direction='both')
    result = pd.DataFrame({'date': frame['timestamp'], 'OT': values.astype('float32')})
    result.to_csv(out, index=False)
    print({'dataset': args.dataset, 'rows': len(result), 'column': args.column, 'output': str(out)})

if __name__ == '__main__':
    main()
