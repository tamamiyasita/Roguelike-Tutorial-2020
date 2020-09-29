from keymap import choices_key
from random import choice
import arcade
from constants import *
from data import *


class LevelupUI:
    def __init__(self, engine):
        self.engine = engine
        self.up_str = ""
        self.up_dex = ""
        self.up_int = ""

    def states_choices(self, key):
        self.tmp_states = None
        if self.engine.player.fighter.ability_points >= 1:
            if key == arcade.key.S:
                self.engine.player.fighter.base_strength += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = self.engine.player.fighter.base_strength
            elif key == arcade.key.D:
                self.engine.player.fighter.base_dexterity += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = self.engine.player.fighter.base_dexterity
            elif key == arcade.key.I:
                self.engine.player.fighter.base_max_mp += 5
                self.engine.player.fighter.max_mp += 5
                self.engine.player.fighter.base_intelligence += 1
                self.engine.player.fighter.ability_points -= 1
                self.tmp_states = self.engine.player.fighter.base_intelligence

        if self.engine.player.fighter.ability_points <= 0:
            self.up_str = ""
            self.up_dex = ""
            self.up_int = ""
            self.y_n(key)

    def y_n(self, key):
        arcade.draw_text(
            text=f"y_or_n",
            start_x=self.viewport_left + 630,
            start_y=self.viewport_bottom + 400,
            font_name="consola.ttf",
            color=arcade.color.BLACK_BEAN,
            font_size=15
        )
        if key == arcade.key.Y:
            self.engine.game_state = GAME_STATE.NORMAL
        elif key == arcade.key.N:
            self.engine.player.fighter.ability_points += 1
            if self.tmp_states:
                self.tmp_states -= 1

    def window_pop(self, viewports):
        self.viewports = viewports

        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]

        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left+650,
            bottom_left_y=self.viewport_bottom+400,
            width=SCREEN_WIDTH - 1170,
            height=SCREEN_HEIGHT - 700,
            color=[255, 255, 255, 150]
        )
        spacing = 30
        text_position_x = self.viewport_left + 660
        text_position_y = self.viewport_bottom + SCREEN_HEIGHT - 300
        text_size = 24

        screen_title = "Level UP!"
        text_color = arcade.color.RED_ORANGE
        arcade.draw_text(
            text=screen_title,
            start_x=text_position_x-10,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size
        )

        text_color = arcade.color.GREEN_YELLOW
        arcade.draw_text(
            text=f"ability point: {self.engine.player.fighter.ability_points}",
            start_x=text_position_x,
            start_y=text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        text_position_y -= spacing
        text_color = arcade.color.YELLOW_ROSE
        self.up_str = "(key press S + 1)"
        arcade.draw_text(
            text=f"STR: {self.engine.player.fighter.base_strength} {self.up_str}",
            start_x=text_position_x,
            start_y=text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        text_position_y -= spacing
        self.up_dex = "(key press D + 1)"
        text_color = arcade.color.YANKEES_BLUE
        arcade.draw_text(
            text=f"DEX: {self.engine.player.fighter.base_dexterity} {self.up_dex}",
            start_x=text_position_x,
            start_y=text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        text_position_y -= spacing
        self.up_int = "(key press I + 1)"
        text_color = arcade.color.HONEYDEW
        arcade.draw_text(
            text=f"INT: {self.engine.player.fighter.base_intelligence} {self.up_int}",
            start_x=text_position_x,
            start_y=text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )
