import arcade
from actor.items.base_flower import BaseFlower
from actor.skills.seed_shot import SeedShot


class Cabbageflower(BaseFlower):
    # cabbageflower = arcade.load_texture(r"image\cabbage_flower.png")
    def __init__(self, x=0, y=0, name="cabbageflower"):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y,
        )

        skill_component = SeedShot()

        # 定数 #############################
        self.scale = 1.6
        self.explanatory_text = f"Is cabbageflower \n st"

        self.my_speed = 2.3
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0
        
        self.flower_color = "yellow"
        self.states_bonus =  {"max_hp": 0, "STR": 0, "DEX": 1, "INT": 0, "defense": 0, "evasion": 0, "speed":0}
        self.skill_bonus = {"seed_shot":1}
        self.resist_bonus = {"physical": 0, "fire": 1, "ice": 0, "elec":0, "acid": 0, "poison": 0, "mind": 0}

