from actor.actor import Actor
from data import *
from constants import *
from fire import Fire
from actor.skills.base_skill import BaseSkill



class SeedShot(BaseSkill):
    def __init__(self, x=0, y=0, name="seed_shot"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        self.data={"switch":False,
                  "count_time":0,
                  "cooldown":False}

        self.amm = "seed_shot_b"

        self.max_cooldown_time = 2

        self._damage = 6
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
            fire.use()



    def update_animation(self, delta_time):
        super().update_animation(delta_time)

        if self.master.state == state.SHOT:
                if self.master.left_face:
                    self.angle = 90
                    self.item_margin_x = self.master.x+4
                    self.item_margin_y = 5
                else:
                    self.angle = -90
                    self.item_margin_x = self.master.x+4
                    self.item_margin_y = 5
        else:
            self.angle = 0
