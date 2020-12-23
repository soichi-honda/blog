## はじめに

sssd で ldaps 通信を行いたいときに、最低限注目すべきパラメータについてまとめました。

設定例も載せます！

記事目安...5分

[:contents]

## ldaps 通信に関するパラメータについて

|Param|Detail|
|---|---|
|ldap_id_use_start_tls|SSL/TLS 通信を行うか決定します|
|ldap_tls_cacert|SSL/TLS 通信開始前の検証の際に、使用するルートCA証明書ファイルを指定します(*1)|
|ldap_tls_cacertdir|検証で使用するルートCA証明書ファイルが格納されたディレクトリを指定したいときは、_ldap\_tls\_cacert_ の代わりにこちらを使用します。(*2)|
|ldap_tls_reqcert|証明書の検証レベルを決定します|

参考: [sssd\-ldap\(5\): config file for SSSD \- Linux man page](https://linux.die.net/man/5/sssd-ldap)

*1) SSL/TLS 通信開始前の証明書検証については、[こちらのブログ](https://blog.serverworks.co.jp/server-cert-verification)をご参考ください。

*2) SSSD が、ディレクトリに格納する証明書ファイルを参照出来るようハッシュリンクを作成する必要がございます。

> Typically the file names need to be the hash of the certificate followed by '.0'. If available, cacertdir_rehash can be used to create the correct names.

引用: [sssd\-ldap\(5\): config file for SSSD \- Linux man page](https://linux.die.net/man/5/sssd-ldap)

## 設定例

設定例を用意してみました。

|key|Value|
|---|---|
|ldapサーバのホスト名|hogehoge.com|
|ldapドメイン|dc=example, dc=com|
|ルートCA証明書|/etc/openldap/certs/hogehoge.crt|

#### パターン1: 証明書の検証を行うパターン

```
[domain/default]

id_provier = ldap
auth_provieder = ldap
access_provieder = permit

ldap_uri = ldap://hogehoge.com
ldap_search_base = dc=example, dc=com

ldap_id_use_start_tls = true
ldap_tls_cacert = /etc/openldap/certs/hogehoge.crt
ldap_tls_reqcert = demand

```

#### 【非推奨】パターン2: 証明書の検証を行わないパターン

```
[domain/default]

id_provier = ldap
auth_provieder = ldap
access_provieder = permit

ldap_uri = ldap://hogehoge.com
ldap_search_base = dc=example, dc=com

ldap_id_use_start_tls = true
ldap_tls_cacert = /etc/openldap/certs/hogehoge.crt
ldap_tls_reqcert = nerver
```

両パターンの違いは、 *ldap_tls_reqcert* の値だけです。

*3) id_provider, auth_provider, access_provider については [こちらのブログ](https://blog.serverworks.co.jp/sssd-ldap-access-filter)をご参考ください。

## ログの出力例

ldaps の通信が出来ていれば、slapd 側のログに以下が出力されます( *loglevel* は *256* に設定)。
```bash
Dec 23 04:09:23 my-ldap-server slapd[2898]: conn=1000 fd=13 TLS established tls_ssf=256 ssf=256
```

## 終わりに

ご覧いただきありがとうございました。
