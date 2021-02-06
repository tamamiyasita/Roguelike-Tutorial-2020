
from actor.items.cirsium import Cirsium


class Paeonia(Cirsium):
    def __init__(self, x=0, y=0, name="paeonia"):
        super().__init__(
            name=name,
            x=x,
            y=y,         
        )

        # # template
        # self.slot = "flower"
        # self.tag = [Tag.item, Tag.equip, Tag.flower]
        # self.current_xp = 0

        # # level
        # self.level = 1
        # self.max_level = 5
        # self.experience_per_level = exp_calc()
        self.level_up_weights = [3, 2, 5]

        # states
        self.states_bonus = {"INT": 1}
        self.skill_generate = "healing"
        self.skill_add = {"healing":1}
        self.data = {2:"p_grenade", 3:"healing"}


        # position
        self.item_margin_x = 17
        self.item_margin_y = -3
        self.my_speed = 3.3
        self.scale = 0.7


        self.explanatory_text = f"Is paeonia $#############4TEst test test \n test$#4444444444testtest"

















