今回は、BlazeMeter 社の Taurus を使って負荷テストをしてみたいと思います。

# やりたいこと
今回は大きく分けて以下2つをやります。
- The BlazeMeter Chrome Extension を使用して、Chrome上でのGUI操作をテストシナリオとして作成する。
- Taurus を使って、Webサイトへの負荷テストを実施する。 

最終的な構成イメージは以下となります。

[How_to_Taurus_1]

負荷対象のWebサイトは、ログイン→ログアウトするだけのシンプルな構成となっています。  
そのためセキュリティはがばがばですが、ご愛嬌ということで。

# 用語説明
BlazeMeter 社の各製品については[こちら]()の記事を参考にしてください。

- Selenium  
    ブラウザのオートメーションツール。Webサイトの動作テストなどに用いる。  
    Selenium WebDriver と呼ばれるAPIを介して各ブラウザドライバへHTTPリクエストを投げることで、ブラウザを操作できる。

- ChromeDriver  
    Chrome を操作するためのドライバ。これに向けてHTTPリクエストをすることで、Chrome の操作が可能となる。
    Selenium が Chrome を操るためにも必須。

# 作業手順

## Web Serverの構築
最初に、AWS 環境に負荷をかけるための Web Server を用意しましょう。
### EC2インスタンスの構築
今回は以下の要件を満たすEC2インスタンスを作成してください。
- Web Server
    |Key|Value|
    |---|---|
    |OS|Amazon Linux2|
    |Instance Type|t3.small|
    |Subnet|任意のPublicSubnet|
    |EIP|有効|
    |タグ|Name: <本日の年月日>-stress-web|

- SG
    |Key|Value|
    |---|---|
    |タグ|Name: sg-<本日の年月日>-stress-web|

    |Rule|Type|Protocol|port|Source/Destination|
    |---|---|---|---|---|
    |Inbound|SSH|TCP|22|<ローカルPCのIPアドレス>|
    |Inbound|HTTP|TCP|80|0.0.0.0/0|
    |Outbound|すべてのトラフィック|すべて|すべて|0.0.0.0/0|

### Webコンテンツの配置
<本日の年月日>-stress-web にSSH接続してください。
Web ServerなのでまずはApacheを入れましょう。
    ```bash
    # yum install httpd
    # systemctl enable httpd
    ```
以下ファイルを/var/www/html配下にダウンロードしてください。
    [index.html]
    [login.html]
    [mypage.html]

    ```bash
    $ cd /var/www/html
    # tree
    .
    ├── index.html
    ├── login.html
    └── mypage.html

    0 directories, 3 files
    # ls -al
    -rwxr--r-x 1 root     root      362 May 30 11:06 index.html
    -rwxr--r-x 1 root     root     1202 May 30 11:08 login.html
    -rwxr--r-x 1 root     root     417 May 30 11:02 mypage.html
    ```

ローカルPCの Chrome から、http:// <EIP> へアクセスします。  
以下画像のページが出るはずです。
    [How_to_Taurus_2]

下の手順に従ってページの遷移を確認してみてください。最初のHomeページに戻れれば、とりあえずOKです。
1. **Login** ボタンをクリック。
1. 以下参考にID/Passwordのテキストボックスを埋めて、**Login** ボタンをクリック。
    |Key|Value|
    |---|---|
    |ID|admin|
    |Password|password|
1. ページ遷移後 **Logout** ボタンをクリック。

