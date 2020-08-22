import arcade
import json
import pyglet.gl as gl

# import logging
# import logging_config

from game_engine import GameEngine
from constants import *
from keymap import keymap, grid_move_key

from ui.normal_ui import NormalUI
from ui.mouse_ui import MouseUI
from ui.select_ui import SelectUI
from ui.character_screen_ui import CharacterScreen

from util import pixel_to_grid
from viewport import viewport

# log = logging.getLogger("__main__")


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)

        self.engine = GameEngine()

        self.player_direction = None
        self.grid_select = [0, 0]
        self.mouse_position = None
        self.viewport_x = 0
        self.viewport_y = 0

    def setup(self):
        self.engine.setup()
        viewport(self.engine.player)
        self.character_screen = CharacterScreen(self.engine.player)

    def draw_sprites(self):
        """ 全てのスプライトリストをここで描画する """
        self.engine.cur_level.map_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.map_obj_sprites.draw()
        self.engine.cur_level.item_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.actor_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.chara_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.effect_sprites.draw()
        self.engine.cur_level.equip_sprites.draw(filter=gl.GL_NEAREST)

    def on_draw(self):
        arcade.start_render()

        # ビューポートの左と下の現在位置を変数に入れる、これはステータスパネルを画面に固定する為に使います
        self.viewport_x = arcade.get_viewport()[0]
        self.viewport_y = arcade.get_viewport()[2]

        self.draw_sprites()

        # ノーマルステート時の画面表示
        if self.engine.game_state == GAME_STATE.NORMAL or self.engine.game_state == GAME_STATE.DELAY_WINDOW:
            normal_UI = NormalUI(self.engine.player, self.viewport_x, self.viewport_y,
                                 self.engine.selected_item, self.engine.messages, self.mouse_position)
            normal_UI.draw_in_normal_state()
            if self.mouse_position:
                self.mouse_ui.draw_mouse_over_text()

            self.grid_select = [0, 0]
        # アイテム使用時マウス位置にグリッド表示
        elif self.engine.game_state == GAME_STATE.SELECT_LOCATION:

            select_UI = SelectUI(engine=self.engine, viewport_x=self.viewport_x, viewport_y=self.viewport_y, sprite_list=[
                                 self.engine.cur_level.actor_sprites, self.engine.cur_level.item_sprites])
            select_UI.grid_select(self.engine, grid=self.grid_select)

            if self.mouse_position:
                self.mouse_ui.draw_select_mouse_location()

        # Character_Screen表示
        elif self.engine.game_state == GAME_STATE.CHARACTER_SCREEN:
            self.character_screen.draw_character_screen(
                self.viewport_x, self.viewport_y)

        # fov_recomputeがTruならfov計算
        if self.engine.fov_recompute:
            self.engine.fov()

    def on_update(self, delta_time):
        """全てのスプライトリストのアップデートを行う
           他にactionqueue、ターンチェンジ、pcの移動とviewport、expのチェック
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

            self.engine.player.check_experience_level(self.engine)

            # playerの装備状態のアップデート
            if self.engine.player.state == state.READY:
                self.engine.player.equipment.update(
                    self.engine.cur_level.equip_sprites)

            # playerがmove状態の時だけviewportを計算する
            if self.engine.player.state == state.ON_MOVE:
                viewport(self.engine.player)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            arcade.close_window()

        # playerの移動
        self.engine.move_switch = True
        self.player_direction = keymap(key, self.engine)

        # カーソルのキー移動量
        grid = grid_move_key(key, self.engine)
        if grid:
            self.grid_select[0] += grid[0]
            self.grid_select[1] += grid[1]

        # ドア開閉
        if self.engine.player.state == state.DOOR:
            door_check = keymap(key, self.engine)
            if door_check:
                self.engine.action_queue.extend([{"use_door": door_check}])

        if key == arcade.key.F11:
            self.save()
        elif key == arcade.key.F12:
            self.load()

    def on_key_release(self, key, modifiers):
        self.player_direction = None

    def on_mouse_motion(self, x, y, dx, dy):
        """マウスオーバー処理"""
        # マウスの位置にビューポートの座標を足す
        self.mouse_position = x + self.viewport_x, y + self.viewport_y

        if self.mouse_position:
            self.mouse_ui = MouseUI(mouse_position=self.mouse_position,
                                    viewport_x=self.viewport_x, viewport_y=self.viewport_y,
                                    sprite_lists=[self.engine.cur_level.actor_sprites, self.engine.cur_level.item_sprites])

    def on_mouse_press(self, x, y, button, modifiers):
        """engineのgrid_clickに渡されるマウスボタン処理"""
        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            grid_x, grid_y = pixel_to_grid(
                x + self.viewport_x, y + self.viewport_y)
            self.engine.grid_click(grid_x, grid_y)
            self.engine.game_state = GAME_STATE.NORMAL

        """ステータスボタン処理"""
        if self.engine.game_state == GAME_STATE.CHARACTER_SCREEN:
            self.character_screen.buttons_click(
                x+self.viewport_x, y+self.viewport_y)

    def save(self):
        self.engine.game_state = GAME_STATE.DELAY_WINDOW
        print("save")
        game_dict = self.engine.get_dict()

        with open("game_save.json", "w") as write_file:
            json.dump(game_dict, write_file, indent=4, sort_keys=True)
        print("**save**")
        self.engine.game_state = GAME_STATE.NORMAL

    def load(self):
        print("load")
        self.engine.game_state = GAME_STATE.DELAY_WINDOW
        with open("game_save.json", "r") as read_file:
            data = json.load(read_file)

        print("**load**")
        self.engine.restore_from_dict(data)
        self.engine.player.state = state.READY
        self.engine.fov_recompute = True
        viewport(self.engine.player)
        self.engine.game_state = GAME_STATE.NORMAL


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
