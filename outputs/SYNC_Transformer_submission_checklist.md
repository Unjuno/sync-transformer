# SYNC Transformer submission checklist

## 現時点で揃っているもの

- [x] SYNCの設計定義（causal episodic retrieval / ordered residual transport）
- [x] 公開ETTデータとmanifest
- [x] 条件付き一次JSON（上書き防止）
- [x] 4データセットのExternal共通runner診断
- [x] 3 seed評価
- [x] causal gap / provenance / order契約テスト
- [x] future leakage監査
- [x] 関連研究監査（RAFT / PFRP）
- [x] negative transferとprotocol差の記録

## 提出前に必要なもの

- [ ] 初期Phase 4A–4B数値の完全再構成
- [ ] RAFT/PFRPとの同一split・同一予算比較
- [ ] Internal / Ranked / Hierarchicalの最終controlled comparison
- [ ] 全主結果のquery-level paired bootstrap
- [x] 複数splitまたは追加データセットでの確認（split probe実施済み。ただし効果の符号反転を確認）
- [ ] split-robustなrolling-origin一般化の確認
- [x] 実行環境・依存version・完全な再実行スクリプトの固定（canonical suite + SHA-256 manifest）

## 現在の安全なタイトル

**SYNC Transformer: Causal Episodic Residual Transport for Conditional Time-Series Forecasting**

## 現在の安全な主張

「過去検索そのものの新規性」ではなく、因果ordered residual transport、候補年齢制御、明示的反証プロトコルを統合したprototypeである。endpoint+seasonal表現はprimary splitのETTh1/ETTm1でheadを改善するが、ETTh2は退避し、ETTm2は悪化する。複数split probeではETTh1/ETTm1とも符号反転し、split-robustな改善は未確認である。

## 提出判断

現状は、技術報告・ワークショップ・research noteとしては提出可能なプロトタイプ段階。強い新規性や主要会議の完全論文として提出するには、上記の未完了項目を満たす必要がある。
