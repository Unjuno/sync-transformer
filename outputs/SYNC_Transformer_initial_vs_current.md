# 初期結果と現在のSYNC Transformerの差分

## 変えていない核

- 過去prefixから候補を検索する
- 候補のfuture offset順序を保つ
- query時点より未来を候補キー・ラベルとして参照しない
- 候補futureを予測headへ補助情報として輸送する

## 現在追加したもの

- causal gap / provenance / orderの契約テスト
- External residual transportの共通runner
- candidate bankの年齢/lookback制約
- K・candidate step・rich representation・gate感度
- Internal bankと学習queryの分離
- Hierarchical hard maskおよびsoft-to-hard診断
- 4データセット・3 seed・paired bootstrap
- 条件付き一次JSONと上書き防止
- RAFT/PFRPとの関連研究監査

## 初期結果からまだ再現できていないもの

- Base 0.4378
- External Sync 0.3868
- Internal E2E 0.3939
- Internal Ranked 0.3858
- Hierarchical Internal 0.3849
- 初期実装の正確なparameter budget・split・loss・候補定義

## 結論

現在の成果は、初期結果の数値再現ではなく、初期仮説を公開ETTデータ上で再構成し、どの条件で成立・失敗するかを監査したprototypeである。したがって、初期結果を「改善した」のではなく、再現可能性・因果性・データ依存性を明らかにした、と表現する。
