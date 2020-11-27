#!/bin/bash

# 読み込むファイル用の変数の定義
CSVFILE=$1

# 抜き出したい Tag キーの配列
tags=("Name" "Env" "Service")

#ヘッダー　 & csvファイルの生成
header="$(IFS=,; echo "${tags[*]}")"
echo "$header" > elbv2-tags-list.csv

while read arn; do
    # Tag 値を一時的に格納する変数の定義&初期化
    value_array=()

    # 改行コードの削除
    arn=`echo $arn| sed -e "s/[\r\n]\+//"`

    # ALB の　Tag を抜き取る
    alb_json=$(aws elbv2 describe-tags --resource-arns $arn)

    # Tag 値の抽出
    for ((i=0; i <${#tags[*]}; i++)) do
        value=$(echo $alb_json| jq -r ".TagDescriptions[].Tags[] | select(.Key==\"${tags[$i]}\") | .Value")
        value_array+=("$value")
    done

    # CSVへの保存
    value_array="$(IFS=,; echo "${value_array[*]}")"
    echo ${value_array}
    echo "$value_array" >> elbv2-tags-list.csv

done < ${CSVFILE}
