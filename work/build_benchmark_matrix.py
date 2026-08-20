"""Build the public benchmark matrix with explicit N/A for unmeasured tasks."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['task','dataset','horizon','split','model','parameter_count','mean_metric','95% CI','improvement_fraction','abstention_or_fallback_rate','latency','failure_notes','status']

def main():
    rows = []
    rows.append(dict(zip(FIELDS, ['ett','ETTh1/ETTh2/ETTm1/ETTm2','task-specific','canonical','Vanilla/SYNC','recorded','recorded','recorded','conditional','recorded','recorded','split-sensitive transfer','measured'])))
    summary = json.loads((ROOT/'outputs/electricity_cross_client_summary.json').read_text())
    for r in summary['rows']:
        rows.append(dict(zip(FIELDS, ['electricity',f"UCI ElectricityLoadDiagrams {r['client']}",'96','60/20/20','Vanilla small/SYNC','12800/19296',f"{r['sync_external_mse']['mean']:.6f}",f"[{r['sync_external_mse']['ci95'][0]:.6f}, {r['sync_external_mse']['ci95'][1]:.6f}]",'not pooled',f"{r['gate_use_rate']:.6f}",'recorded',r['failure'],'measured'])))
    pending = [('renewable','GEFCom solar/wind or NREL'),('traffic','METR-LA/PEMS-BAY'),('hvac','Building Data Genome 2'),('server','Alibaba cluster trace'),('retail','M5/Favorita'),('industrial','NASA C-MAPSS'),('robot_manipulation','RoboMimic/Open X subset'),('robot_trajectory','nuScenes or simulator logs')]
    for task, dataset in pending:
        note = 'official source unavailable/license unspecified' if task == 'industrial' else 'adapter/data not ready'
        rows.append(dict(zip(FIELDS,[task,dataset,'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A',note,'pending'])))
    out = ROOT/'outputs/benchmark_matrix.csv'; out.write_text('')
    with out.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print(f'Wrote {out} ({len(rows)} rows)')
if __name__ == '__main__': main()
