

from data import IMAGE_ID
import arcade
from constants import *
from itertools import chain


class NormalUI:
    """GameState=Normal時に描画するUI
    """

    def __init__(self, engine):
        self.engine = engine
        self.player = engine.player

        self.messages = engine.messages
        self.panel_line_width = 1


    def draw_in_normal_state(self, viewport):
        """mainに渡すメソッドをまとめる"""

        self.viewport_left = viewport[0]
        self.viewport_right = viewport[1]
        self.viewport_bottom = viewport[2]
        self.viewport_top = viewport[3]
        self.side_panel_height = SCREEN_HEIGHT - GRID_SIZE*3
        self.side_panel_width = SCREEN_WIDTH - STATES_PANEL_WIDTH
        self.side_panel_x_line = self.viewport_left + SCREEN_WIDTH - STATES_PANEL_WIDTH-15
        self.side_panel_y_line = self.viewport_bottom+GRID_SIZE*3+6

        self.active_panel_line = self.viewport_left+(GRID_SIZE*6)+7
        self.passive_panel_line = self.active_panel_line+(GRID_SIZE*5)-11
        self.states_panel_line =  self.passive_panel_line+GRID_SIZE*2-28
        self.skill_panel_height = (GRID_SIZE*3)-10

        self.a_skill_left_position = self.active_panel_line+37
        self.p_skill_left_position = self.passive_panel_line+37
        self.panel_top_position = self.viewport_bottom + self.skill_panel_height
        self.skill_top_position = self.panel_top_position - 45
        self.separate_size=3.57
        self.field_width = SCREEN_WIDTH / 6 / self.separate_size  # アイテム表示感覚を決める変数
        self.item_font_size = 11

        self.text_level = self.skill_top_position-35

        self.panel_ui()
        self.draw_hp_and_status_bar()
        self.draw_active_skill()
        self.draw_messages_handle()
        self.draw_passive_skill()
        self.draw_status_icons()


    def draw_status_icons(self):
        y = 0
        x = 34
        icon_pos_x = self.states_panel_line
        icon_pos_y = self.side_panel_y_line+self.skill_panel_height-32
        if self.player.fighter.states:
             # 状態変化枠背景
            arcade.draw_xywh_rectangle_filled(
                bottom_left_x=self.states_panel_line,
                bottom_left_y=self.side_panel_y_line,
                width=STATES_PANEL_WIDTH+10,
                height=self.skill_panel_height+3,
                color=(25,25,25,55)
            )
            # 状態変化ステータス枠
            arcade.draw_xywh_rectangle_outline(
                bottom_left_x=self.states_panel_line,
                bottom_left_y=self.side_panel_y_line,
                width=STATES_PANEL_WIDTH+10,
                height=self.skill_panel_height+3,
                color=arcade.color.YELLOW_ROSE,
                border_width=self.panel_line_width
            )
        for i in range(len(self.player.fighter.states)):
            icon = self.player.fighter.states[i].icon[0]

            arcade.draw_texture_rectangle(
                center_x=icon_pos_x + x,
                center_y=icon_pos_y + y,
                width=40,
                height=40,
                texture=IMAGE_ID["black_board"]
            )
            arcade.draw_texture_rectangle(
                    center_x=icon_pos_x + x,
                    center_y=icon_pos_y + y,
                    width=40,
                    height=40,
                    texture=icon
                    )
            if i < 2:
                x += GRID_SIZE
            elif i == 2:
                x = 34
                y -= 58
            elif i < 5:
                x += GRID_SIZE
            elif i == 5:
                x = 34
                y -= 58
            elif i < 9:
                x += GRID_SIZE


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
            bottom_left_x=self.side_panel_x_line,
            bottom_left_y=self.side_panel_y_line,
            width=STATES_PANEL_WIDTH+8,
            height=self.side_panel_height-16,
            color=(25,25,55,55)
        )

       # 横パネルの周りの線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.side_panel_x_line,
            bottom_left_y=self.side_panel_y_line,
            width=STATES_PANEL_WIDTH + 8,
            height=self.side_panel_height-14,
            color=(255,129,128),
            border_width=self.panel_line_width
        )
        # アクティブスキルアイコン枠
        d = 14
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.active_panel_line,
            bottom_left_y=self.viewport_bottom+8,
            width=(SCREEN_WIDTH-(GRID_SIZE*10))/2 +d,
            height=self.skill_panel_height,
            color=arcade.color.ORANGE,
            border_width=self.panel_line_width
        )
        # パッシブスキルアイコン枠
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.passive_panel_line,
            bottom_left_y=self.viewport_bottom+8,
            width=(SCREEN_WIDTH-(GRID_SIZE*10))/2 +d,
            height=self.skill_panel_height,
            color=arcade.color.BABY_BLUE,
            border_width=self.panel_line_width
        )
        # メッセージパネル枠
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_left+8,
            bottom_left_y=self.viewport_bottom+8,
            width=GRID_SIZE*6-8,
            height=self.skill_panel_height,
            color=arcade.color.WHITE_SMOKE,
            border_width=self.panel_line_width
        )



        # ミニマップ黒背景
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.side_panel_x_line,
            bottom_left_y=self.viewport_bottom+8,
            width=STATES_PANEL_WIDTH+8,
            height=self.skill_panel_height,
            color=arcade.color.BLACK
        )
        # ミニマップ囲い線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.side_panel_x_line,
            bottom_left_y=self.viewport_bottom+8,
            width=STATES_PANEL_WIDTH+8,
            height=self.skill_panel_height,
            color=arcade.color.GO_GREEN,
            border_width=self.panel_line_width
        )

    def draw_hp_and_status_bar(self):
        """ステータスパネルとHPバー"""
        # パネル用変数
        hp_font_size = 15
        hp_bar_width = 180  # HPバーの幅
        hp_bar_height = hp_font_size + 4  # HPバーの太さ
        hp_bar_margin = self.viewport_top -35  # 15パネル上端からのHPバーの位置
        left_margin = self.viewport_left + self.side_panel_width-5  # 画面左からのHPとバーの位置

        Player_attr = f"{self.player.race} {self.player.name}"

        arcade.draw_text(text=Player_attr,
                         start_x=left_margin,
                         start_y=hp_bar_margin,
                         color=(132,255,142),
                         font_size=hp_font_size,
                         font_name=UI_FONT

                         )


        # HPの表示
        hp_text = f"HP {self.player.fighter.hp: >2}/{self.player.fighter.max_hp}"
        # HPバーの描画 割合で色を変化させる
        c = 255
        h = 255-int(127*((self.player.fighter.hp)/self.player.fighter.max_hp))
        if h >= 55:
            c = int(255*(self.player.fighter.hp/self.player.fighter.max_hp))
        hp_color = (h,c,60,150)
        front_color=hp_color

        draw_status_bar(start_x=left_margin,
                        start_y=hp_bar_margin-61,
                        width=hp_bar_width,
                        height=hp_bar_height,
                        current_value=self.player.fighter.hp,
                        front_color=front_color,
                        max_value=self.player.fighter.max_hp
                        )

        arcade.draw_text(text=hp_text,
                         start_x=left_margin+3,
                         start_y=hp_bar_margin-62,
                         color=(c,255,255),
                         font_size=hp_font_size,
                         font_name=UI_FONT2

                         )

        # EXPの表示
        if self.player.fighter.level < len(self.player.experience_per_level):
            xp_to_next_level = self.player.experience_per_level[self.player.fighter.level+1]
            exp_text = f"XP {self.player.fighter.current_xp: >4} / {xp_to_next_level: >4}"
        else:
            exp_text = f"XP {self.player.fighter.current_xp}"

        # EXPバーの描画
        draw_status_bar(start_x=left_margin,
                        start_y=hp_bar_margin-36,
                        width=hp_bar_width,
                        height=15,
                        current_value=self.player.fighter.current_xp,
                        max_value=xp_to_next_level,
                        front_color=(71,130,239),
                        bac_color=(180,180,180,140)
                        )
        arcade.draw_text(text=exp_text,
                         start_x=left_margin+3,
                         start_y=hp_bar_margin-38,
                         color=(239,192,70),
                         font_size=13,
                         font_name=UI_FONT2
                         )

        # レベルの表示
        level_text = f"Level {self.player.fighter.level}"

        arcade.draw_text(text=level_text,
                         start_x=left_margin+3,
                         start_y=hp_bar_margin-18,
                         color=(252,248,151),
                         font_size=13,
                         font_name=UI_FONT
                         )
        self.flower_icons()

    def flower_icons(self):
        flower_x_position = self.side_panel_x_line+10
        flower_y_position = self.viewport_top - GRID_SIZE * 2 + 20
        y = 75

        arcade.draw_text(
            "[Flowers]",
            flower_x_position-4,
            flower_y_position - 14,
            (255,129,128),
            12,
            font_name=UI_FONT
        )



        for i, flower in enumerate(self.player.equipment.flower_slot):
            # アイコン背景
            arcade.draw_lrwh_rectangle_textured(
                bottom_left_x=flower_x_position,
                bottom_left_y=flower_y_position - y,
                width=40,
                height=40,
                texture=IMAGE_ID["black_board"]
            )

            # flower_icon 描画
            # arcade.draw_texture_rectangle(
            #     center_x=flower_x_position,
            #     center_y=flower_y_position,
            #     width=40,
            #     height=40,
            #     texture=flower.icon
            # )

            # アイコン（仮）
            arcade.draw_xywh_rectangle_filled(
                flower_x_position,
                flower_y_position-y,
                20,
                20,
                (200,150,200)
            )
            arcade.draw_text(
                f"{flower.name}".replace("_", " ").title(),
                flower_x_position,
                flower_y_position+41-y,
                (255,255,255),
                11,
                font_name=UI_FONT
            )
            # HPの表示
            hp_text = f"HP {flower.hp: >2}/{flower.max_hp}"
            # HPバーの描画 割合で色を変化させる
            c = 255
            h = 255-int(127*((flower.hp)/flower.max_hp))
            if h >= 55:
                c = int(255*(flower.hp/flower.max_hp))
            hp_color = (h,c,60,150)
            front_color=hp_color

            draw_status_bar(start_x=flower_x_position+50,
                            start_y=flower_y_position+1-y,
                            width=100,
                            height=13,
                            current_value=flower.hp,
                            front_color=front_color,
                            max_value=flower.max_hp
                            )

            arcade.draw_text(text=hp_text,
                            start_x=flower_x_position+52,
                            start_y=flower_y_position-y,
                            color=(c,255,255),
                            font_size=10,
                            font_name=UI_FONT
                            )


            # EXPの表示
            if flower.level < len(flower.experience_per_level):
                xp_to_next_level = flower.experience_per_level[flower.level+1]
                exp_text = f"XP {flower.current_xp: >4} / {xp_to_next_level: >4}"
            else:
                exp_text = f"XP {flower.current_xp}"

            # EXPバーの描画
            draw_status_bar(start_x=flower_x_position+50,
                            start_y=flower_y_position+18-y,
                            width=100,
                            height=11,
                            current_value=flower.current_xp,
                            max_value=xp_to_next_level,
                            front_color=(71,130,239),
                            bac_color=(180,180,180,140)
                            )
            arcade.draw_text(text=exp_text,
                            start_x=flower_x_position+52,
                            start_y=flower_y_position+17-y,
                            color=(239,192,70),
                            font_size=9,
                            font_name=UI_FONT2
                            )

            # レベルの表示
            level_text = f"Level {flower.level}"

            arcade.draw_text(text=level_text,
                            start_x=flower_x_position+50,
                            start_y=flower_y_position+29-y,
                            color=(252,248,151),
                            font_size=10,
                            font_name=UI_FONT
                            )
            y += 70
    def draw_active_skill(self):
        """スキルアイコンの表示"""
    #     slot_len = len(self.player.fighter.active_skill)
    #     self.skill_left_position = self.viewport_left + GRID_SIZE*7
    #    self. # パネル左からの所持アイテム表示位置の調整に使う変数
        skill_top_position = self.skill_top_position
    #     # パネル上端からの所持アイテム表示位置の調整に使う変数
    #     self.separate_size = 4.5  # スキル名の表示間隔の調整に使う変数
    #     self.field_width = SCREEN_WIDTH / (slot_len + 1) / self.separate_size  # アイテム表示感覚を決める変数

        # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
        # TODO 複数行にする処理を考える（５回ループしたら縦と横の変数に増減するなど）
        # <active skill>        
        arcade.draw_text(text="[Active Skill]",
                         start_x=self.active_panel_line+5,
                         start_y=self.panel_top_position - 15,
                         color=arcade.color.ORANGE,
                         font_size=12,
                         font_name=UI_FONT
                         )
        for i, skill in enumerate(self.player.fighter.active_skill):
            if i == 5:
                skill_top_position = skill_top_position - GRID_SIZE
            if i > 4:
                i -= 5
            skill_position = i * self.field_width + self.a_skill_left_position  # self.左からの所持skillの表示位置

            key_number = f"[Key {i+1}]"

            # スキルアイコンの描画
            arcade.draw_texture_rectangle(
                center_x=skill_position,
                center_y=skill_top_position,
                width=40,
                height=40,
                texture=IMAGE_ID["black_board"]
            )
            arcade.draw_texture_rectangle(
                center_x=skill_position,
                center_y=skill_top_position,
                width=40,
                height=40,
                texture=skill.icon
            )
            # アイコンに白幕をかけクールダウンタイム表示
            if 0 < skill.count_time:
                arcade.draw_texture_rectangle(
                    center_x=skill_position,
                    center_y=skill_top_position,
                    width=40,
                    height=40,
                    texture=IMAGE_ID["cool_down"],
                    alpha=200
                )
                arcade.draw_text(
                    text=str(skill.count_time),
                    start_x=skill_position,
                    start_y=skill_top_position,
                    color=arcade.color.BLUE,
                    font_size=27,
                    anchor_x="center",
                    anchor_y="center"
                )
            else:
                arcade.draw_text(
                    text=key_number,
                    start_x=skill_position,
                    start_y=self.text_level-12,
                    color=arcade.color.YELLOW_ORANGE,
                    font_size=self.item_font_size,
                    anchor_x="center"
                )

            arcade.draw_text(
                text=f"Level {skill.level}",
                start_x=skill_position,
                start_y=self.text_level,
                color=COLORS["status_panel_text"],
                font_size=self.item_font_size,
                anchor_x="center"
            )

    def draw_passive_skill(self):
        """スキルアイコン及びステータスを右パネルに描画する"""
        self.p_skill_left_position = self.passive_panel_line+37
        # self.panel_top_position = self.viewport_bottom + self.skill_panel_height
        skill_top_position = self.skill_top_position
        # self.separate_size=3.57
        # self.field_width = SCREEN_WIDTH / 6 / self.separate_size  # アイテム表示感覚を決める変数

        item_text = ""

        # <passive skill>        
        arcade.draw_text(text="[Passive Skill]",
                         start_x=self.passive_panel_line+5,
                         start_y=self.panel_top_position - 15,
                         color=arcade.color.BABY_BLUE,
                         font_size=12,
                         font_name=UI_FONT
                         )

        
        for i, skill in enumerate(self.player.fighter.passive_skill):
            if i == 5:
                skill_top_position = skill_top_position - GRID_SIZE
            if i > 4:
                i -= 5

            skill_position = i * self.field_width + self.p_skill_left_position  # 左からの所持skillの表示位置

            arcade.draw_texture_rectangle(
                center_x=skill_position,
                center_y=skill_top_position,
                width=40,
                height=40,
                texture=IMAGE_ID["black_board"]
            )
            arcade.draw_texture_rectangle(
                center_x=skill_position,
                center_y=skill_top_position,
                width=40,
                height=40,
                texture=skill.icon
            )

            arcade.draw_text(
                text=f"Level {skill.level}",
                start_x=skill_position,
                start_y=self.text_level,
                color=COLORS["status_panel_text"],
                font_size=self.item_font_size,
                anchor_x="center"
            )





    def draw_messages_handle(self):
        """メッセージ表示領域"""
        margin = -15
        message_top_position = 19  # パネル上端からのメッセージ表示位置
        message_left_position = self.viewport_left - margin  # 画面左からのメッセージ表示位置
        message_first_position = self.viewport_bottom + GRID_SIZE*3-26# self.side_panel_height#self.viewport_bottom + 170# STATES_PANEL_HEIGHT - message_top_position  # 最初の行


        c = 255
        for message in list(reversed(self.messages)):
            arcade.draw_text(
                text=message,
                start_x=message_left_position,
                start_y=message_first_position,
                color=(255,255,255,c),
                font_size=14
            )
            c -= 15 # 行ごとに文字列を減色させる

            # 文字送り
            message_first_position -= message_top_position


def draw_status_bar(start_x, start_y, width, height, current_value, max_value, front_color, bac_color=(155,155,155,155)):
    """ステータスバーの実体"""

    arcade.draw_xywh_rectangle_filled(start_x, start_y, width, height, color=bac_color)

    states_width = (current_value / max_value) * width


    arcade.draw_xywh_rectangle_filled(start_x ,start_y, states_width, height, color=front_color)
