from actor.actor import Actor
from constants import *
from data import *
from util import exp_calc
import math
from random import random, uniform
from actor.skills.base_skill import BaseSkill



class BaseFlower(Actor):
    def __init__(self, x=0, y=0, name="silver_grass", image=None):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y,
        )
        skill_component = BaseSkill()# コンポーネントの切替で変化を表したい

        # 定数 #############################
        self.tag = [Tag.item, Tag.equip, Tag.flower]
        self.max_level = 5
        self.level_up_weights = [3, 3, 4]
        self.experience_per_level = exp_calc()
        self.explanatory_text = f"test \n test"
        self.owner = None
        self.flower_skill = skill_component
        self.flower_skill.flower = self

        # position
        self.item_margin_x = 0
        self.item_margin_y = 0
        self.my_speed = 4.3
        self.scale=2
        # TODO 別の動きをそのうち実装したい
        self.flower_move = 0
        # self.move_time = 3
        ###################################



        # 変数（要保存）####################

        # level
        self.level = 1
        self.current_xp = 0
        self.count_time = 0

        # states
        self.rarity = "common"
        self.flower_color = ""
        self.states_bonus = {"max_hp": 0,"STR": 0,"DEX": 0, "INT": 0, "defense": 0, "evasion": 0, "attack_speed":0}
        self.skill_bonus = {}
        self.resist_bonus = {"physical": 0, "fire": 0, "ice": 0, "lightning":0, "acid": 0, "poison": 0, "mind": 0}

        ###################################




    def get_dict(self):
        result = {}
        result["level"] = self.level
        result["current_xp"] = self.current_xp
        result["skill_count_time"] = self.flower_skill.count_time
        result["skill_during_cool_down"] = self.flower_skill.during_cool_down


        result["states_bonus"] = self.states_bonus
        result["skill_bonus"] = self.skill_bonus
        result["resist_bonus"] = self.resist_bonus
        return result

    def restore_from_dict(self, result):
        self.level = result["level"]
        self.current_xp = result["current_xp"]
        self.flower_skill.count_time = result["skill_count_time"]
        self.flower_skill.during_cool_down = result["skill_during_cool_down"]

        self.states_bonus = result["states_bonus"]
        self.skill_bonus = result["skill_bonus"]
        self.resist_bonus = result["resist_bonus"]



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

