# SYNC Transformer: next experiments

## Priority 1 — external retrieval baselines

Implement a same-budget RAFT-like retrieved-patch baseline and a local/global memory baseline. Freeze splits, query arrays, candidate budget, and parameter count. Report paired query-level differences against the pooled-gated SYNC prototype. Do not claim novelty from retrieval alone.

**Acceptance:** three seeds, four ETT datasets, bootstrap CI, and no test-future use in candidate selection.

## Priority 2 — recover or falsify the initial table

Ask for the original source archive or exact artifact if available. If it cannot be recovered, retain the current reconstruction as a clearly labeled protocol and run a sensitivity envelope over P/H, candidate stride, K, and recency.

**Acceptance:** either exact source-level reproduction or an explicit non-reproduction statement with all available sensitivity results.

## Priority 3 — internalization

Test a capacity-matched Internal selector with a frozen external teacher, cross-fitted ranking labels, and the same pooled gate. The Internal variant is adopted only if its paired CI beats External on at least three of four datasets without degrading the remaining dataset.

## Priority 4 — robustness

Add rolling-origin splits and a held-out dataset/frequency condition. The pooled gate threshold must be frozen before the held-out evaluation.

Initial split probe automation is now available in `work/run_split_probe.py` and was rerun successfully. ETTh1 and ETTm1 both show sign reversals across the three tested splits, so this priority remains open and is now a blocking condition for any generalization claim.

## Newly completed sensitivity probe

The legacy ETTh1/OT candidate-gap probe (`work/phase138_candidate_gap.py`) was rerun for gaps 0, 24, and 48. Raw transport degraded for all three settings (delta approximately +1.644, +1.649, and +1.645 MSE), while the calibrated gate selected the transport in 0% of test queries and therefore returned the head baseline. This is a negative result, not a headline gain: it supports retaining abstention/fallback as a required SYNC component and shows that changing the temporal gap alone does not rescue an incompatible retrieval regime.

The patched Base Transformer + External SYNC connection was also rerun with the same seed as the Base Transformer control (seed 155). Raw external transport had MSE 7.8196 versus the head MSE 5.0794; the calibrated mixture selected alpha=0 and therefore reproduced the head (MSE 5.0794). The earlier apparent gain from a different seed is not used as evidence. This controlled rerun confirms that the gate prevents negative transfer, but does not yet demonstrate a gain for this Transformer implementation.

### New ETTm1 alternate-split run

Using the frozen protocol with a 50/25/25 chronological split, `P=720`, `H=96`, query step 96, candidate step 48, `K=8`, threshold 0.079168, and 20 training epochs, the three seeds produced head-to-External paired deltas of -0.002367, -0.002723, and -0.000092 MSE. The mean is -0.001727 MSE; the gate use rate was 1.0 for all seeds. This is a modest alternate-split improvement, but it does not remove the broader split sensitivity already observed, so it is recorded as supporting evidence rather than a generalization claim. Artifact: `common_runner_ETTm1_q96_c48_lbfull_k8_rich0_vg0.079168_tr0.5_ca0.75.json`.

Two additional controlled seeds gave seed 163: base 4.0069, fused 4.0069 (alpha=0), and seed 164: base 4.3323, fused 4.2953 (alpha=0.05). Across seeds 155/163/164, the gate used no external signal in two runs and only 5% mixture weight in one; the mean fused change is only about -0.0123 MSE and is not a robust headline result. The external raw transport remains 7.8196 in all three runs.

### New alternate-split runs: ETTm2 and ETTh2

The same 50/25/25 chronological protocol was applied to ETTm2 (`P=720`, `H=96`, query step 96, candidate step 48, `K=8`, threshold 0.079168, 20 epochs). Seed-level paired deltas were +0.003199, 0.000000, and +0.005359 MSE, for a mean of +0.002853 MSE. The gate used the external signal in all three runs, but the small mean degradation means this is not evidence of a robust gain. Artifact: `common_runner_ETTm2_q96_c48_lbfull_k8_rich0_vg0.079168_tr0.5_ca0.75.json`.

For ETTh2 (`P=720`, `H=24`, query step 24, candidate step 8, `K=8`) the paired deltas were 0.000000, 0.000000, and -0.000421 MSE, for a mean of -0.000140 MSE; gate use was approximately 1.1% in each seed. The system therefore almost always abstained and reverted to the head forecast. Artifact: `common_runner_ETTh2_q24_c8_lbfull_k8_rich0_vg0.079168_tr0.5_ca0.75.json`.

