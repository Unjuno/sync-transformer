# SYNC Transformer publication-readiness audit

監査日: 2026-08-14

## Verified

- Python compilation: passed.
- Architecture tests: 5 passed.
- Reconstruction artifact validator: passed, 37 files / 105 rows / 0 errors.
- Public-data audit: passed.
- Primary results use chronological splits, three seeds, paired query-level arrays, and condition-keyed filenames.
- Negative transfer and failed selection variants are documented.

## Not yet verified or complete

- Exact reproduction of the initially supplied full SYNC_CORE Phase 4A–4B table.
- Same-budget implementation and comparison against RAFT/PFRP.
- A regime gate that is uniformly safe across ETTh1/ETTh2/ETTm1/ETTm2.
- A demonstrated Internal Transformer variant that beats the External pathway.
- Independent third-party reproduction.
- A read-only search of the available Codex workspace and attachment locations found no recoverable original `SYNC_CORE` source or JSON matching the initial Phase 4A–4B values.
- ETTh1 split probes (50/25/25, 60/20/20, 40/20/40) change the gated delta from -0.001330 to +0.001905 to +0.010858; therefore ETTh1 is not a stable positive-result condition.
- Later-origin 70/15/15 probes give ETTh1 +0.017607 and ETTm1 +0.001226 with the threshold frozen; rich features give ETTh1 +0.006421; the AND distance/volatility gate collapses to the volatility gate in this condition.

## Publication claim allowed now

The project can be presented as a reproducible research prototype and empirical study of causal episodic residual transport, with conditional gains and explicit negative-transfer analysis. It should not yet be presented as a universally superior Transformer or as an exact reproduction of the original supplied table.
## Canonical deterministic rerun note (2026-08-14)

The common runner now enforces deterministic CPU execution and the four primary 60/20/20 artifacts have been regenerated. Their fixed-gate deltas are ETTh1 +0.008479, ETTh2 0.000000 (abstention), ETTm1 +0.001070, and ETTm2 +0.008027. Earlier narrative values from nondeterministic runs must not be used as headline evidence. The present evidence supports an auditable causal retrieval/fallback prototype, not a demonstrated accuracy improvement.
