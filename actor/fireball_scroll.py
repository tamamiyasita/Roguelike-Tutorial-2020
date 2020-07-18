import math

from typing import Optional
from constants import *
from data import *
from actor.item import Item
from actor.actor import Actor
from util import get_blocking_entity, grid_to_pixel, pixel_to_grid


class FireballEfc(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y, texture=effect1[134])
        self.alpha = 255
        EFFECT_LIST.append(self)
        self.scale = 0.1

    def update(self):
        self.alpha -= 1
        if self.alpha > 100:
            self.scale += 0.6
            self.angle += 14
        if self.alpha < 220:
            EFFECT_LIST.remove(self)


class FireballScroll(Actor):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x=x, y=y, texture=scroll[6], name="Fireball Scroll", color=COLORS["transparent"],
                         visible_color=arcade.color.WHITE,
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
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        print(f"{pixel_x}{pixel_y} apply pixel_x_y")
        sprites = arcade.get_sprites_at_point((pixel_x, pixel_y), ACTOR_LIST)
        for sprite in sprites:
            print(sprite, "sprite")
            if sprite.fighter and not sprite.is_dead:
                results.extend(
                    [{"message": f"{sprite.name} was struck by a fireball for {amount} points."}])
                result = sprite.fighter.take_damage(amount)
                if result:
                    results.extend(result)

    def click(self, x, y):
        print("Click!", x, y)
        results = []
        print(results, "results")
        fireball = FireballEfc(x, y)
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
