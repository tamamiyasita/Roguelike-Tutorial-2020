from random import choice
import arcade
from arcade.gl import geometry
import json
import pyglet.gl as gl

# import logging
# import logging_config

from game_engine import GameEngine
from constants import *
from keymap import keymap, grid_move_key, choices_key

from ui.normal_ui import NormalUI
from ui.mouse_ui import MouseUI
from ui.select_ui import SelectUI
from ui.character_screen_ui import draw_character_screen
from ui.inventory_ui import draw_inventory
from ui.message_window import MessageWindow
from ui.level_up_ui import LevelupUI

from util import pixel_to_grid, stop_watch
from viewport import viewport

# log = logging.getLogger("__main__")


class MG(arcade.Window):
    """メインウィンドウを表示し、キーボードとマウスの操作を行います"""

    def __init__(self, width, height, title):
        """
        Args:
            width = 画面の幅
            height = 画面の高さ
            title = タイトル
            antialiasing = 画像にアンチエイリアスを掛けるかどうか
        """
        super().__init__(width, height, title, antialiasing=False)

        self.engine = GameEngine()

        self.player_direction = None
        self.grid_select = [0, 0]
        self.mouse_position = None
        self.viewports = None
        self.grid_press = None
        self.viewport_left = 0
        self.viewport_bottom = 0
        self.choice = 0
        self.game_dict = None

    def setup(self):
        """変数に値を設定する、ミニマップ作成の情報もここで渡す"""
        self.engine.setup()
        viewport(self.engine.player.center_x, self.engine.player.center_y)

        # ここでminimapの作成を行う
        # ----------------------
        # ミニマップの描画位置指定
        screen_size = (GAME_GROUND_WIDTH, GAME_GROUND_HEIGHT)
        self.program = self.ctx.load_program(
            vertex_shader=arcade.resources.shaders.vertex.default_projection,
            fragment_shader=arcade.resources.shaders.fragment.texture)

        # ピクセルの色を保存するために色の添付ファイルを追加します
        self.color_attachment = self.ctx.texture((screen_size), components=4,
                                                 filter=(gl.GL_NEAREST, gl.GL_NEAREST))

        # 必要な色を添付したフレームバッファを作成する
        self.offscreen = self.ctx.framebuffer(
            color_attachments=[self.color_attachment])

        self.quad_fs = geometry.quad_2d_fs()

        self.mini_map_quad = geometry.quad_2d(
            size=(0.5792, 0.97), pos=(0.949, 1.022))
        # ----------------------

        # Lコマンドで呼び出すlook機能
        self.select_UI = SelectUI(engine=self.engine)

        # 会話画面の初期化はここで行う
        self.massage_window = MessageWindow(self.engine)

        self.level_up_window = LevelupUI(self.engine)

    def draw_sprites(self):
        """ 全てのスプライトリストをここで描画する """
        # 背景が表示されないように最初に黒で塗りつぶす、他の方法を考えないと…
        arcade.draw_rectangle_filled(-1000, -1000,
                                     10000, 10000, color=arcade.color.BLACK)
        # 以下スプライトリスト
        self.engine.cur_level.floor_sprites.draw()
        self.engine.cur_level.wall_sprites.draw()
        self.engine.cur_level.map_obj_sprites.draw(filter=gl.GL_LO_BIAS_NV)
        self.engine.cur_level.item_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.actor_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.chara_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.equip_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.effect_sprites.draw()
        for e in self.engine.cur_level.effect_sprites:
            if hasattr(e, "emitter"):
                e.emitter.draw()

    def on_draw(self):
        """全画像の表示"""

        arcade.start_render()
        """minimap draw"""
        if self.engine.game_state == GAME_STATE.NORMAL or self.engine.game_state == GAME_STATE.DELAY_WINDOW:
            self.offscreen.use()
            self.offscreen.clear(arcade.color.BLACK)

            arcade.set_viewport(0, GAME_GROUND_WIDTH, 0,
                                GAME_GROUND_HEIGHT+GRID_SIZE*2)

            self.engine.cur_level.map_point_sprites.draw()
            arcade.draw_rectangle_filled(center_x=self.engine.player.center_x,
                                         center_y=self.engine.player.center_y, width=50, height=50, color=arcade.color.BLUE)

            self.engine.cur_level.item_point_sprites.draw()

        self.use()
        self.color_attachment.use(0)
        self.quad_fs.render(self.program)
        # アタック時はビューポート固定する
        if self.engine.player.state == state.ATTACK or self.engine.player.state == state.TURN_END:
            viewport(self.engine.player.target_x, self.engine.player.target_y)
        else:
            viewport(self.engine.player.center_x, self.engine.player.center_y)
        # ビューポートの左と下の現在位置を変数に入れる、これはステータスパネルを画面に固定する為に使います
        self.viewports = arcade.get_viewport()
        self.viewport_left = self.viewports[0]
        self.viewport_bottom = self.viewports[2]
        self.draw_sprites()
        arcade.set_background_color(arcade.color.BLACK)

        # ノーマルステート時の画面表示
        if self.engine.game_state == GAME_STATE.NORMAL or self.engine.game_state == GAME_STATE.DELAY_WINDOW:
            normal_UI = NormalUI(self.engine.player, self.viewport_left, self.viewport_bottom,
                                 self.engine.selected_item, self.engine.messages, self.mouse_position)
            normal_UI.draw_in_normal_state()
            if self.mouse_position:
                self.mouse_ui.draw_mouse_over_text()
            self.grid_select = [0, 0]

        # アイテム使用時マウス位置にグリッド表示
        elif self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            self.select_UI.draw_in_select_ui(
                arcade.get_viewport(), self.grid_press, self.grid_select)

        # Character_Screen表示
        elif self.engine.game_state == GAME_STATE.CHARACTER_SCREEN:
            draw_character_screen(self.viewport_left, self.viewport_bottom)


        elif self.engine.game_state == GAME_STATE.INVENTORY:
            draw_inventory(self.engine.player, self.engine.selected_item, self.viewport_left, self.viewport_bottom)

        elif self.engine.game_state == GAME_STATE.LEVEL_UP_WINDOW:
            self.level_up_window.window_pop(self.viewports)

        # 会話画面の表示
        elif self.engine.game_state == GAME_STATE.MESSAGE_WINDOW:
            self.massage_window.window_pop(arcade.get_viewport(), self.choice)

        # fov_recomputeがTruならfov計算
        if self.engine.fov_recompute:
            self.engine.fov()

        # draw the mini_map
        if self.engine.game_state == GAME_STATE.NORMAL or self.engine.game_state == GAME_STATE.DELAY_WINDOW:
            self.color_attachment.use(0)
            self.mini_map_quad.render(self.program)

    def on_update(self, delta_time):
        """全てのスプライトリストのアップデートを行う
           他にアクションキュー、ターンチェンジ、pcの移動とviewport、expのチェック
        """
        if self.engine.game_state == GAME_STATE.NORMAL:

            self.engine.cur_level.chara_sprites.update_animation()
            self.engine.cur_level.chara_sprites.update()
            self.engine.cur_level.actor_sprites.update_animation()
            self.engine.cur_level.actor_sprites.update()
            self.engine.cur_level.effect_sprites.update()
            self.engine.cur_level.equip_sprites.update()
            self.engine.cur_level.equip_sprites.update_animation()

            self.engine.process_action_queue(delta_time)
            self.engine.turn_loop.loop_on(self.engine)
            self.engine.check_for_player_movement(self.player_direction)
            self.engine.cur_level.map_obj_sprites.update_animation()

            # EXPのチェック
            if self.engine.player.state == state.READY:
                self.engine.player.check_experience_level(self.engine)

            # ここでdamageのポップアップを行う
            if self.engine.damage_pop:
                for pop in self.engine.damage_pop:
                    pop.start()

            # playerの装備状態のアップデート
            if self.engine.player.state == state.READY:
                self.engine.player.equipment.update(
                    self.engine.cur_level.equip_sprites)

        # look機能のアップデート
        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            self.select_UI.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.engine.game_state = GAME_STATE.DELAY_WINDOW
            print("save")
            self.game_dict = self.engine.get_dict()

            with open("game_save.json", "w") as write_file:
                json.dump(self.game_dict, write_file, indent=4, sort_keys=True, check_circular=False)  # indent=4, sort_keys=True
                
            arcade.close_window()

        # playerの移動
        self.engine.move_switch = True
        self.player_direction = keymap(key, self.engine)

        # カーソルのキー移動量
        grid = grid_move_key(key, self.engine)
        if isinstance(grid, tuple):
            self.grid_select[0] += grid[0]
            self.grid_select[1] += grid[1]
        else:
            self.grid_press = grid

        # ドア開閉
        if self.engine.player.state == state.DOOR:
            door_check = keymap(key, self.engine)
            if door_check:
                self.engine.action_queue.extend([{"use_door": door_check}])

        # Level states up処理
        if self.engine.game_state == GAME_STATE.LEVEL_UP_WINDOW:
            self.level_up_window.states_choices(key)

        # 会話画面の返答処理
        if self.engine.game_state == GAME_STATE.MESSAGE_WINDOW:
            self.choice = self.massage_window.message_choices(key)

        if key == arcade.key.F7:
            self.save()
        elif key == arcade.key.F8:
            self.load()
        elif key == arcade.key.F1:
            self.engine.player.fighter.ability_points += 1
            self.engine.player.fighter.level += 1
            self.engine.game_state = GAME_STATE.LEVEL_UP_WINDOW

    def on_key_release(self, key, modifiers):
        self.player_direction = None
        # print(self.engine.player.fighter.skill_list)
        # print(self.engine.player.fighter.skill_list[0].level,
        #       self.engine.player.fighter.skill_list[0].name)

    def on_mouse_motion(self, x, y, dx, dy):
        """マウスオーバー処理"""
        # マウスの位置にビューポートの座標を足す
        self.mouse_position = x + self.viewport_left, y + self.viewport_bottom

        if self.mouse_position:
            self.mouse_ui = MouseUI(mouse_position=self.mouse_position,
                                    viewport_x=self.viewport_left, viewport_y=self.viewport_bottom,
                                    sprite_lists=[self.engine.cur_level.actor_sprites, self.engine.cur_level.item_sprites])

    def on_mouse_press(self, x, y, button, modifiers):
        # engineのgrid_clickに渡されるマウスボタン処理
        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            grid_x, grid_y = pixel_to_grid(
                x + self.viewport_left, y + self.viewport_bottom)
            self.engine.grid_click(grid_x, grid_y)
            self.engine.game_state = GAME_STATE.NORMAL


    @stop_watch
    def save(self):

        self.engine.game_state = GAME_STATE.DELAY_WINDOW
        self.game_dict = self.engine.get_dict()
        self.engine.game_state = GAME_STATE.NORMAL
        print("**save**")

    @stop_watch
    def load(self):
        data = None

        if self.game_dict:
            data = self.game_dict
        else:
            with open("game_save.json", "r") as read_file:
                data = json.load(read_file)
        if data:
            self.engine.game_state = GAME_STATE.DELAY_WINDOW
            print("**load**")
            self.engine.restore_from_dict(data)
            self.engine.player.state = state.READY
            viewport(self.engine.player.center_x, self.engine.player.center_y)
            self.engine.game_state = GAME_STATE.NORMAL
            self.engine.fov_recompute = True


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
