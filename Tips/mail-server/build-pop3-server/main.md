## はじめに

今回はPOP3サーバを構築して、受信したメールを取得してみます。

本記事は第２回目の記事になるのでご注意ください。

- [【第1回】【EC2】PostfixでシンプルなSMTPサーバを構築してみる](https://blog.serverworks.co.jp/build-smtp-server)
- [【第2回】【EC2】Dovecotを使って、POP3サーバを構築してみる](https://blog.serverworks.co.jp/build-pop3-server)　***← イマココ***
- [【第3回】Postfixでメールリレーを試してみる](https://blog.serverworks.co.jp/mail-relay)
- [【第4回】SMTP認証を実装して、メールリレーをセキュアにする](https://blog.serverworks.co.jp/set-smtp-auth)

記事目安...10分

[:contents]

## ゴール

以下ができることがゴールです。

- [前回記事](https://blog.serverworks.co.jp/build-smtp-server)で作成したサーバに、Dovecotをインストールして、POP3サーバを構築する。
- [前回記事](https://blog.serverworks.co.jp/build-smtp-server)で受信したメールをPOP3で取得する

## 用語

#### POP3
メールサーバからメールを取得する際に使用するプロトコル。  
110番ポートを使用します。

また、POP3はメールを取得する都合上、デフォルトでユーザ認証機能があります

#### Dovecot
Unix系動作する、POP3での通信を行う際に必要なサーバソフト。

## POP3の通信許可

まずは、POP3でのインバウンド通信を許可します。

[前回記事](https://blog.serverworks.co.jp/build-smtp-server)で作成した、 セキュリティグループ:*****sg_YYYYMMDD-smtp-handson-server***** に以下インバウンド通信を許可してください。

|Rule|Type|Port|Source|Detail|
|---|---|---|---|---|
|Inbound|POP3|110|0.0.0.0/0|POP3 port|

## Dovecotの導入

[前回記事](https://blog.serverworks.co.jp/build-smtp-server)で作成した、EC2:*****YYYYMMDD-smtp-handson-server***** にログインしてください。

---

まずは、Dovecotをインストールします。

```bash
$ sudo yum install -y dovecot
```

---

続いて、設定を編集します。

まずは、主設定ファイルの *****dovcot.conf***** を編集します。

```bash
$ sudo cp -a /etc/dovecot/dovecot.conf /etc/dovecot/dovecot.conf.`date +"%Y%m%d"`
$ ls /etc/dovecot/
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

続いて、*****10-mail.conf*****を編集します。  
メール取得時の主設定を記述します。

```bash
$ sudo cp -a /etc/dovecot/conf.d/10-mail.conf /etc/dovecot/conf.d/10-mail.conf.`date +"%Y%m%d"`
$ ls /etc/dovecot/conf.d
$ sudo vi /etc/dovecot/conf.d/10-mail.conf

---
#   mail_location = maildir:~/Maildir
→mail_location = maildir:~/Maildir //メールボックスの場所を定義します。
---

$ sudo diff /etc/dovecot/conf.d/10-mail.conf /etc/dovecot/conf.d/10-mail.conf.`date +"%Y%m%d"`
```

---

今度は、*****10-auth.conf*****を編集します。  
このファイルはDovecotの認証周りを設定します。

```bash
$ sudo cp -a /etc/dovecot/conf.d/10-auth.conf /etc/dovecot/conf.d/10-auth.conf.`date +"%Y%m%d"`
$ ls /etc/dovecot/conf.d
$ sudo vi /etc/dovecot/conf.d/10-auth.conf

---
#disable_plaintext_auth = yes
→ disable_plaintext_auth = no //平文でのログインを許可します。
---

$ sudo diff /etc/dovecot/conf.d/10-auth.conf /etc/dovecot/conf.d/10-auth.conf.`date +"%Y%m%d"`
```

---
さらに、*****10-ssl.conf*****を編集します。  
このファイルはDovecotのSSL接続を設定します。

```bash
$ sudo cp -a /etc/dovecot/conf.d/10-ssl.conf /etc/dovecot/conf.d/10-ssl.conf.`date +"%Y%m%d"`
$ ls /etc/dovecot/conf.d
$ sudo vi /etc/dovecot/conf.d/10-ssl.conf

---
#ssl = required
ssl = yes //クライアントとの接続時SSLを必須としない。(*1)
---

$ sudo diff /etc/dovecot/conf.d/10-ssl.conf /etc/dovecot/conf.d/10-ssl.conf.`date +"%Y%m%d"`
```

*1. 今回は検証のため、SSL接続しなくても大丈夫な設定にしています。

---
最後に、*****10-master.conf***** を編集します。  
ここでは、各ポートでの待ち受け設定を行います。

```
$ sudo cp -a /etc/dovecot/conf.d/10-master.conf /etc/dovecot/conf.d/10-master.conf.`date +"%Y%m%d"`
$ ls /etc/dovecot/conf.d
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

ここまで出来たら ***doveconf***(*2) コマンドで設定を確認しましょう。

```bash
$ doveconf -a
$ doveconf -n
```

*2. ***doveconf***コマンド

|Option|Detail|
|---|---|
|a|読み込まれる全ての設定を表示します|
|n|デフォルト値と異なる全ての設定を表示します|

参考: [Doveconf](https://wiki.dovecot.org/Tools/Doveconf)

---

変更した値がきちんと読み込まれていることを確認したら、Dovecotを起動しましょう。

```bash
$ sudo systemctl start dovecot
$ systemctl status dovecot
$ ss -nlt4
LISTEN   0         100                 0.0.0.0:110              0.0.0.0: (*****3)
```

## 動作確認

[前回記事](https://blog.serverworks.co.jp/build-smtp-server)で、*****YYYYMMDD-smtp-handson-server***** にメールを送信しているので、そちらを確認しましょう。

---

POP3を飛ばすクライアントですが、ローカルPCで実行して頂いても結構です。

CloudFormationテンプレートを用意したので、こちらでPOP3クライアント用サーバを構築していただいてもかまいません。(ブログはこちらを前提に進めます。)

|リソース|スタック名|URL|
|---|---|
|EC2:*****YYYYMMDD-smtp-handson-pop3-client*****|smtp-handson-pop3-client-YYYYMMDD|[cfn-template-ec2](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/build-pop3-server/templates/cfn-template-ec2.yml)|

*3. 今回立てるEC2の詳細は以下です。

- YYYYMMDD-smtp-handson-pop3-client

  |Key|Value|
  |---|---|
  |OS|AmazonLinux2|
  |Inbound|SSH:0.0.0.0/0|
  |Role|Pop3 Client|

---

*****YYYYMMDD-smtp-handson-pop3-client***** にSSH接続します。

---

今回はtelnetコマンドで接続するので、インストールを行います。

```bash
$ sudo yum install -y telnet
$ which telnet
```

---

では、telnetコマンドで *****YYYYMMDD-smtp-handson-server***** にPOP3接続します。

```bash
$ telnet <*****YYYYMMDD-smtp-handson-server***** のドメイン名> 110
user muser //ユーザ認証を開始
pass <muserのパスワード>
list //取得したメールの一覧を確認する
retr 1　//一つ目のメールを取得する
quit //通信を終了する
```

〇凡例

```bash
[ec2-user@ip-192-168-2-64 ~]$ telnet mail.example.com 110
Trying xxx.xxx.xxx.xxx...
Connected to mail.example.com.
Escape character is '^]'.
+OK Dovecot ready.
user muser
+OK
pass xxx
+OK Logged in.
list
+OK 1 messages:
1 5738
.
retr 1
+OK 5738 octets
<~省略~>
.
quit
+OK Logging out.
Connection closed by foreign host.
```

## リソースの削除

今回作成したリソースはもう使わないので、削除しましょう。

以下、CloudFormationスタックを削除することで完了します。

|削除されるリソース|スタック名|
|---|---|
|EC2:*****YYYYMMDD-smtp-handson-pop3-client*****|smtp-handson-pop3-client-YYYYMMDD|

---

ほかの記事に進まない場合は、以下を参考に今まで作ったリソースを削除ください。

[削除するリソース一覧について](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/cfn-delete.md#%E7%AC%AC2%E5%9B%9Eec2dovecot%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6pop3%E3%82%B5%E3%83%BC%E3%83%90%E3%82%92%E6%A7%8B%E7%AF%89%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B)

## まとめ

これでPOP3サーバの構築が完了しました。

POP3は受信するためのプロトコルと思いがちですが、実際は受信したメールを取得する際のプロトコルです。  
実際に触っていただいたことで理解していただけたのではないでしょうか? 

ただセキュリティ面はまだ脆弱なため、セキュリティを強化する方法もどこかで書きたいと思います。

ご覧いただきありがとうございました。
