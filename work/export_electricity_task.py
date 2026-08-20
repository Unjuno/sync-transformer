"""Export the documented per-task artifact layout from electricity runs."""
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--client', required=True); ap.add_argument('--sync', required=True); ap.add_argument('--vanilla', required=True); ap.add_argument('--output', required=True); a=ap.parse_args()
    sync=json.loads(Path(a.sync).read_text())['rows']; van=json.loads(Path(a.vanilla).read_text())['rows']
    root=Path(a.output); root.mkdir(parents=True, exist_ok=True)
    query=[]; per_seed=[]
    for s,v in zip(sync,van):
        query.append({'seed':s['seed'],'base_head_mse':s['head_query_mse'],'external_mse':s['external_query_mse'],'vanilla_mse':v['query_mse']})
        per_seed.append({'seed':s['seed'],'base_head_mse':s['base_head_mse'],'external_mse':s['external_residual_mse'],'vanilla_mse':v['normalized_mse'],'gate_use_rate':s['gate_use_rate'],'persistence_mse':s['persistence_mse']})
    config={'task_id':'electricity','client':a.client,'context_length':720,'horizon':96,'split':'chronological 60/20/20','seeds':[int(x['seed']) for x in per_seed],'epochs':20,'device':'cpu'}
    (root/'config.json').write_text(json.dumps(config,indent=2)); (root/'per_seed.json').write_text(json.dumps(per_seed,indent=2)); (root/'query_metrics.json').write_text(json.dumps(query,indent=2))
    mean=lambda k: sum(x[k] for x in per_seed)/len(per_seed)
    summary={'task_id':'electricity','client':a.client,'status':'measured','mean_external_mse':mean('external_mse'),'mean_vanilla_mse':mean('vanilla_mse'),'mean_gate_use_rate':mean('gate_use_rate'),'failure_notes':'client-dependent; inspect query bootstrap report'}
    (root/'summary.json').write_text(json.dumps(summary,indent=2))
    (root/'comparison.md').write_text(f"# Electricity {a.client}\n\nSame 720/96 causal protocol, 3 seeds, 20 epochs.\n\n- Vanilla MSE: `{summary['mean_vanilla_mse']:.6f}`\n- SYNC external MSE: `{summary['mean_external_mse']:.6f}`\n- Gate use rate: `{summary['mean_gate_use_rate']:.6f}`\n\nSee the committed bootstrap report for uncertainty intervals and failure interpretation.\n")
if __name__=='__main__': main()
