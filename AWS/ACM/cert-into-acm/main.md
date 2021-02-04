## はじめに

ACM に登録している外部証明書のインポート/再インポートを大量にやらなければいけない、そんな時に役立つスクリプト書いてみました。

※今回のスクリプトは、証明書チェーンを含む証明書のインポート/再インポートには対応していないので、その場合は若干改修する必要がございます。

記事目安...10分

[:contents]


## 使用場面

以下ような場面に有効なスクリプトとなっています。

* 特定リージョンで、外部から ACM に証明書を 1~n 枚 インポートしたい
* 特定リージョンにある ACM 証明書の有効期限が切れるので、1~n 枚 再インポートしたい
* 上記の 2つを同時に行いたい。

※ **証明書チェーンを含む証明書のインポート/再インポートには対応していません。**

## 出力結果

* インポート/再インポートした 証明書の **ドメイン名, ARN, 有効期限** が CSVファイルに出力されます。

## スクリプトの中身

[reimport-cert-info-acm.sh](https://github.com/sugaya0204/blog/blob/Public/AWS/ACM/cert-into-acm/src/import-and-reimport-cert-into-acm.sh) をご参考ください。

## 実行環境

以下の AWSCLI バージョンでの動作が確認済みです。

```sh
$ aws --version
aws-cli/2.0.58 Python/3.7.3 Linux/4.19.128-microsoft-standard exe/x86_64.ubuntu.20
```

## 使い方

### 事前準備

事前作業として以下を行います。

* 証明書と鍵ファイルの用意
* 入力する CSV ファイルの作成
* 変数の定義

---

#### 証明書と鍵ファイルの用意

1. 各証明書ディレクトリをまとめる作業ディレクトリを用意してください。  
ex) /home/ec2-user/certs
1. 作業ディレクトリの下に 証明書に配置する `ドメイン名` で証明書ディレクトリを作成します。  
ex) /home/ec2-user/certs/hoge.example.com
1. インポート/再インポートする証明書および、鍵ファイルを準備して、**項目 2** で作成した証明書ディレクトリに配置します。  
ファイル名はどちらも `ドメイン名+拡張子` としてください。
自己証明書を作成して試したい方は [こちら](https://blog.serverworks.co.jp/make-self-cert) をご参考ください！  
ex)   
鍵ファイル: /home/ec2-user/certs/hoge.example.com/hoge.example.com.key  
証明書ファイル: /home/ec2-user/certs/hoge.example.com/hoge.example.com.crt  
1. **項目 2 ~ 3** をインポート/再インポートしたい証明書数分繰り返します。

#### 入力する CSV ファイルの作成

CSV ファイルを作成してインポート/再インポートしたい証明書の全ドメイン名を記述します。

CSV ファイルの置場はどこでも問題ないですが、作業ディレクトリ内に置くといいと思います。

例えば、hoge.example.com, fuga.example.com の両方をインポート/再インポートしたい場合は、以下の用に記述します

```csv
hoge.example.com
fuga.example.com  

```

※ スクリプト内で使用している *while read* は改行コードがある行しか読み込まないため、**最終行の末尾が改行コードになっていることを確認してください。**

#### スクリプトのアップロード

スクリプトを `import-and-reimport-cert-into-acm.sh` というファイル名で配置してください。  
置く場所に制限はありませんが、先ほど作成した作業ディレクトリに配置するのが推奨です。

#### 変数の定義

スクリプトを開いて、以下部分を定義します。

```sh
# ユーザ定義
## 作業ディレクトリの定義
base_dir_path=""

## 鍵ディレクトリ/ファイルのサフィックス定義
key_file_suffix=".key"

## 証明書ディレクトリ/ファイルのサフィックス定義
cert_file_suffix=".crt"

## リージョンの定義
region=""
```

※ `base_dir_path` には、**"証明書と鍵ファイルの用意"の項目 1** で作成した作業ディレクトリのパスを入れてください。

〇凡例
```sh
# ユーザ定義
## 作業ディレクトリの定義
base_dir_path="/home/ec2-user/certs"

## 鍵ディレクトリ/ファイルのサフィックス定義
key_file_suffix=".key"

## 証明書ディレクトリ/ファイルのサフィックス定義
cert_file_suffix=".crt"

## リージョンの定義
region="ap-northeast-1"
```

### スクリプトの実行

スクリプトを *bash* コマンドで実行します。この時、第一引数に、作成した CSV ファイルを渡してください。

```sh
$ bash import-and-reimport-cert-into-acm.sh <CSVファイル>
```

〇実行例
```sh
$ bash import-and-reimport-cert-into-acm.sh /home/ec2-user/certs/input.csv
---Start hoge.example.com---
---Start fuga.example.com---
---End---
```

### 出力の確認

* 作業ディレクトリに **output.csv** が作成され、処理に成功すると、出力結果が書き込まれます。
* インポート/再インポートの段階で、エラーが発生した場合は、作業ディレクトリ内の **error.log** にエラー出力が書き込まれます。

## その他注意事項

* 1年間にインポート/再インポートできる証明書数は、リージョンごとに限りがあります。  
上限を超えると以下のようなエラーが出力されます。
```sh
An error occurred (LimitExceededException) when calling the ImportCertificate operation (reached max retries: 2): You have imported the maximum number of xx certificates in the last year.
```
参考: https://docs.aws.amazon.com/ja_jp/acm/latest/userguide/acm-limits.html

## まとめ

外部からの大量インポート/再インポートを行う場面で是非お使いください。

ご覧いただきありがとうございました