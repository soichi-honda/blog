## はじめに

自分用に、自己証明書を発行するコマンドについてまとめました。

自己証明書を発行する仕組みについては以下ブログをご覧いただけると幸いです。

[【初心者向け】自己証明書を発行する流れについてまとめてみた](https://blog.serverworks.co.jp/self-cert-validation)

記事目安...5分

[:contents]

## 自己証明書を発行するコマンド集

#### 前提条件
それぞれ以下と仮定します。

|Key|Value|
|---|---|
|ホストネーム|hogehoge.com, hogehoge2.com|
|IPアドレス|10.2.2.xxx|
|ファイルの置き場|*/home/hogehoge/self*|

---

- openssl コマンドが入っている確認します  
```bash
$ which openssl
```

---

- フォルダを作成して、移動します。  
**以後このフォルダ内で作業を行います**。
```bash
$ mkdir /home/hogehoge/self/
$ cd /home/hogehoge/self/
```

#### 秘密鍵ファイルの作成

**秘密鍵ファイル( *server.key* )を作成** します
```bash
$ openssl genrsa -out server.key 2048
$ less server.key //確認用
```

#### 署名要求ファイルの作成

作成した秘密鍵ファイル( *server.key* )から **署名要求ファイル( *server.csr* )を作成** します
```bash
$ openssl req -new -key server.key \
-out server.csr
```
対話型モードになるので、各項目にはそれぞれ適切な値を入れてください。  
※ "Common Name" には、名前解決出来るサーバのホスト名か IP アドレスを入れてください。  
ここが一致しないと、正しいサーバとして認証されません。

```bash
Country Name (2 letter code) [XX]:JP
State or Province Name (full name) []:Tokyo
Locality Name (eg, city) [Default City]:Shinjuku
Organization Name (eg, company) [Default Company Ltd]:TestCompany
Organizational Unit Name (eg, section) []:
Common Name (eg, your name or your server's hostname) []:hogehoge.com
Email Address []:
 
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```
作成した署名要求ファイル( *server.csr* )の中身を確認します。
```bash
$ openssl req -text -in server.csr -noout
```

#### (Conditional)SAN 設定用テキストファイルの作成

サーバ証明書の Common Name に **複数のサーバホスト名, IP アドレスを入力したい場合** のみ、 SAN 設定用テキストファイル( *subjectnames.txt* )　を作成してください。

```bash
$ vi subjectnames.txt
```
```
subjectAltName = DNS: hogehoge2.com, IP: 10.2.2.xxx
```

#### 自己証明書の作成
秘密鍵ファイル( *server.key* ) で、署名要求ファイル( *server.csr* )に電子署名を行い、　**自己証明書( *server.crt* )を作成** します。  
※今回は、3650 日(=10年間) を有効期限として作成します。
```bash
$ openssl x509 -req -days 3650 -in server.csr \
-signkey server.key \
-out server.crt

// SAN 設定用テキストファイル( *subjectnames.txt* ) を作成している場合はこちら
$ openssl x509 -req -days 3650 -in server.csr \
-signkey server.key \
-out server.crt \
-extfile subjectnames.txt
```
中身を確認します。
```bash
$ openssl x509 -text -in server.crt -noout
```

## おわりに

ご覧いただきありがとうございました。
