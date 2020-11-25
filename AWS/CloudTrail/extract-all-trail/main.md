## はじめに
 CloudTrail を触っていると アカウント内で使われている全トレイルをリージョン超えて、一覧に出したいときってありますよね。  
ということで、全トレイルの一覧をcsvファイルに吐き出すシェルスクリプトを書いてみました。

今回は最低限、トレイル名と、どのリージョンに属するかという情報だけ出します。

記事目安...10分

[:contents]

## 全トレイルを抽出するシェルスクリプト

```bash
#!/bin/bash

# trail-list.csv の生成および、ヘッダーの生成。csv ファイルには、Trail 名と、そのホームリージョンがそれぞれ格納される。
echo "Name, HomeRegion" > trail-list.csv

# CloudTrail 対応リージョンを regions 変数に格納(*1)
regions=("us-east-2" "us-east-1" "us-west-1" "us-west-2" "ca-central-1" "af-south-1" "ap-east-1" "ap-south-1" "ap-northeast-3" "ap-northeast-2" "ap-southeast-1" "ap-southeast-2" "ap-northeast-1" "cn-north-1" "cn-northwest-1" "eu-central-1" "eu-north-1" "eu-west-1" "eu-west-2" "eu-west-3" "eu-south-1" "me-south-1" "us-gov-east-1" "us-gov-west-1" "sa-east-1")

# 全リージョンで、describe-trails を実行(*2)
for region in ${regions[@]}; do
    echo "$region"
    trail_output=$(aws cloudtrail describe-trails --no-include-shadow-trails --region $region )
    if [ $? = 0  ]; then
        echo $trail_output\
        | jq -r '.trailList[] | [.Name, .HomeRegion] | @csv'\
        >> trail-list.csv
        echo "Success"
    fi
    echo "------------"
done
```

\*1. *regions* 変数に格納する値   
ここで格納している全リージョンは **2020/11/25** 時点での CloudTrail 対応リージョンとなっています。  
最新版は [CloudTrail がサポートされているリージョン \- AWS CloudTrail](https://docs.aws.amazon.com/ja_jp/awscloudtrail/latest/userguide/cloudtrail-supported-regions.html) で確認ください。

\*2.  *--no-include-shadow-trails* オプション  
出力結果から各リージョンの シャドウトレイル を除外します。  
同様に、オーガニゼーショントレイル, リージョンレプリケーショントレイルも出力結果に含まれないため、これらを出力結果に含めたい場合はオプションを削除して実行してください。

> Specifies whether to include shadow trails in the response. A shadow trail is the replication in a region of a trail that was created in a different region, or in the case of an organization trail, the replication of an organization trail in member accounts. If you do not include shadow trails, organization trails in a member account and region replication trails will not be returned. The default is true.  

参考: [Specifies whether to include shadow trails in the response\. A shadow trail is the replication in a region of a trail that was created in a different region, or in the case of an organization trail, the replication of an organization trail in member accounts\. If you do not include shadow trails, organization trails in a member account and region replication trails will not be returned\. The default is true\.](https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/describe-trails.html)

\*3. 実行結果に以下のエラーが出た時は、アカウント内で利用するには申請が必要なリージョンに対して、 *describe-trails* している可能性が高いです。
```bash
An error occurred (UnrecognizedClientException) when calling the DescribeTrails operation: The security token included in the request is invalid
```

## まとめ

よき CloudTrail ライフを!

ご覧いただきありがとうございました。
