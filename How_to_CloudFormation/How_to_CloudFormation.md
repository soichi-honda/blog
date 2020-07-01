突然ですが、CloudFormationって便利ですよねー。
ハンズオン形式のブログ書きたいとかにも使えますし。
ということで今回はCloudFormationを触ってみます。

お時間ない人は完成したYamlファイルを最後に載せているので、そこだけ見ていただければ！

記事目安...15分

# 事前知識
CloudFormation...AWSリソースをコードのように定義して作成するためのサービス。いわゆるIaC(=Infrastructure as Code)。
テンプレートファイルはYamlとJsonのどちらでも記述可能。

# ゴール
今回はVPC × 1, PublicSubnet × 1, InternetGW × 1, RouteTable × 1について定義したテンプレートファイルを作成しようと思います。今回はYamlで書きます。
最終的に出来上がる構成図イメージは以下です。

[How_to_CloudFormation_1]

# 作業
CloudFormationのテンプレートファイルは色々なセクションに分かれています。
今回はとりあえず最低限の以下2セクションを扱います。
|Key|Value|
|---|---|
|Parameters|ユーザがパラメータを定義するセクション|
|Resources|作成するAWSリソースを定義するセクション|

```yaml
Parameters:

Resources:
```

## VPCの定義
まずは、VPCについて定義していきます。以下のページに載っているVPCを定義するのに必要なパラメータを確認して、貼り付けましょう。
なお、各Resourceには論理IDと呼ばれる一意の名前を付けることができるのでそちらも合わせて書きます。ここではMyVPCとしました。
[AWS::EC2::VPC](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html)

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

各パラメータの詳細については先ほどのAWS公式ページを見ていただくといいと思います。
今回僕は以下のように書きました。
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
ちなみに *!Ref* とは *Ref: xxx* の短縮系です。
CloudFormationにはたくさん関数が用意されているので、気になった人は
参考: [擬似パラメーター参照](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html)

Ref関数を定義したということは、参照先を定義する必要もあります。
今回は定義したパラメータはすべてユーザ定義のため、Parameterセクションに記述していきます。
|Key|Value|
|---|---|
|Description|パラメータの説明を記述する|
|Type|パラメータの型を記述する。|
|Default|デフォルトで入力されるパラメータを定義する|
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

これでVPCは完成しました。

## Public Subnetの定義
続いてPublic Subnetについて定義します。以下のページをを確認しながら進めてください。
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

続いて各パラメータをいじって下記のようにしました。
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
ここでも2つ新しいことをやっています。
1. Parameters > AZ > Type で *AWS::EC2::AvailabilityZone::Name* と宣言しています。これはAWS 固有のパラメータータイプです。今回の場合、設定することでマネコンの現在のリージョンをもとにアベイラビリティゾーンの一覧を選択することができます。
参考: [パラメータ](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html)
1. 最終行で !Ref MyVPC と書いていますが、実はVPCの論理IDをRef関数に渡すと、該当するVPCリソースのVPC IDを返してくれます。
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
localターゲットへのルーティングは定義しなくても自動でつきます。
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

ということでVPC × 1, PublicSubnet × 1, InternetGW × 1, RouteTable × 1 を作成するためのテンプレートファイルができました。

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

記事が長くなってしまったので、CloudFormationに流すのはまた別の記事で書こうと思います。

# まとめ
今回はCloudFormationで使うテンプレートファイルの書き方についてまとめました。
基本はAWSドキュメントの見方さえわかってしまえば記述自体はすぐできそうですが、RouteTableのように複数にリソースに分割して定義するのはちょっと大変だなあという印象です。

しかし冪等性が担保されているなどメリットがあることは間違いないので、ぜひみなさんも書いてみてください。

ご覧いただきありがとうございました。