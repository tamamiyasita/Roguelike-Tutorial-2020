from actor.actor import Actor
from constants import *
from data import *
from util import exp_calc
import math
from random import random, uniform

class BaseFlower(Actor):
    def __init__(self, x=0, y=0, name="silver_grass"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        # template
        self.tag = [Tag.item, Tag.equip, Tag.flower]
        self.current_xp = 0

        # level
        self.level = 1
        self.max_level = 5
        self.experience_per_level = exp_calc()
        self.level_up_weights = [3, 3, 4]

        # states
        self.states_bonus = {}
        self.skill_generate = ""
        self.skill_add = {}
        self.data = {}
      
        self.explanatory_text = f"test \n test"

        # position

        self.item_margin_x = 0
        self.item_margin_y = 0

        self.my_speed = 4.3
        self.scale=2

        # TODO 別の動きをそのうち実装したい
        self.flower_move = 0
        # self.move_time = 3


    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        try:

            if self.master.left_face:
                item_margin_x = self.item_margin_x
            else:
                item_margin_x = -self.item_margin_x
            item_margin_y = self.item_margin_y

            if self.flower_move == 0:
                    
                self.angle += uniform(0.1, 3)
                x_diff = (self.master.center_x + item_margin_x + random()) - (self.center_x)
                y_diff = (self.master.center_y + item_margin_y +random()) - (self.center_y)
                angle = math.atan2(y_diff, x_diff)

                if abs(x_diff) > 15 or abs(y_diff) > 15:

                    self.change_x = math.cos(
                        angle) * (self.my_speed + uniform(0.6, 4.2))
                    self.change_y = math.sin(
                        angle) * (self.my_speed + uniform(0.6, 4.2))
                else:
                    self.change_x = math.cos(angle) * uniform(0.02, 0.3)
                    self.change_y = math.sin(angle) * uniform(0.02, 0.3)


            elif self.flower_move == 1:
                pass

        except:

            pass

