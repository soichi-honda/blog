こんにちは。サーバーワークスの菅谷です。

先日、CloudFormationヘルパースクリプトというものを触りました。  
せっかくなのでこれを使ってwebサーバを1台構築します。

以下記事をやっていること前提で話を進めるので、
CloudFormationを触ったことがない人はまずこちらを見ていただけると幸いです。

- [【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 前編](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn)
- [【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 後編](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn-2)

記事目安 - 20 ~ 30分

[:contents]

## 事前知識
### CloudFormationヘルパースクリプト
CloudFormationでEC2インスタンスを作成する際に、テンプレートファイルにスクリプト実行を定義することで使用します。

例えば、インスタンス起動後のソフトウェアインストールやサービス開始などのために使用でき、ミドル~アプリケーションレイヤーまでCloudFormationで自動構築可能になります。

実態はPythonスクリプトらしいですが、本記事ではこの点には触れません。

参考:[CloudFormation ヘルパースクリプトリファレンス](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/cfn-helper-scripts-reference.html)

## 今回のゴール
- Web Server 1台を構築するテンプレートファイルを作成する
- 作成したテンプレートを使い、CloudformationでWebServer 1台を構築する。

せっかくなので、サイトにアクセスしたときに簡易のオリジナルWebページが表示されるようにもします。

## CloudFormationテンプレートの作成
### ECインスタンスの定義
今回はシンプルなWeb Serverを作りたいので、サーバとしては最低限以下の要件があればよさそうです。

|Key|Value|
|---|---|
|OS|AmazonLinux2|
|InstanceType|t3.micro|
|IPAddress|PublicIPAddressがアタッチされている|
|Volume|8GiB|
|Port|HTTPとSSHが開放されている|

ということで定義するリソースは以下です。

|AWS Resource|
|---|
|EC2|
|SG|

※"NetWorkInterface" と "EBS" を分けて記述することもできますが、今回はEC2にまとめて定義します。

参考: [AWS::EC2::Instance](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/  UserGuide/aws-properties-ec2-instance.html)  
参考: [AWS::EC2::SecurityGroup](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/ UserGuide/aws-properties-ec2-security-group.html)

---

上記のドキュメントを参考に、必要な項目のみをテンプレートファイルに記述しました。

※SGのアウトバウンド通信はDefaultで全ポートからの通信を許可します。

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties: 
      BlockDeviceMappings: 
        - BlockDeviceMapping
      ImageId: String
      InstanceType: String
      KeyName: String
      NetworkInterfaces: 
        - NetworkInterface
      Tags: 
        - Tag
      UserData: String
  
  WebSG:
    Type: AWS::EC2::SecurityGroup
    Properties: 
      GroupDescription: String
      GroupName: String
      SecurityGroupIngress: 
        - Ingress
      Tags: 
        - Tag
      VpcId: !Ref VpcId
```

---

続いて、各項目の値を変更します。  
一部はParametersセクションからユーザ定義パラメータを取得します。

※ "!Sub" について  
CloudFormationの組み込み関数の一つ。  
文字列と変数 を組み合わせる場合に使用します。("!Ref" では文字列組み合わせられない。)  
変数は ***${xxx}*** の形式で定義します。  
参考: [Fn::Sub](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-sub.html)

```yaml
Parameters:
  VpcId:
    Description: Select your vpc id.
    Type: AWS::EC2::VPC::Id
  SubnetId:
    Description: Select your subnet id that exits in your selected vpc.
    Type: AWS::EC2::Subnet::Id
  KeyName: 
    Description: Select your key pair.
    Type: AWS::EC2::KeyPair::KeyName
  YYYYMMDD:
    Description: Input a today's date. ex)20200704
    Type: String
  HandsonName:
    Description: Input a handson name. Do not change as much as possible.
    Type: String
    Default: cfn-handson
    AllowedValues: 
      - cfn-handson
  InstanceName:
    Description: Input a instance name. Do not change as much as possible.
    Type: String
    Default: web
    AllowedValues: 
      - web

Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties: 
      BlockDeviceMappings: 
      - DeviceName: /dev/xvda
        Ebs: 
          VolumeSize: 8
          VolumeType: gp2
          DeleteOnTermination: true
      ImageId: ami-0a1c2ec61571737db
      InstanceType: t3.micro
      KeyName: !Ref KeyName
      NetworkInterfaces: 
        - AssociatePublicIpAddress: true
          DeleteOnTermination: true
          GroupSet: 
            - !Ref WebSG
          DeviceIndex: 0
          SubnetId: !Ref SubnetId
      Tags: 
        - Key: Name
          Value: !Sub ${YYYYMMDD}-${HandsonName}-${InstanceName}
      UserData: String

  WebSG:
    Type: AWS::EC2::SecurityGroup
    Properties: 
      GroupDescription: !Sub Security Group attached to ${YYYYMMDD}-${HandsonName}-${InstanceName}
      GroupName: !Sub sg_${YYYYMMDD}-${HandsonName}-${InstanceName}
      SecurityGroupIngress: 
        - CidrIp: 0.0.0.0/0
          Description: SSH port
          FromPort: 22
          IpProtocol: tcp
          ToPort: 22
        - CidrIp: 0.0.0.0/0
          Description: HTTP port
          FromPort: 80
          IpProtocol: tcp
          ToPort: 80
      VpcId: !Ref VpcId

