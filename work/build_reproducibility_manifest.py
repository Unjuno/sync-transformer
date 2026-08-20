"""Hash the scripts and canonical evidence artifacts used in the paper handoff."""
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'outputs'; WORK=ROOT/'work'
paths=[WORK/'sync_core_runner.py',WORK/'bootstrap_endpoint_features.py',WORK/'bootstrap_raw_vs_sync.py',WORK/'validate_reconstruction_artifacts.py',WORK/'audit_public_sync.py',OUT/'SYNC_Transformer_paper_handoff.md',OUT/'SYNC_Transformer_canonical_results_table.md',OUT/'endpoint_feature_bootstrap.json',OUT/'raw_vs_sync_bootstrap.json',OUT/'seasonal_baseline_summary.json',OUT/'paper_evidence_summary.json']
rows=[]
for p in paths:
 h=hashlib.sha256(p.read_bytes()).hexdigest(); rows.append({'path':str(p.relative_to(ROOT)),'sha256':h,'bytes':p.stat().st_size})
manifest={'protocol':'SYNC Transformer paper handoff reproducibility manifest','files':rows}
(OUT/'SYNC_Transformer_reproducibility_manifest.json').write_text(json.dumps(manifest,indent=2)); print(json.dumps(manifest,indent=2))
