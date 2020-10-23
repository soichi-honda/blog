## はじめに
本記事では、Postfixを使ったメールリレーの実装にチャレンジします。  

以下記事の実施を前提としているので、先にこちらを読んでいただけると幸いです。

[【初心者向け】【Route53+EC2】PostfixでシンプルなSMTPサーバを構築してみる](https://blog.serverworks.co.jp/build-smtp-server)

記事目安...15分

[:contents]

## ゴール
以下ができることがゴールです。

- Mail Clientから送信したメールを、Mail Server経由で自分のメールアドレス宛に届ける

[f:id:swx-sugaya:20200914103312p:plain]


## 用語
#### メールリレー
メール送信時に、複数サーバを経由してメールを届けること。  
直接配送の時に比べて以下メリットがある。

- メール周りの運用をリレーサーバに集中できる(SPFレコード設定, パブリック証明書の設置など)
- リレーサーバのみをパブリックに晒せばいいため、セキュリティが向上する

## 事前作業
まずはCloudFormationテンプレートを用いて、下記の環境を作成しましょう。

[f:id:swx-sugaya:20200914103318p:plain]

---

[前回の記事](https://blog.serverworks.co.jp/build-smtp-server)で途中までは環境ができていると思うので、以下テンプレートファイルを流して環境にリソース追加を行ってください。(*1)

|作成リソース|スタック名|テンプレートURL|
|---|---|---|
|PrivateSubnet|smtp-handson-pri-sub-YYYYMMDD|[cfn-template-pri-sub.yml](https://github.com/sugaya0204/blog/tree/Public/Tips/mail-server/mail-relay/templates/cfn-template-pri-sub.yml)|
|EC2:"YYYYMMDD-smtp-handson-client"|smtp-handson-client-YYYYMMDD|[cfn-template-client.yml](https://github.com/sugaya0204/blog/tree/Public/Tips/mail-server/mail-relay/templates/cfn-template-client.yml)|

*1. CloudFormationテンプレートの流し方は、以下を参考ください。

参考:[【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 後編](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn-2)

*2. 今回立てるEC2の詳細は以下です。

- YYYYMMDD-smtp-handson-client

  |Key|Value|
  |---|---|
  |OS|AmazonLinux2|
  |Inbound|SSH: "0.0.0.0/0"|
  |Role|Mail Client|

## Postfixの設定変更

前回作成した "YYYYMMDD-smtp-handson-server" にSSHアクセスしてください。

---

Postfixの設定ファイルで、"YYYYMMDD-smtp-handson-client" からのリレーを許可します。

```bash
$ sudo cp -a /etc/postfix/main.cf /etc/postfix/main.cf.`date +"%Y%m%d"` //日付でバックアップを取得
$ ls /etc/postfix/main.cf.`date +"%Y%m%d"`　//取得したバックアップを確認
$ sudo vi /etc/postfix/main.cf

---
mynetworks=<"YYYYMMDD-smtp-handson-client"のPrivateIPアドレス> (*3)
---

$ sudo diff /etc/postfix/main.cf /etc/postfix/main.cf.`date +"%Y%m%d"` //差分を確認するコマンド
```

〇凡例

```text
mynetworks=xxx.xxx.xxx.xxx/32
```

*3. "mynetworks"について  
リレーを許可するサーバを定義するパラメータです。  
許可したいサーバのIPアドレスを値に入力します。

参考: [Postfix設定パラメータ](http://www.postfix-jp.info/trans-2.2/jhtml/postconf.5.html)

---

設定が間違ってないか確認して、問題なければ再起動を行います。

```bash
$ postconf -n
$ sudo systemctl restart postfix
$ systemctl status postfix
```

## 動作確認
### メールの送信
"YYYYMMDD-smtp-handson-client" にSSHアクセスしてください。(*4)

*4. PrivateSubnetにあるため、"YYYYMMDD-smtp-handson-server"　を踏み台にしてください。

---

"YYYYMMDD-smtp-handson-client" からの送信には "mail" コマンドを使用します。

まずダウンロードしましょう

```
$ sudo yum install -y mailx
$ which mail //確認用
```

---

では、メールを送信します。ご自身の所有するメールアドレスに向けてみましょう。  
今回は、Gmailに向けて送信してみます。

```bash
$ echo "smtp-handson" | mail -v -s "Relay Success" -S smtp=smtp://<"YYYYMMDD-smtp-handson-server"のPrivateIPアドレス>:25 -r hogehoge@fugafuga.com <送信先メールアドレス>
```

〇凡例

```bash
$ echo "smtp-handson" | mail -v -s "Relay Success" -S smtp=smtp://xxx.xxx.xxx.xxx:25 -r hogehoge@fugafuga.com example@gmail.com
Resolving host xxx.xxx.xxx.xxx . . . done.
Connecting to xxx.xxx.xxx.xxx:25 . . . connected.
220 mail.example.com ESMTP Postfix
>>> HELO ip-192-168-2-227.ap-northeast-1.compute.internal
250 mail.example.com
>>> MAIL FROM:<hogehoge@fugafuga.com>
250 2.1.0 Ok
>>> RCPT TO:<example@gmail.com>
250 2.1.5 Ok
>>> DATA
354 End data with <CR><LF>.<CR><LF>
>>> .
250 2.0.0 Ok: queued as 92D2FC01537
>>> QUIT
221 2.0.0 Bye
```

### メールの受信確認

送ったメールアドレスのメールボックスを確認してみてください。

[f:id:swx-sugaya:20200914103324p:plain]

届いてますね！

---

ほんとにリレーがされているのか確認するために、"YYYYMMDD-smtp-handson-server" にSSHして、 "/var/log/maillog" を見てみましょう。

```bash
$ sudo less /var/log/maillog
```

以下のようなログが出ていればOKです！

```text
Sep 13 14:18:16 ip-192-168-2-44 postfix/smtpd[2733]: connect from ip-192-168-2-227.ap-northeast-1.compute.internal[192.168.2.227]
Sep 13 14:18:16 ip-192-168-2-44 postfix/smtpd[2733]: 65182C01537: client=ip-192-168-2-227.ap-northeast-1.compute.internal[192.168.2.227]
Sep 13 14:18:16 ip-192-168-2-44 postfix/cleanup[2736]: 65182C01537: message-id=<5f5e2a28.TJbGiIEO6aAQotCT%hogehoge@fugafuga.com>
Sep 13 14:18:16 ip-192-168-2-44 postfix/qmgr[2731]: 65182C01537: from=<hogehoge@fugafuga.com>, size=605, nrcpt=1 (queue active)
Sep 13 14:18:16 ip-192-168-2-44 postfix/smtpd[2733]: disconnect from ip-192-168-2-227.ap-northeast-1.compute.internal[192.168.2.227]
Sep 13 14:18:18 ip-192-168-2-44 postfix/smtp[2737]: 65182C01537: to=<example@gmail.com>, relay=aspmx.l.google.com[64.233.189.26]:25, delay=1.7, delays=0.05/0/0.42/1.2, dsn=2.0.0, status=sent (250 2.0.0 OK  1600006698 u9si6432770pgm.64 - gsmtp)
Sep 13 14:18:18 ip-192-168-2-44 postfix/qmgr[2731]: 65182C01537: removed
```

---

Gmailだと以下からメール経路を確認できるので、やってみてください。

[f:id:swx-sugaya:20200914103330p:plain]

---


## リソースの削除

必要なければ、今回作成したリソースを削除しましょう。

以下、CloudFormationスタックを全て削除することで完了します。

*5. 別の記事に進む場合は、まだ消さないでください。

- [【初心者向け】SMTP認証を実装して、メールリレーをセキュアにする](https://blog.serverworks.co.jp/set-smtp-auth)


|削除されるリソース|スタック名|
|---|---|
|PrivateSubnet|smtp-handson-pri-sub-YYYYMMDD|
|EC2:"YYYYMMDD-smtp-handson-client"|smtp-handson-client-YYYYMMDD|

## まとめ

ということでメールリレーを実装してみました。

メールサーバの運用を楽にするために、メールリレーは必須なのでぜひやってみてください！

ご覧いただきありがとうございました。
