from actor.items.base_flower import BaseFlower


class Pineapple(BaseFlower):
    def __init__(self, x=0, y=0, name="pineapple"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        # template
        # self.slot = "flower"
        # self.tag = [Tag.item, Tag.equip, Tag.flower]
        # self.current_xp = 0
        self.scale = 2


        # # level
        # self.level = 1
        # self.max_level = 5
        # self.experience_per_level = exp_calc()
        self.level_up_weights = [2, 3, 5]

        # states
        self.states_bonus = {"INT": 1}
        self.skill_generate = "p_grenade"
        self.skill_add = {"p_grenade":1}
        self.data = {2:"p_grenade", 3:"healing"}
        

        # position
        self.item_margin_x = 19
        self.item_margin_y = 11
        self.my_speed = 4.0


        self.explanatory_text = f"Is pineapple \n and pineapple"
