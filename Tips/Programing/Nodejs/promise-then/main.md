## はじめに

*Promise.prototype.then()* メソッドの使い方がわからなかったので、自分なりにまとめてみました。

具体例を交えて解説するので、参考にしてみてください！

記事目安...10分

[:contents]

## *Promise.prototype.then()* メソッドとは

Promise オブジェクトに渡されたコールバック関数の処理結果を取得するインスタンスメソッドです。

もう少し細かく言うと、 Promise オブジェクトは実行時に一旦、仮の値を返します。  
これは非同期関数が何かしらの値を返さないと、次の処理に進めないためです。  
しかし、 *Promise.prototype.then()* メソッドを使用すると、 **Promise に渡されたコールバック関数の処理結果を受け取ることができます**。

メリットは以下です。

1. 非同期処理の終了を待ってから後続の処理をつなげられる。
1. コールバック地獄を回避し、 可読性を向上させる。(今回は触れません)

---

では、サンプルコードを交えて解説していきます。

## 具体例を用いた *Promise.prototype.then()* の解説
### パターン1: *Promise.prototype.then()* メソッドを使用しない場合

今回は、「1st, 2nd, 3rd」を順番にコンソールに表示するようコードを作成します。  

〇 期待する結果

```bash
1st
2nd
3rd
```

#### サンプルコード
```javascript
function myPromise() {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            resolve("2nd")
        }, 3000)
    })
}

function main() {
    console.log("1st");
    const second = myPromise()
    console.log(second)
    console.log("3rd")
}

main()
```

#### 出力結果
```
1st
Promise { <pending> }
3rd
```

#### 解説
*Promise.prototype.then()* メソッドを使用しない場合、コンソールへの出力が期待通りとなりませんでした。  
「2nd」が出てほしいところに、「Promise { <pending\> }」が返っています。

これは、**非同期関数 *myPromise()* が最初に返した仮の値 「Promise { <pending\> }」が、 `second` 変数に格納されてしまったため** です。

### パターン2: *Promise.prototype.then()* メソッドを使用する場合

先ほどと同じ処理を *Promise.prototype.then()* メソッドを用いて書き直します。

---

#### サンプルコード
```javascript
function myPromise() {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            resolve("2nd")
        }, 3000)
    })
}

function main() {
    console.log("1st");
    myPromise().then(
        function(second) {
            console.log(second)
            console.log("3rd")
        }
        )
}

main()

```

#### 出力結果
```
1st
2nd
3rd
```

#### 解説
*Promise.prototype.then()* メソッドを使用すると、コンソールへの出力が期待通りとなりました。

```javascript
    myPromise().then(
        function(second) {
            console.log(second)
```

これは上記の部分で、myPromise().then() メソッドが、即座に *myPromise()* から返ってくる 仮の値 「Promise { <pending\> }」ではなく、  
**myPromise() の実行結果である 「2nd」 を `second` 変数に格納してくれたため** です！


## まとめ

以上のサンプルから *Promise.prototype.then()* メソッドを使用することで、**非同期処理の結果を取得して、後続の処理につなげられる** ことがわかりました。

本記事と対照に *async/await* についても書いているので、[こちら](https://blog.serverworks.co.jp/async-await) も確認いただけると幸いです。

ご覧いただきありがとうございました。
