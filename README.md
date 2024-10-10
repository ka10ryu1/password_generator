- [password\_generator](#password_generator)
  - [環境設定](#環境設定)
  - [使い方](#使い方)

# password_generator

どうしても手動で安全にパスワードを生成したいときに使う


## 環境設定

- `pip install` は不要
- Python 3.12で動作確認済み

## 使い方

- `./passwd_gen.py` を実行するだけ
- 必要に応じて、生成する文字数や記号の有無を切り替えられる
- ほかにも、拡張子をつけたりできる `./filename_gen.py` がある


```bash
$ tree
.
├── LICENSE         # とりあえずMITライセンス
├── README.md       # ここ
├── filename_gen.py # 適当なファイル名を生成するスクリプト
├── measure_time.py # 時間計測スクリプト（実行時間の分析もできる）
└── passwd_gen.py   # 適当なパスワードを生成するスクリプト

1 directory, 5 files
```
