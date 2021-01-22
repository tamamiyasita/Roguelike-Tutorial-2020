from actor.actor import Actor
from constants import *
from data import *
from util import exp_calc


class Paeonia(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="paeonia",
            x=x,
            y=y,
            scale=1.2
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
        self.states_bonus = {"INT": 1}
        self.skill_add = {"healing":1}

        # position
        self.item_margin_x = 17
        self.item_margin_y = -3
        self.my_speed = 3.3


        self.explanatory_text = f"Is Ebony $#############4TEst test test \n test$#4444444444testtest"
















