from actor.actor import Actor
from constants import *
from data import *



class Ebony(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="ebony",
            x=x,
            y=y,
        )

        self.slot = "head"
        self.states_bonus = {"STR": 1}

        self.level = 1

        self.tag = [Tag.item, Tag.equip, Tag.flower]
        
        self.skill_add = {"branch_baton":1}

        self.item_margin_x = 16
        self.item_margin_y = 17
        self.my_speed = 4.3
