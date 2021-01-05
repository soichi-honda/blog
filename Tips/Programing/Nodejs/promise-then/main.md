## はじめに

Promise.then メソッドの使い方がわからなかったので、自分なりにまとめてみました。

具体例を交えて解説するので、参考にしてみてください！

記事目安...10分

[:contents]

## Promise.then メソッドとは

* 非同期処理が含まれる特定の処理の実行終了を待ってから、次の処理を実行したい場合に使用するメソッド
* コールバック地獄を回避し、コードの可読性を向上できる

## パターン1: Promise.then メソッドを使用しない

ここから具体的なコードを踏まえて、解説します。

今回は、「1, 2, 3」を順番に表示するようコードを作成します。  

〇 サンプルコードの処理の流れ

1. コンソールに、「1」を表示する
1. 非同期関数 *setTimeout* を実行する(=非同期処理開始)
1. 3秒後に、コンソールに、「2」を表示する(=非同期処理終了)
1. コンソールに、「3」を表示する

#### サンプルコード
```javascript
function myPromise() {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            resolve(console.log(2))
        }, 3000)
    })
}

function main() {
    console.log(1);
    myPromise()
    console.log(3)
}

main()
```

#### 出力結果
```
1
3
2
```

Promise.then メソッドを使用しない場合、コンソールへの出力が **期待通りとなりません。**

3秒後にコンソールに「2」を表示する処理が終了する前に、コンソールに「3」を表示する処理が実行されてしまうためです。

## パターン2: *Promise.then* メソッドを使用する

先ほどと同じ処理を *Promise.then* を用いて書き直します。

---

#### サンプルコード
```javascript
function myPromise() {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            resolve(console.log(2))
        }, 3000)
    })
}

function main() {
    console.log(1);
    myPromise().then(function() {console.log(3)})
}

main()

```

#### 出力結果
```
1
2
3
```

*Promise.then* メソッドを使用すると、コンソールへの出力が **期待通りとなりました。**

```js
    myPromise().then(function() {console.log(3)})
```

上記の部分で *myPromise()* の実行が完了した後、*.then* の中身を実行するよう制御できたためです。


## まとめ

Promise.then メソッドを使用することで、 **非同期処理の終了を待ってから後続の処理をつなげられる** ことがわかりました。

ご覧いただきありがとうございました。
