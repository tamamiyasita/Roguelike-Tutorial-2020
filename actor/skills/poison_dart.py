from actor.actor import Actor
from constants import *
from data import *
from actor.skills.base_skill import BaseSkill
from actor.states.poison_status import PoisonStatus
from fire import Fire

class PoisonDart(BaseSkill):
    def __init__(self, x=0, y=0, name="poison_dart"):
        super().__init__(
            x=x,
            y=y,
            name=name,
        )

        self.data={"switch":False,
                  "count_time":0,
                  "cooldown":False}

        self.amm = "seed_shot_b"

        self.max_cooldown_time = 4

        self._damage = 2
        self.hit_rate = 85
        self.speed = 10
        self.attr = "poison"
        self.effect = PoisonStatus(count_time=3)

        self.item_weight = 6



        self.level = 1

        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill, Tag.equip]

        self.explanatory_text = f""

        self.icon = IMAGE_ID["seed_shot_icon"]  
        

    def use(self, engine):
        self.effect = PoisonStatus(count_time=3)

        if self.data["count_time"] <= 0:

            fire = Fire(engine, self.owner, self)
            fire.use()