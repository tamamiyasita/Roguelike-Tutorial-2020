import arcade
from random import randint
from constants import *
from data import *
from functools import wraps
import time


def Bresenham(p0, p1):
    #1, 原点p0にx,yを入れる、
    #2, 行き先P1にも同じ処理をする
    #3, state_ui
    def plot(x, y):
        # この位置にgrid_to_pixelでdraw_Rectを被せる
        x, y = grid_to_pixel(x, y)
        arcade.draw_rectangle_filled(x,y,GRID_SIZE,GRID_SIZE,arcade.color.BLACK_BEAN)
    x0, y0 = p0
    x1, y1 = p1
    delta_x = x1 - x0
    delta_y = y1 - y0
    error = 0
    y = y0
    for x in range(min(x0, x1+1), max(x0, x1+1)):
        plot(x, y)
        error += 2*delta_y
        if error > delta_x:
            y += 1
            error -= 2*delta_x
    return None

def grid_to_pixel(x, y):
    """tilepositionからsprite_sizeに変換する"""
    px = x * SPRITE_SIZE * SPRITE_SCALE + SPRITE_SIZE / 2 * SPRITE_SCALE
    py = (y * SPRITE_SIZE * SPRITE_SCALE + SPRITE_SIZE /
          2 * SPRITE_SCALE) + STATES_PANEL_HEIGHT
    return px, py


def pixel_to_grid(x, y):
    """sprite_sizeからtile_pixel_to_gridへの位置を指定する"""
    px = x - SPRITE_SIZE / 2 * SPRITE_SCALE
    px = round(px / GRID_SIZE)

    py = y - SPRITE_SIZE / 2 * SPRITE_SCALE - STATES_PANEL_HEIGHT
    py = round(py / GRID_SIZE)
    return px, py


def dice(D, max_d):
    return D * randint(1, max_d)


def get_entity(x, y, sprite_lists):
    px, py = grid_to_pixel(x, y)
    get_sprite = arcade.SpriteList()
    for sprite_list in sprite_lists:
        s_list = arcade.get_sprites_at_exact_point((px, py), sprite_list)
        for sprite in s_list:
            if sprite.blocks:
                get_sprite.append(sprite)


def get_blocking_entity(x, y, sprite_lists):
    px, py = grid_to_pixel(x, y)
    blocking_sprite = arcade.SpriteList()
    for sprite_list in sprite_lists:
        s_list = arcade.get_sprites_at_exact_point((px, py), sprite_list)
        for sprite in s_list:
            if sprite.blocks:
                blocking_sprite.append(sprite)

    if len(blocking_sprite) > 0:
        return blocking_sprite
    else:
        return None


def get_door(x, y, sprite_list):
    px, py = grid_to_pixel(x, y)
    sprite_list = arcade.get_sprites_at_exact_point((px, py), sprite_list)
    door_sprite = arcade.SpriteList()
    for sprite in sprite_list:
        if sprite and Tag.door in sprite.tag:
            door_sprite.append(sprite)

    if len(door_sprite) > 0:
        return door_sprite
    else:
        return None


def result_add(value=0):
    """関数やメソッドの出力に任意の値やリストの合計を加えるデコレータ
    プロパティに使用する場合の例
        @property
        @result_add([i for i in range(10)])
        def x(self):
            x = 5
            return x
    """
    def _result_add(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if hasattr(value, "__iter__"):
                result += sum(value)
                return result
            else:
                result += value
                return result
        return wrapper
    return _result_add


def stop_watch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print(f"{func.__name__}は{elapsed_time}秒かかりました")
        return result
    return wrapper


def get_tile_set(img, tile_size):
    """
    読み込んだタイルセットイメージからtile_sizeに従って一つずつ画像オブジェクトに変換する
    null_tileがTrueならタイルセットイメージの空白部分を取り除くようにがんばる(?)
    """
    tile_img = arcade.load_texture(img)
    # print(f"タイルセットの画像サイズ, {tile_img.width} x {tile_img.height}")
    tile_column = tile_img.width // tile_size
    # print("列のタイル数", tile_column)
    tile_count = (tile_img.height // tile_size) * tile_column
    # print("暫定タイルの数", tile_count)
    textures = arcade.load_spritesheet(
        img, tile_size, tile_size, tile_column, tile_count)

    # 空白タイルを取り除く
    textures = [i for i in textures if i.image.getbbox()]

    # print("タイル総数：", len(textures), type(textures[0]), textures[0].width)

    return textures


class TileImageTest(arcade.Window):
    """
    get_tile_setで作られる画像オブジェクトのテスト
    ついでに番号をつけた
    """

    def __init__(self, width=1100, height=600, title="tile_test", textures=None, tile_size=32):
        super().__init__(width, height, title)
        self.tile_size = tile_size
        arcade.set_background_color(arcade.color.AERO_BLUE)

        self.textures = get_tile_set(textures, tile_size)

    def on_draw(self):
        arcade.start_render()
        I = 0
        c = 25

        for i, v in enumerate(self.textures):
            v.draw_scaled(center_x=I * self.tile_size + 25, center_y=c)
            arcade.draw_text(str(i), start_x=I * self.tile_size + 25,
                             start_y=c+15, color=arcade.color.BLACK_BEAN, font_size=9, anchor_x="center")
            if i >= 0:
                I += 1
            if i >= 2 and i % 50 == 0:
                c += 40
                I = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    t = r"image/bs_walls.png"
    tst = TileImageTest(textures=t)

    arcade.run()


if __name__ == "__main__":
    main()
