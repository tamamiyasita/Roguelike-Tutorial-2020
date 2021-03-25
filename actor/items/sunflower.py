from actor.items.base_flower import BaseFlower
from actor.skills.seed_shot import SeedShot

class Sunflower(BaseFlower):
    def __init__(self, x=0, y=0, image="sunflower"):
        super().__init__(
            image=image,
            x=x,
            y=y,
        )
        skill_component = SeedShot()
        # 定数 #############################
        self.scale = 1.6
        self.level_up_weights = [3, 5, 2]
        self.explanatory_text = f"Is sunflower \n st"
        self.item_margin_x = 17
        self.item_margin_y = 6
        self.my_speed = 2.3
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################


        # 変数（要保存）####################

        # level
        self.level = 1
        self.current_xp = 0
        
        # states
        self.states_bonus = {"DEX": 1}
        self.skill_bonus = {"seed_shot":1}
        self.resist_bonus = {"fire":1}


        ###################################






        



