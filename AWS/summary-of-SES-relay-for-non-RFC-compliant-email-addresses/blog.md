
案件で、SESが"RFC非準拠メールアドレス"をどこまでリレーしてくれるのか調べる機会がありました。

ドキュメント上にそれらしき記載がなかったので、誰かの役に立つのではないかと思い、調査結果をまとめてみます。

[:contents]

## 調査方針

### 調査環境
[f:id:swx-sugaya:20200818145127p:plain](summary-of-SES-relay-for-non-RFC-compliant-email-addresses_1.PNG)

上記環境にて、"RFC非準拠メールアドレス"宛にメールを送信した場合、どこまでSESがリレーするのか調査します。

本調査は"RFC非準拠メールアドレス"を実際に用意して行うわけではない点だけご留意ください(*1)。

ドメインがわかりづらいですが、ご愛嬌ということで...

*1)受信サーバ(sugasugasugaya.mlサーバ)にメールが正常受信されたことは保証できません。

### "RFC非準拠メールアドレス"の条件
本調査では、以下の条件を"RFC非準拠のメールアドレス"と定義します。

- 「() [] <> : ; , @ \ "」のいずれかがローカル部に含まれる
- スペースがローカル部に含まれる
- "."が2個以上連続する場合がローカル部に含まれる 
- ローカル部の先頭が"."で始まる
- "@"直前に"."が入る

参考:

-  [\[wikipedia\]メールアドレス](https://ja.wikipedia.org/wiki/%E3%83%A1%E3%83%BC%E3%83%AB%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9)
- [RFC 5322](http://srgia.com/docs/rfc5322j.html)
    - [3.2.3. アトム](http://srgia.com/docs/rfc5322j.html#p3.2.3)
    - [4.4. 廃止されたアドレス指定](http://srgia.com/docs/rfc5322j.html#p4.4)

---
本調査で使う、送信先"RFC非準拠メールアドレス"です。

|「() [] <> : ; , @ \ "」のいずれかがローカル部に含まれる|
|---|
|re(ceiver@sugasugasugaya.ml|
|re)ceiver@sugasugasugaya.ml|
|re[ceiver@sugasugasugaya.ml|
|re]ceiver@sugasugasugaya.ml|
|re<ceiver@sugasugasugaya.ml|
|re>ceiver@sugasugasugaya.ml|
|re\\>ceiver@sugasugasugaya.ml|
|re:ceiver@sugasugasugaya.ml|
|re;ceiver@sugasugasugaya.ml|
|re,ceiver@sugasugasugaya.ml|
|re@ceiver@sugasugasugaya.ml|
|re\\ceiver@sugasugasugaya.ml|
|re\\\ceiver@sugasugasugaya.ml|
|re\"ceiver@sugasugasugaya.ml|

|スペースがローカル部に含まれる|
|---|
|re ceiver@sugasugasugaya.ml|

|"."が2個以上連続する場合がローカル部に含まれる|
|---|
|re..ceiver@sugasugasugaya.ml|

|ローカル部の先頭が"."で始まる|
|---|
|.receiver@sugasugasugaya.ml|

|"@"直前に"."が入る|
|---|
|receiver.@sugasugasugaya.ml|

### 調査コマンド

以下のコマンドを実行します。

1.まずは以下コマンドでメールを送信します
```bash
$ telnet localhost 25
mail from: sender@postfix-test.ml
rcpt to: "re(ceiver"@sugasugasugaya.ml
data
From: sender@postfix-test.ml
To: "re(ceiver"@sugasugasugaya.ml
Subject: Not RFC test
hogehoge
.
quit
$
```

\* re(ceiver@sugasugasugaya.mlの場合

\* RFC非準拠メールアドレスを送信する場合は全て、ダブルクォートでローカル部を囲う必要があります。

2.次に tail コマンド等で当該配送ログを確認します。
```bash
$ sudo tail /var/log/maillog
```


## 調査結果
|RFC非準拠メールアドレス|Status|StatusCode|捕捉|
|---|---|---|---|
|re(ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re)ceiver@sugasugasugaya.ml|sent|250 Ok|-|	
|re[ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re]ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re<ceiver@sugasugasugaya.ml|sent|250 Ok|-|	
|re;ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re,ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re\ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re\\ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|.receiver@sugasugasugaya.ml|sent|250 Ok|-|
|receiver.@sugasugasugaya.ml|sent|250 Ok|-|
|re..ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re'ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re\"ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re ceiver@sugasugasugaya.ml|sent|250 Ok|-|
|re>ceiver@sugasugasugaya.ml|bounced|501 Invalid RCPT TO address provided|RCPT TO が"to=<re\>ceiver@sugasugasugaya.ml>" となるため
|re\\>ceiver@sugasugasugaya.ml|bounced|501 Invalid RCPT TO address provided|RCPT TO が "to=<re\>ceiver@sugasugasugaya.ml>" となるため
|re:ceiver@sugasugasugaya.ml|bounced|554 Transaction failed: Address contains illegal characters in user name: '<"re:ceiver"@sugasugasugaya.ml>'.|RFC非準拠によるエラー|
|re@ceiver@sugasugasugaya.ml|bounced|554 Transaction failed: Address contains illegal characters in user name: '<"re@ceiver"@sugasugasugaya.ml>'.|RFC非準拠によるエラー|

## 調査ログ

送信サーバ(postfix-testサーバ)のメールログ: "/var/log/maillog" の中身を以下URL にまとめました。  
証跡として、ご確認ください。

[Response-log.md](https://github.com/sugaya0204/blog/blob/Public/AWS/summary-of-SES-relay-for-non-RFC-compliant-email-addresses/assets/Response-log.md)

## まとめ

それぞれの合計値は以下でした。

|Response|StatusCode|Number|
|---|---|
|Success||15|
||250|15|
|Error||4|
||501|2|
||554|2|
|ALL ||19|

個人的な感想としては、予想よりもSESはリレー送信をしてくれるなという感じでした。

"RFC非準拠メールアドレス"は今後減っていく傾向にあるので、キャリアメールなどのリレー送信にSESを使うのも現実的になってきたのではないでしょうか!

以上ご覧いただきありがとうございました。