Together with the existing ETTh1/ETTm1 split probes, these runs reinforce split- and dataset-dependent behavior. No split-robust generalization claim is licensed yet; same-budget retrieval and held-out evaluation remain open.

### Later-origin 70/15/15 probe

Using the same frozen threshold (0.079168) but moving the train/calibration boundary to 70/15/15 produced a strong negative result on ETTh1: seed means +0.014447, +0.015876, and +0.022499 MSE, pooled +0.017607; gate use was 44.4%. On ETTm1 the seed means were 0.000000, 0.000000, and +0.003678, pooled +0.001226, with gate use 100%. The change in temporal origin materially changes the outcome, so this probe further rules out a split-insensitive improvement claim. Artifacts: `common_runner_ETTh1_q24_c8_lbfull_k8_rich0_vg0.079168_tr0.7_ca0.85.json` and `common_runner_ETTm1_q96_c48_lbfull_k8_rich0_vg0.079168_tr0.7_ca0.85.json`.

### Fixed-gate K ablation on ETTh1

With the primary 60/20/20 split and the gate threshold fixed at 0.079168, a K=1 run (three seeds, `P=720`, `H=24`, query/candidate steps 24/8, 20 epochs) yielded seed means +0.003198, +0.007800, and +0.006794 MSE, pooled +0.005931 MSE; gate use was 62.8% in every seed. The corresponding K=8 pooled result is +0.001905 MSE under the same threshold. Thus increasing K reduced, but did not eliminate, the ETTh1 degradation; this is an ablation result, not evidence of a universal K optimum. Artifact: `common_runner_ETTh1_q24_c8_lbfull_k1_rich0_vg0.079168.json`.

As a gate-design control, the same ETTh1 70/15/15 run was repeated without the externally fixed volatility gate, using the runner's calibration-only distance gate. It selected external transport 100% of the time and degraded by +0.030956 pooled MSE (seed means +0.023858, +0.028126, +0.040884). This confirms that the fixed volatility gate is acting as a safety filter in this condition; the calibration-only distance gate is not yet robust to temporal shift. Artifact: `common_runner_ETTh1_q24_c8_lbfull_k8_rich0_tr0.7_ca0.85.json`.

The runner now also supports an explicit AND-composed gate (`--combine-gates`), requiring both the calibration distance gate and volatility gate. On the same ETTh1 70/15/15 condition, calibration selected an infinite distance threshold, so the AND gate reduced exactly to the volatility safety gate: pooled +0.017607 MSE with 44.4% use. The implementation is retained for future conditions where distance calibration is selective; it is not presented as a current gain. Artifact: `common_runner_ETTh1_q24_c8_lbfull_k8_rich0_vg0.079168_and_tr0.7_ca0.85.json`.

### Rich retrieval representation control

The primary ETTh1 protocol was repeated with the richer candidate/query feature representation (`--rich`, 13,304 parameters versus 10,904). Seed means were +0.001442, +0.008783, and +0.009038 MSE, pooled +0.006421 MSE, with the same 62.8% gate use. The basic representation's pooled result was +0.001905, so richer features did not improve this condition and are not adopted as the default. Artifact: `common_runner_ETTh1_q24_c8_lbfull_k8_rich1_vg0.079168.json`.

### ETTm1 K=1 versus K=8 under a fixed gate

To separate local single-neighbor retrieval from multi-candidate aggregation, ETTm1 was rerun with the same seeds, splits, threshold, and training budget. K=1 produced pooled `+0.001207` MSE (seed means 0.000000, 0.000000, +0.003622), whereas K=8 produced pooled `-0.010439` (seed means -0.009671, -0.011990, -0.009654). This is evidence that multi-candidate ordered aggregation is important for the ETTm1 gain, but it remains dataset-dependent because the analogous ETTh1 K ablation is negative. Artifact: `common_runner_ETTm1_q96_c48_lbfull_k1_rich0_vg0.079168.json`.

The same K=1 control on ETTm2 was negative (`+0.007227` pooled; seed means +0.009078, +0.004580, +0.008024), whereas the existing K=8 result is `-0.004928`. Thus both minute-scale datasets tested so far show a K=8-versus-K=1 separation; ETTh1 shows no such improvement, while ETTh2 abstains for both K values under the fixed volatility gate. This frequency interaction is now an explicit hypothesis for the same-budget baseline section. Artifact: `common_runner_ETTm2_q96_c48_lbfull_k1_rich0_vg0.079168.json`.

The fixed-gate K summary is now generated by `work/summarize_k_ablation.py` as `k_ablation_fixed_gate_summary.json`. ETTh2 K=1 is now present; both ETTh2 K values abstain completely (0% use), so their identical zero deltas reflect fallback rather than equivalent retrieval quality.

