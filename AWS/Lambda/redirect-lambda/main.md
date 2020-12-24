## はじめに

CloudFront にきた特定ホスト向けのリクエストを、 Lambda@Edge(以後L@E) で URI を維持しながらリダイレクトするコードを Node.js で書いてみました。

記事目安...5分~10分

## コードについて

サンプルコードは [こちら](https://github.com/sugaya0204/blog/blob/Public/AWS/Lambda/redirect-lambda/src/redirect.js) をご覧ください。

---

サンプルでは、URI を維持したまま *hogehoge.com* → *www.hogehoge.com* にリダイレクトします。 

hogehoge.com 以外のホスト名指定でリクエストが来た場合は、オリジンにリクエストを通します。



## 使い方

**STEP1. コードを変更する**

* `redirectSrcHost` にリダイレクト元のホスト名を挿入します
```js
const redirectSrcHost = 'hogehoge.com';
```
* `redirectHost` にリダイレクト先のホスト名を挿入します
```js
const redirectHost = 'www.hogehoge.com';
```

---

**STEP2. L@E をデプロイする**

デプロイの詳細手順は省きますが、  
L@E の処理をキャッシュしたい場合は、 **オリジンリクエスト** にデプロイしてください。


## テスト用リクエストについて

Lambda でのテストで使用したリクエストの Json もおいておきます。

---

#### パターン1: hogehoge.com へリクエストを投げた場合
```json
{
  "Records": [
    {
      "cf": {
        "config": {
          "distributionDomainName": "d111111abcdef8.cloudfront.net",
          "distributionId": "EDFDVBD6EXAMPLE",
          "eventType": "origin-request",
          "requestId": "4TyzHTaYWb1GX1qTfsHhEqV6HUDd_BzoBZnwfnvQc_1oF26ClkoUSEQ=="
        },
        "request": {
          "clientIp": "203.0.113.178",
          "headers": {
            "x-forwarded-for": [
              {
                "key": "X-Forwarded-For",
                "value": "203.0.113.178"
              }
            ],
            "user-agent": [
              {
                "key": "User-Agent",
                "value": "Amazon CloudFront"
              }
            ],
            "via": [
              {
                "key": "Via",
                "value": "2.0 2afae0d44e2540f472c0635ab62c232b.cloudfront.net (CloudFront)"
              }
            ],
            "host": [
              {
                "key": "Host",
                "value": "hogehoge.com"
              }
            ],
            "cache-control": [
              {
                "key": "Cache-Control",
                "value": "no-cache, cf-no-cache"
              }
            ]
          },
          "method": "GET",
          "origin": {
            "custom": {
              "customHeaders": {},
              "domainName": "hogehoge.com",
              "keepaliveTimeout": 5,
              "path": "",
              "port": 443,
              "protocol": "https",
              "readTimeout": 30,
              "sslProtocols": [
                "TLSv1",
                "TLSv1.1",
                "TLSv1.2"
              ]
            }
          },
          "querystring": "",
          "uri": "/test"
        }
      }
    }
  ]
}
```

#### パターン2: fugafuga.hogehoge.com へリクエストを投げた場合
```json
{
  "Records": [
    {
      "cf": {
        "config": {
          "distributionDomainName": "d111111abcdef8.cloudfront.net",
          "distributionId": "EDFDVBD6EXAMPLE",
          "eventType": "origin-request",
          "requestId": "4TyzHTaYWb1GX1qTfsHhEqV6HUDd_BzoBZnwfnvQc_1oF26ClkoUSEQ=="
        },
        "request": {
          "clientIp": "203.0.113.178",
          "headers": {
            "x-forwarded-for": [
              {
                "key": "X-Forwarded-For",
                "value": "203.0.113.178"
              }
            ],
            "user-agent": [
              {
                "key": "User-Agent",
                "value": "Amazon CloudFront"
              }
            ],
            "via": [
              {
                "key": "Via",
                "value": "2.0 2afae0d44e2540f472c0635ab62c232b.cloudfront.net (CloudFront)"
              }
            ],
            "host": [
              {
                "key": "Host",
                "value": "fugafuga.hogehoge.com"
              }
            ],
            "cache-control": [
              {
                "key": "Cache-Control",
                "value": "no-cache, cf-no-cache"
              }
            ]
          },
          "method": "GET",
          "origin": {
            "custom": {
              "customHeaders": {},
              "domainName": "fugafuga.hogehoge.com",
              "keepaliveTimeout": 5,
              "path": "",
              "port": 443,
              "protocol": "https",
              "readTimeout": 30,
              "sslProtocols": [
                "TLSv1",
                "TLSv1.1",
                "TLSv1.2"
              ]
            }
          },
          "querystring": "",
          "uri": "/test"
        }
      }
    }
  ]
}
```

参考: [Lambda@Edge イベント構造 \- Amazon CloudFront \-オリジンリクエストの例](https://docs.aws.amazon.com/ja_jp/AmazonCloudFront/latest/DeveloperGuide/lambda-event-structure.html#example-origin-request)

## 参考
* [Lambda@Edge 関数の例 \- Amazon CloudFront](https://docs.aws.amazon.com/ja_jp/AmazonCloudFront/latest/DeveloperGuide/lambda-examples.html)