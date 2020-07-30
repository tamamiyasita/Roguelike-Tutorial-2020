from actor.actor import Actor
from actor.equip import Equippable
from actor.equipment import EquipmentSlots
from data import *
from constants import *


class ShortSword(Actor):
    def __init__(self, x=0, y=0):
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
        super().__init__(
            name="short_sword",
            x=x,
            y=y,
            equippable=equippable_component
        )