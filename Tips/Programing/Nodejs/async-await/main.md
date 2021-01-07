## はじめに

Nodejs の async/await について、自分なりに整理してまとめてみました。

本記事と対照に書いた Promise.prototype.then()  に関する [こちら](https://blog.serverworks.co.jp/promise-then) の記事も見ていただけると理解しやすいと思います。

具体例を交えて解説するので、参考にしてみてください！

記事目安...10分

[:contents]

## async/await とは

### 用語整理
#### async

宣言することで、関数を非同期関数にします。

async で宣言された関数は、*Promise* オブジェクト同様、仮の値を返すようになります。

使用することのメリットは、 *Promise* オブジェクトを使うよりもコードの可読性を向上できる点です。

#### await

宣言することで、非同期関数の処理結果(*return* メソッドで返される値)を取得出来ます。

*await* は *async* が宣言された関数内でしか使用できません。

### Promise と async/await の対応表

それぞれの用法を対応表でまとめてみました。

|Role|Promise|async/await|
|---|---|---|
|関数を非同期にする|Promise()|async|
|非同期関数の成功時の結果を返す|resolve|return|
|非同期関数のエラー時の結果を返す|reject|throw|
|非同期関数の処理結果を取得する|Promise.prototype.then() |await|

---

では、サンプルコードを交えて解説していきます。

## 具体例を用いた async/await の解説

今回は、「1st, 2nd, 3rd」を順番にコンソールに表示するようコードを作成します。

〇 期待する結果

```bash
1st
2nd
3rd
```

---

### パターン1: async/await を使用しない場合
#### サンプルコード
```javascript
function myAsync() {
    return "2nd"
}

function main() {
    console.log("1st");
    const second = myAsync()
    console.log(second)
    console.log("3rd")
}

main()
```
#### 出力結果
```bash
1st
2nd
3rd
```

#### 解説
当然ですが、期待通りの結果となりました。

上から下に素直にコードが流れていくので、**myAsync() の処理結果である 「2nd」 が `second` 変数に期待通りに格納されています**。

また、ポイントとして、*main()* および、 *myAsync()* が **同期処理関数** です。



### パターン2: async のみを使用した場合

#### サンプルコード
```js
async function myAsync() {
    return "2nd"
}

function main() {
    console.log("1st");
    const second = myAsync()
    console.log(second)
    console.log("3rd")
    
}

main()
```

#### 出力結果
```bash
1st
Promise { '2nd' }
3rd
```

#### 解説

コンソールへの出力が期待通りとなりませんでした。  
「2nd」が出てほしいところに、「Promise { '2nd' }」が返っています。

これは、 **非同期関数 myAsync() が最初に返した仮の値 「Promise { '2nd' }」が、 `second` 変数に格納されてしまったため** です。

このことからも分かるように、*async* がついたことで、 *myAsync()* が **非同期関数**　に変化しています。  
*main()* は、パターン1同様、同期処理関数です。


### パターン3: async/await を使用した場合

#### サンプルコード
```javascript
async function myAsync() {
    return "2nd"
}

async function main() {
    console.log("1st");
    const second = await myAsync()
    console.log(second)
    console.log("3rd")
}

main()
```

#### 出力結果
```bash
1st
2nd
3rd
```

#### 解説

*async/await* を両方使用すると、コンソールへの出力が期待通りとなりました。

```javascript
    const second = await myAsync()
```

これは上記の部分で、 *await* が、即座に myAsync() から返ってくる 仮の値 「Promise { '2nd' }」ではなく、
**myAsync() の実行結果である 「2nd」 を `second` 変数に格納してくれたため** です。

また、ポイントとして、*main()* および、 *myAsync()* が **非同期処理関数** です。(*1)

---

*1 main() の非同期関数化について

最初に申し上げた通り、 *await* は *async* を宣言した関数内でしか使用できないため、

```javascript
async function main() {
```

上記のように、*main()* を無理やり *async* を使って非同期処理関数にしています。  
そうゆう仕様なのでしょうがないですが、別に *async* を宣言しなくても *await* を使えるようにすればいいのにと思いました。

この仕様について、理由がわかる人いたらコメントいただけると幸いです。

## まとめ

ということで、若干解決していない部分もありますが、 *async/await* を使った非同期処理についておおむね理解していただけたのではないでしょうか。

Promise よりも簡潔かつ、わかりやすくコードを書けることも一目瞭然だと思います。  
個人的に *return* で値を返せるのがわかりやすくていいなと思います。

以上ご覧いただきありがとうございました。