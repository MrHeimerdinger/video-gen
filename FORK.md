# このフォークについて

[Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15)（MIT License）をもとに、Windows で動かすための調整と日本語の動画制作を加えた版です。元の README・ライセンスはそのまま残しています。

## 追加・変更したもの

| 場所 | 内容 |
|---|---|
| `render-win.ps1` | Windows 用の書き出しスクリプト。Chrome のパス、GPU（ANGLE/D3D11）、一時フォルダを設定し、`audio.py` → 映像の順に書き出す |
| `assets/fonts/cjk/notosansjp/` | **Noto Sans JP**（可変フォント、OFL。`OFL.txt` 同梱） |
| `assets/fonts/latin/inter/` | **Inter**（可変フォント、OFL）。日本語デモの数字・英字に使う |
| `assets/fonts/fonts.css` | 末尾に `Noto Sans JP` の `@font-face` を追加 |
| `demos/23-ssd-ja` 〜 `demos/28-ssd-ja-vertical` | 日本語の動画 6 本のソース（下表） |
| `docs/revision-log-ja.md` | 動画ごとの修正履歴と、初稿の質を上げるためのチェックリスト |

| フォルダ | 内容 | 画面 | 長さ |
|---|---|---|---|
| `23-ssd-ja` | SSD 容量解説（スタイル 07 ステッカー解説） | 1920×1080 | 15 秒 |
| `24-ssd-ja-30s` | 同・進行速度 50% 版 | 1920×1080 | 30 秒 |
| `28-ssd-ja-vertical` | 同・縦型（セーフマージン対応） | 1080×1920 | 30 秒 |
| `25-mdl-map` | MDL 店舗マップ（スタイル 02 アイソメトリック） | 1920×1080 | 10 秒 |
| `26-mdl-map-15s` | 同・東京→大阪→福岡→鹿児島の順 | 1920×1080 | 15 秒 |
| `27-mdl-map-vertical` | 同・縦型 | 1080×1920 | 15 秒 |

## Windows での使い方

必要なもの：Node.js 22.12 以上、Google Chrome、ffmpeg、Python 3.11 以上。

```powershell
npm install
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt   # Python 3.13 では matplotlib を 3.9.2 以上に上げる
.\render-win.ps1 demos\28-ssd-ja-vertical                       # → demos\28-ssd-ja-vertical\out\video.mp4
.\render-win.ps1 demos\28-ssd-ja-vertical --stills '4,10,17'    # 静止画だけ確認
```

注意：
- 元のデモ（01〜22）の多くは、このリポジトリに含まれていないフォントを使います。フォントが見つからないとページが初期化を止めて書き出しが進みません。必要なフォントは `assets/fonts/README.md` を参照してください。
- 書き出した動画（`out/` 以下）はリポジトリに含めていません。

## 素材のライセンス
- Noto Sans JP・Inter：SIL Open Font License 1.1
- 日本地図（`demos/25〜27/assets/japan.json`）：Natural Earth 1:10m（パブリックドメイン）、world-atlas@2.0.2 経由
- それ以外は元リポジトリのライセンス（MIT ほか、元の README の License 節）に従います
