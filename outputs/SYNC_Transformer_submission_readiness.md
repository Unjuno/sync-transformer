# SYNC Transformer 掲載準備監査

## 掲載可能な核

因果的なepisodic candidate retrievalとordered future transportを、forecast headへのresidual correctionとして統合する設計。候補のprovenance、future leakage防止、順序保存、reverse interventionの契約テストは実装済み。

canonical deterministic runnerでは、endpoint+seasonal表現がETTh1/ETTm1で条件付き改善、ETTh2でフォールバック、ETTm2で悪化を示した。したがって「表現依存の条件付き改善」という主張は可能だが、「minute-levelで一貫して改善」や「全データセットで改善」は不可。

## 未完成

1. 初期Phase 4A–4Bの数値（Base 0.4378等）の完全再現。
2. 初期実装と同一のparameter budget・候補定義でのBase/External/Internal E2E/Ranked/Hierarchical完全比較。
3. 既存手法との文献比較による新規性確認。
4. ETTh1を含むhourly系列でのbenefit predictorの改善。
5. 全主結果でのquery-level paired bootstrapと独立test protocol。

## 掲載時に避ける表現

- 「世界初」「普遍的に精度向上」
- 初期表の数値を再現済みとする表現
- primitive protocolと共通Transformer protocolの結果の混同
- oracle診断を通常の性能結果として扱うこと

## 次の優先順位

1. 初期Phase 4A–4Bの完全再構成を最優先で実装する。
2. 共通runnerでcandidate rankingをcross-fitし、ETTh1/ETTm1を同一表で評価する。
3. 有効性が条件依存であることを主結果として明示する。
4. その後に文献比較とsubmission draftを確定する。

## 現在の名称

**SYNC Transformer — causal episodic residual transport prototype**

これは完成モデルの断定ではなく、検証済みの設計核と未検証範囲を正確に表す作業名である。
