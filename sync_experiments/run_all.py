"""Orchestrate the ten-task benchmark without bundling raw data.

Phase A executes the validated ETT CPU suite. Other task adapters fail loudly
with an actionable message until their licensed data and adapter are present.
"""
import argparse, json, subprocess, sys
from pathlib import Path
from .tasks import TASKS, get_task
from .adapters import adapter_for, AdapterNotReady

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
        adapter = adapter_for(task_id, ROOT / "outputs")
        if task_id not in ("ett", "electricity"):
            try:
                if task_id == "hvac":
                    adapter.load(context_length=720, horizon=96, step=96)
                    record.update({"status": "source_verified_adapter_ready", "message": "BDG2 CSV adapter validated; model benchmark not yet run."})
                else:
                    adapter.load()
            except AdapterNotReady as exc:
                source_statuses = {"blocked_source_unavailable", "source_public_license_unresolved", "source_verified_pending_adapter"}
                record.update({"status": task.status if task.status in source_statuses else "pending_adapter", "message": str(exc)})
        elif args.device != "cpu":
            record.update({"status": "deferred_cuda", "message": "CUDA execution is reserved for the separate GPU machine."})
        elif task_id == "electricity":
            artifacts = sorted(ROOT.glob("outputs/common_runner_Electricity*_q96_c48_lbfull_k8_rich0_end_sf_vg0.079168.json"))
            vanilla = sorted(ROOT.glob("outputs/vanilla_Electricity*_20.json"))
            base_vanilla = ROOT / "outputs/vanilla_Electricity20.json"
            if base_vanilla.exists():
                vanilla.append(base_vanilla)
            if artifacts and vanilla:
                record.update({"status": "completed_existing", "artifacts": [str(p) for p in artifacts + vanilla]})
                # Export the documented per-client files from the immutable run artifacts.
                for artifact in artifacts:
                    token = "MT002" if "MT002" in artifact.name else "MT003" if "MT003" in artifact.name else "MT001"
                    client = {"MT001":"MT_001", "MT002":"MT_002", "MT003":"MT_003"}[token]
                    vname = f"vanilla_Electricity_{token}_20.json" if token != "MT001" else "vanilla_Electricity20.json"
                    vpath = ROOT / "outputs" / vname
                    if vpath.exists():
                        subprocess.run([sys.executable, "work/export_electricity_task.py", "--client", client, "--sync", str(artifact), "--vanilla", str(vpath), "--output", str(out / "electricity" / client)], cwd=ROOT, check=True)
            else:
                record.update({"status": "pending_adapter", "message": "Run work/prepare_electricity.py and the electricity benchmark commands first."})
        else:
            subprocess.run([sys.executable, "work/run_canonical_suite.py"], cwd=ROOT, check=True)
            record.update({"status": "completed", "artifact": "outputs/common_runner_*.json"})
        # Keep the historical flat record and also emit the documented task layout.
        (out / f"{task_id}.json").write_text(json.dumps(record, indent=2))
        task_out = out / task_id
        task_out.mkdir(parents=True, exist_ok=True)
        (task_out / "config.json").write_text(json.dumps({"task_id": task_id, "seeds": args.seeds, "epochs": args.epochs, "device": args.device}, indent=2))
        (task_out / "summary.json").write_text(json.dumps(record, indent=2))
        records.append(record)
    (out / "run_manifest.json").write_text(json.dumps({"tasks": records, "seeds": args.seeds, "epochs": args.epochs, "device": args.device}, indent=2))
    print(json.dumps(records, indent=2))

if __name__ == "__main__":
    main()
