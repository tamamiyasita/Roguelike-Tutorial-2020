from actor.actor import Actor
from constants import *
from data import *



class Paeonia(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="paeonia",
            x=x,
            y=y,
            scale=1.2
        )

        self.slot = "flower"
        self.states_bonus = {"INT": 1}

        self.level = 1

        self.tag = [Tag.item, Tag.equip, Tag.flower]
        
        self.skill_add = {"healing":1}

        self.explanatory_text = f"Is Ebony $#############4TEst test test \n test$#4444444444testtest"


        self.item_margin_x = 17
        self.item_margin_y = 6
        self.my_speed = 2.3
