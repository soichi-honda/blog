## はじめに
SaaSサービスなどがある今、メールサーバを1から構築する人なんてどれだけいるかわかりませんが、せっかくやったので備忘録。

メールサーバはとにかくやることが色々あって混乱するので、本記事では最低限smtpサーバとして機能することをゴールとします。

記事目安...15分

[:contents]

## ゴール
今回は、以下構成でEC2上にsmtpサーバを構築します。

[f:id:swx-sugaya:20200912151915p:plain]

## 用語
#### メールアドレス
メールを送受信する際に使用します。    
形式は "ローカル部"@"ドメイン部" 。デフォルトではローカル部はUNIXユーザとなります。

ex) aaa@example.com  
ローカル部..."aaa", ドメイン部..."example.com"

#### Postfix
メールを送信するためのアプリケーション。  
たぶん最もよく使われている気がします。

#### smtp
メール送信時に用いられるプロトコル。  
25番ポートを使用します。

## 事前作業
### 環境の準備
まずはCloudFormationテンプレートを用いて、下記の環境を作成しましょう。

[f:id:swx-sugaya:20200912151923p:plain]

---

以下のテンプレートを上から流してください。(*1)

|作成リソース|スタック名|テンプレートURL|
|---|---|---|
|SSMパラメータ|smtp-handson-common-YYYYMMDD|[cfn-template-common.yml](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/build-smtp-server/templates/cfn-template-common.yml)|
|VPC, PublicSubnet×2|smtp-handson-vpc-YYYYMMDD|[cfn-template-vpc.yml](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/build-smtp-server/templates/cfn-template-vpc.yml)|
|EC2:"YYYYMMDD-smtp-handson-server"|smtp-handson-server-YYYYMMDD|[cfn-template-server.yml](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/build-smtp-server/templates/cfn-template-server.yml)|

*1. CloudFormationテンプレートの流し方は、以下を参考ください。

参考:[【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 後編](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn-2)

*2. 今回立てるEC2の詳細は以下です。

- YYYYMMDD-smtp-handson-server

  |Key|Value|
  |---|---|
  |OS|AmazonLinux2|
  |Inbound|SSH:0.0.0.0/0, SMTP:0.0.0.0/0|
  |Role|Mail Server|

### メール用ドメインの用意
#### メール用ドメインの取得とRoute53への委任
メールを行う上で、ドメインが必須となります。

メールで使うドメインを取得し、DNSに登録しましょう。

---

今回はFreenomで取得したドメインを、Route53に委任します。  
やりかたがわからない方は、以下ページをご参考ください。

参考: [freenomで取得したドメインをRoute53に委任する。](https://blog.serverworks.co.jp/delegate-route53)

ここからは取得したドメインを "example.com"と仮定したうえで進めていきます。

#### DNSレコード登録

続いて、メールを行うために必須なDNSレコードを登録します。

先ほど作成したホストゾーンに2つのレコードを作成してください。

- Aレコード

  |Key|Value|
  |---|---|
  |ルーティングポリシー|シンプルルーティング|
  |レコード名|任意のサブドメイン名 ex) mail.example.com|
  |値/トラフィックのルーティング先|"YYYYMMDD-smtp-server"のPublicIPアドレス|
  |レコードタイプ|A|
- MXレコード

  |Key|Value|
  |---|---|
  |ルーティングポリシー|シンプルルーティング|
  |レコード名|ドメイン名 ex) example.com|
  |値/トラフィックのルーティング先|10 "Aレコードに登録したサブドメイン"　ex) 10 mail.example.com (*3)|
  |レコードタイプ|MX|

*3. 値に入れた数字はメールを振り分ける際の比重を表します。

## smtpサーバーの構築

ここから、smtpサーバの構築に移ります。

"YYYYMMDD-smtp-handson-server" にSSHしてください。

### Postfixの導入
まず、"YYYYMMDD-smtp-handson-server" にPostfixをインストールします。

が、AmazonLinux2だと、デフォルトでPostfixはインストールされています。

```bash
$ yum list installed |grep postfix
postfix.x86_64                        2:2.10.1-6.amzn2.0.3           installed
$ sudo yum install -y postfix //なければ実行してください。
```

---

続いて、基本的な設定ファイルの "main.cf" を編集します。(*4)

```bash
$ sudo cp -a /etc/postfix/main.cf /etc/postfix/main.cf.`date +"%Y%m%d"` //日付でバックアップを取得
$ ls /etc/postfix/main.cf.`date +"%Y%m%d"`　//取得したバックアップを確認
$ sudo vi /etc/postfix/main.cf
---
#myhostname = host.domain.tld
→myhostname = <サブドメイン名> 

#mydomain = domain.tld
→mydomain = <ドメイン名>

#inet_interfaces = all
inet_interfaces = localhost
→inet_interfaces = all
#inet_interfaces = localhost

mydestination = $myhostname, localhost.$mydomain, localhost
#mydestination = $myhostname, localhost.$mydomain, localhost, $mydomainmynetworks_style = host
→#mydestination = $myhostname, localhost.$mydomain, localhost
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain

#home_mailbox = Maildir/
→home_mailbox = Maildir/
---
```

