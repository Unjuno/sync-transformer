import json
from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'outputs'
def main():
 names=['ETTh1','ETTh2','ETTm1','ETTm2']; checks=[]
 for n in names:
  d=pd.read_csv(OUT/f'{n}.csv'); checks.append((n,bool(len(d)>0),bool('OT' in d.columns),bool(d.OT.notna().all())))
 for f in ['phase150_sync_architecture_public_summary.md','phase151_learned_benefit_gate.md','phase152_reverse_transport.md','phase153_stride_sensitivity.md','public_dataset_manifest.md']:
  checks.append((f,bool((OUT/f).exists())))
 j=json.loads((OUT/'phase151_learned_benefit_gate.json').read_text())
 for r in j:
  checks.append((r['dataset'],bool(np.isfinite([r['base_mse'],r['learned_gate_mse'],*r['gate_minus_base_bootstrap95']]).all())))
 ok=all(all(x[1:]) if isinstance(x,tuple) and len(x)>2 else x[1] for x in checks); print(json.dumps({'passed':ok,'checks':checks},indent=2)); raise SystemExit(0 if ok else 1)
if __name__=='__main__':main()
