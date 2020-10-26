
記事が進むにつれ削除対象リソースが増えるため、注意して下さい

スタック削除の仕方がわからない方は、以下の記事を参考にしてください。

[【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 後編-環境の削除](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn-2#%E7%92%B0%E5%A2%83%E3%81%AE%E5%89%8A%E9%99%A4)

## [【第1回】【EC2】PostfixでシンプルなSMTPサーバを構築してみる](https://blog.serverworks.co.jp/build-smtp-server)
- 今回作成したリソース
    - スタックの削除
        |削除されるリソース|スタック名|
        |---|---|
        |SSMパラメータ|smtp-handson-common-YYYYMMDD|
        |VPC, PublicSubnet|smtp-handson-vpc-YYYYMMDD|
        |EC2:"YYYYMMDD-smtp-handson-server"|smtp-handson-server-YYYYMMDD|

- ホストゾーンの削除
    1. コンソールにアクセスして、今回作成したRoute53のホストゾーンを削除しましょう。
    2. 取得したドメインが必要なければ、Freenom側でもドメインを削除してください。

## [【第2回】【EC2】Dovecotを使って、POP3サーバを構築してみる](https://blog.serverworks.co.jp/build-pop3-server)
- 前回までに作成したリソース  
ほかの記事に進まない場合は [【第1回】【EC2】PostfixでシンプルなSMTPサーバを構築してみる](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/cfn-delete.md#%E7%AC%AC1%E5%9B%9Eec2postfix%E3%81%A7%E3%82%B7%E3%83%B3%E3%83%97%E3%83%AB%E3%81%AAsmtp%E3%82%B5%E3%83%BC%E3%83%90%E3%82%92%E6%A7%8B%E7%AF%89%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B) を参考にしてください　

## [【第3回】Postfixでメールリレーを試してみる](https://blog.serverworks.co.jp/mail-relay)
- 前回までに作成したリソース
[【第1回】【EC2】PostfixでシンプルなSMTPサーバを構築してみる](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/cfn-delete.md#%E7%AC%AC1%E5%9B%9Eec2postfix%E3%81%A7%E3%82%B7%E3%83%B3%E3%83%97%E3%83%AB%E3%81%AAsmtp%E3%82%B5%E3%83%BC%E3%83%90%E3%82%92%E6%A7%8B%E7%AF%89%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B) を参考にしてください

- 今回作成したリソース
    |削除されるリソース|スタック名|
    |---|---|
    |PrivateSubnet|smtp-handson-pri-sub-YYYYMMDD|
    |EC2:"YYYYMMDD-smtp-handson-client"|smtp-handson-client-YYYYMMDD|

## [【第4回】SMTP認証を実装して、メールリレーをセキュアにする](https://blog.serverworks.co.jp/set-smtp-auth)
- 前回までに作成したリソース  
以下を参考にしてください
    - [【第1回】【EC2】PostfixでシンプルなSMTPサーバを構築してみる](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/cfn-delete.md#%E7%AC%AC1%E5%9B%9Eec2postfix%E3%81%A7%E3%82%B7%E3%83%B3%E3%83%97%E3%83%AB%E3%81%AAsmtp%E3%82%B5%E3%83%BC%E3%83%90%E3%82%92%E6%A7%8B%E7%AF%89%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B)
    - [【第3回】Postfixでメールリレーを試してみる](https://github.com/sugaya0204/blog/blob/Public/Tips/mail-server/cfn-delete.md#%E7%AC%AC3%E5%9B%9Epostfix%E3%81%A7%E3%83%A1%E3%83%BC%E3%83%AB%E3%83%AA%E3%83%AC%E3%83%BC%E3%82%92%E8%A9%A6%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B)