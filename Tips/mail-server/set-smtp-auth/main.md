## はじめに

前回メールリレーの実装を行いましたが、リレーサーバが増えるごとに ***mynetworks*** パラメータを変更する運用はあまり柔軟ではありません。  
そこでSMTPリレーに認証機能を付けて、より柔軟かつセキュアに運用できるようにしていきましょう。

以下記事をやっていることが前提となるので、こちらをやっていると理解が早くなると思います。

[【初心者向け】Postfixでメールリレーを試してみる](https://blog.serverworks.co.jp/mail-relay)

記事目安...15分

[:contents]


## 用語
#### SMTP認証
SMTP で送信を行う前に認証を行う。これにより意図しないユーザが SMTP サーバを使用して、不正リレーすることを防ぐ。  
認証には SASL 認証を使うことが多い。

#### サブミッションポート
メール送信にSMTP認証を実装する際、よく使用されるポート。***587番ポート*** を用いる。  
SMTP の well known ポートである25番ポートで SASL 認証を有効にしてしまうと、対応していないアプリケーションが軒並みメールを送受信できなくなってしまうため、わざわざ別で用意している。

#### SASL
「Simple Authentication and Security Layer」の略。認証やセキュリティに関する処理を行うための層を指す。  
SASL により認証部分をコンポーネント化できるため、アプリケーションごとに独自の認証方式を採用する必要がなくなる。

#### Cyrus SASL
Cyrus 社から出ている SASL を提供するパッケージソフト。

参考: [Cyrus SASL](https://www.cyrusimap.org/sasl/)

## ゴール
今回は、以下ができることがゴールです。

- SMTP認証を実装する
- SMTP認証を行った後、メールがリレー送信できることを確認する

## 構成図

[前回記事](https://blog.serverworks.co.jp/mail-relay) まで終わっていると以下の構成になっているはずです。

[f:id:swx-sugaya:20201021115129p:plain]

## 作業
### ポートの開放
セキュリティグループ ***sg_YYYYMMDD-smtp-handson-smtp-server*** (*) で以下ポートを開放してください。

|Rule|Type|Protocol|Port|Source/Destination|
|---|---|---|---|---|
|inbound|カスタムTCP|TCP|587|0.0.0.0/0|

*. *YYYYMMDD* にはリソース作成時の日付が入ります。

### SASLの導入
#### 必要パッケージのインストール
yumで Cyrus SASL パッケージをインストールします。
```bash
$ sudo yum install cyrus-sasl cyrus-sasl-lib cyrus-sasl-plain
```

#### SASL側の設定

まず、Postfixが利用する認証方式をSASLにします。

今回は認証情報の格納先に ***sasldb*** を用意して、認証情報を管理します。

```bash
$ sudo cp -a /etc/sasl2/smtpd.conf /etc/sasl2/smtpd.conf.`date +"%Y%m%d"`
$ sudo ls /etc/sasl2/smtpd.conf.`date +"%Y%m%d"`
$ sudo vi /etc/sasl2/smtpd.conf
---
pwcheck_method: auxprop　//認証方法を決定する。"auxprop" だと sasldb を認証に使用します。
mech_list: PLAIN //認証情報の送信に平文を利用する
---
$ sudo diff /etc/sasl2/smtpd.conf /etc/sasl2/smtpd.conf.`date +"%Y%m%d"`
```

#### sasldb の作成

sasldb を作成して、ユーザ認証情報を格納します

```bash
$ sudo saslpasswd2 -c -u <メールドメイン> <ユーザ名> //新規ユーザー作成
$ sudo sasldblistusers2 //ユーザー一覧表示
```

〇凡例
```bash
$ sudo saslpasswd2 -c -u example.com smtp-auth //新規ユーザー作成
```

---

sasldb のパーミッションも確認します。以下と同じにしてください。
```
$ ll /etc/sasldb2
-rw-r----- 1 root postfix 12288 Oct 20 08:41 /etc/sasldb2
```

#### Postfix側の設定

Postfix が SASL を使用して SMTP 認証を行うよう設定を追加します。

まず ***main.cf*** を編集して、①メールリレー元の制限 ② SMTP 認証の有効化 をします。

```bash
$ sudo cp -a /etc/postfix/main.cf /etc/postfix/main.cf.`date +"%Y%m%d"`
$ ls /etc/postfix/main.cf.`date +"%Y%m%d"`
$ sudo vi /etc/postfix/main.cf
---
// 最終行に追加
# relay-control
smtpd_recipient_restrictions = permit_mynetworks, reject_unauth_destination (*1)

# smtp-auth
smtpd_sasl_auth_enable = yes
---
$ sudo diff /etc/postfix/main.cf /etc/postfix/main.cf.`date +"%Y%m%d"`
$ postconf -n //確認用
```
*1. smtpd_recipient_restrictions　について

- permit_mynetworks → mynetworks パラメータで許可されたサーバのみ SMTP リレーを許可する
- reject_unauth_destination → $mydestination で承認されていないドメインへの SMTP 送信を許可しない。

---

続いて ***master.cf*** を変更し、サブミッションポートでリッスンするようにしましょう。

```bash
$ sudo cp -a /etc/postfix/master.cf /etc/postfix/master.cf.`date +"%Y%m%d"`
$ ls /etc/postfix/master.cf.`date +"%Y%m%d"`
$ sudo vi /etc/postfix/master.cf
---
#submission inet n       -       n       -       -       smtpd
submission inet n       -       n       -       -       smtpd
#  -o smtpd_recipient_restrictions=permit_sasl_authenticated,reject
→  -o smtpd_client_restrictions=permit_sasl_authenticated,reject　//サブミッションポートでは、SMTP認証を行っていないユーザ以外は拒否します
---
$ sudo diff /etc/postfix/master.cf /etc/postfix/master.cf.`date +"%Y%m%d"`
```

---

Postfix 再起動します。

```
$ systemctl status postfix
$ sudo systemctl restart postfix
$ systmectl status postfix
$ ss -nlt4 //587番ポートが動いてることを確認する
```


#### SASLの起動

SASL を起動します。

```
$ sysmtctl status saslauthd
$ sudo systemctl start saslauthd
$ sysmtctl status saslauthd
```

## 動作確認
#### リレー元サーバの準備
[前回記事](https://blog.serverworks.co.jp/mail-relay) で作ったリソースを消してしまった人は、こちらのテンプレートを流してください。

|作成リソース|スタック名|テンプレートURL|
|---|---|---|
|PrivateSubnet|smtp-handson-pri-sub-YYYYMMDD|[cfn-template-pri-sub.yml](https://github.com/sugaya0204/blog/tree/Public/Tips/mail-server/mail-relay/templates/cfn-template-pri-sub.yml)|
|EC2:"YYYYMMDD-smtp-handson-client"|smtp-handson-client-YYYYMMDD|[cfn-template-client.yml](https://github.com/sugaya0204/blog/tree/Public/Tips/mail-server/mail-relay/templates/cfn-template-client.yml)|

*2. CloudFormation テンプレートの流し方は、以下を参考ください。

参考:[【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 後編](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn-2)

*3. 今回立てる EC2 の詳細は以下です。

- YYYYMMDD-smtp-handson-client

  |Key|Value|
  |---|---|
  |OS|AmazonLinux2|
  |Inbound|SSH: "0.0.0.0/0"|
  |Role|Mail Client|

#### SMTPリレー送信

*** YYYYMMDD-smtp-handson-client *** にSSHアクセスしてください。*4

*4. PrivateSubnetにあるため、 ***YYYYMMDD-smtp-handson-server***　を踏み台にしてください。

---

***mail*** コマンドを使用して、リレー送信を行います。

```bash
$ which mail //確認
$ sudo yum install mailx //入ってない場合は実行してください
```

今回は、SMTP認証を通る必要があるので、 ***.mailrc*** という mail コマンドの設定ファイルにあらかじめ定義します。

```bash
$ vi ~/.mailrc
---
set smtp-auth=plain
set smtp-auth-user=<sasldbに登録したSMTP-AUTHユーザ名>
set smtp-auth-password=<ユーザに設定したパスワード>
---
```

メールを送信します。送信したら、送信先のメールフォルダを確認してみてください!

```
$ echo "smtp-handson" | mail -v -s "Relay Success via 587" -S smtp=smtp://<YYYYMMDD-smtp-handson-serverのPrivateIPアドレス>:587 -r hogehoge@fugafuga.com <送信先メールアドレス>
```

#### メールログの確認

***YYYYMMDD-smtp-handson-server*** にSSH接続します。

以下コマンドでメールリレーが行われていることをログから確認してください。
```bash
$ sudo vi /var/log/maillog
```

リレーに成功すると以下のようなログが出るはずです。(Gmailの場合)

```bash
Oct 21 02:21:14 ip-192-168-2-44 postfix/smtpd[2996]: connect from ip-xxx-xxx-xxx-xxx.ap-northeast-1.compute.internal[xxx.xxx.xxx.xxx]
Oct 21 02:21:14 ip-192-168-2-44 postfix/smtpd[2996]: 66857C01110: client=ip-xxx-xxx-xxx-xxx.ap-northeast-1.compute.internal[xxx.xxx.xxx.xxx], sasl_method=PLAIN, sasl_username=<認証ユーザ名>
Oct 21 02:21:14 ip-192-168-2-44 postfix/cleanup[2999]: 66857C01110: message-id=<5f8f9b1a.JEdmKAU2e4kqPSBs%hogehoge@fugafuga.com>
Oct 21 02:21:14 ip-192-168-2-44 postfix/qmgr[2924]: 66857C01110: from=<hogehoge@fugafuga.com>, size=609, nrcpt=1 (queue active)
Oct 21 02:21:14 ip-192-168-2-44 postfix/smtpd[2996]: disconnect from ip-xxx-xxx-xxx-xxx.ap-northeast-1.compute.internal[xxx.xxx.xxx.xxx]
Oct 21 02:21:14 ip-192-168-2-44 postfix/smtp[3000]: connect to aspmx.l.google.com[2404:6800:4008:c07::1a]:25: Network is unreachable
Oct 21 02:21:15 ip-192-168-2-44 postfix/smtp[3000]: 66857C01110: to=<送信先メールアドレス>, relay=aspmx.l.google.com[108.177.97.26]:25, delay=1.2, delays=0.06/0.01/0.43/0.71, dsn=2.0.0, status=sent (250 2.0.0 OK  1603246875 x30si882009pge.334 - gsmtp)
Oct 21 02:21:15 ip-192-168-2-44 postfix/qmgr[2924]: 66857C01110: removed
```

## リソースの削除

必要なければ、今回作成したリソースを削除しましょう。

以下、CloudFormationスタックを全て削除することで完了します。

|削除されるリソース|スタック名|
|---|---|
|PrivateSubnet|smtp-handson-pri-sub-YYYYMMDD|
|EC2:"YYYYMMDD-smtp-handson-client"|smtp-handson-client-YYYYMMDD|

## まとめ

ということで、SMTP認証を利用したメールリレーをセットアップしてみました。  
これで、第三者による不正なメールリレーが行われる危険性はぐんと下がったと思います。

ご覧いただきありがとうございました。
