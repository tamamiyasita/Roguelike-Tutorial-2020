import math

from typing import Optional
from constants import *
from data import *
from actor.item import Item
from actor.actor import Actor
import random


class LightningEfc(Actor):
    def __init__(self, x, y, item_sprites):
        super().__init__(
            x=x,
            y=y,
            texture="lightning_effect",
            item_sprites=None
        )
        self.item_sprites = item_sprites
        self.alpha = 255
        self.item_sprites.append(self)
        self.scale = 3.6

    def update(self):
        self.alpha -= 5
        if self.alpha % 10 == 0:
            self.scale += random.random()
            self.center_x += random.randint(1, 3)
        else:
            # self.scale += random.random()
            self.center_x -= random.randint(1, 3)

        if self.alpha <= 90:

            self.actor_list.remove(self)


class LightningScroll(Actor):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(
            x=x,
            y=y,
            texture="lightning_scroll",
            name="lightning_scroll",
            item=Item()
        )
        self.alpha = 0

    def use(self, game_engine: "GameEngine"):
        closest_distance: Optional[float] = None
        closest_actor: Optional[Actor] = None
        results = []

        for actor in game_engine.actor_list:
            if actor.is_visible and actor.fighter and not actor.is_dead and actor.ai:
                x1 = game_engine.player.x
                y1 = game_engine.player.y
                x2 = actor.x
                y2 = actor.y
                distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if closest_distance is None or distance < closest_distance:
                    closest_actor = actor
                    closest_distance = distance

        if closest_actor:
            lightning = LightningEfc(
                closest_actor.x, closest_actor.y, game_engine.item_sprites)
            damage = 10
            game_engine.player.inventory.remove_item(self)
            results.append(
                {"message": f"{closest_actor.name} was struck by lighting for {damage} points."})
            results.extend(closest_actor.fighter.take_damage(damage))

            return results
        else:
            results.extend([{"message": "not enemy"}])

        return results
