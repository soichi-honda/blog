## はじめに
CloudWatch Logs に 出力した VPC フローログ情報を CloudWatch Insight で色々加工してみます。

記事目安...10分

[:contents]

## VPC フローログのログ形式について
デフォルトでは以下の形式で保存されます。また各値は *parse* コマンドを使う必要なく、CloudWatch Insight で取り出せます(*1)。  

```
<version> <account-id> <interface-id> <srcaddr> <dstaddr> <srcport> <dstport> <protocol> <packets> <bytes> <start> <end> <action> <log-status>
```

*1. 各値を抜き出すとき、指定するフィールド名が地味に異なるので注意です。
[f:id:swx-sugaya:20201124115324p:plain]

自由にカスタムできるので、このフォーマットに当てはまらない場合もあります。

参考: [VPC フローログ \- Amazon Virtual Private Cloud \- デフォルト形式](https://docs.aws.amazon.com/ja_jp/vpc/latest/userguide/flow-logs.html#flow-logs-default)

---

今回は、 [フローログレコードの例 \- Amazon Virtual Private Cloud](https://docs.aws.amazon.com/ja_jp/vpc/latest/userguide/flow-logs-records-examples.html#flow-log-example-accepted-rejected) に載っているログを少し加工して、サンプルログとしています。

〇サンプルログ
```
2 123456789010 eni-1235b8ca123456789 172.31.16.139 172.31.16.21 20641 22 6 20 4249 1418530010 1418530070 ACCEPT OK
※ eni-1235b8ca123456789 の IP アドレスは、172.31.16.21 と仮定します。
```

---

**ロググループ** は、自分の VPC フローログを保存しているロググループ名を指定してください。

**ログストリーム** は ENI ごとに生成されます。

ドキュメントにもそのように書いてありますね。

> If you launch more instances into your subnet after you've created a flow log for your subnet or VPC, a new log stream (for CloudWatch Logs) or log file object (for Amazon S3) is created for each new network interface. 

参考: [VPC フローログ \- Amazon Virtual Private Cloud](https://docs.aws.amazon.com/ja_jp/vpc/latest/userguide/flow-logs.html)

## VPC フローログの解析クエリ集

今回は Inbound 通信に着目しました。
Outbound 通信について調べたいときは、 dst/src の部分を反対にして考えてください。

#### ENI のどの wellknown ポートで Inbound 通信が ACCEPT されているか確認するクエリ

```sql
fields @message
| filter @logStream =~ /<対象 ENI ID>/
| filter (dstAddr =~ /<対象 ENI のプライベート IP アドレス>/ and 0 <= dstPort and dstPort <= 1023 and action =~ /ACCEPT/)
| count (*) by dstPort
| display dstPort
| limit 10
```

〇凡例  
ENI *eni-1235b8ca123456789* における どの wellknown ポートが Inbound 通信で ACCEPT されている確認する
```sql
fields @message
| filter @logStream =~ /eni-1235b8ca123456789/
| filter (dstAddr =~ /172.31.16.21/ and 0 <= dstPort and dstPort <= 1023 and action =~ /ACCEPT/)
| count (*) by dstPort
| display dstPort
| limit 10
```
〇結果

|dstPort|
|---|
|22|

#### ENI の特定ポートで Inbound 通信が許可されているか確認するクエリ

```sql
fields @message
| filter @logStream =~ /<対象ENI ID>/
| filter (dstAddr =~ /<対象 ENI のプライベート IP アドレス>/ and　dstPort in [<ポート番号1>, <ポート番号2>, ...] and action =~ /ACCEPT/)
| count (*) by dstPort
| display dstPort
| limit 10
```

〇凡例  
ENI *eni-1235b8ca123456789* SSH(22) および HTTP(80) のポートに Inbound 通信があるか確認する。
```sql
fields @message
| filter @logStream =~ /eni-1235b8ca123456789/
| filter (dstAddr =~ /172.31.16.21/ and　dstPort in [22, 80] and action =~ /ACCEPT/)
| count (*) by dstPort
| display dstPort
| limit 10
```

〇結果

|dstPort|
|---|
|22|


#### 特定リソースからの Inbound 通信について調べる
```sql
fields @message
| filter @logStream =~ /<対象のENI ID>/
| filter (srcAddr =~ /<送信元リソースの IPアドレス>/ and dstAddr =~ /<対象 ENI のプライベート IP アドレス>/)
| count (*) by dstPort, action
| display dstPort, action
| limit 10
```


〇凡例  
IP アドレス *172.31.16.139* のリソースから、 ENI *eni-1235b8ca123456789* への Inbound 通信を抽出する
```sql
fields @message
| filter @logStream =~ /eni-1235b8ca123456789/
| filter (srcAddr =~ /172.31.16.139/ and dstAddr =~ /172.31.16.21/)
| count (*) by dstPort, action
| display dstPort, action
| limit 10
```

〇結果

|dstPort|action|
|---|
|22|ACCEPT|

## まとめ

また、よさげなクエリができたら追記します!