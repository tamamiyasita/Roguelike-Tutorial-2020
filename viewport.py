import arcade
from constants import *


def viewport(x, y):

    view_left = 0
    view_bottom = 0
    changed = False

    left_boundary = int(view_left + VIEWPORT_MARGIN)
    if x < left_boundary:
        view_left -= left_boundary - x
        changed = True

    right_boundary = int(view_left + SCREEN_WIDTH -
                         VIEWPORT_MARGIN - STATES_PANEL_WIDTH)
    if x > right_boundary:
        view_left += x - right_boundary
        changed = True

    top_boundary = int(view_bottom + SCREEN_HEIGHT - \
        VIEWPORT_MARGIN - STATES_PANEL_HEIGHT)
    if y > top_boundary:
        view_bottom += y - top_boundary
        changed = True
    bottom_boundary = int(view_bottom + VIEWPORT_MARGIN - \
        STATES_PANEL_HEIGHT + GRID_SIZE) + GRID_SIZE
    if y < bottom_boundary:
        view_bottom -= bottom_boundary - y
        changed = True

    if changed:
        arcade.set_viewport(view_left, SCREEN_WIDTH + view_left,
                            view_bottom, SCREEN_HEIGHT + view_bottom)
