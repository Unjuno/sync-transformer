import numpy as np
from sync_experiments.trajectory_metrics import ade, fde, fallback_rate, safety_violation_rate, bootstrap_ci

def test_trajectory_distance_metrics():
    target = np.zeros((2, 3, 2)); pred = target.copy(); pred[:, -1, 0] = 2
    assert ade(pred, target) == 2 / 3
    assert fde(pred, target) == 2.0

def test_trajectory_rates_and_ci():
    assert fallback_rate([True, False]) == 0.5
    assert safety_violation_rate([False, True, True]) == 2 / 3
    result = bootstrap_ci([1.0, 2.0, 3.0], reps=100)
    assert result['n'] == 3 and result['ci95'][0] <= 2.0 <= result['ci95'][1]
