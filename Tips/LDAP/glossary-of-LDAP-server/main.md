## はじめに

この前 LDAP サーバを構築したので、アウトプットしようかなと思って書きました。

ただ、 LDAP サーバはなかなか中身が複雑で理解するまでに時間がかかります。

そこで、まずは構築せず、** *CentOS7* 系ディストリビューション でありがちな LDAP サーバの構成を解説してみようと思います。**

記事目安...10分

[:contents]

## 構成図

色々なネット記事を見ましたが、以下の構成を組んでいることが多かったです。  
LDAP でよく使うのは、LDAP ユーザによる *SSH* 接続だろうと勝手に推測して、補足しました。

[f:id:swx-sugaya:20201201150543p:plain]

役割ごとに細かくサーバを分けて書いてますが、実際は **LDAP Server と LDAP Manager が同じサーバであることが多いです。**


## 各サーバとインストールされるパッケージについて

### LDAP Server ~LDAP データの保存場所~

LDAP 本体ともいえる役割を持つサーバです。  
ツリー型 DB として、 **各 LDAP のエンティティ(*1) を保存しています。**

*1. エンティティについて  
参考: [https://docs\.oracle\.com/cd/E19253\-01/819\-0960/eypin/index\.html](https://docs.oracle.com/cd/E19253-01/819-0960/eypin/index.html)

---

#### openldap-servers
LDAP サーバとして起動するために必要なパッケージ。

インストールすると、*slapd* がプロセス起動できるようになり、クライアントからのアクセスを受け付けます。

### LDAP Manager ~LDAPを管理する~

LDAP を管理するサーバです。インストールされている *openldap* コマンドを使って、 **LDAP サーバに様々な操作を行うことができます。**

e.g.) 操作例

- *ldapadd* : 新しい LDAP エンティティを追加する
- *ldapmodify* : LDAP エンティティを修正する
- *ldapsearch* : 各種 LDAP エンティティを閲覧する

---

基本的には、LDAP サーバ にまとめてインストールすることが多いと思います。上記の構成図の使い方だとサーバがだいぶもったいないような...。

ただし、LDAP クライアント 側に入れることは非推奨です。 LDAP クライアント にログインしたユーザが、 LDAP の設定変更や エンティティの変更を行うリスクが高まります。

---

#### *openldap-client*
LDAP サーバと通信するためのクライアントパッケージ。

インストールすることで、 LDAP サーバを管理する *openldap* コマンドを使えるようになります。  
これが *nslcd* と混ざってよくわからんってなりました。

### LDAP Client ~LDAP サーバに問い合わせを行う~

**LDAP サーバに問い合わせを行う** サーバ群のことです。いわゆる各環境で動く一般サーバを指しています。  
LDAP サーバへの問い合わせは *nslcd* が受け付けて、各システムの代わりに通信をおこないます。

---

ポイントとしては、問い合わせを行う場合、 **コマンドによって問い合わせ元が変化します** (個人的にはここが一番混乱しました)。

- *ssh* コマンドの場合  
*ssh* コマンドを受け付けるのは、 *sshd* ですが、正しいユーザが認証する機構は *PAM* が行っています。
したがって PAM が *nslcd* に問い合わせを行います。
- *id, getent passwd* の場合  
*id* や *getent passwd* コマンドは、 *NSS* がコマンドを受け付けます。NSS の設定ファイルには、記述された各情報の問い合わせ先が記述されています。  
したがって *nslcd* に問い合わせを行います。

---

#### *nss-pam-ldapd*
*NSS* および、 *PAM* が LDAP と連携するために必要なモジュールライブラリを提供するパッケージ。

インストールすると、*nslcd* がプロセス起動できるようになります。名前がややこしいです。

#### *nscd*
LDAP への問い合わせ情報をキャッシュ機能を提供するパッケージです。  
これにより、 *nslcd* から LDAP サーバへの **ネットワークトラフィック量を減らすことができます。**

インストールすると、 *nscd* がプロセス起動できるようになり、 キャッシュ情報の問い合わせ先となります。 名前がややこしいです。

## 注意点

今後、Redhat では、 *openldap-server*, *nss-pam-ldapd* を利用することは **非推奨になるそうです。**

参考: [9\.2。 OpenLDAP Red Hat Enterprise Linux 7 \| RedHatカスタマーポータル](https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/7/html/system-level_authentication_guide/openldap)

参考: [5\.4\. 非推奨の機能 Red Hat Enterprise Linux 8 \| Red Hat Customer Portal](https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/8/html/8.0_release_notes/deprecated_functionality)

このあたりについてはまた別途まとめたいと思います。

## まとめ

ということで、 CentOS7系ディストリビューション において、一番メジャーと思われる LDAP 構成について解説しました。

EC2 上に構築するブログもいずれ書きたいなあと思います。

ご覧いただきありがとうございました。
