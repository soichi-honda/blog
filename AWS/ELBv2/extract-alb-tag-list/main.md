## はじめに

ELBv2 の特定タグを CLI で抜きたい！と思った時に使えるシェルスクリプトを書いてみました。


記事目安...10分

[:contents]

## 前提条件

1. *jq* コマンドが環境にインストールされている
1. *AWS CLI* コマンドが環境にインストールされている
1. 実行ホストは、ELBv2 リソースに対して読み込み権限がある

## シェルスクリプト
〇 *extract-elbv2-tags.sh*
```
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
```

## 使い方


*elbv2 describe-tags* コマンドに渡す ELBv2 ARN は、**事前に csv ファイルでご準備ください。**

〇 *input.csv*
```
arn:aws:elasticloadbalancing:ap-northeast-1:xxx:loadbalancer/net/blog-stg-nlb-1/xxx
arn:aws:elasticloadbalancing:ap-northeast-1:xxx:loadbalancer/app/blog-stg-alb-1/xxx

```
※ *while read* は改行コードがある行しか読み込まないため、最終行の末尾が改行コードになっていることを確認してください。

---
抜き出したいタグのキー名を、シェルスクリプト内の以下 *tags* 変数に記述してください。

> tags=("Name" "Env" "Service")

---

実行時は、シェルスクリプトに csv ファイルを渡して実行してください。
```
$ bash extract-alb-tags.sh input.csv
```

---

## 実行結果例

〇elbv2-tags-list.csv
```
Name,Env,Service
blog-stg-nlb-1,stg,test
blog-stg-alb-1,stg,test

```

## まとめ

ほかのリソースで、特定タグを取得したい時もこのスクリプトを改修すれば役立つかもです。

ご覧いただきありがとうございました。
