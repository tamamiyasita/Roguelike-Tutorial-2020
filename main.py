import arcade
from arcade.gl import geometry
import json
import pyglet.gl as gl

# import logging
# import logging_config

from constants import *
from game_engine import GameEngine
from keymap import keymap, grid_select_key, inventory_key, character_screen_key

from ui.normal_ui import NormalUI
from ui.mouse_ui import MouseUI
from ui.select_ui import SelectUI
from ui.character_screen_ui import draw_character_screen
from ui.inventory_ui import draw_inventory
from ui.message_window import MessageWindow
from ui.level_up_ui import LevelupUI
from ui.level_up_flower_ui import LevelUpFlower

from util import grid_to_pixel, pixel_to_grid, stop_watch
from viewport import viewport
from actor.states.poison_status import PoisonStatus

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
        self.mouse_position = None
        self.viewports = None
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
            size=(0.86, 0.95), pos=(1.0155, 1.055))
        # ----------------------

        # Lコマンドで呼び出すlook機能
        self.select_UI = SelectUI(engine=self.engine)

        # 会話画面の初期化はここで行う
        self.massage_window = MessageWindow(self.engine)

        self.level_up_window = LevelupUI()
        self.level_up_flower = LevelUpFlower(self.engine)

    def draw_sprites(self):
        """ 全てのスプライトリストをここで描画する """
        # 背景が表示されないように最初に黒で塗りつぶす、他の方法を考えないと…
        arcade.draw_rectangle_filled(-1000, -1000,
                                     10000, 10000, color=arcade.color.BLACK)
        # 以下スプライトリスト
        self.engine.cur_level.floor_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.wall_sprites.draw()
        self.engine.cur_level.map_obj_sprites.draw(filter=gl.GL_LO_BIAS_NV)
        self.engine.cur_level.item_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.actor_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.flower_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.chara_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.equip_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.effect_sprites.draw(filter=gl.GL_NEAREST)

        TMP_EFFECT_SPRITES.draw(filter=gl.GL_NEAREST)
        for e in TMP_EFFECT_SPRITES:
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
                                         center_y=self.engine.player.center_y, width=45, height=45, color=arcade.color.BLUE)

            self.engine.cur_level.item_point_sprites.draw()

        self.use()
        self.color_attachment.use(0)
        self.quad_fs.render(self.program)
        # アタック時はビューポート固定する
        if self.engine.player.state == state.ATTACK or self.engine.player.state == state.TURN_END and hasattr(self.engine.player, "from_x"):
            viewport(self.engine.player.from_x, self.engine.player.from_y)
        else:
            viewport(self.engine.player.center_x, self.engine.player.center_y)
        # LOOKシステム
        if self.engine.game_state == GAME_STATE.SELECT_LOCATION or self.engine.game_state == GAME_STATE.LOOK:
            x, y = grid_to_pixel(self.select_UI.grid_select[0]+self.engine.player.x, self.select_UI.grid_select[1]+self.engine.player.y)
            viewport(x, y)

        # ビューポートの左と下の現在位置を変数に入れる、これはステータスパネルを画面に固定する為に使います
        self.viewports = arcade.get_viewport()
        self.viewport_left = self.viewports[0]
        self.viewport_bottom = self.viewports[2]
        self.draw_sprites()
        arcade.set_background_color(arcade.color.BLACK)

        # ノーマルステート時の画面表示6
        if self.engine.game_state == GAME_STATE.NORMAL or self.engine.game_state == GAME_STATE.DELAY_WINDOW:
            normal_UI = NormalUI(self.engine, self.viewports,
                                 self.engine.selected_item, self.engine.messages, self.mouse_position)
            normal_UI.draw_in_normal_state()
            if self.mouse_position:
                self.mouse_ui.draw_mouse_over_text()

        # アイテム使用時マウス位置にグリッド表示
        elif self.engine.game_state == GAME_STATE.SELECT_LOCATION or self.engine.game_state == GAME_STATE.LOOK:
            self.select_UI.draw_in_select_ui(arcade.get_viewport(), self.engine)

        # Character_Screen表示
        elif self.engine.game_state == GAME_STATE.CHARACTER_SCREEN:
            draw_character_screen(self.engine, arcade.get_viewport(), self.engine.selected_item)


        elif self.engine.game_state == GAME_STATE.INVENTORY:
            draw_inventory(self.engine.player, self.engine.selected_item, self.viewports)

        elif self.engine.game_state == GAME_STATE.LEVEL_UP_WINDOW:
            self.level_up_window.window_pop(self.viewports, self.engine)

        elif self.engine.game_state == GAME_STATE.LEVEL_UP_FLOWER:
            self.level_up_flower.window_pop(self.viewports)

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
        self.engine.process_action_queue(delta_time)


        if self.engine.game_state == GAME_STATE.NORMAL:

            self.engine.cur_level.chara_sprites.update_animation(delta_time)
            self.engine.cur_level.chara_sprites.update()
            self.engine.cur_level.actor_sprites.update_animation(delta_time)
            self.engine.cur_level.actor_sprites.update()
            self.engine.cur_level.effect_sprites.update()
            self.engine.cur_level.effect_sprites.update_animation()
            self.engine.cur_level.equip_sprites.update()
            self.engine.cur_level.equip_sprites.update_animation()
            self.engine.flower_sprites.update()
            self.engine.flower_sprites.update_animation()
            self.engine.cur_level.map_obj_sprites.update_animation()
            TMP_EFFECT_SPRITES.update()
            TMP_EFFECT_SPRITES.update_animation()


            self.engine.normal_state_update(self.player_direction, delta_time)







    def on_key_press(self, key, modifiers):
        # windowを閉じた時にjsonにダンプする
        if key == arcade.key.BACKSPACE:
            self.engine.game_state = GAME_STATE.DELAY_WINDOW
            print("save")
            self.game_dict = self.engine.get_dict()

            with open("game_save.json", "w") as write_file:
                json.dump(self.game_dict, write_file, indent=4, sort_keys=True, check_circular=False) 
                
            arcade.close_window()
        
        if key == arcade.key.DELETE:
            arcade.close_window()


                     
        # playerの移動
        self.engine.move_switch = True
        if self.engine.game_state == GAME_STATE.NORMAL:
            self.player_direction = keymap(key, self.engine)

        # ドア開閉
        if self.engine.player.form == form.DOOR:
            door_check = keymap(key, self.engine)
            if door_check:
                self.engine.action_queue.extend([{"use_door": door_check}])

        # Lコマンド時、スクロール仕様時などのカーソル移動と選択
        elif self.engine.game_state == GAME_STATE.SELECT_LOCATION or self.engine.game_state == GAME_STATE.LOOK:
            grid_select_key(key, self.select_UI)

        # インベントリを操作する
        elif self.engine.game_state == GAME_STATE.INVENTORY:
            inventory_key(key, self.engine)


        # Level states up処理
        elif self.engine.game_state == GAME_STATE.LEVEL_UP_WINDOW:
            self.level_up_window.states_choices(key)
        elif self.engine.game_state == GAME_STATE.LEVEL_UP_FLOWER:
            self.level_up_flower.states_choices(key)

 
        # 会話画面の返答処理
        elif self.engine.game_state == GAME_STATE.MESSAGE_WINDOW:
            self.choice = self.massage_window.message_choices(key)

        # キャラクタースクリーンでスキルのオンオフ操作
        elif self.engine.game_state == GAME_STATE.CHARACTER_SCREEN:
            character_screen_key(key, self.engine)
        

        if key == arcade.key.F7:

            self.save()
        elif key == arcade.key.F8:

            self.load()
        elif key == arcade.key.F1:
            from level_up_sys import check_experience_level

            self.engine.player.fighter.current_xp += 70
            self.engine.player.equipment.item_exp_add(100)
            check_experience_level(self.engine.player, self.engine)

        if key == arcade.key.F2:
            self.engine.player.fighter.states.append(PoisonStatus(3))



    def on_key_release(self, key, modifiers):
        self.player_direction = None

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
        self.game_dict = self.engine.get_dict()

    @stop_watch
    def load(self):
        data = None

        if self.game_dict:
            data = self.game_dict
        else:
            with open("game_save.json", "r") as read_file:
                data = json.load(read_file)
        if data:
            self.engine.restore_from_dict(data)
            viewport(self.engine.player.center_x, self.engine.player.center_y)


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
