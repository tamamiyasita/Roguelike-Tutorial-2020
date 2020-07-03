import arcade
from constants import *


def viewport(player):

    view_left = 0
    view_bottom = 0
    changed = False

    left_boundary = view_left + VIEWPORT_MARGIN
    if player.left < left_boundary:
        view_left -= left_boundary - player.left
        changed = True

    right_boundary = view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
    if player.right > right_boundary:
        view_left += player.right - right_boundary
        changed = True

    top_boundary = view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
    if player.top > top_boundary:
        view_bottom += player.top - top_boundary
        changed = True

    bottom_boundary = view_bottom + VIEWPORT_MARGIN
    if player.bottom < bottom_boundary:
        view_bottom -= bottom_boundary - player.bottom
        changed = True

    if changed:
        arcade.set_viewport(view_left, SCREEN_WIDTH + view_left,
                            view_bottom+STATES_PANEL_HEIGHT, SCREEN_HEIGHT + view_bottom)
