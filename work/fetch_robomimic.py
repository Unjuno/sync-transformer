"""Fetch a small RoboMimic low-dimensional demonstration file atomically."""
import argparse,hashlib,os,tempfile
from pathlib import Path
from urllib.request import urlopen
URL='https://huggingface.co/datasets/amandlek/robomimic/resolve/main/v1.5/lift/ph/low_dim_v15.hdf5?download=true'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='data/raw/robomimic_lift_ph_low_dim_v15.hdf5'); a=ap.parse_args(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); fd,tmp=tempfile.mkstemp(prefix=out.name+'.',suffix='.part',dir=out.parent); h=hashlib.sha256(); n=0
    try:
        with os.fdopen(fd,'wb') as dst, urlopen(URL,timeout=120) as src:
            while chunk:=src.read(1024*1024): dst.write(chunk); h.update(chunk); n+=len(chunk)
        os.replace(tmp,out); print({'output':str(out),'bytes':n,'sha256':h.hexdigest(),'source':URL})
    except Exception:
        if os.path.exists(tmp): os.unlink(tmp)
        raise
if __name__=='__main__': main()
