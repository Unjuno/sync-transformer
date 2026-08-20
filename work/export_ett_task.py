"""Export one ETT dataset into the documented task artifact layout."""
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dataset',required=True); ap.add_argument('--sync',required=True); ap.add_argument('--vanilla',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    sync=json.loads(Path(a.sync).read_text())['rows']; van=json.loads(Path(a.vanilla).read_text())['rows']; root=Path(a.output); root.mkdir(parents=True,exist_ok=True)
    per=[]; query=[]
    for s,v in zip(sync,van):
        per.append({'seed':s['seed'],'sync_base_mse':s['base_head_mse'],'sync_external_mse':s['external_residual_mse'],'vanilla_mse':v['normalized_mse'],'gate_use_rate':s['gate_use_rate']})
        query.append({'seed':s['seed'],'sync_external_mse':s['external_query_mse'],'vanilla_mse':v['query_mse']})
    cfg={'task_id':'ett','dataset':a.dataset,'context_length':sync[0]['P'],'horizon':sync[0]['H'],'split':'canonical','seeds':[x['seed'] for x in per],'epochs':20,'device':'cpu'}
    (root/'config.json').write_text(json.dumps(cfg,indent=2)); (root/'per_seed.json').write_text(json.dumps(per,indent=2)); (root/'query_metrics.json').write_text(json.dumps(query,indent=2))
    mean=lambda k: sum(x[k] for x in per)/len(per); summary={'task_id':'ett','dataset':a.dataset,'status':'measured','mean_sync_external_mse':mean('sync_external_mse'),'mean_vanilla_mse':mean('vanilla_mse'),'mean_gate_use_rate':mean('gate_use_rate'),'failure_notes':'canonical ETT result; interpretation is dataset/split conditional'}
    (root/'summary.json').write_text(json.dumps(summary,indent=2)); (root/'comparison.md').write_text(f"# {a.dataset}\n\n- Vanilla small MSE: `{summary['mean_vanilla_mse']:.6f}`\n- SYNC external MSE: `{summary['mean_sync_external_mse']:.6f}`\n- Gate use rate: `{summary['mean_gate_use_rate']:.6f}`\n")
if __name__=='__main__': main()
