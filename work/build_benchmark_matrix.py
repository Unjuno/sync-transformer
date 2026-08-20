"""Build the public benchmark matrix with explicit N/A for unmeasured tasks."""
import csv, json
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
    hvac=json.loads((ROOT/'outputs/benchmark_runs/hvac/BDG2_Panther_office_Hannah/summary.json').read_text())
    rows.append(dict(zip(FIELDS, ['hvac','BDG2 Panther_office_Hannah','96','60/20/20','Vanilla/SYNC','75360/19296',f"{hvac['mean_sync_external_mse']:.6f}",f"[{hvac['paired_delta_95ci'][0]:.6f}, {hvac['paired_delta_95ci'][1]:.6f}]",'paired delta',f"{hvac['mean_gate_use_rate']:.6f}",'recorded',hvac['failure_notes'],'measured'])))
    pending = [('renewable','GEFCom solar/wind or NREL','source_public_license_unresolved'),('traffic','METR-LA/PEMS-BAY','pending'),('server','Alibaba cluster trace','pending'),('retail','M5/Favorita','pending'),('industrial','NASA C-MAPSS','blocked_source_unavailable'),('robot_manipulation','RoboMimic/Open X subset','pending'),('robot_trajectory','nuScenes or simulator logs','pending')]
    for task, dataset, status in pending:
        note = 'official source unavailable/license unspecified' if task in ('industrial','renewable') else 'adapter/data not ready'
        rows.append(dict(zip(FIELDS,[task,dataset,'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A',note,status])))
    out = ROOT/'outputs/benchmark_matrix.csv'; out.write_text('')
    with out.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print(f'Wrote {out} ({len(rows)} rows)')
if __name__ == '__main__': main()
