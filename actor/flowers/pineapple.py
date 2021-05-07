import arcade
from actor.flowers.base_flower import BaseFlower
from actor.skills.p_grenade import P_Grenade
# from arcade.experimental.lights import Light


class Pineapple(BaseFlower):
    def __init__(self, x=0, y=0, name="pineapple"):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y,
        )
        skill_component = P_Grenade()

        # 定数 #############################
        self.explanatory_text = f"Is pineapple \n and pineapple"

        self.my_speed = 4.0
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0


        self.flower_color = arcade.color.ORANGE
        # self.light = Light(0, 0, radius=self.texture.width/3, color=self.flower_color, mode="soft")

        self.states_bonus =  {"max_hp": 3, "STR": 0, "DEX": 0, "INT": 0, "defense": 0, "evasion": 0, "speed":0}
        self.skill_bonus = {"p_grenade":1}
        self.resist_bonus = {"physical": 0, "fire": 0, "ice": 0, "elec":0, "acid": 0, "poison": 0, "mind": 0}

