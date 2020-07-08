AmazonLinux2にServerless Frameworkの環境を構築して試してみます。

記事目安 - 10分

# 事前知識
## Serverless Framework
サーバレスアプリケーションを構成管理+デプロイするためのツール。
様々なクラウドプロバイダーで上にデプロイができる。

# ゴール
構成図のイメージです。

[How_to_Serverless_Framework_1]

今回は大きく2つのことを行います。
- AmazonLinux2環境にServerlessFrameworkを構築する
- ServerlessFrameworkを構築して、Lambdaをデプロイする

# 作業
## Serverless Frameworkの準備

### NW環境の構築

最初にServerless Frameworkを環境を作りましょう。

まずは、以下URLのテンプレートをCloudFormationで流して、VPCとPublicSubnetを作成してください。
スタック名は 、serverless-handson-<YYYYMMDD>-vpc でお願いします。

[templates/cfn-template-vpc.yml]

CloudFormationへの流し方がわからない方は以下の記事を参考にしていただけると。
[]()

### IAM Roleの構築
先にも書きましたが、Serverless Frameworkはデプロイツールです。
ゆえに様々なリソースに対して権限が必要です。

ということでまずはIAMRoleを作成します。

本当はよくないのですが、すぐ消す環境なので *AdministratorAccess* で作成します。

以下URLのテンプレートをスタック名 serverless-handson-<YYYYMMDD>-iam-role　で流してください。

[templates/cfn-template-iam-role.yml]


### EC2の構築
Serverless FrameworkをインストールするEC2とアタッチするSGを構築します。

以下URLのテンプレートをスタック名 serverless-handson-<YYYYMMDD>-ec2 で流してください。
なお、先ほど作成したロールもアタッチされた状態で構築されます。

[templates/cfn-template-ec2.yml]


### Serverless Frameworkのインストール

環境をサクッと構築したところで本題のServerless Frameworkに触れていきます。


EC2の <YYYYMMDD>-serverless-framework-handson-ap にSSHしてください。

まずは、nodejsを入れます。

```bash
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
$ . ~/.nvm/nvm.sh
$ nvm install node
$ node -v //確認
```
参考: [チュートリアル: Amazon EC2 インスタンスでの Node.js のセットアップ](https://docs.aws.amazon.com/ja_jp/sdk-for-javascript/v2/developer-guide/setting-up-node-on-ec2-instance.html)

次に、Serverless Frameworkを入れます。こちらはnpmを使用します。
```bash
$ npm install -g serverless
$ serverless -v //確認
```

一応、pythonがインストールされているかも確認しておいてください。
```bash
$ python -V
```

※捕捉
1. パッケージについて
僕は以下のバージョンで必要なパッケージをインストールしました。  
Pythonはデフォルトでインストールされていたものをそのまま使っています。
|Package|Version|
|---|---|
|node|14.4.0|
|Serverless Framework|1.73.1|
|python|2.7.16|

2. Pythonについて
後半、ローカルでテストをする際に使用します。

## Lambdaのデプロイ

Serverless Frameworkでは、いくつかのテンプレートが用意されています。
今回はそれを用いて、Lambdaをデプロイします。

sls createコマンドを使用して、環境フォルダとテンプレートファイルを作成しましょう。
オプションは以下です。
|Option|Detail|
|---|---|
|p|作成されるフォルダの名前を指定|
|t|使用する言語を指定|

```bash
$ sls create -p <YYYYMMDD>-serverless-handson -t aws-python
$ ls <YYYYMMDD>-serverless-handson
handler.py  serverless.yml
```

※捕捉
1. 作成されたフォルダの詳細
|File|Detail|
|---|---|
|handler.py|Lambda上で実行されるコードを記述するファイル|
|serverless.yml|デプロイの設定を記述するファイル|

続いて、Lambdaにデプロイする前にコードが正しく動作するか確認しておきましょう。
-f で handler.py 内の関数helloを指定します。


```bash
$ sls invoke local -f hello
```

このような返り値が返ればOKです。
```bash
{
    "body": "{\"input\": {}, \"message\": \"Go Serverless v1.0! Your function executed successfully!\"}",
    "statusCode": 200
}
```

ローカルでコードが正しく動作することを確認できたので、Lambdaをデプロイをしましょう。
```bash
$ sls deploy
```

# 確認
実際にマネコンに入って、Lambdaができているか確認してみましょう!
リージョンは明記していないとus-east-1に作られるみたいです。

ちなみに、裏側はCloudFormationが動いてるので、CloudFormmationコンソールからもデプロイしていることがわかりますよ。

EC2から、Lambdaを動かすことも可能です。
正しくデプロイできていれば、sls invoke localの返り値と一致します。

```bash
$ sls invoke -f hello
```

# リソースの削除
最後に今回使ったリソースを削除しましょう。

Serverless Frameworkで作成したリソースは、コマンド一つで消すことができます。
CloudFormationに感謝です。
```
$ sls remove -r us-east-1
```

また、今回のために作った環境も忘れず消してください
|AWS Resource|Name|
|---|---|
|CloudFormation Stack|serverless-handson-<YYYYMMDD>-ec2|
|CloudFormation Stack|serverless-handson-<YYYYMMDD>-iam-role|
|CloudFormation Stack|serverless-handson-<YYYYMMDD>-vpc|

# まとめ
今回はServerless Frameworkを使って、シンプルなLambdaを作成しました。

デプロイ~削除まで簡単にできて、ローカルでテストできるのは魅力的ですね。

以上ありがとうございました。