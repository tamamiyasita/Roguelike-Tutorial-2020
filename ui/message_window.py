import arcade
from constants import *


class MessageWindow:
    def __init__(self, engine):
        self.actor = engine.message_event
        self.engine = engine

    def window_pop(self, viewports):
        self.viewports = viewports
        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]

    def panel_ui(self):
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left+200,
            bottom_left_y=self.viewport_bottom+200,
            width=SCREEN_WIDTH - 200,
            height=SCREEN_HEIGHT - 200,
            color=[255, 255, 255, 150]
        )
        arcade.draw_text(
            text=)
