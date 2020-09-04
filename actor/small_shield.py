from actor.actor import Actor
from actor.equippable import Equippable
from data import *
from constants import *


class SmallShield(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="small_shield",
            x=x,
            y=y,
            scale=1.75,
        )
        self.item = True
        self.slot = "off_hand"
        self.states_bonus = {"defense":2}

        self.category = {ItemType.equip}


        self.item_margin_x = -5.5*SPRITE_SCALE
        self.item_margin_y = 4*SPRITE_SCALE

    @staticmethod
    def challenge():
        return 1