### ETTm1 recency-bounded K=8 probe

Restricting the candidate bank to the most recent 672 points (`lookback=672`, 13 candidates) while keeping K=8, the threshold, seeds, and split fixed yielded seed means -0.002436, -0.003491, and +0.000898 MSE, pooled -0.001676. The full-history K=8 result is -0.010439, so recency bounding preserves a small conditional improvement but removes most of the gain. Artifact: `common_runner_ETTm1_q96_c48_lb672_k8_rich0_vg0.079168.json`.

An intermediate 1344-point bank (27 candidates) gave nearly the same result: seed means -0.002392, -0.003367, and +0.000860, pooled -0.001633. The recency curve therefore plateaus around a small gain until the full history is restored; candidate count alone is not a monotonic explanation. Artifact: `common_runner_ETTm1_q96_c48_lb1344_k8_rich0_vg0.079168.json`.

## Current stop rule

Do not expand the novelty claim unless a same-budget baseline comparison and held-out evaluation pass. Current publication wording remains “reproducible causal episodic-residual prototype with conditional gains.”

### Deterministic canonical rerun (2026-08-14)

After enabling deterministic CPU execution, the four primary 60/20/20 artifacts were regenerated under the same nominal protocol. The frozen volatility-gate deltas are now ETTh1 `+0.008479`, ETTh2 `0.000000` (complete abstention), ETTm1 `+0.001070`, and ETTm2 `+0.008027`. These canonical reruns supersede earlier lightweight-runner values in narrative comparisons; the older values remain historical artifacts only. Under this reproducible configuration, the current evidence does not show a primary-dataset gain, so the claim boundary is narrowed to a causal, auditable retrieval/fallback mechanism pending same-budget baselines and held-out evaluation.

### Same-budget controls and utility-gate control

The canonical artifacts were compared at identical query/seed/training budgets against the head, raw transport, and persistence controls. SYNC is substantially safer than raw transport on ETTh1 and ETTm1, but still does not beat the head; on ETTh2 the raw transport is better while the fixed gate abstains completely. A cross-fitted calibration utility gate was also tested descriptively (`utility_gate_control.json`); it did not yield a held-out improvement and is not adopted. These controls support the safety/fallback interpretation, not an accuracy claim. Summary: `same_budget_control_summary.json`.

Persistence is a stronger baseline than the learned head on these data: it is lower-MSE than SYNC on ETTh1 and ETTm1, while SYNC's ungated external forecast is lower than persistence on ETTh2 and ETTm2. Future headline comparisons must therefore include persistence (and a standard seasonal/naive baseline), not only the learned head.

A causal seasonal-naive baseline was added as a stronger reference. Period-24/96 seasonal forecasts achieve MSE 0.0691 (ETTh1), 0.1590 (ETTh2), 0.0698 (ETTm1), and 0.1588 (ETTm2), all below the current SYNC forecasts. This rules out presenting SYNC as a competitive forecaster on these canonical settings; its remaining research value is architectural and safety-oriented unless a stronger learned model or a better-conditioned task is identified. Artifact: `seasonal_baseline_summary.json`.

### Endpoint-preserving feature ablation

The original 30-patch-mean representation discarded the latest value in every patch. A new `--endpoint-features` representation appends each patch endpoint to the patch means (60-dimensional input) while keeping the same optimizer budget, candidate bank, K=8, gate threshold, and seeds. The deterministic fixed-gate deltas versus the corresponding head are: ETTh1 `-0.025849`, ETTh2 `0.000000` (abstention), ETTm1 `-0.008600`, and ETTm2 `+0.015014`. This is the first reproducible feature-level improvement over the weak learned head on ETTh1 and ETTm1, but it remains below the seasonal-naive baseline and is not a universal gain. Artifacts use the `_end_` filename tag.

Appending two explicit seasonal lag values (`--seasonal-features`) to the endpoint representation further changes the deltas to ETTh1 `-0.033155`, ETTh2 `0.000000` (abstention), ETTm1 `-0.009465`, and ETTm2 `+0.013750`. The improvement is modest relative to endpoint-only features and remains frequency-dependent. These results justify treating endpoint/seasonal features as a representation ablation, not as a universal SYNC architecture result. Artifacts use the `_end_sf_` filename tag.

Finally, SYNC residual transport was applied on top of the strong seasonal-naive base (`--seasonal-base`). The calibration selected zero residual weight and the gate abstained on all four datasets, reproducing the seasonal baseline exactly. This is a useful negative control: the current residual mechanism adds no value once a strong periodic prior is supplied, so future gains must be demonstrated beyond this baseline rather than against the weaker learned head.