## テストシナリオの作成
[こちら](https://chrome.google.com/webstore/detail/blazemeter-the-continuous/mbopgmdnpcbohhpnfglgohlbhfongabi)のURLにアクセスして The BlazeMeter Chrome Extension を入れてください。
Web Server にアクセスしている Chrome タブを開いてください。
Chrome のメニューバーから、BlazeMeter のアイコンを押してください。
[How_to_Taurus_3]
ポップアップが表示されるので、プロジェクト名を <本日の年月日>_LOGIN_TEST に変更します。  
その後、赤い録画ボタンを押します。
[How_to_Taurus_4]
ポップアップが以下に切り替わったらブラウザを操作してきます。
[How_to_Taurus_5]
以下の手順を実行して操作を録画してください。
1. **Login** ボタンをクリック。
1. 以下参考にID/Passwordのテキストボックスを埋めて、**Login** ボタンをクリック。
    |Key|Value|
    |---|---|
    |ID|admin|
    |Password|password|
1. ページ遷移後 **Logout** ボタンをクリック。
1. Homeページに戻ったことを確認後、ポップアップの停止ボタンを押す。
再度、メニューバーからBlazeMeterを開き **Editの▼** > **Selenium** を押します。
以下の画面にポップアップが変更したら、再生ボタンをクリックしましょう。先ほどの操作を自動で実行してくれます。
[How_to_Taurus_6]
動作が正常に行われていることを確認後 **Saveの▼** > **Selenium YAML**　を押して、ファイルをローカルにダウンロードします。これで、Selenium のテストシナリオ作成が終了しました。  
僕が作ったYamlファイルを置いておくので、参考にしてください。
[20200531_login_test--Selenium.yaml]

## Taurus Serverの構築
### EC2インスタンスの構築
AWS 環境に Taurus Server を用意しましょう。
今回は以下の要件を満たすインスタンスを作成してください。
- Taurus Server
    |Key|Value|
    |---|---|
    |OS|Amazon Linux2|
    |Instance Type|t3.small|
    |Subnet|インターネットへのOutbound通信が可能なサブネット|
    |タグ|Name: <本日の年月日>-stress-taurus|

- SG
    |Key|Value|
    |---|---|
    |タグ|Name: sg-<本日の年月日>-stress-taurus|

    |Rule|Type|Protocol|port|Source/Destination|
    |---|---|---|---|---|
    |Inbound|SSH|TCP|22|<ローカルPCのIPアドレス>|
    |Outbound|すべてのトラフィック|すべて|すべて|0.0.0.0/0|

### Taurus環境の準備
<本日の年月日>-stress-taurus にSSHログインします。
まずはpython3環境を準備します。
    ``` bash
    # yum install python3 -y
    $ python3 -m venv my_app/env
    $ source ~/my_app/env/bin/activate
    $ pip install pip --upgrade 
    ```
参考: [Amazon Linux 2 で Boto 3 ライブラリを使用して Python 3 仮想環境を作成する方法を教えてください。](https://aws.amazon.com/jp/premiumsupport/knowledge-center/ec2-linux-python3-boto3/)

以下の順番に沿って、必要パッケージをインストールします。
1. Chromeをインストールします
    ```bash
    # curl https://intoli.com/install-google-chrome.sh | bash
    $ google-chrome --version
    Google Chrome 83.0.4103.61 //バージョンを控えておいてください。
    ```
1. ChromeDriverをインストールします。もし、一致するバージョンがない場合はなるべく近いバージョンのものをインストールすると動きます。
    ```bash
    $ pip install chromedriver-binary==<Chromeのバージョン>
    ```
1. seleniumをインストールします
    ```bash
    $ pip install selenium
    ```
1. Taurusをインストールします
    ```bash
    # yum install python3-devel gcc
    $ pip install bzt
    ```

## 負荷試験デモ
### テストシナリオの実施
まずは、テストシナリオの動作を確認しましょう。
*/home/ec2-user/my_app/* にさきほど作成したテストシナリオを配置してください。
    ```bash
    $ pwd
    /home/ec2-user/my_app
    $ ls
    20200531_login_test--Selenium.yaml  env
    ```
テスト時Chromeをヘッドレスモードで起動するように、Yamlファイルを一部変更します。  
※ヘッドレスモードとは、ChromeをブラウザUIなしにコマンドライン上で実行することを指します。  
参考: [ヘッドレス Chrome ことはじめ](https://developers.google.com/web/updates/2017/04/headless-chrome?hl=ja)
    ```bash
    $ vi `date +%Y%m%d`_login_test--Selenium.yaml
    ---
        headless: false
    →    headless: true
    ---
    ```
Taurusで一回目の負荷テストを実施してみましょう。
    ```bash
    $ bzt <本日の年月日>_login_test--Selenium.yaml
    ```
    テストが成功すると画面に以下のようなメッセージが出力されます。  
    ※ 実行ログは Artifacts dir に格納されるので、興味ある人は見てください。
    [How_to_Taurus_7]

### 負荷テストの実施
テストが無事成功したところで、最後に Web Serverに向けて負荷を行いましょう。
まずは、テストシナリオが書かれたYamlファイルを変更します。  
※iterationsは、テストシナリオを何回実行するかという値です。

    ```bash
    vi `date +%Y%m%d`_login_test--Selenium.yaml
    ---
    iterations: 1
    →  iterations: 10 //好きな数字を入れてください
    ---
    ```
Taurusを再実行します
    ```bash
    bzt `date +%Y%m%d`_login_test--Selenium.yaml
    ```
せっかくなので以下手順を実行して、Web ServerのCPUUtilization がどれだけ上昇しているか確認してみてください。
1. Web Server のインスタンスIDを控えてください。
1. CloudWatch コンソールに入ってください。
1. 左ペインのメトリクスを開き **EC2** > **インスタンス別メトリクス** を押します。
1. Web Server のインスタンスIDでフィルタリング後、メトリクス名 **CPUUtilization** を有効にします。

# リソースの削除
最後に今回作成したリソースを削除しましょう。
|Resource|Name|
|---|---|
|EC2|<本日の年月日>-stress-web|
|EC2|<本日の年月日>-stress-taurus|
|SG|sg-<本日の年月日>-stress-web|
|SG|sg-<本日の年月日>-stress-taurus|

# まとめ
今回はBlazeMeter社の製品を使って、WebServerの負荷テストデモを行いました。  
個人的に負荷テストは準備が大変そうだなあという印象がありましたが、Taurus のおかげで比較的容易に環境を整えることができて驚きました。  
同じテストシナリオを用いて、BlazeMeter から負荷テストを実施することもできるので試してみてください！

ご覧いただきありがとうございました。