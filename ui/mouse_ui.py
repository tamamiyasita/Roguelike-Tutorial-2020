
import arcade
from itertools import chain
from constants import *
from util import pixel_to_grid, grid_to_pixel


class MouseUI:
    def __init__(self, mouse_over_text, mouse_position, viewport_x, viewport_y, sprite_lists):
        self.mouse_over_text = mouse_over_text
        self.mouse_position = mouse_position
        self.viewport_x = viewport_x
        self.viewport_y = viewport_y
        self.actor_sprites = sprite_lists[0]
        self.item_sprites = sprite_lists[1]



    def draw_mouse_over_text(self):
        """マウスオーバー時のオブジェクト名表示"""
                # マウスオーバー時に表示するスプライトリストの取得
        actor_list = arcade.get_sprites_at_point(
                        point=self.mouse_position,
                        sprite_list=self.actor_sprites
                        )
        item_list = arcade.get_sprites_at_point(
                        point=self.mouse_position,
                        sprite_list=self.item_sprites
                        )

        self.mouse_over_text = None
        for actor in chain(actor_list, item_list):
            if actor.fighter and actor.is_visible:
                self.mouse_over_text = f"{actor.name} {actor.fighter.hp}/{actor.fighter.max_hp}"
            elif actor.name:
                self.mouse_over_text = f"{actor.name}"

        if self.mouse_over_text:
            x, y = self.mouse_position
            back_ground_width = 100 # テキスト背景幅
            back_ground_height = 16 # テキスト背景高

            arcade.draw_xywh_rectangle_filled(
                        bottom_left_x=x,
                        bottom_left_y=y,
                        width=back_ground_width,
                        height=back_ground_height,
                        color=arcade.color.BLACK
                        )
            arcade.draw_text(
                        text=self.mouse_over_text,
                        start_x=x,
                        start_y=y,
                        color=COLORS["white"]
                        )

    def draw_select_mouse_location(self):
        """ マウス操作時のグリッド表示"""

        mouse_x, mouse_y = self.mouse_position
        grid_x, grid_y = pixel_to_grid(mouse_x, mouse_y)
        center_x, center_y = grid_to_pixel(grid_x, grid_y)

        arcade.draw_rectangle_outline(
                    center_x=center_x,
                    center_y=center_y,
                    width=SPRITE_SIZE*SPRITE_SCALE,
                    height=SPRITE_SIZE*SPRITE_SCALE,
                    color=arcade.color.LIGHT_BLUE,
                    border_width=2
                    )
