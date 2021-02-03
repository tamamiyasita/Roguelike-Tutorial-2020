

from data import IMAGE_ID
import arcade
from constants import *
from itertools import chain


class NormalUI:
    """GameState=Normal時に描画するUI
    """

    def __init__(self, engine, viewport, selected_item, messages, mouse_position):
        self.engine = engine
        self.player = engine.player
        self.viewport_left = viewport[0]
        self.viewport_right = viewport[1]
        self.viewport_bottom = viewport[2]
        self.viewport_top = viewport[3]

        self.selected_item = selected_item
        self.messages = messages
        self.mouse_position = mouse_position
        self.panel_line_width = 1
        self.side_panel_height = SCREEN_HEIGHT - GRID_SIZE*3
        self.side_panel_width = SCREEN_WIDTH - STATES_PANEL_WIDTH


    def draw_in_normal_state(self):
        """mainに渡すメソッドをまとめる"""
        self.panel_ui()
        self.draw_hp_and_status_bar()
        self.draw_active_skill()
        self.draw_messages_handle()
        self.draw_passive_skill()
        self.draw_status_icons()

    def draw_status_icons(self):
        y = GRID_SIZE+5
        icon_pos_x = self.viewport_right - (GRID_SIZE*4.5)
        icon_pos_y = self.viewport_top - (GRID_SIZE * 6)
        for i in range(len(self.player.fighter.states)):
            icon = self.player.fighter.states[i].icon[0]
            # arcade.draw_scaled_texture_rectangle(
            #         center_x=icon_pos_x,
            #         center_y=icon_pos_y + y,
            #         texture=icon,
            #         scale=4
            # )
            arcade.draw_texture_rectangle(
                    center_x=icon_pos_x,
                    center_y=icon_pos_y + y,
                    width=155,
                    height=155,
                    texture=icon
                    )
            y += y


    def panel_ui(self):
        # 画面下のパネルをarcadeの四角形を描画する変数で作成
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left,
            bottom_left_y=self.viewport_bottom,
            width=self.side_panel_width,
            height=STATES_PANEL_HEIGHT,
            color=(255,255,255,0)#COLORS["status_panel_background"]
        )


        # 画面横のパネル
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left + SCREEN_WIDTH - STATES_PANEL_WIDTH,
            bottom_left_y=self.viewport_bottom,
            width=STATES_PANEL_WIDTH,
            height=self.side_panel_height,
            color=(25,25,55,255)
        )

       # 横パネルの周りの線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_left + SCREEN_WIDTH -
            STATES_PANEL_WIDTH + self.panel_line_width*0.5,
            bottom_left_y=self.viewport_bottom + self.panel_line_width*0.5,
            width=STATES_PANEL_WIDTH - self.panel_line_width,
            height=self.side_panel_height-3,
            color=arcade.color.LEMON_CHIFFON,
            border_width=self.panel_line_width
        )
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left + SCREEN_WIDTH - STATES_PANEL_WIDTH,
            bottom_left_y=self.viewport_top - GRID_SIZE*3,
            width=STATES_PANEL_WIDTH,
            height=GRID_SIZE*3,
            color=arcade.color.BLACK
        )

        # ミニマップ囲い線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_left + SCREEN_WIDTH -
            STATES_PANEL_WIDTH + self.panel_line_width*0.5,
            bottom_left_y=self.viewport_top - GRID_SIZE*3,
            width=STATES_PANEL_WIDTH - self.panel_line_width,
            height=GRID_SIZE*3,
            color=arcade.color.BABY_BLUE,
            border_width=self.panel_line_width
        )

    def draw_hp_and_status_bar(self):
        """ステータスパネルとHPバー"""
        # パネル用変数
        hp_font_size = 15
        hp_bar_width = hp_font_size * 12  # HPバーの幅
        hp_bar_height = hp_font_size + 2  # HPバーの太さ
        hp_bar_margin = self.viewport_bottom + self.side_panel_height - 55  # 15パネル上端からのHPバーの位置
        left_margin = self.viewport_left + self.side_panel_width + 7  # 画面左からのHPとバーの位置

        Player_attr = f"{self.player.race} {self.player.name}"

        arcade.draw_text(text=Player_attr,
                         start_x=left_margin,
                         start_y=hp_bar_margin+25,
                         color=(132,255,142),
                         font_size=hp_font_size+1,
                         font_name=UI_FONT

                         )

        # HP/MAXHPの表示
        hp_text = f"HP {self.player.fighter.hp: >2}/{self.player.fighter.max_hp}"

        arcade.draw_text(text=hp_text,
                         start_x=left_margin,
                         start_y=hp_bar_margin-25,
                         color=COLORS["status_panel_text"],
                         font_size=hp_font_size,
                         font_name=UI_FONT

                         )

        # EXPの表示
        if self.player.fighter.level < len(self.player.experience_per_level):
            xp_to_next_level = self.player.experience_per_level[self.player.fighter.level+1]
            exp_text = f"XP {self.player.fighter.current_xp: >4} / {xp_to_next_level: >4}"
        else:
            exp_text = f"XP {self.player.fighter.current_xp}"

        arcade.draw_text(text=exp_text,
                         start_x=left_margin+2,
                         start_y=hp_bar_margin+4,
                         color=arcade.color.BABY_BLUE_EYES,
                         font_size=13
                         )
        # EXPバーの描画
        draw_status_bar(center_x=left_margin+168,
                        center_y=hp_bar_margin+12,
                        width=140,
                        height=7,
                        current_value=self.player.fighter.current_xp,
                        max_value=xp_to_next_level,
                        front_color=arcade.color.BABY_BLUE_EYES,
                        bac_color=(100,100,100,100)
                        )

        # レベルの表示
        level_text = f"Level {self.player.fighter.level}"

        arcade.draw_text(text=level_text,
                         start_x=left_margin+140,
                         start_y=hp_bar_margin+25,
                         color=(252,248,151),
                         font_size=15,
                         font_name=UI_FONT
                         )

        # HPバーの描画
        draw_status_bar(center_x=hp_bar_width / 2 + left_margin+74,
                        center_y=hp_bar_margin-14,
                        width=hp_bar_width-28,
                        height=hp_bar_height,
                        current_value=self.player.fighter.hp,
                        max_value=self.player.fighter.max_hp
                        )

        # <passive skill>        
        arcade.draw_text(text="<Passive Skill>",
                         start_x=left_margin+5,
                         start_y=hp_bar_margin-50,
                         color=(252,248,151),
                         font_size=12,
                         font_name=UI_FONT
                         )

    def draw_active_skill(self):
        """スキルアイコンの表示"""
        slot_len = len(self.player.fighter.active_skill)
        item_left_position = self.viewport_left + GRID_SIZE*7
            # ((SCREEN_WIDTH-STATES_PANEL_WIDTH) / 2.4)   # パネル左からの所持アイテム表示位置の調整に使う変数
        skill_top_position = self.viewport_bottom + GRID_SIZE*1.7
            # STATES_PANEL_HEIGHT + 12  # パネル上端からの所持アイテム表示位置の調整に使う変数
        separate_size = 4.5  # スキル名の表示間隔の調整に使う変数
        item_font_size = 11
        field_width = SCREEN_WIDTH / (slot_len + 1) / separate_size  # アイテム表示感覚を決める変数

        # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
        # TODO 複数行にする処理を考える（５回ループしたら縦と横の変数に増減するなど）
        for i, skill in enumerate(self.player.fighter.active_skill):
            skill.owner = self.player
            skill_position = i * field_width + item_left_position  # 左からの所持skillの表示位置

            key_number = f"<key {i+1}>"


            # スキルアイコンの描画
            arcade.draw_texture_rectangle(
                center_x=skill_position+10,
                center_y=skill_top_position-10,
                width=64,
                height=64,
                texture=skill.icon
            )
            # アイコンに白幕をかけクールダウンタイム表示
            if 0 < skill.data["count_time"]:
                arcade.draw_texture_rectangle(
                    center_x=skill_position+10,
                    center_y=skill_top_position-10,
                    width=64,
                    height=64,
                    texture=IMAGE_ID["cool_down"],
                    alpha=200
                )
                arcade.draw_text(
                    text=str(skill.data["count_time"]),
                    start_x=skill_position + 10,
                    start_y=skill_top_position - 10,
                    color=arcade.color.DARK_BLUE,
                    font_size=27,
                    anchor_x="center",
                    anchor_y="center"
                )
            else:
                arcade.draw_text(
                    text=key_number,
                    start_x=skill_position-13,
                    start_y=skill_top_position-67,
                    color=arcade.color.YELLOW_ORANGE,
                    font_size=item_font_size
                )

            arcade.draw_text(
                text=f"level {skill.level}",
                start_x=skill_position-11,
                start_y=skill_top_position-55,
                color=COLORS["status_panel_text"],
                font_size=item_font_size
            )

    def draw_passive_skill(self):
        """スキルアイコン及びステータスを右パネルに描画する"""
        item_row = self.viewport_top - GRID_SIZE*5#(SCREEN_HEIGHT //1.3) - 320 # 行の最上段
        item_font_size = 17
        item_text = ""
        left_margin = self.viewport_left + self.side_panel_width + 7  # 画面左からのHPとバーの位置
        y = 0

        # try:
        #     if self.player.fighter.data["weapon"] in self.player.fighter.switch_off_skills:
        #         self.engine.cur_level.equip_sprites.remove(self.player.fighter.data["weapon"])
        # except:
        #     pass
        
        for passive in self.player.fighter.passive_skill:

            # if passive in self.player.fighter.switch_off_skills:
            #     passive.remove_from_sprite_lists()
                # self.engine.cur_level.equip_sprites.remove(passive)

            if passive not in self.engine.cur_level.equip_sprites:
                self.engine.cur_level.equip_sprites.append(passive)

            item_text = f"{passive.name} (level {passive.level})".replace("_", " ").title()


            arcade.draw_text(
                text=item_text,
                start_x=left_margin,
                start_y=item_row + y,
                color=arcade.color.ARYLIDE_YELLOW,
                font_size=item_font_size-3,
                # font_name="consola.ttf"
            )

            arcade.draw_texture_rectangle(
                center_x=left_margin+25,
                center_y=item_row + y-25,
                width=40,
                height=40,
                texture=passive.icon
            )
                
            arcade.draw_text(
                text=f"{passive.explanatory_text}",
                start_x=left_margin +55,
                start_y=item_row + y-6,
                color=arcade.color.WHITE,
                font_size=item_font_size-4,
                # font_name="consola.ttf",
                anchor_y="top"
            )


            y -= 104        




    def draw_messages_handle(self):
        """メッセージ表示領域"""
        margin = 3
        message_top_position = 20  # パネル上端からのメッセージ表示位置
        message_left_position = self.viewport_left - margin + 20  # 画面左からのメッセージ表示位置
        message_first_position = self.viewport_bottom + 165# STATES_PANEL_HEIGHT - message_top_position  # 最初の行


        c = 255
        for message in list(reversed(self.messages)):
            arcade.draw_text(
                text=message,
                start_x=message_left_position,
                start_y=message_first_position,
                color=(255,255,255,c),
                font_size=16
            )
            c -= 20 # 行ごとに文字列を減色させる

            # 文字送り
            message_first_position -= message_top_position


def draw_status_bar(center_x, center_y, width, height, current_value, max_value, front_color=(255,103,123), bac_color=(255,255,255,255)):
    """ステータスバーの実体"""
    arcade.draw_rectangle_filled(
        center_x, center_y, width, height, color=bac_color)

    states_width = (current_value / max_value) * width

    arcade.draw_rectangle_filled(center_x - (width / 2 - states_width / 2),
                                 center_y, states_width, height, color=front_color)

