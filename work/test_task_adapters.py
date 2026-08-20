import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from sync_experiments.adapters import AdapterNotReady, PendingAdapter, PendingTrajectoryAdapter, TrajectoryMetrics, adapter_for

def test_pending_adapter_fails_explicitly():
    with pytest.raises(AdapterNotReady):
        PendingAdapter("traffic", "METR-LA").load()

def test_ett_adapter_is_selected():
    assert adapter_for("ett", "outputs").task_id == "ett"

def test_trajectory_adapter_is_separate_and_explicit():
    adapter = adapter_for("robot_trajectory", "outputs")
    assert isinstance(adapter, PendingTrajectoryAdapter)
    with pytest.raises(AdapterNotReady):
        adapter.load_trajectory()

def test_trajectory_metrics_contract():
    metrics = TrajectoryMetrics(ade=1.0, fde=2.0, tracking_error=None,
                                success_rate=0.0, fallback_rate=1.0,
                                safety_violations=2)
    assert metrics.fallback_rate == 1.0
