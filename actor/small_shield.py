from actor.actor import Actor
from actor.equip import Equippable
from actor.equipment import EquipmentSlots
from data import *
from constants import *


class SmallShield(Actor):
    def __init__(self, x=0, y=0):
        equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=3)
        super().__init__(
            name="small_shield",
            x=x,
            y=y,
            equippable=equippable_component
        )

s = SmallShield(0,0)
print(s.equippable.slot.name,"DDDDDDDDDDDDDDDDD")