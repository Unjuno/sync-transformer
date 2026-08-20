"""Small, reproducible RoboMimic trajectory benchmark.

SYNC formulation here is explicit: nearest-context retrieval from prior demonstrations;
it is not conflated with the scalar forecasting runner.  A distance gate falls back to
persistence and all trajectory metrics are reported separately.
"""
import json
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from sync_experiments.adapters import RoboMimicAdapter
from sync_experiments.trajectory_metrics import ade, fde, bootstrap_ci, fallback_rate, safety_violation_rate

def main():
    batches=RoboMimicAdapter(ROOT/'data'/'raw', filename='robomimic_lift_ph_low_dim_v15.hdf5').load_trajectory(context_length=10,horizon=10,step=10)
    by_demo={}
    for b in batches: by_demo.setdefault(b.metadata['demo'],[]).append(b)
    demos=sorted(by_demo); n=len(demos); train=set(demos[:max(1,int(.6*n))]); cal=set(demos[max(1,int(.6*n)):max(2,int(.8*n))]); test=set(demos[max(2,int(.8*n)):])
    train_b=[b for b in batches if b.metadata['demo'] in train]; cal_b=[b for b in batches if b.metadata['demo'] in cal]; test_b=[b for b in batches if b.metadata['demo'] in test]
    dcal=[]
    for b in cal_b:
        dcal.append(min(float(np.linalg.norm(b.observed[-1]-x.observed[-1])) for x in train_b))
    threshold=float(np.quantile(dcal,.95)) if dcal else float('inf')
    # conservative displacement envelope learned from training futures
    dis=np.concatenate([np.linalg.norm(np.diff(np.vstack([b.observed[-1:],b.future]),axis=0),axis=1) for b in train_b])
    safety_limit=float(np.quantile(dis,.999)) if dis.size else float('inf')
    rows=[]
    for b in test_b:
        nearest=min(train_b,key=lambda x: float(np.linalg.norm(b.observed[-1]-x.observed[-1])))
        dist=float(np.linalg.norm(b.observed[-1]-nearest.observed[-1])); fallback=dist>threshold
        pred=np.repeat(b.observed[-1][None,:],len(b.future),axis=0) if fallback else nearest.future
        violation=bool(np.any(np.linalg.norm(np.diff(np.vstack([b.observed[-1:],pred]),axis=0),axis=1)>safety_limit))
        rows.append({'demo':b.metadata['demo'],'ade_sync':ade(pred,b.future),'fde_sync':fde(pred,b.future),'tracking_error_sync':ade(pred,b.future),'open_loop_success_sync':bool(np.linalg.norm(pred[-1]-b.future[-1])<=0.05),'ade_persistence':ade(np.repeat(b.observed[-1][None,:],len(b.future),axis=0),b.future),'fde_persistence':fde(np.repeat(b.observed[-1][None,:],len(b.future),axis=0),b.future),'fallback':fallback,'safety_violation':violation,'distance':dist})
    out=ROOT/'outputs'/'benchmark_runs'/'robot_manipulation'/'robomimic_lift_ph'; out.mkdir(parents=True,exist_ok=True)
    summary={'task_id':'robot_manipulation','dataset':'robomimic_lift_ph','status':'measured_alternative','n_train':len(train_b),'n_calibration':len(cal_b),'n_test':len(test_b),'sync_ade':bootstrap_ci([r['ade_sync'] for r in rows]),'sync_fde':bootstrap_ci([r['fde_sync'] for r in rows]),'tracking_error':bootstrap_ci([r['tracking_error_sync'] for r in rows]),'open_loop_success_rate':float(np.mean([r['open_loop_success_sync'] for r in rows])),'persistence_ade':bootstrap_ci([r['ade_persistence'] for r in rows]),'persistence_fde':bootstrap_ci([r['fde_persistence'] for r in rows]),'fallback_rate':fallback_rate([r['fallback'] for r in rows]),'safety_violation_rate':safety_violation_rate([r['safety_violation'] for r in rows]),'gate_threshold':threshold,'safety_limit':safety_limit,'failure_notes':'nearest-context retrieval SYNC formulation; success is open-loop endpoint tolerance <=0.05m, not closed-loop control'}
    (out/'config.json').write_text(json.dumps({'context_length':10,'horizon':10,'split':'demo-level 60/20/20','source':'RoboMimic lift ph low_dim'},indent=2)); (out/'trajectory_metrics.json').write_text(json.dumps(rows,indent=2)); (out/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
