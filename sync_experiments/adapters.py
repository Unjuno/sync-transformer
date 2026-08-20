"""Dataset adapter contracts for the ten-task benchmark.

Adapters return causal windows in a common shape. Only ETT is implemented in
the current public checkout; pending adapters fail explicitly rather than
silently substituting another dataset.
"""
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd

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

class CSVSeriesAdapter(BaseAdapter):
    """Load one deterministic numeric column from a timestamped CSV."""
    def __init__(self, task_id: str, root: str | Path, filename: str, column: str | None):
        self.task_id, self.root, self.filename, self.column = task_id, Path(root), filename, column

    def load(self, context_length: int, horizon: int, step: int = 1) -> WindowBatch:
        path = self.root / self.filename
        if not path.exists():
            raise FileNotFoundError(path)
        if self.column is None:
            header = pd.read_csv(path, nrows=0).columns.tolist()
            candidates = [c for c in header if c.lower() not in {'timestamp','datetime','date','time'}]
            if not candidates:
                raise ValueError(f'{path}: no sensor column found')
            self.column = candidates[0]
        frame = pd.read_csv(path, usecols=[self.column])
        y = pd.to_numeric(frame[self.column], errors='coerce').interpolate(limit_direction='both').to_numpy(np.float32)
        if not np.isfinite(y).any():
            raise ValueError(f'{path}: sensor column contains no numeric values')
        starts = np.arange(0, len(y) - context_length - horizon + 1, step)
        if len(starts) == 0:
            raise ValueError(f'{path}: insufficient rows for context={context_length}, horizon={horizon}')
        return WindowBatch(self.task_id,
                           np.stack([y[t:t+context_length] for t in starts]),
                           np.stack([y[t+context_length:t+context_length+horizon] for t in starts]))

class HVACAdapter(CSVSeriesAdapter):
    """BDG2 electricity series adapter; column choice is explicit for reproducibility."""
    def __init__(self, root: str | Path, filename='bdg2_electricity_cleaned.csv', column='Panther_office_Hannah'):
        super().__init__('hvac', root, filename, column)

class TrafficAdapter(CSVSeriesAdapter):
    """METR-LA/PEMS-BAY single-sensor view for the forecasting track."""
    def __init__(self, root: str | Path, filename='METR-LA.csv', column=None):
        super().__init__('traffic', root, filename, column)

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
    if task_id == "hvac":
        return HVACAdapter(Path(data_root).parent / 'data' / 'raw')
    if task_id == "traffic":
        return TrafficAdapter(Path(data_root).parent / 'data' / 'raw')
    from .tasks import get_task
    task = get_task(task_id)
    if task.track == "trajectory":
        return PendingTrajectoryAdapter(task.task_id, task.dataset)
    return PendingAdapter(task.task_id, task.dataset)
