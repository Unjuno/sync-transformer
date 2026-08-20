# SYNC Transformer GPU拡張実験計画

## 目的

CPUで確定したSYNC結果を変更せず、外部ベースラインRAFTとの同条件比較を行う。GPU実験は拡張実験であり、CPUで確定した結論を置き換えない。

## 固定する条件

- データ：ETTh1、ETTh2、ETTm1、ETTm2
- 予測長：hourly=24、minute=96
- SYNC：endpoint+seasonal、K=8、width=80、seeds=163/164/165
- split：60/20/20を主条件、rolling-originを補助条件
- 指標：平均MSE、query-level bootstrap 95% CI、改善クエリ率、棄却率、実行時間、パラメータ数
- 比較対象：seasonal naive、head-only、raw retrieval、SYNC、RAFT

## 実行手順

1. `nvidia-smi` でGPU名・VRAM・CUDAを記録する。
2. `work/vendor/RAFT` の依存関係とデータハッシュを記録する。
3. RAFTを各データセットで公式設定のままスモーク実行する。
4. 同じ入力窓・予測長・評価窓でRAFTを本実行する。
5. SYNCのCPU基準JSONを再生成せず、そのまま比較に使用する。
6. `outputs/raft_*_summary.json` と比較表を生成する。

## 判定基準

- RAFTを含む比較群でSYNCが優位なデータセットがあるか。
- 優位性がある場合、95% CIが0を跨がないか。
- 優位性がない場合、精度主張を追加せず、条件付き残差輸送・明示的棄却・監査性に主張を限定する。
- ETTh2の全棄却は性能向上として数えない。
- GPU実験結果がCPU基準と矛盾する場合、まず実装・split・正規化・seedを監査し、CPU基準を上書きしない。

## 実行例

```powershell
nvidia-smi
Set-Location work/vendor/RAFT
python -m torch.distributed.run --nproc_per_node=1 run.py --config configs/ETTm1.yaml
Set-Location ../../..
python work/run_canonical_suite.py
```

実際のRAFTの設定ファイル名・引数は、GPU環境で `work/vendor/RAFT/README.md` と各configを確認してから確定する。上記コマンドは実行テンプレートであり、未検証の固定コマンドではない。

## 成果物

- RAFT各データセットの生ログ
- 予測値またはquery-level MSE
- `outputs/raft_comparison_summary.json`
- SYNC/seasonal-naive/head/raw/RAFTの比較表
- 実行環境（GPU、CUDA、PyTorch、commit、seed）のmanifest

## 現在の状態

GPU未接続のため、RAFT本実行は未完了。CPU側の基準結果、rolling-origin、アブレーション、監査、テストは完了しており、GPU入手時にこの計画から再開する。
