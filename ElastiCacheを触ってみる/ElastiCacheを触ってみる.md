# はじめに
ElastiCache for Redisを触ったので、備忘録。  
ハンズオン形式で書いたのでぜひ試してみてください。

# 事前知識
## ElastiCacheとは
- 完全マネージド型のインメモリデータストア
- RedisとMemcachedの2種類がある。
- RedisではデータをKey:Valueの形式で保存する。従来のキーバリューストアとは異なり、文字列以外の様々なデータ構造を格納することができる。
- データはHDDやSSDなどのディスクではなく、メモリに蓄積される。したがってレイテンシーが非常に小さい。

## ユースケース
1. リアルタイム処理などにおいて、レイテンシーの少ないDBとして使用する  
※この場合データを永続化できるRedisを使用するとよさそう
1. セッションIDなど一時的なデータの管理を行うDBとして使用する
1. DBのキャッシュサーバとして使用する  
※マルチスレッドであるMemcachedを使用した方がキャッシュ性能はよさそう

## ゴール
- 以下の構成でリソースを作成する

[Elasticache_1]

- Redis内に以下のデータを登録する
    |key|value|type|
    |---|---|---|
    |word|hello|String|
    |user|hoge|List|
    |user|piyo|List|

# 環境準備
以下の環境まで用意しておいてください。

[Elasticache_2]

**Subnet**
- Public Subnet x 1  
    タグ > Name：redis-handson-<今日の日付>-pub
- Private Subnet x 1  
    タグ > Name：redis-handson-<今日の日付>-prv

**EC2**
- AmazonLinux2
- t3.micro
- Public Subnetに配置
- タグ > Name：redis-handson-<今日の日付>
- SG
    |Key|Value|
    |---|---|
    |名前|redis-handson-<今日の日付>-ec2|
    |説明|redis-handson-<今日の日付>-ec2|
    - inbound
        |プロトコル|ポート|ソース|
        |---|---|---|
        |SSH|22|<自分のPCのIPアドレス>|
    - outbound
        |プロトコル|ポート|送信先|
        |---|---|---|
        |すべて|すべて|0.0.0.0/0|

# ElastiCacheハンズオン
## SGの準備
各種パラメータは以下を参考にしてください。
|Key|Value|
|---|---|
|名前|redis-handson-<今日の日付>-redis|
|説明|redis-handson-<今日の日付>-redis|
**ルール**
- inbound
    |プロトコル|ポート|ソース|
    |---|---|---|
    |カスタムTCP|6379|<接続元EC2にアタッチされたSGID>|
    
- outbound
    |プロトコル|ポート|送信先|
    |---|---|---|
    |すべて|すべて|0.0.0.0/0|

## パラメータグループの準備
ElastiCacheダッシュボードにて、**[パラメータグループ]** > **[パラメータグループの作成]**　を選択。

パラメータは以下を参照。
|Key|Value|
|---|---|
|ファミリー|redis5.0|
|名前|redis-handson-<今日の日付>|
|説明|redis-handson-<今日の日付>|

## サブネットグループの準備
ElastiCacheダッシュボードにて、**[サブネットグループ]** > **[サブネットグループの作成]**　を選択。

パラメータは以下を参照。
|Key|Value|
|---|---|
|名前|redis-handson-<今日の日付>|
|説明|redis-handson-<今日の日付>|
VPC, AZ, Subnetについては、今回用意した環境に沿って値を埋めること。  
※Subnetは *redis-handson-<今日の日付>-prv* 選択する。

## ElastiCache for Redisの構築
ElastiCacheダッシュボードにて、**[Redis]** > **[作成]**　を選択。

パラメータは以下を参照。
|Key|Value|
|---|---|
|クラスターエンジン|Redis|
|クラスターモード|無効|
|名前|redis-handson-<今日の日付>|
|説明|redis-handson-<今日の日付>|
|エンジンバージョンの互換性|5.0.6 ※5.0系であれば最新のものでOK|
|ポート|6379|
|パラメータグループ|redis-handson-<今日の日付>|
|ノードタイプ|cache.t3.micro|
|レプリケーション数|0|
|自動フェイルオーバーを備えたマルチ AZ|無効|
|サブネットグループ|redis-handson-<今日の日付>|
|優先アベイラビリティーゾーン|指定なし|
|セキュリティグループ|redis-handson-<今日の日付>|
|保管時の暗号化| 無効|
|送信中の暗号化| 無効|
|シードする RDB ファイルの S3 の場所|空欄|
|自動バックアップの有効化| 無効|
|メンテナンスウインドウ|指定なし|
|SNS通知トピック|通知の無効化|

# 確認
## redis-cliのインストール
今回はredis-cliの4.0をインストールする。
```bash
$ sudo amazon-linux-extras install redis4.0
$ which redis-cli
```

## データの登録
EC2にSSHログインする。

以下コマンドを実行し、Redisへ接続をする。
```bash
$ redis-cli -h <ElastiCacheのプライマリエンドポイント> -p 6379
※プライマリエンドポイントの":6379"を含めないこと。
```

データを**String型**で登録する。
|コマンド|詳細|
|---|---|
|set <key> <value>|keyに対するvalueをString型で登録する|
|get <key>|String型のkeyに対するvalueを取得する|

```bash
$ set word hello => OK
$ get word => "hello"
```
データを**List型**で登録する。
|コマンド|詳細|
|---|---|
|rpush <key> <value>|keyに対するvalueをList型で登録する|
|lrange <key> <start> <end>|List型のkeyに対するvalueを取得する。先頭の要素を0, 2番目の要素を1として扱う|
```bash
> rpush user hoge => (integer) 1
> rpush user piyo => (integer) 2
> lrange user 0 1
1) "hoge"
2) "piyo"
```
登録したkeyは*keys <key>*で取得することができる。
```bash
> keys *
1) "user"
2) "word"
```
以下のコマンドでredis-cliを終了する。
```bash
> exit
```

# リソースの削除
最後にリソースを削除しましょう。
## ElastiCache
|Resource|Name|
|---|---|
|ElastiCache for Redis|redis-handson-<今日の日付>|
|サブネットグループ|redis-handson-<今日の日付>|
|パラメータグループ|redis-handson-<今日の日付>|
|SG|redis-handson-<今日の日付>-redis|

## EC2
|Resource|Name|
|---|---|
|EC2|redis-handson-<今日の日付>|
|SG|redis-handson-<今日の日付>-ec2|

## Subnet
|Resource|Name|
|---|---|
|Subnet|redis-handson-<今日の日付>-pub|
|Subnet|redis-handson-<今日の日付>-prv|

# まとめ
今回はElastiCacheの構築から初歩的なredis-cliの操作までハンズオン形式でご紹介しました。

時間があるときに、プログラミングからの操作についても記事を書いてみたいと思います。

ご覧いただきありがとうございました。