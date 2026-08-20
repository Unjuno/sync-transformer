# SYNC Transformer — research brief

## Model

SYNC Transformer (episodic-residual prototype) consists of a learned forecast head plus a causal episodic candidate pathway. Candidate prefixes are selected only from the past, their futures retain offset order, and the transported trajectory enters as a residual/context correction. A benefit gate can abstain when candidate quality is uncertain.

## Strongest evidence

On ETTm1 (`P=720`, `H=96`, chronological split, 3 seeds):

- Hybrid MSE: `3.7403 / 3.8045 / 4.1675`
- matched forecast-head MSE: `6.2960 / 4.8504 / 5.2059`
- pooled paired delta Hybrid − head: `-1.5466`
- 95% paired bootstrap CI: `[-1.9410,-1.1654]`

Capacity-matched check: Base `19,640` parameters versus Hybrid `19,866`; pooled Hybrid-minus-head delta `-0.9133`, 95% CI `[-1.1926,-0.6388]`.

On the same ETTm1 protocol, Hybrid also beats persistence (`5.3289`) in all seeds.

## Mechanistic validation

- Future-order reversal degrades performance on all four ETT datasets.
- Causal gap and provenance checks are unit-tested.
- Candidate stride and K sensitivities have been measured.
- Search/transport latency has been measured separately.

## Limitations

- The original supplied full Transformer table has not been exactly reproduced.
- The current prototype is not a matched-parameter SYNC_CORE implementation.
- ETTh1 dense rolling evaluation exposed sensitivity: Hybrid can lose to persistence.
- Therefore the result should be presented as a prototype mechanism result, not universal superiority.

## Publication-safe wording

“We introduce SYNC Transformer, an episodic-residual forecasting architecture. On ETTm1, the causal ordered episodic residual improves a matched forecast head across three seeds; paired bootstrap confidence intervals exclude zero under the stated protocol. Performance is protocol-sensitive, motivating future work on cross-fitted benefit gating and full parameter-matched Transformer reproduction.”
