
from actor.items.base_flower import BaseFlower
from actor.skills.healing import Healing
from data import *

class Paeonia(BaseFlower):
    def __init__(self, x=0, y=0, name="paeonia"):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y,         
        )
  
        skill_component = Healing()

        # 定数 #############################
        self.explanatory_text = f"Is paeonia  \ntest"

        self.my_speed = 3.3
        self.scale = 1.2
        self.flower_skill = skill_component
        self.flower_skill.flower = self

        ###################################

        self.level = 1
        self.current_xp = 0

        self.flower_color = "pink"
        self.states_bonus =  {"max_hp": 0,"STR": 0,"DEX": 0, "INT": 1, "defense": 0, "evasion": 0, "speed":0}
        self.skill_bonus = {"healing":1}
        self.resist_bonus = {"physical": 0, "fire": 0, "ice": 0, "elec":0, "acid": 0, "poison": 1, "mind": 0}






















