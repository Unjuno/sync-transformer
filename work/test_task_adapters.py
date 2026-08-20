import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from sync_experiments.adapters import AdapterNotReady, PendingAdapter, PendingTrajectoryAdapter, TrajectoryMetrics, adapter_for, HVACAdapter, TrafficAdapter, RoboMimicAdapter

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
    (tmp_path / "METR-LA.csv").write_text("timestamp,sensor_123\n" + "\n".join(f"t{i},{i}" for i in range(8)))
    batch = TrafficAdapter(tmp_path).load(context_length=3, horizon=2, step=2)
    assert batch.task_id == "traffic"
    assert batch.context.shape == (2, 3)

def test_trajectory_adapter_is_separate_and_explicit():
    adapter = adapter_for("robot_trajectory", "outputs")
    assert isinstance(adapter, PendingTrajectoryAdapter)
    with pytest.raises(AdapterNotReady):
        adapter.load_trajectory()

def test_robomimic_adapter_reads_pose_windows(tmp_path):
    h5py = pytest.importorskip('h5py')
    with h5py.File(tmp_path/'low_dim_v15.hdf5','w') as f:
        ds=f.create_dataset('data/demo_0/obs/robot0_eef_pos', data=[[float(i),0,0] for i in range(8)])
    batches=RoboMimicAdapter(tmp_path).load_trajectory(context_length=3,horizon=2,step=2)
    assert batches[0].observed.shape == (3,3)
    assert batches[0].future.shape == (2,3)

def test_trajectory_metrics_contract():
    metrics = TrajectoryMetrics(ade=1.0, fde=2.0, tracking_error=None,
                                success_rate=0.0, fallback_rate=1.0,
                                safety_violations=2)
    assert metrics.fallback_rate == 1.0
