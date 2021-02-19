from actor.items.base_flower import BaseFlower
from actor.skills.poison_dart import PoisonDart

class Aconite(BaseFlower):
    def __init__(self, x=0, y=0, name="aconite"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        skill_component = PoisonDart()

        # 定数 #############################
        self.level_up_weights = [3, 5, 2]
        self.explanatory_text = f"Is aconite \n st"
        self.item_margin_x = 17
        self.item_margin_y = 6
        self.my_speed = 2.7
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0


        self.states_bonus = {"DEX": 1}
        self.skill_bonus = {"poison_dart":1}
        self.resist_bonus = {"poison":1}







        