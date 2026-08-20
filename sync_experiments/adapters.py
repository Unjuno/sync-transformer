"""Dataset adapter contracts for the ten-task benchmark.

Adapters return causal windows in a common shape. Only ETT is implemented in
the current public checkout; pending adapters fail explicitly rather than
silently substituting another dataset.
"""
from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass
class WindowBatch:
    task_id: str
    context: np.ndarray
    target: np.ndarray
    timestamps: np.ndarray | None = None

@dataclass
class TrajectoryBatch:
    """Causal trajectory contract kept separate from scalar forecasting."""
    task_id: str
    observed: np.ndarray
    future: np.ndarray
    timestamps: np.ndarray | None = None
    metadata: dict | None = None

@dataclass
class TrajectoryMetrics:
    ade: float
    fde: float
    tracking_error: float | None
    success_rate: float | None
    fallback_rate: float
    safety_violations: int
    latency_ms: float | None = None

class AdapterNotReady(RuntimeError):
    pass

class BaseAdapter:
    task_id = ""
    def load(self, *args, **kwargs) -> WindowBatch:
        raise NotImplementedError

class ETTAdapter(BaseAdapter):
    task_id = "ett"
    def __init__(self, root: str | Path):
        self.root = Path(root)
    def load(self, dataset: str, context_length: int, horizon: int, step: int) -> WindowBatch:
        path = self.root / f"{dataset}.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        import pandas as pd
        y = pd.read_csv(path).OT.to_numpy(np.float32)
        starts = np.arange(0, len(y) - context_length - horizon + 1, step)
        return WindowBatch("ett", np.stack([y[t:t+context_length] for t in starts]),
                           np.stack([y[t+context_length:t+context_length+horizon] for t in starts]))

class ElectricityAdapter(ETTAdapter):
    task_id = "electricity"
    def load(self, dataset="Electricity", context_length=720, horizon=96, step=96):
        return super().load(dataset, context_length, horizon, step)

class PendingAdapter(BaseAdapter):
    def __init__(self, task_id: str, dataset: str):
        self.task_id, self.dataset = task_id, dataset
    def load(self, *args, **kwargs):
            raise AdapterNotReady(f"{self.task_id}: acquire and license {self.dataset}, then implement its adapter")

class PendingTrajectoryAdapter(PendingAdapter):
    """Explicit trajectory-side blocker; never returns forecasting windows."""
    def load_trajectory(self, *args, **kwargs) -> TrajectoryBatch:
        raise AdapterNotReady(f"{self.task_id}: trajectory dataset/formulation is not ready for {self.dataset}")

def adapter_for(task_id: str, data_root: str | Path):
    if task_id == "ett":
        return ETTAdapter(data_root)
    if task_id == "electricity":
        return ElectricityAdapter(data_root)
    from .tasks import get_task
    task = get_task(task_id)
    if task.track == "trajectory":
        return PendingTrajectoryAdapter(task.task_id, task.dataset)
    return PendingAdapter(task.task_id, task.dataset)
