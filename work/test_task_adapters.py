import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from sync_experiments.adapters import AdapterNotReady, PendingAdapter, PendingTrajectoryAdapter, TrajectoryMetrics, adapter_for, HVACAdapter, TrafficAdapter

def test_pending_adapter_fails_explicitly():
    with pytest.raises(AdapterNotReady):
        PendingAdapter("traffic", "METR-LA").load()

def test_ett_adapter_is_selected():
    assert adapter_for("ett", "outputs").task_id == "ett"

def test_hvac_adapter_loads_numeric_series(tmp_path):
    (tmp_path / "bdg2_electricity_cleaned.csv").write_text(
        "timestamp,Panther_office_Hannah\n" + "\n".join(f"t{i},{i if i != 3 else ''}" for i in range(12))
    )
    batch = HVACAdapter(tmp_path).load(context_length=4, horizon=2, step=2)
    assert batch.task_id == "hvac"
    assert batch.context.shape == (4, 4)
    assert batch.target.shape == (4, 2)
    assert batch.context[0, 3] == pytest.approx(3.0)

def test_traffic_adapter_loads_sensor_column(tmp_path):
    (tmp_path / "METR-LA.csv").write_text("timestamp,0\n" + "\n".join(f"t{i},{i}" for i in range(8)))
    batch = TrafficAdapter(tmp_path).load(context_length=3, horizon=2, step=2)
    assert batch.task_id == "traffic"
    assert batch.context.shape == (2, 3)

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
