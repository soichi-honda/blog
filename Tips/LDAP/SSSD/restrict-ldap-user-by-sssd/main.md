## はじめに

SSSD で LDAP ユーザのアクセス制御をしたいときに、 *id_provider, auth_provider, access_provider* の違いに混乱して結局どの設定が大事なんだよ!!ってなったので検証してみました。

時間ない人は、考察と結論だけ読んでいただければ大丈夫です!

記事目安...15分

[:contents]

## 前提条件

- SSSD の接続先は OpenLDAP Server とします。
- 確認に使うユーザ名は *ldap-user* とします。
- *sssd.conf* の中身は以下とします。
```
[sssd]

services = nss, pam
domains = default
config_file_version = 2
debug_level = 0

[domain/default]

id_provider = ldap
auth_provider = none or ldap
access_provider = deny or permit

ldap_search_base = dc=example, dc=com
ldap_uri = ldaps://xxx.xxx.xxx.xxx/

cache_credentials = True

[nss]　

[pam]

```

## 調査方法について

*id_provider, auth_provider, access_provider* それぞれの値を変動させて、どのコマンドが実行できるか検証します。

---

実行するコマンド

- ID
ldap-user の ID 情報を取得します。
```bash
ec2-user$ id ldap-user
```
- GETENT PASSWD
ldap-user のパスワード情報を取得します。
```bash
ec2-user$ getent passwd ldap-user
```
- SU
*ec2-user* から *ldap-user* にユーザ切り替えを行います。
```bash
ec2-user$ su ldap-user
```
- SUDO SU(LDAPユーザ)
*ec2-user* から *ldap-user* に **パスワード入力無し** で、ユーザ切り替えを行います。
```bash
ec2-user$ sudo su ldap-user
```
- SUDO SU(ROOTユーザ)
*ldap-user* から *root* に、ユーザ切り替えを行います。
```bash
ldap-user$ sudo su
```

- SSH
*ssh-client* ホスト の ec2-user から、 *ldap-user* で *ldap-client* ホストにSSH接続します。
```bash
ec2-user@ssh-client$ ssh ldap-user@ldap-client
```


## 結果

- *id_provider* 未定義(*3)

|auth_provider||access_provider|ID|GETENT PASSWD|SU|SUDO SU(LDAPユーザ)|SUDO SU(ROOTユーザ)|SSH|
|---|---|---|---|---|---|---|---|---|
|none|かつ|deny|×|×|×|×|-|×|
|none|かつ|permit|×|×|×|×|-|×|
|ldap|かつ|deny|×|×|×|×|-|×|
|ldap|かつ|permit|×|×|×|×|-|×|

*1. テーブル見出しの各項目の詳細は、 調査方法を参照してください。

*2. *-* はユーザ切り替えができず、実行出来ていないことを示しています。

- *id_provider=ldap*

|auth_provider||access_provider|ID|GETENT Passwd|SU|SUDO SU swx-sugaya|SUDO SU|SSH|
|---|---|---|---|---|---|---|---|---|
|none|かつ|deny|〇|〇|×|〇|×|×|
|none|かつ|permit|〇|〇|×|〇|×|×|
|ldap|かつ|deny|〇|〇|×|〇|×|×|
|ldap|かつ|permit|〇|〇|〇|〇|〇|〇|

\*2. *id_provider* を無効化する場合は、*sssd.config* で未定義にする必要があります。
参考: [sssd\.conf\(5\): config file for SSSD \- Linux man page](https://linux.die.net/man/5/sssd.conf)

## 考察

- *id_provider* が定義されていない場合、 LDAP ユーザは解決できなくなる。
- *auth_provider* が *none* の場合、LDAP ユーザによる認証ができないため、結果として *access_provider* の設定の意味がなくなる。
- *auth_provider=noneかつ、access_provider＝ldap* と*auth_provider=ldapかつ、access_provider＝deny* は SSH 接続時のエラー文に違いがあったことから、認証段階で拒否されるか認証突破後アクセス段階で拒否されるかの違いがあると考察できる。
    - *auth_provider=noneかつ、access_provider＝ldap* → Permission denied, please try again.
    - *auth_provider=ldapかつ、access_provider＝deny* → Authentication failed.

## 結論

ということで以上の結果から、もし LDAP ユーザによるアクセス制御をしなければいけない場合は、

**id_provider, auth_provider, access_provider 全てを ldap に向けなければいけない**

ことがわかりました。

auth_provider, access_provider はデフォルト値がそれぞれ設定されているので、設定時注意してください。

参考: [sssd\.conf\(5\): config file for SSSD \- Linux man page](https://linux.die.net/man/5/sssd.conf)

ご覧いただきありがとうございました。
