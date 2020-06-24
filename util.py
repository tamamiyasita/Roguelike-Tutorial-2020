import arcade
from constants import *


def pixel_position(x, y):
    """tilepositionからsprite_sizeに変換する"""
    px = x * SPRITE_SIZE * SPRITE_SCALE + SPRITE_SIZE // 2 * SPRITE_SCALE
    py = y * SPRITE_SIZE * SPRITE_SCALE + SPRITE_SIZE // 2 * SPRITE_SCALE
    return px, py


def map_position(x, y):
    """sprite_sizeからtile_map_positionへの位置を指定する"""
    px = x - SPRITE_SIZE // 2 * SPRITE_SCALE
    px = round(px // (SPRITE_SIZE * SPRITE_SCALE))

    py = y - SPRITE_SIZE / 2 * SPRITE_SCALE
    py = round(py // (SPRITE_SIZE * SPRITE_SCALE))
    return px, py


def get_tile_set(img, tile_size):
    """
    読み込んだタイルセットイメージからtile_sizeに従って一つずつ画像オブジェクトに変換する
    null_tileがTrueならタイルセットイメージの空白部分を取り除くようにがんばる(?)
    """
    tile_img = arcade.load_texture(img)
    print(f"タイルセットの画像サイズ, {tile_img.width} x {tile_img.height}")
    tile_column = tile_img.width // tile_size
    print("列のタイル数", tile_column)
    tile_count = (tile_img.height // tile_size) * tile_column
    print("暫定タイルの数", tile_count)
    textures = arcade.load_spritesheet(
        img, tile_size, tile_size, tile_column, tile_count)

    # 空白タイルを取り除く
    textures = [i for i in textures if i.image.getbbox()]

    print("タイル総数：", len(textures), type(textures))

    return textures


class TileImageTest(arcade.Window):
    """
    get_tile_setで作られる画像オブジェクトのテスト
    ついでに番号をつけた
    """

    def __init__(self, width=1100, height=600, title="tile_test", textures=None, tile_size=16):
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
    t = r"image\Wall1.png"
    tst = TileImageTest(textures=t)

    arcade.run()


if __name__ == "__main__":
    main()
