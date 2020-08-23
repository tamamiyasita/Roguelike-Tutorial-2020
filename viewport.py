import arcade
from constants import *


def viewport(player):

    view_left = 0
    view_bottom = 0
    changed = False

    left_boundary = int(view_left + VIEWPORT_MARGIN  + (SPRITE_SIZE * SPRITE_SCALE)) +15
    if player.left < left_boundary:
        view_left -= left_boundary - player.left
        changed = True
    # print(left_boundary)

    right_boundary = int(view_left + SCREEN_WIDTH - VIEWPORT_MARGIN - STATES_PANEL_WIDTH - (SPRITE_SIZE * SPRITE_SCALE)) -21
    if player.right > right_boundary:
        view_left += player.right - right_boundary
        changed = True

    # print(right_boundary)
    top_boundary = view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN - STATES_PANEL_HEIGHT - (SPRITE_SIZE * SPRITE_SCALE) -16
    if player.top > top_boundary:
        view_bottom += player.top - top_boundary
        changed = True
    # print(f"{top_boundary=}")
    bottom_boundary = view_bottom + VIEWPORT_MARGIN - STATES_PANEL_HEIGHT + (SPRITE_SIZE * SPRITE_SCALE) + (SPRITE_SIZE * SPRITE_SCALE)+16
    if player.bottom < bottom_boundary:
        view_bottom -= bottom_boundary - player.bottom
        changed = True
    # print(f"{bottom_boundary=}")

    if changed:
        arcade.set_viewport(view_left, SCREEN_WIDTH + view_left,
                            view_bottom, SCREEN_HEIGHT + view_bottom)
