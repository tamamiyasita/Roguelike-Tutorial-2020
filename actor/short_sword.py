from actor.actor import Actor
from actor.equippable import Equippable
from data import *
from constants import *


class ShortSword(Actor):
    def __init__(self, x=0, y=0):
        equippable_component = Equippable("main_hand", power_bonus=3)
        super().__init__(
            name="short_sword",
            x=x,
            y=y,
            scale=1.4,
            equippable=equippable_component
        )
        self.category = {ItemType.equip}

        self.item_margin_x = 13
        self.item_margin_y = 5

    @staticmethod
    def challenge():
        return 1
