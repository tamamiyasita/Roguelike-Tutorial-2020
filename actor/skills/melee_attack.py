
class Unarmed:
    def __init__(self, level=1, damage=1, hit_rate=90, attr="physical", effect=None) -> None:
        self.level = level
        self.damage = damage
        self.hit_rate=hit_rate
        self.attr=attr
        self.effect=effect


from actor.actor import Actor
from constants import *
from data import *




class MeleeAttack(Actor):
    def __init__(self, x=0, y=0, name="melee_attack", data={"switch":False}):
        super().__init__(
            name=name,
            x=x,
            y=y,
            data=data
        )
        self.color=COLORS["white"]

        self.damage = 5
        self.hit_rate = 95
        self.speed = 6
        self.attr = "physical"
        self.effect = None

        self.level = 1

        self.tag = []

        self.icon = IMAGE_ID["leaf_blade_icon"]

        self.item_weight = 1.1

        self.item_margin_x = 9
        self.item_margin_y = 2

        self.item_position_x = 9
        self.item_position_y = 2

    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        try:
            if Tag.skill in self.tag:
                if self.master.state == state.ON_MOVE:
                    self.item_margin_x = self.item_position_x * SPRITE_SCALE
                    self.item_margin_y = (self.item_position_y - 1)
                else:
                    self.item_margin_x = self.item_position_x * SPRITE_SCALE
                    self.item_margin_y = self.item_position_y * SPRITE_SCALE

        except:
            pass
