
from constants import *
from data import IMAGE_ID
from actor.skills.base_skill import BaseSkill
from random import randint

class BambooBlade(BaseSkill):
    def __init__(self, x=0, y=0, name="bamboo_blade"):
        super().__init__(
            name=name,
            image=IMAGE_ID[name],
            x=x,
            y=y,
        )

        self._damage = 7
        self.hit_rate = 92
        self.speed = 6
        self.attr = "physical"
        self.effect = None

        self.tag = [Tag.item, Tag.equip, Tag.weapon, Tag.skill, Tag.passive]

        self._level = 1
        
        self.item_weight = 1


        self.explanatory_text = f"damage: {self.level}D{self.damage}\nhit rate: {self.hit_rate}"




    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        try:

            if self.master.state == state.ATTACK and Tag.weapon in self.tag:
                # self.item_margin_x = (self.item_position_x + 3) * SPRITE_SCALE
                # self.item_margin_y += randint(-8,8)
                # self.item_margin_x += randint(-8,8)
                self.item_margin_x = (self.item_position_x + 5) * SPRITE_SCALE
                # self.item_margin_x += randint(-3,3)

                if self.owner.left_face:
                    self.angle += 40
                    if self.angle >= 90:
                        self.angle -= 170
                elif not self.owner.left_face:
                    self.angle -= 40
                    if self.angle <= -90:
                        self.angle += 170


                        
            else:
                self.angle = 0

        except:
            pass
