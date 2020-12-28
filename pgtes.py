### インポート
import sys
import math
import pygame
from pygame.locals import *
 
### 定数
WIDTH  = 640  # 幅
HEIGHT = 400  # 高さ
SIZE   = 20   # 辺長
BLANK  = 40   # 余白
angle = 0

### モジュール初期化
pygame.init()

### 時間オブジェクト生成
clock = pygame.time.Clock()

### 画面設定
surface = pygame.display.set_mode((WIDTH, HEIGHT))

### 四角形作成
rect = pygame.Rect(0, HEIGHT-SIZE, SIZE, SIZE)

### サイン角度

while True:

    ### 幅サイズ分ループ
    for x in range(0, WIDTH):

        ### 座標設定
        rect.left = x
        p  = int(HEIGHT-math.sin(math.radians(angle))*(HEIGHT-BLANK))-SIZE

        ### 画面初期化
        surface.fill((0,0,0))

        ### 四角形描画
        surface.fill((255,255,255), rect)
        pygame.display.update()

        ### 角度180度確認
        if angle >= 180-1:
            angle = 0
        else:
            angle += 1

        ### フレームレート設定
        clock.tick(60)

        ### イベント処理
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:

                ### 終了処理
                pygame.quit()
                sys.exit()