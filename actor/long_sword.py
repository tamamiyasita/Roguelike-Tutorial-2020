from actor.actor import Actor
from data import *
from constants import *


class LongSword(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="long_sword",
            x=x,
            y=y,
        )

        self.slot = "main_hand"
        self.states_bonus = {"strength": 1, "defense": 1}
        self.attack_damage = (1, 2, 6)

        self.category = {ItemType.equip}

        self.explanatory_text = f"common long sword\nthat deals {self.attack_damage[0]}D({self.attack_damage[1]} - {self.attack_damage[2]})damage"

        self.item_margin_x = 9 * SPRITE_SCALE
        self.item_margin_y = 0

    @staticmethod
    def challenge():
        return 2
