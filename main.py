from os import write
import arcade
import json
import pyglet.gl as gl
from itertools import chain

from game_engine import GameEngine
from constants import *
from status_bar import draw_status_bar
from util import grid_to_pixel, pixel_to_grid
from viewport import viewport


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)

        self.engine = GameEngine()
        self.player_direction = None
        self.mouse_over_text = None
        self.mouse_position = None

    def setup(self):
        self.engine.setup()
        viewport(self.engine.player)

    def draw_hp_and_status_bar(self):
        """ステータスパネルとHPバー"""
        # パネル用変数
        hp_font_size = 13
        hp_bar_width = hp_font_size * 5  # HPバーの幅
        hp_bar_height = hp_font_size - 2  # HPバーの太さ
        hp_bar_margin = self.viewport_y + STATES_PANEL_HEIGHT - 7  # パネル上端からのHPバーの位置
        left_margin = self.viewport_x + 25  # 画面左からのHPとバーの位置
        top_hp_margin = hp_bar_margin - 23  # パネル上端からのHPの位置
        top_exp_margin = top_hp_margin - 15  # top_hp_marginからのEXPの位置

        # HP/MAXHPの表示
        hp_text = f"HP: {self.engine.player.fighter.hp}/{self.engine.player.fighter.max_hp}"

        arcade.draw_text(hp_text,
                         left_margin,
                         top_hp_margin,
                         color=COLORS["status_panel_text"],
                         font_size=hp_font_size
                         )
        # EXPの表示
        if self.engine.player.fighter.level < len(EXPERIENCE_PER_LEVEL):
            xp_to_next_level = EXPERIENCE_PER_LEVEL[self.engine.player.fighter.level - 1]
            exp_text = f"XP: {self.engine.player.fighter.current_xp} / {xp_to_next_level}"
        else:
            exp_text = f"XP: {self.engine.player.fighter.current_xp}"

        arcade.draw_text(exp_text,
                         left_margin,
                         top_exp_margin,
                         color=arcade.color.BAZAAR
                         )

        level_text = f"Level:{self.engine.player.fighter.level}"

        arcade.draw_text(level_text,
                         left_margin,
                         top_exp_margin - 20,
                         color=arcade.color.BITTERSWEET
                         )
        # HPバーの描画
        draw_status_bar(hp_bar_width / 2 + left_margin,
                        hp_bar_margin,
                        hp_bar_width,
                        hp_bar_height,
                        self.engine.player.fighter.hp,
                        self.engine.player.fighter.max_hp
                        )
    
    def draw_inventory(self):
        """インベントリの表示"""
        item_left_position = SCREEN_WIDTH / 2.3 # パネル左からの所持アイテム表示位置の調整に使う変数
        item_top_position = STATES_PANEL_HEIGHT - 22 # パネル上端からの所持アイテム表示位置の調整に使う変数
        separate_size = 1.5  # アイテム名の表示間隔の調整に使う変数
        margin = 3 # 選択したアイテムのアウトライン線の位置調整に使う変数
        item_font_size = 12
        outline_size = 2
        capacity = self.engine.player.inventory.capacity
        selected_item = self.engine.selected_item  # ボタン押下で選択したアイテムオブジェクト
        field_width = SCREEN_WIDTH / (capacity + 1) / separate_size  # アイテム表示感覚を決める変数

        # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
        for item in range(capacity):
            items_position = item * field_width + item_left_position  # パネル左からの所持アイテムの表示位置
            if item == selected_item:
                arcade.draw_lrtb_rectangle_outline(
                    items_position + self.viewport_x - margin,
                    items_position + self.viewport_x + field_width - margin,
                    item_top_position + item_font_size + self.viewport_y + margin*2,
                    item_top_position + self.viewport_y - margin,
                    arcade.color.BLACK, outline_size
                    )

            if self.engine.player.inventory.bag[item]:
                item_name = self.engine.player.inventory.bag[item].name
            else:
                item_name = ""

            text = f"{item+1}: {item_name}"

            arcade.draw_text(text,
                             items_position + self.viewport_x,
                             self.viewport_y + item_top_position,
                             color=COLORS["status_panel_text"],
                             font_size=item_font_size
                             )

    def draw_mouse_over_text(self):
        """マウスオーバー時のテキスト表示"""
        if self.mouse_over_text:
            x, y = self.mouse_position
            arcade.draw_xywh_rectangle_filled(x, y, 100, 16, arcade.color.BLACK)
            arcade.draw_text(self.mouse_over_text, x, y, arcade.color.WHITE)

    def draw_messages_handle(self):
        """メッセージ表示領域"""
        message_top_position = 19 # パネル上端からのメッセージ表示位置
        message_left_position = 125 # 画面左からのメッセージ表示位置
        left_position = SCREEN_WIDTH / 2.3
        margin = 3

        message_position = STATES_PANEL_HEIGHT - message_top_position
        arcade.draw_xywh_rectangle_filled(self.viewport_x + message_left_position - margin,
                                          self.viewport_y,
                                          left_position - message_left_position - margin,
                                          STATES_PANEL_HEIGHT,
                                          arcade.color.SHAMPOO
                                          )

        for message in self.engine.messages:
            arcade.draw_text(message,
                             message_left_position + self.viewport_x,
                             message_position + self.viewport_y,
                             color=COLORS["status_panel_text"])

            message_position -= message_top_position

    def draw_sprites_and_status_panel(self):
        """ 全てのスプライトリストとステータスパネルの表示 """
        self.engine.map_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.item_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.actor_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.chara_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.effect_sprites.draw()

        # 画面下のパネルをarcadeの四角形を描画する変数で作成
        arcade.draw_xywh_rectangle_filled(self.viewport_x,
                                          self.viewport_y,
                                          SCREEN_WIDTH,
                                          STATES_PANEL_HEIGHT,
                                          COLORS["status_panel_background"]
                                          )

    def draw_in_normal_state(self):
        """ノーマルステート時に描画する関数をまとめる"""
        self.draw_hp_and_status_bar()
        self.draw_inventory()
        self.draw_mouse_over_text()
        self.draw_messages_handle()

    def draw_select_mouse_location(self):
        """ マウス操作時のグリッド表示"""
        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            mouse_x, mouse_y = self.mouse_position
            grid_x, grid_y = pixel_to_grid(mouse_x, mouse_y)
            center_x, center_y = grid_to_pixel(grid_x, grid_y)
            arcade.draw_rectangle_outline(center_x,
                                          center_y,
                                          SPRITE_SIZE*SPRITE_SCALE,
                                          SPRITE_SIZE*SPRITE_SCALE,
                                          arcade.color.LIGHT_BLUE,
                                          border_width=2
                                          )

    def on_draw(self):
        try:
            arcade.start_render()

            # ビューポートの左と下の現在位置を変数に入れる、これはステータスパネルを画面に固定する為に使います
            self.viewport_x = arcade.get_viewport()[0]
            self.viewport_y = arcade.get_viewport()[2]

            self.draw_sprites_and_status_panel()

            # ノーマルステート時の画面表示
            if self.engine.game_state == GAME_STATE.NORMAL:
                self.draw_in_normal_state()
            
            # マウスセレクト時の画面表示
            elif self.engine.game_state == GAME_STATE.SELECT_LOCATION:
                self.draw_select_mouse_location()
                    
            if self.engine.fov_recompute:
                self.engine.fov()

        except Exception as e:
            print(e)

    def on_update(self, delta_time):
        self.engine.chara_sprites.update_animation()
        self.engine.chara_sprites.update()
        self.engine.actor_sprites.update_animation()
        self.engine.actor_sprites.update()
        self.engine.effect_sprites.update()

        self.engine.process_action_queue(delta_time)
        self.engine.player.check_experience_level(self.engine)
        self.engine.turn_change(delta_time)
        self.engine.check_for_player_movement(self.player_direction)

        # playerがmove状態の時だけviewportを計算する
        if self.engine.player.state == state.ON_MOVE:
            viewport(self.engine.player)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            arcade.close_window()
        elif key == arcade.key.ESCAPE:
            self.engine.game_state = GAME_STATE.NORMAL

        elif self.engine.player.state == state.READY and self.engine.game_state == GAME_STATE.NORMAL:
            direction = None
            if key in KEYMAP_UP:
                direction = (0, 1)
            elif key in KEYMAP_DOWN:
                direction = (0, -1)
            elif key in KEYMAP_LEFT:
                direction = (-1, 0)
            elif key in KEYMAP_RIGHT:
                direction = (1, 0)
            elif key in KEYMAP_UP_LEFT:
                direction = (-1, 1)
            elif key in KEYMAP_DOWN_LEFT:
                direction = (-1, -1)
            elif key in KEYMAP_UP_RIGHT:
                direction = (1, 1)
            elif key in KEYMAP_DOWN_RIGHT:
                direction = (1, -1)
            elif key in KEYMAP_REST:
                self.engine.player.state = state.TURN_END

            elif key in KEYMAP_PICKUP:
                self.engine.action_queue.extend([{"pickup": True}])
            elif key in KEYMAP_SELECT_ITEM_1:
                self.engine.action_queue.extend([{"select_item": 1}])
            elif key in KEYMAP_SELECT_ITEM_2:
                self.engine.action_queue.extend([{"select_item": 2}])
            elif key in KEYMAP_SELECT_ITEM_3:
                self.engine.action_queue.extend([{"select_item": 3}])
            elif key in KEYMAP_SELECT_ITEM_4:
                self.engine.action_queue.extend([{"select_item": 4}])
            elif key in KEYMAP_SELECT_ITEM_5:
                self.engine.action_queue.extend([{"select_item": 5}])
            elif key in KEYMAP_SELECT_ITEM_6:
                self.engine.action_queue.extend([{"select_item": 6}])
            elif key in KEYMAP_SELECT_ITEM_7:
                self.engine.action_queue.extend([{"select_item": 7}])
            elif key in KEYMAP_SELECT_ITEM_8:
                self.engine.action_queue.extend([{"select_item": 8}])
            elif key in KEYMAP_SELECT_ITEM_9:
                self.engine.action_queue.extend([{"select_item": 9}])
            elif key in KEYMAP_SELECT_ITEM_0:
                self.engine.action_queue.extend([{"select_item": 0}])
            elif key in KEYMAP_USE_ITEM:
                self.engine.action_queue.extend([{"use_item": True}])
            elif key in KEYMAP_DROP_ITEM:
                self.engine.action_queue.extend([{"drop_item": True}])
            elif key in KEYMAP_USE_STAIRS:
                self.engine.action_queue.extend([{"use_stairs": True}])

            elif key == arcade.key.P:
                self.save()
            elif key == arcade.key.L:
                self.load()

            elif key == arcade.key.SPACE:
                self.engine.game_state = GAME_STATE.SELECT_LOCATION

            self.player_direction = direction


    def on_key_release(self, key, modifiers):
        self.player_direction = None

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = x + self.viewport_x, y + self.viewport_y
        # 忘れずにビューポートの座標を足す
        actor_list = arcade.get_sprites_at_point(
            self.mouse_position, self.engine.actor_sprites)
        item_list = arcade.get_sprites_at_point(
            self.mouse_position, self.engine.item_sprites)
        self.mouse_over_text = None
        for actor in chain(actor_list, item_list):
            if actor.fighter and actor.is_visible:
                self.mouse_over_text = f"{actor.name} {actor.fighter.hp}/{actor.fighter.max_hp}"
            elif actor.name:
                self.mouse_over_text = f"{actor.name}"

    def on_mouse_press(self, x, y, button, modifiers):
        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            grid_x, grid_y = pixel_to_grid(x + self.viewport_x, y + self.viewport_y)
            self.engine.grid_click(grid_x, grid_y)
        self.engine.game_state = GAME_STATE.NORMAL

    def save(self):
        print("save")
        game_dict = self.engine.get_dict()
        # print(game_dict)

        with open("game_save.json", "w") as write_file:
            json.dump(game_dict, write_file, indent=4, sort_keys=True)
        print("**save**")

    def load(self):
        print("load")
        with open("game_save.json", "r") as read_file:
            data = json.load(read_file)

        # print(data)
        print("**load**")
        self.engine.restore_from_dict(data)
        self.engine.player.state = state.READY
        self.engine.fov_recompute = True
        self.engine.viewport(self.engine.player)


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
