import arcade
from actor.actor import Actor
from util import grid_to_pixel
from constants import COLORS


class ItemPoint:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.item_sprites = engine.cur_level.item_sprites
        self.item_point_sprites = engine.cur_level.item_point_sprites

    def remove_point(self, item):
        for item_point in self.item_point_sprites:
            if item.center_x == item_point.center_x and item.center_y == item_point.center_y:
                item_point.remove_from_sprite_lists()

    def add_point(self, item):
        item_point = Actor(image="items_point", scale=1.2,
                           color=COLORS["light_ground"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])

        item_point.center_x = self.engine.player.center_x
        item_point.center_y = self.engine.player.center_y

        self.item_point_sprites.append(item_point)
