from actor.items.base_flower import BaseFlower
from actor.skills.grass_cutter import GrassCutter

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
        self.level_up_weights = [3, 5, 2]
        self.explanatory_text = f"Is silvergrass \n st"
        self.item_margin_x = 17
        self.item_margin_y = 6
        self.my_speed = 4.3
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0

        self.flower_color = "white"
        self.states_bonus =  {"max_hp": 0,"STR": 0,"DEX": 1, "INT": 0, "defense": 0, "evasion": 0, "attack_speed":0}
        self.skill_bonus = {"grass_cutter":1}

        self.resist_bonus = {"physical": 0, "fire": 0, "ice": 0, "lightning":0, "acid": 0, "poison": 0, "mind": 0}