```

これでEC2, SGを構築する記述が完成しました。

### cfn-initの定義

スタックで作成されるEC2インスタンスが、Webサーバとして機能するために実行してほしいコマンドをcfn-initヘルパースクリプトで定義します。

#### cfn-initとUserDataの違いについて
CloudFormationではEC2インスタンスで実行するコマンドを定義する箇所が2つあります。

1. "UserData" で記述する。
1. "cfn-init" ヘルパースクリプトで記述する。

両者の違いは、 ***コマンドの実行成否がスタックの成否に影響するか否か*** です。  
基本的に定義したコマンドが成功しなかったときは、自動的にロールバックしてほしいですよね。  

- "UserData" の場合、コマンドの成否はスタックの成否に影響しないため、定義したコマンドが失敗してもスタックは成功ステータスになります。  
- "cfn-init" の場合、後述の "cfn-signal" と組み合わせることで、定義したコマンドの実行成否はスタックの成否に影響するようになります。

参考: [cfn-init](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/cfn-init.html)

---

今回は、cloud-initを以下のように書きます。

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Metadata:
      AWS::CloudFormation::Init:
        config:
          packages:
            yum:
              httpd: []
          services:
            sysvinit:
              httpd:
                ensureRunning: true
                enabled: true
          files:
            /var/www/html/index.html:
              content: |
                <html>
                  <head>
                    <title>test</title>
                  </head>
                  <body>
                    <p>Success to deploy WebServer</p>
                  </body>
                </html>
              mode: "000644"
              owner: root
              group: root
```

---

ポイントとなる箇所を解説します。

---

cfn-init の設定はメタデータ項目 ***AWS::CloudFormation::Init*** に書く必要があるため　***Metadata*** セクションを追加します。

参考: [メタデータ](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/metadata-section-structure.html)

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Metadata:
      AWS::CloudFormation::Init:
    Properties: 
```

---

Apacheのインストール定義は、以下のように記述します。

|項目|説明|
|---|---|
|packeages|パッケージのインストール方法を定義|
|yum|値に入力されたパッケージをyumでインストールする|
|httpd|httpdパッケージのこと。値にはパッケージのバージョンを定義する ※|

※ httpd項目の値を空にすることで最新パッケージをインストールします。

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Metadata:
      AWS::CloudFormation::Init:
        config:
          packages:
            yum:
              httpd: []
```

---

インストールしたApacheの起動および自動起動の有効化は以下の部分で定義します。  

|項目|説明|
|---|---|
|services|サービスの起動状態を定義。|
|ensureRunning|cfn-initが終了した後でサービスを実行するかを定義。|
|enabled|起動時にサービスを自動起動するかを定義。|

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Metadata:
      AWS::CloudFormation::Init:
        config:
          packages:
            ~省略~
          services:
            sysvinit:
              httpd:
                ensureRunning: true
                enabled: true
```

---

以下の部分で、ドキュメントルートにオリジナルのhtmlファイルを置くよう定義します。

|項目|説明|
|---|---|
|files|インスタンス内にファイルを新しく生成する ※|
|content|ファイルの中身を定義|
|mode|ファイルの権限を定義|
|owner|ファイルの権限ユーザを定義|
|group|ファイルの権限グループを定義|

※存在しないディレクトリ下にファイルを作成することはできません。

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Metadata:
      AWS::CloudFormation::Init:
        config:
          ~省略~
          files:
            /var/www/html/index.html:
              content: |
                "html"
                  "head"
                    "title"test"/title"
                  "/head"
                  "body"
                    "p"Success to deploy WebServer!"/p"
                  "/body"
                "/html"
              mode: "000644"
              owner: root
              group: root
```

---

実はこれだけではcfn-initは動作してくれません。
cfn-init自身の処理を開始するコマンドがないためです。

"Resources.WebServer.Properties.UserData" にcfn-initの開始処理を記述します。

※ UserDataに記述するコマンドは全てBase64で暗号化する必要があります。

参考: [Base64](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-base64.html)

```yaml
        UserData:
          Fn::Base64:
            !Sub |
              #!/bin/bash
              yum update -y
              yum install -y aws-cfn-bootstrap　# Download the latest helper script
              /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource WebServer --region ${AWS::Region}
```

これでcfn-initの記述は完成しました。

この時点でテンプレートファイルを流してもWebServerは立ち上がります。  
しかし、まだコマンドが失敗してもスタックはロールバックが走らない状態です。

最後に、cfn-signalを記述する必要があります。

### cfn-signalの定義

