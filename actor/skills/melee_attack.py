
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
    def __init__(self, x=0, y=0, name="melee_attack", data={"switch":True}):
        super().__init__(
            name=name,
            x=x,
            y=y,
            data=data
        )
        self.color=COLORS["white"]
        if self.name == "melee_attack":
            self.alpha = 0

        #attackに渡される属性
        self.damage = 1
        self.hit_rate = 95
        self.speed = 10
        self.attr = "physical"
        self.effect = None

        self.level = 1

        self.tag = []

        self.item_margin_x = 0
        self.item_margin_y = 0

        self.item_position_x = 0
        self.item_position_y = 0

    # def update_animation2(self, delta_time):
    #     super().update_animation(delta_time)
    #     try:
    #         if Tag.weapon in self.tag:
    #             if self.master.state == state.ON_MOVE:
    #                 self.item_margin_x = self.item_position_x * SPRITE_SCALE
    #                 self.item_margin_y = (self.item_position_y - 1) * SPRITE_SCALE
    #             elif self.master.state == state.DELAY:
    #                 self.item_margin_x = self.item_position_x * SPRITE_SCALE
    #                 self.item_margin_y = self.item_position_y * SPRITE_SCALE


    #     except:
    #         pass

