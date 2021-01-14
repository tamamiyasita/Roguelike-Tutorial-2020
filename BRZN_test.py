"""
shinsa82
@shinsa82
2020年12月02日に更新
【プログラムと証明】線分を描画する「ブレゼンハムのアルゴリズム」を検証する
Python
アルゴリズム
Status
いまのところ描画と人力での証明のところまで。次は TLA+ か Coq などの定理証明系で証明したい。
ところで、MathJax の垂直位置ずれすぎじゃね？

概要
ブレゼンハムのアルゴリズムとは、ピクセルで表現された画面上に線分を描画するためのアルゴリズムである。
ピクセルの座標は整数値しか持てないため、近似アルゴリズムが必要になる。
そのときに、誤差を持つ浮動小数点演算を行わないで計算を行える点がこのアルゴリズムの長所である。

参考文献
Wikipedia, ブレゼンハムのアルゴリズム: https://w.wiki/P2G
問題設定
端点 (x0,y0)(x0,y0) と (x1,y1)(x1,y1) を結ぶ線分を描画する。ただし、

端点は格子点、つまり座標値は整数である。
端点はどちらも第一象限にある、つまり、0<x0,0<y0,0<x1,0<y10<x0,0<y0,0<x1,0<y1 とする。
右上に向かう線分である。つまり、x0<x1,y0≤y1x0<x1,y0≤y1 とする。なお、水平線を含んでよいが、垂直線は含まない。
さらに、線分の傾きは 11 以下である、つまり、
y1−y0x1−x0≤1
y1−y0x1−x0≤1
である。
仮定がいろいろついているが、他のケースもすべてこのケースに帰着できるので、こう仮定して一般性を失わない。1

アルゴリズム
以下、x1−x0=Δxx1−x0=Δx, y1−y0=Δyy1−y0=Δy とおく。傾きは Δy/ΔxΔy/Δx と表せる。

傾きが 11 以下であることから、端点間の整数値の xx 座標 XX に対して、yy 座標 Y^(X)Y^(X) を整数になるように計算し、点 (X,Y^(X))(X,Y^(X)) を描画していけば直線っぽく見えると思われる。
ただし、本来の直線の近似でなければいけないから、本来の yy 座標 Y(X)Y(X) と Y^(X)Y^(X) の誤差の絶対値 |Y^(X)−Y(X)||Y^(X)−Y(X)| が 1/21/2 以下になるようにするとよい。yy 座標値を四捨五入しながら描画していくイメージである。

具体例
たとえば、(1,1)(1,1) から (12,5)(12,5) (傾き 4/114/11) への線分を描画するとこのようになる (matplotlib で描いた)。

bre1.png

プログラム
Wikipedia にある最初のアルゴリズムは分数 (deltaerr の分母の ΔxΔx および if 文の 0.5 の分母の 22) を使用しているため、浮動小数点演算が必要である。そこで、誤差計算の部分についてすべてを 2Δx2Δx 倍すると、以下のような Python プログラムになる。
なお、grid を NumPy の配列としておくと matplotlib の imshow() や matshow() で描画できる。
"""

    #1, 原点p0にx,yを入れる、
    #2, 行き先P1にも同じ処理をする
    #3, state_ui
    # def plot(x, y):
    #     pass# この位置にgrid_to_pixelでdraw_Rectを被せる
    # x1, y1 = p0
    # x2, y2 = p1
    # dx = x2 - x1
    # dy = y2 - y1
    # error = 0
    # y = y1
    # for x in range(x1, x2+1):
    #     plot(x, y)
    #     error += 2*y
    #     if error > x:
    #         y += 1
    #         error -= 2*delta_x
    # return None

        # Setup initial conditions
def Bresenham(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points