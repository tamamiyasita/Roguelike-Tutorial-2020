from actor.states.poison_status import PoisonStatus
import random
from constants import *
from util import dice, stop_watch
from actor.actor_set import *


class Fighter:
    def __init__(self, hp=0, mp=0, defense=0, STR=0, DEX=0, INT=0, unarmed_attack=(1, 1, 1), attack_speed=DEFAULT_ATTACK_SPEED,
                 evasion=0, hit_rate=100, xp_reward=0, current_xp=0, level=1, ability_points=0):
        self.hp = hp
        self.base_max_hp = self.hp
        self.mp = mp
        self.base_max_mp = self.mp

        self.base_strength = STR
        self.base_dexterity = DEX
        self.base_intelligence = INT

        self.unarmed_attack = unarmed_attack
        self.base_defense = defense
        self.base_evasion = evasion
        self.hit_rate = hit_rate
        self._attack_speed = attack_speed
        self.weapon = None

        self.owner = None
        self.xp_reward = xp_reward
        self.current_xp = current_xp
        self.level = level
        self.ability_points = ability_points
        self._states = []

        self._skill_list = []

        self.damage = None

    def get_dict(self):
        result = {}

        result["hp"] = self.hp
        result["max_hp"] = self.base_max_hp

        result["strength"] = self.base_strength
        result["dexterity"] = self.base_dexterity
        result["intelligence"] = self.base_intelligence

        result["unarmed_attack"] = self.unarmed_attack
        result["defense"] = self.base_defense
        result["evasion"] = self.base_evasion
        result["hit_rate"] = self.hit_rate
        result["_attack_speed"] = self._attack_speed

        result["xp_reward"] = self.xp_reward
        result["current_xp"] = self.current_xp
        result["level"] = self.level
        result["ability_points"] = self.ability_points
        result["skill_list"] = [skill.__class__.__name__ for skill in self._skill_list]
        # result["passive_skill"] = [skill.__class__.__name__ for skill in self._skill_list if Tag.active not in skill.tag]
        # result["active_skill"] = [(skill.__class__.__name__, result.get_dict()) for skill, result in zip(self._skill_list, self._skill_list) if Tag.active in result.tag]

        # クラスと内部値をタプルで保存する
        result["states"] = [(states.__class__.__name__, result.get_dict()) for states, result in zip(self.states, self.states)]

        return result

    def restore_from_dict(self, result):

        self.hp = result["hp"]
        self.base_max_hp = result["max_hp"]
 
        self.base_strength = result["strength"]
        self.base_dexterity = result["dexterity"]
        self.base_intelligence = result["intelligence"]

        self.unarmed_attack = result["unarmed_attack"]
        self.base_defense = result["defense"]
        self.base_evasion = result["evasion"]
        self.hit_rate = result["hit_rate"]
        self._attack_speed = result["_attack_speed"]

        self.xp_reward = result["xp_reward"]
        self.current_xp = result["current_xp"]
        self.level = result["level"]
        self.ability_points = result["ability_points"]
        self._skill_list = [eval(skill)() for skill in result["skill_list"]]
        # self._skill_list = [eval(skill)() for skill in result["passive_skill"]]
        # for i, c in result["active_skill"]:
        #     if i:
        #         print(i, c, "active_skill")
        #         ps = eval(i)()
        #         ps.restore_from_dict(c)
        #         self._skill_list.append(ps)

        # クラスと内部値を結合する
        for s, r in result["states"]:
            if s:
                print(s, r)
                sd = eval(s)()
                sd.restore_from_dict(r)
                self._states.append(sd)

    @property
    def skill_list(self):
        """skill listをループして花の追加skill levelをskill levelに加える"""
        for skill in self._skill_list:  # [LeafBlade()]が入る
            skill.owner = self.owner
            # if skill and not isinstance(skill, str) and self.owner.equipment is not None:
            #     skill.level = 0
            #     skill.level = self.owner.equipment.skill_level_sum.get(skill.name)
            #     if skill.level is None:
            #         skill.level = 0
           

        return self._skill_list

    @property
    def states(self):
        for states in self._states:
            if states and not isinstance(states, str):
                states.owner = self.owner

        return self._states
    
    
    @property
    def active_skill(self):
        return [skill for skill in self.skill_list if Tag.active in skill.tag and skill.actor_data["switch"] == True]

    @property
    def passive_skill(self):
        return [skill for skill in self.skill_list if Tag.passive in skill.tag]

                    


                 

    # skill level が1以上ならpassive skillを発動する
    # equipmentによって呼び出される
    # @property
    # def passive_skill(self):
    #     result = []
    #     for skill in self.skill_list:
    #         if Tag.passive in skill.tag:
    #             if 0 < skill.level:
    #                 skill.activate(self.owner)
    #             else:
    #                 skill.deactivate(self.owner)

    #             result.append(skill)

                 
    #     return result


            


    @property
    def equip_image(self):
        return [skill for skill in self.passive_skill if Tag.equip in skill.tag]



    @property
    def attack_speed(self):
        if self.weapon:
            return self.weapon.speed
        else:
            return self._attack_speed



    @property
    def max_hp(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["max_hp"]

        return self.base_max_hp + bonus

    @property
    def max_mp(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["max_mp"]

        return self.base_max_mp + bonus

    @property
    def STR(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["STR"]

        return self.base_strength + bonus

    @property
    def DEX(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["DEX"]

        return self.base_dexterity + bonus

    @property
    def INT(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["INT"]

        return self.base_intelligence + bonus

    @property
    def defense(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["defense"]

        return self.base_defense + bonus

    @property
    def evasion(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["evasion"]

        return self.base_evasion + bonus + (self.DEX / 2)
    

    @property
    def weapon_damage(self):

        
        if self.weapon:
            max_d = self.weapon.damage
            level = self.weapon.level
        else:
            max_d = self.owner.fighter.unarmed_attack
            level = self.level

        weapon_damage = dice(1 + level//3, max_d+(self.STR//3))

        return weapon_damage



    def hit_chance(self, target):
        # (命中率)％ ＝（α／１００）＊（１ー （β ／ １００））＊ １００
        # 命中率（α）＝９５、回避率（β）＝５
        hit = None

        if self.weapon:
            hit = self.weapon.hit_rate
        else:
            hit = self.owner.fighter.hit_rate


        hit_chance = ((hit+self.DEX) / 100) * \
            (1 - (target.fighter.evasion / 100)) * 100

        return hit_chance

    def change_hp(self, value):
        
        results = []

        self.hp += value

        if self.hp <= 0:#死亡
            self.owner.blocks = False
            self.owner.is_dead = True
            results.append({"dead": self.owner})
            print(f"{self.owner.name} is dead x!")

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        results.append({"damage_pop": self.owner, "damage": value})

        return results

    @stop_watch
    def attack(self, target, ranged=None):
        results = []

        if ranged:
            if random.randrange(1, 100) <= self.hit_chance(target):
                self.damage = dice(1 + ranged.level//3, ranged.damage+(self.DEX//3)) // target.fighter.defense
                if random.randrange(1, (100-self.DEX)) < 5:
                    self.damage *= 2
                    results.append({"message": f"{self.owner.name.capitalize()} attack is critical HIT!"})

        else:
            if random.randrange(1, 100) <= self.hit_chance(target):
                self.damage = self.weapon_damage // target.fighter.defense
                if random.randrange(1, (100-self.DEX)) < 5:
                    self.damage *= 2
                    results.append({"message": f"{self.owner.name.capitalize()} attack is critical HIT!"})


        if self.damage:
            if self.damage >= 0:
                # damage表示メッセージを格納する

                results.append(
                    {"message": f"{self.owner.name.capitalize()} attacks {target.name} for {str(self.damage)} hit points."})
                results.extend(target.fighter.change_hp(-self.damage))

                # # xp獲得処理
                # if target.is_dead:
                #     self.current_xp += target.fighter.xp_reward

            else:# 完全防御
                results.append(
                    {"message": f"{self.owner.name.capitalize()} attacks {target.name} but no self.damage"}
                )


        else:#回避
            results.append(
                {"message": f"{self.owner.name.capitalize()} attacks {target.name} Avoided"}
            )

        return results
