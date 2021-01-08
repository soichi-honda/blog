## はじめに

SSSD パラメータ *ldap_user_search_base* について備忘録です。

記事目安...5分

[:contents]

## *ldap_user_search_base* とは

* LDAP サーバ へのユーザ問い合わせを行う際の、検索ベースを定義するパラメータです。  
この検索ベース条件に当てはまらないユーザは、LDAPクライアントから存在しないユーザとして扱われます。

* 値は、検索ベースDN, スコープ, フィルター条件を組み合わせて作成します(ldap_search_base と同じです)。

```
search_base[?scope?[filter][?search_base?scope?[filter]]*]
```

* 問い合わせ先が AD サーバでも機能しますが、フィルタ機能はサポートされません(shadowFlag 属性によるフィルタは効きました)


---

より正確な詳細は　*man* コマンドを確認してください。

```bash
$ man sssd-ldap
```

## 設定例

各項目を以下とした設定例を記載します。

|Key|Value|
|---|---|
|ドメイン名|dc=example, dc=com|

---

#### パターン1: ユーザ検索ベースDN を "ou=Users, dc=example, dc=com" にする
```bash
ldap_user_search_base = ou=Users, dc=example, dc=com
```

---

#### パターン2: ユーザ検索ベースDN を "ou=Users, dc=example, dc=com" にするかつ、shadowFlag属性値が「1」のユーザのみを検索対象とする
```bash
ldap_user_search_base = ou=Users, dc=example, dc=com?subtree?shadowFlag=1
```

## 確認

*id* コマンドでユーザを検索することで、検索ベースおよびフィルタが適切に設定されているか確認することができます。  
意図したとおりに設定していれば、ユーザ情報が返ってくるはずです。

キャッシュが設定されている場合は、削除してから実施してください！

---
```bash
$ sss_cache -u <ユーザ名> //キャッシュの削除
$ id <ユーザ名>
```

参考: [11\.2\.26\. SSSD キャッシュの管理 Red Hat Enterprise Linux 6 \| Red Hat Customer Portal](https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache)

## まとめ

ということで、ldap_user_search_base の使い方について触れました。  
ldap_user_search_base を有効に活用して、検索効率を上げてみてくださいね。


ご覧いただきありがとうございました。
