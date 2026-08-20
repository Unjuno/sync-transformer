"""Common-protocol SYNC_CORE reconstruction runner.

This is deliberately a transparent reconstruction, not a claim of reproducing
the missing original implementation. All methods share P/H, split, queries,
candidate futures, optimizer budget, and normalized MSE.
"""
import argparse, json, random
from pathlib import Path
import numpy as np, pandas as pd, torch
from torch import nn

ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'outputs'
def seed(s):
 random.seed(s); np.random.seed(s); torch.manual_seed(s)
 # Keep CPU reductions reproducible across repeated runs of the common protocol.
 torch.use_deterministic_algorithms(True)
 torch.set_num_threads(1)
class Head(nn.Module):
 def __init__(self,d,h,in_features=30):
  super().__init__(); self.q=nn.Sequential(nn.Linear(in_features,d),nn.Tanh(),nn.Linear(d,d)); self.head=nn.Linear(d,h)
 def forward(self,x):
  q=self.q(x); return self.head(q),q
def run(ds='ETTm1',seed_value=163,step=96,width=80,epochs=100,hier=False,candidate_step=None,rich=False,final_k=4,lookback=None,vol_gate_threshold=None,train_frac=.6,cal_frac=.8,combine_gates=False,endpoint_features=False,seasonal_features=False,seasonal_base=False,multiscale_features=False,eval_start_frac=None,eval_end_frac=None):
 seed(seed_value); y=pd.read_csv(OUT/f'{ds}.csv').OT.to_numpy(np.float32); n=len(y); tr=int(train_frac*n); ca=int(cal_frac*n)
 mu,sd=y[:tr].mean(),y[:tr].std(); z=(y-mu)/(sd+1e-8); P,H=(720,24) if ds.startswith('ETTh') else (720,96)
 # use 30 fixed patches; candidates end before every query and remain disjoint by H
 def feat(t):
  u=z[t-P:t].reshape(30,-1)
  if multiscale_features:
   f=np.r_[u.mean(1), u.reshape(15,2,-1).mean((1,2)), u.reshape(5,6,-1).mean((1,2))]
   return f
  if endpoint_features:
   f=np.r_[u.mean(1), u[:,-1]]
   if seasonal_features: f=np.r_[f, z[t-step], z[t-2*step]]
   return f
  return np.r_[u.mean(1),u.std(1)] if rich else u.mean(1)
 if candidate_step is None: candidate_step=step
 # Keep forecast-head training queries fixed; vary only the candidate bank.
 train_e=np.arange(P,tr-H+1,step); X=torch.tensor(np.stack([feat(t) for t in train_e])); Y=torch.tensor(np.stack([z[t:t+H] for t in train_e]));
 cstart=P if lookback is None else max(P,tr-int(lookback)); e=np.arange(cstart,tr-H+1,candidate_step); C=torch.tensor(np.stack([feat(t) for t in e])); F=torch.tensor(np.stack([z[t:t+H] for t in e]));
 cv=np.arange(tr,ca,step); tx=torch.tensor(np.stack([feat(t) for t in cv])); cy=np.stack([z[t:t+H] for t in cv])
 eval_start=ca if eval_start_frac is None else max(ca,int(eval_start_frac*n))
 eval_end=n if eval_end_frac is None else min(n,int(eval_end_frac*n))
 te=np.arange(eval_start,eval_end-H+1,step); qx=torch.tensor(np.stack([feat(t) for t in te])); qy=np.stack([z[t:t+H] for t in te])
 din=X.shape[1]
 m=Head(width,H,din) if not rich else nn.Module()
 if rich:
  class RichHead(nn.Module):
   def __init__(self):
    super().__init__();self.q=nn.Sequential(nn.Linear(din,width),nn.Tanh(),nn.Linear(width,width));self.head=nn.Linear(width,H)
   def forward(self,x):
    q=self.q(x);return self.head(q),q
  m=RichHead()
 opt=torch.optim.AdamW(m.parameters(),lr=3e-3,weight_decay=1e-4); loss=nn.MSELoss()
 for _ in range(epochs):
  opt.zero_grad(); p,_=m(X); loss(p,Y).backward(); opt.step()
 with torch.no_grad(): base,_=m(qx); cb,_=m(tx)
 if seasonal_base:
  base=torch.tensor(np.stack([z[t-step:t-step+H] for t in te]),dtype=torch.float32)
  cb=torch.tensor(np.stack([z[t-step:t-step+H] for t in cv]),dtype=torch.float32)
 # candidate bank is train futures, with a causal H gap from calibration/test query
 candidates=C.numpy();
 def transport(q):
  dist=((q[:,None,:]-C[None,:,:])**2).mean(-1); scores=-dist; k=min(12,len(e)); coarse=torch.topk(scores,k,1).indices
  kk=min(final_k,k); chosen=torch.gather(coarse,1,torch.topk(torch.gather(scores,1,coarse),kk,1).indices)
  mask=torch.full_like(scores,float('-inf')); mask.scatter_(1,chosen,torch.gather(scores,1,chosen)); w=torch.softmax(mask,1)
  return (w[:,:,None]*F[None,:,:]).sum(1),w,dist.min(1).values
 with torch.no_grad(): cc,cw,qd=transport(qx); tc,tw,cd=transport(tx); test_corr,test_w,td=transport(qx)
 # calibrate residual scale and use same scale for all test queries
 alpha_grid=np.linspace(-.4,.8,49); best=(1e9,0.)
 for a in alpha_grid:
  v=float(np.mean((cb.numpy()+a*tc.numpy()-cy)**2))
  if v<best[0]: best=(v,float(a))
 a=best[1]; base_np=base.numpy(); corr_np=test_corr.numpy(); truth=qy
 # Calibrate an abstention threshold using calibration queries only.
 # Fit gate on the first half of calibration to reduce threshold overfit.
 mid=max(1,len(cd)//2); fit_d=cd.numpy()[:mid]; fit_cy=cy[:mid]; fit_cb=cb.numpy()[:mid]; fit_tc=tc.numpy()[:mid]
 val_d=cd.numpy()[mid:]; val_cy=cy[mid:]; val_cb=cb.numpy()[mid:]; val_tc=tc.numpy()[mid:]
 cal_d=fit_d; thresholds=np.unique(np.r_[np.quantile(cal_d,np.linspace(0,1,21)),np.inf]); gate_best=(1e9,float(thresholds[-1]))
 for th in thresholds:
  use=val_d<=th; pp=np.where(use[:,None],val_cb+a*val_tc,val_cb); v=float(np.mean((pp-val_cy)**2)) if len(val_d) else float('inf')
  if v<gate_best[0]: gate_best=(v,float(th))
 gate_threshold=gate_best[1]; use_test=td.numpy()<=gate_threshold
 if vol_gate_threshold is not None:
  vol_test=np.asarray([np.std(np.diff(z[t-P:t])) for t in te])<=float(vol_gate_threshold)
  use_test = (use_test & vol_test) if combine_gates else vol_test
 ext=np.where(use_test[:,None],base_np+a*corr_np,base_np); head_mse=np.mean((base_np-truth)**2,1); ext_mse=np.mean((ext-truth)**2,1)
 raw=np.mean((test_corr.numpy()-truth)**2,1); persistence=np.mean((np.repeat(z[te-1,None],H,1)-truth)**2,1)
 cal_head_q=np.mean((cb.numpy()-cy)**2,1); cal_ext_q=np.mean((cb.numpy()+a*tc.numpy()-cy)**2,1)
 cal_reg=np.asarray([np.std(np.diff(z[t-P:t])) for t in cv]); test_reg=np.asarray([np.std(np.diff(z[t-P:t])) for t in te])
 raw_q=np.mean((test_corr.numpy()-truth)**2,1)
 r={'dataset':ds,'seed':seed_value,'P':P,'H':H,'query_step':step,'candidate_step':candidate_step,'final_k':final_k,'width':width,'hierarchical':hier,'candidate_count':len(e),'train_queries':len(e),'calibration_queries':len(cv),'test_queries':len(te),'parameter_count':sum(p.numel() for p in m.parameters()),'alpha':a,'calibration_head_mse':float(cal_head_q.mean()),'calibration_external_mse':float(cal_ext_q.mean()),'calibration_head_query_mse':cal_head_q.tolist(),'calibration_external_query_mse':cal_ext_q.tolist(),'calibration_distance':cd.numpy().tolist(),'test_distance':td.numpy().tolist(),'calibration_regime_volatility':cal_reg.tolist(),'test_regime_volatility':test_reg.tolist(),'gate':'nearest_distance_calibrated','gate_threshold':gate_threshold,'gate_use_rate':float(use_test.mean()),'base_head_mse':float(head_mse.mean()),'external_residual_mse':float(ext_mse.mean()),'raw_transport_mse':float(raw_q.mean()),'raw_transport_query_mse':raw_q.tolist(),'persistence_mse':float(persistence.mean()),'head_query_mse':head_mse.tolist(),'external_query_mse':ext_mse.tolist(),'paired_delta_external_minus_head':(ext_mse-head_mse).tolist()}
 return r
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--dataset',default='ETTm1'); ap.add_argument('--seeds',default='163,164,165'); ap.add_argument('--step',type=int,default=96); ap.add_argument('--candidate-step',type=int,default=None); ap.add_argument('--lookback',type=int,default=None); ap.add_argument('--width',type=int,default=80); ap.add_argument('--epochs',type=int,default=100); ap.add_argument('--rich',action='store_true'); ap.add_argument('--endpoint-features',action='store_true'); ap.add_argument('--seasonal-features',action='store_true'); ap.add_argument('--seasonal-base',action='store_true'); ap.add_argument('--multiscale-features',action='store_true'); ap.add_argument('--k',type=int,default=4); ap.add_argument('--vol-gate-threshold',type=float,default=None); ap.add_argument('--combine-gates',action='store_true'); ap.add_argument('--train-frac',type=float,default=.6); ap.add_argument('--cal-frac',type=float,default=.8); ap.add_argument('--eval-start-frac',type=float,default=None); ap.add_argument('--eval-end-frac',type=float,default=None); args=ap.parse_args()
 rows=[run(args.dataset,int(s),args.step,args.width,args.epochs,candidate_step=args.candidate_step,rich=args.rich,final_k=args.k,lookback=args.lookback,vol_gate_threshold=args.vol_gate_threshold,train_frac=args.train_frac,cal_frac=args.cal_frac,combine_gates=args.combine_gates,endpoint_features=args.endpoint_features,seasonal_features=args.seasonal_features,seasonal_base=args.seasonal_base,multiscale_features=args.multiscale_features,eval_start_frac=args.eval_start_frac,eval_end_frac=args.eval_end_frac) for s in args.seeds.split(',')]; out={'protocol':'common reconstruction; not original code','rich_features':args.rich,'endpoint_features':args.endpoint_features,'seasonal_features':args.seasonal_features,'seasonal_base':args.seasonal_base,'multiscale_features':args.multiscale_features,'final_k':args.k,'lookback':args.lookback,'vol_gate_threshold':args.vol_gate_threshold,'combine_gates':args.combine_gates,'train_frac':args.train_frac,'cal_frac':args.cal_frac,'eval_start_frac':args.eval_start_frac,'eval_end_frac':args.eval_end_frac,'rows':rows}; lb='full' if args.lookback is None else str(args.lookback); cs=str(args.candidate_step or args.step); vg='' if args.vol_gate_threshold is None else f'_vg{args.vol_gate_threshold:g}'; cg='_and' if args.combine_gates else ''; split='' if (args.train_frac,args.cal_frac)==(.6,.8) else f'_tr{args.train_frac:g}_ca{args.cal_frac:g}'; wt='' if args.width==80 else f'_w{args.width}'; ep='_end' if args.endpoint_features else ''; sf='_sf' if args.seasonal_features else ''; sb='_sb' if args.seasonal_base else ''; ms='_ms' if args.multiscale_features else ''; ev='' if args.eval_start_frac is None else f'_ev{args.eval_start_frac:g}-{args.eval_end_frac:g}'; tag=f'{args.dataset}_q{args.step}_c{cs}_lb{lb}_k{args.k}_rich{int(args.rich)}{ep}{sf}{sb}{ms}{wt}{vg}{cg}{split}{ev}'; p=OUT/f'common_runner_{tag}.json'; p.write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
