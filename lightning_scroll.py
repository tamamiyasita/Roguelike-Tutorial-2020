import math

from typing import Optional
from constants import *
from data import *
from item import Item
from actor import Actor


class LightningScroll(Actor):
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, image=lightning_scroll[1], name="Lightning Scroll", color=COLORS["transparent"], visible_color=arcade.color.WHITE,
                         not_visible_color=COLORS.get("dark_ground"), item=Item())
        self.alpha = 0

    def use(self, game_engine: "GameEngine"):
        closest_distance: Optional[float] = None
        closest_actor: Optional[Actor] = None

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
            results = []
            damege = 10
            game_engine.player.inventory.remove_item(self)
            results.append(
                {"message": f"{closest_actor.name} was struck by lighting for {damege} points."})
            results.extend(closest_actor.fighter.take_damege(damege))

            return results
        else:
            return None
