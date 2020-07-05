今回は、BlazeMeter 社の Taurus を使って負荷テストをしてみたいと思います。

# ゴール

最終的な構成イメージは以下となります。

[assets/stress-test-demo-with-taurus_1.png]

そのために今回は大きく以下2つのことをやります。
- The BlazeMeter Chrome Extension を使用して、Chrome上でのGUI操作をテストシナリオとして作成する。
- Taurus を使って、Webサイトへの負荷テストを実施する。 

# 用語説明
BlazeMeter 社の各製品については[こちら]()の記事を参考にしてください。

- Selenium  
    ブラウザのオートメーションツール。Webサイトの動作テストなどに用いる。  
    Selenium WebDriver と呼ばれるAPIを介して各ブラウザドライバへHTTPリクエストを投げることで、ブラウザを操作できる。

- ChromeDriver  
    Chrome を操作するためのドライバ。これに向けてHTTPリクエストをすることで、Chrome の操作が可能となる。
    Selenium が Chrome を操るためにも必須。

# 作業手順
## 環境の準備
CloudFormationを使ってVPC環境を準備しましょう。
スタック名 *turus-handson-vpc-<YYYYMMDD>* で以下テンプレートを流してください。

[templates/cfn-template-vpc.yml]

流し方がわからない人はこちらの記事を参考にしていただけると幸いです。

[]()

## Web Serverの構築

続いて負荷対象のWeb Serverを用意します。
スタック名 *turus-handson-web-<YYYYMMDD>* で以下テンプレートを流してください。

[templates/cfn-template-web.yml]

これでWeb Serverができたので、アクセスしてみましょう。

ローカルPCの Chrome から、http://<PublicIP> へアクセスします。  
以下画像のページが出るはずです。

[assets/stress-test-demo-with-taurus_2.png]

下の手順に従ってページの遷移を確認してみてください。最初のIndexページに戻れれば、とりあえずOKです。
1. **Login** ボタンをクリック。
1. 以下参考にID/Passwordのフォームを埋めて、**Login** ボタンをクリック。
    |Key|Value|
    |---|---|
    |ID|admin|
    |Password|passwd|
1. ページ遷移後 **Logout** ボタンをクリック。

## テストシナリオの作成

続いてテストシナリオを作成します。

[こちら](https://chrome.google.com/webstore/detail/blazemeter-the-continuous/mbopgmdnpcbohhpnfglgohlbhfongabi)のURLにアクセスして The BlazeMeter Chrome Extension を入れてください。

Chrome タブで、Web ServerのIndexページを開いてください。

Chrome のメニューバーから、BlazeMeter のアイコンを押してください。

[assets/stress-test-demo-with-taurus_3.png]

ポップアップが表示されるので、プロジェクト名を <YYYYMMDD>_LOGIN_TEST に変更します。  
その後、赤い録画ボタンを押します。

[assets/stress-test-demo-with-taurus_4.png]

ポップアップが以下に切り替わったらブラウザを操作してきます。

[assets/stress-test-demo-with-taurus_5.png]

再度、以下手順を実行して操作を録画してください。
1. **Login** ボタンをクリック。
1. 以下参考にID/Passwordのテキストボックスを埋めて、**Login** ボタンをクリック。
    |Key|Value|
    |---|---|
    |ID|admin|
    |Password|passwd|
1. ページ遷移後 **Logout** ボタンをクリック。
1. Indexページに戻ったことを確認後、ポップアップの停止ボタンを押す。

再度、メニューバーからBlazeMeterを開き **Editの▼** > **Selenium** を押します。  
以下の画面にポップアップが変更したら、再生ボタンをクリックしましょう。先ほどの操作を自動で実行してくれます。

[assets/stress-test-demo-with-taurus_6.png]

動作が正常に行われていることを確認後 **Saveの▼** > **Selenium YAML**　を押して、ファイルをローカルにダウンロードします。

これで、Selenium のテストシナリオ作成が終了しました。  
僕が作ったYamlファイルを置いておくので、参考にしていただければ。
[templates/selenium.yaml]

## Taurus Serverの構築
### EC2インスタンスの構築
続いて、負荷をかける Turus Server を作成していきます。

スタック名 *turus-handson-turus-<YYYYMMDD>* で以下テンプレートを流してください。

[templates/cfn-template-turus.yml]

### Taurus環境の準備

<YYYYMMDD>-turus-handson-taurus にSSHログインします。

まずはpython3環境を準備します。
    ``` bash
    # yum install python3 -y
    $ python3 -m venv my_app/env
    $ source ~/my_app/env/bin/activate
    $ pip install pip --upgrade 
    ```
参考: [Amazon Linux 2 で Boto 3 ライブラリを使用して Python 3 仮想環境を作成する方法を教えてください。](https://aws.amazon.com/jp/premiumsupport/knowledge-center/ec2-linux-python3-boto3/)

以下順番に沿って、必要パッケージをインストールします。
1. Chromeをインストールします
    ```bash
    # curl https://intoli.com/install-google-chrome.sh | bash
    $ google-chrome --version
    Google Chrome 83.0.4103.61 //バージョンを控えておいてください。
    ```
1. ChromeDriverをインストールします。もし、一致するバージョンがない場合はなるべく近いバージョンのものをインストールすると動くはずです。
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

※捕捉: ヘッドレスモード
ChromeをブラウザUIなしにコマンドライン上で実行することを指します。

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

[assets/stress-test-demo-with-taurus_7.png]

※捕捉 実行ログ
 実行ログは Artifacts dir に格納されます。興味ある人は見てください。

### 負荷テストの実施
テストが無事成功したところで、最後に Web Serverに向けて実際の負荷を行いましょう。

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

※捕捉 CloudWatchメトリクスを見る  
以下手順を実行すると、Web ServerのCPUUtilization がどれだけ上昇しているかをみることができます。
1. インスタンス名: <YYYYMMDD>-turus-handson-web のインスタンスIDを控えてください。
1. CloudWatch コンソールに入ってください。
1. 左ペインのメトリクスを開き **EC2** > **インスタンス別メトリクス** を押します。
1. Web Server のインスタンスIDでフィルタリング後、メトリクス名 **CPUUtilization** を有効にします。

# リソースの削除
最後に今回作成したリソースを削除しましょう。

今回作成したリソースはすべてCloudFormationで作ったので、スタックを消すだけで大丈夫です。
|Resource|Name|
|---|---|
|CloudFormation Stack|turus-handson-turus-<YYYYMMDD>|
|CloudFormation Stack|turus-handson-web-<YYYYMMDD>|
|CloudFormation Stack|turus-handson-vpc-<YYYYMMDD>|

# まとめ
今回はBlazeMeter社の製品を使って、WebServerの負荷テストデモを行いました。

個人的に負荷テストは準備が大変そうだなあという印象がありましたが、Taurus のおかげで比較的容易に環境を整えることができて驚きました。  
同じテストシナリオを用いて、BlazeMeter から負荷テストを実施することもできるので試してみてください！

ご覧いただきありがとうございました。