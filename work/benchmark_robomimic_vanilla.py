"""Vanilla Transformer trajectory baseline for RoboMimic lift/ph."""
import json,sys,time
from pathlib import Path
import numpy as np, torch
from torch import nn
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from sync_experiments.adapters import RoboMimicAdapter
from sync_experiments.trajectory_metrics import ade,fde,bootstrap_ci
class M(nn.Module):
 def __init__(self,d):
  super().__init__();self.i=nn.Linear(d,32);self.e=nn.TransformerEncoder(nn.TransformerEncoderLayer(32,4,64,batch_first=True),2);self.o=nn.Linear(32,10*d)
 def forward(self,x):return self.o(self.e(self.i(x))[:,-1]).view(-1,10,x.shape[-1])
def main():
 b=RoboMimicAdapter(ROOT/'data'/'raw',filename='robomimic_lift_ph_low_dim_v15.hdf5').load_trajectory(context_length=10,horizon=10,step=10); ds=sorted({x.metadata['demo'] for x in b});n=len(ds);tr=set(ds[:int(.6*n)]);te=set(ds[int(.8*n):]);a=[x for x in b if x.metadata['demo'] in tr];z=[x for x in b if x.metadata['demo'] in te];mu=np.concatenate([x.observed for x in a]+[x.future for x in a]).mean(0);sd=np.concatenate([x.observed for x in a]+[x.future for x in a]).std(0)+1e-6;X=torch.tensor(np.stack([(x.observed-mu)/sd for x in a]),dtype=torch.float32);Y=torch.tensor(np.stack([(x.future-mu)/sd for x in a]),dtype=torch.float32);Xt=torch.tensor(np.stack([(x.observed-mu)/sd for x in z]),dtype=torch.float32);YT=np.stack([x.future for x in z]);rows=[]
 for seed in [163,164,165]:
  torch.manual_seed(seed);m=M(X.shape[-1]);o=torch.optim.Adam(m.parameters(),lr=2e-3);t=time.perf_counter()
  for _ in range(20):o.zero_grad();l=((m(X)-Y)**2).mean();l.backward();o.step()
  with torch.no_grad():p=m(Xt).numpy()*sd+mu
  rows.append({'seed':seed,'ade':ade(p,YT),'fde':fde(p,YT),'parameter_count':sum(q.numel() for q in m.parameters()),'elapsed_seconds':time.perf_counter()-t})
 out=ROOT/'outputs'/'benchmark_runs'/'robot_manipulation'/'robomimic_lift_ph';(out/'vanilla_transformer.json').write_text(json.dumps({'model':'vanilla_transformer_trajectory','rows':rows,'ade':bootstrap_ci([x['ade'] for x in rows]),'fde':bootstrap_ci([x['fde'] for x in rows])},indent=2));print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
