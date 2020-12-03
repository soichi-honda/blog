記事目安: 5分

[:contents]

## 結論

Outputs セクション の Value 属性 は、どうやら String 型しか受け付けないらしいので、 **List 型を無理やり String 型** にしてあげましょう。

ちなみに、String 型以外を入れるとこんなエラーがでます。

```
Template format error: The Value field of every Outputs member must evaluate to a String.
```

## やり方

List 型の出力を *Join* 関数で結合して、無理やり String 型にします。  
今回は区切り文字を 「,」にして結合しました。

〇変更前
```yaml
Outputs:
  MyMicrosoftAdDnsIpAddress:
    Description: IP address of Microsoft AD DNS server
    Value: !GetAtt MyMicrosoftAd.DnsIpAddresses # e.g. [ "192.0.2.○○○", "192.0.2.xxx" ]　← List 型
```

〇変更後
```yaml
Outputs:
  MyMicrosoftAdDnsIpAddress:
    Description: IP address of Microsoft AD DNS server
    Value: !Join # e.g. 192.0.2.○○○,192.0.2.xxx ← String 型
      - ','
      - !GetAtt MyMicrosoftAd.DnsIpAddresses
```

## 参考
* [Outputs \- AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html)
* [Fn::Join \- AWS CloudFormation](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-join.html)


