import arcade
from data import IMAGE_ID
from actor.flowers.base_flower import BaseFlower
from actor.skills.seed_shot import SeedShot

class Sunflower(BaseFlower):
    def __init__(self, x=0, y=0, name="sunflower"):
        super().__init__(
            name=name,
            image=IMAGE_ID[name],
            x=x,
            y=y,
        )

        skill_component = SeedShot()

        # 定数 #############################
        self.scale = 1.6
        self.explanatory_text = f"Is sunflower \n st"

        self.my_speed = 2.3
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0
        
        self.flower_color = arcade.color.GOLDEN_YELLOW

        self.states_bonus =  {"max_hp": 0, "STR": 0, "DEX": 1, "INT": 0, "defense": 0, "evasion": 0, "speed":0}
        self.skill_bonus = {"seed_shot":1}
        self.resist_bonus = {"physical": 0, "fire": 1, "ice": 0, "elec":0, "acid": 0, "poison": 0, "mind": 0}




        


