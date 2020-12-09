
## はじめに

SSSD で LDAP ユーザの SSH アクセス制御をするにはどうすればいいのか検証しました。

ドキュメントによると、access_provider, ldap_access_order, ldap_access_filter を使用すればいいみたいなので、これらのパラメータを中心に触れていきます。

記事目安...10分

[:contents]

## 関連する各パラメータの概要

#### access_provider
Linux へのアクセス制御を行う際に使用されるプロバイダーを決定するパラメータです。  
パラメータが取れる値は、 *permit, deny, ipa, ad, ldap, simple* です。  
デフォルト値は、*permit* (=全て許可) です。

>access_provider (string)
>The access control provider used for the domain. There are two built-in access providers (in >addition to any included in installed backends) Internal special providers are:
>"permit" always allow access. It's the only permitted access provider for a local domain.
>
>"deny" always deny access.
>
>"ldap" for native LDAP authentication. See sssd-ldap(5) for more information on configuring LDAP.
>
>"ipa": FreeIPA and Red Hat Enterprise Identity Management provider. See sssd-ipa(5) for more >information on configuring FreeIPA.
>
>"ad": Active Directory provider. See sssd-ad(5) for more information on configuring Active >Directory.
>
>"simple" access control based on access or deny lists. See sssd-simple(5) for more information >on configuring the simple access module.
>
>Default: "permit"

引用: [sssd\.conf（5）：SSSDの設定ファイル\-Linuxのマニュアルページ](https://linux.die.net/man/5/sssd.conf)

#### ldap_access_order
*access_provider* が、ldap の時だけ機能するパラメータです。  
Linux へのアクセス制御を行う場合に、どのパラメータで細かいアクセス制御を行うか定義します。
パラメータが取れる値は *filter, expire,, authorized_service, host* です。  
デフォルト値は *filter* です。

>ldap_access_order (string)
>Comma separated list of access control options. Allowed values are:
>filter: use ldap_access_filter
>
>expire: use ldap_account_expire_policy
>
>authorized_service: use the authorizedService attribute to determine access
>
>host: use the host attribute to determine access
>
>Default: filter
>
>Please note that it is a configuration error if a value is used more than once.

引用: [sssd\-ldap\(5\): config file for SSSD \- Linux man page](https://linux.die.net/man/5/sssd-ldap)

#### ldap_access_filter
*access_provider=ldap かつ、 ldap_access_order=filter* の時だけ機能するパラメータです。  
Linux へのアクセス制御を行う際に、どの LDAP オブジェクトにアクセスを許可するのかというフィルタを定義します。  
デフォルトの値は空です。

※ *ldap_access_filter* では変数展開がサポートされていない点に注意ください
参考: [\[RFE\] ldap\_access\_filter with variable expansion · Issue \#3024 · SSSD/sssd](https://github.com/SSSD/sssd/issues/3024)

> ldap_access_filter (string)
> If using access_provider = ldap and ldap_access_order = filter (default), this option is > mandatory. It specifies an LDAP search filter criteria that must be met for the user to be > granted access on this host. If access_provider = ldap, ldap_access_order = filter and this > option is not set, it will result in all users being denied access. Use access_provider = permit > to change this default behavior.
> Example:
> 
> access_provider = ldap
> ldap_access_filter = memberOf=cn=allowedusers,ou=Groups,dc=example,dc=com
> 
> This example means that access to this host is restricted to members of the "allowedusers" group > in ldap.
> Offline caching for this feature is limited to determining whether the user's last online login > was granted access permission. If they were granted access during their last login, they will > continue to be granted access while offline and vice-versa.
> 
> Default: Empty

引用: [sssd\-ldap\(5\): config file for SSSD \- Linux man page](https://linux.die.net/man/5/sssd-ldap)

---

そのほかに、 *id_provider, auth_provider の値が ldap* になっていることも前提となります。

詳細については、[こちらのブログ](http://blog.serverworks.co.jp/restrict-ldap-user-by-sssd) を参照ください。

## *sssd.conf* の設定例

状況に応じた config の設定例を載せます。  

アクセス先サーバ(=sssd が稼働するサーバ)のホストネームは、 *ldap-client* と仮定します。

※ 一部パラメータは省略しているため、以下の設定だけでは *sssd.conf* を構成できません。

---

- 全 LDAP オブジェクトを許可する
```bash
id_provider = ldap
auth_provider = ldap
access_provider = permit
```
- host属性値が 「*\**」または、「ldap-client」の LDAP オブジェクトを許可する
```bash
id_provider = ldap
auth_provider = ldap
access_provider = ldap

ldap_access_order = host
```
- POSIX アカウントの LDAP オブジェクトを許可する
```bash
id_provider = ldap
auth_provider = ldap
access_provider = ldap

ldap_access_order = filter
ldap_access_filter = objectClass=posixAccount
```
- POSIX アカウントかつ、host属性値が 「*\**」または、「ldap-client」の LDAP オブジェクトを許可する
```bash
id_provider = ldap
auth_provider = ldap
access_provider = ldap

ldap_access_order = filter
ldap_access_filter = (&(objectClass=posixAccount)(|(host=ldap-client-1)(host=\*)))
```

## おわりに

今回は、 SSSD による LDAP ユーザのアクセス制御方法に着目しました。

個人的には、 **制御する自由度が高い ldap_access_filter の使用** がいいと思います。。

以上ありがとうございました。