from actor.actor import Actor
from data import *
from constants import *
from fire import Fire
from actor.skills.leaf_blade import LeafBlade


class SeedShot(LeafBlade):
    def __init__(self, x=0, y=0, name="seed_shot"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        self.data={"switch":False,
                  "count_time":0,
                  "cooldown":False}

        self.amm = IMAGE_ID["seed_shot_icon"]

        self.owner = None

        self.max_cooldown_time = 2

        self.damage = 3
        self.hit_rate = 85
        self.speed = 10
        self.attr = "physical"

        self.item_weight = 6



        self.level = 1

        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill, Tag.equip]

        self.explanatory_text = f""

        self.icon = IMAGE_ID["seed_shot_icon"]

    def use(self, engine):

        if self.data["count_time"] <= 0:

            fire = Fire(engine, self.owner, self)
            result = fire.use()



