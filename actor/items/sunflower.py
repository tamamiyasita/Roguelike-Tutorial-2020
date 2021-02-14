from actor.items.base_flower import BaseFlower


class Sunflower(BaseFlower):
    def __init__(self, x=0, y=0, name="sunflower"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        self.scale = 1.6



        self.level_up_weights = [3, 5, 2]


        self.states_bonus = {"DEX": 1}
        self.skill_generate = "poison_dart"
        self.skill_add = {"poison_dart":1}
        self.data = {2:"p_grenade", 3:"healing"}


        self.item_margin_x = 17
        self.item_margin_y = 6
        self.my_speed = 2.3

        self.explanatory_text = f"Is sunflower \n st"




        



