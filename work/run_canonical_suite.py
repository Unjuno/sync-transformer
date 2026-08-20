"""Regenerate the four deterministic canonical SYNC artifacts."""
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
configs=[('ETTh1',24,8),('ETTh2',24,8),('ETTm1',96,48),('ETTm2',96,48)]
for ds,step,cstep in configs:
 cmd=[sys.executable,'work/sync_core_runner.py','--dataset',ds,'--seeds','163,164,165','--step',str(step),'--candidate-step',str(cstep),'--width','80','--k','8','--epochs','20','--endpoint-features','--seasonal-features','--vol-gate-threshold','0.079168']
 print('RUN',' '.join(cmd)); subprocess.run(cmd,cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
subprocess.run([sys.executable,'work/run_pooled_gate.py'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'work/build_reproducibility_manifest.py'],cwd=ROOT,check=True)
print('canonical suite complete')
