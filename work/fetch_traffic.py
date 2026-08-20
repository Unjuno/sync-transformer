"""Fetch the CC-BY-4.0 Zenodo METR-LA CSV atomically."""
import argparse, hashlib, os, tempfile
from pathlib import Path
from urllib.request import urlopen
URL='https://zenodo.org/api/records/5146275/files/METR-LA.csv/content'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='data/raw/METR-LA.csv'); a=ap.parse_args(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=out.name+'.',suffix='.part',dir=out.parent); h=hashlib.sha256(); n=0
    try:
        with os.fdopen(fd,'wb') as dst, urlopen(URL,timeout=120) as src:
            while chunk:=src.read(1024*1024): dst.write(chunk); h.update(chunk); n+=len(chunk)
        os.replace(tmp,out); print({'output':str(out),'bytes':n,'sha256':h.hexdigest(),'source':URL,'license':'CC BY 4.0'})
    except Exception:
        if os.path.exists(tmp): os.unlink(tmp)
        raise
if __name__=='__main__': main()
