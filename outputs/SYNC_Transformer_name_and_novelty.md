# SYNC Transformer: 名称・新規性・実験上の位置づけ

## 名称

現時点の正式な作業名は **SYNC Transformer — capacity-matched hierarchical episodic-residual prototype** とする。
単に「Transformerに候補を足したモデル」ではなく、因果的に保存した過去エピソードから候補futureを検索し、forecast headの残差として輸送する構成を指す。

## 新規性の判定

「SYNC」という名前自体、または候補をattentionで検索すること自体の新規性は主張できない。類似する部品（nearest-neighbor retrieval、memory/episodic forecasting、mixture/gating、residual correction、hierarchical top-k）は既存研究にも現れ得るため、文献調査なしに「世界初」とは言わない。

現時点で主張候補になるのは、次の組合せと検証プロトコルである。

1. 過去prefixとの因果検索を明示的なprovenance/gap検査で制約する。
2. 候補futureを直接予測値へ置換せず、学習済みforecast headへの残差輸送として使う。
3. coarse top-12からfinal top-4へ再選択する階層検索を同じモデル予算で評価する。
4. 同じquery・同じfuture・同じforecast head上で、paired bootstrapを使って差を検定する。

これは「新しい部品」よりも、**因果episodic residual transportをforecasting Transformerへ統合し、安全ゲートと予算一致評価まで含めた方法論的貢献**として位置づけるのが安全である。

## 現在の最強の証拠

ETTm1、P=720、H=24、test stride=96、width=80、3 seedの階層版では、Hybridの平均MSEは3.2294、同じforecast headは4.0246、persistenceは5.3289。435 queryをプールしたpaired bootstrapで Hybrid − head の平均差は -0.7951、95% CIは [-1.0653, -0.5332] で0を含まない（`phase185_hierarchical_bootstrap.md`）。

## まだ未証明の点

- 初期に提示された Phase 4A–4B の数値（0.4378等）の完全再現。
- ETTh1の密なstride=12評価での頑健な改善（現状はpersistenceを上回らない）。
- 既存手法に対する文献ベースの新規性。
- 全候補（Base / External / Internal E2E / Ranked / Hierarchical）の同一予算・同一splitでの完全比較。

したがって、論文や公開時の表現は「新規性が確定したTransformer」ではなく、**新規な統合仮説を検証中のSYNC Transformer prototype**とする。
