import math

from typing import Optional
from constants import *
from data import *
from actor.item import Item
from actor.actor import Actor
import random


class LightningEfc(Actor):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, texture=effect1[87])
        self.alpha = 255
        EFFECT_LIST.append(self)
        self.scale = 3.6

    def update(self):
        self.alpha -= 5
        print(self.alpha, "ALF")
        if self.alpha % 10 == 0:
            self.scale += random.random()
            self.center_x += random.randint(1, 3)
        else:
            # self.scale += random.random()
            self.center_x -= random.randint(1, 3)

        if self.alpha <= 90:

            EFFECT_LIST.remove(self)


class LightningScroll(Actor):
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, texture=scroll[1], name="Lightning Scroll", color=COLORS["transparent"], visible_color=arcade.color.WHITE,
                         not_visible_color=COLORS.get("dark_ground"), item=Item())
        self.alpha = 0
        ITEM_LIST.append(self)

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
            lightning = LightningEfc(closest_actor.x, closest_actor.y)
            damage = 10
            game_engine.player.inventory.remove_item(self)
            results.append(
                {"message": f"{closest_actor.name} was struck by lighting for {damage} points."})
            results.extend(closest_actor.fighter.take_damage(damage))

            return results
        else:
            results.extend([{"message": "not enemy"}])

        return results
