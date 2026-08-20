"""Build the public benchmark matrix with explicit N/A for unmeasured tasks."""
import csv, json
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['task','dataset','horizon','split','model','parameter_count','mean_metric','95% CI','improvement_fraction','abstention_or_fallback_rate','latency','failure_notes','status']

def main():
    rows = []
    rows.append(dict(zip(FIELDS, ['ett','ETTh1/ETTh2/ETTm1/ETTm2','task-specific','canonical','Vanilla/SYNC','recorded','recorded','recorded','conditional','recorded','recorded','split-sensitive transfer','measured'])))
    for dataset in ('ETTh1','ETTh2','ETTm1','ETTm2'):
        d=json.loads((ROOT/'outputs/benchmark_runs/ett'/dataset/'summary.json').read_text())
        rows.append(dict(zip(FIELDS,['ett',dataset,d['horizon'] if 'horizon' in d else 'task-specific','canonical','Vanilla small/SYNC','recorded',f"{d['mean_sync_external_mse']:.6f}",'recorded','conditional',f"{d['mean_gate_use_rate']:.6f}",'recorded',d['failure_notes'],'measured'])))
    summary = json.loads((ROOT/'outputs/electricity_cross_client_summary.json').read_text())
    for r in summary['rows']:
        rows.append(dict(zip(FIELDS, ['electricity',f"UCI ElectricityLoadDiagrams {r['client']}",'96','60/20/20','Vanilla small/SYNC','12800/19296',f"{r['sync_external_mse']['mean']:.6f}",f"[{r['sync_external_mse']['ci95'][0]:.6f}, {r['sync_external_mse']['ci95'][1]:.6f}]",'not pooled',f"{r['gate_use_rate']:.6f}",'recorded',r['failure'],'measured'])))
    hvac=[json.loads(p.read_text()) for p in (ROOT/'outputs/benchmark_runs/hvac').glob('*/summary.json')]
    if hvac:
        rows.append(dict(zip(FIELDS, ['hvac','BDG2 Panther (3 meters)','96','60/20/20','Vanilla/SYNC','75360/19296',f"{np.mean([x['mean_sync_external_mse'] for x in hvac]):.6f}",'per-meter CI','paired delta',f"{np.mean([x['mean_gate_use_rate'] for x in hvac]):.6f}",'recorded','three meters; series-dependent; not building-wide','measured'])))
    traffic=[json.loads(p.read_text()) for p in (ROOT/'outputs/benchmark_runs/traffic').glob('METR_LA_sensor*/summary.json')]
    rows.append(dict(zip(FIELDS, ['traffic','METR-LA (2 sensors)','96','60/20/20','Vanilla/SYNC','75360/19296',f"{np.mean([x['mean_sync_external_mse'] for x in traffic]):.6f}",'per-sensor CI','paired delta',f"{np.mean([x['mean_gate_use_rate'] for x in traffic]):.6f}",'recorded','two sensors; spatial multivariate effects not evaluated','measured'])))
    renewable = json.loads((ROOT/'outputs/benchmark_runs/renewable/OPSD_solar_DE/summary.json').read_text())
    rows.append(dict(zip(FIELDS, ['renewable','OPSD solar_DE_generation','96','60/20/20','Vanilla/SYNC','75360/19296',f"{renewable['mean_sync_external_mse']:.6g}",'query bootstrap CI','paired delta',f"{renewable['mean_gate_use_rate']:.6f}",'recorded',renewable['failure_notes'],'measured_alternative'])))
    pending = [('server','Alibaba cluster trace','pending'),('retail','M5/Favorita','pending'),('industrial','NASA C-MAPSS','blocked_source_unavailable'),('robot_manipulation','RoboMimic/Open X subset','pending'),('robot_trajectory','nuScenes or simulator logs','pending')]
    for task, dataset, status in pending:
        note = 'official source unavailable/license unspecified' if task in ('industrial','renewable') else 'adapter/data not ready'
        rows.append(dict(zip(FIELDS,[task,dataset,'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A',note,status])))
    out = ROOT/'outputs/benchmark_matrix.csv'; out.write_text('')
    with out.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print(f'Wrote {out} ({len(rows)} rows)')
if __name__ == '__main__': main()
