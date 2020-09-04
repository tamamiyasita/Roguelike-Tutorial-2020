from actor.actor import Actor
from actor.equippable import Equippable
from data import *
from constants import *
from random import randint


class ShortSword(Actor):
    def __init__(self, x=0, y=0):
        damage = randint(1,4)
        equippable_component = Equippable("main_hand", power_bonus=damage)
        super().__init__(
            name="short_sword",
            x=x,
            y=y,
            scale=1.4,
            equippable=equippable_component
        )
        self.category = {ItemType.equip}

        self.explanatory_text = f"common short sword\nthat deals {damage} damage"

        self.item_margin_x = 13
        self.item_margin_y = 5

    @staticmethod
    def challenge():
        return 1
