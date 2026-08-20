"""Export the measured BDG2 single-meter run into the public task layout."""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
def main():
    sync_path = next(ROOT.glob('outputs/common_runner_BDG2_Panther_office_Hannah*.json'))
    van = json.loads((ROOT/'outputs/vanilla_BDG2_Panther_office_Hannah_20.json').read_text())['rows']
    sync = json.loads(sync_path.read_text())['rows']
    out = ROOT/'outputs/benchmark_runs/hvac/BDG2_Panther_office_Hannah'; out.mkdir(parents=True, exist_ok=True)
    per=[]; query=[]
    for s,v in zip(sync,van):
        per.append({'seed':s['seed'],'sync_base_mse':s['base_head_mse'],'sync_external_mse':s['external_residual_mse'],'vanilla_mse':v['normalized_mse'],'persistence_mse':s['persistence_mse'],'gate_use_rate':s['gate_use_rate'],'parameter_count_sync':s['parameter_count'],'parameter_count_vanilla':v['parameter_count']})
        query.append({'seed':s['seed'],'sync_external_mse':s['external_query_mse'],'vanilla_mse':v['query_mse'],'paired_delta':(np.asarray(s['external_query_mse'])-np.asarray(v['query_mse'])).tolist()})
    deltas=np.concatenate([np.asarray(x['paired_delta']) for x in query]); rng=np.random.default_rng(163); boots=np.array([deltas[rng.integers(0,len(deltas),len(deltas))].mean() for _ in range(10000)])
    summary={'task_id':'hvac','dataset':'BDG2_Panther_office_Hannah','status':'measured','mean_sync_external_mse':float(np.mean([x['sync_external_mse'] for x in per])),'mean_vanilla_mse':float(np.mean([x['vanilla_mse'] for x in per])),'paired_delta_sync_minus_vanilla':float(deltas.mean()),'paired_delta_95ci':[float(np.quantile(boots,.025)),float(np.quantile(boots,.975))],'mean_gate_use_rate':float(np.mean([x['gate_use_rate'] for x in per])),'failure_notes':'single BDG2 meter; gate abstained on all test queries; not a building-wide claim'}
    (out/'config.json').write_text(json.dumps({'task_id':'hvac','dataset':'BDG2_Panther_office_Hannah','context_length':720,'horizon':96,'split':'chronological 60/20/20','seeds':[163,164,165],'epochs':20,'device':'cpu'},indent=2))
    (out/'per_seed.json').write_text(json.dumps(per,indent=2)); (out/'query_metrics.json').write_text(json.dumps(query,indent=2)); (out/'summary.json').write_text(json.dumps(summary,indent=2))
    (out/'comparison.md').write_text(f"# HVAC BDG2 single-meter benchmark\n\n- SYNC external MSE: `{summary['mean_sync_external_mse']:.6f}`\n- Vanilla Transformer MSE: `{summary['mean_vanilla_mse']:.6f}`\n- Paired SYNC−Vanilla delta: `{summary['paired_delta_sync_minus_vanilla']:.6f}` (95% CI `{summary['paired_delta_95ci']}`)\n- Gate use rate: `{summary['mean_gate_use_rate']:.6f}`\n\nThis is one meter, not a building-wide result.\n")
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
