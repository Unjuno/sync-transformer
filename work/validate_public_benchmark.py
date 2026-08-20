"""Validate the public benchmark contract without running training."""
import json, subprocess
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
    tracked=subprocess.run(['git','ls-files','data/raw'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    assert not tracked, f'raw data tracked: {tracked}'
    print({'tasks':len(manifest['tasks']),'electricity_clients':3,'raw_tracked':False,'cuda_overwrite_cpu':False})
if __name__=='__main__': main()
