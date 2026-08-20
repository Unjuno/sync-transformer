"""Export measured BDG2 meter runs into the public task layout."""
import argparse, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def export(dataset):
    sync=json.loads(next(ROOT.glob(f'outputs/common_runner_{dataset}*.json')).read_text())['rows']
    van=json.loads((ROOT/f'outputs/vanilla_{dataset}_20.json').read_text())['rows']
    out=ROOT/f'outputs/benchmark_runs/hvac/{dataset}'; out.mkdir(parents=True,exist_ok=True)
    per=[]; query=[]
    for s,v in zip(sync,van):
        per.append({'seed':s['seed'],'sync_base_mse':s['base_head_mse'],'sync_external_mse':s['external_residual_mse'],'vanilla_mse':v['normalized_mse'],'persistence_mse':s['persistence_mse'],'gate_use_rate':s['gate_use_rate'],'parameter_count_sync':s['parameter_count'],'parameter_count_vanilla':v['parameter_count']})
        query.append({'seed':s['seed'],'sync_external_mse':s['external_query_mse'],'vanilla_mse':v['query_mse'],'paired_delta':(np.asarray(s['external_query_mse'])-np.asarray(v['query_mse'])).tolist()})
    deltas=np.concatenate([np.asarray(x['paired_delta']) for x in query]); rng=np.random.default_rng(163); boots=np.array([deltas[rng.integers(0,len(deltas),len(deltas))].mean() for _ in range(10000)])
    summary={'task_id':'hvac','dataset':dataset,'status':'measured','mean_sync_external_mse':float(np.mean([x['sync_external_mse'] for x in per])),'mean_vanilla_mse':float(np.mean([x['vanilla_mse'] for x in per])),'paired_delta_sync_minus_vanilla':float(deltas.mean()),'paired_delta_95ci':[float(np.quantile(boots,.025)),float(np.quantile(boots,.975))],'mean_gate_use_rate':float(np.mean([x['gate_use_rate'] for x in per])),'failure_notes':'three BDG2 meters; gate behavior is series-dependent; not a building-wide claim'}
    (out/'config.json').write_text(json.dumps({'task_id':'hvac','dataset':dataset,'context_length':720,'horizon':96,'split':'chronological 60/20/20','seeds':[163,164,165],'epochs':20,'device':'cpu'},indent=2)); (out/'per_seed.json').write_text(json.dumps(per,indent=2)); (out/'query_metrics.json').write_text(json.dumps(query,indent=2)); (out/'summary.json').write_text(json.dumps(summary,indent=2)); (out/'comparison.md').write_text(f"# HVAC BDG2 {dataset}\n\nSYNC external MSE `{summary['mean_sync_external_mse']:.6f}`; Vanilla MSE `{summary['mean_vanilla_mse']:.6f}`; paired delta `{summary['paired_delta_sync_minus_vanilla']:.6f}` (95% CI `{summary['paired_delta_95ci']}`).\n")
    return summary
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--datasets',default='BDG2_Panther_office_Hannah,BDG2_Panther_office_Catherine,BDG2_Panther_lodging_Cora'); args=ap.parse_args()
    for dataset in args.datasets.split(','): print(json.dumps(export(dataset),indent=2))
if __name__=='__main__': main()
