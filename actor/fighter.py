import random
from constants import *
from util import dice, stop_watch
from anime.hit_anime import hit_particle, Hit_Anime


class Fighter:
    def __init__(self, hp=0, defense=0, STR=0, DEX=0, INT=0, speed=10,
                 evasion=0, xp_reward=0, level=1,
                 # 物理:オレンジ, 火:赤, 氷:白, 雷:青, 酸:黄色, 毒:紫, 精神:ピンク
                 resist={"physical": 1, "fire": 1, "ice": 1, "elec":1, "acid": 1, "poison": 1, "mind": 1},
                 skill_list=None,           
                 ability_points=0):

        self.hp = hp
        self.max_hp = self.hp

        self.STR = STR
        self.DEX = DEX
        self.INT = INT

        self.defense = defense
        self.evasion = evasion
        self.speed = speed
        self.wait = 0

        self.resist = resist

        self.owner = None
        self.xp_reward = xp_reward
        self.level = level
        self._states = []

        self._skill_list = skill_list

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
        # result["speed"] = self.speed

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
        # self.speed = result["speed"]

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
        if self.skill_list:
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
        if self._skill_list:
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
    




    def effect_hit_chance(self, effect, target):
        # skillの追加効果
        resist = target.fighter.resist.get(effect.attr)
        if resist:
            hit_chance = 100/resist
            resist_chance = random.randrange(1, 99)
            print(f"{resist_chance=} < {hit_chance=} ")
            if  resist_chance < hit_chance:
                target.fighter.states.append(effect)
                print(f"success hit {effect=}")
            if Tag.used in effect.tag:
                effect.use(target)# 即時効果
                # self.owner.name is {effect.name} rd
        else:
            target.fighter.states.append(effect)

    def recovery_process(self, skill):
        results = []

        damage = skill.damage
        attr = skill.attr
        # HP回復
        if attr == "recovery":
            damage = int(damage)
            results.append({"damage_pop": self.owner, "damage": damage, "message": f"has recovered {damage}HP"})
            self.hp += damage
            # 超過処理
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            return results




    def skill_process(self, skill):
        
        owner = skill.owner
        target = self.owner

        message = ""
        results = []
        target_name = target.name.capitalize()
        skill_name = skill.name

        damage = skill.damage
        attr = skill.attr
        hit_rate = skill.hit_rate


        # カウンターチェック
        check = self.other_counter_check(skill, owner, target)
        if check:
            results.extend(check)
            # death chaeck
            if target.fighter.hp < 1 or target.state == state.TURN_END:
                return results


        

        # (命中率)％ ＝（α／１００）＊（１ー （β ／ １００））＊ １００
        # 命中率（α）＝９５、回避率（β）＝５
        if target.state != state.STUN and Tag.player in target.tag:
            target.form = form.DEFENSE
        if hit_rate:
            hit_chance = ((hit_rate-self.DEX+owner.fighter.DEX) / 100) * (1 - (self.evasion / 100)) * 100
            if random.randrange(1, 100) <= hit_chance:
                # ヒット 
                message = f"Hit"
                hit_particle(target=target)


                # critical_flag:
                if random.randrange(1, (100+target.fighter.DEX)) < 3+owner.fighter.DEX:
                    damage = skill.damage * 2
                    message += " CRITICAL!"

                # 物理防御処理
                elif attr == "physical":
                    defens_p = target.fighter.level // 3
                    damage = damage - dice(defens_p, defens_p+target.fighter.defense, target.fighter.level)

            else:
                # 回避
                results.append({"damage_pop": target, "damage": "MISS"})
                results.append({"message": f"{target_name} Avoided {skill_name}"})
                return results






        if target.fighter.resist[attr] <= 0:
            damage *= 2.5# 弱点ダメージ
        else:
            damage = damage / target.fighter.resist[attr]


        # 完全防御
        if damage < 1:
            message += f" But {target_name} was undamaged."
            results.extend([{"message": message},{"damage_pop": target, "damage": "Guard!"}])
            return results

        
        elif damage >= 1:
            if skill.anime and Tag.range_attack not in skill.tag:
                Hit_Anime(skill, target)
            message += f" {target_name} took {int(damage)} damage!"
            results.append({"message": f"from {skill_name}"})
            results.append({"message": message})

            damage = int(damage)

            results.extend(target.fighter.change_hp(damage, target))

            if skill.effect:
                owner.fighter.effect_hit_chance(skill.effect, target)

        return results

    def change_hp(self, damage, target):
        results = []

        target.fighter.hp -= damage

        # 死亡処理
        if target.fighter.hp <= 0 and target.is_dead == False:
            target.is_dead = True
            target.blocks = False
            results.append({"dead": target})

            print(f"{target.name} is dead x!")

        results.append({"damage_pop": target, "damage": -damage})

        return results

    @stop_watch
    def attack(self, target):
        """ここはダンプアタックを処理する
            attack_skillをループしskill_process関数に渡す"""
        results = []
        owner = self.owner

        results.append({"message": f"{owner.name.capitalize()} attacked {target.name}"})
        for skill in self.attack_skill:

                results.extend(target.fighter.skill_process(skill))

        return results

    def other_counter_check(self, skill, owner, target):
        # カウンターチェック
        result = []            

        if Tag.counter not in skill.tag and Tag.range_attack not in skill.tag and Tag.shot not in skill.tag:# カウンタースキルにはカウンターチェックしない

            if target.fighter.skill_list:
                for counter in target.fighter.counter_skill:
                    result = counter.use(owner)

                return result