Query-level bootstrap (435 pooled queries per dataset) gives endpoint+seasonal deltas of ETTh1 `-0.033155` (95% CI `[-0.04198,-0.02457]`), ETTm1 `-0.009465` (CI `[-0.01556,-0.00354]`), ETTh2 `0` (abstention), and ETTm2 `+0.013750` (CI `[+0.00641,+0.02090]`). Thus the two positive conditions are statistically distinguishable from zero against the learned head, while the frequency-dependent failure is also statistically clear. Artifact: `endpoint_feature_bootstrap.json`.

### K=1 versus K=8 with endpoint+seasonal features

Under the same endpoint+seasonal representation, K=8 remained slightly better than K=1 on ETTh1 (`-0.033155` vs `-0.030688`) and ETTm1 (`-0.009465` vs `-0.005328`). On ETTm2 both were negative relative to the head, with K=8 less harmful (`+0.013750` vs `+0.016084`). This supports multi-candidate aggregation as a modest structural contributor, but not as a universal remedy.

### Endpoint+seasonal split robustness

The same representation was tested on alternate chronological splits. At 50/25/25, pooled deltas were ETTh1 `-0.030759` and ETTm1 `-0.018494`; at 70/15/15 they reversed to ETTh1 `+0.031582` and ETTm1 `+0.008979`. Thus the feature improvement is real under the primary and 50/25/25 origins but not later-origin robust. These results prevent a split-invariant claim and motivate a future rolling-origin protocol.

As a gate diagnostic, thresholds were re-estimated using only the 70/15/15 calibration period with a cross-fitted utility objective. ETTh1 remained `+0.031582` pooled and ETTm1 remained positive (approximately `+0.0054` pooled), so the late-origin failure is not explained solely by the frozen 0.079168 threshold; it reflects representation/transport distribution shift.

An additional exploratory distance-quantile gate was evaluated offline. On the primary split, restricting transport to queries below the calibration-distance 90th percentile changed the pooled deltas to ETTh1 `-0.015231` and ETTm1 `-0.007882`, better than always transporting. On the 50/25/25 split the effect was smaller (ETTh1 `-0.001371`, ETTm1 `-0.004273`), while on 70/15/15 it did not prevent failure (ETTh1 `+0.031582`, ETTm1 `+0.008979`). This supports distance as a useful primary-split selector but not a solved shift-robustness mechanism.

### Multi-scale retrieval representation control

As a transparent RAFT-like representation control, 30 patch means were augmented with 15- and 5-patch coarse means (`--multiscale-features`). With the same 20-epoch budget, deltas were ETTh1 `-0.009821`, ETTh2 `0.000000` (abstention), ETTm1 `+0.004185`, and ETTm2 `+0.014736`, with 12,504 parameters on hourly and 18,336 on minute data. This did not improve over endpoint+seasonal features and is not adopted; it also reinforces that multi-scale retrieval alone is not the proposed contribution.
### Capacity control on ETTm1 (width 40 vs width 80)

The same ETTm1 protocol was rerun with the hidden width reduced from 80 to 40 (6,816 vs 16,736 trainable parameters; seeds 163/164/165, K=8, volatility threshold 0.079168). The width-40 run produced external-minus-head MSE deltas of -0.008238, -0.023011, and -0.033341 (mean -0.021530), so the residual-transport signal remains present under substantially lower capacity. The restored width-80 run produced 0.000000, 0.000000, and +0.003210 (mean +0.001070). The runner now fixes deterministic CPU execution; an exact same-seed rerun matched query-level outputs. This remains a capacity-sensitivity probe, not a definitive scaling law. Artifacts: `common_runner_ETTm1_q96_c48_lbfull_k8_rich0_w40_vg0.079168.json` and the standard-width artifact `common_runner_ETTm1_q96_c48_lbfull_k8_rich0_vg0.079168.json`.
### Raw retrieval versus residual transport (same candidate bank)

Using the endpoint+seasonal representation and identical candidates, fused residual transport beat raw candidate transport by `-0.060598` MSE on ETTh1 (95% CI `[-0.07700,-0.04485]`) and `-0.064815` on ETTm1 (CI `[-0.08067,-0.04944]`). On ETTm2 the difference was `+0.009229` (CI `[-0.00407,+0.02247]`), not distinguishable from zero. This is the clearest evidence that the useful component, where present, is residual transport/fusion rather than retrieval alone. It remains a conditional mechanism result, not a universal forecasting gain. Artifact: `raw_vs_sync_bootstrap.json`.
