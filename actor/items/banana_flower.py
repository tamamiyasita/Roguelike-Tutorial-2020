from actor.items.base_flower import BaseFlower
from actor.skills.banana_slip import BananaSlip

class Bananaflower(BaseFlower):
    def __init__(self, x=0, y=0, name="bananaflower"):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y,
        )
        skill_component = BananaSlip()
        # 定数 #############################
        # self.scale = 1.6
        self.level_up_weights = [3, 5, 2]
        self.explanatory_text = f"Is bananalower \n st"
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
        self.skill_bonus = {"banana_slip":1}
        self.resist_bonus = {"fire":1}


        ###################################


