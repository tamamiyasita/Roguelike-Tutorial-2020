from actor.actor import Actor
from constants import *
from data import *
from actor.skills.base_skill import BaseSkill
from actor.states.poison_status import PoisonStatus
from ranged import Ranged

class PoisonDart(BaseSkill):
    def __init__(self, x=0, y=0, name="poison_dart"):
        super().__init__(
            x=x,
            y=y,
            name=name,
        )

        effect_component = PoisonStatus(count_time=4)

        self.amm = "poison_dart"

        self.max_cooldown_time = 4

        self._damage = 1
        self.hit_rate = 80
        self.speed = 23
        self.attr = "poison"
        self.effect = effect_component

        self.damage_range = "single"
        self.player_state = state.THROW


        self.item_weight = 5

        self._level = 1

        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill, Tag.equip]

        self.explanatory_text = f""

        self.icon = IMAGE_ID["poison_dart_icon"]  
        self.anime = (IMAGE_ID["poison_start"], "default")
        

    def use(self, engine):

        if self.count_time <= 0:

            effect_component = PoisonStatus(count_time=4)
            self.effect = effect_component
            fire = Ranged(engine, self.owner, self)
            fire.use()

    def update_animation(self, delta_time):
        super().update_animation(delta_time)

        if self.master.state == state.THROW:
            self.alpha = 0
        else:
            self.alpha = 255
            if self.master.left_face:
                self.angle = -90
            else:
                self.angle = 90
        

