from actor.items.cirsium import Cirsium



class Ebony(Cirsium):
    def __init__(self, x=0, y=0, name="ebony"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        # template
        # self.slot = "flower"
        # self.tag = [Tag.item, Tag.equip, Tag.flower]
        # self.current_xp = 0


        # # level
        # self.level = 1
        # self.max_level = 5
        # self.experience_per_level = exp_calc()
        self.level_up_weights = [5, 3, 2]

        # states
        self.states_bonus = {"STR": 1}
        self.skill_add = {"branch_baton":1}
        self.data = {2:"branch_baton", 3:"healing"}
        

        # position
        self.item_margin_x = 19
        self.item_margin_y = 11
        self.my_speed = 4.0


        self.explanatory_text = f"Is Ebony $#############4TEst test test \n test$#4444444444testtest"
