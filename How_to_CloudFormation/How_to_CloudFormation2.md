前回、CloudFormationテンプレートの書き方をやりました。
今回はその続きとして、作ったテンプレートファイルを実際にCloudFormationに流すところをやってみます。

前回記事: []()

# ゴール
最終的に出来上がる構成図は以下です。前回と同じですね。
[How_to_CloudFormation_1]

# 作業
今回使うテンプレートファイルは前回作ったものを流用します。
ローカルに保存していない人は下記をYaml形式で保存しておいてください。
```yaml
Parameters:
# VPC
  VpcCidrBlock:
    Description: Input a VPC IPv4 CidrBlock. ex) 192.168.2.0/24
    Type: String
  VpcName:
    Description: Input a VPC name. This Parameter will be a Name tag.
    Type: String
    Default: ""

# Public Subnet
  AZ:
    Description: Input a AZ where Public Subnet will be created.
    Type: AWS::EC2::AvailabilityZone::Name
  PublicSubnetCidrBlock:
    Description: Input a Public Subnet IPv4 CidrBlock.  ex) 192.168.2.0/25
    Type: String
  PublicSubnetName:
    Description: Input a Public Subnet name. This Parameter will be a Name tag.
    Type: String
    Default: ""

# Internet GW
  InternetGwName:
    Description: Input a IntenetGW name. This Parameter will be a Name tag.
    Type: String
    Default: ""

# RouteTable for Public Subnet
  RouteTableName:
    Description: Input a RouteTable name. This Parameter will be a Name tag.
    Type: String
    Default: ""


Resources:
# VPC
  MyVPC:
    Type: AWS::EC2::VPC
    Properties: 
      CidrBlock: !Ref VpcCidrBlock
      EnableDnsHostnames: true
      EnableDnsSupport: true
      InstanceTenancy: default
      Tags: 
        - Key: Name
          Value: !Ref VpcName

# PublicSubnet
  MyPublicSubnet:
    Type: AWS::EC2::Subnet
    Properties: 
      AvailabilityZone: !Ref AZ
      CidrBlock: !Ref PublicSubnetCidrBlock
      MapPublicIpOnLaunch: true
      Tags: 
        - Key: Name
          Value: !Ref PublicSubnetName
      VpcId: !Ref MyVPC

# InternetGW
  MyInternetGW:
    Type: AWS::EC2::InternetGateway
    Properties: 
      Tags: 
        - Key: Name
          Value: !Ref InternetGwName
  
  MyVPCGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties: 
      InternetGatewayId: !Ref MyInternetGW
      VpcId: !Ref MyVPC

# RouteTable for Public Subnet
  MyRouteTable:
    Type: AWS::EC2::RouteTable
    Properties: 
      Tags: 
        - Key: Name
          Value: !Ref RouteTableName
      VpcId: !Ref MyVPC

  MyPublicRoute:
    Type: AWS::EC2::Route
    Properties: 
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref MyInternetGW
      RouteTableId: !Ref MyRouteTable

  MySubnetRouteTableAssociation:
      Type: AWS::EC2::SubnetRouteTableAssociation
      Properties: 
        RouteTableId: !Ref MyRouteTable
        SubnetId: !Ref MyPublicSubnet
```

マネコンからCloudFormationコンソールに入ってください。

左ペインから *スタック* を選択してください。

右上の *スタックの作成* > *新しいリソースを使用(標準)* を選択します。　

各パラメータを埋めて *次へ* を選択します。
※余談ですが、今回はYaml内で短縮系の表現を用いているので、Amazon S3 からファイルを実行することはできません。
|Key|Value|
|---|---|
|テンプレートの準備|テンプレートの準備完了|
|テンプレートソース|テンプレートファイルのアップロード|
|ファイルの選択|ローカルに保存したyamlファイル|

スタックの名前を *cf-handson-YYYYMMDD* にして、各パラメータを埋めた後 *次へ* を押します。
※各リソースの名前タグへの入力は任意です。空欄でも構いません。
|Key|Value|
|---|---|---|
|AZ|ap-northeast-1a|
|PublicSubnetCidrBlock|192.168.2.0/25 ※埋まっていれば別Cidrを指定すること|
|VpcCidrBlock|192.168.2.0/24 ※埋まっていれば別Cidrを指定すること|

特に入力せず *次へ* を押します。

入力を確かめて、問題なければ *スタックの作成*　を押しましょう。

先ほどのスタック画面に戻った後 *cf-handson-YYYYMMDD* を選択して *イベント* タブ　を開いてみましょう。
ここでは、AWSリソースがそれぞれ作成されていく過程が見ることができます。

ステータスが *CREATE_IN_PROGRESS* > *CREATE_COMPLETE* になれば完了です。

# 確認
テンプレートファイルで定義されたAWSリソースが意図した通りにできているかVPCコンソールで確認してみてください。
今回作成したAWSリソースの一覧は以下です。
|Resource|Number|
|---|---|
|VPC|1|
|Subnet|1|
|InternetGateWay|1|
|RouteTable|1|

# 削除
最後に今回作成したリソースを削除しましょう。
通常、手動で作成したリソースは一つずつ消さなければいけませんが、
CloudFormationで作成したリソースはスタックを消すことで自動的に削除されます！

CloudFormationのコンソールに入ります。

左ペインでスタックを選択します。

*cf-handson-YYYYMMDD* を選択して *削除* > *スタックの削除* を押します。

ステータスが *DELETE_IN_PROGRESS* に変わるので、しばらく待って一覧から削除されれば完了です。

# まとめ
CloudFormationを使って、リソースを構築~削除する流れを行いました。
実際に使うことで、メリット感じていただけたのではないかなと思います。
たくさんのAWSリソースが記述可能なので、どんどん試してみてください。

ご覧いただきありがとうございました。
