"""
GPU機能を使ったパーティクルのテスト
"""
import arcade
import arcade.gl
from array import array
from dataclasses import dataclass
import random
import time
import math



SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "GPU Particle Explosion"
PARTICLE_COUNT = 35
MIN_FADE_TIME = 0.25
MAX_FADE_TIME = 1.5

@dataclass
class Burst:
    """各バーストの追跡"""
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float



class MyWindow(arcade.Window):
    """ Main window"""
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.burst_list = []

        # ポイントを視覚化するプログラム
        # vertex_shaderはパーティクルの各頂点をレンダリングする、四角形なら4回実行される
        # fragment_shaderは各ピクセルに対してレンダリングする
        # vertex_shader_v1.glslファイルを読み込み位置と色を取得
        # shaderファイルは日本語でコメントするとエラーがでるので注意
        self.program = self.ctx.load_program(
            vertex_shader="vertex_shader_v1.glsl",
            fragment_shader="fragment_shader.glsl",
        )



        self.ctx.enable_only(self.ctx.BLEND)

    def on_draw(self):
        """ Draw everything """
        self.clear()

        # 粒子サイズの設定
        self.ctx.point_size = 146 * self.get_pixel_ratio()

        # 各バーストをループする
        for burst in self.burst_list:

            # uniform data をセットする
            self.program["time"] = time.time() - burst.start_time

            # バーストをレンダリングする
            burst.vao.render(self.program, mode=self.ctx.POINTS)

    def on_update(self, dt):
        """ Update everything """
        temp_list = self.burst_list.copy()
        for burst in temp_list:
            if time.time() - burst.start_time > MAX_FADE_TIME:
                self.burst_list.remove(burst)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ User clicks mouse """
        # ボタンを押すたびにバーストを作成する
        def _gen_initial_data(initial_x, initial_y):
            # パーティクルを生成するジェネレータ関数
            for i in range(PARTICLE_COUNT):
                angle = random.uniform(0, 2 * math.pi)
                # speed = random.uniform((0.0, 0.3))
                speed = abs(random.gauss(0.1, 0.5)) * 0.7

                dx = math.sin(angle) * speed
                dy = math.cos(angle) * speed
                red = random.uniform(0.5, 1.0)
                green = random.uniform(0, red)
                blue = 0
                fade_rate = random.uniform(1 / MAX_FADE_TIME, 1 / MIN_FADE_TIME)
                if i % 5 == 0:
                    fade_rate = 4.0

                yield initial_x
                yield initial_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate



        # 現在のピクセル位置からOpenGLへの座標を再計算する
        x2 = x / self.width * 2.0 - 1.0
        y2 = y / self.height * 2.0 - 1.0

        # 粒子の初期データの取得
        initial_data = _gen_initial_data(x2, y2)

        # そのデータでバッファを作成
        buffer = self.ctx.buffer(data=array("f", initial_data))

        # バッファのデータがどのようにフォーマットされているかを示すバッファの説明文を作成します
        buffer_description = arcade.gl.BufferDescription(buffer,
                                                         "2f 2f 3f f",
                                                         ["in_pos",
                                                          "in_vel",
                                                          "in_color",
                                                          "in_fade_rate"])

        # 頂点属性オブジェクトの作成
        vao = self.ctx.geometry([buffer_description])

        # バーストオブジェクトを作成しバーストリストに追加する
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.burst_list.append(burst)







    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            arcade.close_window()


if __name__ == "__main__":
    window = MyWindow()
    window.center_window()
    arcade.run()