こんにちは。

Develop Associateの勉強をして、STSを使った一時的なセキュリティ認証情報取得のAPIコールがよくわからんってなったのでまとめてみました。

なるべく図を多めに解説していくので、技術職でない方もぜひ読んでみてください！

記事目安 -15分

[:contents]

## 事前知識
本題に入る前に必要な知識を説明します。

#### 一時的なセキュリティ認証情報セット

AWSリソースへのアクセスに必要な情報のセット。STSがユーザからのリクエストに対して発行します。  
実態は以下。

- アクセスキー(アクセスキーID, シークレットアクセスキー)(*1)
- セキュリティトークン
- 有効期限

参考: [一時的セキュリティ認証情報](https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/id_credentials_temp.html)

ちなみになぜ "一時的" と付くかというと、IAMユーザ固有の認証情報を ***長期的なセキュリティ認証情報セット***(*2)と呼ぶため。

*1) ***一時的*** に発行されるアクセスキー

*2) IAM Userに紐づく以下の情報のセット。

1. サインイン認証情報
ユーザ名/パスワード, 多要素認証
1. アクセス認証情報
アクセスキー(アクセスキーIDとシークレットキー), API呼び出しに対するMFA

参考: [AWS 認証情報の管理](https://d1.awsstatic.com/whitepapers/ja_JP/Security/AWS_Security_Best_Practices.pdf#page=32)


#### 信頼関係
IAM Roleを引き受けられるリソース/IAM User/Federated User(\*3)を指す。  
IAM Roleの信頼関係タブにて、 ***信頼ポリシー*** により定義します。

*3) Federated User は、フェデレーションにより認証されたユーザを指します。

## 一時的なセキュリティ認証情報セットを取得するAPIコール

STSで一時的なセキュリティ認証情報セットを取得する場合、APIコールは2種類に大別されます。

1. GetxxxToken系
1. AssumeRole系

両者の大きな違いは以下です。

|-|GetxxxToken系|AssumeRole系|
|---|---|---|
|発行される一時的なセキュリティ認証情報がxxxのもの|IAMUser|IAMRole|
|有効期限がxxx|36h(※デフォルト12h)|1h|

---

さらに細かく見ると、一時的なセキュリティ認証情報セットを取得するAPIコールは5つに分別されます。

1. GetSessionToken
1. GetFederationToken
1. AssumeRole
1. AssumeRoleWithWebIdentity
1. AssumeRoleWithSAML

以下の図のような関係性です。

[f:id:swx-sugaya:20200818114336p:plain](001.PNG)

参考: [一時的なセキュリティ認証情報のリクエスト](https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/id_credentials_temp_request.html)

---

それではそれぞれのAPIコールついて見ていきます。

フェデレーションについては、Idp-initiated方式で説明します。

### 背景
アカウント内に以下リソースがあることを前提に解説します。

[f:id:swx-sugaya:20200818114307p:plain](002.PNG)

### GetSessionToken
〇概要

IAM Userの長期的なセキュリティ認証情報から、IAM Userの一時的なセキュリティ認証情報を発行するAPIリクエストです。

[f:id:swx-sugaya:20200818114315p:plain](003.PNG)

〇流れ

1. GetSessionTokenリクエストを行います。この時、以下の情報がSTSに送信されます
    - IAM User Aのアクセスキー
1. 送られてきた認証情報とIAM User Aの認証情報を検証します
1. 問題なければ、IAM User Aの一時的なセキュリティ認証情報を発行します
1. 一時的なセキュリティ認証情報を使用して、ReadOnlyAccess権限でAWSリソースにアクセスします

〇ユースケース

- 信頼されていない環境からIAM Userでアクセスする時

### AssumeRole
〇概要

IAM Userの長期的なセキュリティ認証情報から、IAM Roleの一時的なセキュリティ認証情報を発行するAPIリクエストです。

[f:id:swx-sugaya:20200818114319p:plain](004.PNG)

〇流れ

1. AssumeRoleリクエストを行います。この時、以下の情報がSTSに送信されます。
    - IAM User Aのアクセスキー
    - Role A or Role B のARN
1. 送られてきた認証情報とIAM User Aの認証情報を検証します。
1. Role A or Role B の信頼ポリシーを確認して、IAM User Aに信頼関係があるか確認します。
1. 問題なければ、Role A or Role Bの一時的なセキュリティ認証情報を発行します
1. 一時的なセキュリティ認証情報を使用して、ReadOnlyAccess or PowerUserAccess 権限でAWSリソースにアクセスします

〇ユースケース

- IAM Userに付与されていないポリシー権限でAWSリソースにアクセスさせたいとき
- SwitchRoleのとき

### GetFederationToken
〇概要

カスタムIDプロバイダーFederated Userの認証情報から、IAM Userの一時的なセキュリティ認証情報を発行するAPIリクエストです。

[f:id:swx-sugaya:20200818114322p:plain](005.PNG)

〇流れ

