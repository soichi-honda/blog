## はじめに

EC2(AmazonLinux2) + SG を作成する CloudFormation テンプレートを書きました。  
最新の EBS タイプ **gp3** に対応しています!

検証などの際に是非お使いください！

記事目安...5分

[:contents]

## cfnテンプレートの詳細

cfnテンプレートの中身は、 [こちら](https://github.com/sugaya0204/blog/blob/Public/AWS/CloudFormation/cfn-template-ec2/templates/ec2.yml)をご参照ください。

---

テンプレートで構築されるリソースの詳細は以下です。

〇 EC2 × 1

|Key|Value|
|---|---|
|OS|AmazonLinux2|
|EBS type|gp3|

〇 SG × 1

|Key|Value|
|---|---|
|Inbound|SSH(22)|
|Outbound|ALL|

## 注意事項

* AMI は、SSM 公開パラメータストアから最新のものを取得します。

* このテンプレートで構築した SG は EC2 に自動的にアタッチされます。
