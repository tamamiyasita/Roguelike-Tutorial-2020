from constants import *
from util import exp_calc
from random import choices, randint


def check_experience_level(player, game_engine):


    xp_to_next_level = player.experience_per_level[player.fighter.level+1]
    flower_level = check_flower_level(player)
    
    if player.fighter.current_xp >= xp_to_next_level:
        player.fighter.level += 1
        player.fighter.ability_points += 1
        game_engine.action_queue.extend([{"message": "Level up!!!"}])
        game_engine.game_state = GAME_STATE.LEVEL_UP_WINDOW
    # 花のレベルアップUI作成

    elif flower_level:
        game_engine.game_state = GAME_STATE.LEVEL_UP_FLOWER
    
    else:
        game_engine.game_state = GAME_STATE.NORMAL



    
    


def check_flower_level(player):
    result = []
    for flower in player.equipment.flower_slot:
        xp_to_next_level = flower.experience_per_level[flower.level+1]
        if flower.current_xp >= xp_to_next_level and flower.max_level >= flower.level:
            result.append(flower)

    return result


class FlowerLevelUp:
    def __init__(self, flower):
        rarity_point = {"common":3, "uncomon":5, "rare":7}
        self.flower = flower
        self.point = rarity_point[self.flower.rarity]

    def point_set(self):
        for _ in range(self.point):
            p = randint(1, 6)
            if p == 6:
                self.resist_bonus = {}

        self.flower.states_bonus 
