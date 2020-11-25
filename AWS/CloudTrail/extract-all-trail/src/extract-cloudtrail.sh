#!/bin/bash

# trail-list.csv の生成および、ヘッダーの生成。csv ファイルには、Trail 名と、そのホームリージョンがそれぞれ格納されます。
echo "Name, HomeRegion" > trail-list.csv

# CloudTrail 対応リージョンを regions 変数に格納(*1)
regions=("us-east-2" "us-east-1" "us-west-1" "us-west-2" "ca-central-1" "af-south-1" "ap-east-1" "ap-south-1" "ap-northeast-3" "ap-northeast-2" "ap-southeast-1" "ap-southeast-2" "ap-northeast-1" "cn-north-1" "cn-northwest-1" "eu-central-1" "eu-north-1" "eu-west-1" "eu-west-2" "eu-west-3" "eu-south-1" "me-south-1" "us-gov-east-1" "us-gov-west-1" "sa-east-1")

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