from constants import *
from data import *
from actor.skills.base_skill import BaseSkill
from random import randint
from hit_anime import Fall

class BananaPeel(BaseSkill):
    def __init__(self, x=0, y=0, name="banana_peel"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )

    
        self._damage = 1
        self.hit_rate = 92
        self.speed = 6
        self.attr = "physical"
        self.effect = None

        self.tag = [Tag.item, Tag.equip, Tag.counter, Tag.skill, Tag.passive]

        self.level = 1
        
        self.item_weight = 4


        self.explanatory_text = f""

        self.icon = IMAGE_ID["banana_peel_icon"]

    def use(self, engine):
        Fall(self)
