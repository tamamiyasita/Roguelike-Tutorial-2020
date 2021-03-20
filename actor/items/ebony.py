from actor.items.base_flower import BaseFlower
from actor.skills.branch_baton import BranchBaton


class Ebony(BaseFlower):
    def __init__(self, x=0, y=0, name="ebony"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        skill_component = BranchBaton()

        # 定数 #############################
        self.level_up_weights = [5, 3, 2]
        self.explanatory_text = f"Is Ebony \n st"
        self.item_margin_x = 19
        self.item_margin_y = 11
        self.my_speed = 4.0
        self.flower_skill = skill_component
        self.flower_skill.flower = self
        ###################################

        self.level = 1
        self.current_xp = 0


        self.states_bonus = {"STR": 1}
        self.skill_bonus = {"branch_baton":1}
        self.resist_bonus = {}
        self.description={"brilliant":0, "glow":0, "fragrance":0, "sharp":0, "robust":0, "supple":0, "medicinal":0},


