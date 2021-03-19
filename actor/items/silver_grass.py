from actor.items.base_flower import BaseFlower
from actor.skills.grass_cutter import GrassCutter

class SilverGrass(BaseFlower):
    def __init__(self, x=0, y=0, name="silver_grass"):
        super().__init__(
            name=name,
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

        self.color = "white"
        self.states_bonus = {"DEX": 1}
        self.skill_bonus = {"grass_cutter":1}
        self.description={"complexion":0, "fragrance":0, "brilliant":0, "thorns":1, "hardness":0, "supple":1},

        self.resist_bonus = {}






