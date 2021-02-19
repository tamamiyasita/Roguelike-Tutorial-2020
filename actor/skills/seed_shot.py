from actor.actor import Actor
from data import *
from constants import *
from fire import Fire
from actor.skills.base_skill import BaseSkill
from ranged import Ranged



class SeedShot(BaseSkill):
    def __init__(self, x=0, y=0, name="seed_shot"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )

        self.amm = "seed_shot_b"
        self.amm_scale = 2

        self.max_cooldown_time = 3

        self._damage = 6
        self.hit_rate = 85
        self.speed = 25
        self.attr = "physical"

        self.damage_range = "single"
        self.player_state = state.SHOT


        self.item_weight = 6

        self._level = 1

        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill, Tag.equip]

        self.explanatory_text = f""

        self.icon = IMAGE_ID["seed_shot_icon"]


    def use(self, engine):

        if self.count_time <= 0:

            fire = Ranged(engine, self.owner, self)
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
