"""Materialize the first numeric METR-LA sensor for the common runner."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
    src=ROOT/'data/raw/METR-LA.csv'; frame=pd.read_csv(src, nrows=32); cols=[c for c in frame.columns if pd.to_numeric(frame[c],errors='coerce').notna().any()]
    if not cols: raise ValueError('no numeric traffic sensor')
    col=cols[0]; full=pd.read_csv(src,usecols=[col]); y=pd.to_numeric(full[col],errors='coerce').interpolate(limit_direction='both')
    out=ROOT/'outputs'/'METR_LA_sensor0.csv'; pd.DataFrame({'date':range(len(y)),'OT':y.astype('float32')}).to_csv(out,index=False); print({'column':col,'rows':len(y),'output':str(out)})
if __name__=='__main__': main()
