"""Attach measured MAE and inference latency from fresh runner artifacts."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main():
    changed=0
    for p in (ROOT/'outputs'/'benchmark_runs').glob('*/*/summary.json'):
        d=json.loads(p.read_text()); name=d.get('dataset') or d.get('client');
        if not name: continue
        lookup=name
        if d.get('task_id')=='electricity': lookup='Electricity' if name=='MT_001' else f"Electricity_{name.replace('_','')}"
        cs=list(ROOT.glob(f'outputs/common_runner_{lookup}*.json')); vs=[ROOT/f'outputs/vanilla_{lookup}_20.json']
        if not cs or not vs[0].exists(): continue
        sr=json.loads(max(cs,key=lambda q:q.stat().st_mtime).read_text()).get('rows',[]); vr=json.loads(vs[0].read_text()).get('rows',[])
        if not sr or not vr: continue
        d['mean_sync_mae']=float(np.mean([r['external_residual_mae'] for r in sr if 'external_residual_mae' in r])) if all('external_residual_mae' in r for r in sr) else None
        d['mean_vanilla_mae']=float(np.mean([r['normalized_mae'] for r in vr if 'normalized_mae' in r])) if all('normalized_mae' in r for r in vr) else None
        d['sync_inference_latency_ms_per_query']=float(np.mean([r['inference_latency_ms_per_query'] for r in sr if 'inference_latency_ms_per_query' in r])) if all('inference_latency_ms_per_query' in r for r in sr) else None
        d['vanilla_inference_latency_ms_per_query']=float(np.mean([r['inference_latency_ms_per_query'] for r in vr if 'inference_latency_ms_per_query' in r])) if all('inference_latency_ms_per_query' in r for r in vr) else None
        p.write_text(json.dumps(d,indent=2)); changed+=1
    print({'enriched':changed})
if __name__=='__main__': main()
