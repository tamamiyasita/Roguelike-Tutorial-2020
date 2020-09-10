import imp

import math
from actor.actor import Actor

class Fire:
    def __init__(self, engine):
        self.amm = None
        self.effect_sprites = engine.cur_level.effect_sprites
        self.actor_sprites = engine.cur_level.actor_sprites
        self.trigger = False

    # def update(self):
    #     if self.trigger:



    def shot(self, shooter):
        amm = shooter.equipment.item_slot["ranged_weapon"]
        target = None
        target_distance = None
        results = []

        if not amm:
            results.append({"message":f"You don't have a shooting weapon"})
            return results

        for actor in self.actor_sprites:
            if actor.is_visible and actor.fighter and not actor.is_dead and actor.ai:
                x1,y1 = shooter.x, shooter.y
                x2,y2 = actor.x, actor.y
                distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if target is None or distance < target_distance:
                    target = actor
                    target_distance = distance

        if target:
            damage = self.amm
            results.append({"message":f"{shooter.name} shot {target.name}"})
            results.extend(target.fighter.take_damage(damage))
            results.extend([{"turn_end": shooter}])

            return results
        
        else:
            results.extend([{"message": "not enemy"}])

        return results


            
