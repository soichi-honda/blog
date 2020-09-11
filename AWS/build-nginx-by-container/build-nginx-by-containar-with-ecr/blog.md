はじめまして、サーバーワークス2年目、エンジニアの菅谷です。  

今回のテーマは「AWSサービスのECRとECSを使ってnginxのページを表示させよう」です。  
本ページでは前編として、ECRへのイメージのプッシュまでを行いたいと思います。

この2つのサービスを使用すると自分で作成したDockerイメージからコンテナを素早く簡単に起動できます。

実はこのテーマ、ちょうど1年前に同じような内容で記事を書いてます。ただ、いかんせん不備が多かったので書き直しています。  
一年間の僕の成長ぶりを見たいよって方がいれば以前の記事もご参照ください笑

[新卒1年目がECR+ECSを使ってNginxやってみた-前編](https://blog.serverworks.co.jp/tech/2019/11/13/post-74593/)

記事目安-15分~20分

[:contents]

## 事前知識
### Docker
コンテナを作成・管理するサービス。

#### コンテナ  
プロセス単位で仮想化された個々の環境を指す。  
必要な時に即座かつ容易に環境構築でき、壊すのも簡単。
#### DockerFile  
どのようなコンテナを起動するか定義するファイル。
#### Dockerイメージ  
コンテナを作成する際に元となるイメージファイル。
前述のDockerFileをビルドすることで作成される。  
Docker社が提供しているものや一般ユーザが公開してるものもある。

### ECR
AWSが提供するDockerイメージのリモート管理サービス。

ECSと組み合わせればマネコンからでもローカル環境からでも迅速にコンテナ環境の構築ができる。

## ゴール
全編通してのゴールは以下です。

[f:id:swx-sugaya:20200818175140p:plain](assets/build-nginx-by-containar-with-ecr_1.png)

前編では、EC2上で準備したDockerfileをECRにPushするところまでをゴールとします。(図でいう手順①)

## 作業
### 作業環境の構築
まずはCloudFormationテンプレ―トを使用して、以下環境を構築します。

[f:id:swx-sugaya:20200818175146p:plain](assets/build-nginx-by-containar-with-ecr_2.png)

リソースと対応するCloudFormationテンプレートを準備したので、手元に控えてスタックを作成してください。

|Resource|TemplateURL|StackName|Detail|
|---|---|---|---|
|SSM Parameter|[cfn-template-common.yml](https://github.com/sugaya0204/blog/blob/Public/AWS/build-nginx-by-containar/build-nginx-by-containar-with-ecr/templates/cfn-template-common.yml)|docker-handson-common-YYYYMMDD|他のテンプレートファイルが参照する値をパラメータストアに保存します。|
|VPC, PublicSubnet|[cfn-template-vpc.yml](https://github.com/sugaya0204/blog/blob/Public/AWS/build-nginx-by-containar/build-nginx-by-containar-with-ecr/templates/cfn-template-vpc.yml)|docker-handson-vpc-YYYYMMDD|-|
|EC2|[cfn-template-ec2.yml](https://github.com/sugaya0204/blog/blob/Public/AWS/build-nginx-by-containar/build-nginx-by-containar-with-ecr/templates/cfn-template-ec2.yml)|docker-handson-ec2-YYYYMMDD|-|

CloudFormationの手順は[こちら](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn-2)のページにまとめているので、参考にしてください。

### IAMRole権限の付与
#### IAM Roleの作成
Worker インスタンスでECRを操作するためのIAM Roleを作成します。

1. マネコンから IAM コンソールへアクセスします。
1. 左ペインから ***ロール*** を選択して ***ロール*** の作成を押します。
1. 各パラメータを選択して ***次のステップ*** へ。

    |Key|Value|
    |---|---|
    |信頼されたエンティティの種類を選択|AWSサービス|
    |一般的なユースケース|EC2|

1. ***AmazonEc2ContainerRegistryFullAccess*** を選択して ***次のステップ:タグ*** へ。
1. タグは特に挿入せず、***次のステップ:確認*** へ。
1. 以下パラメータを埋めて ***ロールの作成*** を押します。

    |Key|Value|
    |---|---|
    |ロール名|YYYYMMDD-docker-handson-worker-role|

#### IAMRoleのアタッチ
作成したIAM RoleをWorkerインスタンスにアタッチします。

1. EC2コンソールにて、左ペインの ***インスタンス*** を選択します。
1. 一覧からインスタンス名 ***YYYYMMDD-docker-handson-worker*** を選択します。  
※この時点でインスタンスがない場合はCloudFormationスタックがエラーを吐いていないか確認してください。
1. ***アクション*** から ***インスタンスの設定*** を押して、 ***IAMロールの割り当て/置換*** を選択します。
1. IAM Role 欄に ***YYYYMMDD-docker-handson-worker-role*** を入れて ***適用*** を押します。

これで必要な権限の付与は完了です。

### Dockerイメージの作成
#### Dockerfileの作成
WorkerインスタンスへSSHログインします。

---

dockerパッケージを入れ、そのままサービス起動します。
```bash
$ sudo yum -y update 
$ sudo yum -y install docker
$ sudo systemctl start docker
```

---

あらかじめ使う単語を環境変数に入れます。

```bash
$ export REGION_NAME=ap-northeast-1
$ export REPOSITORY_NAME=YYYYMMDD-docker-handson-repo
$ export -p //確認用
```

---

Nginxで表示させたいオリジナルのhtmlファイルを作成します。
```bash
$ vi new_index.html
```
```html
<p>Deployed Nginx content using Docker container!!</p>
```

---

続いてDockerfileの中身を定義します。


```bash
$ vi Dockerfile
```
```
ARG VERSION=2
FROM amazonlinux:$VERSION
MAINTAINER sugaya
RUN echo "now building..."
RUN amazon-linux-extras install nginx1 -y　#Nginxのversionは都度確認して変更してください。
ADD ./new_index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["/usr/sbin/nginx", "-g", "daemon off;"] #フォアグラウンドでNginxを起動する
```

※捕捉

1. Dockerfile内の各パラメータ  
それぞれのパラメータは以下を参考にしてください。

    |Key|Value|
    |---|---|
    |ARG|宣言された変数を格納する。FROMより前に宣言されたARGは、ビルドステージ内に含まれないためFROM以降で利用するには再宣言する必要がある|
    |FROM|ベース・イメージを定義する。宣言することでビルド時に公開リポジトリからイメージを取得する。|
    |MAINTAINER|Dockerfileの作者情報を記述する|
    |RUN|ビルド時に実行されるコマンドを定義する|
    |ADD|指定のファイルをコンテナ内に保存する|
    |EXPOSE|コンテナの実行時にコンテナ上のどのポートでリッスンするか指定する|
    |CMD|コンテナ起動時に実行されるコマンドを定義する|

    参考: [Dockerfile リファレンス](http://docs.docker.jp/engine/reference/builder.html)

1. バックグラウンド動作  
コンテナ内で起動するプロセスがバックグラウンド実行の場合は起動後すぐ停止してしまうので、必ずフォアグラウンドで実行しましょう。  
参考: https://heartbeats.jp/hbblog/2014/07/3-tips-for-nginx-on-docker.html

1. Nginxの起動  
 amazonlinux2イメージにデフォルトでsystemdが導入されていないため、systemctl ではなく直接nginxを起動させています。  
参考: https://qiita.com/mach3/items/33f2b234babe679c759f

---

ここまで色々やりましたが、フォルダが以下の構成になっていればOKです

```bash
$ ls
Dockerfile  new_index.html
```

#### Dockerイメージの作成
出来上がったDockerfileをビルドしてDockerイメージを作成しましょう。

---

ビルドには ***docker image build*** コマンドを使います。

```bash
$ sudo docker image build -t nginx-test .
$ sudo docker images //確認用
```

※捕捉

1. 各オプションについて  
"-t" はビルドイメージの名前をしてします。
1. "."について  
*docker image build* を実行する際は、使用するDockerfileがあるディレクトリを指定する必要があります。
ここでは、"."を付けることで現在いるディレクトリを指定しています。

#### Dockerイメージの動作確認
作ったDockerイメージを起動してみましょう。

コンテナの起動は *docker container run* で行えます。  

```bash
$ sudo docker container run -d -p 8080:80 nginx-test:latest
$ sudo docker ps -a //プロセス起動確認
```
※捕捉

1. 各オプションについて  
"-d"を付けることで、コンテナプロセスをバックグラウンドで起動します。    
"-p <LocalPort>:<ContainerPort>" は、特定のローカルポートからきた通信を特定のコンテナポートへ誘導するようマッピング定義をします。

---

実際にWebブラウザでWorkerの8080ポートにアクセスしてみましょう。

***http://"PublicIPaddress":8080*** にアクセスすると先ほど定義したhtmlファイルが反映されているはずです。

---

動作確認後はコンテナを削除しましょう。   
必ず停止させてから削除してください。

```bash
$ sudo docker ps -a
$ sudo docker stop <CONTAINER ID> //コンテナを停止
$ sudo docker rm <CONTAINER ID> //コンテナを削除
$ sudo docker ps -a
```

### ECRへのプッシュ
Dockerイメージが正しいことを確認したので、ECRにプッシュを行います。

---

まずはECRへログインします。以下コマンドを実行しましょう。  
ものすごい返り値が出るのでびっくりしますが、コピペして実行しましょう。

```bash
$ aws ecr get-login --region ${REGION_NAME} --no-include-email
docker login -u AWS -p ××××××××××...(以下略)
$ sudo docker login -u AWS -p ××××××××××...(以下略)
Login Succeeded //これが出ればOK
```

---

続いてECR上にレポジトリを作成します。  
```bash
$ aws ecr create-repository --repository-name ${REPOSITORY_NAME} --region ${REGION_NAME}
```

返り値の ***repositoryUri*** を環境変数 ***REPOSITORY_URI*** に格納しましょう。
```bash
$ export REPOSITORY_URI=<repositoryUri>
$ export -p |grep REPOSITORY_URI
```

---

最後にもう一度DockerイメージをECRレポジトリにプッシュします(イメージ名を変更するため)。

Dockerイメージへビルドしましょう。
```bash
sudo docker build -t ${REPOSITORY_URI}:latest .
```

ECRへプッシュします。
```bash
$ sudo docker push ${REPOSITORY_URI}:latest
```

## 確認

#### マネコンから
ECRコンソールに入ってください。

---

***リポジトリ*** から ***YYYYMMDD-docker-handson-repo*** を選択すると、
latestタグが付いたイメージが確認できます。

#### CLIから
まずaws configureにデフォルトリージョンを登録します。  
これはaws ecr list-images にリージョンを選択するオプションがないためです。  
アップデートがあれば飛ばしてください。
```bash
$ aws configure
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]: ap-northeast-1
Default output format [None]:
```
---

ECRから情報を取得してきます。
```bash
$ aws ecr list-images --repository-name ${REPOSITORY_NAME}
```
JSON形式でレポジトリ内のイメージ一覧が返されるので、latestタグがあることを確認しましょう。

## 後片付け
作成したリソースの後片付けを実施します。  
※後編に進む人はまだ実行しないでください。

#### ECRの削除
ブログ執筆時点で、CLIから消す方法はなさそうです。
ということでマネコンから削除してください。

参考:[リポジトリの削除](https://docs.aws.amazon.com/ja_jp/AmazonECR/latest/userguide/repository-delete.html)

1. ECRコンソールへアクセスします。
1. ***リポジトリ*** > ***YYYYMMDD-docker-handson-repo*** を選択して、***削除*** を押します。

#### その他AWSリソース
以下のリソースも削除してください。

|Resource|Name|
|---|---|
|IAMRole|YYYYMMDD-20200701-docker-handson-worker-role|
|CloudFormation Stack|docker-handson-ec2-YYYYMMDD|
|CloudFormation Stack|docker-handson-vpc-YYYYMMDD|
|CloudFormation Stack|docker-handson-common-YYYYMMDD|

# まとめ

前編では、NginxプロセスのコンテナイメージをECRにプッシュしました。 
こうゆうツールがあると自分がよく使うDockerイメージをリモートに分散管理できるので、積極的にとりいれたいですね。

後編では実際にプッシュしたイメージからコンテナを作成したいと思います。
なるべく早く書きます。頑張ります。

ご覧いただきありがとうございました。