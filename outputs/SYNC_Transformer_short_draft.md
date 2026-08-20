# SYNC Transformer: Causal Episodic Residuals for Long-Horizon Forecasting

## Abstract draft

We study whether causal episodic trajectories can provide useful context beyond a learned forecasting head. SYNC Transformer retrieves past-compatible episodes, preserves the temporal order of their future offsets, and injects a selected residual trajectory into a capacity-matched forecast head. In the current common reconstruction, External residual transport improves the matched head on ETTm1 and ETTm2, is near-neutral on ETTh2, and degrades on ETTh1 unless the candidate bank is bounded by recency. Hierarchical internal selection does not yet improve the matched head in the separated-bank evaluation. We also verify causal gap, provenance, future-order sensitivity, and leakage checks. The current implementation is an episodic-residual prototype; exact reproduction of the initially supplied full SYNC_CORE table remains future work.

## Contributions

1. A causal episodic residual pathway with ordered future transport.
2. A transparent comparison protocol for external, internal, and hierarchical candidate selection, including same-query paired testing.
3. Public-data evidence that the external residual pathway can add information beyond the same forecast head under specific data conditions.
4. Explicit falsification and leakage tests rather than universal-performance claims.

## Related work and novelty boundary

Retrieval-augmented forecasting is an active area. RAFT retrieves similar historical patches and their subsequent values, then aggregates them with attention-like weights; PFRP uses a global memory bank and adaptively combines retrieved global predictions with a local predictor. Our claim is therefore not that historical retrieval or memory augmentation is new. The proposed distinction is the explicit combination of causal provenance/gap constraints, ordered future residual transport into a forecast head, recency-bounded candidate banks, and a falsification protocol that reports negative transfer on hourly datasets. This combination remains a prototype-level hypothesis and requires a complete controlled comparison against these methods before a strong novelty claim.

The controlled ETTh1 reconstruction with identical query arrays found External residual transport ahead of both Internal E2E and Internal Ranked. Internal E2E minus External had mean `+0.006151` (95% CI `[+0.004176,+0.008156]`), while Ranked minus External had mean `+0.008400` (95% CI `[+0.006108,+0.010776]`). These negative results are retained as evidence against the current internalization design.

Additional ablations show that candidate aggregation is frequency/data dependent: increasing `K` from 1 to 8 improves ETTm1 (`External-head=-0.010439`) and ETTm2 (`-0.004928`), but worsens ETTh1 (`+0.004224`) and ETTh2 (`+0.003270`). Calibration-selected K does not remove this shift. A low-dimensional volatility gate reduces ETTh1 harm to about `+0.001905` while retaining ETTm1 improvement (`-0.008913`), but cross-fitted and volatility+distance gates are not uniformly better. These results motivate a conservative, regime-conditioned fallback rather than a universal always-on retrieval claim.

Under a fixed gate on ETTm1, K=1 was near-neutral (`+0.001207` pooled MSE), while K=8 improved the head (`-0.010439`). The opposite direction on ETTh1 shows that multi-candidate aggregation is a conditional mechanism result, not a universal benefit from increasing K.

As a mechanism control, direct raw retrieval of candidate futures (without residual transport) worsens ETTm1 by `+0.096050` relative to the head, whereas SYNC External improves it. Raw retrieval improves only ETTm2 (`-0.097189`). This indicates that the ETTm1 gain is not explained by retrieval alone, although this control is not a full RAFT/PFRP reproduction.

The raw-retrieval ETTm1 bootstrap interval is `[+0.080476,+0.112230]`, while the pooled-gated SYNC interval is below zero. We therefore describe residual transport as a necessary candidate mechanism in this reconstruction, not as a proven causal explanation.

In a direct same-query control, pooled-gated SYNC beats raw retrieval on ETTh1 (`-0.139135`), ETTh2 (`-0.048196`), and ETTm1 (`-0.106488`), but loses on ETTm2 (`+0.092261`). This supports a conditional mechanism claim rather than a universal residual-transport advantage.

An alternate ETTh1 chronological split (50/25/25 instead of 60/20/20) yielded a gated mean delta of `-0.001330` across three seeds, versus `+0.001905` on the primary split. This split sensitivity is reported explicitly and motivates rolling-origin validation before any universal claim.

A later-origin 70/15/15 probe further exposed this limitation: ETTh1 degraded by `+0.017607` pooled MSE with the frozen volatility threshold, while ETTm1 was near-neutral (`+0.001226`). A richer retrieval representation increased the ETTh1 primary pooled delta to `+0.006421` (versus `+0.001905` for the basic representation), and an AND-composed distance/volatility gate reduced to the volatility gate because calibration selected no finite distance cutoff. These controls are negative results and are included to prevent post-hoc claims that more features or stricter gating automatically solve distribution shift.

## Reproducibility sentence

Reported prototype results use public ETT CSVs, chronological splits, fixed `P/H`, three seeds, and test-future exclusion; primary JSON artifacts are condition-keyed under `outputs/common_runner_*.json`. The initial supplied full SYNC_CORE implementation and exact table are not available in the workspace and are not claimed to be reproduced.
## Canonical result boundary

The deterministic canonical rerun does not establish an accuracy improvement over the forecast head: fixed-gate deltas are +0.008479 (ETTh1), 0.000000 with full abstention (ETTh2), +0.001070 (ETTm1), and +0.008027 (ETTm2). The defensible contribution is therefore the causal episodic-residual transport and auditable fallback protocol, not a universal forecasting gain. All earlier positive values from nondeterministic runner executions are excluded from the headline result.

An endpoint-preserving input ablation recovers information discarded by patch averaging and changes the conditional result to -0.025849 (ETTh1), 0.000000 with abstention (ETTh2), -0.008600 (ETTm1), and +0.015014 (ETTm2). This supports a narrower representation-sensitive improvement claim, while seasonal-naive baselines remain stronger overall.
# Status note (2026-08-14)

The historical values in this draft (including `-0.010439`, `-0.004928`, and earlier raw-control deltas) came from superseded nondeterministic or protocol-variant runs. They are retained for provenance only and must not be used in the headline table. Use `SYNC_Transformer_paper_handoff.md` and `SYNC_Transformer_canonical_results_table.md` for current claims.
