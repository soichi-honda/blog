## はじめに
CloudWatch Logs に出力した Apache アクセスログ情報を、CloudWatch Logs Insight で解析する方法をまとめてみました。  
**parse** コマンドの使い方も簡単に解説しているのでご参照ください!

まだ、Apache アクセスログを CloudWatch Logs に出力していないという方は以下をご参照ください

[【AmazonLinux2】【amazon-cloudwatch-agent】最速で Apache のアクセスログを CloudWatch Logs にログ出力してみる](https://blog.serverworks.co.jp/cw-apache-access_log)

記事目安...10分

[:contents]

## Apache アクセスログのログ形式について

Apache アクセスログの形式は、 デフォルト設定の以下を前提とします。(*1)

```sh
%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"
```

*1. httpd バージョン *2.4.46-1* のデフォルト設定です。

---

今回は以下サンプルログが CloudWatch logs グループ に格納されている前提として、クエリを実行します。

* サンプルログ1
```sh
103.xxx.xxx.xxx - - [14/Feb/2021:10:40:57 +0000] "GET / HTTP/1.1" 200 16 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
```
* サンプルログ2
```sh
172.xxx.xxx.xxx - - [14/Feb/2021:14:01:30 +0000] "GET /fuga.html HTTP/1.1" 200 5 "-" "curl/7.61.1"
```

## parse コマンドによるログ加工について

CloudWatch Logs にインポートした Apache アクセスログは、各値が事前に項目分けされていないので、  
**parse** コマンドでエフェメラルフィールド(=一時的な項目) を作成してからクエリを投げることが望ましいです。

〇 Apache ログの parse 例
```sql
| parse @message '* * * [*] "* * *" * "*" "*"' as srcIpAddress, srcUser, remoteUser, timestamp, httpMethod, requestUri, protocol, statusCode, transferredData,referer, userAgent
```

参考: [CloudWatch Logs Insights クエリ構文 \- Amazon CloudWatch Logs](https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)

## クエリを投げてみた

アクセスログを parse した後、
*requestUri* が "/" かつ、statusCode が "2xx系" のアクセスを、送信元 IP ごとにカウントしてみます。

〇 サンプルクエリ
```sql
fields @message
| filter @logStream =~ /<ログストリーム名>/
| parse @message '* * * [*] "* * *" * "*" "*"' as srcIpAddress, srcUser, remoteUser, timestamp, httpMethod, requestUri, protocol, statusCode, transferredData, referer, userAgent
| filter requestUri = "/"
| filter statusCode =~ /2\d\d/
| stats count(*) as count by srcIpAddress
| sort count desc
| limit 10
```

〇 凡例    
"ログストリーム名: i-08c0f578afa9xxxxx" の場合

```sql
fields @message
| filter @logStream =~ /i-08c0f578afa9xxxxx/
| parse @message '* * * [*] "* * *" * "*" "*"' as srcIpAddress, srcUser, remoteUser, timestamp, httpMethod, requestUri, protocol, statusCode, transferredData, referer, userAgent
| filter requestUri = "/"
| filter statusCode =~ /2\d\d/
| stats count(*) as count by srcIpAddress
| sort count desc
| limit 10
```

〇 結果

|@message|count|
|---|---|
|103.xxx.xxx.xxx|1|

---

無事取得できましたね。

## まとめ

Apache アクセスログの解析クエリについて触れました。

今回使用した *parse* コマンドは Apache アクセスログ以外の解析でも使用できる便利なコマンドなのでぜひ使ってみてください!

またよさげなクエリができたら追記します!

## 参考
[CloudWatch Logs Insights クエリ構文 \- Amazon CloudWatch Logs](https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
