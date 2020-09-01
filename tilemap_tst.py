from constants import *
import arcade
from arcade.gl import geometry
import pyglet.gl as gl

import test_game_engine
from keymap import keymap, grid_move_key

from ui.normal_ui import NormalUI
from ui.mouse_ui import MouseUI
from ui.select_ui import SelectUI
from ui.character_screen_ui import CharacterScreen

from util import pixel_to_grid
from viewport import viewport


class test_game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title="test")
        self.engine = test_game_engine.GameEngine()
        self.player_direction = None
        self.grid_select = [0, 0]
        self.mouse_position = None
        self.viewports = None
        self.grid_press = None
        self.viewport_left = 0
        self.viewport_bottom = 0

    def setup(self):
        self.engine.setup()
        viewport(self.engine.player.center_x, self.engine.player.center_y)
        self.character_screen = CharacterScreen(self.engine.player)

        """minimap"""
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


        self.select_UI = SelectUI(engine=self.engine)

    
    def draw_sprites(self):
        """ 全てのスプライトリストをここで描画する """
        arcade.draw_rectangle_filled(-1000, -1000, 10000,10000,color=arcade.color.BLACK)
        self.engine.cur_level.wall_sprites.draw()
        # self.engine.cur_level.map_obj_sprites.draw(filter=gl.GL_LO_BIAS_NV)
        # self.engine.cur_level.item_sprites.draw(filter=gl.GL_NEAREST)
        # self.engine.cur_level.actor_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.chara_sprites.draw(filter=gl.GL_NEAREST)
        # self.engine.cur_level.effect_sprites.draw()
        # self.engine.cur_level.equip_sprites.draw(filter=gl.GL_NEAREST)

    def on_draw(self):

        arcade.start_render()
        """minimap draw"""
        if self.engine.game_state == GAME_STATE.NORMAL or self.engine.game_state == GAME_STATE.DELAY_WINDOW:
            self.offscreen.use()
            self.offscreen.clear(arcade.color.BLACK)

            arcade.set_viewport(0, GAME_GROUND_WIDTH, 0, GAME_GROUND_HEIGHT+GRID_SIZE*2)

            self.engine.cur_level.map_point_sprites.draw()
            arcade.draw_rectangle_filled(center_x=self.engine.player.center_x,
                                         center_y=self.engine.player.center_y, width=50, height=50, color=arcade.color.BLUE)

            self.engine.cur_level.item_point_sprites.draw()

        self.use()
        self.color_attachment.use(0)
        self.quad_fs.render(self.program)

        # アタック時はビューポート固定する
        if self.engine.player.state == state.ATTACK:
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
            self.character_screen.draw_character_screen(
                self.viewport_left, self.viewport_bottom)

        # fov_recomputeがTruならfov計算
        if self.engine.fov_recompute:
            self.engine.fov()

        if self.engine.game_state == GAME_STATE.NORMAL or self.engine.game_state == GAME_STATE.DELAY_WINDOW:
            """minimap_related"""
            # draw the mini_map
            self.color_attachment.use(0)
            self.mini_map_quad.render(self.program)
    def on_update(self, delta_time):
        """全てのスプライトリストのアップデートを行う
           他にactionqueue、ターンチェンジ、pcの移動とviewport、expのチェック
        """
        if self.engine.game_state == GAME_STATE.NORMAL:

            self.engine.cur_level.chara_sprites.update_animation()
            self.engine.cur_level.chara_sprites.update()
            # self.engine.cur_level.actor_sprites.update_animation()
            # self.engine.cur_level.actor_sprites.update()
            # self.engine.cur_level.effect_sprites.update()
            # self.engine.cur_level.equip_sprites.update()
            # self.engine.cur_level.equip_sprites.update_animation()

            self.engine.process_action_queue(delta_time)
            self.engine.turn_loop.loop_on(self.engine)
            self.engine.check_for_player_movement(self.player_direction)
            # self.engine.cur_level.map_obj_sprites.update_animation()

            self.engine.player.check_experience_level(self.engine)

            # playerの装備状態のアップデート
            if self.engine.player.state == state.READY:
                self.engine.player.equipment.update(
                    self.engine.cur_level.equip_sprites)

        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            self.select_UI.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
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

    def on_key_release(self, key, modifiers):
        self.player_direction = None


def main():
    window = test_game()
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
