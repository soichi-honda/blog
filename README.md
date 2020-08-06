# ブログ公開手順
- ブランチを切る  
blog/パーマリンクurl
- 記事を書く
- Github上で公開したいコンテンツのみPublicブランチへマージ
```
git format-patch --histogram '<別ブランチ>' -- <ファイル名>
git am -3 *.patch
```
参考:https://qiita.com/locona_0810/items/4cecab00befc8bf608a4
- URL部分更新
- 記事公開後、masterにマージ
- 切ったブランチを消す

# MarkDown to Wordress

1. Copy as HTML

1. 以下の点を Ctrl + F で変更
|HTML|Markdown|
|---|---|
||>|
||<|
||"|

1. コードブロックの改行を削除

1. Wordpressにて画像の挿入