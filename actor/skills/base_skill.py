
# class BaseSkill:
#     def __init__(self, level=1, damage=1, hit_rate=90, attr="physical", effect=None) -> None:
#         self.level = level
#         self.damage = damage
#         self.hit_rate=hit_rate
#         self.attr=attr
#         self.effect=effect


from actor.actor import Actor
from constants import *
from data import *




class BaseSkill(Actor):
    def __init__(self, x=0, y=0, name="base_skill", data={"switch":False},
                level=1, damage=1, hit_rate=90, attr="physical", effect=None):
        super().__init__(
            name=name,
            x=x,
            y=y,
            data=data
        )
        self.color=COLORS["white"]

        self.level = level
        self.damage = damage
        self.hit_rate = hit_rate
        self.attr = attr
        self.effect = effect


        self.tag = []

        self.icon = IMAGE_ID["grass_cutter_icon"]

        self.item_weight = 1.1

        self.item_margin_x = 0
        self.item_margin_y = 0

        self.item_position_x = 0
        self.item_position_y = 0

    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        try:


            if Tag.skill in self.tag:

                if self.master.left_face:
                    self.left_face = True
                    self.center_y = self.master.center_y - self.item_margin_y
                    self.center_x = self.master.center_x - self.item_margin_x
                if self.master.left_face == False:
                    self.left_face = False
                    self.center_y = self.master.center_y - self.item_margin_y
                    self.center_x = self.master.center_x + self.item_margin_x

                if self.master.state == state.ON_MOVE:
                    self.item_margin_x = self.item_position_x * SPRITE_SCALE
                    self.item_margin_y = (self.item_position_y - 1)
                else:
                    self.item_margin_x = self.item_position_x * SPRITE_SCALE
                    self.item_margin_y = self.item_position_y * SPRITE_SCALE

        except:
            pass
