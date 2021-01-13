## はじめに

AWS Microsoft AD (以下AWS MMAD) と通信するときに ldaps が使える！とのことだったので、試してみました。
今回は、最速で ldaps を作れる手順で構築をします。

記事目安...15分

[:contents]

## 今回のゴール
* Windows サーバから ldaps で通信できる
* Linux サーバから ldaps で通信できる

## ldaps 通信を有効化する手順
### AD 用の証明書の設置
#### ルート認証局の構築
```powershell
& notepad.exe c:\Windows\CAPolicy.inf
```
```

```
#### ルート証明書の設置
#### 証明書テンプレートの作成
#### AD とルート認証局の通信の有効化
### AWS MMAD との ldaps 通信の確認
#### windows サーバからの疎通確認
#### Linux サーバからの疎通確認

## まとめ

証明書を設置すれば AWS MMAD で ldaps 通信できることがわかりました。

以上ご覧いただきありがとうございました。

## 参考
* [How to Enable Server\-Side LDAPS for Your AWS Microsoft AD Directory \| AWS Security Blog](https://aws.amazon.com/jp/blogs/security/how-to-enable-ldaps-for-your-aws-microsoft-ad-directory/)