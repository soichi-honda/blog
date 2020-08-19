こんにちは、サーバーワークス菅谷です。

備忘録として、Amazon Linux 2にServerless Frameworkの環境を構築して、Lambdaを構築してみます。

使用する言語はPython2です。

記事目安 - 15分~20分

[:contents]

## 事前知識
#### Serverless Framework
オープンソースのサーバレスアプリケーション構成管理ツール。  
AWS, Azure, GCPなど、様々なパブリッククラウドプロバイダーにサーバレスアプリケーションをデプロイできます。

参考: [Serverless Framework](https://www.serverless.com/)

## ゴール
構成図のイメージです。

[f:id:swx-sugaya:20200821164637p:plain](assets/build-lambda-by-serverless-framework_1.PNG)

---

今回は大きく2つのことを行います。

- Amazon Linux 2環境にServerless Frameworkを構築する
- Serverless Frameworkを利用して、Lambdaをデプロイする

Serverless Frameworkではローカル環境でテストができるので、今回はそちらも試してみましょう。


## 作業
### Serverless Frameworkの準備

#### NW環境の構築

Serverless FrameworkのNW環境を作りましょう。

以下URLのテンプレートをCloudFormationで流して、VPCとPublicSubnetを作成してください。  
スタック名は ***serverless-handson-vpc-YYYYMMDD*** (*1)でお願いします。

[cfn-template-vpc.yml](https://github.com/sugaya0204/blog/blob/Public/AWS/build-lambda-by-serverless-framework/templates/cfn-template-vpc.yml)

*1) YYYYMMDDは本日の日付に置き換えてください。

---

CloudFormationへの流し方がわからない方は以下の記事を参考にしていただけると。

[【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 後編](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn-2)

#### IAM Roleの構築
Serverless Frameworkはリソースのデプロイを行います。  
ゆえに様々なリソースに対して権限が必要です。

ということで、IAM Roleを作成します。

本当はよくないのですが、すぐ消す環境なので ***AdministratorAccess*** で作成します。

以下URLのテンプレートをスタック名 ***serverless-handson-iam-role-YYYYMMDD*** で流してください。

[cfn-template-iam-role.yml](https://github.com/sugaya0204/blog/blob/Public/AWS/build-lambda-by-serverless-framework/templates/cfn-template-iam-role.yml)


#### EC2の構築
Serverless FrameworkをインストールするEC2とアタッチするSGを構築します。

以下URLのテンプレートをスタック名 ***serverless-handson-ec2-YYYYMMDD*** で流してください。
なお、先ほど作成したロールもアタッチされた状態で構築されます。

[cfn-template-ec2.yml](https://github.com/sugaya0204/blog/blob/Public/AWS/build-lambda-by-serverless-framework/templates/cfn-template-ec2.yml)


#### Serverless Frameworkのインストール

環境をサクッと構築したところで本題のServerless Frameworkに触れていきます。


構築したEC2 ***YYYYMMDD-serverless-framework-handson-ap*** にSSHしてください。

まずは、node.jsを入れます。

```bash
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
$ . ~/.nvm/nvm.sh
$ nvm install node
$ node -v //確認
```

参考: [チュートリアル: Amazon EC2 インスタンスでの Node.js のセットアップ](https://docs.aws.amazon.com/ja_jp/sdk-for-javascript/v2/developer-guide/setting-up-node-on-ec2-instance.html)

---

次に、Serverless Frameworkをインストールします。こちらはnpmを使用します。

```bash
$ npm install -g serverless
$ serverless -v //確認
```

一応、Python2がインストールされているかも確認しておいてください(*2)。
```bash
$ python -V
```

*2) Python2について  
後半、ローカルでテストをする際に使用します。

*3) パッケージについて  
僕は以下のバージョンで必要なパッケージをインストールしました。  
Python2はデフォルトでインストールされていたものをそのまま使っています。

|Package|Version|
|---|---|
|node|14.4.0|
|Serverless Framework|1.73.1|
|python|2.7.16|

### Lambdaのデプロイ

Serverless Frameworkでは、いくつかのテンプレートが用意されています。
今回はそれを用いて、Lambdaをデプロイします。

***sls create*** コマンドを使用して、環境フォルダとテンプレートファイルを作成しましょう。  
オプションの詳細は以下です。

|Option|Detail|
|---|---|
|p|作成されるフォルダの名前を指定|
|t|使用する言語を指定|

```bash
$ sls create -p YYYYMMDD-serverless-handson -t aws-python
$ cd YYYYMMDD-serverless-handson
$ ls
handler.py  serverless.yml
```

*4) 作成されたフォルダの詳細

|File|Detail|
|---|---|
|handler.py|Lambda上で実行されるコードを記述するファイル|
|serverless.yml|デプロイの設定を記述するファイル|

---

Lambdaにデプロイする前にコードが正しく動作するか確認しておきましょう。  
"-f" で handler.py 内の関数helloを指定します。

```bash
$ sls invoke local -f hello
```

以下のような返り値が返ればOKです。

```bash
{
    "body": "{\"input\": {}, \"message\": \"Go Serverless v1.0! Your function executed successfully!\"}",
    "statusCode": 200
}
```

---

ローカルでコードが正しく動作することを確認できたので、Lambdaをデプロイをしましょう。

```bash
$ sls deploy
```

## 確認
実際にマネコンに入って、Lambdaができているか確認してみましょう!  
リージョンは明記していないと"us-east-1"に作られるみたいです。

ちなみに、裏側はCloudFormationが動いてるので、CloudFormationコンソールからもデプロイしていることがわかりますよ。

---

EC2から、Lambdaを動かすことも可能です。  

```bash
$ sls invoke -f hello
```

正しくデプロイできていれば、sls invoke local時の返り値と一致するはずです。

## リソースの削除
最後に、使ったリソースを削除しましょう。

Serverless Frameworkで作成したリソースは、コマンド一つで消すことができます。  
CloudFormationに感謝です。

```
$ sls remove -r us-east-1
```

---

また、今回のために作った環境も忘れず消してください!

|AWS Resource|Name|
|---|---|
|CloudFormation Stack|serverless-handson-ec2-YYYYMMDD|
|CloudFormation Stack|serverless-handson-iam-role-YYYYMMDD|
|CloudFormation Stack|serverless-handson-vpc-YYYYMMDD|

## まとめ
今回はServerless Frameworkを使って、シンプルなLambdaを作成しました。

デプロイ~削除まで簡単にできて、ローカルでテストできるのは魅力的ですね。

以上ありがとうございました。
