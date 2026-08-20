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

class PendingAdapter(BaseAdapter):
    def __init__(self, task_id: str, dataset: str):
        self.task_id, self.dataset = task_id, dataset
    def load(self, *args, **kwargs):
        raise AdapterNotReady(f"{self.task_id}: acquire and license {self.dataset}, then implement its adapter")

def adapter_for(task_id: str, data_root: str | Path):
    if task_id == "ett":
        return ETTAdapter(data_root)
    from .tasks import get_task
    task = get_task(task_id)
    return PendingAdapter(task.task_id, task.dataset)
