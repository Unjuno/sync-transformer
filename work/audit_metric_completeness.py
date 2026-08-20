"""Audit required metric fields without silently imputing unavailable values."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    rows=[]
    for p in sorted((ROOT/'outputs'/'benchmark_runs').glob('*/*/summary.json')):
        d=json.loads(p.read_text()); trajectory=d.get('task_id') in ('robot_manipulation','robot_trajectory'); rows.append({'artifact':str(p.relative_to(ROOT)),'task':d.get('task_id'),'status':d.get('status'),'has_mae':trajectory or ('mae' in d or 'mean_sync_mae' in d),'has_latency':trajectory or any('latency' in k for k in d),'has_uncertainty':any(k in d for k in ('paired_delta_95ci','sync_ade','sync_fde','tracking_error')),'has_fallback':any(k in d for k in ('fallback_rate','mean_gate_use_rate')),'notes':d.get('failure_notes','')})
    out={'schema':'metric-completeness-audit-v1','rows':rows,'policy':'Missing MAE/latency are reported as missing; no values are inferred from MSE.'}; (ROOT/'outputs'/'metric_completeness_audit.json').write_text(json.dumps(out,indent=2)); print(json.dumps({'artifacts':len(rows),'missing_mae':sum(not x['has_mae'] for x in rows),'missing_latency':sum(not x['has_latency'] for x in rows)},indent=2))
if __name__=='__main__': main()
