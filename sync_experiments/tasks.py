"""Task registry for the ten-task SYNC benchmark plan.

Raw datasets are deliberately not bundled. Each task declares the adapter and
the metrics needed before it can be marked as validated.
"""
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    track: str
    dataset: str
    adapter: str
    metrics: Tuple[str, ...]
    status: str = "candidate"

TASKS = (
    TaskSpec("ett", "forecasting", "ETTh1/ETTh2/ETTm1/ETTm2", "ett", ("mse", "mae", "bootstrap_ci", "abstention_rate"), "validated_cpu"),
    TaskSpec("electricity", "forecasting", "UCI ElectricityLoadDiagrams", "electricity", ("mse", "mae", "bootstrap_ci", "abstention_rate"), "benchmarked_cpu_mt001_mt002_mt003"),
    TaskSpec("renewable", "forecasting", "GEFCom solar/wind or NREL", "renewable", ("mse", "mae", "bootstrap_ci", "abstention_rate")),
    TaskSpec("traffic", "forecasting", "METR-LA/PEMS-BAY", "traffic", ("mse", "mae", "bootstrap_ci", "abstention_rate")),
    TaskSpec("hvac", "forecasting", "Building Data Genome 2", "hvac", ("mse", "mae", "bootstrap_ci", "abstention_rate")),
    TaskSpec("server", "forecasting", "Alibaba cluster trace", "server", ("mse", "mae", "bootstrap_ci", "abstention_rate")),
    TaskSpec("retail", "forecasting", "M5/Favorita", "retail", ("mse", "mae", "bootstrap_ci", "abstention_rate")),
    TaskSpec("industrial", "forecasting", "NASA C-MAPSS", "industrial", ("mse", "mae", "bootstrap_ci", "abstention_rate"), "blocked_source_unavailable"),
    TaskSpec("robot_manipulation", "trajectory", "RoboMimic/Open X subset", "robomimic", ("ade", "fde", "success_rate", "fallback_rate", "safety_violations")),
    TaskSpec("robot_trajectory", "trajectory", "nuScenes or simulator logs", "trajectory", ("ade", "fde", "success_rate", "fallback_rate", "safety_violations")),
)

def get_task(task_id: str) -> TaskSpec:
    for task in TASKS:
        if task.task_id == task_id:
            return task
    raise KeyError(f"unknown task: {task_id}")
