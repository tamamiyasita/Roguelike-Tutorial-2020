from actor.skills.bamboo_blade import BambooBlade
from actor.items.base_flower import BaseFlower
from actor.skills.bamboo_blade import BambooBlade


class Bambooflower(BaseFlower):
    def __init__(self, x=0, y=0, name="bambooflower"):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y,
        )
        
        skill_component = BambooBlade()

        # 定数 #############################
        self.explanatory_text = f"Is Bamboo \n st"

        self.my_speed = 4.0
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0


        self.flower_color = "white"
        self.states_bonus =  {"max_hp": 0, "STR": 1, "DEX": 0, "INT": 0, "defense": 0, "evasion": 0, "speed":0}
        self.skill_bonus = {"bamboo_blade":1}
        self.resist_bonus = {"physical": 0, "fire": 1, "ice": 0, "elec":0, "acid": 0, "poison": 0, "mind": 0}



