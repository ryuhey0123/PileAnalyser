# Pile Analyser

杭の多層地盤解析を行うWebアプリです。地盤は非線形、線形、共に対応しています。
herokuにデプロイしていますが、非常に遅いのでローカルで実行することをお勧めします。

![](./assets/screenshot.png)


## Usage

### 解析方法の設定

![](./assets/screenshot2.png)

- Analysis mode

地盤の非線形性を考慮するかどうかを設定します。

- Reduction mode

地盤の非線形性を考慮する場合のみ有効。変位による地盤の水平反力係数低減を、各レベルごとに行うか、杭頭変位を一律で適用するかの差になります。

- Pile top condition

杭頭固定度。固定かピンか選びます。反剛接合は未実装。

- Material

杭体の材料です。スチールにするということは鋼管杭だと思いますが、板厚入力未実装なので無垢材になってしまいいます。

### 解析条件の設定

![](./assets/screenshot3.png)

- Level

ボーリング天端からの杭天端レベルを設定してください。

### 地盤情報ファイルのアップロード

![](./assets/screenshot4.png)

`./sample.xlsx` を参考に作成してアップロードしてください。
標準貫入試験結果、土質、液状化低減係数、実測したE0を入力します。

### 解析精度の設定

![](./assets/screenshot5.png)

行列のサイズを設定します。大きくした方が精度は上がりますが、計算が遅くなります。
ローカルだと500でもまず問題ないですが、ウェブアプリ上だとかなり厳しいです。気をつけてください。

## Theory

線形地盤における基本方程式は、

<div align="center"><img src="./assets/tex/texclip20200427102410.png"></div>

である。ここで、![](./assets/tex/texclip20200427102932.png) は水平地盤反力係数。
初期値が不明なため、差分法を用いて解析を行う。差分法による表現は下記となる。

<div align="center"><img src="./assets/tex/texclip20200427102327.png"></div>

境界条件は、まず杭頭について、

<div align="center"><img src="./assets/tex/texclip20200427102445.png"></div>

また、杭頭の回転剛性 ![](./assets/tex/texclip20200427102535.png) を用いて、

<div align="center"><img src="./assets/tex/texclip20200427102610.png"></div>

杭脚についての境界条件は、ローラー支点を仮定して、

<div align="center"><img src="./assets/tex/texclip20200427102714.png"></div>

以上より、一般化された行列として下記を組み立てることができる。

<div align="center"><img src="./assets/tex/texclip20200427102750.png"></div>

あとは両辺に左から逆行列を乗ずることによって、連立方程式をとけば良い。地盤の多層状態を考慮する場合は、![](./assets/tex/texclip20200427102820.png) についてデータを与えれば良いし、地盤の非線形性を考慮する場合は、$k_h(x)$ に $y^{-1/2}$ を乗じて収斂計算を行えば良い。


## Licence
MIT


## Author
Ryuhei Fujita
