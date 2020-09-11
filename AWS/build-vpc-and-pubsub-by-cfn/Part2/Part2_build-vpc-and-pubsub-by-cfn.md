前回、CloudFormationテンプレートの書き方について触れました。  
今回はその続きとして、作ったテンプレートファイルを実際にCloudFormationに流してみます。

前回記事: [【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 前編](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn)

記事目安...10分

[:contents]

## 今回のゴール
最終的に出来上がる構成図は以下です。前回と同じですね。
[f:id:swx-sugaya:20200813132940p:plain](assets/Part_1.PNG)

## 作業
### CloudFormationテンプレートの準備
今回使うテンプレートファイルは前編で作ったものを利用します。  
ローカルに保存していない人は下記をYml形式で保存しておいてください。

[templates/cfn-template.yml](https://github.com/sugaya0204/blog/blob/Public/AWS/build-vpc-and-pubsub-by-cfn/templates/cfn-template.yml)

### CloudFomationの利用

下記の手順に沿って、マネコンからスタック(*1)を作成します。

    *1. スタックとは  
    構築するAWSリソースを管理する単位です。基本的にCloudFormationテンプレ―トと1:1の関係になっています。


1. CloudFormationコンソールに入ってください。
1. 左ペインから ***スタック*** を選択してください。
1. 右上の ***スタックの作成*** から ***新しいリソースを使用(標準)*** を選択します。　
1. 各パラメータを埋めて ***次へ*** を選択します。

    |Key|Value|
    |---|---|
    |テンプレートの準備|テンプレートの準備完了|
    |テンプレートソース|テンプレートファイルのアップロード|
    |ファイルの選択|ローカルに保存したyamlファイル|
1. スタックの名前を ***cfn-handson-YYYYMMDD*** にして、各パラメータを埋めた後 ***次へ*** を押します。
*各リソースの名前タグへの入力は任意です。空欄でも構いません。

    |Key|Value|
    |---|---|---|
    |AZ|ap-northeast-1a|
    |PublicSubnetCidrBlock|192.168.2.0/25 ※埋まっていれば別Cidrを指定すること|
    |VpcCidrBlock|192.168.2.0/24 ※埋まっていれば別Cidrを指定すること|
1. 特に入力せず ***次へ*** を押します。
1. 入力を確かめて、問題なければ ***スタックの作成***　を押しましょう。

先ほどのスタック画面に戻った後 ***cfn-handson-YYYYMMDD*** を選択して ***イベント*** タブ　を開いてみましょう。
ここでは、AWSリソースがそれぞれ作成されていく過程が見ることができます。

ステータスが ***CREATE_IN_PROGRESS*** から ***CREATE_COMPLETE*** になれば完了です。

### 確認
テンプレートファイルで定義されたAWSリソースが意図した通りにできているかVPCコンソールで確認してみてください。
今回作成したAWSリソースの一覧は以下です。

|Resource|Number|
|---|---|
|VPC|1|
|Subnet|1|
|InternetGateWay|1|
|RouteTable|1|

### 環境の削除
最後に今回作成したリソースを削除しましょう。
通常、手動で作成したリソースは一つずつ消さなければいけませんが、CloudFormationで作成したリソースはスタックを消すことで自動的に削除できます！

1. CloudFormationのコンソールに入ります。
1. 左ペインで ***スタック*** を選択します。
1. ***cfn-handson-YYYYMMDD*** を選択して ***削除*** から ***スタックの削除*** を押します。

ステータスが ***DELETE_IN_PROGRESS*** に変わるので、しばらく待って一覧から削除されれば完了です。

## まとめ
CloudFormationを使って、リソースを構築~削除する流れを行いました。

実際に使うことで、メリット感じていただけたのではないかなと思います。
たくさんのAWSリソースが記述可能なので、どんどん試してみてください。

ご覧いただきありがとうございました。
