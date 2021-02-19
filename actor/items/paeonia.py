
from actor.items.base_flower import BaseFlower
from actor.skills.healing import Healing

class Paeonia(BaseFlower):
    def __init__(self, x=0, y=0, name="paeonia"):
        super().__init__(
            name=name,
            x=x,
            y=y,         
        )
  
        skill_component = Healing()

        # 定数 #############################
        self.level_up_weights = [3, 2, 5]
        self.explanatory_text = f"Is paeonia  \ntest"
        self.item_margin_x = 17
        self.item_margin_y = -3
        self.my_speed = 3.3
        self.scale = 0.7
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0


        self.states_bonus = {"INT": 1}
        self.skill_bonus = {"healing":1}
        self.resist_bonus = {"poison":1}
























