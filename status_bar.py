import arcade

from constants import *


def draw_status_bar(center_x, center_y, width, height, current_value, max_value):

    arcade.draw_rectangle_filled(
        center_x, center_y, width, height, color=COLORS.get("status_bar_background"))
    states_width = (current_value / max_value) * width
    arcade.draw_rectangle_filled(center_x - (width / 2 - states_width / 2),
                                 center_y, states_width, height, COLORS["status_bar_foreground"])
