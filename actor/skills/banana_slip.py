from constants import *
from data import *
from actor.skills.base_skill import BaseSkill
from actor.states.stun import StunStatus
from hit_anime import Fall

class BananaSlip(BaseSkill):
    def __init__(self, x=0, y=0, name="banana_slip"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )

    
        self._damage = 1
        self.hit_rate = 92
        self.speed = 6
        self.attr = "mind"
        self.effect = None

        self.tag = [Tag.item, Tag.equip, Tag.counter, Tag.skill, Tag.counter, Tag.passive]

        self._level = 1
        
        self.item_weight = 4


        self.explanatory_text = f""

        self.icon = IMAGE_ID["banana_slip_icon"]
        self.anime = IMAGE_ID["banana_fall"]
        self.anime_type = "fall"


    def use(self, target):
        self.effect = StunStatus(count_time=1)
        return target.fighter.skill_process(self)
            