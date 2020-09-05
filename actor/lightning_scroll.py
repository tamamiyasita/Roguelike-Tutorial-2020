import math

from typing import Optional

from constants import *
from data import *
from actor.actor import Actor
import random


class LightningEffect(Actor):
    def __init__(self, x, y, effect_sprites):
        super().__init__(
            x=x,
            y=y,
            name="lightning_effect",
            color=COLORS["white"]
        )
        self.effect_sprites = effect_sprites
        self.alpha = 255
        self.effect_sprites.append(self)
        self.scale = 3.6

    def update(self):
        self.alpha -= 5
        if self.alpha % 10 == 0:
            self.scale += random.random()
            self.center_x += random.randint(1, 3)
        else:
            self.center_x -= random.randint(1, 3)

        if self.alpha <= 70:

            self.effect_sprites.remove(self)


class LightningScroll(Actor):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(
            x=x,
            y=y,
            name="lightning_scroll",
            not_visible_color=COLORS["black"],

        )
        self.category = {ItemType.used}

    def use(self, game_engine):
        closest_distance: Optional[float] = None
        closest_actor: Optional[Actor] = None
        results = []

        for actor in game_engine.cur_level.actor_sprites:
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
            lightning = LightningEffect(
                closest_actor.x, closest_actor.y, game_engine.cur_level.effect_sprites)
            damage = 10
            game_engine.player.inventory.remove_item(self)
            results.append(
                {"message": f"{closest_actor.name} was struck by lighting for {damage} points."})
            results.extend(closest_actor.fighter.take_damage(damage))

            return results
        else:
            results.extend([{"message": "not enemy"}])

        return results

    @staticmethod
    def challenge():
        return 1
