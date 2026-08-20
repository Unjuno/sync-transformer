"""CPU benchmark for a conventional TransformerEncoder forecaster.

This is deliberately separate from SYNC. It uses the same causal ETT data,
chronological split, seeds, prediction horizon, normalized target, and query
stride as the common runner. The model receives a sequence of 30 patch means
and predicts the full horizon directly.
"""
import argparse, json, random, time
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"

def seed_all(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)

class VanillaTransformer(nn.Module):
    def __init__(self, d_model=64, nhead=4, layers=2, ff=128, horizon=24):
        super().__init__()
        self.proj = nn.Linear(1, d_model)
        enc = nn.TransformerEncoderLayer(d_model, nhead, ff, batch_first=True,
                                         dropout=0.0, activation="gelu")
        self.encoder = nn.TransformerEncoder(enc, layers)
        self.pos = nn.Parameter(torch.zeros(1, 30, d_model))
        self.out = nn.Sequential(nn.LayerNorm(d_model), nn.Linear(d_model, horizon))

    def forward(self, x):
        h = self.proj(x.unsqueeze(-1)) + self.pos
        h = self.encoder(h)
        return self.out(h.mean(1))

def run(dataset, seed, epochs=40, step=None, train_frac=.6, cal_frac=.8):
    seed_all(seed)
    y = pd.read_csv(OUT / f"{dataset}.csv").OT.to_numpy(np.float32)
    n = len(y); tr = int(n * train_frac); ca = int(n * cal_frac)
    mu, sd = y[:tr].mean(), y[:tr].std(); z = (y - mu) / (sd + 1e-8)
    P, H = (720, 24) if dataset.startswith("ETTh") else (720, 96)
    step = step or (24 if dataset.startswith("ETTh") else 96)
    def feat(t):
        return z[t-P:t].reshape(30, -1).mean(1)
    train = np.arange(P, tr-H+1, step)
    test = np.arange(ca, n-H+1, step)
    X = torch.tensor(np.stack([feat(t) for t in train]), dtype=torch.float32)
    Y = torch.tensor(np.stack([z[t:t+H] for t in train]), dtype=torch.float32)
    TX = torch.tensor(np.stack([feat(t) for t in test]), dtype=torch.float32)
    TY = np.stack([z[t:t+H] for t in test])
    model = VanillaTransformer(horizon=H)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    loss_fn = nn.MSELoss(); start = time.perf_counter()
    model.train()
    for _ in range(epochs):
        opt.zero_grad(); pred = model(X); loss = loss_fn(pred, Y)
        loss.backward(); opt.step()
    model.eval()
    with torch.no_grad(): pred = model(TX).numpy()
    elapsed = time.perf_counter() - start
    q_mse = np.mean((pred - TY) ** 2, axis=1)
    return {
        "dataset": dataset, "seed": seed, "model": "vanilla_transformer",
        "P": P, "H": H, "query_step": step, "train_frac": train_frac,
        "cal_frac": cal_frac, "epochs": epochs, "d_model": 64,
        "nhead": 4, "layers": 2, "parameter_count": sum(p.numel() for p in model.parameters()),
        "train_queries": len(train), "test_queries": len(test),
        "normalized_mse": float(q_mse.mean()), "query_mse": q_mse.tolist(),
        "elapsed_seconds": elapsed,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default="ETTh1,ETTh2,ETTm1,ETTm2")
    ap.add_argument("--seeds", default="163,164,165")
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--output", default="vanilla_transformer_benchmark.json")
    args = ap.parse_args()
    rows = [run(ds, int(s), epochs=args.epochs)
            for ds in args.datasets.split(",") for s in args.seeds.split(",")]
    summary = []
    for ds in args.datasets.split(","):
        rr = [r for r in rows if r["dataset"] == ds]
        summary.append({"dataset": ds, "mean_mse": float(np.mean([r["normalized_mse"] for r in rr])),
                        "mean_seconds": float(np.mean([r["elapsed_seconds"] for r in rr])),
                        "parameter_count": rr[0]["parameter_count"]})
    out = {"protocol": "same causal ETT protocol; vanilla Transformer baseline", "rows": rows, "summary": summary}
    path = OUT / args.output
    path.write_text(json.dumps(out, indent=2)); print(json.dumps(out, indent=2))

if __name__ == "__main__": main()
