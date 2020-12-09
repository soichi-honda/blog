## はじめに

SSSD で LDAP ユーザの SSH アクセス制御をしたいときに、 *id_provider, auth_provider, access_provider* の違いに混乱して、結局どの設定が大事なんだよ!!ってなったので検証してみました。

ついでに、ほかのコマンドについてもここら辺のパラメータで制御できるかもと思い検証してます。

時間ない人は、 **考察と結論だけ読んでいただければ大丈夫です!**

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

id_provider = ldap or 未定義(*1)
auth_provider = none or ldap
access_provider = deny or permit

ldap_search_base = dc=example, dc=com
ldap_uri = ldaps://xxx.xxx.xxx.xxx/

cache_credentials = False

[nss]　

[pam]

```

\*1. *id_provider* を無効化する場合は、*sssd.config* で未定義にする必要があります。  
参考: [sssd\.conf\(5\): config file for SSSD \- Linux man page](https://linux.die.net/man/5/sssd.conf)


## 調査方法について

*id_provider, auth_provider, access_provider* それぞれの値を変動させて、どのコマンドが実行できるか検証します。

---

〇実行するコマンドと対応するテーブル項目について

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

「〇」 - コマンドが成功して出力が返ってきた  
「×」 - エラーになった or 出力に何も返ってこなかった。
「-」- 実行できなかったため、不明

### *id_provider* が未定義 の場合

|auth_provider||access_provider|ID|GETENT PASSWD|SU|SUDO SU(LDAPユーザ)|SUDO SU(ROOTユーザ)|★SSH★|
|---|---|---|---|---|---|---|---|---|
|none|かつ|deny|×|×|×|×|-|×|
|none|かつ|permit|×|×|×|×|-|×|
|ldap|かつ|deny|×|×|×|×|-|×|
|ldap|かつ|permit|×|×|×|×|-|×|

*2. テーブル見出しの各項目の詳細は、 「調査方法」の項目を参照してください。

### *id_provider=ldap* の場合

|auth_provider||access_provider|ID|GETENT PASSWD|SU|SUDO SU(LDAPユーザ)|SUDO SU(ROOTユーザ)|★SSH★|
|---|---|---|---|---|---|---|---|---|
|none|かつ|deny|〇|〇|×|〇|×|×|
|none|かつ|permit|〇|〇|×|〇|×|×|
|ldap|かつ|deny|〇|〇|×|〇|×|×|
|ldap|かつ|permit|〇|〇|〇|〇|〇|〇|


## 考察

- *id_provider* が定義されていない場合、 **LDAP ユーザは解決できなくなる** 。
- *auth_provider* が *none* の場合、LDAP ユーザによる認証ができないため、 **結果として *access_provider* の設定値が意味なくなる** 。
- *auth_provider=noneかつ、access_provider＝ldap* と、*auth_provider=ldapかつ、access_provider＝deny* は SSH 接続時のエラー文に違いがあったことから、 **認証する前の段階で拒否されるか、認証段階で拒否されるか** の違いがあると考察できる。
    - *auth_provider=noneかつ、access_provider＝ldap* → Permission denied, please try again.
    - *auth_provider=ldapかつ、access_provider＝deny* → Authentication failed.
- *id_provider=ldapかつ、auth_provider=ldapかつ、access_provider=permit* の場合、 **全てのコマンドが実行できた** 。

## 結論

ということで以上の結果から、もし LDAP ユーザによるアクセス制御をしなければいけない場合は、

**id_provider, auth_providerを ldap に向けなければいけないかつ、 access_provider で LDAP ユーザのアクセスを許可しなければいけない**

ことがわかりました。

*sssd.conf** にするとこんな感じです。

```
id_provider = ldap
auth_provider = ldap
access_provider = permit or ldap　(*4)
```

*4. 値を ldap にする場合は、filter 条件を定義する必要がございます。

---

なお、 *auth_provider, access_provider* はデフォルト値がそれぞれ設定されているので、設定時注意してください。

参考: [sssd\.conf\(5\): config file for SSSD \- Linux man page](https://linux.die.net/man/5/sssd.conf)

---

色々とコマンドを打ったので、結果的に 各パラメータの理解も深まった気がします。

ご覧いただきありがとうございました。
