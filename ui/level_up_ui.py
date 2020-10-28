from random import choice
from typing import Tuple
import arcade
from constants import *
from data import *
from actor.items.leaf_blade import LeafBlade
from actor.items.branch_baton import BranchBaton
from enum import Enum, auto
from collections import deque


class Select(Enum):
    ability = auto()
    delay = auto()
    open_skill = auto()



class LevelupUI:
    def __init__(self, engine):
        self.engine = engine
        self.up_str = ""
        self.up_dex = ""
        self.up_int = ""
        self.tmp_states = None
        self.ui_state = Select.delay
        self.skill_queue = deque([None, (LeafBlade(), BranchBaton()), BranchBaton()])
        self.skill_result = []
        self.get_skill = None

    def states_choices(self, key):
        self.key = key
        if self.engine.player.fighter.ability_points >= 1:
            if key == arcade.key.S:
                self.engine.player.fighter.base_strength += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = "STR"
            elif key == arcade.key.D:
                self.engine.player.fighter.base_dexterity += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = "DEX"
            elif key == arcade.key.I:
                self.engine.player.fighter.base_intelligence += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = "INT"
            self.ui_state = Select.open_skill

    def window_pop(self, viewports):
        """Levelup時に出現するwindow"""

        self.viewports = viewports

        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]

        self.draw_base_window()
        self.draw_ability_select()

        if self.ui_state == Select.open_skill or self.get_skill:
            self.get_skill = self.get_skill_queue(self.get_skill)
            self.draw_skill_get_window()



    def draw_base_window(self):
        # 最下部の基本枠
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left+650,
            bottom_left_y=self.viewport_bottom+500,
            width=SCREEN_WIDTH - 1180,
            height=SCREEN_HEIGHT - 800,
            color=[255, 255, 255, 190]
        )

        # テキストに使う変数
        spacing = 30
        self.text_position_x = self.viewport_left + 660
        self.text_position_y = self.viewport_bottom + SCREEN_HEIGHT - 300
        text_size = 24

        # 最上段のタイトル
        screen_title = "Level UP!"
        text_color = arcade.color.GREEN_YELLOW
        arcade.draw_text(
            text=screen_title,
            start_x=self.text_position_x-10,
            start_y=self.text_position_y,
            color=text_color,
            font_size=text_size
        )

        # ability point表示
        text_color = arcade.color.PALATINATE_PURPLE
        arcade.draw_text(
            text=f"ability point: {self.engine.player.fighter.ability_points}",
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        # 以下ステータスpointの表示
        self.text_position_y -= spacing
        text_color = arcade.color.RED_ORANGE
        arcade.draw_text(
            text=f"STR: {self.engine.player.fighter.base_strength} {self.up_str}",
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        self.text_position_y -= spacing
        text_color = arcade.color.BLUEBERRY
        arcade.draw_text(
            text=f"DEX: {self.engine.player.fighter.base_dexterity} {self.up_dex}",
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        self.text_position_y -= spacing
        text_color = arcade.color.BLACK_LEATHER_JACKET
        arcade.draw_text(
            text=f"INT: {self.engine.player.fighter.base_intelligence} {self.up_int}",
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

    def draw_ability_select(self):
        # ability pointがゼロ、かつstateがabilityで選択文が出る
        if self.engine.player.fighter.ability_points == 0 and self.ui_state == Select.ability:
            self.up_str = ""
            self.up_dex = ""
            self.up_int = ""
            arcade.draw_text(
                text=f"It's OK? ( YES : key[y]   NO : key[n] )",
                start_x=self.text_position_x+10,
                start_y=self.text_position_y-60,
                # font_name="consola.ttf",
                color=arcade.color.OLD_BURGUNDY,
                font_size=15
            )

            # Yボタンが押されたらgame stateをノーマルに戻し終了
            if self.key == arcade.key.Y:
                self.engine.game_state = GAME_STATE.NORMAL
                self.engine.player.fighter.skill_list.extend(self.skill_result)
                self.engine.player.equipment.equip_update_check = True
                self.get_skill = None



            # Nボタンならability pointを戻し再選択させる
            elif self.key == arcade.key.N or self.key == arcade.key.ESCAPE:
                self.engine.player.fighter.ability_points += 1
                if self.tmp_states == "STR":
                    self.engine.player.fighter.base_strength -= 1
                elif self.tmp_states == "DEX":
                    self.engine.player.fighter.base_dexterity -= 1
                elif self.tmp_states == "INT":
                    self.engine.player.fighter.base_intelligence -= 1

        elif self.engine.player.fighter.ability_points != 0:
            self.up_str = "(key press S + 1)"
            self.up_dex = "(key press D + 1)"
            self.up_int = "(key press I + 1)"

    
    def get_skill_queue(self, get_skill):
        if get_skill is None and self.skill_queue:
            skill = self.skill_queue.popleft()
            return skill
        else:
            return get_skill


    def draw_skill_get_window(self):
        # ability pointがゼロかつスキル取得レベルなら追加で窓を表示する
        # if self.ui_state == Select.open_skill and self.engine.player.fighter.ability_points < 1 and self.engine.player.fighter.level == 2 or self.engine.player.fighter.level % 3 == 0:
        if isinstance(self.get_skill, Tuple):
            if self.engine.player.fighter.ability_points < 1 and self.engine.player.fighter.level == 2 or self.engine.player.fighter.level % 3 == 0:
                skill_A = self.get_skill[0]
                skill_B = self.get_skill[1]

                # ベーススキル窓
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.viewport_left+650,
                    bottom_left_y=self.viewport_bottom+330,
                    width=SCREEN_WIDTH - 1180,
                    height=SCREEN_HEIGHT - 790,
                    color=[59, 25, 29, 170]
                )

                # スキル枠A
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.viewport_left+662,
                    bottom_left_y=self.viewport_bottom+340,
                    width=128,
                    height=128,
                    color=[25, 25, 45, 190]
                )
                # スキル枠Aのスキルアイコン
                arcade.draw_texture_rectangle(
                    self.viewport_left+662+64,
                    self.viewport_bottom+340+64,
                    64, 64,
                    texture=skill_A.icon
                )


                # スキル枠B
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.viewport_left+662 + 140,
                    bottom_left_y=self.viewport_bottom+340,
                    width=128,
                    height=128,
                    color=[55, 25, 25, 190]
                )


                # スキル枠Bのスキルアイコン
                arcade.draw_texture_rectangle(
                    self.viewport_left+662+140+64,
                    self.viewport_bottom+340+64,
                    64, 64,
                    texture=skill_B.icon
                )

                # スキル選択テキスト
                if self.ui_state == Select.open_skill:

                    arcade.draw_text(
                        text=f"key press A",
                        start_x=self.viewport_left+662,
                        start_y=self.text_position_y-98,
                        # font_name="consola.ttf",
                        color=arcade.color.WHITE,
                        font_size=16
                    )
                    arcade.draw_text(
                        text=f"key press B",
                        start_x=self.viewport_left+660 + 142,
                        start_y=self.text_position_y-98,
                        # font_name="consola.ttf",
                        color=arcade.color.WHITE,
                        font_size=16
                    )

                # スキル枠Aのタイトル
                arcade.draw_text(
                    text=skill_A.name.replace("_", " ").title(),
                    start_x=self.viewport_left+665,
                    start_y=self.text_position_y-123,
                    # font_name="consola.ttf",
                    color=arcade.color.GREEN_YELLOW,
                    font_size=15
                )

                # スキル枠Bのタイトル
                arcade.draw_text(
                    text=skill_B.name.replace("_", " ").title(),
                    start_x=self.viewport_left+660 + 145,
                    start_y=self.text_position_y-123,
                    # font_name="consola.ttf",
                    color=arcade.color.PALE_GOLD,
                    font_size=15
                )

                # スキル選択でui_stateをabilityにして決定の確認に進む
                if self.key == arcade.key.A:
                    self.skill_result = []
                    self.skill_result.append(skill_A)

                    arcade.draw_xywh_rectangle_outline(
                        bottom_left_x=self.viewport_left+662,
                        bottom_left_y=self.viewport_bottom+340,
                        width=128,
                        height=128,
                        color=[255, 155, 155, 255],
                        border_width=5
                    )

                    # playerのskill listに追加し、装備更新をチェックさせる
                    self.ui_state = Select.ability

                elif self.key == arcade.key.B:
                    self.skill_result = []
                    self.skill_result.append(skill_B)

                    arcade.draw_xywh_rectangle_outline(
                        bottom_left_x=self.viewport_left+662 + 140,
                        bottom_left_y=self.viewport_bottom+340,
                        width=128,
                        height=128,
                        color=[255, 155, 155, 255],
                        border_width=5
                    )

                    self.ui_state = Select.ability

        elif self.get_skill:
                # ベーススキル窓
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.viewport_left+650,
                    bottom_left_y=self.viewport_bottom+330,
                    width=SCREEN_WIDTH - 1180,
                    height=SCREEN_HEIGHT - 790,
                    color=[59, 25, 29, 170]
                )

                # スキル枠
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.viewport_left+732,
                    bottom_left_y=self.viewport_bottom+340,
                    width=128,
                    height=128,
                    color=[55, 55, 55, 190]
                )
        
                # スキルアイコン
                arcade.draw_texture_rectangle(
                    self.viewport_left+732+64,
                    self.viewport_bottom+340+64,
                    64, 64,
                    texture=self.get_skill.icon
                )



                arcade.draw_text(
                    text=f"Get Skill",
                    start_x=self.viewport_left+732,
                    start_y=self.text_position_y-98,
                    # font_name="consola.ttf",
                    color=arcade.color.WHITE,
                    font_size=16
                )

                # スキル枠のタイトル
                arcade.draw_text(
                    text=self.get_skill.name.replace("_", " ").title(),
                    start_x=self.viewport_left+735,
                    start_y=self.text_position_y-123,
                    # font_name="consola.ttf",
                    color=arcade.color.GREEN_YELLOW,
                    font_size=15
                )

                self.skill_result = []
                self.skill_result.append(self.get_skill)

                # playerのskill listに追加し、装備更新をチェックさせる
                self.ui_state = Select.ability

        else:
            # スキル取得レベルで無ければスキル窓表示をスキップ
            self.ui_state = Select.ability