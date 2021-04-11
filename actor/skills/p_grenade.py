from constants import *
from data import *
from actor.skills.base_skill import BaseSkill
from ranged import Ranged
from util import dice


class P_Grenade(BaseSkill):
    def __init__(self, x=0, y=0, name="p_grenade"):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y
            )

        self.amm = "p_grenade"

        self.max_cooldown_time = 6

        self._damage = 11
        self.hit_rate = 100
        self.attr = "fire"
        self.effect = None

        self.damage_range = "circle"
        self.size = 2
        self.player_form = form.THROW
        self._level = 1



        self.shot_speed = 16
        self.item_weight = 4



        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill, Tag.equip, Tag.range_attack]

        self.explanatory_text = f""
         
        self.icon = IMAGE_ID["p_grenade_icon"]
        self.anime = IMAGE_ID["explosion_effect"]


    @property
    def damage(self):
        if self.owner:
            return dice((self.level / 3 + 1), ((self.owner.fighter.INT+self._damage))/2, (self.level+10))


    def use(self, engine):

        if self.count_time <= 0:

            fire = Ranged(engine, self.owner, self, spin=60)
            fire.use()


    def update_animation(self, delta_time):
        super().update_animation(delta_time)

        if self.master.form == form.THROW:
            self.alpha = 0
        else:
            self.alpha = 255

