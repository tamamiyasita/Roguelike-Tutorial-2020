from actor.items.base_flower import BaseFlower
from actor.skills.p_grenade import P_Grenade

class Pineapple(BaseFlower):
    def __init__(self, x=0, y=0, name="pineapple"):
        super().__init__(
            name=name,
            image=name,
            x=x,
            y=y,
        )
        skill_component = P_Grenade()

        # 定数 #############################
        self.scale = 2
        self.level_up_weights = [2, 3, 5]
        self.explanatory_text = f"Is pineapple \n and pineapple"
        self.item_margin_x = 19
        self.item_margin_y = 11
        self.my_speed = 4.0
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0


        self.states_bonus = {"INT": 1}
        self.skill_bonus = {"p_grenade":1}
        self.resist_bonus = {"fire":1}

