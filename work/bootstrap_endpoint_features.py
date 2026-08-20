"""Query bootstrap CIs for endpoint/seasonal feature controls."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'outputs'; rng=np.random.default_rng(20260814)
datasets={'ETTh1':'q24_c8','ETTh2':'q24_c8','ETTm1':'q96_c48','ETTm2':'q96_c48'}; result=[]
for ds,tag in datasets.items():
 p=OUT/f'common_runner_{ds}_{tag}_lbfull_k8_rich0_end_sf_vg0.079168.json'; d=json.loads(p.read_text()); delta=np.concatenate([np.asarray(r['external_query_mse'])-np.asarray(r['head_query_mse']) for r in d['rows']]); n=len(delta); means=[]
 for _ in range(10000): means.append(delta[rng.integers(0,n,n)].mean())
 result.append({'dataset':ds,'queries':n,'mean_delta':float(delta.mean()),'ci95_low':float(np.quantile(means,.025)),'ci95_high':float(np.quantile(means,.975)),'fraction_improved':float(np.mean(delta<0))})
(OUT/'endpoint_feature_bootstrap.json').write_text(json.dumps({'protocol':'endpoint+seasonal features, pooled query bootstrap','rows':result},indent=2)); print(json.dumps(result,indent=2))
