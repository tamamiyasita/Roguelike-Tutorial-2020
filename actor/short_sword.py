from actor.actor import Actor
from actor.equippable import Equippable
from data import *
from constants import *
from random import randint


class ShortSword(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="short_sword",
            x=x,
            y=y,
            scale=1.4,
        )

        self.slot = "main_hand"
        self.states_bonus = {"power":1}

        self.category = {ItemType.equip}

        # self.explanatory_text = f"common short sword\nthat deals ? damage"

        self.item_margin_x = 6.5*SPRITE_SCALE
        self.item_margin_y = 2.5*SPRITE_SCALE

    @staticmethod
    def challenge():
        return 1
