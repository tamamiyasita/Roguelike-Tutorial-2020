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
        self.explanatory_text = f"Is silvergrass \n st"

        self.my_speed = 4.3
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0

        self.flower_color = "white"
        self.states_bonus =  {"max_hp": 1,"STR": 1,"DEX": 1, "INT": 1, "defense": 1, "evasion": 1, "move_speed":1, "attack_speed":1}
        self.skill_bonus = {"grass_cutter":1}
        self.resist_bonus = {"physical": 1, "fire": 1, "ice": 1, "lightning":1, "acid": 1, "poison": 1, "mind": 1}






