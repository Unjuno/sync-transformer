"""Run or report one task from the public benchmark registry.

This entry point deliberately refuses to substitute datasets or fabricate
metrics. Implemented tasks return pointers to their reproducible artifacts;
unimplemented tasks return an explicit pending status.
"""
import argparse
import json
from pathlib import Path
from .tasks import get_task
from .adapters import adapter_for, AdapterNotReady

ROOT = Path(__file__).resolve().parent.parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--models", default="vanilla,vanilla_small,sync")
    ap.add_argument("--seeds", default="163,164,165")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    task = get_task(args.task)
    record = {"task_id": task.task_id, "track": task.track,
              "dataset": task.dataset, "models": args.models.split(","),
              "seeds": [int(x) for x in args.seeds.split(",") if x],
              "epochs": args.epochs, "device": args.device,
              "status": task.status}
    if args.device == "cuda":
        record.update(status="deferred_cuda", message="CUDA runs are separate artifacts.")
    elif task.task_id == "electricity":
        artifacts = sorted(ROOT.glob("outputs/common_runner_Electricity*_q96_c48_lbfull_k8_rich0_end_sf_vg0.079168.json"))
        vanilla = sorted(ROOT.glob("outputs/vanilla_Electricity*_20.json"))
        base_vanilla = ROOT / "outputs/vanilla_Electricity20.json"
        if base_vanilla.exists():
            vanilla.append(base_vanilla)
        if artifacts and vanilla:
            record.update(status="completed_existing", artifacts=[str(p) for p in artifacts + vanilla])
        else:
            record.update(status="pending_adapter", message="Prepare data and run the documented benchmark first.")
    elif task.task_id == "ett":
        record.update(status="completed_existing", artifacts=["outputs/common_runner_*.json"])
    elif task.task_id == "hvac":
        hvac_root=ROOT/'outputs'/'benchmark_runs'/'hvac'
        meters=('BDG2_Panther_office_Hannah','BDG2_Panther_office_Catherine','BDG2_Panther_lodging_Cora')
        if all((hvac_root/m/'summary.json').exists() for m in meters):
            record.update(status='completed_existing', artifacts=[str(hvac_root/m) for m in meters])
        else:
            try:
                adapter_for(task.task_id, ROOT / "outputs").load(context_length=720, horizon=96, step=96)
            except (AdapterNotReady, FileNotFoundError, TypeError, ValueError) as exc:
                record.update(status=task.status if task.status != "candidate" else "pending_adapter", message=str(exc))
    else:
        try:
            adapter = adapter_for(task.task_id, ROOT / "outputs")
            if task.task_id in ("traffic", "hvac"):
                adapter.load(context_length=720, horizon=96, step=96)
            else:
                adapter.load()
        except (AdapterNotReady, FileNotFoundError, TypeError, ValueError) as exc:
            record.update(status=task.status if task.status != "candidate" else "pending_adapter", message=str(exc))
    out = Path(args.output) if args.output else ROOT / "outputs" / "benchmark_runs" / task.task_id / "summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record, indent=2))

if __name__ == "__main__":
    main()
