import arcade


class PoisonStatus:
    def __init__(self, owner=None, power=None, effect_time=None):
        self.owner = owner
        self.power = power
        self.effect_time = effect_time

    def apply(self):
        if 0 < self.effect_time:
            result = self.owner.fighter.change_hp(-self.power)
            
            self.owner.color = arcade.color.GREEN

            return [{"apply":self.owner}, {"message":f"You took {self.power} damage from poison"}, *result]

    def call_off(self):
        self.owner.color = arcade.color.WHITE
        return [{"message":f"The poison has disappeared from your body"}]

    def get_dict(self):
        result = {}

        result["owner"] = self.owner
        result["power"] = self.power
        result["effect_time"] = self.effect_time

        return result

    def restore_from_dict(self, result):
        self.owner = result["owner"]
        self.power = result["power"]
        self.effect_time = result["effect_time"]


