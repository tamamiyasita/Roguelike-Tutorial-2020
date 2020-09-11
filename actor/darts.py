from actor.actor import Actor
from data import *
from constants import *


class Darts(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="darts",
            x=x,
            y=y,
            scale=1.7
        )

        self.slot = "ranged_weapon"
        self.states_bonus = {}
        self.attack_damage = (1, 1, 3)
        self.hit_rate = 75

        self.level = 1

        self.category = {ItemType.equip}

        self.explanatory_text = f"common darts\nthat deals {self.attack_damage[0]}D({self.attack_damage[1]} - {self.attack_damage[2]})damage"

        self.item_margin_x = 6.5*SPRITE_SCALE
        self.item_margin_y = 2.5*SPRITE_SCALE
