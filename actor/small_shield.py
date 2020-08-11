from actor.actor import Actor
from actor.equippable import Equippable
from data import *
from constants import *


class SmallShield(Actor):
    def __init__(self, x=0, y=0):
        equippable_component = Equippable("off_hand", defense_bonus=3)
        super().__init__(
            name="small_shield",
            x=x,
            y=y,
            scale=1.5,
            equippable=equippable_component
        )

        self.item_margin_x = -11
        self.item_margin_y = 8

    @staticmethod
    def challenge():
        return 1