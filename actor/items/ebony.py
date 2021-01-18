from actor.actor import Actor
from constants import *
from data import *
from random import choices
from util import exp_calc



class Ebony(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="ebony",
            x=x,
            y=y,
        )

        self.slot = "flower"
        self.states_bonus = {"STR": 1}

        self.level = 1
        self.max_level = 5

        self.tag = [Tag.item, Tag.equip, Tag.flower]
        
        self.skill_add = {"branch_baton":1, "leaf_blade":1}

        self.experience_per_level = exp_calc()

        self.current_xp = 0

        self.explanatory_text = f"Is Ebony $#############4TEst test test \n test$#4444444444testtest"


        self.item_margin_x = 19
        self.item_margin_y = 11
        self.my_speed = 4.0


