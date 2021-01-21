from constants import *
from util import exp_calc
from random import choices


def check_experience_level(player, game_engine):

    xp_to_next_level = player.experience_per_level[player.fighter.level+1]
    if player.fighter.current_xp >= xp_to_next_level:
        player.fighter.level += 1
        player.fighter.ability_points += 1
        game_engine.action_queue.extend([{"message": "Level up!!!"}])
        game_engine.game_state = GAME_STATE.LEVEL_UP_WINDOW

def check_flower_level(player):
    result = []
    for flower in player.equipment.item_slot:
        xp_to_next_level = flower.experience_per_level[flower.level+1]
        if flower.current_xp >= xp_to_next_level and flower.max_level >= flower.level:
            result.append(flower)

    return result


def level_up(flower, weights):
    select = ["STR", "DEX", "INT"]
    bonus = choices(select, weights=weights)
    flower.states_bonus.setdefault(bonus[0], 0)
    flower.states_bonus[bonus[0]] += 1

    return bonus