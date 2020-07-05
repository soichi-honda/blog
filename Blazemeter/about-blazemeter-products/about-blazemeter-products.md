# はじめに
Blazemter社の製品を使ったので備忘録。

# イメージ図
[assets/about-blazemeter-products_1.png]

# 用語整理
## BlazeMeter
テスト実行のプラットフォーム。URLは[こちら](https://www.blazemeter.com/)  
テストシナリオさえあれば、ブラウザからGUI操作で負荷試験を行える。  
Taurusで動作するYaml/Jsonファイルを実行することも可能。

**メリット**
- SaaSのため導入が容易
- クラウドリソースを使った大規模な負荷テストが容易かつ低価格で実行できる
- 負荷テスト後は、自動でレポートを生成してくれる
- 様々なテストシナリオ作成ツール(Jmeter, selenium, pytestなど)と互換がある

## Taurus
テストシナリオのラッパーツール。URLは[こちら](https://gettaurus.org/)。  
ローカルにインストールすることで、Yaml/Jsonファイルに沿った負荷シナリオを実行することができる。  

**メリット**
- テストシナリオさえあれば、簡単に負荷シナリオを作成することができる。変更も柔軟に可能。  
- 様々なテストシナリオ作成ツール(Jmeter, selenium, pytestなど)と互換がある

## The BlazeMeter Chrome Extension
Chrome拡張機能で提供されるテストシナリオ作成ツール。URLは[こちら](https://chrome.google.com/webstore/detail/blazemeter-the-continuous/mbopgmdnpcbohhpnfglgohlbhfongabi)。  
このツールを用いてGUIのブラウザ操作を録画すると、各操作がテキストベースで記録された様々なテストシナリオファイルと負荷シナリオファイルを作成してくれる。

**メリット** 
- コードが書けない人でも、WebサイトのGUIテストシナリオを作成できる。