## はじめに
EC2上で動く踏み台サーバのバージョンアップを行う際に、ユーザ/グループファイルを編集することがあったので備忘録です。

記事目安 - 10分

[:contents]

## ゴール
既存サーバから、新規サーバに以下ファイル群を移行します。  

- /etc/passwd
- /etc/shadow
- /etc/group
- /etc/gshadow

## 用語の整理
#### /etc/passwd
ユーザを管理されているファイル。xは、各ユーザの暗号化されたパスワードの代わりに代入される値。

#### /etc/shadow
各ユーザの暗号化されたパスワードが書かれたファイル。OSやそのバージョンによって暗号化方法が変わるので、安易にコピペすると、エラーを起こすので注意。

#### /etc/group
ユーザに充てる権限グル―プを管理するファイル。こちらもxは、暗号化されたパスワードの代わりに代入される値。

#### /etc/gshadow
各グループの暗号化されたパスワードのハッシュが書かれたファイル。/etc/shadowと同じく慎重に触ってください。

## 作業手順
### /etc/passwdの移行
それぞれのサーバの "/etc/passwd" の中身をコピーし、差分をdiffツールかなにかでとります。  
取得した差分は、テキストファイルに保存します。

```bash
$ vi ~/diff.txt
```

---

差分を新規サーバの "/etc/passwd" へ "cat" コマンドで書き込んでいきます。

```bash
$ sudo su
# cat <diff.txtのファイルパス> >> /etc/passwd
# exit
$ sudo diff /etc/passwd /etc/passwd- (*1)
```

*1. "/etc/passwd-" について  
/etc/passwdのバックアップファイル。自動的に作成されます。

#### /etc/shadowの更新

"pwconv" コマンドを使用して、新規サーバの "/etc/shadow" を更新します。

```bash
$ sudo pwconv　(*2)
$ sudo diff /etc/shadow /etc/shadow-
```

*2. "pwconv"コマンド  
"/etc/passwd" の情報を元に、"/etc/shadow" の内容を書き換えてくれます。

#### 変更の確認

最後に、"pwck"コマンドで、パスワードファイルが正しい状態かチェックします。

```
$ sudo pwck (*3)
```

*3. "pwck"コマンド  
パスワードファイルが正しい状態かチェックするコマンド。  
重複しているユーザがいないか、ホームディレクトリがないユーザはいないかまで確認してくれます。  
"/etc/shadow" については、"/etc/passwd" 内に間違ったユーザがいない時しか削除プロンプトを出してくれないです。


## /etc/groupの移行
#### /etc/groupの置き換え
それぞれのサーバの "/etc/group" の中身をコピーし、差分をdiffツールかなにかでとります。  
取得した差分は、テキストファイルに保存します。

```bash
$ vi ~/group_diff.txt
```

---

差分を新規サーバの "/etc/group" へ "cat" コマンドで書き込んでいきます。

```bash
$ sudo su
# cat <group_diff.txtのファイルパス> >> /etc/group
# exit
$ sudo diff /etc/passwd /etc/group-
```

#### /etc/gshadowの更新

"grpconv"コマンドを使用して、新規サーバの "/etc/gshadow"を更新します。    
基本的に、"pwconv"コマンドの時と同じです。

```bash
$ sudo grpconv
$ sudo diff /etc/gshadow /etc/gshadow-
```

#### 変更の確認
最後に、"grpck"コマンドで、パスワードファイルが正しい状態かチェックします。  
ここも"pwck"コマンドの時とほぼ同じです。

```bash
$ sudo grpck (*1)
```

*1. "grpck"コマンド  
pwckとほぼ同じ。なぜかこっちは、"/etc/group" 内の不要ユーザを削除するプロンプトまで出してくれます。  
"/etc/group" をチェックした後に "/etc/gshadow" 内をチェックして、不要パスワードを削除するプロンプトを出してくれます。

## 最後に
Linuxのユーザ/グループファイルは奥が深い...

ご覧いただきありがとうございました。
