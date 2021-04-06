"""
GPU機能を使ったパーティクルのテスト
"""
import arcade
import arcade.gl
from array import array
from dataclasses import dataclass



SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "GPU Particle Explosion"


@dataclass
class Burst:
    """各バーストの追跡"""
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry



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



        self.ctx.enable_only()

    def on_draw(self):
        """ Draw everything """
        self.clear()

        # 粒子サイズの設定
        self.ctx.point_size = 2 * self.get_pixel_ratio()

        # 各バーストをループする
        for burst in self.burst_list:
            # バーストをレンダリングする
            burst.vao.render(self.program, mode=self.ctx.POINTS)

    def on_update(self, dt):
        """ Update everything """
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ User clicks mouse """
        # ボタンを押すたびにバーストを作成する
        def _gen_initial_data(initial_x, initial_y):
            # パーティクルを生成するジェネレータ関数
            yield initial_x
            yield initial_y

        # 現在のピクセル位置からOpenGLへの座標を再計算する
        x2 = x / self.width * 2.0 - 1.0
        y2 = y / self.height * 2.0 - 1.0

        # 粒子の初期データの取得
        initial_data = _gen_initial_data(x2, y2)

        # そのデータでバッファを作成
        buffer = self.ctx.buffer(data=array("f", initial_data))

        # バッファのデータがどのようにフォーマットされているかを示すバッファの説明文を作成します
        buffer_description = arcade.gl.BufferDescription(buffer, "2f", ["in_pos"])

        # 頂点属性オブジェクトの作成
        vao = self.ctx.geometry([buffer_description])

        # バーストオブジェクトを作成しバーストリストに追加する
        burst = Burst(buffer=buffer, vao=vao)
        self.burst_list.append(burst)







    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            arcade.close_window()


if __name__ == "__main__":
    window = MyWindow()
    window.center_window()
    arcade.run()