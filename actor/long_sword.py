from actor.actor import Actor
from actor.equippable import Equippable
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
        self.states_bonus = {"power":3, "defense":1}

        self.category = {ItemType.equip}

        self.item_margin_x = 9 * SPRITE_SCALE
        self.item_margin_y = 0

    @staticmethod
    def challenge():
        return 2
