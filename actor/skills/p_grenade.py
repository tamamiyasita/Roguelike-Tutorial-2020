from constants import *
from data import *
from actor.skills.seed_shot import SeedShot
from throw import Throw

class P_Grenade(SeedShot):
    def __init__(self, x=0, y=0, name="p_grenade"):
        super().__init__(
            name=name,
            x=x,
            y=y
            )

        self.max_cooldown_time = 6

        self.damage = 7
        self.hit_rate = 80
        self.speed = 16
        self.attr = "physical"


        self.icon = IMAGE_ID["p_grenade_icon"]
        self.effect = IMAGE_ID["explosion_effect"]

        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill, Tag.equip]



        self.item_margin_x = 9 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE
        


    def use(self, engine):

        if self.data["count_time"] <= 0:

            fire = Throw(engine, self.owner, self)
            result = fire.use()

    def update(self):
        super().update()
        # if self.master.state == state.ON_MOVE:
        #     self.item_margin_y = 2 * SPRITE_SCALE
        #     # self.item_margin_x = 7 * SPRITE_SCALE
        # else:
        #     self.item_margin_y = 3 * SPRITE_SCALE
            # self.item_margin_x = 6 * SPRITE_SCALE
        if self.master.state == state.THROW:
            self.alpha = 0
        else:
            self.alpha = 255
            self.item_margin_x = -13 * SPRITE_SCALE