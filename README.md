# GPTを利用した営業メール作成スクリプト

## 用意するもの

### .env
- JSON_KEY_FILE：Googleスプレッドシートに書き込むための鍵ファイル（JSON）
  - jsonファイルは、 `main.py` と同じ階層に置く
- SHEET_ID：鍵ファイル（JSON）のclient_emailに共有したスプレッドシートのID
- BASE_DATA_SHEET_NAME：スプレッドシートのインプット用データのあるシート名
- OUTPUT_SHEET_NAME：GPTに作成してもらった文章を出力するシート名
- OPEN_AI_API_KEY：OpenAIのAPI KEY
- GPT_MODEL：GPTのモデル（.env.sampleには `gpt-3.5-turbo` を指定してある）

### order.txt

- このテキストはGPTに与えるオーダーのテンプレート文章となる。
- このテキストはスクリプト中ではヒアドキュメントとして扱い、変数は `{hoge}` の形式で入力する
- 現実装では、スプレッドシートの見出しをキー名として取得したデータを `makeOrderContent()` 内でバインドしている

## 実行方法

### イメージのビルド

```
./build.sh
```

### 実行

```
$ docker run --rm -it -v $(pwd):/app sales-mail-by-gpt:latest
```