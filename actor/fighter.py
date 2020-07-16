from constants import *


class Fighter:
    def __init__(self, hp=0, defense=0, power=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.owner = None

    def get_dict(self):
        result = {}
        result["max_hp"] = self.max_hp
        result["hp"] = self.hp
        result["defense"] = self.defense
        result["power"] = self.power
        return result

    def restore_from_dict(self, result):
        self.max_hp = result["max_hp"]
        self.hp = result["hp"]
        self.defense = result["defense"]
        self.power = result["power"]

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({"dead": self.owner})
            print(f"{self.owner.name} is dead x!")

        return results

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append(
                {"message": f"{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points."})
            results.extend(target.fighter.take_damage(damage))

        else:
            results.append(
                {"message": f"{self.owner.name.capitalize()} attacks {target.name} but no damage"})

        return results
