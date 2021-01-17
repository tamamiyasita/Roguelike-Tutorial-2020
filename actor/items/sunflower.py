from actor.actor import Actor
from constants import *
from data import *



class Sunflower(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="sunflower",
            x=x,
            y=y,
            scale=1.5
        )

        self.slot = "flower"
        self.states_bonus = {"DEX": 1}

        self.level = 1

        self.tag = [Tag.item, Tag.equip, Tag.flower]
        
        self.skill_add = {"seed_shot":1}

        self.explanatory_text = f"Is sunflower \n st"


        self.item_margin_x = 17
        self.item_margin_y = 6
        self.my_speed = 2.3