1. Idp A or Amazon Cognito に認証トークンをリクエストします。
1. Idp A or Amazon Cognito から認証トークンがレスポンスされます。
1. GetFederationTokenリクエストを行います。この時、以下の情報がSTSに送信されます。
    - IAM User Bのアクセスキー
    - Idp A or Amazon Congito から取得した認証トークン
1. 送られてきた認証情報とIAM User Bの認証情報を検証します。
1. 問題なければ、IAM User Bの一時的なセキュリティ認証情報を発行します。
1. 一時的なセキュリティ認証情報を使用して、ReadOnlyAccess権限でAWSリソースにアクセスします。

〇ユースケース

- 別のIdpにプールされたユーザを利用したいとき

---

ちなみにこのケースで、Web Idpを使用する場合、Amazon Cognitoや AssumeRoleWithWebIdentity を使用することが推奨されるそうです。

>You can create a mobile-based or browser-based app that can authenticate users using a web identity provider like Login with Amazon, Facebook, Google, or an OpenID Connect-compatible identity provider. In this case, we recommend that you use Amazon Cognito or AssumeRoleWithWebIdentity. For more information, see Federation Through a Web-based Identity Provider in the IAM User Guide.

参考: [GetFederationToken](https://docs.aws.amazon.com/ja_jp/STS/latest/APIReference/API_GetFederationToken.html) 


### AssumeRoleWithWebIdentity
〇概要

パブリックWebベースのIDプロバイダー(*4)を経由したFederated Userの認証情報から、IAM Userの一時的なセキュリティ認証情報を発行するAPIリクエストです。

Amazon Cognito をIdpに使う場合もこのAPIの利用が推奨されます。

*4) Facebook、Google,など。

[f:id:swx-sugaya:20200818114322p:plain](006.PNG)

〇流れ

1. Idp A or Amazon Cognito に認証トークンをリクエストします。
1. Idp A or Amazon Cognito から認証トークンがレスポンスされます。
1. AssumeRoleWithWebIdentityリクエストを行います。この時、以下の情報がSTSに送信されます。
    - Idp A or Amazon Cognito から取得した認証トークン
    - Role A or B のARN
1. Role A or Role B の信頼ポリシーを確認して、Federated User Bに信頼関係があるか確認します。
1. 問題なければ、Role A or Role Bの一時的なセキュリティ認証情報を発行します。
1. 一時的なセキュリティ認証情報を使用して、ReadOnlyAccess or PowerUserAccess 権限でAWSリソースにアクセスします。

〇ユースケース

- Web Idp にプールされたユーザを利用したいとき
- Amazon Cognitoにプールされたユーザを利用したいとき

### AssumeRoleWithSAML
〇概要

SAML2.0ベースのIDプロバイダーを経由したFederated Userの認証情報から、IAM Userの一時的なセキュリティ認証情報を発行するAPIリクエストです。

[f:id:swx-sugaya:20200818114331p:plain](007.PNG)

〇流れ

1. Idp BにAssertionをリクエストします。
1. Idp BからAssertionがレスポンスされます。
1. AssumeRoleWithWebIdentityリクエストを行います。この時、以下の情報がSTSに送信されます。
    - Idp B から取得したAssertion
    - Role A or B のARN
1. Role A or Role B の信頼ポリシーを確認して、Federated User Cに信頼関係があるか確認する。
1. 問題なければ、Role A or Role Bの一時的なセキュリティ認証情報を発行する
1. 一時的なセキュリティ認証情報を使用して、ReadOnlyAccess or PowerUserAccess 権限でAWSリソースにアクセスする

〇ユースケース

- SSOサービスによりプールされたユーザを利用したいとき


## 確認
最後に確認問題を作ってみました。解答は最後に書いておきます。

---
あなたはパブリッククラウドにAWSを採用している会社に勤めています。社内の開発担当者から本番用AWSアカウントでEC2をローンチできる権限を付けてほしいとの要望がありました。
なお、社内の全開発担当者には事前に本番用AWSアカウントで使えるReadOnlyAccessポリシーがアタッチされたIAM Userが存在します。

次の選択肢の中から最もセキュアに開発担当者に上記権限を付与する方法を選んでください。

1. AmazonEC2FullAccess ポリシーが付いたIAM Roleを作成する。開発担当者がこの権限を使う際は、GetSessionToken リクエストをSTSに送り、一時認証情報を取得する。
1. AmazonEC2FullAccess ポリシーを既存IAM Userにアタッチする。開発担当者がこの権限を使う際は、GetSessionToken リクエストをSTSに送り、一時認証情報を取得する。
1. AmazonEC2FullAccess ポリシーが付いたIAM Roleを作成する。開発担当者がこの権限を使う際は、AssumeRole リクエストをSTSに送り、一時認証情報を取得する。
1. AmazonEC2FullAccess ポリシーを既存IAM Userにアタッチする。開発担当者は既存IAM Userの長期認証情報を使用して、この権限を使うことができる

## まとめ

ということで、STSの5つの一時的なセキュリティ認証情報取得APIコールについて説明しました。

似たような概念があるので非常に混乱しますが、ここまで押さえておけば認証系の話はかなり理解できるようになるのではないでしょうか?

以上ご覧いただきありがとうございました。

---

解答

"A. 3"