AmazonLinux2にServerless Frameworkの環境を構築して試してみます。

# 事前知識
Serverless Framework
サーバレスアプリケーションを構成管理+デプロイするためのツール。
様々なクラウドプロバイダーで上にデプロイができる。

# ゴール
- AmazonLinux2環境にServerlessFrameworkを構築する
- ServerlessFrameworkを構築して、Lambdaをデプロイする
[How_to_Serverless_Framework_1]

# 作業
## 環境構築

### IAM Roleの準備
Serverless Frameworkは他のAWSサービスを触れる必要があるので、
IAM Roleを用意します。
|Key|Value|
|---|---|
|RoleName|<本日の年月日>-serverless-handson-role|

IAM Role を作成ので、ポリシーをアタッチしましょう。
1. 対象のロールを選択。
1. *アクセス権限* タブ > *インラインポリシーの追加*
1. *JSON*　タブ を開く。
1. [こちら](https://github.com/serverless/serverless/issues/1439)のサイトにあるJSONを貼り付ける。
※一行目に *{* 抜けているので追記してください。
1. *ポリシーの確認* を押す。
1. 名前を *<本日の年月日>-serverless-handson-policy* にして *ポリシーの作成* を押す。

### EC2の構築
以下の条件でEC2とSGを準備してください
- EC2
|OS|Amazonlinux2|
|Instance Type|t3.micro|
|Tag|Name: <本日の年月日>-serverless-handson|

- SG
|Key|Value|
|---|---|
|SecurityGroupName|sg-<本日の年月日>-serverless-handson|

|Rule|Type|Protocol|port|Source/Destination|
|---|---|---|---|---|
|Inbound|SSH|TCP|22|<ローカルPCのIPアドレス>|
|Outbound|すべてのトラフィック|すべて|すべて|0.0.0.0/0|

EC2作成後は、IAMロールをアタッチします。
1. *アクション* > *IAMロールの割当/置換* を押す
1. ＩＡＭロ―ルの欄に先ほど作成したロールを選択して *適用* を押す

### ServerlessFrameworkのインストール
参考までに、今回使ったパッケージとバージョンです。
※Pythonはデフォルトでインストールされているものをそのまま使っています。
|Package|Version|
|---|---|
|node|14.4.0|
|Serverless Framework|1.73.1|
|python|2.7.16|

対象のEC2にSSHしてください。

最初に、nodejsを入れます。
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

## Lambdaのデプロイ
今回はテンプレートを用いて、Lambdaをデプロイします。
まずは、環境フォルダとテンプレートファイルを作成しましょう。
```bash
$ sls create -p serverless-handson -t aws-python
$ ls serverless-handson
handler.py  serverless.yml
```
各ファイル詳細は以下です。
|File|Detail|
|---|---|
|handler.py|Lambda上で実行されるコードを記述するファイル|
|serverless.yml|デプロイの設定を記述するファイル|

続いて、Lambdaにデプロイする前にコードが正しく動作するか確認しておきましょう。
*hello* とは、handler.py内の関数 *hello* を指します。
```bash
$ sls invoke local -f hello
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

EC2に入っている状態で、Lambdaを動かすことも可能です。
正しくデプロイできていれば、sls invoke localの返り値と一致します。
こちらでも確認してみましょう。
```bash
$ sls invoke -f hello
```

# リソースの削除
最後に今回使ったリソースを削除しましょう。

Serverless Frameworkで作成したリソースは、コマンド一つで消すことができます。
CloudFormationに感謝です
```
$ sls remove -r us-east-1
```

今回は手動で作ったリソースもあるので、こちらも忘れず消してください
|AWS Resource|Name|
|---|---|
|EC2|<本日の年月日>-serverless-handson|
|SG|sg-<本日の年月日>-serverless-handson|
|IAMRole|<本日の年月日>-serverless-handson-role|

# まとめ
今回はServerless Frameworkを使って、シンプルなLambdaを作成しました。

デプロイ~削除まで簡単にできて、ローカルでテストできるのは魅力的ですね。
Codeシリーズとうまく組み合わせられるとさらに便利なんじゃないかなーと思いました。

以上ありがとうございました。