import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_run_task_reports_pending_candidate(tmp_path):
    out = tmp_path / "summary.json"
    subprocess.run([sys.executable, "-m", "sync_experiments.run_task",
                    "--task", "traffic", "--output", str(out)],
                   cwd=ROOT, check=True, capture_output=True, text=True)
    record = json.loads(out.read_text(encoding="utf-8"))
    assert record["status"] == "source_verified_pending_data"
    assert record["task_id"] == "traffic"

def test_run_task_reports_electricity_artifacts(tmp_path):
    out = tmp_path / "summary.json"
    subprocess.run([sys.executable, "-m", "sync_experiments.run_task",
                    "--task", "electricity", "--output", str(out)],
                   cwd=ROOT, check=True, capture_output=True, text=True)
    record = json.loads(out.read_text(encoding="utf-8"))
    assert record["status"] == "completed_existing"
    assert len(record["artifacts"]) >= 6
