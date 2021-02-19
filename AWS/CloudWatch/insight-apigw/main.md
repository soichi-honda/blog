## はじめに
API GW から CloudWatch Logs に 出力した REST API アクセスログ情報を、   CloudWatch Watch Logs Insight で加工したいときに使えるサンプルクエリをまとめてみました。

複雑なクエリはないので、CloudWatch Watch Logs Insight 初心者の方も是非参考にしていただけると！

記事目安...10分

[:contents]

## REST API アクセスログのログ形式について

REST API アクセスログの形式は、  
AWS ドキュメントで紹介されている一般的なログ形式を前提とします。

今回は、その中でも JSON 形式のログ形式に注力して紹介します。

```json
{ 
  "requestId":"$context.requestId", \
  "ip": "$context.identity.sourceIp", \
  "caller":"$context.identity.caller", \
  "user":"$context.identity.user", \
  "requestTime":"$context.requestTime", \
  "httpMethod":"$context.httpMethod", \
  "resourcePath":"$context.resourcePath", \
  "status":"$context.status", \
  "protocol":"$context.protocol", \
  "responseLength":"$context.responseLength" \
}
```

参考: [API Gateway での CloudWatch によるログの形式
](https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/set-up-logging.html#apigateway-cloudwatch-log-formats)

*1. 各属性値は *parse* コマンドで加工する必要なく、指定することができます。

*2. それぞれのログ属性の詳細については、[API Gateway マッピングテンプレートとアクセスのログ記録の変数リファレンス](https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html#context-variable-reference) をご参考ください。

---

今回は、以下サンプルログが CloudWatch logs グループ に格納されている前提として、クエリを実行します。

* サンプルログ1
```json
{ 
  "requestId":"8d2f5138-019f-449c-bde7-432ff3cb49a1", 
  "ip": "103.4.xxx.xxx", 
  "caller":"-", 
  "user":"-",
  "requestTime":"13/Feb/2021:07:45:36 +0000", 
  "httpMethod":"GET",
  "resourcePath":"/hello", 
  "status":"200",
  "protocol":"HTTP/1.1", 
  "responseLength":"26" 
}
```
* サンプルログ2
```json
{
    "requestId": "f56dfc01-5f1b-4509-b2f6-124bb3fa0feb",
    "ip": "52.68.xxx.xxx",
    "caller": "-",
    "user": "-",
    "requestTime": "13/Feb/2021:07:54:52 +0000",
    "httpMethod": "GET",
    "resourcePath": "/hello",
    "status": "200",
    "protocol": "HTTP/1.1",
    "responseLength": "26"
}

```

余談ですが、  
上記サンプルログは [こちら](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html) の AWS ドキュメントに従って構築した HelloWorld API のアクセスログです。

## REST API アクセスログのサンプルクエリ集

役に立ちそうなクエリを場面を想像して、いくつかピックアップしてみました。


### "ステータスコード 2xx 系のメッセージログを抽出する" クエリ
〇クエリテンプレート
```sql
fields @message
| filter (status < 300)
| display @message
| limit 10
```

〇結果

|@message|
|---|
| { "requestId":"f56dfc01-5f1b-4509-b2f6-124bb3fa0feb", "ip": "52.68.xxx.xxx", "caller":"-", "user":"-","requestTime":"13/Feb/2021:07:54:52 +0000", "httpMethod":"GET","resourcePath":"/hello", "status":"200","protocol":"HTTP/1.1", "responseLength":"26" } |
|{ "requestId":"8d2f5138-019f-449c-bde7-432ff3cb49a1", "ip": "103.4.xxx.xxx", "caller":"-", "user":"-","requestTime":"13/Feb/2021:07:45:36 +0000", "httpMethod":"GET","resourcePath":"/hello", "status":"200","protocol":"HTTP/1.1", "responseLength":"26" }|

### "特定の送信元 IP アドレス以外の 送信元 IP アドレスごとのリクエスト数をカウントする" クエリ
〇クエリテンプレート
```sql
fields @message
| filter ip not in ["<除外したい IP アドレス1>", "<除外したい IP アドレス2>", ...]
| stats count(*) as count by ip
| sort count desc
| limit 10
```

〇凡例  
*103.4.xxx.xxx* の 送信元 IP アドレスのみ除外する
```sql
fields @message
| filter ip not in ["103.4.xxx.xxx"]
| stats count(*) as count by ip
| sort count desc
| limit 10
```

〇結果

|      ip      | count |
|--------------|-------|
| 52.68.xxx.xxx | 1     |

### "送信元 IP アドレス, リクエストメソッド, リクエストURI ごとのリクエスト数をカウントする" クエリ

〇クエリテンプレート
```sql
fields @message
| stats count(*) as count by ip, httpMethod, resourcePath, status
| sort count desc
| limit 10
```

〇結果

|      ip      | httpMethod | resourcePath | status | count |
|--------------|------------|--------------|--------|-------|
| 52.68.xxx.xxx | GET        | /hello       | 200    | 1     |
| 103.4.xxx.xxx | GET        | /hello       | 200    | 1     |

## まとめ

またよさげなクエリができたら追記します!