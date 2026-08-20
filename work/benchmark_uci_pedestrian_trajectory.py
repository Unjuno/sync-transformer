"""UCI pedestrian traffic trajectory alternative for the mobile trajectory task."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from sync_experiments.trajectory_metrics import ade,fde,bootstrap_ci,fallback_rate,safety_violation_rate
def main():
 d=pd.read_csv(ROOT/'data'/'raw'/'uci_pedestrian'/'pedestrian_traffic_data'/'tracks.csv'); batches=[]
 for oid,g in d.groupby('oid'):
  g=g.sort_values('timestamp'); xy=g[['x','y']].to_numpy(float); ts=g.timestamp.to_numpy();
  for i in range(0,len(xy)-20+1,2): batches.append((str(oid),ts[i],xy[i:i+8],xy[i+8:i+20]))
 demos=sorted({x[0] for x in batches}); n=len(demos); train=set(demos[:max(1,int(.6*n))]); cal=set(demos[max(1,int(.6*n)):max(2,int(.8*n))]); test=set(demos[max(2,int(.8*n)):]); tr=[x for x in batches if x[0] in train]; ca=[x for x in batches if x[0] in cal]; te=[x for x in batches if x[0] in test]
 dist=[min(np.linalg.norm(x[2][-1]-y[2][-1]) for y in tr) for x in ca]; threshold=float(np.quantile(dist,.95)) if dist else float('inf'); steps=np.concatenate([np.linalg.norm(np.diff(np.vstack([x[2][-1:],x[3]]),axis=0),axis=1) for x in tr]); lim=float(np.quantile(steps,.999))
 rows=[]
 for x in te:
  near=min(tr,key=lambda y:np.linalg.norm(x[2][-1]-y[2][-1])); dd=float(np.linalg.norm(x[2][-1]-near[2][-1])); fb=dd>threshold; pred=np.repeat(x[2][-1][None,:],12,axis=0) if fb else near[3]+(x[2][-1]-near[2][-1]); vio=bool(np.any(np.linalg.norm(np.diff(np.vstack([x[2][-1:],pred]),axis=0),axis=1)>lim)); pers=np.repeat(x[2][-1][None,:],12,axis=0); rows.append({'track':x[0],'ade_sync':ade(pred,x[3]),'fde_sync':fde(pred,x[3]),'ade_persistence':ade(pers,x[3]),'fde_persistence':fde(pers,x[3]),'fallback':fb,'safety_violation':vio})
 out=ROOT/'outputs'/'benchmark_runs'/'robot_trajectory'/'uci_pedestrian'; out.mkdir(parents=True,exist_ok=True); summary={'task_id':'robot_trajectory','dataset':'uci_pedestrian','status':'measured_alternative','n_train':len(tr),'n_calibration':len(ca),'n_test':len(te),'sync_ade':bootstrap_ci([r['ade_sync'] for r in rows]),'sync_fde':bootstrap_ci([r['fde_sync'] for r in rows]),'persistence_ade':bootstrap_ci([r['ade_persistence'] for r in rows]),'persistence_fde':bootstrap_ci([r['fde_persistence'] for r in rows]),'fallback_rate':fallback_rate([r['fallback'] for r in rows]),'safety_violation_rate':safety_violation_rate([r['safety_violation'] for r in rows]),'vanilla_transformer_artifact':'vanilla_transformer.json','failure_notes':'UCI pedestrian traffic alternative; open-loop trajectory forecast, no vehicle control or collision guarantee'}; (out/'config.json').write_text(json.dumps({'observed_steps':8,'predicted_steps':12,'split':'track-level 60/20/20','source':'UCI pedestrian in traffic','license':'CC BY 4.0'},indent=2)); (out/'trajectory_metrics.json').write_text(json.dumps(rows,indent=2)); (out/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
