from actor.states.poison_status import PoisonStatus
import random
from constants import *
from util import dice, stop_watch, result_add
from actor.actor_set import *
from collections import Counter
import math
from actor.skills.base_skill import BaseSkill
from hit_anime import hit_particle, Hit_Anime


class Fighter:
    def __init__(self, hp=0, defense=0, STR=0, DEX=0, INT=0, attack_speed=DEFAULT_ATTACK_SPEED,
                 evasion=0, xp_reward=0, level=1,
                 # 物理:オレンジ, 火:赤, 氷:白, 雷:青, 酸:黄色, 毒:紫, 精神:ピンク
                 resist={"physical": 1, "fire": 0, "ice": 1, "lightning":1, "acid": 1, "poison": 1, "mind": 1},           
                 ability_points=0):

        self.hp = hp
        self.max_hp = self.hp

        self.STR = STR
        self.DEX = DEX
        self.INT = INT

        self.defense = defense
        self.evasion = evasion
        self.attack_speed = attack_speed
        self.resist = resist

        self.owner = None
        self.xp_reward = xp_reward
        self.level = level
        self._states = []

        self._skill_list = arcade.SpriteList()

        # TODO バフデバフ効果に使う辞書　effect_bonus_update関数を作らねば
        self.effect_bonus = {"max_hp": 0, "max_mp": 0, "STR": 0,
                 "DEX": 0, "INT": 0, "defense": 0, "evasion": 0}


    def get_dict(self):
        # pass
        result = {}

        # result["hp"] = self.hp
        # result["max_hp"] = self.base_max_hp

        # result["strength"] = self.base_strength
        # result["dexterity"] = self.base_dexterity
        # result["intelligence"] = self.base_intelligence

        # result["defense"] = self.base_defense
        # result["evasion"] = self.base_evasion
        # result["attack_speed"] = self.attack_speed

        # result["xp_reward"] = self.xp_reward
        # result["current_xp"] = self.current_xp
        # result["level"] = self.level
        # result["ability_points"] = self.ability_points
        # result["level_skills"] = self.level_skills

        # result["base_skill_dict"] = {name : result.get_dict() for name, result in  self.base_skill_dict.items()}

        # クラスと内部値をタプルで保存する
        result["states"] = [(states.__class__.__name__, result.get_dict()) for states, result in zip(self.states, self.states)]

        return result

    def restore_from_dict(self, result):
        # pass

        # self.hp = result["hp"]
        # self.base_max_hp = result["max_hp"]
 
        # self.base_strength = result["strength"]
        # self.base_dexterity = result["dexterity"]
        # self.base_intelligence = result["intelligence"]

        # self.base_defense = result["defense"]
        # self.base_evasion = result["evasion"]
        # self.attack_speed = result["attack_speed"]

        # self.xp_reward = result["xp_reward"]
        # self.current_xp = result["current_xp"]
        # self.level = result["level"]
        # self.ability_points = result["ability_points"]
        # self.level_skills = result["level_skills"]

        # クラスと内部値を結合する
        for s, r in result["states"]:
            if s:
                print(s, r)
                sd = eval(s)()
                sd.restore_from_dict(r)
                self._states.append(sd)

        # for s, r in result["base_skill_dict"].items():
        #     if s:
        #         print(s, r)
        #         sd = self.base_skill_dict[s]
        #         sd.restore_from_dict(r)
        #         print(sd)
    @property
    def unarmed(self):
        return self.owner.unarmed


    @property
    def passive_skill(self):
        result =  [skill for skill in self.skill_list if Tag.passive in skill.tag]
        return result
    @property
    def active_skill(self):
        result =  [skill for skill in self.skill_list if Tag.active in skill.tag]
        return result
    @property
    def counter_skill(self):
        result = [skill for skill in self.skill_list if Tag.counter in skill.tag]
        if not result:
            return []
        return result
    @property
    def attack_skill(self):
        try:
            result =  [skill for skill in self.skill_list if Tag.weapon in skill.tag]
            if not result:
                result = [self.unarmed]
        except:
            result = [self.unarmed]
        return result


    @property
    def skill_list(self):
        for skill in self._skill_list:
            if skill and not isinstance(skill, str):
                skill.owner = self.owner

        return self._skill_list

    @property
    def states(self):
        result = []
        for states in self._states:
            if states and not isinstance(states, str):
                states.owner = self.owner
            if states.count_time > 0:
                result.append(states)
            else:
                states.remove_from_sprite_lists()

        self._states = result

        return self._states
    




    def effect_hit_chance(self, effect):
        resist = self.resist.get(effect.attr)
        if resist:
            hit_chance = 100/resist
            resist_chance = random.randrange(1, 99)
            print(f"{resist_chance=} < {hit_chance=} ")
            if  resist_chance < hit_chance:
                self.states.append(effect)
                print(f"success hit {effect=}")
            if Tag.used in effect.tag:
                effect.use(self.owner)# 即時効果
                # self.owner.name is {effect.name} rd
        else:
            self.states.append(effect)



    def skill_process(self, skill):
        
        message = ""
        results = []
        owner_name = self.owner.name.capitalize()
        skill_name = skill.name

        level = skill.level
        damage = skill.damage
        attr = skill.attr
        hit_rate = skill.hit_rate

        # damage = dice(level, damage)

        # HP回復
        if attr == "recovery":
            results.append({"damage_pop": self.owner, "damage": damage, "message": f"has recovered {damage}HP"})
            self.hp += damage
            # 超過処理
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            return results

        if Tag.counter not in skill.tag or Tag.range_attack not in skill.tag or Tag.shot not in skill.tag:# カウンタースキルにはカウンターチェックしない
            results.extend(self.other_counter_check(skill.owner))
            if skill.owner.fighter.hp < 1 or skill.owner.state == state.STUN:
                return results

        

        # (命中率)％ ＝（α／１００）＊（１ー （β ／ １００））＊ １００
        # 命中率（α）＝９５、回避率（β）＝５
        if self.owner.state != state.STUN and Tag.player in self.owner.tag:
            self.owner.form = form.DEFENSE
        if hit_rate:
            hit_chance = ((hit_rate-self.DEX+skill.owner.fighter.DEX) / 100) * (1 - (self.evasion / 100)) * 100
            if random.randrange(1, 100) <= hit_chance:
                # ヒット 
                message = f"Hit"
                hit_particle(target=self.owner)


                # critical_flag:
                if random.randrange(1, (100+self.DEX)) < 3+skill.owner.fighter.DEX:
                    damage = skill.damage * 2
                    message += " CRITICAL!"

                # 物理防御処理
                elif attr == "physical":
                    defens_p = self.level // 3
                    damage = damage - dice(defens_p, defens_p+self.defense, self.owner.fighter.level)

            else:
                # 回避
                results.append({"damage_pop": self.owner, "damage": "MISS"})
                results.append({"message": f"{owner_name} Avoided {skill_name}"})
                return results


        if self.resist[attr] <= 0:
            damage *= 2.5# 弱点ダメージ
        else:
            damage = damage / self.resist[attr]


        # 完全防御
        if damage < 1:
            message += f" But {owner_name} was undamaged."
            results.extend([{"message": message},{"damage_pop": self.owner, "damage": "Guard!"}])
            return results

        
        elif damage >= 1:
            if skill.anime and Tag.range_attack not in skill.tag:
                Hit_Anime(skill, self.owner)
            message += f" {owner_name} took {int(damage)} damage! from {skill_name}"
            results.append({"message": message})

            damage = int(damage)

            results.extend(self.change_hp(damage))

            if skill.effect:
                self.effect_hit_chance(skill.effect)

        return results

    def change_hp(self, damage):
        results = []

        self.hp -= damage

        # 死亡処理
        if self.hp <= 0 and self.owner.is_dead == False:
            self.owner.is_dead = True
            self.owner.blocks = False
            results.append({"dead": self.owner})

            print(f"{self.owner.name} is dead x!")

        results.append({"damage_pop": self.owner, "damage": -damage})

        return results

    @stop_watch
    def attack(self, target):
        """ここはダンプアタックを処理する
            attack_skillをループしskill_process関数に渡す"""
        results = []

        results.append({"message": f"{self.owner.name.capitalize()} attacked {target.name}"})
        for skill in self.attack_skill:

                results.extend(target.fighter.skill_process(skill))

        return results

    def other_counter_check(self, target):
        result = []            
        for c in self.counter_skill:
            result = c.use(target)

        return result
