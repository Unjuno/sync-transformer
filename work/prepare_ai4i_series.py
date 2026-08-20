"""Materialize the UCI AI4I industrial sensor alternative."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
    d=pd.read_csv(ROOT/'data'/'raw'/'ai4i2020.csv')
    y=pd.to_numeric(d['Process temperature [K]'],errors='coerce')
    pd.DataFrame({'date':range(len(y)),'OT':y.astype('float32')}).to_csv(ROOT/'outputs'/'AI4I_process_temperature.csv',index=False)
    print({'rows':len(y)})
if __name__=='__main__': main()
