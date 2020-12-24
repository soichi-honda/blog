## はじめに

slapd のログレベルを変更するのがだいぶ癖だったので、備忘録に残しておきます。

記事目安...5分

[:contents]

## 各ログレベルについて

man コマンド実行後、 *loglevel* でサーチすれば各ログレベルの詳細が見れます
```bash
$ man slapd.conf
```

## 変更手順

*root* ユーザで作業します。

```bash
$ sudo su
```

---

ホームディレクトリに、ログ変更用の ldif ファイルを作成します。

```bash
$ cd ~
$ vi change-loglevel.ldif
```
```bash
dn: cn=config
changetype: modify
replace: olcLogLevel
olcLogLevel: 256 //変更したいログレベルに変えてください。
```

---

作成した *ldif* ファイルを使用して、ログレベルの変更を行います。
```bash
$ ldapmodify -x -D cn=config -w <パスワード> -f change-loglevel.ldif
```

## 確認

以下コマンドで現在のログレベルを確認できます。

```bash
ldapsearch -Y EXTERNAL -H ldapi:// -b cn=config | grep olcLogLevel
```

## おわりに

ldapxxx系コマンドは何度やっても慣れませんね...。
