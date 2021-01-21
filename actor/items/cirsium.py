from actor.actor import Actor
from constants import *
from data import *
from random import choices
from util import exp_calc


class Cirsium(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="cirsium",
            x=x,
            y=y,
        )
        # template
        self.slot = "flower"
        self.tag = [Tag.item, Tag.equip, Tag.flower]
        self.current_xp = 0

        # level
        self.level = 1
        self.max_level = 5
        self.experience_per_level = exp_calc()
        self.level_up_weights = [3, 5, 2]

        # states
        self.states_bonus = {"DEX":1}
        self.skill_add = {"leaf_blade":1}
        

        # position
        self.item_margin_x = 16
        self.item_margin_y = 17
        self.my_speed = 4.3

        self.explanatory_text = f"Is Cirsium TEst test test \n testtesttest"



