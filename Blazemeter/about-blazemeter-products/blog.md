BlazeMeter社の製品を使ったので備忘録です。

記事目安 -5分~10分

[:contents]

## イメージ図
製品同士の関係は下記のイメージです。
[f:id:swx-sugaya:20200819104715p:plain](assets/about-blazemeter-products_1.png)

## 各サービスについて
### BlazeMeter
テスト実行のプラットフォーム。

SaaSサービスゆえテストシナリオさえあれば、ブラウザからGUI操作で負荷試験を行える。  
Taurusで動作するYAML/JSONファイルを実行することも可能。

一定以上のスペックの場合、有料プランとなるので注意が必要。

[Try BlazeMeter for free now. Choose your plan later.](https://www.blazemeter.com/pricing/)

---

〇メリット

- SaaSのため導入が容易
- クラウドリソースにより、大規模な負荷テストが容易かつ低価格で実行できる
- 負荷テスト後は、自動でレポートを生成してくれる
- 様々なテストシナリオ作成ツール(JMeter, Selenium, pytestなど)と互換がある

参考: [BlazeMeter](https://www.blazemeter.com/)

### Taurus
テストシナリオのラッパーツールおよび、テスト実行プラットフォーム。

ローカルにインストールすることで、YAML/JSONファイルに沿った負荷シナリオを実行することができる。

---

〇メリット

- テストシナリオさえあれば、簡単に負荷シナリオを作成することができる。変更も柔軟に可能。  
- 様々なテストシナリオ作成ツール(JMeter, Selenium, pytestなど)と互換がある。

参考: [Taurus](https://gettaurus.org/)

### The BlazeMeter Chrome Extension
Chrome拡張機能で提供されるテストシナリオ作成ツール。

このツールを用いてGUIのブラウザ操作を録画すると、各操作がテキストベースで記録された様々なテストシナリオファイルと負荷シナリオファイルを作成してくれる。

---

〇メリット

- コードが書けない人でも、WebサイトのGUIテストシナリオを作成できる。

参考: [BlazeMeter | The Continuous Testing Platform](https://chrome.google.com/webstore/detail/blazemeter-the-continuous/mbopgmdnpcbohhpnfglgohlbhfongabi)