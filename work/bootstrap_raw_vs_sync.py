"""Bootstrap raw-candidate versus fused residual transport controls."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'outputs'; rng=np.random.default_rng(20260815)
cfg={'ETTh1':'q24_c8','ETTm1':'q96_c48','ETTm2':'q96_c48'}; rows=[]
for ds,tag in cfg.items():
 d=json.loads((OUT/f'common_runner_{ds}_{tag}_lbfull_k8_rich0_end_sf_vg0.079168.json').read_text()); delta=np.concatenate([np.asarray(r['external_query_mse'])-np.asarray(r['raw_transport_query_mse']) for r in d['rows']]); n=len(delta); bs=np.array([delta[rng.integers(0,n,n)].mean() for _ in range(10000)])
 rows.append({'dataset':ds,'queries':n,'sync_minus_raw':float(delta.mean()),'ci95_low':float(np.quantile(bs,.025)),'ci95_high':float(np.quantile(bs,.975)),'fraction_sync_better':float(np.mean(delta<0))})
(OUT/'raw_vs_sync_bootstrap.json').write_text(json.dumps({'protocol':'same candidate bank; endpoint+seasonal; query bootstrap','rows':rows},indent=2)); print(json.dumps(rows,indent=2))
