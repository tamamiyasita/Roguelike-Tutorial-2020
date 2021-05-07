import arcade
from constants import *
import random
from actor.flowers.base_flower import BaseFlower
from actor.skills.grass_cutter import GrassCutter
from arcade.experimental.lights import Light

class SilverGrass(BaseFlower):
    def __init__(self, x=0, y=0, name="silver_grass"):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y,
        )


        skill_component = GrassCutter()

        # 定数 #############################
        self.explanatory_text = f"This flower will equip your tentacles with a mower.\nThis will give you extra damage when you hit an enemy. \nSince it's called a mower,\nI think it works well on grass-based enemies.\nUse it with safety first."

        self.my_speed = 4.3
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0

        self.states_bonus =  {"max_hp": 1,"STR": 1,"DEX": 1, "INT": 1, "defense": 1, "evasion": 1, "speed":1}
        self.skill_bonus = {"grass_cutter":1}
        self.resist_bonus = {"physical": 1, "fire": 1, "ice": 1, "elec":1, "acid": 1, "poison": 1, "mind": 1}

        self.flower_color = arcade.color.SILVER
        # self.light = Light(0, 0, radius=self.texture.width/3, color=self.flower_color, mode="soft")
        # self.a_time = 0

    # def update_animation(self, delta_time):
    #     super().update_animation(delta_time)
    #     self.a_time +=1
    #     if self.a_time < 70:
    #         self.light.radius += delta_time*random.uniform(1.2, 4.6)
    #     elif self.a_time < 140:
    #         self.light.radius -= delta_time*random.uniform(1.2, 4.6)
    #     elif self.a_time < 210:
    #         self.a_time = 0
    #         self.light.radius =self.texture.width/3

    #     self.light.position = self.position







