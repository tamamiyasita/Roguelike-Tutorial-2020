from constants import *
from data import *
from actor.skills.base_skill import BaseSkill
from actor.states.stun import StunStatus

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

    def use(self, target):
        if self.count_time <= 0:

            effect_component = StunStatus(count_time=4)
            self.effect = effect_component
            target.fighter.skill_process(self)
            