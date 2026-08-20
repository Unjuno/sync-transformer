"""Materialize Microsoft Cloud Monitoring consumer purchase counts as retail demand."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
 parts=[]
 for p in sorted((ROOT/'data'/'raw'/'cloud-monitoring'/'data'/'consumer-purchase-rate').glob('*.csv')):
  d=pd.read_csv(p); parts.append(pd.DataFrame({'date':d.TimeStamp.astype(str),'OT':pd.to_numeric(d.Value,errors='coerce').interpolate(limit=3,limit_direction='both')}))
 out=pd.concat(parts,ignore_index=True); out.to_csv(ROOT/'outputs'/'CloudMonitoring_consumer_purchase.csv',index=False); print({'rows':len(out),'series':len(parts)})
if __name__=='__main__': main()
