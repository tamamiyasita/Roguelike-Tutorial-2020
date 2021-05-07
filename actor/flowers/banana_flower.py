import arcade
from data import IMAGE_ID
from actor.flowers.base_flower import BaseFlower
from actor.skills.banana_slip import BananaSlip

class Bananaflower(BaseFlower):
    def __init__(self, x=0, y=0, name="bananaflower"):
        super().__init__(
            name=name,
            image=IMAGE_ID[name],
            x=x,
            y=y,
        )

        skill_component = BananaSlip()
        
        # 定数 #############################
        # self.scale = 1.6
        self.explanatory_text = f"Is bananalower \n st"

        self.my_speed = 2.3
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0
        
        self.flower_color = arcade.color.YELLOW
        self.states_bonus =  {"max_hp": 2,"STR": 0,"DEX": 0, "INT": 0, "defense": 0, "evasion": 0, "speed":0}
        self.skill_bonus = {"banana_slip":1}
        self.resist_bonus = {"physical": 0, "fire": 0, "ice": 0, "elec":0, "acid": 0, "poison": 0, "mind": 0}



        ###################################


