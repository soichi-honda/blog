#!/bin/bash

# 引数定義
CSVFILE=$1

# ユーザ定義
## 作業ディレクトリの定義
# base_dir_path="/home/ec2-user/certs"
base_dir_path="/mnt/c/Users/user/Desktop/git-repo/blog/AWS/ACM/reimport-cert-into-acm/test/certs"

## 鍵ディレクトリ/ファイルのサフィックス定義
key_file_suffix=".key"

## 証明書ディレクトリ/ファイルのサフィックス定義
cert_file_suffix=".crt"

## リージョンの定義
region="us-west-1"

# 出力用CSVファイル作成
echo "DomainName, Arn, ExpireDate(JST)" > output.csv

# ACM のリストをjson形式で取得
acm_json=$(aws acm list-certificates --region ${region})
# echo "acm_json: ${acm_json}"

# 入力した CSVFILE から一つずつドメイン名を抽出
while read domain_name; do
    # 改行コードの削除
    domain_name=`echo ${domain_name} | sed -e "s/[\r\n]\+//"`

    echo "---Start ${domain_name}---"
    # echo "domain_name: ${domain_name}"

    # 変数定義
    cert_dir_path="${base_dir_path}/${domain_name}"
    # echo "cert_dir_path: ${cert_dir_path}"

    ## 鍵ファイルのパス定義
    key_file="${domain_name}${key_file_suffix}"
    key_file_path="${cert_dir_path}/${key_file}"
    # echo "key_file_path: ${key_file_path}"

    ## サーバ証明書のパス定義
    server_cert_file="${domain_name}${cert_file_suffix}"
    server_cert_file_path="${cert_dir_path}/${server_cert_file}"
    # echo "server_cert_file_path ${server_cert_file_path}"

    # ACM の ARN を取得
    acm_arn=$(echo ${acm_json} | jq -r ".CertificateSummaryList[] | select(.DomainName==\"${domain_name}\") | .CertificateArn")
    # echo "acm_arn: ${acm_arn}"

    if [ -n "${acm_arn}" ]; then
        # ACMへの証明書再インポート
        aws acm import-certificate --certificate fileb://${server_cert_file_path} \
        --private-key fileb://${key_file_path} \
        --certificate-arn ${acm_arn} \
        --region ${region} \
        2>>${base_dir_path}/error.log
    else
        # ACMへの証明書インポート
        acm_arn=$(aws acm import-certificate --certificate fileb://${server_cert_file_path} \
        --private-key fileb://${key_file_path} \
        --region ${region} \
        2>>${base_dir_path}/error.log \
        | jq -r ".CertificateArn")
    fi
    # 再インポート後の有効期限を出力用CSVファイルに出力
    aws acm describe-certificate \
      --certificate-arn "${acm_arn}"  \
      --region ${region} \
      | jq -r '.Certificate| [.DomainName, .CertificateArn, .NotAfter] | @csv' >> ${base_dir_path}/output.csv
done < ${CSVFILE}
echo "---End---"
