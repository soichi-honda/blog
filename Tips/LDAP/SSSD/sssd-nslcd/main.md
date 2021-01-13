## はじめに

備忘録のために、自分が確認している範囲で nslcd と sssd のパラメータの対照表を作ってみました。

サンプルコンフィグも載せています！

LDAPサーバへの接続が前提です。

記事目安...10分

[:contents]

## 対応表

#### バインドの基本設定
|Detail|nslcd|sssd|
|---|---|---|
|接続する ldap のURIの定義|URI|ldap_uri|
|検索ベースDNの定義|base|ldap_search_base|
|ユーザ検索ベースDNの定義(*1)|base passwd, filter passwd|ldap_user_search_base|
|ユーザパスワード検索ベースDNの定義|base shadow, filter shadow|-|
|グループ検索ベースDNの定義|base group, filter group|ldap_group_search_base|
|バインドDNのユーザ名定義|binddn|ldap_default_bind_dn|
|バインドDNのパスワード定義|bindpw|ldap_default_authtok|

*1. ユーザ検索ベースDN の詳しい設定方法は[こちらのブログ](https://blog.serverworks.co.jp/sssd-ldap_search_base)をご参考ください。

#### SSL/TLS設定
|Detail|nslcd|sssd|
|---|---|---|
|SSL/TLS の有効化|ssl|ldap_id_use_start_tls|
|ルート証明書ディレクトリの定義|TLS_CACERTDIR|ldap_tls_cacertdir|
|ルート証明書ファイルの定義|TLS_CACERT|ldap_tls_cacert|
|ルート証明書の検証レベルの定義|TLS_REQCERT|ldap_tls_reqcert|

SSL/TLS を有効にする詳しい設定方法は[こちらのブログ](https://blog.serverworks.co.jp/sssd-ldaps)をご参考ください。

#### キャッシュ設定

|Detail|nslcd|sssd|
|---|---|---|
|キャッシュの有効化|nscdにて対応|cache_credentials|

#### その他設定
|Detail|nslcd|sssd|
|---|---|---|
|LDAPに問い合わせないユーザ/グループの定義|nss_initgroups_ignoreusers|filter_users, filter_groups|
|LDAPユーザのアクセス制御(*2)|pam_authz_search|access_provider, ldap_access_filter|

*2. LDAPユーザのアクセス制御する詳しい方法は[こちらのブログ](https://blog.serverworks.co.jp/sssd-ldap-access-filter)をご参考ください。

## サンプルコンフィグ

各項目を以下にした時のコンフィグ例を載せておきます。

|Key|Value|
|---|---|
|ldapサーバのIPアドレス|10.0.0.x|
|ldapサーバのホストネーム|hogehoge-server|
|ドメインDN|dc=example, dc=com|
|ルート証明書ファイルパス|/etc/openldap/certs/hogehoge.crt|
|バインドDNユーザ|cn=hogehoge, dc=People, dc=example, dc=com|
|バインドDNユーザパスワード|fugafuga|

#### nslcd.conf
```bash
uid nslcd
gid nslcd

URI ldap://10.0.0.x/
base dc=example, dc=com
base passwd ou=People, dc=example, dc=com
filter passwd (shadowFlag=1)
base group ou=Group, dc=example, dc=com

ssl on
TLS_CACERT /etc/openldap/certs/hogehoge.crt
TLS_REQCERT never

pam_authz_search (&(objectClass=posixAccount)(|(host=hogehoge-server)(host=\*))

binddn cn=hogehoge, dc=People, dc=example, dc=com
bindpw fugafuga

nss_initgroups_ignoreusers root
```

#### sssd.conf
```bash
[sssd]
 
services = nss, pam
domains = default
config_file_version = 2
debug_level = 0
 
[domain/default]
 
id_provider = ldap
auth_provider = ldap
access_provider = ldap
 
ldap_uri = ldap://10.0.0.x/
ldap_search_base = dc=example, dc=com
ldap_user_search_base = ou=People, dc=example, dc=com?subtree?shadowFlag=1
ldap_group_search_base = ou=Group, dc=example, dc=com

ldap_id_use_start_tls = true
ldap_tls_cacert = /etc/openldap/certs/hogehoge.crt
ldap_tls_reqcert = never

ldap_access_order = filter
ldap_access_filter = (&(objectClass=posixAccount)(|(host=hogehoge-server)(host=\*))

ldap_default_bind_dn=cn=hogehoge, dc=People, dc=example, dc=com
ldap_default_authtok <ハッシュ化されたパスワード>

cache_credentials = false

[nss]
filter_users = root
filter_groups = root
 
[pam]
```

## まとめ

nslcd と sssd の対応表についてまとめました。

わかり次第、また追加したいと思います。

ご覧いただきありがとうございました。
