from keymap import choices_key
from random import choice
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
        self.skill_queue = deque([LeafBlade()])
        self.skill_result = []
        self.select = None

    def states_choices(self, key):
        self.key = key
        if self.engine.player.fighter.ability_points >= 1:
            if key == arcade.key.S:
                self.engine.player.fighter.base_strength += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = "str"
            elif key == arcade.key.D:
                self.engine.player.fighter.base_dexterity += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = "dex"
            elif key == arcade.key.I:
                self.engine.player.fighter.base_intelligence += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = "int"
            self.ui_state = Select.open_skill

    def window_pop(self, viewports):
        """Levelup時に出現するwindow"""

        self.viewports = viewports

        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]


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

        # ability pointがゼロ、かつstateがabilityで選択文が出る
        if self.engine.player.fighter.ability_points < 1 and self.ui_state == Select.ability:
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



            # Nボタンならability pointを戻し再選択させる
            elif self.key == arcade.key.N:
                self.select = None
                self.engine.player.fighter.ability_points += 1
                if self.tmp_states == "str":
                    self.engine.player.fighter.base_strength -= 1
                elif self.tmp_states == "dex":
                    self.engine.player.fighter.base_dexterity -= 1
                elif self.tmp_states == "int":
                    self.engine.player.fighter.base_intelligence -= 1

        else:
            self.up_str = "(key press S + 1)"
            self.up_dex = "(key press D + 1)"
            self.up_int = "(key press I + 1)"

        # ability pointがゼロかつスキル取得レベルなら追加で窓を表示する
        if self.engine.player.fighter.ability_points < 1 and self.engine.player.fighter.level == 2 or self.engine.player.fighter.level % 3 == 0:

            # スキル表示最下部の窓
            arcade.draw_xywh_rectangle_filled(
                bottom_left_x=self.viewport_left+650,
                bottom_left_y=self.viewport_bottom+330,
                width=SCREEN_WIDTH - 1180,
                height=SCREEN_HEIGHT - 790,
                color=[225, 225, 225, 120]
            )

            # スキル枠A
            arcade.draw_xywh_rectangle_filled(
                bottom_left_x=self.viewport_left+662,
                bottom_left_y=self.viewport_bottom+340,
                width=128,
                height=128,
                color=[255, 25, 25, 190]
            )
            # スキル枠Aのスキルアイコン
            arcade.draw_texture_rectangle(
                self.viewport_left+662+64,
                self.viewport_bottom+340+64,
                64, 64,
                texture=arcade.load_texture("image\leaf_blade_icon.png")
            )


            # スキル枠B
            arcade.draw_xywh_rectangle_filled(
                bottom_left_x=self.viewport_left+662 + 140,
                bottom_left_y=self.viewport_bottom+340,
                width=128,
                height=128,
                color=[255, 25, 25, 190]
            )


            # スキル枠Bのスキルアイコン
            arcade.draw_texture_rectangle(
                self.viewport_left+662+140+64,
                self.viewport_bottom+340+64,
                64, 64,
                texture=arcade.load_texture(r"image\branch_baton_icon.png")
            )



            # スキル枠Aのタイトル
            arcade.draw_text(
                text=f"Leaf Blade",
                start_x=self.viewport_left+662,
                start_y=self.text_position_y-100,
                # font_name="consola.ttf",
                color=arcade.color.AQUA,
                font_size=15
            )

            # スキル枠Bのタイトル
            arcade.draw_text(
                text=f"Branch Baton",
                start_x=self.viewport_left+660 + 142,
                start_y=self.text_position_y-100,
                # font_name="consola.ttf",
                color=arcade.color.BABY_BLUE_EYES,
                font_size=15
            )

            # スキル選択でui_stateをablityにして決定の確認に進む
            if self.key == arcade.key.A and self.ui_state == Select.open_skill:
                self.skill_result = []
                self.skill_result.append(LeafBlade())
                self.select = "A"

                # TODO このあたりにキューで選択肢をポップさせる仕様にしたい

                # playerのskill listに追加し、装備更新をチェックさせる
                self.ui_state = Select.ability

            elif self.key == arcade.key.B and self.ui_state == Select.open_skill:
                self.skill_result = []
                self.skill_result.append(BranchBaton())
                self.select = "B"

                # self.engine.player.equipment.equip_update_check = True
                self.ui_state = Select.ability

        else:
            # スキル取得レベルで無ければスキル窓表示をスキップ
            self.ui_state = Select.ability

        if self.select == "A":
            arcade.draw_xywh_rectangle_filled(
                bottom_left_x=self.viewport_left+662,
                bottom_left_y=self.viewport_bottom+340,
                width=128,
                height=128,
                color=[255, 255, 255, 100]
            )



        if self.select == "B":
            arcade.draw_xywh_rectangle_filled(
                bottom_left_x=self.viewport_left+662 + 140,
                bottom_left_y=self.viewport_bottom+340,
                width=128,
                height=128,
                color=[255, 255, 255, 100]
            )
