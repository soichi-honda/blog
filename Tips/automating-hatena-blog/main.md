弊社のはてなブログ移行を記念に、記事本文と画像の自動投稿pythonスクリプトを書いてみました！

記事目安...10分

[:content]

## pythonスクリプトについて
今回、2つのpythonスクリプトを用意しました。

- [post_hatena.py|https://github.com/sugaya0204/blog/blob/Public/TF/automating-hatena-blog/src/post_hatena.py]
- [execution.py|https://github.com/sugaya0204/blog/blob/Public/TF/automating-hatena-blog/src/execution.py]

---

要点をざっくり解説します。

### Post_hatena.py

はてなブログに、記事本文と画像をアップロードする処理を定義したモジュールです。

大きく以下2クラスで構成されます。

#### "PostHatena"クラス
はてなブログに、マークダウン形式で記述された記事をアップロードします。

認証はBasic認証を使用します。

参考: [はてなブログAtomPub-ブログエントリの投稿|http://developer.hatena.ne.jp/ja/documents/blog/apis/atom]

#### "PostHatenaPhoto"クラス
はてなフォトライフに、PNG形式の画像ファイルをアップロードします。

認証にはWSSE認証を使用します(*1)。

参考: [はてなフォトライフAtomAPI-PostURI|http://developer.hatena.ne.jp/ja/documents/fotolife/apis/atom]

*1. Oauth認証を使いたかったのですが、どうしてもCLIで完結できなかったため、WSSE認証を使用しています。

### execution.py
"Post_hatena"モジュールを読み込み、実際にアップロード処理を行うpythonスクリプトです。

大きく以下3つの関数から構成されます。

#### main関数
他の関数を呼び出すメイン関数です。

#### upload_text()
はてなブログに記事本文をアップロードする関数です。

"post_hatena"モジュールから"PostHatena"クラスをインポートしています。

#### upload_images()
はてなフォトライフに画像ファイルをアップロードする関数です。

"post_hatena"モジュールから"PostHatenaPhoto"クラスをインポートしています。

## 使い方

Python3が実行できる環境で行ってください。(*2)

*2. 以下環境で実行できました。

|Key|Value|
|---|---|
|EC2|AmazonLinux2|
|Python|3.7.8|

### 事前準備
以下のモジュールをインストールしてください。

```bash
sudo pip3 install bs4
sudo pip3 install lxml
sudo pip3 install requests
```

---

以下環境変数に登録します。

|Key|Value|
|---|---|
|HATENA_ID|自分のはてなID|
|BLOG_ID|対象ブログのブログID|
|API_KEY|対象ブログのAPIキー|

各値については、"各ブログダッシュボード" の "設定" にて "詳細設定" タブを選択後、"AtomPub" にて確認できます。

毎回読み込まれるよう、".bash_profile" に追記してください。

```bash
vi ~/.bash_profile
---
export HATENA_ID='<自分のはてなID>'
(以下略)
---
```

---

先ほどのpythonスクリプトを実行環境に保存します。

- [post_hatena.py|https://github.com/sugaya0204/blog/blob/Public/TF/automating-hatena-blog/src/post_hatena.py]
- [execution.py|https://github.com/sugaya0204/blog/blob/Public/TF/automating-hatena-blog/src/execution.py]

以下フォルダを作成して、保存しましょう。

```bash
$ mkdir ~/hatena_src
$ cd ~/hatena_src
$ tree
.
├── execution.py
└──post_hatena.py
```
---

これで準備は完了です。

### はてなブログへのアップロード

では、アップロードを行います。

---

今回はデモとして以下をアップロードしてみましょう。

- 記事本文
[test.md|]
- 画像ファイル
[test-image-green.png|]
[test-image-red.PNG|]

これらを以下フォルダ構成で保存してください。

```bash
$ mkdir ~/hatena_demo
$ cd ~/hatena_demo
.
├── assets
│   ├── test-image-green.png
│   └── test-image-red.PNG
└── test.md
```

ここのフォルダ構成が崩れると正しくアップロードできないので注意してください。
---

pythonスクリプトを実行します。
実行後は、プロンプトに従がってファイルをアップロードしてください。

```bash
$ cd ~/hatena_src
$ python3 execution.py ~/hatena_demo
```

〇凡例
```bash
$ python3 execution.py ~/hatena_demo

---Upload the following file---
/home/ec2-user/blog/TF/automating-hatena-blog/hatena_demo/test.md


If everything is OK, enter "yes" or "y".
If you don't like it, enter "no" or "n".

y
-----
Success!
URL: "アップロード先のURL"
-----

Want to uploading images?


If you want, enter "yes" or "y".
If you don't want it, enter "no" or "n".

y

---Upload the following file---
/home/ec2-user/hatena_demo/assets/test-image-green.png
/home/ec2-user/hatena_demo/assets/test-image-red.PNG


If everything is OK, enter "yes" or "y".
If you don't like it, enter "no" or "n".

y
-----
Success!
URL: "アップロード先のURL"
-----

-----
Success!
URL: "アップロード先のURL"
-----

All Done.
Good bye!
```

### 確認

アップロード先のはてなブログにアクセスして、"下書き" 一覧を確認してください。

"test.md" という記事が見えるはずです。

[](automating-hatena-blog_1.png)


続いてはてなフォトライフにアクセスして、画像ファイルのアップロードを確認しましょう。

以下のURLでアクセスいただけます。
```text
https://f.hatena.ne.jp/"Your_Hatena_ID"
```

"hatena_demo"フォルダが出来ているので、開いてください。

中身が以下になっていれば、アップロード成功です!
[](automating-hatena-blog_2.png)

### 後片付け

今回アップロードした記事/画像を削除しましょう。

やり方がわからない方は、以下参考にしていただけると幸いです。

[記事を管理する-はてなブログヘルプ|https://help.hatenablog.com/entry/entries]
[はてなブログの画像を削除する方法→はてなフォトライフから削除する|https://yoshizo.hatenablog.com/entry/how-to-delete-hatenablog-image]

---

必要なければ作成したフォルダも削除しましょう。
```bash
$ rm -r hatena_demo
$ rm -r hatena_src
```

---

今回入れたモジュールも必要なければアンインストールしてください。

```bash
sudo pip3 uninstall bs4
sudo pip3 uninstall lxml
sudo pip3 uninstall requests
```

## まとめ

