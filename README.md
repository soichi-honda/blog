# ブログ公開手順
- ブランチを切る  
blog/パーマリンクurl
- 記事を書く
- Github上で公開したいコンテンツのみPublicブランチへマージ
```
git checkout --patch <別ブランチ> <ファイル名>
```
- URL部分更新
- 記事公開後、masterにマージ
- 切ったブランチを消す
