from constants import *
from util import exp_calc
from random import choices, randint, choice


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
            # flower.level += 1
            result.append(flower)

    return result


class Select_param:
    def __init__(self, flower):
        """rarity値からlevel_pointを割り振る
        rare:1 = description, rare:2 = max_hp rare:3 = str.dex.int,
        rare:4 = eva.def, rare:5 = resist, rare:6 speed
        """
        rarity_point = {"common":3, "uncomon":5, "rare":7}
        self.flower = flower
        self.point = rarity_point[self.flower.rarity]
        self.up_state = ("description", "max_hp", "base_states", "high_states", "resist", "speed")
        if self.flower.rarity == "common":
            self.choice_pram = [5, 5, 5, 4, 2, 1]
        if self.flower.rarity == "uncommon":
            self.choice_pram = [10, 10, 5, 4, 2, 1]
        if self.flower.rarity == "rare":
            self.choice_pram = [1, 1, 1, 1, 1, 1]


    def point_set(self):
        result = {}
        for _ in range(self.point):
            param = choices(self.up_state, self.choice_pram)
            if "description" in param:
                choice_des =  choice(["complexion", "fragrance", "brilliant", "sharp", "robust", "supple"])
                self.flower.description[choice_des] += 1
                result[choice_des] = 1

            elif "max_hp" in param:
                get_hp = randint(4, 8) 
                self.flower.states_bonus["max_hp"] += get_hp
                result["max_hp"] = get_hp

            elif "base_states" in param:
                choice_base = choice(["STR", "DEX", "INT"])
                self.flower.states_bonus[choice_base] += 1
                result[choice_base] = 1

            elif "high_states" in param:
                choice_high = choice(["evasion", "defense"])
                self.flower.states_bonus[choice_high] += 1
                result[choice_high] = 1

            elif "resist" in param:
                choice_reg = choice(["fire", "ice", "lightning", "acid", "poison", "mind"])
                self.flower.resist_bonus[choice_reg] += 1
                result[choice_reg] = 1

            elif "speed" in param:
                self.flower.states_bonus["attack_speed"] += 1
                result["speed"] = 1

        return result



def random_flower_gen(flower, level_value):
    """mapに配置するitemのrandomstatesを決める"""
    for l in range(level_value):
        Select_param(flower).point_set()
    flower.level += level_value





