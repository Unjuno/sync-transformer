"""Orchestrate the ten-task benchmark without bundling raw data.

Phase A executes the validated ETT CPU suite. Other task adapters fail loudly
with an actionable message until their licensed data and adapter are present.
"""
import argparse, json, subprocess, sys
from pathlib import Path
from .tasks import TASKS, get_task

ROOT = Path(__file__).resolve().parent.parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="ett")
    ap.add_argument("--track", choices=("all", "forecasting", "trajectory"), default="all")
    ap.add_argument("--seeds", default="163,164,165")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    ap.add_argument("--output", default="outputs/benchmark_runs")
    args = ap.parse_args()
    requested = [t.task_id for t in TASKS if (args.tasks == "all" or t.task_id in args.tasks.split(",")) and (args.track == "all" or t.track == args.track)]
    if not requested:
        raise SystemExit("no tasks selected")
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    records = []
    for task_id in requested:
        task = get_task(task_id)
        record = {"task_id": task.task_id, "track": task.track, "dataset": task.dataset, "status": task.status}
        if task_id != "ett":
            record.update({"status": "pending_adapter", "message": "Provide licensed data and implement the declared adapter before running."})
        elif args.device != "cpu":
            record.update({"status": "deferred_cuda", "message": "CUDA execution is reserved for the separate GPU machine."})
        else:
            subprocess.run([sys.executable, "work/run_canonical_suite.py"], cwd=ROOT, check=True)
            record.update({"status": "completed", "artifact": "outputs/common_runner_*.json"})
        (out / f"{task_id}.json").write_text(json.dumps(record, indent=2))
        records.append(record)
    (out / "run_manifest.json").write_text(json.dumps({"tasks": records, "seeds": args.seeds, "epochs": args.epochs, "device": args.device}, indent=2))
    print(json.dumps(records, indent=2))

if __name__ == "__main__":
    main()
