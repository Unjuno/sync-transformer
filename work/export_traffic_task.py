"""Export METR-LA sensor benchmark artifacts."""
import argparse,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def export(sensor):
    dataset=f'METR_LA_sensor{sensor}'; sync=json.loads(next(ROOT.glob(f'outputs/common_runner_{dataset}*.json')).read_text())['rows']; van=json.loads((ROOT/f'outputs/vanilla_{dataset}_20.json').read_text())['rows']; out=ROOT/'outputs'/'benchmark_runs'/'traffic'/dataset; out.mkdir(parents=True,exist_ok=True)
    per=[]; query=[]
    for s,v in zip(sync,van):
        per.append({'seed':s['seed'],'sync_external_mse':s['external_residual_mse'],'vanilla_mse':v['normalized_mse'],'persistence_mse':s['persistence_mse'],'gate_use_rate':s['gate_use_rate']}); query.append({'seed':s['seed'],'sync_external_mse':s['external_query_mse'],'vanilla_mse':v['query_mse']})
    delta=np.concatenate([np.asarray(q['sync_external_mse'])-np.asarray(q['vanilla_mse']) for q in query]); rng=np.random.default_rng(163); boots=np.array([delta[rng.integers(0,len(delta),len(delta))].mean() for _ in range(10000)])
    summary={'task_id':'traffic','dataset':dataset,'status':'measured','mean_sync_external_mse':float(np.mean([x['sync_external_mse'] for x in per])),'mean_vanilla_mse':float(np.mean([x['vanilla_mse'] for x in per])),'paired_delta_sync_minus_vanilla':float(delta.mean()),'paired_delta_95ci':[float(np.quantile(boots,.025)),float(np.quantile(boots,.975))],'mean_gate_use_rate':float(np.mean([x['gate_use_rate'] for x in per])),'failure_notes':'one METR-LA sensor; spatial multivariate traffic effects not evaluated'}
    (out/'config.json').write_text(json.dumps({'task_id':'traffic','dataset':dataset,'context_length':720,'horizon':96,'split':'chronological 60/20/20','seeds':[163,164,165],'epochs':20,'device':'cpu'},indent=2)); (out/'per_seed.json').write_text(json.dumps(per,indent=2)); (out/'query_metrics.json').write_text(json.dumps(query,indent=2)); (out/'summary.json').write_text(json.dumps(summary,indent=2)); (out/'comparison.md').write_text(f"# METR-LA {dataset}\n\nSYNC `{summary['mean_sync_external_mse']:.6f}`; Vanilla `{summary['mean_vanilla_mse']:.6f}`; delta `{summary['paired_delta_sync_minus_vanilla']:.6f}` (95% CI `{summary['paired_delta_95ci']}`).\n")
    return summary
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--sensors',default='0,1'); args=ap.parse_args()
    for sensor in args.sensors.split(','): print(json.dumps(export(sensor),indent=2))
if __name__=='__main__': main()
