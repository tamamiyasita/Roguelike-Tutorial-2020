from constants import *


class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.owner = None

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
