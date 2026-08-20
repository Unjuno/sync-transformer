"""Fetch one BDG2 LFS blob without accepting partial or unverified data."""
import argparse, hashlib, os, tempfile
from pathlib import Path
from urllib.request import urlopen

URL = "https://media.githubusercontent.com/media/buds-lab/building-data-genome-project-2/master/data/meters/cleaned/electricity_cleaned.csv"
EXPECTED_SHA256 = "b6ffc9b4dfcefe5c753594730a08ae822b0d50fec6815abb8f185591e6c630a3"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output', default='data/raw/bdg2_electricity_cleaned.csv'); a=ap.parse_args()
    out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=out.name+'.', suffix='.part', dir=out.parent)
    digest=hashlib.sha256(); size=0
    try:
        with os.fdopen(fd, 'wb') as dst, urlopen(URL, timeout=60) as src:
            while chunk := src.read(1024*1024):
                dst.write(chunk); digest.update(chunk); size += len(chunk)
        actual=digest.hexdigest()
        if actual != EXPECTED_SHA256:
            raise RuntimeError(f"checksum mismatch: got {actual}, expected {EXPECTED_SHA256}; partial file rejected")
        os.replace(tmp, out)
        print({'output': str(out), 'bytes': size, 'sha256': actual})
    except Exception:
        if os.path.exists(tmp): os.unlink(tmp)
        raise
if __name__=='__main__': main()
