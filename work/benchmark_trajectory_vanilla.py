"""Vanilla Transformer trajectory baseline on the UCI pedestrian alternative."""
import json, time
import sys
from pathlib import Path
import numpy as np, pandas as pd, torch
from torch import nn
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from sync_experiments.trajectory_metrics import ade,fde,bootstrap_ci
def windows():
 d=pd.read_csv(ROOT/'data'/'raw'/'uci_pedestrian'/'pedestrian_traffic_data'/'tracks.csv'); a=[]
 for oid,g in d.groupby('oid'):
  z=g.sort_values('timestamp')[['x','y']].to_numpy(float)
  for i in range(0,len(z)-20+1,2): a.append((str(oid),z[i:i+8],z[i+8:i+20]))
 ds=sorted({x[0] for x in a}); n=len(ds); tr=set(ds[:max(1,int(.6*n))]); te=set(ds[max(2,int(.8*n)):]); return [(x[1],x[2]) for x in a if x[0] in tr],[(x[1],x[2]) for x in a if x[0] in te]
class Model(nn.Module):
 def __init__(self):
  super().__init__(); self.inp=nn.Linear(2,32); layer=nn.TransformerEncoderLayer(32,4,64,batch_first=True); self.enc=nn.TransformerEncoder(layer,2); self.out=nn.Linear(32,24)
 def forward(self,x): return self.out(self.enc(self.inp(x))[:,-1]).view(-1,12,2)
def main():
 tr,te=windows(); allxy=np.concatenate([np.concatenate([x,y]) for x,y in tr]); mu=allxy.mean(0); sd=allxy.std(0)+1e-6; X=torch.tensor(np.stack([(x-mu)/sd for x,y in tr]),dtype=torch.float32); Y=torch.tensor(np.stack([(y-mu)/sd for x,y in tr]),dtype=torch.float32); Xt=torch.tensor(np.stack([(x-mu)/sd for x,y in te]),dtype=torch.float32); Yt=np.stack([y for x,y in te]); results=[]
 for seed in [163,164,165]:
  torch.manual_seed(seed); m=Model(); opt=torch.optim.Adam(m.parameters(),lr=2e-3); t=time.perf_counter()
  for _ in range(20): opt.zero_grad(); loss=((m(X)-Y)**2).mean(); loss.backward(); opt.step()
  with torch.no_grad():
   ti=time.perf_counter(); pred=m(Xt).numpy()*sd+mu; infer_ms=(time.perf_counter()-ti)*1000/max(1,len(te))
  results.append({'seed':seed,'ade':ade(pred,Yt),'fde':fde(pred,Yt),'parameter_count':sum(p.numel() for p in m.parameters()),'elapsed_seconds':time.perf_counter()-t,'inference_latency_ms_per_query':infer_ms})
 out=ROOT/'outputs'/'benchmark_runs'/'robot_trajectory'/'uci_pedestrian'; payload={'model':'vanilla_transformer_trajectory','rows':results,'ade':bootstrap_ci([x['ade'] for x in results]),'fde':bootstrap_ci([x['fde'] for x in results])}; (out/'vanilla_transformer.json').write_text(json.dumps(payload,indent=2)); print(json.dumps(payload,indent=2))
if __name__=='__main__': main()