#### cfn-signalヘルパースクリプトとは
cfn-signalヘルパースクリプトは、EC2インスタンスが正常に作成/更新されたかを示すシグナルをCloudFormationに送信します。

cfn-signalを使うには、cfn-initと同様にUserDataに記述します。

参考: [cfn-signal](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/cfn-signal.html)

---

では書いていきましょう。  

今回はcfn-initから返される終了ステータスを確認して、0(成功ステータス)が返された場合にcfn-signalがシグナルをCloudFormationに発信するよう記述します。

※1 終了ステータスとは  
コマンドの実行成否を表すステータス。  
特殊変数 "$?" を用いると、直前に実行したコマンドの成否がわかります。  
参考: [終了ステータス](https://shellscript.sunone.me/exit_status.html)

※2 "-e" オプション  
成否判断に仕様できる終了ステータスを受け取るためのオプション。
0(成功ステータス)の値が入るとcfn-signalがエラーなく起動します。

```yaml
        UserData:
          Fn::Base64:
            !Sub |
              ~省略~
                    /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebServer --region ${AWS::Region}
```

---

また、cfn-signalはCreationPolicy項目を定義する必要があります。

この項目を定義することで、CloudFormationが成功シグナルを受信するかタイムアウト期間超過まで、ステータスが作成完了にならないようになります。

参考: [CreationPolicy 属性](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-attribute-creationpolicy.html)

今回は以下の要件で記述します。

|Key|Value|
|---|---|
|成功までに必要なシグナル数|1回|
|タイムアウト|5分|

```yaml
        UserData:
          ~省略~
      CreationPolicy:
        ResourceSignal:
          Count: 1
          Timeout: PT5M
```

---

これでcfn-signalの設定も完了しました。

完成したテンプレートファイルのURLも載せておくので、比較してみてください。

[cfn-template-ec2.yaml](https://github.com/sugaya0204/blog/blob/Public/build-web-server-by-cfn/templates/cfn-templatet-ec2.yml)

## VPCの立ち上げ

ここから書いたテンプレートファイルを用いてリソースを立ち上げます。

まず、WebServerを起動するVPCを準備しましょう。  
※既存VPCに作成する場合はこちらの手順はスキップしてください。

以下のテンプレートファイルを使って環境を作成してください。  
スタック名は ***cfn-handson-vpc-YYYYMMDD*** でお願いします。

※YYYYMMDDには本日の日付を入れてください。

[cfn-template-vpc.yaml](https://github.com/sugaya0204/blog/blob/Public/build-web-server-by-cfn/templates/cfn-template-vpc.yml)

CloudFormationを作成したことがない方は以下記事を参考にしていただけると。

参考: [【初心者向け】VPC+PublicSubnetをCloudFormationを使って構築する 前編](https://blog.serverworks.co.jp/build-vpc-and-pubsub-by-cfn-2)


## WebServerの立ち上げ

先ほど作成したテンプレートファイルを用いて、WebServerを立ちあげます。  
スタック名は ***cfn-handson-ec2-YYYYMMDD*** でお願いします。

VPCを先ほどのテンプレートファイルで作成した場合は、
以下のパラメータに気を付けてCloudformationでWebServerを立ち上げてください。

|Key|Value|
|---|---|
|VpcId|YYYYMMDD-cfn-handson-vpc|
|SubnetId|YYYYMMDD-cfn-handson-pub-sub|

※ 既存VPCに立てた人は、SubnetにPublicSubnetを選んでいただければ問題ないです。

---

もしシグナルが返ってこないでエラーになっている場合は、cfn-initのログを見てみましょう。

1. 再度スタックの作成を行います。
1. ***スタックオプションの設定ページ*** にて、 ***スタックの作成オプション*** から ***失敗時のロールバック*** を ***無効*** にしてください。
1. 対象EC2インスタンスにSSHログインし、 ***/var/log/cfn-init.log*** を見てください。

参考: [失敗時に AWS CloudFormation スタックがロールバックしないようにする方法を教えてください。](https://aws.amazon.com/jp/premiumsupport/knowledge-center/cloudformation-prevent-rollback-failure/)

## 確認
Webブラウザに ***http://"PublicIPAddress"*** を入力してアクセスしてください。

以下の文言が、Webページに表示されれば完了です。
[f:id:swx-sugaya:20200817170229p:plain](assets/build-web-server-by-cfn_1.PNG)

## 後片付け

最後に作成した環境を片づけていきましょう。

|Resource|Name|
|---|---|
|CloudFormation Stack|cfn-handson-vpc-YYYYMMDD ※新規VPCで作った人のみ|
|CloudFormation Stack|cfn-handson-ec2-YYYYMMDD|

## まとめ

今回はCloudFormationを使ってWebServerを作成しました。

ヘルパースクリプトの部分はなかなか理解するのが難しいですが、
ミドル~アプリレイヤ―まで記述できるのは非常に魅力的ですよね。  

なかなかのボリュームになってしまいましたが、ご覧いただきありがとうございました。
