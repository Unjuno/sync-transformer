"""Materialize Microsoft Cloud Monitoring MongoDB machine RPS series."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
 d=pd.read_csv(ROOT/'data'/'raw'/'cloud-monitoring'/'data'/'mongodb-machine-rps'/'machine-01.csv'); y=pd.to_numeric(d.Value,errors='coerce').interpolate(limit=3,limit_direction='both'); pd.DataFrame({'date':d.TimeStamp.astype(str),'OT':y.astype('float32')}).to_csv(ROOT/'outputs'/'CloudMonitoring_machine_rps.csv',index=False); print({'rows':len(y)})
if __name__=='__main__': main()