設定例
```
myhostname = mail.example.com
mydomain = example.com
inet_interfaces = all
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
home_mailbox = Maildir/ 
```

*4. Postfixの設定パラメータについて

|パラメータ|詳細|
|---|---|
|myhostname|サーバのホスト名を定義する。この値はほかのパラメータで頻繁に使用される。|
|mydomain|メールドメイン名を定義する。この値はほかのパラメータで頻繁に使用される。|
|inet_interfaces|メールを受信するIPアドレスを定義にする。"all"の場合、全てのIPアドレスからメールを受信する。|
|mydestination|メールの終着点を定義する。宛名がこの値のどれかと一致すると、そのメールは該当するローカルフォルダに格納する。|
|home_mailbox|メールの格納先を定義する。自動的に送り先UNIXユーザのホームディレクトリパスが付け足される。|

参考: [Postfix設定パラメータ](http://www.postfix-jp.info/trans-2.2/jhtml/postconf.5.html)

---

設定の編集が完了したら、以下コマンドで設定ファイルに誤りがないか確認しましょう。

```bash
$ sudo diff /etc/postfix/main.cf /etc/postfix/main.cf.`date +"%Y%m%d"` //差分を確認するコマンド
$ postconf -n
```

---

"postconf"コマンドの出力で、error, warningがなければ、Postfixを起動します。

```bash
$ sudo systemctl restart postfix
$ systemctl status postfix
```

### メールユーザを作成
メールを受信するメールユーザを作成します。

今回、メールユーザはUNIXユーザと1:1の関係です。

```
$ sudo useradd muser 
$ less /etc/passwd //確認用
$ exit
```

## 動作確認
### メールの送信
お好きなメーラーソフトで、"muser@example.com" 宛にメールを送ってみてください。

今回はGmailから送信します。

[f:id:swx-sugaya:20200912151908p:plain]

### 受信確認

再度、"YYYYMMDD-smtp-handson-server" サーバにSSHしてください。

---

受信したメールを確認します。  
"/home/muser/Maildir/new/" に新しいメールが届いているので、
開いてください

```bash
$ sudo less /home/muser/Maildir/new/"該当のメールファイル名"
```

---

以下で受信したメールログも確認いただけます。

```bash
$ sudo less /var/log/maillog
```

成功していると以下のようなログが出るはずです。

```text
Sep 12 04:46:57 ip-192-168-2-74 postfix/smtpd[3164]: warning: hostname ec2-54-249-33-61.ap-northeast-1.compute.amazonaws.com does not resolve to address 54.249.33.61
Sep 12 04:46:57 ip-192-168-2-74 postfix/smtpd[3164]: connect from unknown[54.249.33.61]
Sep 12 04:46:57 ip-192-168-2-74 postfix/smtpd[3164]: 8A129CA445F: client=unknown[54.249.33.61]
Sep 12 04:46:57 ip-192-168-2-74 postfix/cleanup[3168]: 8A129CA445F: message-id=<5f5c52c1.maVN9DqAvW1S9kc0%hogehoge@fugafuga.com>
Sep 12 04:46:57 ip-192-168-2-74 postfix/qmgr[3127]: 8A129CA445F: from=<hogehoge@fugafuga.com>, size=564, nrcpt=1 (queue active)
Sep 12 04:46:57 ip-192-168-2-74 postfix/smtpd[3164]: disconnect from unknown[54.249.33.61]
Sep 12 04:46:57 ip-192-168-2-74 postfix/local[3169]: 8A129CA445F: to=<muser@example.com>, relay=local, delay=0.05, delays=0.04/0/0/0, dsn=2.0.0, status=sent (delivered to maildir)
Sep 12 04:46:57 ip-192-168-2-74 postfix/qmgr[3127]: 8A129CA445F: removed
Sep 12 04:50:17 ip-192-168-2-74 postfix/anvil[3166]: statistics: max connection rate 2/60s for (smtp:54.249.33.61) at Sep 12 04:46:57
Sep 12 04:50:17 ip-192-168-2-74 postfix/anvil[3166]: statistics: max connection count 1 for (smtp:54.249.33.61) at Sep 12 04:46:34
Sep 12 04:50:17 ip-192-168-2-74 postfix/anvil[3166]: statistics: max cache size 1 at Sep 12 04:46:34
```


## リソースの削除

今回作成したリソースを削除しましょう。

以下、テンプレートファイルを全て削除することで完了します。

|削除されるリソース|スタック名|
|---|---|
|SSMパラメータ|smtp-handson-common-YYYYMMDD|
|VPC, PublicSubnet×2|smtp-handson-vpc-YYYYMMDD|
|EC2:"YYYYMMDD-smtp-handson-server"|smtp-handson-server-YYYYMMDD|

## まとめ
長くなりましたが、smtpサーバの構築が完了しました。

本記事ではほんとに最低限のsmtpサーバ構築しかおこなっていないので、気になる人はほかの記事も読んでいただけると幸いです。

ご覧いただきありがとうございました。
