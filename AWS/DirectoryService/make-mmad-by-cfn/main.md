AWS Directory Service の一つ、 AWS Managed Microsoft AD(以下 AWS MMAD) 環境を構築できる CloudFormation を書いてみました。

[:contents]

## Cfnテンプレートについて

★注意点★

- Edition は Standard となっています。
- パラメータで指定した VPC に対して、新規構築した DHCPOptionSet を関連付けます。DHCPOptionSet を変更したくない VPC は絶対に指定しないでください。

---

テンプレートは [こちら](https://github.com/sugaya0204/blog/blob/Public/AWS/DirectoryService/make-mmad-by-cfn/templates/cfn-template-mmad.yml) になります。


## 作った背景

AWS MMAD は従量課金にもかかわらず停止ができないので、割とコストがかかります。

e.g. Standard Edition かつ、2つのドメインコントローラを持つ AWS MMAD を 1ヵ月間使った場合

1時間あたり 0.146USD × 24h × 30 days = 105.12 USD

参考: [料金 \- AWS Directory Service \| AWS](https://aws.amazon.com/jp/directoryservice/pricing/)

ゆえに頻繁に構築したり消した利する必要がありましたが、もういっそ CloudFormation に流すだけの方が楽なんじゃないかと思い作ってみました。


## テンプレートの処理

このテンプレートを流すと、大きく3つの動作が行われます。

1. AWS MMAD を構築する (30分近く時間がかかります)
1. 構築した AWS MMAD の DNS サーバを関連付けた DHCPOptionSet を構築する。
1. VPC と DHCPOptionSet を関連付けます。

## 最後に

当たり前ですが、スタックを削除したら AD 内のデータは消えてしまいます。  
そこは、毎回環境を復元できる Powershell スクリプトを作るしかないと思います。。

スナップショットが AD 削除後も残ってくれれば一番いいのですが。。。

ほかにいい方法があればコメントで教えてください。

## 参考
- [AWS::DirectoryService::MicrosoftAD \- AWS CloudFormation](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html)
- [AWS::EC2::DHCPOptions \- AWS CloudFormation](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html)
- [AWS::EC2::VPCDHCPOptionsAssociation \- AWS CloudFormation](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-dhcp-options-assoc.html)