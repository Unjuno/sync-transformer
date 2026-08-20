"""Validate the public benchmark contract without running training."""
import csv, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    manifest=json.loads((ROOT/'outputs/data_manifest.json').read_text())
    assert len(manifest['tasks']) == 10
    required={'task_id','status','source'}
    assert all(required <= set(t) for t in manifest['tasks'])
    runtime=json.loads((ROOT/'outputs/runtime_manifest.json').read_text())
    assert runtime['cuda_extension']['overwrite_cpu'] is False
    for client in ('MT_001','MT_002','MT_003'):
        d=ROOT/'outputs/benchmark_runs/electricity'/client
        for name in ('config.json','per_seed.json','query_metrics.json','summary.json','comparison.md'):
            assert (d/name).exists(), f'missing {d/name}'
    for dataset in ('ETTh1','ETTh2','ETTm1','ETTm2'):
        d=ROOT/'outputs/benchmark_runs/ett'/dataset
        for name in ('config.json','per_seed.json','query_metrics.json','summary.json','comparison.md'):
            assert (d/name).exists(), f'missing {d/name}'
    for dataset in ('BDG2_Panther_office_Hannah','BDG2_Panther_office_Catherine','BDG2_Panther_lodging_Cora'):
        d=ROOT/'outputs/benchmark_runs/hvac'/dataset
        for name in ('config.json','per_seed.json','query_metrics.json','summary.json','comparison.md'):
            assert (d/name).exists(), f'missing {d/name}'
        cfg=json.loads((d/'config.json').read_text()); assert cfg['seeds']==[163,164,165]
        per=json.loads((d/'per_seed.json').read_text()); query=json.loads((d/'query_metrics.json').read_text()); summary=json.loads((d/'summary.json').read_text())
        assert len(per)==len(query)==3
        assert all(len(q['sync_external_mse'])==len(q['vanilla_mse']) for q in query)
        assert len(summary['paired_delta_95ci'])==2
        assert summary['paired_delta_95ci'][0] <= summary['paired_delta_95ci'][1]
    for sensor in ('0','1'):
        traffic_dir=ROOT/'outputs/benchmark_runs/traffic'/f'METR_LA_sensor{sensor}'
        for name in ('config.json','per_seed.json','query_metrics.json','summary.json','comparison.md'):
            assert (traffic_dir/name).exists(), f'missing {traffic_dir/name}'
    traffic_manifest=next(t for t in manifest['tasks'] if t['task_id']=='traffic')
    assert traffic_manifest['status']=='benchmarked_one_sensor'
    matrix_path=ROOT/'outputs/benchmark_matrix.csv'
    rows=list(csv.DictReader(matrix_path.open(newline='', encoding='utf-8')))
    assert len(rows) == 16, f'expected 16 benchmark matrix rows, got {len(rows)}'
    ett_rows={r['dataset'] for r in rows if r['task']=='ett'}
    assert {'ETTh1','ETTh2','ETTm1','ETTm2'} <= ett_rows
    electricity_rows={r['dataset'] for r in rows if r['task']=='electricity'}
    assert all(any(client in dataset for dataset in electricity_rows) for client in ('MT_001','MT_002','MT_003'))
    assert sum(r['task']=='hvac' and r['status']=='measured' for r in rows) == 1
    hvac_manifest=next(t for t in manifest['tasks'] if t['task_id']=='hvac')
    assert hvac_manifest['status']=='benchmarked_three_meters'
    assert all(r['status']=='measured' for r in rows if r['task'] in {'ett','electricity'})
    tracked=subprocess.run(['git','ls-files','data/raw'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    assert not tracked, f'raw data tracked: {tracked}'
    print({'tasks':len(manifest['tasks']),'matrix_rows':len(rows),'electricity_clients':3,'ett_datasets':4,'hvac_meters':3,'traffic_sensors':2,'raw_tracked':False,'cuda_overwrite_cpu':False})
if __name__=='__main__': main()
