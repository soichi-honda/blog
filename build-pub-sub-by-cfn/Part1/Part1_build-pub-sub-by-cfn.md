IaCっていいですよね。  
ということで今回はCloudFormationを触ってみます。

お時間ない人は完成したYamlファイルを最後に載せているので、そこだけ見ていただければ！

記事目安...15分

# 事前知識
## CloudFormation
AWSリソースやサードパーティ製アプリケーションリソースをコードのように定義して、実際に作成できるサービス。  
IaCを実現するうえで非常に重要なサービスである。

AWSリソースを構築する場合、利用料金は無料。

参考: [AWS CloudFormation](https://aws.amazon.com/jp/cloudformation/)

# ゴール
今回は前編・後編に分けてやっていきます。

前編ではリソースをテンプレートファイルに定義するところに注力しようと思います。
|Resource|Number|
|---|---|
|VPC|1|
|PublicSubnet|1|
|InternetGW|1|
|RouteTable|1|

最終的に出来上がる構成図イメージは以下です。

[assets/build-pub-sub-by-cfn_1.PNG]

# 作業
CloudFormationのテンプレートファイルは色々なセクションに分かれています。

今回は最低限必須な2セクションを扱います。
|Key|Value|
|---|---|
|Parameters|ユーザがパラメータを定義するセクション|
|Resources|作成するAWSリソースを定義するセクション|

```yaml
Parameters:

Resources:
```

※作成過程をわかりやすくするためにあえてこのように書いてます。これだけではYamlシンタックスとしては誤りなので注意してください。

## VPCの定義
まず、VPCについて定義していきます。

以下ページに載っているVPCを定義するのに必要なパラメータを確認して、貼り付けましょう。

なお、各Resourceには論理IDと呼ばれる一意の名前を付けることができるのでそちらも合わせて書きます。 

ここではMyVPCとしました。

参考: [AWS::EC2::VPC](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html)

```yaml
Parameters:

Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties: 
      CidrBlock: String
      EnableDnsHostnames: Boolean
      EnableDnsSupport: Boolean
      InstanceTenancy: String
      Tags: 
        - Tag
```

続いて各パラメータを編集します。  
各パラメータの詳細については先ほどのAWS公式ページを見ていただくといいと思います。  
僕は以下のように書きました。
```yaml
Parameters:

Resources:
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

```

ここで突然でてきた *!Ref* に皆さん困惑されたのではないでしょうか。  
これはRef関数と呼ばれるもので、ユーザ定義パラメータや疑似パラメータ(AWSで事前定義されたパラメータ)を参照します。  
ちなみに !Ref とは Ref: xxx の短縮系です。

参考: [擬似パラメーター参照](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html)

CloudFormationにはたくさんの関数が用意されているので、気になった人は確認してみてください。

参考: [組み込み関数リファレンス](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)


Ref関数を定義したことにより、参照先を定義する必要があります。 

定義したパラメータはすべてユーザ定義パラメータのため、Parameterセクションに記述していきます。
|Key|Value|
|---|---|
|Description|パラメータについて説明を記述する|
|Type|パラメータの型を記述する。|
|Default|デフォルトで入力されるパラメータを定義する|

参考: [パラメータ](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html)
```yaml
Parameters:
  VpcCidrBlock:
    Description: Input a VPC IPv4 CidrBlock. ex) 192.168.2.0/24
    Type: String
  VpcName:
    Description: Input a VPC name. This Parameter will be a Name tag.
    Type: String
    Default: ""

Resources:
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
```

これでVPCが完成しました。

## Public Subnetの定義
続いてPublic Subnetについて定義します。  
以下のページをを確認しながら進めてください。

参考:[AWS::EC2::Subnet](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html)

今回は論理IDをMyPublicSubnetで定義します。

```yaml
Parameters:
~省略~

Resources:
~省略~

  MyPublicSubnet:
    Type: AWS::EC2::Subnet
    Properties: 
      AssignIpv6AddressOnCreation: Boolean
      AvailabilityZone: String
      CidrBlock: String
      Ipv6CidrBlock: String
      MapPublicIpOnLaunch: Boolean
      Tags: 
        - Tag
      VpcId: String
```

続いて各パラメータを編集します。
```yaml
Parameters:
~省略~

Resources:
~省略~
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
```

最後にParametersセクションも変更します。 

ここでは2つ新しいことをやっています。
1. AWS::EC2::AvailabilityZone::Name  
Parameters > AZ > Type で *AWS::EC2::AvailabilityZone::Name* と宣言しています。  
これはAWS 固有のパラメータータイプです。  
今回だと、設定することでマネコンの現在のリージョンをもとにアベイラビリティゾーンの一覧を選択することができます。  
参考: [AWS 固有のパラメーター型
](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-specific-parameter-types)
1. !Ref <論理ID>  
最終行で !Ref MyVPC と記述していますが、実はVPCの論理IDをRef関数に渡すと、該当するVPCリソースのVPC IDを返してくれます。
参考: [Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)
```yaml
Parameters:
~省略~
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

Resources:
~省略~
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
```

これでサブネットの定義も完了しました。

## InternetGatewayの定義
InternetGWを定義します。

参考:[AWS::EC2::InternetGateway](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html)

```yaml
Parameters:
~省略~
  InternetGwName:
    Description: Input a IntenetGW name. This Parameter will be a Name tag.
    Type: String
    Default: ""

Resources:
~省略~
  MyInternetGW:
    Type: AWS::EC2::InternetGateway
    Properties: 
      Tags: 
        - Key: Name
          Value: !Ref InternetGwName
```

InternetGWを作成したのでVPCと関連付けます。

参考: [AWS::EC2::VPCGatewayAttachment](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html)

```yaml
Parameters:
~省略~

Resources:
~省略~
  MyVPCGatewayAttachment:
  Type: AWS::EC2::VPCGatewayAttachment
  Properties: 
    InternetGatewayId: !Ref MyInternetGW
    VpcId: !Ref MyVPC
```

これでInternetGWの定義は完了です。

## RouteTableの定義
RouteTableを定義します。

参考:[AWS::EC2::RouteTable](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html)

```yaml
Parameters:
~省略~
  RouteTableName:
    Description: Input a RouteTable name. This Parameter will be a Name tag.
    Type: String
    Default: ""

Resources:
~省略~
  MyRouteTable:
    Type: AWS::EC2::RouteTable
    Properties: 
      Tags: 
        - Key: Name
          Value: !Ref RouteTableName
      VpcId: !Ref MyVPC
```

次にルートテーブルのルーティングを設定します。  
※localターゲットへのルーティングは定義しなくても自動でつきます。

参考: [AWS::EC2::Route](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html)

```yaml
~省略~
Resources:
~省略~
  MyPublicRoute:
    Type: AWS::EC2::Route
    Properties: 
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref MyInternetGW
      RouteTableId: !Ref MyRouteTable
```

さらにRouteTableとSubnetを関連付けます。

参考: [AWS::EC2::SubnetRouteTableAssociation](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html)

```yaml
~省略~
Resources:
~省略~
  MySubnetRouteTableAssociation:
      Type: AWS::EC2::SubnetRouteTableAssociation
      Properties: 
        RouteTableId: !Ref MyRouteTable
        SubnetId: !Ref MyPublicSubnet
```

これでRouteTableの定義も完了です。
# 確認

ということでテンプレートファイルができました。
こちらが完成版となります。

[templates/build-pub-sub-by-cfn.yml]

# まとめ
前編ではCloudFormationで使うテンプレートファイルの書き方についてまとめました。

基本はAWSドキュメントの見方さえわかってしまえば記述自体はすぐできそうですが、RouteTableのように複数にリソースに分割して定義するのはちょっと大変だなあという印象です。

後半では、実際に作ったテンプレート流していきます。

ご覧いただきありがとうございました。