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
            if item.x == item_point.x and item.y == item_point.y:
                item_point.remove_from_sprite_lists()

    def add_point(self, item):
        item_point = Actor(name="items_point", scale=1,
                           color=COLORS["light_ground"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])
        item_point.x = item.x
        item_point.y = item.y
        cx, cy = grid_to_pixel(item.x, item.y)
        item_point.center_x = cx
        item_point.center_y = cy

        self.item_point_sprites.append(item_point)
