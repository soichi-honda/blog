## はじめに

AWS Microsoft AD (以下 AWS MMAD ) のスキーマを拡張する機会があったので備忘録です。

今回は、オブジェクトクラス hostObject クラスをスキーマに追加します。

記事目安...10分

[:contents]

## hostObject クラスとは

Ldapns.schema にて定義された補助型オブジェクトクラスです。

この objectClass は 以下属性を含みます。

* host

---

余談ですが AWS MMAD スキーマでは、*host* 属性がすでに存在します。

しかし、この属性を持つオブジェクトクラスが構造型の *account* クラスのみのため、
今回はこのオブジェクトクラスを新しく定義します。

## 今回のゴール
以下できることがゴールです

* hostObject クラスを AWS MMAD のスキーマに追加できる

## hostObject クラスをスキーマに追加する手順

### hostObject を追加する LDIF ファイルの作成
hostObject クラスを追加する LDIF ファイルは [こちら](https://github.com/sugaya0204/blog/blob/Public/AWS/DirectoryService/mmad-hostObject/add-hostObject-and-update-schema-cache.ldif)をご参考ください。

### LDIF ファイルを使った AWS MMAD のスキーマの拡張

スキーマを拡張するためには以下を実施します。

1. AWS マネコンの DirectoryService コンソールを開き、スキーマ拡張を行いたいディレクトを指定します。
1. [ メンテナンス ] を選択します。
1. スキーマ拡張ペインの [ アクション ] を開いた後、[ スキーマのアップロードと更新 ] を押します。
1. ポップアップが開いたら、先ほど作成したLDIFファイルをアップロードし、[ 説明 ] 欄に "add-hostObject-and-update-schema-cache" と入力します。入力に問題ないことを確認したら、[ スキーマ更新 ] を押します。  
※手動スナップショットを作成していない場合は作成されます。これは 30分 ~ 1h 程かかります。

### hostObject クラスの確認

1. AD 管理用サーバに、AD の管理者ユーザで RDP ログインしてください。
1. *Powershell* プログラムを開きます。
1. 以下コマンドを実行して *hostObject* クラスがあることを確認する(DCが "example.com" の場合)
```
$ get-adobject -Identity 'CN=hostObject,CN=Schema,CN=Configuration,DC=example,DC=com' -Properties *
```

---

ここまで確認出来たら、実際に User オブジェクトに追加出来るか確認してみてください！

## まとめ

* LDIFファイルを使用することで、AWS MMAD のスキーマを拡張できます
* 上記のスキーマ拡張方法により、新しい ObjectClass を追加できます

以上ご覧いただきありがとうございました

## 参考

* [チュートリアル: スキーマの拡張AWS Managed Microsoft AD \- AWS Directory Service](https://docs.aws.amazon.com/ja_jp/directoryservice/latest/admin-guide/ms_ad_tutorial_extend_schema.html)

* [How to Move More Custom Applications to the AWS Cloud with AWS Directory Service \| AWS Security Blog](https://aws.amazon.com/jp/blogs/security/how-to-add-more-application-support-to-your-microsoft-ad-directory-by-extending-the-schema/)
