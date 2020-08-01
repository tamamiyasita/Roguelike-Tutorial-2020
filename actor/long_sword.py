from actor.actor import Actor
from actor.equip import Equippable
from actor.equipment import EquipmentSlots
from data import *
from constants import *


class LongSword(Actor):
    def __init__(self, x=0, y=0):
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=5)
        super().__init__(
            name="long_sword",
            x=x,
            y=y,
            # scale=1.7,
            equippable=equippable_component,
        )

        self.item_margin_x = 18
        self.item_margin_y = 0

    @staticmethod
    def challenge():
        return 2