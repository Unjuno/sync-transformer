"""Export AI4I industrial sensor alternative benchmark."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main():
 d='AI4I_process_temperature'; sf=max(ROOT.glob(f'outputs/common_runner_{d}*.json'),key=lambda p:p.stat().st_mtime); s=json.loads(sf.read_text())['rows']; v=json.loads((ROOT/f'outputs/vanilla_{d}_20.json').read_text())['rows']; out=ROOT/'outputs'/'benchmark_runs'/'industrial'/d; out.mkdir(parents=True,exist_ok=True); q=[]; per=[]
 for a,b in zip(s,v): per.append({'seed':a['seed'],'sync_external_mse':a['external_residual_mse'],'vanilla_mse':b['normalized_mse'],'gate_use_rate':a['gate_use_rate']}); q.append(np.asarray(a['external_query_mse'])-np.asarray(b['query_mse']))
 delta=np.concatenate(q); rng=np.random.default_rng(163); boot=np.array([delta[rng.integers(0,len(delta),len(delta))].mean() for _ in range(10000)]); summary={'task_id':'industrial','dataset':d,'status':'measured_alternative','mean_sync_external_mse':float(np.mean([x['sync_external_mse'] for x in per])),'mean_vanilla_mse':float(np.mean([x['vanilla_mse'] for x in per])),'paired_delta_95ci':[float(np.quantile(boot,.025)),float(np.quantile(boot,.975))],'mean_gate_use_rate':float(np.mean([x['gate_use_rate'] for x in per])),'failure_notes':'UCI AI4I 2020 is synthetic predictive-maintenance data; process-temperature forecasting, not RUL classification'}; (out/'config.json').write_text(json.dumps({'context_length':720,'horizon':96,'seeds':[163,164,165],'epochs':20,'source':'UCI AI4I 2020','license':'CC BY 4.0'},indent=2)); (out/'per_seed.json').write_text(json.dumps(per,indent=2)); (out/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
