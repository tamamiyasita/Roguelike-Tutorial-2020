from actor.items.cirsium import Cirsium


class Sunflower(Cirsium):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="sunflower",
            x=x,
            y=y,
        )
        self.scale = 1.6



        self.level_up_weights = [3, 5, 2]


        self.states_bonus = {"DEX": 1}
        self.skill_add = {"seed_shot":1}

        self.item_margin_x = 17
        self.item_margin_y = 6
        self.my_speed = 2.3

        self.explanatory_text = f"Is sunflower \n st"




        



