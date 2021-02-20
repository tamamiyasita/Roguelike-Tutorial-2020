import arcade
from constants import *
from data import *

from actor.actor_set import *

from level_up_sys import check_flower_level

from enum import Enum, auto



class LevelupUI:
    def __init__(self):
        self.up_str = ""
        self.up_dex = ""
        self.up_int = ""
        self.tmp_states = None
        self.get_skill = None
        self.select_skill = True


        self.window_width = SCREEN_WIDTH - 924
        self.window_height = SCREEN_HEIGHT - 800

    def states_choices(self, key):
        self.key = key
        if self.engine.game_state == GAME_STATE.LEVEL_UP_WINDOW:
            if self.player.fighter.ability_points >= 1:
                if key == arcade.key.S:
                    self.player.fighter.base_strength += 1
                    self.player.fighter.ability_points -= 1
                    self.tmp_states = "STR"
                elif key == arcade.key.D:
                    self.player.fighter.base_dexterity += 1
                    self.player.fighter.ability_points -= 1
                    self.tmp_states = "DEX"
                elif key == arcade.key.I:
                    self.player.fighter.base_intelligence += 1
                    self.player.fighter.ability_points -= 1
                    self.tmp_states = "INT"

            

    def window_pop(self, viewports, engine):
        """Levelup時に出現するwindow"""
            
        self.engine = engine
        self.player = engine.player
        self.viewports = viewports

        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]

        self.bottom_left_x=self.viewport_left+(MAIN_PANEL_X/2) -(self.window_width/2)
        self.bottom_left_y=self.viewport_bottom+500
        self.back_panel_top_left = self.viewport_top - (GRID_SIZE*4)


        if self.engine.game_state == GAME_STATE.LEVEL_UP_WINDOW:
            self.draw_base_window()
            self.draw_ability_select()

        
                       
                


    def draw_base_window(self):
        # 最下部の基本枠
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.bottom_left_x,
            bottom_left_y=self.bottom_left_y,
            width=self.window_width,
            height=self.window_height,
            color=[255, 255, 255, 190]
        )

        # テキストに使う変数
        spacing = 30
        self.text_position_x = self.bottom_left_x + 10
        self.text_position_y = self.bottom_left_y + 160
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
            text=f"ability point: {self.player.fighter.ability_points}",
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )
        STR = f"STR: {self.player.fighter.base_strength} {self.up_str}"
        DEX = f"DEX: {self.player.fighter.base_dexterity} {self.up_dex}"
        INT = f"INT: {self.player.fighter.base_intelligence} {self.up_int}"

        # 以下ステータスpointの表示
        self.text_position_y -= spacing
        text_color = arcade.color.RED_ORANGE

        arcade.draw_text(
            text=STR,
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        self.text_position_y -= spacing
        text_color = arcade.color.BLUEBERRY
        arcade.draw_text(
            text=DEX,
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        self.text_position_y -= spacing
        text_color = arcade.color.BLACK_LEATHER_JACKET
        arcade.draw_text(
            text=INT,
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

    def draw_ability_select(self):
        # ability pointがゼロで選択文が出る
        if self.player.fighter.ability_points == 0:
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


            # Nボタンならability pointを戻し再選択させる
            elif self.key == arcade.key.N or self.key == arcade.key.ESCAPE:
                self.player.fighter.ability_points += 1
                if self.tmp_states == "STR":
                    self.player.fighter.base_strength -= 1
                elif self.tmp_states == "DEX":
                    self.player.fighter.base_dexterity -= 1
                elif self.tmp_states == "INT":
                    self.player.fighter.base_intelligence -= 1

        elif self.player.fighter.ability_points != 0:
            self.up_str = "(key press S + 1)"
            self.up_dex = "(key press D + 1)"
            self.up_int = "(key press I + 1)"

    

