from actor.actor import Actor
from data import *
from constants import *


class ShortSword(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="short_sword",
            x=x,
            y=y,
            scale=1.4,
        )

        self.slot = "main_hand"
        self.states_bonus = {}
        self.attack_damage = (1, 1, 4)
        self.hit_rate = 97

        self.level = 1

        self.tag = {Tag.item, Tag.equip}

        self.explanatory_text = f"common short sword\nthat deals {self.attack_damage[0]}D({self.attack_damage[1]} - {self.attack_damage[2]})damage"

        self.item_margin_x = 6.5*SPRITE_SCALE
        self.item_margin_y = 2.5*SPRITE_SCALE
