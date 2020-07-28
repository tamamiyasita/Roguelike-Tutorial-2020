from os import write
import arcade
import json
from arcade.arcade_types import Point
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
        self.viewport_x = 0
        self.viewport_y = 0

        self.character_sheet_buttons = arcade.SpriteList()

    def setup(self):
        self.engine.setup()
        viewport(self.engine.player)


        spacing = 37
        sheet_y = self.viewport_y + SCREEN_HEIGHT - 75
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_x + 200
        button.center_y = sheet_y
        button.name = "Attack"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_x + 200
        button.center_y = sheet_y
        button.name = "Defense"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_x + 200
        button.center_y = sheet_y
        button.name = "HP"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_x + 200
        button.center_y = sheet_y
        button.name = "Capacity"
        self.character_sheet_buttons.append(button)


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

        arcade.draw_text(text=hp_text,
                         start_x=left_margin,
                         start_y=top_hp_margin,
                         color=COLORS["status_panel_text"],
                         font_size=hp_font_size
                         )

        # EXPの表示
        if self.engine.player.fighter.level < len(EXPERIENCE_PER_LEVEL):
            xp_to_next_level = EXPERIENCE_PER_LEVEL[self.engine.player.fighter.level - 1]
            exp_text = f"XP: {self.engine.player.fighter.current_xp} / {xp_to_next_level}"
        else:
            exp_text = f"XP: {self.engine.player.fighter.current_xp}"

        arcade.draw_text(text=exp_text,
                         start_x=left_margin,
                         start_y=top_exp_margin,
                         color=arcade.color.BAZAAR
                         )

        # レベルの表示
        level_text = f"Level:{self.engine.player.fighter.level}"

        arcade.draw_text(text=level_text,
                         start_x=left_margin,
                         start_y=top_exp_margin - 20,
                         color=arcade.color.BITTERSWEET
                         )

        # HPバーの描画
        draw_status_bar(center_x=hp_bar_width / 2 + left_margin,
                        center_y=hp_bar_margin,
                        width=hp_bar_width,
                        height=hp_bar_height,
                        current_value=self.engine.player.fighter.hp,
                        max_value=self.engine.player.fighter.max_hp
                        )
    
    def draw_inventory(self):
        """インベントリの表示"""
        item_left_position = self.viewport_x + SCREEN_WIDTH / 2.3 # パネル左からの所持アイテム表示位置の調整に使う変数
        item_top_position = self.viewport_y + STATES_PANEL_HEIGHT - 22 # パネル上端からの所持アイテム表示位置の調整に使う変数
        separate_size = 1.5  # アイテム名の表示間隔の調整に使う変数
        margin = 3 # 選択したアイテムのアウトライン線の位置調整に使う変数
        item_font_size = 12
        outline_size = 2
        capacity = self.engine.player.inventory.capacity
        selected_item = self.engine.selected_item  # ボタン押下で選択したアイテムオブジェクト
        field_width = SCREEN_WIDTH / (capacity + 1) / separate_size  # アイテム表示感覚を決める変数

        # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
        # TODO 複数行にする処理を考える（５回ループしたら縦と横の変数に増減するなど）
        for item in range(capacity):
            items_position = item * field_width + item_left_position  # パネル左からの所持アイテムの表示位置
            if item == selected_item:
                arcade.draw_lrtb_rectangle_outline(
                        left=items_position - margin,
                        right=items_position + field_width - margin,
                        top=item_top_position + item_font_size + margin*2,
                        bottom=item_top_position - margin,
                        color=arcade.color.BLACK,
                        border_width=outline_size
                        )

            if self.engine.player.inventory.bag[item]:
                item_name = self.engine.player.inventory.bag[item].name
            else:
                item_name = ""

            item_text = f"{item+1}: {item_name}"

            arcade.draw_text(
                        text=item_text,
                        start_x=items_position,
                        start_y=item_top_position,
                        color=COLORS["status_panel_text"],
                        font_size=item_font_size
                        )

    def draw_mouse_over_text(self):
        """マウスオーバー時のオブジェクト名表示"""
        if self.mouse_over_text:
            x, y = self.mouse_position
            back_ground_width = 100 # テキスト背景幅
            back_ground_height = 16 # テキスト背景高

            arcade.draw_xywh_rectangle_filled(
                        bottom_left_x=x,
                        bottom_left_y=y,
                        width=back_ground_width,
                        height=back_ground_height,
                        color=arcade.color.BLACK
                        )
            arcade.draw_text(
                        text=self.mouse_over_text,
                        start_x=x,
                        start_y=y,
                        color=arcade.color.WHITE
                        )

    def draw_messages_handle(self):
        """メッセージ表示領域"""
        margin = 3
        message_top_position = 19 # パネル上端からのメッセージ表示位置
        message_left_position = self.viewport_x -margin + 125 # 画面左からのメッセージ表示位置
        message_panel_width = (SCREEN_WIDTH / 2.3) - 125 - margin # メッセージパネル幅
        message_panel_height = STATES_PANEL_HEIGHT # メッセージパネル高
        message_first_position = self.viewport_y + STATES_PANEL_HEIGHT - message_top_position # 最初の行
        
        arcade.draw_xywh_rectangle_filled(
                        bottom_left_x=message_left_position,
                        bottom_left_y=self.viewport_y,
                        width=message_panel_width,
                        height=message_panel_height,
                        color=arcade.color.SHAMPOO
                        )

        for message in self.engine.messages:
            arcade.draw_text(
                        text=message,
                        start_x=message_left_position,
                        start_y=message_first_position,
                        color=COLORS["status_panel_text"]
                        )

            # 文字送り
            message_first_position -= message_top_position

    def draw_sprites_and_status_panel(self):
        """ 全てのスプライトリストとステータスパネルの表示 """
        self.engine.cur_level.map_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.item_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.actor_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.chara_sprites.draw(filter=gl.GL_NEAREST)
        self.engine.cur_level.effect_sprites.draw()

        # 画面下のパネルをarcadeの四角形を描画する変数で作成
        arcade.draw_xywh_rectangle_filled(
                        bottom_left_x=self.viewport_x,
                        bottom_left_y=self.viewport_y,
                        width=SCREEN_WIDTH,
                        height=STATES_PANEL_HEIGHT,
                        color=COLORS["status_panel_background"]
                        )


    def draw_in_normal_state(self):
        """ノーマルステート時に描画する関数をまとめる"""
        self.draw_hp_and_status_bar()
        self.draw_inventory()
        self.draw_mouse_over_text()
        self.draw_messages_handle()

    def draw_select_mouse_location(self):
        """ マウス操作時のグリッド表示"""

        # マウスが画面外ならNoneを返す
        if self.mouse_position is None:
            return

        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            mouse_x, mouse_y = self.mouse_position
            grid_x, grid_y = pixel_to_grid(mouse_x, mouse_y)
            center_x, center_y = grid_to_pixel(grid_x, grid_y)

            arcade.draw_rectangle_outline(
                        center_x=center_x,
                        center_y=center_y,
                        width=SPRITE_SIZE*SPRITE_SCALE,
                        height=SPRITE_SIZE*SPRITE_SCALE,
                        color=arcade.color.LIGHT_BLUE,
                        border_width=2
                        )

    def character_screen_click(self, x, y):
        if self.engine.player.fighter.ability_points > 0:
            buttons_clicked = arcade.get_sprites_at_point(
                        point=(x, y),
                        sprite_list=self.character_sheet_buttons
                        )
            for buttons in buttons_clicked:
                if buttons.name == "Attack":
                    self.engine.player.fighter.power += 1
                    self.engine.player.fighter.ability_points -= 1
                elif buttons.name == "Defense":
                    self.engine.player.fighter.defense += 1
                    self.engine.player.fighter.ability_points -= 1
                elif buttons.name == "HP":
                    self.engine.player.fighter.hp += 15
                    self.engine.player.fighter.max_hp += 15
                    self.engine.player.fighter.ability_points -= 1
                elif buttons.name == "Capacity":
                    self.engine.player.fighter.gp += 5
                    self.engine.player.fighter.ability_points -= 1



    def draw_character_screen(self):
        arcade.draw_xywh_rectangle_filled(
                        bottom_left_x=0+self.viewport_x,
                        bottom_left_y=0+self.viewport_y,
                        width=SCREEN_WIDTH,
                        height=SCREEN_HEIGHT,
                        color=COLORS["status_panel_background"]
                        )

        spacing = 1.8
        text_position_y = SCREEN_HEIGHT - 50 + self.viewport_y
        text_position_x = 10 + self.viewport_x

        text_size = 24
        screen_title = "Character Screen"
        arcade.draw_text(
                        text=screen_title,
                        start_x=text_position_x,
                        start_y=text_position_y,
                        color=arcade.color.AFRICAN_VIOLET,
                        font_size=text_size
                        )

        text_position_y -= text_size * spacing
        text_size = 20
        states_text = f"Attack: {self.engine.player.fighter.power}"
        arcade.draw_text(
                        text=states_text,
                        start_x=text_position_x,
                        start_y=text_position_y,
                        color=arcade.color.AFRICAN_VIOLET,
                        font_size=text_size
                        )

        text_position_y -= text_size * spacing
        states_text = f"Defense: {self.engine.player.fighter.defense}"
        arcade.draw_text(
                        text=states_text,
                        start_x=text_position_x,
                        start_y=text_position_y,
                        color=arcade.color.AFRICAN_VIOLET,
                        font_size=text_size
                        )

        text_position_y -= text_size * spacing
        states_text = f"HP: {self.engine.player.fighter.hp} / {self.engine.player.fighter.max_hp}"
        arcade.draw_text(
                        text=states_text,
                        start_x=text_position_x,
                        start_y=text_position_y,
                        color=arcade.color.AFRICAN_VIOLET,
                        font_size=text_size
                        )

        text_position_y -= text_size * spacing
        states_text = f"Max Inventory: {self.engine.player.inventory.capacity}"
        arcade.draw_text(
                        text=states_text,
                        start_x=text_position_x,
                        start_y=text_position_y,
                        color=arcade.color.AFRICAN_VIOLET,
                        font_size=text_size
                        )

        text_position_y -= text_size * spacing
        states_text = f"Level: {self.engine.player.fighter.level}"
        arcade.draw_text(
                        text=states_text,
                        start_x=text_position_x,
                        start_y=text_position_y,
                        color=arcade.color.AFRICAN_VIOLET,
                        font_size=text_size
                        )
    
    def draw_button(self):
        self.character_sheet_buttons = arcade.SpriteList()

        spacing = 37
        sheet_y = self.viewport_y + SCREEN_HEIGHT - 75
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_x + 200
        button.center_y = sheet_y
        button.name = "Attack"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_x + 200
        button.center_y = sheet_y
        button.name = "Defense"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_x + 200
        button.center_y = sheet_y
        button.name = "HP"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_x + 200
        button.center_y = sheet_y
        button.name = "Capacity"
        self.character_sheet_buttons.append(button)


        
        if self.engine.player.fighter.ability_points > 0:
            self.character_sheet_buttons.draw()


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

            # Character_Screen表示
            elif self.engine.game_state == GAME_STATE.CHARACTER_SCREEN:
                self.draw_character_screen()
                self.draw_button()
            
            # fov_recomputeがTruならfov計算
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

        elif key in KEYMAP_CHARACTER_SCREEN:
            self.engine.game_state = GAME_STATE.CHARACTER_SCREEN

        elif key in KEYMAP_CANCEL:
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


            self.player_direction = direction


    def on_key_release(self, key, modifiers):
        self.player_direction = None

    def on_mouse_motion(self, x, y, dx, dy):
        """マウスオーバー処理"""

        # 忘れずにビューポートの座標を足す
        self.mouse_position = x + self.viewport_x, y + self.viewport_y

        # マウスオーバー時に表示するスプライトリストの取得
        actor_list = arcade.get_sprites_at_point(
                        point=self.mouse_position,
                        sprite_list=self.engine.cur_level.actor_sprites
                        )
        item_list = arcade.get_sprites_at_point(
                        point=self.mouse_position,
                        sprite_list=self.engine.cur_level.item_sprites
                        )

        self.mouse_over_text = None
        for actor in chain(actor_list, item_list):
            if actor.fighter and actor.is_visible:
                self.mouse_over_text = f"{actor.name} {actor.fighter.hp}/{actor.fighter.max_hp}"
            elif actor.name:
                self.mouse_over_text = f"{actor.name}"

    def on_mouse_press(self, x, y, button, modifiers):
        """engineのgrid_clickに渡されるマウスボタン処理"""
        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            grid_x, grid_y = pixel_to_grid(x + self.viewport_x, y + self.viewport_y)
            self.engine.grid_click(grid_x, grid_y)
            self.engine.game_state = GAME_STATE.NORMAL
        
        if self.engine.game_state == GAME_STATE.CHARACTER_SCREEN:
            self.character_screen_click(x+self.viewport_x, y+self.viewport_y)

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
