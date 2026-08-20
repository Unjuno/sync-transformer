# SYNC Transformer 新規性・既存研究監査（一次文献ベース）

## 既存と重なる部分

- RAFT (ICML 2025) は、入力に類似する過去patchをtraining seriesから検索し、その直後のfuture patchを予測へ取り込む。top-mをsoftmax集約し、固定lookbackだけでなく全系列から検索する構成である。
- PFRP (AAAI 2026) はGlobal Memory Bankから類似patternを検索し、local predictorとglobal predictionをadaptiveに組み合わせる。
- したがって、過去prefix検索、future candidate利用、外部memory、local forecastとの融合は、SYNC固有の新規性とは言えない。

## SYNCで差分候補になり得る部分

1. candidate futureを直接予測へ置換せず、ordered future residualとしてforecast headへtransportする。
2. candidateの因果gap・provenance・future offset順序を契約として明示し、reverse-order interventionで検証する。
3. candidate bankの有効年齢を制約し、非定常性に対する候補windowを設計変数として扱う。
4. External retrieval / Internal selection / Hierarchical selectionを同じquery・future・budgetで比較する。

これらは「新しい検索という部品」ではなく、**ordered causal residual transport + candidate-age control + explicit falsification protocol**という統合として主張するのが安全である。文献との差分が確定したとはまだ言えず、厳密な関連研究調査と同一データセット比較が必要である。

## 判定

現時点で「世界初」「retrieval-augmented forecastingとして初」は主張不可。安全な表現は、**既存のretrieval-augmented forecastingと異なる因果残差transport・候補年齢制御・反証プロトコルを検証するprototype** である。

## 参照

- Han et al., “Retrieval Augmented Time Series Forecasting,” ICML 2025 / arXiv: https://arxiv.org/abs/2505.04163
- Du et al., “Predicting the Future by Retrieving the Past,” AAAI 2026: https://ojs.aaai.org/index.php/AAAI/article/view/39230
