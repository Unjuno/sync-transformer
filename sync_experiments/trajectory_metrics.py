"""Metrics for the trajectory/control track, kept separate from forecasting."""
import numpy as np

def ade(predicted, target):
    p, t = np.asarray(predicted, float), np.asarray(target, float)
    return float(np.linalg.norm(p - t, axis=-1).mean())

def fde(predicted, target):
    p, t = np.asarray(predicted, float), np.asarray(target, float)
    return float(np.linalg.norm(p[..., -1, :] - t[..., -1, :], axis=-1).mean())

def fallback_rate(fallback_flags):
    x = np.asarray(fallback_flags, bool)
    return float(x.mean()) if x.size else 0.0

def safety_violation_rate(violations):
    x = np.asarray(violations, bool)
    return float(x.mean()) if x.size else 0.0

def bootstrap_ci(values, seed=20260820, reps=2000):
    x = np.asarray(values, float).reshape(-1)
    if not x.size:
        raise ValueError("trajectory metric requires at least one trajectory")
    rng = np.random.default_rng(seed)
    draws = rng.choice(x, size=(reps, x.size), replace=True).mean(axis=1)
    return {"mean": float(x.mean()), "ci95": [float(np.quantile(draws, .025)), float(np.quantile(draws, .975))], "n": int(x.size)}
