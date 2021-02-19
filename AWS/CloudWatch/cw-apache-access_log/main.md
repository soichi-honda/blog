
## はじめに

Apache のアクセスログを CloudWatch Logs に出力する手順をまとめてみました。

*awslogs* でなく、**amazon-cloudwatch-agent** の方です。

記事目安...10分

[:contents]

## 前提条件

〇実行環境

|Key|Value|
|---|---|
|os|AmazonLinux2|
|httpd|2.4.46-1|
|amazon-cloudwatch-agent|1.247345.35-1|

## セットアップ

### EC2 インスタンスのセットアップ

#### EC2 インスタンスのデプロイ

[こちら](https://blog.serverworks.co.jp/cfn-template-ec2)のブログにある cfnテンプレートを使用して、  
**パブリックサブネット上に** EC2 インスタンスをデプロイしてください。

---

#### (Condtional)SG へのインバウンドルール追加

**※ ループバックアドレス以外で接続確認を行いたい方のみ実施してください。**

"EC2 インスタンスのデプロイ" 項目にて構築した SG に、  
任意の IP アドレスからの HTTP アクセスを許可してください。

---

#### CloudWatch Logs へのログ出力権限の追加

CloudWatchAgent(*amazon-cloudwatch-agent*) から CloudWatch Logs へログ出力を行うために、  
先ほどデプロイした EC2 インスタンスに必要な権限を追加します。

1. 以下の条件で、 IAM Role を作成してください。

    |Key|Value|
    |---|---|
    |名前|httpd-access-log-handson-role|
    |ポリシー|CloudWatchAgentServerPolicy|

1. EC2 コンソールにて、作成した IAM Role を対象の EC2 インスタンスにアタッチしてください。

### Apache のセットアップ

以下のコマンドを実行して、Apache をインストールします。
```sh
$ sudo yum install httpd
```

---

`index.html` ファイルを作成します。中身は適当です。
```sh
$ sudo vi /var/www/html/index.html
```
```html
<p>hogehoge</p>
```

---

Apache を起動します。
```sh
$ sudo systemctl start httpd
$ sudo systemctl status httpd //起動確認
```

---

Apache の確認のために、ループバックアドレスを使用して自分自身に curl しましょう。
```sh
$ curl 127.0.0.1
<p>hogehoge</p> //返り値
```


### amazon-cloudwatch-agent のセットアップ

ここから本命の *amazon-cloudwatch-agent* をセットアップします。

---

*amazon-cloudwatch-agent* をインストールします。

```sh
$ sudo yum install amazon-cloudwatch-agent
```

---

ログ出力設定を行うために、
設定ファイル `amazon-cloudwatch-agent.json` ファイルを新規作成して記述します。

```sh
$ sudo vi /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```
```json
{
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/var/log/httpd/access_log",
                        "log_stream_name": "{instance_id}",
                        "log_group_name": "/var/log/httpd/access_log",
                        "timestamp_format": "%d/%b/%Y:%H:%M:%S %z",
                        "timezone": "UTC"
                    }
                ]
            }
        }
    }
}
```

〇 各パラメータについて

|Key|Detail|
|---|---|
|file_path|CloudWatch Logs に出力するローカルファイルを定義|
|log_stream_name|ログストリーム名の定義|
|log_group_name|ロググループ名の定義<br>*{instance_id}* は、instaceID がロググループ名となる|
|timestamp_format|タイムスタンプを取得するために、ログ内のタイムスタンプ形式を記述する。|
|timezone|タイムスタンプを *UTC* で取得する<br>*timestamp_format* が存在するときのみ有効。|

詳細は [CloudWatch Agent Configuration File: Logs Section](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html#CloudWatch-Agent-Configuration-File-Logssection) を参照してください。

---

*amazon-cloudwatch-agent* を起動します。
```sh
$ sudo systemctl start amazon-cloudwatch-agent.service
$ sudo systemctl status amazon-cloudwatch-agent.service
```

---

これでセットアップはすべて完了です。

## ログの出力確認

再びループバックアドレスを使用して自分自身に curl を打ち、  
Apache アクセスログが CloudWatch Logs にログ出力されるか確認します。

```sh
$ curl 127.0.0.1
<p>hogehoge</p> //返り値
```

---

最後に、 CloudWatch Logs で出力されたログを確認します。

1. ブラウザで CloudWatch コンソールを開いて、CloudWatch Logs のページに行きます。
2. ロググループ `/var/log/httpd/access_log` を開いて、デプロイした EC2インスタンスの *instanceID* のログストリーム を選択します。

問題なければ curl を打った時刻に以下のようなログが出力されるはずです。

```
127.0.0.1 - - [14/Feb/2021:10:36:06 +0000] "GET / HTTP/1.1" 200 16 "-" "curl/7.61.1"
```

## Tips

* *amazon-cloudwatch-agent* のエラーはデフォルトで以下ログファイルに出力されます。
```sh
/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log
```

## 後片付け

リソースを削除しましょう。

|Resource|Name|
|---|---|
|**CloudFormation スタック**|-|
|IAM Role|httpd-access-log-handson-role|
|**CloudWatch ロググループ**|/var/log/httpd/access_log|

*1. 太字のリソースは、料金が発生する可能性があるので、ご注意ください

## まとめ

*amazon-cloudwatch-agent* により、Apache のアクセスログを CloudWatch Logs に出力する方法に触れました。

CloudWatch Logs にログを貯めると、サーバにログインしなくてもログ解析ができるようになり安心安全なので、お金が許す限りは保存したいですね。

ご覧いただきありがとうございました

## 参考

[CloudWatchAgent設定ファイルを手動で作成または編集する\-AmazonCloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html)
