from actor.actor import Actor
from constants import *
from data import *
import math
import random
from actor.skills.leaf_blade import LeafBlade

class Cirsium(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="cirsium",
            x=x,
            y=y,
        )
        self.materialization = ""


        self.slot = "head"
        self.states_bonus = {"str":1}

        self.level = 1
        
        self.tag = {Tag.item, Tag.equip, Tag.flower}
        self.skill_activation = LeafBlade()

        self.item_margin_x = 16
        self.item_margin_y = 17
        self.my_speed = 4.3

