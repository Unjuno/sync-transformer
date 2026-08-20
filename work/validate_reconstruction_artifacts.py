"""Validate condition-keyed common-runner artifacts before reporting them."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'outputs'
required={'dataset','seed','P','H','query_step','candidate_step','width','candidate_count','base_head_mse','external_residual_mse','paired_delta_external_minus_head'}
def main():
 files=sorted(OUT.glob('common_runner_*.json')); errors=[]; checked=0
 for p in files:
  d=json.loads(p.read_text()); rows=d.get('rows',[])
  if not rows: errors.append(f'{p.name}: no rows'); continue
  for r in rows:
   checked+=1; missing=required-set(r)
   if missing: errors.append(f'{p.name}: missing {sorted(missing)}')
   if len(r.get('paired_delta_external_minus_head',[])) != r.get('test_queries',len(r.get('paired_delta_external_minus_head',[]))): errors.append(f'{p.name}: delta length mismatch')
 print(json.dumps({'passed':not errors,'files':len(files),'rows':checked,'errors':errors},indent=2))
 if errors: raise SystemExit(1)
if __name__=='__main__': main()
