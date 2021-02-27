## はじめに

AWS Managed Microsoft AD (以下AWS MMAD) と通信するときに ldaps が使えるとのことだったので試してみました。
今回は最速での ldaps 通信出来る環境を目指します。

本手順を行うことで Windows, Linux を問わず、AWS MMAD ドメインコントローラーとの LDAPS 接続が可能となります。

記事目安...20分

[:contents]

## 前提条件

* AWS MMAD によるドメインコントローラーが構築済み
未構築の方は [こちらのブログ](https://blog.serverworks.co.jp/make-mmad-by-cfn) にある cfn テンプレートをお使いください。  
※作成に 20分ほどかかります
* 上記のドメインコントローラーを管理する Windows サーバが構築済み(以後 AD 管理サーバと呼びます。)  
詳しい構築方法は [こちらのAWSドキュメント](https://docs.aws.amazon.com/ja_jp/directoryservice/latest/admin-guide/microsoftadbasestep3.html#installadtools)をご参照ください

## 構成図

[f:id:swx-sugaya:20210226175342p:plain]


1. AWS MMAD ドメインコントローラーはエンタープライズ CA と通信して、エンタープライズ CA が発行した証明書を取得します。  
AWS MMAD ドメインコントローラーは、スタンドアロン CA および、サードパーティ CA の証明書をサポートしていないので、**エンタープライズ CA からの証明書発行を行うことが必須となります。**  
> AWS Managed Microsoft AD のサーバー側 LDAPS はスタンドアロン CA から発行される証明書をサポートしていません。また、サードパーティーの認証期間によって発行された証明書もサポートしていません。  
引用元: https://docs.aws.amazon.com/ja_jp/directoryservice/latest/admin-guide/ms_ad_ldap_server_side.html

2. アクセスしたいサーバ(今回は AD 管理サーバ) から ldp ツールを使用して、AWS MMAD ドメインコントローラーに LDAPS 接続を行います。  
このとき AWS MMAD ドメインコントローラーは、1. で取得した証明書をアクセス元サーバに提示します。  
AWS MMAD ドメインコントローラーにアタッチされた SG は、事前に LDAPSポート: 636 が開いているので、証明書を設置するだけで LDAPS による通信が可能です。

## ldaps 通信を有効化する手順

### エンタープライズ CA サーバのセットアップ


#### 1. エンタープライズ CA 用 Windows サーバ の構築

まず、エンタープライズ CA 用 Windows サーバを構築します。

**OS: Windows2019** のサーバを一台、パブリックサブネットに構築してください。  
[こちらのブログ](https://blog.serverworks.co.jp/cfn-template-windows2019-on-ec2) にある cloudformation テンプレートを流すと早いです。

#### 2. エンタープライズ CA 用 Windwos サーバのドメイン参加

先ほど構築したサーバに RDP ログインして、AD ドメインへ参加してください。  
細かい手順は調べると出てくるので、省略します!

#### 3. エンタープライズ CA のインストール

ここからエンタープライズ CA として動作するよう、機能を追加します。

まずは、 AD CS アプリケーションを以下の手順で追加します。

1. デスクトップから [ Server Manager ] を開きます。
1. ページが切り替わったのち、 [ Manage ] > [ Add Role and Features ] を選択します。
    1. "Before you begin" ページは、そのまま[ Next ] を押します。
    1. "Select installation" ページでは、"Role-based or feature-based installation" が選択されていることを確認し、そのまま[ Next ] を押します。
    1. "Select destination server" ページでは、ログイン中の PC が選択されていることを確認し、そのまま[ Next ] を押します。
    1. "Select server roles" ページでは、 "Active Directory Certificate Services" にチェックをいれます。新しいペインが開いたら、[ Add Feature ] を押します。元の画面に戻ったら[ Next ] を押します。
    1. "Select Features" ページでは、そのまま [ Next ] を押します。
    1. "AD CS" ページでは、そのまま [ Next ] を押します。
    1. "Select Role services" では、"Certification Authority" が選択されていることを確認し、 [ Next ] を押します。
    1. "Confirm installation selections" ページでは、問題がなければ [ Install ] を押します。
1. インストールが完了したら [ Close ] を押します

---

続いて、AD CS アプリケーションの設定を行って、**ルートかつ、エンタープライズ CA の認証局** をセットアップします。

1. [ Server Manager ] のダッシュボード画面の右上にある [ フラグマーク ] を押します。
1. [ Configure Active Directory Certificate Services on the destination server ] を選択します。
1. あたらしいページが開いたら、[ Change ] を押して、 AD 管理ユーザの認証情報をいれてください。その後  [ Next ] を押します。
    1. "Role Services" ページで "Certificate Authority" を選択します。その後  [ Next ] を押します。
    1. "Setup Type" ページで "Enterprise CA" を選択します。その後  [ Next ] を押します。
    1. "CA Type" ページで "Root CA" を選択します。その後  [ Next ] を押します。
    1. "Private Key" ページで、"Create a new private key" を選択します。その後  [ Next ] を押します。
    1. "Cryptography for CA" ページは、そのまま [ Next ] を押します。
    1. "CA Name" ページは、"Common name for this CA" に "root-CA" と入力して [ Next ] を押します。
    1. "Validity Period" ページは、5年のまま [ Next ] を押します。
    1. "CA Database" ページは、そのまま [ Next ] を押します。
1. 入力した値に誤りがないことを確認して、[ Configure ] を押します。セットアップが完了したら、 [ Close ] を押してページを閉じます。

#### 4. 証明書テンプレートの設置

エンタープライズ CA を構築したら、以下の手順で証明書テンプレートを作成します。

1. 再び [ Server Manager ] のダッシュボード画面に戻り、[ Tools ][ Certification Authority ] を押して、"certsrv" を開きます。 
1. [ root-CA ] を開き、[ Certificate Templates ] を右クリックして、 [ Manage ] を押します。
1. 一覧から [ Kerberos Authentification ] を右クリックし、 [ Dupulicate Template ] を押します。
1. 以下を行います。全て完了したら [ OK ] を押します。
    1. [ General ]  タブにて、"Template display name" を "LDAPSOverSSL" に変更します。
    "Publish ceritificate in Active Directory" にチェックを入れます。
    1. [ Compatibility ] タブにて、 "Certification Authority" を "Windows Server 2016" にします。
    "Ceritification recipient" を "Windows Server 2012 R2" に変更します。
    1. [ Security ] タブにて、[ Domain Controllers ] の権限を Read, Enroll, Autoenroll にします。
1. コンソールを閉じて、先ほどの "certsrv" に戻り、再び [ Certificate Templates ] を右クリックして、 [ New ] > [ Certificate Template to issue ]を押します。
1. 先ほどの作成した証明書テンプレート "LDAPSOverSSL" を選択して [ OK ] を押します。
※ "LDAPSOverSSL" が一覧に出るまで、ラグがあります。

---

ここまででエンタープライズ CA サーバのセットアップは完了となります。

### AWS MMAD ドメインコントローラーとエンタープライズ CA 間の通信許可

最後に AWS MMAD ドメインコントローラーが証明書を取得できるよう、エンタープライズ CA への通信許可を行います。

#### AWS MMAD ドメインコントローラーの SG 編集
1. LDAPS 通信を許可したい AWS MMAD ドメインコントローラの SG を選択します。  
※ SG 名は **<ディレクトリID名>_controllers** で生成されます。
1. [ インバウンドルール ] タブを開いて、ポート *636* が許可されていることを確認します。
1. [ アウトバウンドルール ] タブを開いて、以下ルールを追加します

|Type|Protocol|Port|dst|
|---|---|---|---|
|全てのトラフィック|全て|全て|<エンタープライズ CA の SG ID>|

#### エンタープライズ CA の SG 編集
1. 構築したエンタープライズ CA の SG を選択します。
1. [ インバウンドルール ] タブを開いて、以下ルールを追加します。

|Type|Protocol|Port|dst|
|---|---|---|---|
|全てのトラフィック|全て|全て|<AWS MMAD ドメインコントローラの SG ID>|

---

これで LDAPS 通信のための準備は完了です。

AD が エンタープライズ CA に証明書を自動取得するまで、最大で30分ほどかかるので気長に待ちましょう。  
※僕が試したときは 10 分くらいかかりました

### AWS MMAD との ldaps 通信の確認

最後に LDAPS 通信が出来ているか、 AD 管理サーバから LDAPS 接続して確認します。

#### AD 管理サーバからの疎通確認

AD 管理サーバに RDP ログインして、ldp ツール実行しましょう。

1. デスクトップで [ ldp ] で検索して、アプリケーションを開始します。
1. [ Connect ] を押して、
    1. "Server" に "ADドメイン名"
    1. Portに "636"
    1. SSL にチェックを付けて、[ OK ] を押します。
1. 接続できると証明書情報が返ってくるはずです!

## まとめ

証明書を設置すれば AWS MMAD で ldaps 通信できることがわかりました。

以上ご覧いただきありがとうございました。

## 参考
* [How to Enable Server\-Side LDAPS for Your AWS Microsoft AD Directory \| AWS Security Blog](https://aws.amazon.com/jp/blogs/security/how-to-enable-ldaps-for-your-aws-microsoft-ad-directory/)
