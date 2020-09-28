from keymap import choices_key
from random import choice
import arcade
from constants import *
from data import *


class LevelupUI:
    def __init__(self, engine):
        self.engine = engine

    def window_pop(self, viewports):
        self.viewports = viewports

        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]    

        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left+660,
            bottom_left_y=self.viewport_bottom+400,
            width=SCREEN_WIDTH - 1200,
            height=SCREEN_HEIGHT - 700,
            color=[255, 255, 255, 150]
        )
        spacing = 1.8
        text_position_x = self.viewport_left + 660
        text_position_y = self.viewport_bottom + SCREEN_HEIGHT - 300
        text_size = 24

        screen_title = "Level UP!"
        text_color = arcade.color.RED_ORANGE
        arcade.draw_text(
            text=screen_title,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size
        )