import math

from typing import Optional
from constants import *
from data import *
from item import Item
from actor import Actor
from util import get_blocking_entity, pixel_position, map_position


class FireballScroll(Actor):
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, image=scroll[6], name="Fireball Scroll", color=COLORS["transparent"], visible_color=arcade.color.WHITE,
                         not_visible_color=COLORS.get("dark_ground"), item=Item())
        self.alpha = 0
        ITEM_LIST.append(self)

    def use(self, game_engine: "GameEngine"):
        print("use")
        self.game_engine = game_engine
        game_engine.game_state = GAME_STATE.SELECT_LOCATION
        game_engine.grid_select_handlers.append(self.click)
        return None

    def apply_damage(self, grid_x, grid_y, amount, results):
        pixel_x, pixel_y = pixel_position(grid_x, grid_y)
        sprites = arcade.get_sprites_at_point((pixel_x, pixel_y), ACTOR_LIST)
        for sprite in sprites:
            if sprite.fighter and not sprite.is_dead:
                results.extend(
                    [{"message": f"{sprite.name} was struck by a fireball for {amount} points."}])
                result = sprite.fighter.take_damage(amount)
                if result:
                    results.extend(result)

    def click(self, x, y):
        print("Click!", x, y)
        results = []
        self.apply_damage(x, y, 10, results)

        self.apply_damage(x-1, y-1, 8, results)
        self.apply_damage(x, y-1, 8, results)
        self.apply_damage(x+1, y-1, 8, results)

        self.apply_damage(x-1, y, 8, results)
        self.apply_damage(x+1, y, 8, results)

        self.apply_damage(x-1, y+1, 8, results)
        self.apply_damage(x, y+1, 8, results)
        self.apply_damage(x + 1, y + 1, 8, results)

        self.game_engine.player.inventory.remove_item(self)

        return results
