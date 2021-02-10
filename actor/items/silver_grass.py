from actor.actor import Actor
from constants import *
from data import *
from util import exp_calc
from actor.items.base_flower import BaseFlower

class SilverGrass(BaseFlower):
    def __init__(self, x=0, y=0, name="silver_grass"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        # template
        self.tag = [Tag.item, Tag.equip, Tag.flower]
        self.current_xp = 0

        # level
        self.level = 1
        self.max_level = 5
        self.experience_per_level = exp_calc()
        self.level_up_weights = [3, 5, 2]

        # states
        self.states_bonus = {"DEX":1}
        self.skill_generate = "grass_cutter"
        self.skill_add = {"grass_cutter":1}
        self.data = {2:"grass_cutter", 3:"grass_cutter"}

        # position

        self.my_speed = 4.3

        self.explanatory_text = f"Is SilverGrass TEst test test \n testtesttest"

        self.flower_move = 0




