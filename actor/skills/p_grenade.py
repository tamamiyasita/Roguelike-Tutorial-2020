from constants import *
from data import *
from actor.skills.seed_shot import SeedShot
from actor.skills.leaf_blade import LeafBlade

from throw import Throw

class P_Grenade(LeafBlade):
    def __init__(self, x=0, y=0, name="p_grenade"):
        super().__init__(
            name=name,
            x=x,
            y=y
            )
        self.data={"switch":False,
                  "count_time":0,
                  "cooldown":False}

        self.amm = "p_grenade"

        self.max_cooldown_time = 6


        self.damage = 10
        self.hit_rate = 80
        self.speed = 16
        self.attr = "physical"

        self.item_weight = 4



        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill, Tag.equip]

        self.explanatory_text = f""
         
        self.icon = IMAGE_ID["p_grenade_icon"]
        self.effect = IMAGE_ID["explosion_effect"]


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

        # try:
        #     if self.master.state == state.ON_MOVE:
        #         self.item_margin_x = self.item_position_x * SPRITE_SCALE
        #         self.item_margin_y = (self.item_position_y - 1) * SPRITE_SCALE
        #     else:
        #         self.item_margin_x = self.item_position_x * SPRITE_SCALE
        #         self.item_margin_y = self.item_position_y * SPRITE_SCALE

        # except:
        #     pass
