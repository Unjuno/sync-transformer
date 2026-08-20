"""Create a small, explicit cross-client electricity evidence table."""
import argparse, json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--mt001', required=True); ap.add_argument('--mt002', required=True); ap.add_argument('--mt003'); ap.add_argument('--output', required=True)
    args = ap.parse_args()
    paths = [('MT_001', args.mt001), ('MT_002', args.mt002)] + ([('MT_003', args.mt003)] if args.mt003 else [])
    rows = []
    for client, path in paths:
        d = json.loads(Path(path).read_text())
        rows.append({'client': client, 'vanilla_small_mse': d['vanilla_small_mse'], 'sync_base_mse': d['sync_base_mse'], 'sync_external_mse': d['sync_external_mse'], 'external_minus_base_delta': d['external_minus_base_delta'], 'gate_use_rate': d['gate_use_rate_mean'], 'failure': 'gate abstained on every query' if d['gate_use_rate_mean'] == 0 else 'deployed residual worsened base head' if d['external_minus_base_delta']['mean'] > 0 else 'no measured worsening'})
    out = {'protocol': 'same 720/96 causal split, 3 seeds, 20 epochs; per-client pooled query bootstrap', 'rows': rows, 'conclusion': 'SYNC behavior is client-dependent; no general electricity advantage is established.'}
    Path(ap.parse_args().output).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
if __name__ == '__main__': main()
