## はじめに

今回はPOP3サーバを構築して、受信したメールを取得してみます。

以下記事をやっていることが前提となるので、まだの人はこちらからやってください！

[【初心者向け】【Route53+EC2】PostfixでシンプルなSMTPサーバを構築してみる](https://blog.serverworks.co.jp/build-smtp-server)

記事目安...10分

[:contents]

## ゴール

以下ができることがゴールです。

- 前回記事で受信したメールをPOP3で取得する

## 用語

#### POP3
メールサーバからメールを取得する際に使用するプロトコル。  
110番ポートを使用します。

また、POP3はメールを取得する都合上、デフォルトでユーザ認証機能があります

#### Dovecot
Unix系動作する、POP3での通信を行う際に必要なサーバソフト。

## POP3の通信許可

まずは、POP3でのインバウンド通信を許可します。

前回作成した セキュリティグループ:"sg_YYYYMMDD-smtp-handson-server" に以下インバウンド通信を許可してください。

|Rule|Type|Port|Source|
|---|---|---|---|
|Inbound|POP3|110|0.0.0.0/0|

## Dovecotの導入

前回記事で作成した、EC2:"YYYYMMDD-smtp-handson-server" にログインしてください。

---

まずは、Dovecotをインストールします。

```bash
$ sudo yum install -y dovecot
```

---

続いて、設定を編集します。

まずは、主設定ファイルの "dovcot.conf" を編集します。

```bash
$ sudo cp -a /etc/dovecot/dovecot.conf /etc/dovecot/dovecot.conf.`date +"%Y%m%d"`
$ sudo vi /etc/dovecot/dovecot.conf

---
#protocols = imap pop3 lmtp
→
#protocols = imap pop3 lmtp
protocols = pop3 //POP3での通信を許可します。
---

$ sudo diff /etc/dovecot/dovecot.conf /etc/dovecot/dovecot.conf.`date +"%Y%m%d"`
```

---

続いて、"10-mail.conf"を編集します。  
このファイルはdovecot.confに読み込まれるファイルです。メール取得時の主設定を記述します。

```bash
$ sudo cp -a /etc/dovecot/conf.d/10-mail.conf /etc/dovecot/conf.d/10-mail.conf.`date +"%Y%m%d"`
$ sudo vi /etc/dovecot/conf.d/10-mail.conf

---
mail_location = maildir:~/Maildir
auth_mechanisms = plain
---

$ sudo diff -a /etc/dovecot/conf.d/10-mail.conf /etc/dovecot/conf.d/10-mail.conf.`date +"%Y%m%d"`
```

*. 各パラメータについて

|Key|Value|
|---|---|
|mail_location|メールボックスの場所を定義します。|
|auth_mechanisms|認証メカニズムを定義します。  "plain login"は平文パスワードの送信を許可します。|

参考: [Mail Location Settings](https://doc.dovecot.org/configuration_manual/mail_location/)  
[authentication_mechanisms](https://doc.dovecot.org/configuration_manual/authentication/authentication_mechanisms/)

---
最後に、"10-master.conf" を編集します。  
ここでは、各ポートでの待ち受け設定を行います。

```
$ sudo cp -a /etc/dovecot/conf.d/10-master.conf /etc/dovecot/conf.d/10-master.conf.`date +"%Y%m%d"`
$ sudo vi /etc/dovecot/conf.d/10-master.conf

---
service pop3-login {
  inet_listener pop3 {
    #port = 110
→    port = 110 //POP3の場合、110番ポートでリッスンします。
　}
---

$ sudo diff /etc/dovecot/conf.d/10-master.conf /etc/dovecot/conf.d/10-master.conf.`date +"%Y%m%d"`
```

---

ここまで出来たら "doveconf"(*) コマンドで設定を確認しましょう。

```bash
$ doveconf -a
$ doveconf -n
```

*. "doveconf"コマンド

|Option|Detail|
|---|---|
|a|読み込まれる全ての設定を表示します|
|n|デフォルト値と異なる全ての設定を表示します|

参考: [Doveconf](https://wiki.dovecot.org/Tools/Doveconf)
---

エラー等がなければ、Dovecotを起動しましょう。

```bash
$ sudo systemclt restart dovecot
$ systemctl status dovecot
$ ss -nlt4

```

## 動作確認

前回、"YYYYMMDD-smtp-handson-server" にメールを送信しているので、そちらを確認しましょう。

---

POP3を飛ばすクライアントですが、ローカルPCで実行して頂いても結構です。

CloudFormationテンプレートを用意したので、こちらでPOP3クライアント用サーバを構築していただいてもかまいません。(ブログはこちらを前提に進めます。)

|リソース|スタック名|URL|
|---|---|
|EC2:"YYYYMMDD-smtp-handson-pop3-client"|smtp-handson-pop3-client-YYYYMMDD|[cfn-template-ec2]()|

---

"YYYYMMDD-smtp-handson-pop3-client" に接続します。

```bash

```
## リソースの削除

今回作成したリソースを削除しましょう。

以下、CloudFormationスタックを全て削除することで完了します。

|削除されるリソース|スタック名|
|---|---|
|SSMパラメータ|xxx-handson-common-YYYYMMDD|
|VPC, PublicSubnet|xxx-handson-vpc-YYYYMMDD|
|EC2:"YYYYMMDD-xxx-handson-server"|xxx-handson-server-YYYYMMDD|

## まとめ

ご覧いただきありがとうございました。
