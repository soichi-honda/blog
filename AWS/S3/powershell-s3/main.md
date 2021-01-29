## はじめに

AWS Tools for Windows PowerShell で S3 に対する操作をしたので、備忘録です。

記事目安...5分

[:contents]

## サンプルコマンド

各値を以下とする、コマンド例を記述します。

|Key|Value|
|---|---|
|バケット名|hogehoge-bucket|
|オブジェクトパス|Sample/hogehoge.txt, Sample/fugafuga.txt|

### S3 のオブジェクト情報を取得する

```powershell
$ (Get-S3Object  -BucketName hogehoge-bucket -Prefix Sample).Key
```

### オブジェクトを S3 からローカルにダウンロードする

#### フォルダを対象とする場合

```powershell
$ Copy-S3Object -BucketName hogehoge-bucket -LocalFolder C:\download\ -KeyPrefix Sample
```

#### オブジェクトを対象とする場合

```powershell
$ foreach ($f in "hogehoge.txt", "fugafuga.txt") {
    Copy-S3Object -BucketName hogehoge-bucket -LocalFolder "C:\download\" -Key "Sample/$($f)"
}
```

### オブジェクトをローカルから S3 にアップロードする

```powershell
$ foreach ($f in "hogehoge.txt", "fugafuga.txt" ) {
    Write-S3Object -BucketName hogehoge-bucket -File "C:\upload\$($f)" -Key "Sample/$($f)"
}
```

## 参考

[AWS Tools for PowerShell - Amazon Simple Storage Service (S3)](https://docs.aws.amazon.com/powershell/latest/reference/)

## まとめ

S3 を Powershell 上で操作するコマンド例について触れました。

ご覧いただきありがとうございました。